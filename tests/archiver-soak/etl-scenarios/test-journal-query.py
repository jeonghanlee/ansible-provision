#!/usr/bin/env python3
"""Exercise actual journal component entries against privately declared inputs."""

import argparse
import ast
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

CALLERS = ('run-etl-fault.py', 'run-etl-fault-v2.py')
ROLES = ('sampler', 'abort')
CASES = (
    'positive', 'original-parser-corrected', 'v2-rounded-corrected',
    'bound-exact', 'bound-minus-1us', 'bound-plus-1us', 'bound-plus-1ns',
    'equivalent-z', 'equivalent-zero-offset', 'equivalent-nonzero-offset',
    'fraction-padding', 'empty-selection', 'unrelated-unit', 'after-fault-end', 'replay-positive',
    'missing-bound', 'nonstring-bound', 'missing-timezone', 'invalid-offset-hours',
    'invalid-offset-minutes', 'invalid-negative-offset-minutes', 'invalid-calendar', 'excess-precision',
    'original-parser-refusal', 'v2-rounded-extra', 'native-source-invalid', 'native-source-unreadable',
    'native-launch-denied', 'query-timeout', 'query-interrupted', 'collector-interrupted',
    'malformed-json', 'duplicate-json-field', 'missing-cursor', 'missing-realtime',
    'invalid-realtime', 'missing-boot', 'conflicting-cursor', 'optional-process-name-absent',
    'repeated-occurrence', 'missing-occurrence', 'extra-occurrence', 'changed-payload', 'independent-failure',
    'native-member-missing', 'native-member-extra', 'native-hash-changed', 'candidate-member-missing',
    'candidate-hash-changed', 'context-mismatch', 'context-unit-mismatch', 'output-overlap', 'unknown-mode',
    'normal-bound-wrong', 'normal-unit-wrong', 'replay-source-negative',
    'case-omitted', 'case-duplicated', 'case-unknown', 'snapshot-source-changed',
)
GUARDS = ('case-omitted', 'case-duplicated', 'case-unknown', 'snapshot-source-changed')
FAULTS = ('query-timeout', 'query-interrupted', 'collector-interrupted')
BOUNDARIES = ('bound-exact', 'bound-minus-1us', 'bound-plus-1us', 'bound-plus-1ns')
COMMAND_TIMEOUT = 120


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def load(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()


def members(root):
    values = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Linked source or evidence member')
        if path.is_file():
            values[str(path.relative_to(root))] = digest(path)
    return values


def verify(specification):
    root = Path(specification['root'])
    manifest = Path(specification['manifest'])
    if (not root.is_absolute() or not manifest.is_absolute() or root.is_symlink()
            or digest(manifest) != specification['sha256']
            or members(root) != load(manifest)['members']):
        raise ValueError('Frozen member identity differs')
    return root


def verify_archives(specification):
    manifest = Path(specification['manifest'])
    if digest(manifest) != specification['sha256']:
        raise ValueError('Original archive manifest identity differs')
    data = load(manifest)
    actual = {}
    for name, root in data['roots'].items():
        directory = Path(root)
        if not directory.exists():
            continue
        for path in sorted(directory.rglob('*@*.journal')):
            if path.is_symlink() or not path.is_file():
                raise ValueError('Unusable archived source member')
            actual[str(Path(name) / path.relative_to(directory))] = {
                'path': str(path), 'size': path.stat().st_size, 'sha256': digest(path)}
    if actual != data['members']:
        raise ValueError('Original archived source membership or bytes changed')


def verify_dependencies(specification):
    manifest = Path(specification['manifest'])
    if digest(manifest) != specification['sha256']:
        raise ValueError('Dependency manifest identity differs')
    if any(digest(Path(name)) != expected for name, expected in load(manifest)['files'].items()):
        raise ValueError('Actual execution dependency differs')


def normal_consumption(root, caller):
    tree = ast.parse((root / 'etl-scenarios' / caller).read_text())
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
             and node.func.value.id == 'evidence' and node.func.attr == 'capture_case_journals']
    wanted = [ast.dump(ast.parse(value, mode='eval').body) for value in
              ("observe.OUT / 'observation.json'", 'ROOT', 'Path(__file__).name')]
    if len(calls) != 1 or [ast.dump(value) for value in calls[0].args] != wanted:
        raise ValueError('Normal caller does not consume the production journal operation')
    return {'caller': caller, 'source_sha256': digest(root / 'etl-scenarios' / caller),
            'production_calls': 1, 'arguments': wanted,
            'scope': 'Source consumption only; native behavior is verified by component execution'}


def required_runs(case):
    callers = (CALLERS[0],) if case == 'original-parser-refusal' else (
        (CALLERS[1],) if case == 'v2-rounded-extra' else CALLERS)
    if case in GUARDS:
        return {('runner', None, None)}
    if case == 'collector-interrupted':
        return {(caller, role, number) for caller in callers for role in ROLES
                for number in (signal.SIGINT, signal.SIGTERM)}
    if case in FAULTS + BOUNDARIES:
        return {(caller, role, None) for caller in callers for role in ROLES}
    return {(caller, None, None) for caller in callers}


def inventory(configuration):
    identifiers = [row['id'] for row in configuration['cases']]
    if len(identifiers) != len(set(identifiers)) or set(identifiers) != set(CASES):
        raise ValueError('Required case IDs are omitted, duplicated or unknown')
    expected = []
    for case in configuration['cases']:
        configured = [(run['caller'], run.get('target_role'), run.get('collector_signal'))
                      for run in case['runs']]
        if len(configured) != len(set(configured)) or set(configured) != required_runs(case['id']):
            raise ValueError('Required caller or fault-target cells differ')
        for caller, target, number in configured:
            roles = (target,) if target else ROLES if caller != 'runner' else ('runner',)
            expected += [[case['id'], caller, role, number] for role in roles]
    pinned = load(configuration['cell_inventory']['path'])
    if (digest(configuration['cell_inventory']['path']) != configuration['cell_inventory']['sha256']
            or sorted(expected, key=str) != sorted(pinned['cells'], key=str)):
        raise ValueError('Independent expected cell inventory differs')
    return expected


def process_identity(pid):
    path = Path('/proc') / str(pid)
    try:
        state = (path / 'stat').read_text().rsplit(')', 1)[1].split()
        return {'pid': pid, 'start_ticks': state[19], 'state': state[0],
                'exe': os.readlink(path / 'exe'),
                'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
    except FileNotFoundError:
        return {'pid': pid, 'ended': True}


def owned_identity(expected):
    actual = process_identity(expected['pid'])
    return actual if all(actual.get(key) == expected.get(key)
                         for key in ('pid', 'start_ticks', 'exe', 'boot_id')) else None


def execute(arguments, output, fault=None):
    receipt = {'arguments': arguments, 'started_at': now(), 'pid': None,
               'returncode': None, 'fault': fault, 'fault_exposed': False}
    stdout, stderr = b'', b''
    child_identity = None
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    receipt['pid'] = process.pid
    receipt['component_identity'] = process_identity(process.pid)
    try:
        if fault:
            role = fault['target_role']
            label = 'actual-' + ('sampler' if role == 'sampler' else 'abort-unit') + '-journal'
            running = Path(fault['output']) / (label + '.running.json')
            deadline = time.monotonic() + 15
            while process.poll() is None and time.monotonic() < deadline:
                try:
                    query = load(running)
                    identity = query['process']
                    actual = owned_identity(identity)
                    if actual is None or actual.get('state') == 'Z':
                        break
                    os.kill(identity['pid'], signal.SIGSTOP)
                    child_identity = identity
                    stop_deadline = time.monotonic() + 2
                    while time.monotonic() < stop_deadline:
                        actual = owned_identity(identity)
                        if actual and actual['state'] in ('T', 't'):
                            receipt.update(fault_exposed=True, query_identity=identity,
                                           stopped_identity=actual, stopped_at=now(),
                                           stopped_monotonic_ns=time.monotonic_ns())
                            break
                        time.sleep(0.0002)
                    break
                except (FileNotFoundError, json.JSONDecodeError, KeyError, ProcessLookupError):
                    time.sleep(0.0002)
            if receipt['fault_exposed']:
                if fault['kind'] == 'query-interrupted':
                    assert owned_identity(child_identity)
                    os.kill(child_identity['pid'], signal.SIGTERM)
                    os.kill(child_identity['pid'], signal.SIGCONT)
                elif fault['kind'] == 'collector-interrupted':
                    assert owned_identity(receipt['component_identity'])
                    os.kill(process.pid, fault['collector_signal'])
                receipt['signal_applied_at'] = now()
                receipt['fault_signal_monotonic_ns'] = time.monotonic_ns()
        stdout, stderr = process.communicate(timeout=COMMAND_TIMEOUT)
    except subprocess.TimeoutExpired as error:
        stdout, stderr = error.stdout or b'', error.stderr or b''
        receipt['runner_timeout'] = True
        if child_identity and owned_identity(child_identity):
            os.kill(child_identity['pid'], signal.SIGCONT)
            os.kill(child_identity['pid'], signal.SIGKILL)
        process.kill()
        stdout, stderr = process.communicate()
    finally:
        if child_identity:
            remaining = owned_identity(child_identity)
            if remaining and remaining.get('state') != 'Z':
                os.kill(child_identity['pid'], signal.SIGCONT)
                os.kill(child_identity['pid'], signal.SIGKILL)
                receipt['runner_child_cleanup_required'] = True
                limit = time.monotonic() + 5
                while owned_identity(child_identity) and time.monotonic() < limit:
                    time.sleep(0.001)
            receipt['query_child_ended'] = owned_identity(child_identity) is None
        receipt.update(returncode=process.returncode, finished_at=now())
        (output / 'command.stdout').write_bytes(stdout)
        (output / 'command.stderr').write_bytes(stderr)
        write(output / 'command.json', receipt)
    return receipt, stdout, stderr


def alter(case, context, work, payload):
    key = 'native' if case.startswith('native-') else 'candidate'
    root = Path(context[key]['root'])
    paths = sorted(path for path in root.rglob('*') if path.is_file())
    if case in ('native-member-missing', 'candidate-member-missing'):
        target = root / 'etl-pass/evidence.py' if key == 'candidate' else paths[0]
        target.rename(work / ('removed-' + key))
    elif case in ('native-hash-changed', 'candidate-hash-changed'):
        target = root / 'etl-pass/evidence.py' if key == 'candidate' else paths[0]
        with target.open('ab') as stream:
            stream.write(b'\n')
    elif case == 'native-member-extra':
        (root / 'unexpected-member').write_bytes(b'controlled membership change\n')
    elif case == 'context-mismatch':
        context['case'] = 'E4' if context['case'] == 'E3' else 'E3'
    elif case == 'context-unit-mismatch':
        context['unit_roles']['sampler'] += '.invalid'
    elif case == 'output-overlap':
        payload['output'] = str(Path(context['inputs']['root']) / 'forbidden-output')
    elif case == 'unknown-mode':
        payload['mode'] = 'undeclared-journal-mode'


def run_component(case, specification, destination, archive_guard, dependencies):
    verify_archives(archive_guard)
    verify_dependencies(dependencies)
    source_contract = Path(specification['contract'])
    if digest(source_contract) != specification['contract_sha256']:
        raise ValueError('Frozen case contract identity differs')
    context = copy.deepcopy(load(source_contract))
    work = destination / 'work'
    work.mkdir(mode=0o700)
    protected = {}
    for key in ('candidate', 'inputs', 'native', 'comparison', 'captures'):
        if key not in context:
            continue
        source = verify(context[key])
        protected[key] = copy.deepcopy(context[key])
        target = work / key
        shutil.copytree(source, target)
        manifest = work / (key + '-members.json')
        shutil.copy2(context[key]['manifest'], manifest)
        context[key].update(root=str(target), manifest=str(manifest))
        verify(context[key])
    write(destination / 'normal-consumption.json', normal_consumption(
        Path(context['candidate']['root']), specification['caller']))
    payload = {'role': 'etl', 'chain': context['chain'], 'case': context['case'],
               'mode': specification.get('mode', 'check-journal-query'),
               'contract': str(work / 'contract.json'), 'output': str(work / 'output')}
    alter(case, context, work, payload)
    write(work / 'contract.json', context)
    write(work / 'payload.json', payload)
    write(destination / 'pre-launch.json', {'context': context, 'payload': payload,
                                           'members': members(work), 'protected': protected})
    working_before = {key: members(work / key) for key in protected}
    arguments = [sys.executable, '-B', str(Path(context['candidate']['root']) / 'etl-scenarios/run.py'),
                 '--source', specification['caller'], '--payload', str(work / 'payload.json')]
    fault = None
    if case in FAULTS:
        fault = {'kind': case, 'target_role': specification['target_role'],
                 'collector_signal': specification.get('collector_signal'), 'output': payload['output']}
    receipt, stdout, stderr = execute(arguments, destination, fault)
    output = Path(payload['output'])
    result = load(output / 'result.json') if (output / 'result.json').is_file() else json.loads(stdout)
    expected = specification['expected']
    agrees = receipt['returncode'] == expected['status'] and result['verdict'] == expected['verdict'] and not stderr
    groups = {group['role']: group for group in result.get('groups', [])}
    cells = []
    selected_roles = (specification['target_role'],) if case in FAULTS + BOUNDARIES else ROLES
    for role in selected_roles:
        wanted = expected['groups'][role]
        actual = groups.get(role)
        if actual is None:
            role_agrees = wanted == {'launched': False}
        else:
            role_agrees = all(
                (type(actual.get('returncode')) is int and actual['returncode'] != 0)
                if key == 'native_nonzero' else
                (type(actual.get('returncode')) is int) if key == 'native_status_retained' else
                actual.get(key) == value for key, value in wanted.items())
        cells.append({'case': case, 'caller': specification['caller'], 'role': role,
                      'collector_signal': specification.get('collector_signal'),
                      'expected': wanted, 'actual': actual, 'expectation_met': role_agrees})
        agrees = agrees and role_agrees
    if fault:
        agrees = agrees and receipt['fault_exposed'] and receipt.get('query_child_ended') is True
        agrees = agrees and not receipt.get('runner_child_cleanup_required')
        actual = groups.get(specification['target_role'], {})
        if receipt['fault_exposed']:
            exposure_end = (actual.get('finalization_monotonic_ns') if case == 'query-timeout'
                            else receipt.get('fault_signal_monotonic_ns'))
            receipt['measured_exposure_ns'] = ((exposure_end - receipt['stopped_monotonic_ns'])
                                              if exposure_end is not None else None)
            agrees = agrees and receipt['measured_exposure_ns'] is not None and receipt['measured_exposure_ns'] > 0
            if case == 'query-timeout':
                agrees = (agrees and actual.get('finalization_identity', {}).get('state') in ('T', 't')
                          and actual.get('timeout_observed_monotonic_ns', 0) >= actual.get('deadline_monotonic_ns', 1)
                          and receipt['stopped_monotonic_ns'] < actual.get('deadline_monotonic_ns', 0))
            write(destination / 'command.json', receipt)
    for source in protected.values():
        verify(source)
    working_unchanged = all(members(work / key) == expected for key, expected in working_before.items())
    verify_archives(archive_guard)
    verify_dependencies(dependencies)
    agrees = agrees and working_unchanged
    outcome = {'case': case, 'caller': specification['caller'], 'cells': cells,
               'actual_status': receipt['returncode'], 'actual_verdict': result['verdict'],
               'expectation_met': agrees, 'fault_exposed': receipt['fault_exposed'],
               'working_copies_unchanged': working_unchanged, 'original_archives_unchanged': True}
    write(destination / 'outcome.json', outcome)
    if fault and receipt.get('query_child_ended') is False:
        raise RuntimeError('Unconfirmed query termination blocks later process faults')
    return outcome


def run_guard(case, configuration, destination):
    modified = copy.deepcopy(configuration)
    if case == 'case-omitted':
        modified['cases'] = modified['cases'][1:]
    elif case == 'case-duplicated':
        modified['cases'].append(copy.deepcopy(modified['cases'][0]))
    elif case == 'case-unknown':
        modified['cases'][0]['id'] = 'unknown-case'
    else:
        original = verify(configuration['snapshot_guard'])
        target = destination / 'changed-snapshot'
        shutil.copytree(original, target)
        first = next(path for path in sorted(target.rglob('*')) if path.is_file())
        with first.open('ab') as stream:
            stream.write(b'controlled snapshot change\n')
        modified['snapshot_guard']['root'] = str(target)
    write(destination / 'guard-cases.json', modified)
    arguments = [sys.executable, '-B', str(Path(__file__).resolve()), '--cases',
                 str(destination / 'guard-cases.json'), '--output', str(destination / 'child-output')]
    receipt, stdout, stderr = execute(arguments, destination)
    result = json.loads(stdout)
    outcome = {'case': case, 'caller': 'runner', 'cells': [],
               'expectation_met': receipt['returncode'] == 2 and result['verdict'] == 'Incomplete'
                                  and result['launched_components'] == 0 and not stderr}
    write(destination / 'outcome.json', outcome)
    return outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = {'verdict': 'Incomplete', 'launched_components': 0, 'started_at': now(), 'outcomes': []}
    created = False
    status = 2
    try:
        configuration = load(args.cases)
        expected = inventory(configuration)
        verify(configuration['snapshot_guard'])
        verify_archives(configuration['archive_guard'])
        verify_dependencies(configuration['dependency_guard'])
        if not args.output.is_absolute() or args.output.exists():
            raise ValueError('Fresh absolute output directory required')
        protected_roots = [Path(configuration['snapshot_guard']['root']).resolve()]
        for case in configuration['cases']:
            for run in case['runs']:
                if run['caller'] == 'runner':
                    continue
                context = load(run['contract'])
                protected_roots += [Path(value['root']).resolve() for key, value in context.items()
                                    if isinstance(value, dict) and 'root' in value]
        output = args.output.resolve()
        if any(output == root or root in output.parents or output in root.parents for root in protected_roots):
            raise ValueError('Suite output overlaps frozen inputs')
        output.mkdir(mode=0o700)
        created = True
        write(output / 'expected-cells.json', {'cells': expected})
        shutil.copy2(args.cases, output / 'cases.json')
        for case in configuration['cases']:
            for index, run in enumerate(case['runs']):
                destination = output / (case['id'] + '-' + str(index))
                destination.mkdir(mode=0o700)
                if case['id'] in GUARDS:
                    outcome = run_guard(case['id'], configuration, destination)
                else:
                    attempts = []
                    limit = run.get('maximum_attempts', 1) if case['id'] in FAULTS else 1
                    if type(limit) is not int or limit < 1:
                        raise ValueError('Positive bounded attempt count required')
                    for attempt in range(limit):
                        selected = destination / ('attempt-' + str(attempt))
                        selected.mkdir(mode=0o700)
                        report['launched_components'] += 1
                        outcome = run_component(case['id'], run, selected, configuration['archive_guard'],
                                                configuration['dependency_guard'])
                        attempts.append(outcome)
                        if case['id'] not in FAULTS or outcome['fault_exposed']:
                            break
                    outcome['attempts'] = attempts[:-1]
                report['outcomes'].append(outcome)
                write(output / 'progress.json', report)
        actual = [[row['case'], row['caller'], cell['role'], cell['collector_signal']]
                  for row in report['outcomes'] for cell in row['cells']]
        actual += [[row['case'], 'runner', 'runner', None] for row in report['outcomes'] if row['caller'] == 'runner']
        report['coverage_complete'] = sorted(actual, key=str) == sorted(expected, key=str)
        report['verdict'] = ('Passed' if report['coverage_complete'] and all(
            row['expectation_met'] for row in report['outcomes']) else 'Failed')
        status = 0 if report['verdict'] == 'Passed' else 1
        verify(configuration['snapshot_guard'])
    except Exception as error:
        report.update(error_type=type(error).__name__, error=str(error))
        report['verdict'] = 'Failed' if any(not row['expectation_met'] for row in report['outcomes']) else 'Incomplete'
        status = 1 if report['verdict'] == 'Failed' else 2
    report.update(finished_at=now(), native_exit_status=status,
                  runner_sha256=digest(Path(__file__)), cases_sha256=digest(args.cases))
    if created:
        write(args.output / 'summary.json', report)
    print(json.dumps({key: report[key] for key in ('verdict', 'launched_components', 'native_exit_status')},
                     sort_keys=True))
    return status


if __name__ == '__main__':
    raise SystemExit(main())
