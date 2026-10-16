#!/usr/bin/env python3
"""Check the retained E3 originals and run the frozen native evaluation unchanged."""

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

COMPONENTS = ('mgmt', 'engine', 'etl', 'retrieval')


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()


def load(path):
    return json.loads(path.read_text())


def lines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--case-root', type=Path, required=True)
    parser.add_argument('--preservation', type=Path, required=True)
    parser.add_argument('--expected-bundle-sha256', required=True)
    args = parser.parse_args()
    TOOLS = args.tools.resolve()
    OUT = args.input.resolve()
    CASE = args.case_root.resolve()
    PRESERVATION = args.preservation.resolve()
    EXPECTED_BUNDLE = args.expected_bundle_sha256
    args.output.mkdir(mode=0o700)
    sys.path.insert(0, str(TOOLS))
    import collect
    import contract
    import evaluate
    import evidence
    import focused
    import observe
    import pass_source

    hashes = contract.verify_bundle(TOOLS)
    assert digest(TOOLS / 'bundle.json') == EXPECTED_BUNDLE
    originals = load(PRESERVATION / 'original-files-sha256.json')
    for name, expected in originals.items():
        assert digest(Path('/') / name) == expected
    runtime = load(CASE / 'runtime.json')
    terminal = load(OUT / 'abort.json')
    manifest = load(OUT / 'observation.json')
    declaration = load(CASE / 'runtime-contract.json')
    began = load(CASE / 'actual-fault-begin.json')
    restored = load(CASE / 'actual-restoration.json')
    assert runtime['case'] == declaration['case'] == 'E3'
    assert runtime['chain'] == declaration['chain'] == 'shortened'
    assert runtime['stage'] == runtime['expectation'] == 'Incomplete'
    assert runtime['error'] == 'An actual fault-case command failed: actual-sampler-journal'
    query = runtime['steps'][-1]
    assert query['name'] == 'actual-sampler-journal' and query['returncode'] == 1
    arguments = query['actual_arguments']
    assert arguments[arguments.index('--since') + 1] == manifest['started_at']
    assert (CASE / 'actual-sampler-journal.stderr').read_text().strip() == (
        'Failed to parse timestamp: ' + manifest['started_at'])
    assert (CASE / 'actual-sampler-journal.stdout').stat().st_size == 0
    assert hashes == declaration['tool_hashes'] == manifest['tool_hashes']
    assert manifest['duration_seconds'] == declaration['configured_duration_seconds'] == 86400
    assert not manifest['start_findings'] and terminal['observation'] == manifest
    assert terminal['terminal_kind'] == 'abort' and terminal['verdict'] != 'Passed'
    assert terminal['stop']['rc'] == 0 and not terminal['errors']
    assert terminal['stop_elapsed_seconds'] <= observe.timeout_seconds(terminal['stop_timeout'])
    assert (CASE / 'actual-sampler-before-fault.txt').read_bytes() == (
        CASE / 'actual-sampler-after-restoration.txt').read_bytes()
    assert (CASE / 'declared-fault-dropin.conf').read_bytes() == (CASE / 'removed-fault-dropin.conf').read_bytes()
    assert restored['fault_dropin_absent'] and restored['original_effective_unit_bytes_equal']
    assert digest(CASE / 'actual-sampler-after-restoration.txt') == restored['restored_effective_unit_sha256']

    states = {}
    for path in sorted((CASE / 'actual-state-history').glob('*.json')):
        assert digest(path) == path.stem
        states[path.stem] = load(path)
    assert states and all(row.get('consecutive_abort_failures', 0) == 0 for row in states.values())
    history = lines(CASE / 'actual-state-history.jsonl')
    assert history and all(row['sha256'] in states for row in history)
    assert all(row.get('consecutive_abort_failures', 0) == 0 for row in history)
    first = load(CASE / 'actual-first-fault-sample.json')
    assert first['automatic_abort_request_absent']
    assert digest(Path(first['sample'])) == first['sample_sha256']
    assert states[first['state_sha256']]['consecutive_abort_failures'] == 0
    assert not (OUT / 'abort-request.json').exists()
    assert not list(CASE.glob('actual-abort-invocation-*.txt'))

    probes = [load(path) for path in (CASE / 'namespace-probes').glob('*/receipt.json')]
    real_probes = sorted((row for row in probes if not row['probe_only']), key=lambda row: row['recorded_at'])
    assert len(real_probes) >= declaration['minimum_fault_full_samples'] == 2
    for probe in real_probes:
        assert probe['native_collector_sha256'] == hashes['collect.py']
        assert probe['native_exec_arguments'] == ['/usr/bin/python3', '-B', str(TOOLS / 'collect.py'),
                                                  str(OUT), str(TOOLS / 'pvs-all.csv')]
        inaccessible = probe['journal_query']
        assert (inaccessible.get('returncode', -1) != 0 and
                ('returncode' in inaccessible or inaccessible.get('errno') in (1, 2, 13)))
        assert set(probe['files']) == set(COMPONENTS)
        assert all(row['available'] for row in probe['files'].values())
    unit_events = lines(PRESERVATION / 'retained-journals/etl-soak-sample.service.jsonl')
    assert not lines(PRESERVATION / 'retained-journals/etl-soak-abort.service.jsonl')
    fault_samples = []
    for path in sorted((OUT / 'raw').glob('*/sample.json')):
        sample = load(path)
        if (sample.get('sample_kind') != 'full' or not
                began['observed_at'] <= sample['observed_at'] <= restored['observed_at']):
            continue
        checks = {row['check'] for row in sample['errors']}
        assert checks == {'health_journal', 'kernel_journal'}
        assert not collect.critical(sample, **collect.abort_policy(OUT))
        matching = []
        for event in unit_events:
            try:
                message = json.loads(event.get('MESSAGE', ''))
            except (ValueError, TypeError):
                continue
            if isinstance(message, dict) and message.get('observed_at') == sample['observed_at']:
                matching.append(event)
        assert len(matching) == 1
        event = matching[0]
        assert event['_SYSTEMD_UNIT'] == 'etl-soak-sample.service'
        assert sum(str(probe['pid']) == event['_PID'] for probe in real_probes) == 1
        wall = datetime.datetime.fromisoformat(sample['observed_at']).timestamp()
        corresponding = [row for row in states.values() if row.get('wall') == wall]
        assert corresponding and all(row['consecutive_abort_failures'] == 0 for row in corresponding)
        fault_samples.append({'observed_at': sample['observed_at'], 'sha256': digest(path),
                              'error_checks': sorted(checks), 'automatic_abort_critical': False})
    assert len(fault_samples) == len(real_probes) == 2
    recovered = load(CASE / 'actual-recovery-samples.json')
    assert len(recovered) >= 2
    recovery_times = []
    for name, expected in recovered.items():
        path = Path(name)
        assert path.is_relative_to(OUT / 'raw') and digest(path) == expected
        sample = load(path)
        assert sample['sample_kind'] == 'full' and not sample['errors']
        assert sample['observed_at'] >= restored['observed_at']
        recovery_times.append(sample['observed_at'])

    state = load(OUT / 'state.json')
    for component in COMPONENTS:
        capture = Path(state['application_file_sources'][component]['capture'])
        receipt = load(capture.with_suffix(capture.suffix + '.receipt.json'))
        source = pass_source.INSTALL / component / 'logs' / pass_source.FILENAME
        assert digest(capture) == receipt['sha256'] == digest(source)
        assert receipt['trailing_bytes'] == 0
        for probe in real_probes:
            assert (probe['files'][component]['device'], probe['files'][component]['inode']) == (
                receipt['device'], receipt['inode'])
        before = CASE / ('outside-before-' + component + '.jsonl')
        before_receipt = load(before.with_suffix(before.suffix + '.receipt.json'))
        assert digest(before) == before_receipt['sha256']
        assert (receipt['device'], receipt['inode']) == (before_receipt['device'], before_receipt['inode'])
        assert source.read_bytes().startswith(before.read_bytes())
    events = pass_source.read('etl', args.output / 'actual-retained-etl-source.jsonl')
    outside = args.output / 'actual-native-passes.jsonl'
    outside.write_text(''.join(json.dumps(row) + '\n' for row in events if evaluate.PASS.search(row['MESSAGE'])))
    records = evaluate.pass_records(outside)
    target = declaration['target_native_sts_pass']
    candidates = [row for row in records if row['transition'] == 0 and
                  row['invocation_id'] == began['identity']['invocation_id'] and
                  evidence.timestamp_ns(row['plannedAt']) == evidence.timestamp_ns(target['planned_at'])]
    assert len(candidates) == 1
    witness = candidates[0]
    focused.successful_pass(witness)
    assert evaluate.epoch(began['observed_at']) <= evaluate.epoch(witness['startedAt'])
    assert evaluate.epoch(witness['startedAt']) <= evaluate.epoch(witness['endedAt'])
    assert evaluate.epoch(witness['endedAt']) <= evaluate.epoch(real_probes[-1]['recorded_at'])
    assert witness in evaluate.pass_records(OUT / 'passes.jsonl')

    native = {}
    for label, arguments in (
            ('evaluate', [str(TOOLS / 'evaluate.py'), '--input', str(OUT)]),
            ('aggregate', [str(TOOLS / 'aggregate.py'), '--input', str(OUT),
                           '--output', str(args.output / 'aggregate.json')])):
        actual = subprocess.run([sys.executable, '-B', *arguments], capture_output=True, timeout=600)
        (args.output / ('native-' + label + '.stdout')).write_bytes(actual.stdout)
        (args.output / ('native-' + label + '.stderr')).write_bytes(actual.stderr)
        value = json.loads(actual.stdout) if label == 'evaluate' else load(args.output / 'aggregate.json')
        assert actual.returncode == 1 and value['verdict'] != 'Passed'
        native[label] = value
    assert digest(OUT / 'abort.json') == originals[str((OUT / 'abort.json').relative_to('/'))]
    assert digest(CASE / 'runtime.json') == originals[str((CASE / 'runtime.json').relative_to('/'))]
    assert contract.verify_bundle(TOOLS) == hashes
    result = {'case': 'E3', 'chain': 'shortened', 'evidence_verdict': 'Passed',
              'original_runtime_verdict': runtime['expectation'],
              'original_native_observation_verdict': terminal['verdict'],
              'original_runtime_sha256': digest(CASE / 'runtime.json'),
              'original_terminal_sha256': digest(OUT / 'abort.json'),
              'frozen_bundle_sha256': digest(TOOLS / 'bundle.json'),
              'verified_original_files': len(originals), 'fault_full_samples': fault_samples,
              'recovery_full_samples': sorted(recovery_times), 'actual_native_pass': witness,
              'journal_access_failed_with_all_four_application_files_available': True,
              'sampler_journal_matched_to_actual_native_collectors': True,
              'automatic_abort_request_absent': True, 'automatic_abort_invocations_absent': True,
              'all_observed_abort_failure_counters_zero': True,
              'native_pass_preserved_in_independent_and_collected_sources': True,
              'planned_time_comparison': {
                  'expected_text': target['planned_at'], 'actual_text': witness['plannedAt'],
                  'expected_ns': evidence.timestamp_ns(target['planned_at']),
                  'actual_ns': evidence.timestamp_ns(witness['plannedAt']),
                  'same_instant': True, 'original_time_strings_unchanged': True},
              'all_four_application_sources_match_final_capture_bytes_and_original_identities': True,
              'fault_configuration_restored_exactly': True, 'recovery_error_count': 0,
              'native_stop_rc': terminal['stop']['rc'], 'terminal_capture_error_count': len(terminal['errors']),
              'original_runtime_and_terminal_unchanged': True,
              'late_collection_failure': 'journalctl rejected the ISO timestamp after native shutdown',
              'native': native}
    (args.output / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: result[key] for key in ('case', 'chain', 'evidence_verdict',
        'original_runtime_verdict', 'original_native_observation_verdict', 'verified_original_files',
        'native_stop_rc', 'terminal_capture_error_count', 'original_runtime_and_terminal_unchanged')}))


if __name__ == '__main__':
    main()
