#!/usr/bin/env python3
"""Replay an unchanged captured case with explicit stable analysis paths."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
BASELINE = 'baseline-v3'
REPLAY_VERSION = 'stable-path-replay-v3'
RUNNER = Path(__file__).with_name('run-etl-independence-v3.py')
SPEC = importlib.util.spec_from_file_location('normal_independence', RUNNER)
support = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(support)


def validate_controller(receipt, source_sha256, configuration_sha256):
    support.require(receipt['returncode'] == 0, 'Actual controller exit 0 is required')
    command = receipt['command']
    support.require(len(command) >= 6 and command[1] == '-B' and
                    Path(command[2]).name == 'run-etl-independence-v3.py' and command[3] == 'run' and
                    command[4] == '--config', 'Receipt does not identify the actual normal controller')
    support.require(receipt['source_sha256'] == source_sha256 and
                    receipt['configuration_sha256'] == configuration_sha256, 'Controller execution identity differs')


def validate_steps(data, config, runtime):
    required = (['instruments', 'preparation', 'startup-passes', 'launch']
                if config['preparation_mode'] == 'fresh' else ['preparation', 'startup-passes', 'launch'])
    support.require([step['label'] for step in runtime['steps']] == required, 'Required native case steps are incomplete')
    for step in runtime['steps']:
        receipt = support.load(data / (step['label'] + '.json'))
        support.require(receipt == {k: v for k, v in step.items() if k != 'label'} and
                        receipt['returncode'] == 0 and not receipt['timed_out'], 'Native preparation/start receipt differs')
        script = Path(receipt['command'][2]).name
        arguments = receipt['command'][3:]
        if step['label'] == 'startup-passes':
            support.require(script == 'wait-etl-startup-v1.py' and receipt['command'][1] == '-B' and
                            Path(receipt['command'][2]).is_absolute(), 'Unexpected startup prerequisite entry point')
            support.require(arguments == ['--chain', config['chain'], '--output',
                            str(Path(config['case_directory']) / 'startup-passes')], 'Startup prerequisite arguments differ')
            continue
        expected = ('launch-retest.py' if step['label'] == 'launch' else
                    'initialize-fresh.py' if config['preparation_mode'] == 'fresh' else 'prepare-retest.py')
        support.require(script == expected and receipt['command'][1] == '-B' and
                        Path(receipt['command'][2]).parent == Path(config['tools']), 'Unexpected native preparation/start entry point')
        if step['label'] == 'instruments':
            support.require(arguments == ['instruments'], 'Actual instrument preparation required')
        else:
            for flag, value in (('--duration-seconds', str(config['duration_seconds'])), ('--chain', config['chain'])):
                support.require(arguments.count(flag) == 1 and arguments[arguments.index(flag) + 1] == value,
                                'Native case arguments differ')
            if step['label'] == 'preparation' and config['preparation_mode'] == 'fresh':
                support.require(arguments[0] == 'prepare', 'Actual native preparation required')


def validate_startup(data, config, runtime, manifest, hashes):
    startup = support.load(data / 'startup-passes/state.json')
    support.require(startup['state'] == 'Ready' and startup['chain'] == config['chain'],
                    'Successful same-chain startup evidence required')
    support.require(startup['tool_hashes'] == hashes and startup['actual_identity'] == runtime['runtime_identity'],
                    'Startup source or runtime identity differs')
    identity = startup['actual_identity']
    unit = dict(line.split('=', 1) for line in manifest['unit_before_observation'].splitlines() if '=' in line)
    support.require(identity['boot_id'] == manifest['boot_id'] and identity['jvms'] == manifest['jvm_identity'] and
                    identity['invocation_id'] == unit['InvocationID'], 'Startup observation identity differs')
    support.require(bool(startup['captures']), 'Actual startup captures required')
    capture = data / 'startup-passes' / ('capture-%04d' % (len(startup['captures']) - 1))
    passes = capture / ('passes-' + identity['invocation_id'] + '.jsonl')
    support.require(support.digest(passes) == startup['captures'][-1]['pass_sha256'], 'Startup pass capture identity differs')
    evaluate, evidence, focused = __import__('evaluate'), __import__('evidence'), __import__('focused')
    records = evaluate.pass_records(passes)
    began = evidence.pass_instant(manifest['started_at'])
    for transition, cadence in enumerate(manifest['configuration']['cadences']):
        rows = [row for row in records if row['invocation_id'] == identity['invocation_id'] and
                row['transition'] == transition and row['cadence'] == cadence]
        support.require(bool(rows), 'Required startup transition is missing: ' + str(transition))
        first = min(rows, key=lambda row: evidence.pass_instant(row['plannedAt']))
        focused.successful_pass(first)
        support.require(evidence.pass_instant(first['endedAt']) < began, 'Startup transition does not precede observation')


def capture(case):
    record = support.load(case / 'capture.json')
    support.require(record['version'] == support.VERSION, 'Normal-finish candidate capture required')
    support.require(support.digest(case / 'frozen-members.json') == record['manifest_sha256'], 'Frozen manifest identity differs')
    frozen = case / 'frozen'
    manifest = support.load(case / 'frozen-members.json')['members']
    support.require(bool(manifest) and support.members(frozen) == manifest, 'Frozen evidence membership or bytes differ')
    for name, expected in record['scenario_sha256'].items():
        support.require(name in support.SCENARIO_FILES and support.digest(Path(__file__).parent / name) == expected,
                        'Replay candidate source differs from captured source')
    support.require(set(record['scenario_sha256']) == set(support.SCENARIO_FILES), 'Incomplete scenario source identities')
    data = frozen / 'case'
    config = support.load(data / 'configuration.json')
    challenge = support.load(data / 'challenge.json')
    runtime = support.load(data / 'runtime.json')
    restoration = support.load(data / 'restoration.json')
    support.require(runtime['version'] == challenge['version'] == support.VERSION and runtime['stage'] == 'NativeComplete',
                    'Completed normal-finish runtime evidence required')
    support.require(runtime['chain'] == challenge['chain'] == config['chain'] and
                    runtime['study_state'] == challenge['study_state'] == config['study_state'] in support.STUDY_STATES,
                    'Scenario identities conflict')
    contract = support.native(frozen / 'native')
    hashes = contract.verify_bundle(frozen / 'native')
    support.require(hashes == challenge['tool_hashes'], 'Captured native bundle identity differs')
    support.require(challenge['scenario_sha256'] == record['scenario_sha256'], 'Scenario source changed during capture')
    support.require(support.digest(data / 'study-original.py') == challenge['original_sha256'] == config['original_sha256'],
                    'Original study bytes differ')
    support.require(restoration['study_sha256'] == config['original_sha256'] and restoration['import_returncode'] == 0,
                    'Actual successful restoration evidence required')
    for label, expected in (('original-import', 0), ('restored-import', 0)):
        receipt = support.load(data / (label + '.json'))
        support.require(receipt['returncode'] == expected and not receipt['timed_out'], 'Recorded native import failed')
        support.require(receipt['command'][1:] == ['-B', '-c', support.IMPORT_CODE, config['study_path']],
                        'Import receipt does not identify the actual study')
    imported = support.load(data / 'challenged-import.json')
    support.require(not imported['timed_out'] and imported['returncode'] == challenge['challenged_import_returncode'],
                    'Challenge native import evidence differs')
    support.require(imported['command'][1:] == ['-B', '-c', support.IMPORT_CODE, config['study_path']],
                    'Challenge receipt does not identify the actual study')
    support.require((imported['returncode'] == 0) == (config['study_state'] == 'changed'), 'Incorrect challenge import outcome')
    if config['study_state'] == 'absent':
        support.require(challenge['challenged_sha256'] is None and 'FileNotFoundError' in (data / 'challenged-import.stderr').read_text(),
                        'Actual absent-study evidence required')
    else:
        support.require(support.digest(data / 'study-challenged.py') == challenge['challenged_sha256'] != challenge['original_sha256'],
                        'Actual challenged study bytes differ')
        if config['study_state'] == 'failing':
            support.require('Intentional unrelated journal-study import failure' in (data / 'challenged-import.stderr').read_text(),
                            'Declared import failure was not observed')
    for label in ('challenge-after-preparation', 'challenge-after-launch', 'challenge-after-finish'):
        probe = support.load(data / (label + '.json'))
        support.require(not probe['timed_out'] and (probe['returncode'] == 0) == (config['study_state'] == 'changed') and
                        probe['command'][1:] == ['-B', '-c', support.IMPORT_CODE, config['study_path']],
                        'Actual challenge phase import is incomplete: ' + label)
    validate_steps(data, config, runtime)
    state = frozen / 'state'
    terminal = support.load(state / 'shutdown.json')
    manifest = support.load(state / 'observation.json')
    support.require(support.digest(state / 'shutdown.json') == record['terminal_sha256'] == runtime['terminal_sha256'],
                    'Original terminal identity differs')
    support.require(support.digest(state / 'observation.json') == runtime['observation_sha256'] and
                    terminal['observation'] == manifest and manifest['tool_hashes'] == hashes,
                    'Observation/native source identities conflict')
    support.require(manifest['duration_seconds'] == config['duration_seconds'] and
                    manifest['configuration'] == contract.chain_configuration(config['chain']), 'Native observation configuration differs')
    validate_startup(data, config, runtime, manifest, hashes)
    service = runtime['finish_service']
    support.require(service['ActiveState'] in ('inactive', 'failed') and service['ExecMainCode'] == '1',
                    'Completed native finish worker required')
    support.validate_terminal(terminal, int(service['ExecMainStatus']))
    support.require(not any((state / name).exists() for name in ('abort.json', 'abort-started.json', 'abort-request.json')),
                    'Abort evidence cannot satisfy normal finish')
    evidence = __import__('evidence')
    evaluate = __import__('evaluate')
    start = evidence.timestamp_ns(manifest['started_at'])
    finish = evidence.timestamp_ns(terminal['finished_at'])
    samples = [support.load(path) for path in (state / 'raw').glob('*/sample.json')]
    full = [row for row in samples if row.get('sample_kind') == 'full' and
            start <= evidence.timestamp_ns(row['observed_at']) <= finish]
    support.require(len(full) >= support.MINIMUM_SAMPLES, 'Two actual full samples required')
    deciding = evaluate.scheduler_checks(manifest)
    support.require(all(row.get('archiving_pvs') == 903 and row.get('connected_pvs') == 903 and
                        not any(error['check'] in deciding for error in row['errors']) for row in full),
                    'Required actual ETL sample evidence is incomplete')
    return frozen, manifest, terminal, config, hashes, len(full)


def native_command(work, caller, aggregate_output, recording_output):
    command = [sys.executable, '-B', str(work / 'native' / (caller + '.py')),
               '--input', str(work / 'state'), '--jfr-output', str(recording_output)]
    if caller == 'aggregate':
        command += ['--output', str(aggregate_output)]
    return command


def replay_native(output, work_root, frozen, caller):
    work = work_root / caller
    shutil.copytree(frozen / 'native', work / 'native')
    shutil.copytree(frozen / 'state', work / 'state')
    support.require(support.members(work / 'native') == support.members(frozen / 'native') and
                    support.members(work / 'state') == support.members(frozen / 'state'), 'Fresh replay copies differ')
    before = support.members(work)
    numerical = output / 'aggregate-result.json'
    command = native_command(work, caller, numerical, work_root / (caller + '-jfr'))
    receipt = support.execute(output, caller, command)
    support.require(support.members(work) == before, 'Replay inputs or tools changed')
    value = (support.load(numerical) if caller == 'aggregate' else
             json.loads((output / 'evaluate.stdout').read_text()))
    return receipt, value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--work-root', type=Path, required=True)
    parser.add_argument('--record-baseline', action='store_true')
    parser.add_argument('--controller-receipt', type=Path)
    args = parser.parse_args()
    case, output = args.case.resolve(), args.output.resolve()
    work_root = args.work_root
    support.require(work_root.is_absolute() and work_root.resolve() == work_root, 'Canonical absolute work root required')
    support.require(not work_root.exists(), 'Existing replay work must be preserved')
    support.require(not case.is_relative_to(work_root) and not work_root.is_relative_to(case / 'frozen') and
                    not output.is_relative_to(work_root) and not work_root.is_relative_to(output),
                    'Replay work overlaps original evidence or output')
    support.require(not output.exists(), 'Output already exists; preserve original evidence')
    support.require(not case.is_relative_to(output) and not output.is_relative_to(case / 'frozen'), 'Output overlaps frozen inputs')
    support.require(not args.record_baseline or output == case / BASELINE, 'Record the baseline in the declared candidate baseline directory')
    frozen, manifest, terminal, config, hashes, full_count = capture(case)
    frozen_before = support.members(frozen)
    if args.record_baseline:
        support.require(args.controller_receipt is not None, 'Actual controller execution receipt required')
        controller_path = args.controller_receipt
    else:
        support.require(args.controller_receipt is None, 'Recipient must preserve the original controller receipt')
        controller_path = case / BASELINE / 'controller-receipt.json'
    controller = support.load(controller_path)
    validate_controller(controller, support.load(case / 'capture.json')['scenario_sha256']['run-etl-independence-v3.py'],
                        support.digest(frozen / 'case/configuration.json'))
    if not args.record_baseline:
        baseline = support.load(case / (BASELINE + '.json'))
        support.require(baseline['replay_source_sha256'] == support.digest(Path(__file__)) and
                        baseline['work_root'] == str(work_root), 'Candidate replay identity or work root differs')
        for name, expected in baseline['artifacts'].items():
            relative = Path(name)
            support.require(not relative.is_absolute() and '..' not in relative.parts, 'Invalid baseline artifact path')
            support.require(support.digest(case / BASELINE / relative) == expected, 'Baseline artifact identity differs')
    work_root.mkdir(parents=True, mode=0o700)
    output.mkdir(parents=True, mode=0o700)
    shutil.copy2(controller_path, output / 'controller-receipt.json')
    artifacts = {}
    artifacts['controller-receipt.json'] = support.digest(output / 'controller-receipt.json')
    values = {}
    receipts = []
    for caller in ('evaluate', 'aggregate'):
        receipt, value = replay_native(output, work_root, frozen, caller)
        support.require(value['verdict'] == terminal['verdict'] and
                        receipt['returncode'] == (0 if value['verdict'] == 'Passed' else 1), 'Native replay verdict/status differs')
        scheduler = value.get('evaluation', value).get('scheduler_verdict')
        support.require(scheduler == 'Passed', 'Required replayed ETL evidence is incomplete')
        values[caller] = value
        receipts.append(receipt)
        for suffix in ('stdout', 'stderr'):
            name = caller + '.' + suffix
            artifacts[name] = support.digest(output / name)
    artifacts['aggregate-result.json'] = support.digest(output / 'aggregate-result.json')
    result = {'version': support.VERSION, 'replay_version': REPLAY_VERSION,
              'replay_source_sha256': support.digest(Path(__file__)), 'work_root': str(work_root),
              'chain': config['chain'], 'study_state': config['study_state'],
              'expectation': 'Passed', 'terminal_kind': 'finish', 'terminal_sha256': support.digest(frozen / 'state/shutdown.json'),
              'tool_hashes': hashes, 'full_samples': full_count, 'native_evaluation': values['evaluate'],
              'native_aggregate': values['aggregate']}
    result_bytes = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
    artifacts['result.json'] = hashlib.sha256(result_bytes).hexdigest()
    support.require(support.members(frozen) == frozen_before, 'Frozen originals changed during replay')
    if not args.record_baseline and not (baseline['frozen_manifest_sha256'] == support.digest(case / 'frozen-members.json') and
            baseline['terminal_sha256'] == result['terminal_sha256'] and baseline['artifacts'] == artifacts):
        result['expectation'] = 'Failed'
        support.save(output / 'result.json', result)
        support.save(output / 'verification.json', {'result': 'Failed', 'matches_baseline': False, 'commands': receipts,
                     'reason': 'Complete replay result bytes differ from the recorded baseline'})
        print(json.dumps({'expectation': 'Failed', 'matches_baseline': False}))
        return 1
    (output / 'result.json').write_bytes(result_bytes)
    if args.record_baseline:
        support.save(case / (BASELINE + '.json'), {'artifacts': artifacts, 'terminal_sha256': result['terminal_sha256'],
                     'frozen_manifest_sha256': support.digest(case / 'frozen-members.json'),
                     'replay_source_sha256': support.digest(Path(__file__)), 'work_root': str(work_root)})
    support.save(output / 'verification.json', {'recorded_at': support.now(), 'baseline_recorded': args.record_baseline,
                 'matches_baseline': None if args.record_baseline else True, 'commands': receipts,
                 'python': sys.executable, 'python_version': sys.version, 'scope': 'Actual captured normal-finish case only'})
    print(json.dumps({'expectation': 'Passed', 'baseline_recorded': args.record_baseline,
                      'matches_baseline': None if args.record_baseline else True}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, KeyError, TypeError, ValueError, RuntimeError, ImportError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(2)
