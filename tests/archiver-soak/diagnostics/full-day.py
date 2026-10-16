#!/usr/bin/env python3
"""Inspect completed full-day records with their frozen native readers."""

import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--chain', required=True, choices=('shortened', 'default'))
parser.add_argument('--input', type=Path, default=Path('/var/lib/etl-soak'))
parser.add_argument('--tools', type=Path, default=Path('/usr/local/share/etl-soak'))
args = parser.parse_args()
CHAIN = args.chain
OUT = args.input.resolve()
TOOLS = args.tools.resolve()
sys.path.insert(0, str(TOOLS))
import contract
import evidence
import evaluate

hashes = contract.verify_bundle(TOOLS)
terminal_hash = contract.digest(OUT / 'shutdown.json')
manifest_hash = contract.digest(OUT / 'observation.json')
terminal = json.loads((OUT / 'shutdown.json').read_text())
manifest = json.loads((OUT / 'observation.json').read_text())
assert manifest['configuration']['chain'] == CHAIN
assert terminal['terminal_kind'] == 'finish' and terminal['stop']['rc'] == 0
state = dict(line.split('=', 1) for line in subprocess.check_output(
    ['systemctl', 'show', 'epicsarchiverap-maven.service', '-p', 'MainPID', '-p', 'ActiveState', '-p', 'Result'],
    text=True).splitlines())
assert state['MainPID'] == '0' and state['ActiveState'] == 'inactive' and state['Result'] == 'success'
for unit in ('etl-soak-sample.timer', 'etl-soak-sample.service', 'etl-soak-finish.timer', 'etl-soak-finish.service'):
    values = dict(line.split('=', 1) for line in subprocess.check_output(
        ['systemctl', 'show', unit, '-p', 'MainPID', '-p', 'ActiveState'], text=True).splitlines())
    assert values.get('MainPID', '0' if unit.endswith('.timer') else None) == '0'
    assert values['ActiveState'] not in ('active', 'activating', 'deactivating')

actual = subprocess.run(['/usr/bin/python3', '-B', str(TOOLS / 'evaluate.py'), '--input', str(OUT)],
                        capture_output=True, timeout=180)
assert actual.returncode in (0, 1) and not actual.stderr
fresh = json.loads(actual.stdout)
result = {'chain': CHAIN, 'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'bundle_sha256': contract.digest(TOOLS / 'bundle.json'), 'tool_hashes': hashes,
          'original_terminal_sha256': terminal_hash, 'original_manifest_sha256': manifest_hash,
          'original_terminal_verdict': terminal['verdict'], 'original_evaluation': terminal['evaluation'],
          'late_native_evaluate_returncode': actual.returncode,
          'late_native_evaluate_stdout_sha256': hashlib.sha256(actual.stdout).hexdigest(),
          'late_native_evaluation': fresh,
          'window': {key: manifest[key] for key in ('started_at', 'earliest_finish_at', 'duration_seconds')},
          'terminal': {key: terminal.get(key) for key in
                       ('finish_started_at', 'finished_at', 'boot_unchanged', 'monotonic_elapsed_seconds',
                        'stop_elapsed_seconds', 'stop_timeout', 'errors')},
          'stop_rc': terminal['stop']['rc'], 'appliance_state': state,
          'abort_request_exists': (OUT / 'abort-request.json').exists()}
start = evidence.timestamp_ns(manifest['started_at'])
finish = evidence.timestamp_ns(terminal['finished_at'])
all_samples = sorted(((p, json.loads(p.read_text())) for p in (OUT / 'raw').glob('*/sample.json')),
                     key=lambda item: item[1]['observed_at'])
window = [(path, sample) for path, sample in all_samples
          if start <= evidence.timestamp_ns(sample['observed_at']) <= finish]
full = [(path, sample) for path, sample in window if sample.get('sample_kind') == 'full']
result['full_sample_count'] = len(full)
result['in_window_error_counts'] = dict(collections.Counter(error['check']
    for _, sample in full for error in sample['errors']))
result['failed_terminal_steps'] = {}
for label in terminal['errors']:
    value = terminal.get(label)
    if isinstance(value, dict):
        result['failed_terminal_steps'][label] = {key: value.get(key) for key in ('rc', 'error') if key in value}
        if value.get('message') == 'Required pass wait could not collect complete journals':
            result['failed_terminal_steps'][label]['cause'] = value['message']
        if 'stdout' in value:
            summary = json.loads(value['stdout'])
            matching = [sample for _, sample in window if sample['observed_at'] == summary.get('observed_at')]
            result['failed_terminal_steps'][label]['actual_sample_error_checks'] = [
                error['check'] for sample in matching for error in sample['errors']]
            result['failed_terminal_steps'][label]['actual_sample_found'] = len(matching) == 1

failures = [(index, path, sample) for index, (path, sample) in enumerate(all_samples)
            if any(error['check'] == 'kernel_journal' for error in sample['errors'])]
if failures:
    index, path, sample = failures[0]
    previous = all_samples[index - 1][1]
    query = path.parent / 'kernel-checkpoint-journal.jsonl'
    result['first_kernel_refusal'] = {
        'previous_successful_sample': previous['observed_at'], 'failed_sample': sample['observed_at'],
        'error': next(error['message'] for error in sample['errors'] if error['check'] == 'kernel_journal'),
        'failed_query_stdout_preserved': query.exists(),
        'failed_query_entry_count': len(query.read_text().splitlines()) if query.exists() else None}

invocation = dict(line.split('=', 1) for line in manifest['unit_before_observation'].splitlines()
                  if '=' in line)['InvocationID']
expected = {(row['transition'], row['cadence'], evidence.timestamp_ns(row['planned_at'])) for row in
            contract.expected_firings(datetime.datetime.fromisoformat(manifest['started_at']),
                                      datetime.datetime.fromisoformat(manifest['earliest_finish_at']),
                                      manifest['configuration'])}
passes = evaluate.pass_records(OUT / 'passes.jsonl')
counts = collections.Counter((row['transition'], row['cadence'], evidence.timestamp_ns(row['plannedAt']))
    for row in passes if row['invocation_id'] == invocation and start <= evidence.timestamp_ns(row['plannedAt']) <
    evidence.timestamp_ns(manifest['earliest_finish_at']))
result['scheduled_passes'] = {'required': len(expected), 'observed': sum(counts.values()),
    'missing': len(expected - counts.keys()), 'duplicates': sum(value != 1 for value in counts.values()),
    'unexpected': len(counts.keys() - expected)}

result['gc_counts'] = {}
for kind, filename, field in (('heap', 'gc-heap.csv', 'heap_events'),
                              ('collection', 'gc-collections.csv', 'collection_events'),
                              ('pause', 'gc-pauses.csv', 'pause_events')):
    rows, proof = evidence.deduplicate(evidence.rows(OUT, filename), kind)
    result['gc_counts'][kind] = {}
    for component, recording in terminal['complete_gc_recordings'].items():
        own = [row for row in rows if row['component'] == component]
        current = [row for row in own if str(row['pid']) == str(recording['pid'])]
        result['gc_counts'][kind][component] = {
            'final_recording_events': recording[field], 'evaluator_all_processes_events': len(own),
            'same_process_events': len(current), 'extra_process_events': len(own) - len(current),
            'same_process_count_matches': len(current) == recording[field],
            'recording_sha256_matches': contract.digest(evidence.path(OUT, recording['recording_path'])) ==
                                        recording['recording_sha256'],
            'recording_bytes_match': evidence.path(OUT, recording['recording_path']).stat().st_size ==
                                     recording['recording_bytes'],
            'full_window_recording_coverage': recording['coverage_complete'],
            'data_loss_events': recording['data_loss_events']}
result['gc_current_process_all_counts_match'] = all(row['same_process_count_matches']
    for components in result['gc_counts'].values() for row in components.values())
result['coherent_terminal_missing_only_during_initial_evaluation'] = (
    'coherent_manifest_and_terminal' in terminal['evaluation']['missing_coverage'] and
    'coherent_manifest_and_terminal' not in fresh['missing_coverage'])
result['physical_checkpoints'] = []
for path in sorted((OUT / 'physical-checks').glob('*/result.json')):
    value = json.loads(path.read_text())
    result['physical_checkpoints'].append({'phase': path.parent.name,
        **{key: value.get(key) for key in ('result', 'started_at', 'finished_at') if key in value},
        'original_sha256': contract.digest(path)})
result['original_terminal_unchanged'] = contract.digest(OUT / 'shutdown.json') == terminal_hash
result['original_manifest_unchanged'] = contract.digest(OUT / 'observation.json') == manifest_hash
result['installed_tools_unchanged'] = contract.verify_bundle(TOOLS) == hashes
assert result['original_terminal_unchanged'] and result['original_manifest_unchanged'] and result['installed_tools_unchanged']
print(json.dumps(result))
