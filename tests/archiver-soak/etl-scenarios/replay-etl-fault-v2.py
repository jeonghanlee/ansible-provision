#!/usr/bin/env python3
"""Assess real filesystem-fault evidence and repeat the shipped native evaluation."""

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import shutil
import fault_support as candidate

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
    parser.add_argument('--case', type=Path)
    parser.add_argument('--check-retained-pass', action='store_true')
    parser.add_argument('--contract', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--tools', type=Path)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--members', type=Path)
    parser.add_argument('--members-sha256')
    parser.add_argument('--controller-receipt', type=Path)
    parser.add_argument('--controller-receipt-sha256')
    parser.add_argument('--record-baseline', action='store_true')
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--baseline-sha256')
    args = parser.parse_args()
    if args.check_retained_pass:
        try:
            context = json.loads(args.contract.read_text())
            sys.path.insert(0, str(Path(context['candidate']['root']).resolve()))
            import evidence
            return evidence.retained_pass_main(args.contract, args.output, __file__)
        except Exception as error:
            print(json.dumps({'verdict': 'Incomplete', 'reason': 'invocation',
                              'native_exit_status': 2, 'error_type': type(error).__name__}, sort_keys=True))
            return 2
    if args.case is None or args.contract is not None:
        parser.error('Full scenario replay requires --case and no retained-input contract')
    candidate.require(args.tools is not None and args.input is not None and args.members is not None and
                      args.members_sha256 is not None and args.controller_receipt is not None and
                      args.controller_receipt_sha256 is not None,
                      'Complete frozen roots and actual controller receipt required')
    candidate.require(args.record_baseline != (args.baseline is not None), 'Select baseline recording or recipient comparison')
    candidate.require((args.baseline is None) == (args.baseline_sha256 is None), 'Pin the recipient baseline manifest')
    roots = {'tools': args.tools.resolve(), 'input': args.input.resolve(), 'case': args.case.resolve()}
    output = args.output.resolve()
    candidate.require(not output.exists() and all(not output.is_relative_to(path) and not path.is_relative_to(output)
                      for path in roots.values()), 'Output exists or overlaps protected inputs')
    frozen = candidate.verified(roots, args.members, args.members_sha256)
    sources = candidate.load(args.case / 'candidate-sources.json')
    candidate.require(set(sources) == set(candidate.FILES) and
                      all(candidate.digest(candidate.ROOT / name) == value for name, value in sources.items()),
                      'Candidate source differs from captured controller')
    candidate.require(digest(args.controller_receipt) == args.controller_receipt_sha256, 'Controller receipt identity differs')
    candidate.controller(candidate.load(args.controller_receipt), sources,
                         digest(args.case / 'candidate-configuration.json'))
    runtime = candidate.load(args.case / 'runtime.json')
    candidate.require(runtime.get('candidate_version') == candidate.VERSION, 'Actual candidate runtime required')
    if args.baseline is not None:
        candidate.require(digest(args.baseline / 'artifacts.json') == args.baseline_sha256,
                          'Baseline manifest identity differs')
        baseline_artifacts = candidate.load(args.baseline / 'artifacts.json')
        candidate.require(set(baseline_artifacts) == {'native-evaluate.stdout', 'native-evaluate.stderr',
                          'native-aggregate.stdout', 'native-aggregate.stderr', 'aggregate.json', 'result.json'},
                          'Complete baseline artifact membership required')
        candidate.require(all(digest(args.baseline / name) == value for name, value in baseline_artifacts.items()),
                          'Original baseline artifacts changed')
    output.mkdir(mode=0o700)
    shutil.copytree(roots['tools'], output / 'native')
    shutil.copytree(roots['input'], output / 'input')
    candidate.require(candidate.members(output / 'native') == frozen['tools'] and
                      candidate.members(output / 'input') == frozen['input'], 'Fresh replay copies differ')
    global TOOLS, OUT
    TOOLS, OUT = output / 'native', output / 'input'
    recorded_path = lambda name: candidate.source_path(name, candidate.OUT, OUT)
    sys.path.insert(0, str(TOOLS))
    import collect
    import contract
    import evaluate
    import evidence
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
    candidate.terminal(terminal, runtime['native_terminal_status'])
    if case == 'E3':
        actual_abort = candidate.load(args.case / 'planned-native-abort.json')
        candidate.require(actual_abort['returncode'] == 1 and not actual_abort['timed_out'],
                          'Actual planned abort exit 1 required')
    else:
        worker = runtime['completed_abort_worker']
        candidate.require(worker == collect.properties((args.case / 'actual-completed-abort-unit.stdout').read_text()) and
                          worker['ActiveState'] in ('inactive', 'failed') and worker['ExecMainCode'] == '1' and
                          worker['ExecMainStatus'] == '1' and worker['InvocationID'] in runtime['actual_abort_invocations'],
                          'Actual automatic abort worker exit 1 required')
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
    assert digest(recorded_path(first['sample'])) == first['sample_sha256']
    assert states[first['state_sha256']]['consecutive_abort_failures'] == (1 if case == 'E4' else 0)
    probes = [json.loads(path.read_text()) for path in (args.case / 'namespace-probes').glob('*/receipt.json')]
    real_probes = [row for row in probes if not row['probe_only']]
    assert len(real_probes) >= 2
    for probe in real_probes:
        assert probe['native_collector_sha256'] == hashes['collect.py']
        assert probe['journal_query'].get('returncode', -1) != 0
        assert all(row['available'] == (case == 'E3') for row in probe['files'].values())
    query_groups = candidate.load(args.case / 'case-journals.json')
    candidate.require({row['role'] for row in query_groups} == {'sampler', 'abort'} and
                      all(row['verdict'] == 'Passed' and row['capture_complete'] and row['returncode'] == 0
                          for row in query_groups), 'Complete real journal queries required for scenario identity')
    unit_events = journal(args.case / 'actual-sampler-journal.selected.jsonl')
    samples = []
    for name, expected in sorted(runtime['actual_fault_sample_hashes'].items()):
        path = recorded_path(name)
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
    identity = json.loads((args.case / 'actual-fault-begin.json').read_text())['identity']
    witness = evidence.checked_pass(args.case / 'outside-native-passes.jsonl',
                                    declaration['target_native_sts_pass'], identity,
                                    runtime['fault_begin'], runtime['fault_end'])
    assert witness == runtime['actual_native_pass'] and witness in outside
    if case == 'E3':
        assert not (OUT / 'abort-request.json').exists() and not runtime['actual_abort_invocations']
        assert witness in evaluate.pass_records(OUT / 'passes.jsonl')
        recovered = json.loads((args.case / 'actual-recovery-samples.json').read_text())
        assert len(recovered) >= 2
        for name, expected in recovered.items():
            path = recorded_path(name)
            assert path.is_relative_to(OUT / 'raw') and digest(path) == expected
            assert not json.loads(path.read_text())['errors']
    else:
        request = json.loads((OUT / 'abort-request.json').read_text())
        assert request['reason'] == 'consecutive_sample_failures'
        assert request['trigger_sample'] == sorted(runtime['actual_fault_sample_hashes'])[1]
        invocations = {row['_SYSTEMD_INVOCATION_ID'] for row in journal(args.case / 'actual-abort-unit-journal.selected.jsonl')
            if row.get('_SYSTEMD_UNIT') == 'etl-soak-abort.service' and row.get('_SYSTEMD_INVOCATION_ID')}
        assert invocations == set(runtime['actual_abort_invocations']) and len(invocations) == 1
    actual = subprocess.run([sys.executable, '-B', str(TOOLS / 'evaluate.py'), '--input', str(OUT)],
                            capture_output=True, timeout=600)
    (args.output / 'native-evaluate.stdout').write_bytes(actual.stdout)
    (args.output / 'native-evaluate.stderr').write_bytes(actual.stderr)
    evaluation = json.loads(actual.stdout)
    candidate.require(actual.returncode == 1 and evaluation['verdict'] == 'Incomplete', 'Native evaluator must preserve Incomplete/1')
    candidate.save(args.output / 'native-evaluate.receipt.json', {'command': actual.args, 'returncode': actual.returncode})
    numerical_file = args.output / 'aggregate.json'
    actual = subprocess.run([sys.executable, '-B', str(TOOLS / 'aggregate.py'), '--input', str(OUT),
                            '--output', str(numerical_file)], capture_output=True, timeout=600)
    (args.output / 'native-aggregate.stdout').write_bytes(actual.stdout)
    (args.output / 'native-aggregate.stderr').write_bytes(actual.stderr)
    numerical = json.loads(numerical_file.read_text())
    candidate.require(actual.returncode == 1 and numerical['verdict'] == 'Incomplete', 'Native aggregator must preserve Incomplete/1')
    candidate.save(args.output / 'native-aggregate.receipt.json', {'command': actual.args, 'returncode': actual.returncode})
    assert digest(OUT / 'abort.json') == terminal_hash
    result = {'case': case, 'chain': runtime['chain'], 'expectation': 'Passed',
              'actual_fault_full_samples': len(samples), 'native_short_observation': terminal['verdict'],
              'native_evaluation': evaluation, 'native_aggregate': numerical,
              'terminal_sha256': terminal_hash, 'original_terminal_unchanged': True}
    result_bytes = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
    artifact_names = ('native-evaluate.stdout', 'native-evaluate.stderr', 'native-aggregate.stdout',
                      'native-aggregate.stderr', 'aggregate.json')
    artifacts = {name: digest(args.output / name) for name in artifact_names}
    artifacts['result.json'] = hashlib.sha256(result_bytes).hexdigest()
    candidate.require(candidate.members(OUT) == frozen['input'] and candidate.members(TOOLS) == frozen['tools'],
                      'Replay changed copied evidence or native sources')
    candidate.verified(roots, args.members, args.members_sha256)
    if args.baseline is not None:
        candidate.require(artifacts == baseline_artifacts, 'Complete recipient artifact bytes differ')
    (args.output / 'result.json').write_bytes(result_bytes)
    candidate.save(args.output / 'artifacts.json', artifacts)
    print(json.dumps({key: result[key] for key in ('case', 'chain', 'expectation',
                     'actual_fault_full_samples', 'native_short_observation', 'terminal_sha256')}))


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, KeyError, TypeError, ValueError, RuntimeError, AssertionError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(2)
