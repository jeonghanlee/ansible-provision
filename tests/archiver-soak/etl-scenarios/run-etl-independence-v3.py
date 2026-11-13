#!/usr/bin/env python3
"""Challenge an unrelated module and collect a real normal-finish observation."""

import argparse
import datetime
import fcntl
import importlib
import json
import hashlib
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

VERSION = 'normal-finish-v3'
STUDY_STATES = ('absent', 'failing', 'changed')
POLL_SECONDS = 5
IMPORT_TIMEOUT = 30
COMMAND_TIMEOUT = 2700
READINESS_TIMEOUT = 600
MINIMUM_SAMPLES = 2
SCENARIO_FILES = ('run-etl-independence-v3.py', 'replay-etl-independence-v3.py', 'wait-etl-startup-v1.py')
IMPORT_CODE = ('import importlib.util, pathlib, sys; p=pathlib.Path(sys.argv[1]); '
               'sys.path.insert(0,str(p.parent)); '
               's=importlib.util.spec_from_file_location("unrelated_study",p); '
               'm=importlib.util.module_from_spec(s); s.loader.exec_module(m)')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def native(tools):
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(tools))
    module = importlib.import_module('contract')
    require(Path(module.__file__).resolve().parent == tools, 'Mixed native tool directories')
    module.verify_bundle(tools)
    return module


def members(root):
    result = {}
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'Linked evidence member: ' + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = digest(path)
    return result


def configuration(value):
    require(isinstance(value, dict) and value.get('role') == 'etl', 'Configuration requires role=etl')
    value = dict(value)
    require(value.get('chain') in ('shortened', 'default'), 'Unsupported chain')
    require(value.get('study_state') in STUDY_STATES, 'Unsupported study state')
    require(type(value.get('duration_seconds')) is int, 'Duration must be an integer')
    for name in ('tools', 'state_directory', 'case_directory', 'study_path'):
        path = Path(value[name])
        require(path.is_absolute() and str(path.resolve()) == str(path), 'Canonical absolute path required: ' + name)
    roots = [Path(value[k]) for k in ('tools', 'state_directory', 'case_directory')]
    for index, left in enumerate(roots):
        for right in roots[index + 1:]:
            require(not left.is_relative_to(right) and not right.is_relative_to(left), 'Case/native roots overlap')
    study = Path(value['study_path'])
    require(all(not study.is_relative_to(root) for root in roots), 'Study must be outside case and native roots')
    require(re.fullmatch('[0-9a-f]{64}', value.get('original_sha256', '')) is not None, 'Original study SHA256 required')
    budget = value.get('timeout_seconds')
    require(type(budget) in (int, float) and math.isfinite(budget) and budget > value['duration_seconds'],
            'Finite case budget must exceed the native observation duration')
    value.setdefault('preparation_mode', 'fresh')
    require(value['preparation_mode'] in ('fresh', 'retest'), 'Unsupported preparation mode')
    contract = native(Path(value['tools']))
    contract.validate_duration(value['duration_seconds'])
    if value['preparation_mode'] == 'retest':
        require(Path(value['capacity_evidence']).is_absolute(), 'Absolute capacity evidence required')
        require(type(value.get('projected_growth_bytes')) is int and value['projected_growth_bytes'] > 0,
                'Measured growth projection required')
    return value


def execute(case, label, command, timeout=COMMAND_TIMEOUT):
    started = now()
    began = time.monotonic()
    with (case / (label + '.stdout')).open('xb') as output, (case / (label + '.stderr')).open('xb') as errors:
        child = subprocess.Popen(command, stdout=output, stderr=errors, start_new_session=True)
        timed_out = False
        try:
            status = child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                status = child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                status = child.wait(timeout=5)
    receipt = {'command': list(map(str, command)), 'started_at': started, 'finished_at': now(),
               'elapsed_seconds': time.monotonic() - began, 'returncode': status, 'timed_out': timed_out}
    save(case / (label + '.json'), receipt)
    require(not timed_out, 'Native command timed out: ' + label)
    return receipt


def import_study(case, label, study):
    return execute(case, label, [sys.executable, '-B', '-c', IMPORT_CODE, str(study)], IMPORT_TIMEOUT)


def challenge_matches(config, record):
    study = Path(config['study_path'])
    if config['study_state'] == 'absent':
        require(not os.path.lexists(study), 'Absent study unexpectedly exists')
    else:
        require(study.is_file() and not study.is_symlink() and digest(study) == record['challenged_sha256'],
                'Challenged study changed unexpectedly')
    require(native(Path(config['tools'])).verify_bundle(Path(config['tools'])) == record['tool_hashes'],
            'Native dependency bundle changed')
    require({name: digest(Path(__file__).parent / name) for name in SCENARIO_FILES} == record['scenario_sha256'],
            'Candidate scenario sources changed')


def probe_challenge(config, record, label):
    challenge_matches(config, record)
    case = Path(config['case_directory'])
    receipt = import_study(case, label, Path(config['study_path']))
    require((receipt['returncode'] == 0) == (config['study_state'] == 'changed'),
            'Challenge import outcome changed: ' + label)
    if config['study_state'] != 'changed':
        expected = 'FileNotFoundError' if config['study_state'] == 'absent' else 'Intentional unrelated journal-study import failure'
        require(expected in (case / (label + '.stderr')).read_text(), 'Unexpected challenge import error: ' + label)
    return receipt


def apply_challenge(config):
    case, study = Path(config['case_directory']), Path(config['study_path'])
    require(not case.exists(), 'Case directory already exists')
    require(study.is_file() and not study.is_symlink() and digest(study) == config['original_sha256'],
            'Original study identity differs')
    contract = native(Path(config['tools']))
    original = study.read_bytes()
    changed = original + (b'\nraise RuntimeError("Intentional unrelated journal-study import failure")\n'
                          if config['study_state'] == 'failing' else b'\nETL_INDEPENDENCE_CHALLENGE = True\n')
    case.mkdir(parents=True, mode=0o700)
    save(case / 'configuration.json', config)
    shutil.copy2(study, case / 'study-original.py')
    require(import_study(case, 'original-import', study)['returncode'] == 0, 'Original study import failed')
    record = {'version': VERSION, 'chain': config['chain'], 'study_state': config['study_state'],
              'original_sha256': digest(study), 'tool_hashes': contract.verify_bundle(Path(config['tools'])),
              'scenario_sha256': {name: digest(Path(__file__).parent / name) for name in SCENARIO_FILES},
              'challenged_sha256': None if config['study_state'] == 'absent' else hashlib.sha256(changed).hexdigest()}
    save(case / 'challenge.json', record)
    study.rename(case / 'study-backup.py')
    try:
        if config['study_state'] != 'absent':
            with study.open('xb') as stream:
                stream.write(changed)
            study.chmod((case / 'study-original.py').stat().st_mode & 0o777)
        challenge_matches(config, record)
        imported = import_study(case, 'challenged-import', study)
        require((imported['returncode'] == 0) == (config['study_state'] == 'changed'),
                'Challenge did not produce its declared native import outcome')
        if config['study_state'] != 'changed':
            expected = 'FileNotFoundError' if config['study_state'] == 'absent' else 'Intentional unrelated journal-study import failure'
            require(expected in (case / 'challenged-import.stderr').read_text(), 'Unexpected native import failure')
        record.update(challenged_import_returncode=imported['returncode'], applied_at=now())
        save(case / 'challenge.json', record)
    except BaseException:
        try:
            restore(config)
        except Exception as error:
            save(case / 'restoration-error.json', {'error': str(error)})
        raise
    return record


def restore(config):
    case, study = Path(config['case_directory']), Path(config['study_path'])
    record = load(case / 'challenge.json')
    require(digest(case / 'study-original.py') == config['original_sha256'] == record['original_sha256'],
            'Preserved original study changed')
    require(native(Path(config['tools'])).verify_bundle(Path(config['tools'])) == record['tool_hashes'],
            'Native dependency bundle changed')
    if (case / 'restoration.json').exists():
        require(study.is_file() and not study.is_symlink() and digest(study) == record['original_sha256'],
                'Restored study changed')
        return load(case / 'restoration.json')
    challenge_matches(config, record)
    backup = case / 'study-backup.py'
    require(backup.is_file() and digest(backup) == record['original_sha256'], 'Original backup is unavailable')
    if config['study_state'] != 'absent':
        study.rename(case / 'study-challenged.py')
    backup.rename(study)
    imported = import_study(case, 'restored-import', study)
    require(imported['returncode'] == 0 and digest(study) == record['original_sha256'], 'Study restoration failed')
    require(native(Path(config['tools'])).verify_bundle(Path(config['tools'])) == record['tool_hashes'],
            'Native dependency bundle changed')
    result = {'restored_at': now(), 'study_sha256': digest(study), 'import_returncode': imported['returncode']}
    save(case / 'restoration.json', result)
    return result


def freeze_evidence(case, out, tools, record, terminal_path):
    contract = native(tools)
    frozen = case / 'frozen'
    frozen.mkdir()
    state_before = members(out)
    shutil.copytree(out, frozen / 'state')
    require(members(out) == state_before == members(frozen / 'state'), 'Finalized state changed during capture')
    (frozen / 'native').mkdir()
    for name in (*contract.BUNDLE_FILES, 'bundle.json'):
        shutil.copy2(tools / name, frozen / 'native' / name)
    (frozen / 'scenario').mkdir()
    for name in SCENARIO_FILES:
        shutil.copy2(Path(__file__).parent / name, frozen / 'scenario' / name)
    (frozen / 'case').mkdir()
    for path in case.iterdir():
        if path.is_file():
            shutil.copy2(path, frozen / 'case' / path.name)
    startup_before = members(case / 'startup-passes')
    require(bool(startup_before), 'Required startup evidence is missing')
    shutil.copytree(case / 'startup-passes', frozen / 'case' / 'startup-passes')
    require(members(case / 'startup-passes') == startup_before ==
            members(frozen / 'case' / 'startup-passes'), 'Startup evidence changed during capture')
    require(contract.verify_bundle(frozen / 'native') == record['tool_hashes'], 'Frozen native source differs')
    save(case / 'frozen-members.json', {'members': members(frozen)})
    save(case / 'capture.json', {'version': VERSION, 'manifest_sha256': digest(case / 'frozen-members.json'),
         'terminal_sha256': digest(terminal_path), 'scenario_sha256': {name: digest(frozen / 'scenario' / name)
         for name in SCENARIO_FILES}, 'expectation': 'Pending'})


def validate_terminal(terminal, native_status):
    require(terminal.get('terminal_kind') == 'finish', 'Normal-finish terminal required')
    require(terminal.get('verdict') in ('Passed', 'Failed', 'Incomplete'), 'Unsupported native verdict')
    require(native_status == (0 if terminal['verdict'] == 'Passed' else 1), 'Native status differs from saved verdict')
    require(terminal.get('stop', {}).get('rc') == 0 and terminal.get('boot_unchanged'), 'Actual same-boot normal stop required')
    require(terminal.get('monotonic_elapsed_seconds', -1) >= terminal['observation']['duration_seconds'],
            'Native observation duration is incomplete')
    require(terminal.get('evaluation', {}).get('scheduler_verdict') == 'Passed', 'Required ETL evidence is incomplete')


def wait_fresh_ready(config, record, deadline):
    case = Path(config['case_directory'])
    limit = min(deadline, time.monotonic() + READINESS_TIMEOUT)
    attempt = 0
    while True:
        remaining = limit - time.monotonic()
        require(remaining > 0, 'Fresh readiness deadline expired; observation not started')
        challenge_matches(config, record)
        receipt = execute(case, 'readiness-%04d' % attempt,
                          [sys.executable, '-B', str(Path(config['tools']) / 'initialize-fresh.py'), 'check'],
                          min(COMMAND_TIMEOUT, remaining))
        challenge_matches(config, record)
        if receipt['returncode'] == 0:
            return
        attempt += 1
        time.sleep(min(POLL_SECONDS, max(0, limit - time.monotonic())))


def run(config):
    tools, out, case = (Path(config[k]) for k in ('tools', 'state_directory', 'case_directory'))
    contract = native(tools)
    observe, focused = importlib.import_module('observe'), importlib.import_module('focused')
    require(observe.TOOLS.resolve() == tools and observe.OUT.resolve() == out, 'Installed native paths differ from configuration')
    require(all((Path(__file__).parent / name).is_file() for name in SCENARIO_FILES), 'Candidate scenario sources are incomplete')
    with (out.parent / '.etl-independence.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        deadline = time.monotonic() + config['timeout_seconds']
        record = apply_challenge(config)
        runtime = {'version': VERSION, 'chain': config['chain'], 'study_state': config['study_state'],
                   'stage': 'Starting', 'expectation': 'Pending', 'steps': []}
        owned = None

        def step(label, arguments):
            runtime['stage'] = label
            save(case / 'runtime.json', runtime)
            remaining = deadline - time.monotonic()
            require(remaining > 0, 'Case time budget expired')
            receipt = execute(case, label, [sys.executable, '-B', *map(str, arguments)], min(COMMAND_TIMEOUT, remaining))
            runtime['steps'].append({'label': label, **receipt})
            save(case / 'runtime.json', runtime)
            require(receipt['returncode'] == 0, 'Native preparation/start failed: ' + label)
            challenge_matches(config, record)

        try:
            duration = str(config['duration_seconds'])
            if config['preparation_mode'] == 'fresh':
                step('instruments', [tools / 'initialize-fresh.py', 'instruments'])
                wait_fresh_ready(config, record, deadline)
                step('preparation', [tools / 'initialize-fresh.py', 'prepare', '--duration-seconds', duration, '--chain', config['chain']])
            else:
                step('preparation', [tools / 'prepare-retest.py', tools, '--projected-growth-bytes',
                     str(config['projected_growth_bytes']), '--capacity-evidence', config['capacity_evidence'],
                     '--duration-seconds', duration, '--chain', config['chain']])
            step('startup-passes', [Path(__file__).parent / 'wait-etl-startup-v1.py',
                 '--chain', config['chain'], '--output', case / 'startup-passes'])
            startup = load(case / 'startup-passes/state.json')
            require(startup['state'] == 'Ready', 'Actual startup transitions are incomplete')
            probe_challenge(config, record, 'challenge-after-preparation')
            require(not (out / 'observation.json').exists(), 'An existing observation must be preserved')
            remaining = deadline - time.monotonic()
            require(remaining > 0, 'Case time budget expired before chain verification')
            verified = execute(case, 'prelaunch-chain', [sys.executable, '-B', str(tools / 'verify-chain.py'),
                               '--chain', config['chain'], '--duration-seconds', duration],
                               min(COMMAND_TIMEOUT, remaining))
            require(verified['returncode'] == 0, 'Required deployed-chain verification failed; observation not started')
            challenge_matches(config, record)
            require(focused.identity() == startup['actual_identity'], 'Runtime identity changed after startup verification')
            step('launch', [tools / 'launch-retest.py', '--duration-seconds', duration, '--chain', config['chain'],
                 '--cause', 'Verify unrelated-study independence', '--corrective-action', 'Run native health verification'])
            owned = digest(out / 'observation.json')
            manifest = load(out / 'observation.json')
            probe_challenge(config, record, 'challenge-after-launch')
            identity = focused.identity()
            runtime.update(stage='Waiting for actual normal finish', observation_sha256=owned, runtime_identity=identity)
            save(case / 'runtime.json', runtime)
            attempt = 0
            while True:
                observed_identity = None
                require(time.monotonic() < deadline, 'Normal-finish deadline expired')
                challenge_matches(config, record)
                require(digest(out / 'observation.json') == owned, 'Observation identity changed')
                require(not any((out / name).exists() for name in ('abort.json', 'abort-started.json', 'abort-request.json')),
                        'Abort evidence cannot satisfy normal finish')
                terminal_path = out / 'shutdown.json'
                elapsed = time.monotonic() - manifest['monotonic_start']
                if terminal_path.exists() or (out / 'shutdown-started.json').exists() or elapsed >= manifest['duration_seconds']:
                    label = 'finish-state-%04d' % attempt
                    attempt += 1
                    receipt = execute(case, label, ['systemctl', 'show', observe.FINISH + '.service',
                        '-p', 'ActiveState', '-p', 'ExecMainStatus', '-p', 'ExecMainCode', '-p', 'ExecMainStartTimestampMonotonic'], 30)
                    require(receipt['returncode'] == 0, 'Native finish service query failed')
                    props = dict(line.split('=', 1) for line in (case / (label + '.stdout')).read_text().splitlines() if '=' in line)
                    current_worker = int(props.get('ExecMainStartTimestampMonotonic') or 0) >= int(manifest['monotonic_start'] * 1000000)
                    if props.get('ActiveState') in ('inactive', 'failed') and current_worker:
                        terminal = load(terminal_path)
                        require(props.get('ExecMainCode') == '1', 'Finish worker did not exit normally')
                        require(int(props['ExecMainStartTimestampMonotonic']) >= int(terminal['observation']['monotonic_start'] * 1000000),
                                'Finish service belongs to an earlier observation')
                        validate_terminal(terminal, int(props['ExecMainStatus']))
                        runtime['finish_service'] = props
                        break
                else:
                    observed_identity = focused.identity()
                    require(observed_identity == identity, 'Actual appliance lifetime changed')
                with (case / 'checkpoints.jsonl').open('a') as stream:
                    stream.write(json.dumps({'observed_at': now(), 'tool_hashes': record['tool_hashes'],
                                             'observation_sha256': owned, 'runtime_identity': observed_identity}) + '\n')
                time.sleep(POLL_SECONDS)
            challenge_matches(config, record)
            probe_challenge(config, record, 'challenge-after-finish')
            runtime['terminal_sha256'] = digest(terminal_path)
            runtime['restoration'] = restore(config)
            runtime.update(stage='NativeComplete', finished_at=now())
            save(case / 'runtime.json', runtime)
            freeze_evidence(case, out, tools, record, terminal_path)
            return {'stage': runtime['stage'], 'expectation': 'Pending', 'case': str(case)}
        except BaseException as error:
            runtime.update(stage='Incomplete', error_type=type(error).__name__, error=str(error))
            markers = ('abort.json', 'shutdown.json', 'abort-started.json', 'shutdown-started.json')
            if owned and (out / 'observation.json').exists() and digest(out / 'observation.json') == owned and not any((out / n).exists() for n in markers):
                try:
                    runtime['failure_abort'] = execute(case, 'failure-abort', [sys.executable, '-B', str(tools / 'observe.py'),
                        'abort', '--reason', 'Independence candidate failed; preserve original evidence'])
                except Exception as cleanup:
                    runtime['abort_error'] = str(cleanup)
            if not (case / 'restoration.json').exists():
                try:
                    runtime['restoration'] = restore(config)
                except Exception as cleanup:
                    runtime['restoration_error'] = str(cleanup)
            save(case / 'runtime.json', runtime)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'challenge', 'restore', 'run'))
    parser.add_argument('--config', type=Path)
    args = parser.parse_args()
    payload = globals().get('PAYLOAD')
    require((payload is None) != (args.config is None), 'Supply exactly one private configuration source')
    config = configuration(load(args.config) if args.config else payload)
    os.umask(0o077)
    if args.action == 'check':
        study = Path(config['study_path'])
        require(study.is_file() and not study.is_symlink() and digest(study) == config['original_sha256'], 'Original study identity differs')
        require(not Path(config['case_directory']).exists(), 'Case directory already exists')
        result = {'configuration': 'Valid', 'runtime': 'Not run'}
    elif args.action == 'challenge':
        result = apply_challenge(config)
    elif args.action == 'restore':
        result = restore(config)
    else:
        result = run(config)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, KeyError, TypeError, ValueError, RuntimeError, ImportError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(2)
