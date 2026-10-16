#!/usr/bin/env python3
"""Assess real filesystem-fault evidence and repeat the shipped native evaluation."""

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()


def journal(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(mode=0o700)
    sys.path.insert(0, str(TOOLS))
    import collect
    import contract
    import evaluate
    import focused
    hashes = contract.verify_bundle(TOOLS)
    runtime = json.loads((args.case / 'runtime.json').read_text())
    declaration = json.loads((args.case / 'runtime-contract.json').read_text())
    manifest = json.loads((OUT / 'observation.json').read_text())
    terminal = json.loads((OUT / 'abort.json').read_text())
    terminal_hash = digest(OUT / 'abort.json')
    case = runtime['case']
    assert case in ('E3', 'E4') and runtime['stage'] == 'Native case complete; preservation and frozen replay pending'
    assert declaration['case'] == case and declaration['chain'] == runtime['chain']
    assert hashes == declaration['tool_hashes'] == manifest['tool_hashes']
    assert manifest['duration_seconds'] == 86400 and not manifest['start_findings']
    assert terminal['observation'] == manifest and terminal['terminal_kind'] == 'abort'
    assert terminal['verdict'] != 'Passed' and terminal['stop']['rc'] == 0 and not terminal['errors']
    assert terminal['stop_elapsed_seconds'] <= __import__('observe').timeout_seconds(terminal['stop_timeout'])
    assert (args.case / 'actual-sampler-before-fault.txt').read_bytes() == (args.case / 'actual-sampler-after-restoration.txt').read_bytes()
    assert (args.case / 'declared-fault-dropin.conf').read_bytes() == (args.case / 'removed-fault-dropin.conf').read_bytes()
    restoration = json.loads((args.case / 'actual-restoration.json').read_text())
    assert restoration['fault_dropin_absent'] and restoration['original_effective_unit_bytes_equal']
    assert digest(args.case / 'actual-sampler-after-restoration.txt') == restoration['restored_effective_unit_sha256']
    states = {}
    for path in (args.case / 'actual-state-history').glob('*.json'):
        assert digest(path) == path.stem
        states[path.stem] = json.loads(path.read_text())
    first = json.loads((args.case / 'actual-first-fault-sample.json').read_text())
    assert first['automatic_abort_request_absent']
    assert digest(Path(first['sample'])) == first['sample_sha256']
    assert states[first['state_sha256']]['consecutive_abort_failures'] == (1 if case == 'E4' else 0)
    probes = [json.loads(path.read_text()) for path in (args.case / 'namespace-probes').glob('*/receipt.json')]
    real_probes = [row for row in probes if not row['probe_only']]
    assert len(real_probes) >= 2
    for probe in real_probes:
        assert probe['native_collector_sha256'] == hashes['collect.py']
        assert probe['journal_query'].get('returncode', -1) != 0
        assert all(row['available'] == (case == 'E3') for row in probe['files'].values())
    unit_events = journal(args.case / 'actual-sampler-journal.stdout')
    samples = []
    for name, expected in sorted(runtime['actual_fault_sample_hashes'].items()):
        path = Path(name)
        assert path.is_relative_to(OUT / 'raw') and digest(path) == expected
        sample = json.loads(path.read_text())
        assert sample['sample_kind'] == 'full' and sample['errors']
        checks = {row['check'] for row in sample['errors']}
        assert checks <= {'journal', 'health_journal', 'kernel_journal'}
        assert {'health_journal', 'kernel_journal'} <= checks
        assert ('journal' in checks) == (case == 'E4')
        assert collect.critical(sample, **collect.abort_policy(OUT)) == (case == 'E4')
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
        assert corresponding
        assert all(row['consecutive_abort_failures'] == (len(samples) + 1 if case == 'E4' else 0)
                   for row in corresponding)
        samples.append(sample)
    assert len(samples) >= declaration['minimum_fault_full_samples'] == 2
    outside = evaluate.pass_records(args.case / 'outside-native-passes.jsonl')
    witness = runtime['actual_native_pass']
    assert witness in outside and witness['transition'] == 0
    assert witness['plannedAt'] == declaration['target_native_sts_pass']['planned_at']
    focused.successful_pass(witness)
    assert evaluate.epoch(runtime['fault_begin']) <= evaluate.epoch(witness['startedAt'])
    assert evaluate.epoch(witness['endedAt']) <= evaluate.epoch(runtime['fault_end'])
    if case == 'E3':
        assert not (OUT / 'abort-request.json').exists() and not runtime['actual_abort_invocations']
        assert witness in evaluate.pass_records(OUT / 'passes.jsonl')
        recovered = json.loads((args.case / 'actual-recovery-samples.json').read_text())
        assert len(recovered) >= 2
        for name, expected in recovered.items():
            path = Path(name)
            assert path.is_relative_to(OUT / 'raw') and digest(path) == expected
            assert not json.loads(path.read_text())['errors']
    else:
        request = json.loads((OUT / 'abort-request.json').read_text())
        assert request['reason'] == 'consecutive_sample_failures'
        assert request['trigger_sample'] == sorted(runtime['actual_fault_sample_hashes'])[1]
        invocations = {row['_SYSTEMD_INVOCATION_ID'] for row in journal(args.case / 'actual-abort-unit-journal.stdout')
            if row.get('_SYSTEMD_UNIT') == 'etl-soak-abort.service' and row.get('_SYSTEMD_INVOCATION_ID')}
        assert invocations == set(runtime['actual_abort_invocations']) and len(invocations) == 1
    actual = subprocess.run([sys.executable, '-B', str(TOOLS / 'evaluate.py'), '--input', str(OUT)],
                            capture_output=True, timeout=600)
    (args.output / 'native-evaluate.stdout').write_bytes(actual.stdout)
    (args.output / 'native-evaluate.stderr').write_bytes(actual.stderr)
    evaluation = json.loads(actual.stdout)
    assert actual.returncode == 1 and evaluation['verdict'] != 'Passed'
    numerical_file = args.output / 'aggregate.json'
    actual = subprocess.run([sys.executable, '-B', str(TOOLS / 'aggregate.py'), '--input', str(OUT),
                            '--output', str(numerical_file)], capture_output=True, timeout=600)
    (args.output / 'native-aggregate.stdout').write_bytes(actual.stdout)
    (args.output / 'native-aggregate.stderr').write_bytes(actual.stderr)
    numerical = json.loads(numerical_file.read_text())
    assert actual.returncode == 1 and numerical['verdict'] != 'Passed'
    assert digest(OUT / 'abort.json') == terminal_hash
    result = {'case': case, 'chain': runtime['chain'], 'expectation': 'Passed',
              'actual_fault_full_samples': len(samples), 'native_short_observation': terminal['verdict'],
              'native_evaluation': evaluation, 'native_aggregate': numerical,
              'terminal_sha256': terminal_hash, 'original_terminal_unchanged': True}
    (args.output / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: result[key] for key in ('case', 'chain', 'expectation',
                     'actual_fault_full_samples', 'native_short_observation', 'terminal_sha256')}))


if __name__ == '__main__':
    main()
