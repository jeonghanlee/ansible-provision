#!/usr/bin/env python3
"""Exercise real retained-pass CLIs with declared private ETL fixtures."""

import argparse
import copy
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

CALLERS = ('run-etl-fault.py', 'run-etl-fault-v2.py', 'replay-etl-fault.py')
COMMAND_TIMEOUT = 120
CASES = {
    'original': ('Passed', 0, 'matched_pass', 1),
    'equivalent_offset': ('Passed', 0, 'matched_pass', 1),
    'fraction_padding': ('Passed', 0, 'matched_pass', 1),
    'wrong_transition': ('Failed', 1, 'pass_count', 0),
    'wrong_cadence': ('Failed', 1, 'pass_count', 0),
    'wrong_invocation': ('Failed', 1, 'pass_count', 0),
    'planned_one_ns': ('Failed', 1, 'pass_count', 0),
    'missing_pass': ('Failed', 1, 'pass_count', 0),
    'repeated_cursor': ('Passed', 0, 'matched_pass', 1),
    'distinct_duplicate': ('Failed', 1, 'pass_count', 2),
    'conflicting_cursor': ('Incomplete', 2, 'unusable_pass_input', None),
    'offset_minutes': ('Incomplete', 2, 'unusable_pass_input', None),
    'negative_offset_minutes': ('Incomplete', 2, 'unusable_pass_input', None),
    'offset_hours': ('Incomplete', 2, 'unusable_pass_input', None),
    'missing_timezone': ('Incomplete', 2, 'unusable_pass_input', None),
    'invalid_date': ('Incomplete', 2, 'unusable_pass_input', None),
    'excess_precision': ('Incomplete', 2, 'unusable_pass_input', None),
    'missing_timestamp': ('Incomplete', 2, 'unusable_pass_input', None),
    'nonstring_bound': ('Incomplete', 2, 'unusable_pass_input', None),
    'missing_bound': ('Incomplete', 2, 'unusable_check_input', None),
    'start_inclusive': ('Passed', 0, 'matched_pass', 1),
    'end_inclusive': ('Passed', 0, 'matched_pass', 1),
    'start_one_ns_late': ('Failed', 1, 'pass_interval', 1),
    'end_one_ns_early': ('Failed', 1, 'pass_interval', 1),
    'reversed_pass': ('Failed', 1, 'pass_interval', 1),
    'failed_jobs': ('Failed', 1, 'execution_contract', 1),
    'malformed_input': ('Incomplete', 2, 'unusable_pass_input', None),
    'missing_input': ('Incomplete', 2, 'integrity', None),
    'candidate_changed': ('Incomplete', 2, 'integrity', None),
    'candidate_missing': ('Incomplete', 2, 'integrity', None),
    'original_changed': ('Incomplete', 2, 'integrity', None),
    'observation_binding': ('Incomplete', 2, 'observation_binding', None),
    'caller_identity': ('Incomplete', 2, 'integrity', None),
    'manifest_identity': ('Incomplete', 2, 'integrity', None),
    'invalid_invocation': ('Incomplete', 2, 'invocation', None),
    'independent_failure': ('Failed', 1, 'pass_count', 0),
}
REPLAY_CASES = ('original', 'missing_pass')


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def load(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def members(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Test inputs must not contain symbolic links')
        if path.is_file():
            result[str(path.relative_to(root))] = digest(path)
    return result


def freeze(root, target):
    write(target, {'members': members(root)})
    return {'root': str(root), 'manifest': str(target), 'sha256': digest(target)}


def value_at(root, reference):
    value = load(root / reference['path'])
    for field in reference['field']:
        value = value[field]
    return value


def set_value(root, reference, value, remove=False):
    path = root / reference['path']
    data = load(path)
    parent = data
    for field in reference['field'][:-1]:
        parent = parent[field]
    key = reference['field'][-1]
    if remove:
        del parent[key]
    else:
        parent[key] = value
    write(path, data)


def time_variant(value, operation):
    match = re.fullmatch(r'(.*T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?(Z|[+-]\d{2}:\d{2})', value)
    if not match:
        raise ValueError('The actual fixture must contain valid original timestamp text')
    head, fraction, zone = match.groups()
    nanos = int((fraction or '').ljust(9, '0'))
    if operation in ('plus_ns', 'minus_ns'):
        carry, nanos = divmod(nanos + (1 if operation == 'plus_ns' else -1), 1000000000)
        instant = datetime.datetime.fromisoformat(head + zone.replace('Z', '+00:00'))
        instant += datetime.timedelta(seconds=carry)
        head = instant.strftime('%Y-%m-%dT%H:%M:%S')
    elif operation == 'offset':
        instant = datetime.datetime.fromisoformat(head + zone.replace('Z', '+00:00'))
        instant = instant.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        head, zone = instant.strftime('%Y-%m-%dT%H:%M:%S'), '+09:00'
    elif operation == 'offset_minutes':
        zone = '+00:60'
    elif operation == 'negative_offset_minutes':
        zone = '-00:60'
    elif operation == 'offset_hours':
        zone = '+24:00'
    elif operation == 'missing_timezone':
        zone = ''
    elif operation == 'invalid_date':
        head = head[:5] + '13' + head[7:]
    suffix = str(nanos).zfill(9)
    if operation == 'excess_precision':
        suffix += '0'
    return head + '.' + suffix + zone


def change_messages(rows, field, function):
    pattern = re.compile(r'(' + re.escape(field) + r'=)([^,\]]+)')
    for row in rows:
        row['MESSAGE'] = pattern.sub(lambda match: match[1] + function(match[2]), row['MESSAGE'])


def mutate(name, context, root, check):
    inputs = Path(context['inputs']['root'])
    source = inputs / check['passes']
    rows = [json.loads(line) for line in source.read_text().splitlines() if line.strip()]
    witness = value_at(inputs, check['expected_witness'])
    if name in ('equivalent_offset', 'fraction_padding'):
        for field in ('plannedAt', 'startedAt', 'endedAt'):
            change_messages(rows, field, lambda value: time_variant(value, 'offset' if name == 'equivalent_offset' else 'pad'))
    elif name in ('wrong_transition', 'wrong_cadence'):
        target = load(inputs / check['declaration'])['target_native_sts_pass']
        pattern = re.compile(r'(ETL pass of transition )(\d+)( cadence )(\d+)( s:)')
        for row in rows:
            row['MESSAGE'] = pattern.sub(lambda match: match[1] +
                str(target['transition'] + 1 if name == 'wrong_transition' else int(match[2])) + match[3] +
                str(target['cadence'] + 1 if name == 'wrong_cadence' else int(match[4])) + match[5], row['MESSAGE'])
    elif name == 'wrong_invocation':
        invocation = value_at(inputs, check['identity'])['invocation_id']
        replacement = hashlib.sha256((invocation + name).encode()).hexdigest()[:32]
        assert replacement != invocation
        for row in rows:
            row['_SYSTEMD_INVOCATION_ID'] = replacement
    elif name == 'planned_one_ns':
        change_messages(rows, 'plannedAt', lambda value: time_variant(value, 'plus_ns'))
    elif name == 'missing_pass':
        rows = []
    elif name == 'repeated_cursor':
        rows += copy.deepcopy(rows)
    elif name == 'distinct_duplicate':
        duplicates = copy.deepcopy(rows)
        for row in duplicates:
            row['__CURSOR'] = 'distinct-copy:' + row['__CURSOR']
        rows += duplicates
    elif name == 'conflicting_cursor':
        conflict = copy.deepcopy(rows[0])
        conflict['controlled_conflict'] = True
        rows.append(conflict)
    elif name in ('offset_minutes', 'negative_offset_minutes', 'offset_hours', 'missing_timezone',
                  'invalid_date', 'excess_precision'):
        change_messages(rows, 'plannedAt', lambda value: time_variant(value, name))
    elif name == 'missing_timestamp':
        for row in rows:
            row['MESSAGE'] = re.sub(r'plannedAt=[^,\]]+, ', '', row['MESSAGE'])
    elif name in ('nonstring_bound', 'missing_bound'):
        set_value(inputs, check['begin'], None, remove=name == 'missing_bound')
    elif name in ('start_inclusive', 'start_one_ns_late'):
        value = witness['startedAt']
        set_value(inputs, check['begin'], time_variant(value, 'plus_ns') if name.endswith('late') else value)
    elif name in ('end_inclusive', 'end_one_ns_early'):
        value = witness['endedAt']
        set_value(inputs, check['end'], time_variant(value, 'minus_ns') if name.endswith('early') else value)
    elif name == 'reversed_pass':
        change_messages(rows, 'startedAt', lambda value: time_variant(witness['endedAt'], 'plus_ns'))
    elif name == 'failed_jobs':
        change_messages(rows, 'jobsFailed', lambda value: '1')
    elif name in ('candidate_changed', 'original_changed'):
        key = 'candidate' if name.startswith('candidate') else 'original'
        path = Path(context[key]['root']) / 'heap.jfc'
        path.write_bytes(path.read_bytes() + b'\n')
    elif name == 'candidate_missing':
        (Path(context['candidate']['root']) / 'heap.jfc').unlink()
    elif name == 'observation_binding':
        path = inputs / check['observation']
        observation = load(path)
        observation['tool_hashes']['evidence.py'] = '0' * 64
        write(path, observation)
    elif name == 'caller_identity':
        context['callers'] = dict.fromkeys(context['callers'], '0' * 64)
    elif name == 'manifest_identity':
        context['original']['sha256'] = '0' * 64
    elif name == 'independent_failure':
        rows = []
        broken = copy.deepcopy(check)
        broken['name'] += '-unusable'
        broken['passes'] = check['case'] + '/broken.jsonl'
        (inputs / broken['passes']).write_bytes(source.read_bytes()[:13])
        context['checks'].append(broken)
    source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    if name == 'malformed_input':
        source.write_bytes(source.read_bytes()[:13])
    context['inputs'] = freeze(inputs, root / 'inputs.json')
    if name == 'missing_input':
        source.unlink()


def execute(arguments, root, protected):
    snapshot = root / 'prelaunch'
    shutil.copytree(protected, snapshot)
    before = members(protected)
    write(root / 'before.json', {'members': before, 'snapshot': str(snapshot)})
    receipt = {'argv': arguments, 'cwd': str(Path.cwd()), 'python': sys.version,
               'interpreter_sha256': digest(Path(sys.executable).resolve()), 'input_snapshot': str(snapshot)}
    receipt['started_at'] = now()
    began = time.monotonic_ns()
    actual = subprocess.run(arguments, capture_output=True, timeout=COMMAND_TIMEOUT)
    receipt['elapsed_ns'] = time.monotonic_ns() - began
    receipt['finished_at'] = now()
    (root / 'command.stdout').write_bytes(actual.stdout)
    (root / 'command.stderr').write_bytes(actual.stderr)
    receipt['returncode'] = actual.returncode
    receipt['protected_members_unchanged'] = all(
        (protected / name).is_file() and digest(protected / name) == expected
        for name, expected in before.items())
    write(root / 'command.json', receipt)
    return actual, receipt


def compare_selected(configuration, context, selected, root, control=None):
    check = context['checks'][0]
    inputs = Path(context['inputs']['root'])
    declaration = load(inputs / check['declaration'])['target_native_sts_pass']
    identity = value_at(inputs, check['identity'])
    expected = {'transition': declaration['transition'], 'cadence': declaration['cadence'],
                'invocation_id': identity['invocation_id'], 'plannedAt': declaration['planned_at']}
    write(root / 'expected.json', [expected])
    records = [copy.deepcopy(selected)]
    wanted = 0
    if control == 'identity':
        records[0]['invocation_id'] = hashlib.sha256((identity['invocation_id'] + control).encode()).hexdigest()[:32]
        wanted = 1
    elif control == 'one_ns':
        records[0]['plannedAt'] = time_variant(records[0]['plannedAt'], 'plus_ns')
        wanted = 1
    elif control == 'missing':
        records = []
        wanted = 1
    elif control == 'duplicate':
        records += copy.deepcopy(records)
        wanted = 1
    elif control == 'invalid_timestamp':
        records[0]['plannedAt'] = None
        wanted = 2
    elif control == 'malformed':
        wanted = 2
    write(root / 'actual.json', records)
    if control == 'malformed':
        (root / 'actual.json').write_bytes((root / 'actual.json').read_bytes()[:13])
    write(root / 'comparison.json', {'format': 'json', 'keys': ['transition', 'invocation_id'],
          'timestamps': ['plannedAt'], 'numbers': {'cadence': 'seconds'},
          'fields': ['transition', 'invocation_id', 'cadence', 'plannedAt'], 'allow_empty': False})
    package = root / 'common'
    shutil.copytree(configuration['common_root'], package,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    arguments = [sys.executable, '-B', str(package / 'scripts/compare-evidence.py'),
                 '--config', str(root / 'comparison.json'), '--expected', str(root / 'expected.json'),
                 '--actual', str(root / 'actual.json')]
    before = members(root)
    snapshot = root / 'prelaunch'
    for name in before:
        target = snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
    write(root / 'before.json', {'members': before, 'snapshot': str(snapshot)})
    started = now()
    began = time.monotonic_ns()
    actual = subprocess.run(arguments, capture_output=True, timeout=COMMAND_TIMEOUT)
    elapsed = time.monotonic_ns() - began
    finished = now()
    (root / 'comparison.stdout').write_bytes(actual.stdout)
    (root / 'comparison.stderr').write_bytes(actual.stderr)
    result = json.loads(actual.stdout)
    unchanged = all(digest(root / name) == expected for name, expected in before.items())
    verdict = {0: 'Passed', 1: 'Failed', 2: 'Incomplete'}[wanted]
    agrees = actual.returncode == wanted and result['verdict'] == verdict and not actual.stderr and unchanged
    write(root / 'comparison-receipt.json', {'argv': arguments, 'cwd': str(Path.cwd()),
          'returncode': actual.returncode, 'before': before, 'original_members_unchanged': unchanged,
          'expected_status': wanted, 'actual_verdict': result['verdict'], 'expectation_met': agrees,
          'started_at': started, 'finished_at': finished, 'elapsed_ns': elapsed,
          'tool_sha256': result['tool']['sha256'], 'python': sys.version,
          'interpreter_sha256': digest(Path(sys.executable).resolve())})
    return agrees


def run_case(configuration, fixture, operation, caller, destination):
    work = destination / 'work'
    evidence = destination / 'evidence'
    work.mkdir(mode=0o700)
    evidence.mkdir(mode=0o700)
    context = copy.deepcopy(load(fixture))
    for key in ('inputs', 'original', 'candidate'):
        target = work / key
        shutil.copytree(context[key]['root'], target)
        shutil.copy2(context[key]['manifest'], work / (key + '.json'))
        context[key]['root'] = str(target)
        context[key]['manifest'] = str(work / (key + '.json'))
    scenarios = work / 'scenarios'
    shutil.copytree(configuration['scenario_root'], scenarios)
    check = context['checks'][0]
    if operation != 'original':
        mutate(operation, context, work, check)
    write(work / 'context.json', context)
    if operation == 'invalid_invocation':
        (work / 'context.json').write_text('{')
    output = work / 'output'
    if caller == 'replay-etl-fault.py':
        arguments = [sys.executable, '-B', str(scenarios / caller), '--check-retained-pass',
                     '--contract', str(work / 'context.json'), '--output', str(output)]
    else:
        write(work / 'payload.json', {'role': 'etl', 'chain': check['chain'], 'case': check['case'],
              'mode': 'check-retained-pass', 'contract': str(work / 'context.json'), 'output': str(output)})
        arguments = [sys.executable, '-B', str(scenarios / 'run.py'), '--source', caller,
                     '--payload', str(work / 'payload.json')]
    actual, receipt = execute(arguments, evidence, work)
    result_path = output / 'result.json'
    result = load(result_path) if result_path.is_file() else json.loads(actual.stdout)
    wanted = (('Failed', 1, 'pass_count', 0) if configuration['phase'] == 'pre-fix' else CASES[operation])
    checks = result.get('checks', [])
    detail = checks[0] if checks else result
    agrees = (result['verdict'] == wanted[0] and actual.returncode == wanted[1]
              and detail['reason'] == wanted[2] and detail.get('match_count') == wanted[3]
              and not actual.stderr and receipt['protected_members_unchanged'])
    if operation == 'independent_failure':
        agrees = agrees and len(checks) == 2 and checks[1]['verdict'] == 'Incomplete'
    if agrees and wanted[0] == 'Passed':
        comparison = destination / 'comparison'
        comparison.mkdir(mode=0o700)
        agrees = compare_selected(configuration, context, detail['selected_pass'], comparison)
    outcome = {'case': check['case'], 'operation': operation, 'caller': caller,
               'expectation_met': agrees, 'expected': wanted, 'actual_verdict': result['verdict'],
               'actual_status': actual.returncode, 'actual_reason': detail['reason'],
               'actual_match_count': detail.get('match_count')}
    write(destination / 'outcome.json', outcome)
    return outcome, actual.stdout, actual.stderr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    configuration = load(args.cases)
    if configuration['phase'] not in ('pre-fix', 'corrected') or set(configuration['fixtures']) != {'E3', 'E4'}:
        parser.error('Declare both real E3/E4 fixtures and the pre-fix or corrected phase')
    for case, fixture in configuration['fixtures'].items():
        checks = load(fixture).get('checks', [])
        if len(checks) != 1 or checks[0].get('case') != case:
            parser.error('Each fixture must declare exactly its own E3 or E4 check')
    args.output.mkdir(mode=0o700)
    started = now()
    began = time.monotonic_ns()
    shutil.copy2(args.cases, args.output / 'cases.json')
    outcomes = []
    positive = {}
    operations = ('original',) if configuration['phase'] == 'pre-fix' else tuple(CASES)
    replays = 0
    for case, fixture in configuration['fixtures'].items():
        for operation in operations:
            for caller in CALLERS:
                name = case + '-' + operation + '-' + caller.removesuffix('.py')
                destination = args.output / name
                destination.mkdir(mode=0o700)
                outcome, stdout, stderr = run_case(configuration, fixture, operation, caller, destination)
                outcomes.append(outcome)
                if configuration['phase'] == 'corrected' and operation == 'original' and caller == CALLERS[0]:
                    positive[case] = (load(destination / 'work/context.json'),
                                      load(destination / 'work/output/result.json')['checks'][0]['selected_pass'])
                if configuration['phase'] == 'corrected' and operation in REPLAY_CASES:
                    replay = args.output / (name + '-replay')
                    replay.mkdir(mode=0o700)
                    repeated, new_stdout, new_stderr = run_case(configuration, fixture, operation, caller, replay)
                    repeated['matches_recorded'] = (stdout, stderr, outcome['actual_status']) == (
                        new_stdout, new_stderr, repeated['actual_status'])
                    repeated['expectation_met'] = repeated['expectation_met'] and repeated['matches_recorded']
                    write(replay / 'outcome.json', repeated)
                    outcomes.append(repeated)
                    replays += 1
    shared = []
    for case, (context, selected) in positive.items():
        for control in ('identity', 'one_ns', 'missing', 'duplicate', 'invalid_timestamp', 'malformed'):
            target = args.output / ('shared-' + case + '-' + control)
            target.mkdir(mode=0o700)
            agrees = compare_selected(configuration, context, selected, target, control)
            shared.append({'case': case, 'control': control, 'expectation_met': agrees})
    failures = [row for row in outcomes + shared if not row['expectation_met']]
    report = {'verdict': 'Failed' if failures else 'Passed', 'phase': configuration['phase'],
              'executed_cases': len(outcomes), 'fresh_replays': replays,
              'shared_negative_controls': len(shared), 'failures': failures,
              'suite_sha256': digest(Path(__file__)), 'cases_sha256': digest(args.cases),
              'started_at': started, 'finished_at': now(), 'elapsed_ns': time.monotonic_ns() - began}
    write(args.output / 'summary.json', report)
    print(json.dumps(report, sort_keys=True))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
