#!/usr/bin/env python3
"""Exercise retained JFR consumers with explicit real inputs and native receipts."""

import argparse
import collections
import csv
import datetime
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

KINDS = {'heap': ('gc-heap.csv', 'heap_events'), 'collection': ('gc-collections.csv', 'collection_events'),
         'pause': ('gc-pauses.csv', 'pause_events')}
COMPONENTS = ('mgmt', 'engine', 'etl', 'retrieval')
CASES = ('equivalent_offset', 'one_ns', 'missing_event', 'extra_event', 'payload', 'balanced_prefix',
         'wrong_component', 'wrong_pid', 'wrong_start', 'pid_reuse', 'missing_boot',
         'missing_metadata', 'damaged_jfr', 'truncated_jfr', 'malformed_csv', 'failed_and_missing',
         'first_edge', 'last_edge', 'sub_ns', 'wrong_chain', 'missing_empty_snapshot')


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def members(root):
    result = {}
    for path in sorted(root.rglob('*')):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            raise ValueError('Replay inputs must contain regular files and directories')
        if path.is_file():
            result[relative] = {'sha256': digest(path), 'mode': path.stat().st_mode & 0o7777}
    return result


def copy_tree(source, target):
    subprocess.run(['cp', '-a', '--reflink=auto', str(source), str(target)], check=True)


def run(root, name, argv, checks=()):
    for source, expected in checks:
        assert members(source) == expected, 'Pre-launch input/tool membership changed'
    start = time.monotonic()
    receipt = {'argv': [str(arg) for arg in argv], 'cwd': str(root),
               'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'verified_roots': [str(source) for source, _ in checks]}
    write(root / (name + '.command.json'), receipt)
    with (root / (name + '.stdout')).open('wb') as out, (root / (name + '.stderr')).open('wb') as err:
        native = subprocess.run(receipt['argv'], cwd=root, stdout=out, stderr=err)
    receipt.update(returncode=native.returncode, elapsed_seconds=time.monotonic() - start,
                   stdout_sha256=digest(root / (name + '.stdout')), stderr_sha256=digest(root / (name + '.stderr')))
    write(root / (name + '.command.json'), receipt)
    return native.returncode


def csv_rows(path):
    with path.open(newline='') as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def write_csv(path, header, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def json_file(path):
    return json.loads(path.read_text())


def shift_ns(value):
    match = re.fullmatch(r'(.*T\d\d:\d\d:\d\d)(?:\.(\d+))?(Z|[+-]\d\d:\d\d)', value)
    fraction = int((match[2] or '').ljust(9, '0'))
    base = datetime.datetime.fromisoformat(match[1] + match[3].replace('Z', '+00:00'))
    seconds, nanos = divmod(fraction + 1, 1000000000)
    return (base + datetime.timedelta(seconds=seconds)).strftime('%Y-%m-%dT%H:%M:%S') + f'.{nanos:09d}' + match[3]


def mutate(state, case, component, kind):
    if case == 'wrong_chain':
        return 'Failed'
    terminal_path = state / 'shutdown.json'
    terminal = json_file(terminal_path)
    observation = json_file(state / 'observation.json')
    pid = str(observation['jvm_identity'][component]['pid'])
    source = state / KINDS[kind][0]
    header, rows = csv_rows(source)
    indices = [i for i, row in enumerate(rows) if row['component'] == component and row['pid'] == pid]
    count = terminal['complete_gc_recordings'][component][KINDS[kind][1]]
    assert count and len(indices) > count
    index = indices[-1]
    expected = 'Failed'
    if case == 'equivalent_offset':
        value = rows[index]['ts']
        match = re.fullmatch(r'(.*T\d\d:\d\d:\d\d)(\.\d+)?(Z|[+-]\d\d:\d\d)', value)
        instant = datetime.datetime.fromisoformat(match[1] + match[3].replace('Z', '+00:00'))
        changed = instant.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
        rows[index]['ts'] = changed.strftime('%Y-%m-%dT%H:%M:%S') + (match[2] or '') + '+01:00'
        expected = 'Passed'
    elif case in ('one_ns', 'first_edge', 'last_edge'):
        if case in ('first_edge', 'last_edge'):
            select = min if case == 'first_edge' else max
            index = select(indices[-count:], key=lambda i: rows[i]['ts'])
        rows[index]['ts'] = shift_ns(rows[index]['ts'])
    elif case == 'missing_event':
        rows.pop(index)
    elif case == 'extra_event':
        rows.insert(index, dict(rows[index]))
    elif case == 'payload':
        field = 'heap_bytes' if kind == 'heap' else 'duration'
        rows[index][field] = str(int(rows[index][field]) + 1) if kind == 'heap' else 'PT123S'
    elif case == 'balanced_prefix':
        prefix = indices[:-count]
        left = prefix[0]
        right = next(i for i in prefix if rows[i] != rows[left])
        rows[left] = dict(rows[right])
    elif case == 'wrong_component':
        rows[index]['component'] = next(item for item in COMPONENTS if item != component)
    elif case == 'wrong_pid':
        rows[index]['pid'] = str(max(int(row['pid']) for row in rows) + 1)
    elif case in ('wrong_start', 'pid_reuse'):
        path = state / 'processes.csv'
        fields, process_rows = csv_rows(path)
        selected = [row for row in process_rows if row['name'] == component and row['pid'] == pid]
        for row in selected if case == 'wrong_start' else selected[:1]:
            row['start'] = str(int(row['start']) + 1)
        write_csv(path, fields, process_rows)
        expected = 'Incomplete' if case == 'pid_reuse' else 'Failed'
    elif case == 'missing_boot':
        observation.pop('boot_id')
        terminal['observation'] = observation
        write(state / 'observation.json', observation)
        expected = 'Incomplete'
    elif case == 'missing_metadata':
        terminal['complete_gc_recordings'].pop(component)
        expected = 'Incomplete'
    elif case in ('damaged_jfr', 'truncated_jfr'):
        recording = terminal['complete_gc_recordings'][component]
        path = state / recording['recording_path']
        with path.open('r+b') as stream:
            stream.truncate(path.stat().st_size // 2)
        if case == 'truncated_jfr':
            recording.update(recording_sha256=digest(path), recording_bytes=path.stat().st_size)
            expected = 'Incomplete'
    elif case == 'sub_ns':
        if kind == 'heap':
            source = state / 'gc-pauses.csv'
            header, rows = csv_rows(source)
            index = next(i for i in range(len(rows) - 1, -1, -1)
                         if rows[i]['component'] == component and rows[i]['pid'] == pid)
        match = re.fullmatch(r'PT(\d+(?:\.\d+)?)S', rows[index]['duration'])
        if not match:
            raise ValueError('Sub-nanosecond case requires a real seconds-format duration')
        rows[index]['duration'] = 'PT' + format(Decimal(match[1]) + Decimal('0.0000000001'), 'f') + 'S'
        expected = 'Incomplete'
    elif case == 'missing_empty_snapshot':
        selected = next((path for path in sorted((state / 'raw').glob('*/sample.json'))
                         if (entry := json_file(path).get('gc', {}).get(component))
                         and str(entry['pid']) == pid and all(entry[field] == 0 for _, field in KINDS.values())), None)
        if selected is None:
            raise ValueError('This fixture has no actual empty snapshot for the selected component')
        selected.rename(state.parent.parent / 'removed-snapshot.json')
        expected = 'Incomplete'
    elif case == 'malformed_csv':
        source.write_text(source.read_text() + 'invalid,width\n')
        expected = 'Incomplete'
    elif case == 'failed_and_missing':
        rows[index]['ts'] = shift_ns(rows[index]['ts'])
        terminal['complete_gc_recordings'].pop(next(item for item in COMPONENTS if item != component))
    else:
        raise ValueError(case)
    if case != 'malformed_csv':
        write_csv(source, header, rows)
    write(terminal_path, terminal)
    return expected


def independent_records(native, identity, kind):
    """Convert native JDK output independently of the production selector/parser."""
    event_type = {'heap': 'jdk.GCHeapSummary', 'collection': 'jdk.GarbageCollection',
                  'pause': 'jdk.GCPhasePause'}[kind]
    for event in native['recording']['events']:
        if event['type'] != event_type:
            continue
        values = event['values']
        row = {**identity, 'kind': kind, 'ts': values['startTime'], 'gc_id': str(values['gcId'])}
        if kind == 'heap':
            row.update(when=values['when'], heap_bytes=values['heapUsed'])
        else:
            row['name'] = values['name']
            if kind == 'collection':
                row['cause'] = values['cause']
            else:
                row['phase_identity'] = 'jdk.GCPhasePause'
            for field in ('duration', 'sumOfPauses', 'longestPause') if kind == 'collection' else ('duration',):
                parts = re.fullmatch(r'PT(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?', values[field])
                row[field] = int(sum(Decimal(v or '0') * scale for v, scale in zip(parts.groups(), (3600, 60, 1))) * 10**9)
        yield row


def common_comparisons(root, native_root, state, comparator, components=COMPONENTS, kinds=KINDS, expected_status=None):
    observation = json_file(state / 'observation.json')
    results = []
    for component in components:
        identity = {'component': component, 'boot_id': observation['boot_id'],
                    'pid': str(observation['jvm_identity'][component]['pid']),
                    'start': observation['jvm_identity'][component]['start']}
        captures = sorted((native_root / component).glob('capture-*'), key=lambda p: int(p.name.split('-')[1]))
        for kind in kinds:
            for population, selected in (('raw', captures), ('final', captures[-1:])):
                name = component + '-' + kind + '-' + population
                expected = root / (name + '-independent.jsonl')
                with expected.open('w') as output:
                    for capture in selected:
                        receipt = json_file(capture / 'command.json')
                        assert receipt['returncode'] == 0 and digest(Path(receipt['argv'][-1])) == receipt['input_sha256']
                        for row in independent_records(json_file(capture / 'stdout'), identity, kind):
                            output.write(json.dumps(row, sort_keys=True) + '\n')
                numbers = {'heap_bytes': 'bytes'} if kind == 'heap' else {'duration': 'ns'}
                if kind == 'collection':
                    numbers.update(sumOfPauses='ns', longestPause='ns')
                configuration = {'format': 'jsonl', 'keys': ['component', 'boot_id', 'pid', 'start', 'kind', 'gc_id'],
                                 'timestamps': ['ts'], 'numbers': numbers, 'required': [], 'optional': [],
                                 'fields': None, 'allow_empty': True}
                config = root / (name + '-contract.json'); write(config, configuration)
                actual = native_root / component / (kind + '-' + population + '-actual.jsonl')
                argv = [sys.executable, '-B', comparator, '--config', config, '--expected', expected, '--actual', actual]
                # The complete case and package were verified before the consumer; these exact comparison inputs are frozen here.
                write(root / (name + '-inputs.json'), {str(p): digest(p) for p in (config, expected, actual, comparator)})
                status = run(root, 'common-' + name, argv)
                results.append({'component': component, 'kind': kind, 'population': population, 'status': status})
                assert status == (expected_status or {}).get(population, 0)
    write(root / 'common-comparisons.json', results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--phase', choices=('positive', 'negative', 'all'), default='all')
    parser.add_argument('--cases', nargs='+', choices=CASES, default=list(CASES[:-1]))
    parser.add_argument('--chains', nargs='+', choices=('shortened', 'default'), default=['shortened', 'default'])
    parser.add_argument('--component', choices=COMPONENTS)
    args = parser.parse_args()
    config = json_file(args.config)
    root = Path(config['output']).resolve(); root.mkdir(parents=True, exist_ok=False)
    write(root / 'config.json', config)
    write(root / 'selection.json', {'phase': args.phase, 'cases': args.cases, 'chains': args.chains,
                                   'component': args.component})
    candidate_source = Path(config['candidate']).resolve()
    common_source = Path(config['comparator']).resolve().parent
    candidate = root / 'candidate'; copy_tree(candidate_source, candidate)
    common = root / 'common'; copy_tree(common_source, common)
    comparator = common / Path(config['comparator']).name
    diagnostic = root / 'full-day.py'; shutil.copy2(config['diagnostic'], diagnostic)
    run(root, 'freeze-candidate', [sys.executable, '-B', candidate / 'contract.py', '--freeze', candidate])
    candidate_members, common_members = members(candidate), members(common)
    write(root / 'candidate-members.json', candidate_members); write(root / 'common-members.json', common_members)
    jfr = Path(config['jfr']).resolve()
    dependencies = {'python': {'version': sys.version, 'path': sys.executable, 'sha256': digest(Path(sys.executable).resolve())},
                    'jfr': {'path': str(jfr), 'sha256': digest(jfr)}, 'diagnostic_sha256': digest(diagnostic)}
    write(root / 'dependencies.json', dependencies)
    outcomes = []
    for chain in args.chains:
        original = Path(config['chains'][chain]).resolve()
        original_members = members(original)
        write(root / (chain + '-original-members.json'), original_members)
        cases = [('positive', None, None)] if args.phase != 'negative' else []
        if args.phase != 'positive':
            cases += [(case, args.component or COMPONENTS[index % len(COMPONENTS)],
                       'pause' if case == 'sub_ns' else list(KINDS)[index % len(KINDS)])
                      for index, case in enumerate(args.cases)]
        for case, component, kind in cases:
            case_root = root / (chain + '-' + case); case_root.mkdir()
            fixture = case_root / 'input'; copy_tree(original, fixture)
            assert members(fixture) == original_members
            expected = 'Passed'
            if case != 'positive':
                expected = mutate(fixture / 'state', case, component, kind)
            frozen = members(fixture)
            write(case_root / 'members.json', frozen)
            write(case_root / 'changed-members.json', {name: value for name, value in frozen.items()
                                                       if original_members.get(name) != value})
            checks = ((fixture, frozen), (candidate, candidate_members), (common, common_members))
            if case == 'positive':
                for old_caller in ('evaluate', 'aggregate'):
                    old_argv = [sys.executable, '-B', fixture / 'tools' / (old_caller + '.py'), '--input', fixture / 'state']
                    if old_caller == 'aggregate':
                        old_argv += ['--output', case_root / 'original-aggregate.json']
                    old_native = run(case_root, 'original-' + old_caller, old_argv, checks)
                    old_result = json_file(case_root / ('original-aggregate.json' if old_caller == 'aggregate' else 'original-evaluate.stdout'))
                    assert old_native == 1 and old_result['verdict'] == 'Incomplete'
                    assert all('jfr_export_' + kind + '_coverage' in old_result['missing_coverage'] for kind in KINDS)
            callers = ['evaluate', 'aggregate', 'diagnostic'] if case == 'positive' else ['evaluate']
            if case == 'failed_and_missing':
                callers = ['evaluate', 'aggregate']
            if case == 'wrong_chain':
                callers = ['diagnostic']
            for caller in callers:
                native_root = case_root / (caller + '-native')
                argv = [sys.executable, '-B', diagnostic if caller == 'diagnostic' else candidate / (caller + '.py'),
                        '--input', fixture / 'state', '--jfr-binary', jfr, '--jfr-output', native_root]
                if caller == 'diagnostic':
                    argv += ['--tools', candidate, '--chain',
                             ('default' if chain == 'shortened' else 'shortened') if case == 'wrong_chain' else chain,
                             '--recordings-only']
                if caller == 'aggregate':
                    argv += ['--output', case_root / 'aggregate.json']
                if case not in ('positive', 'failed_and_missing'):
                    argv += ['--recordings-only', '--recording-component', component]
                native = run(case_root, caller, argv, checks)
                result = json_file(case_root / ('aggregate.json' if caller == 'aggregate' else caller + '.stdout'))
                recordings = result.get('jfr_recordings', result)
                expected_native = 1 if case in ('positive', 'failed_and_missing') and caller != 'diagnostic' else {'Passed': 0, 'Failed': 1, 'Incomplete': 2}[expected]
                outcome = {'chain': chain, 'case': case, 'component': component, 'kind': kind, 'caller': caller,
                           'expected': expected, 'observed': recordings['verdict'], 'native_status': native,
                           'expected_native': expected_native, 'failed_assertions': recordings['failed_assertions'],
                           'missing_coverage': recordings['missing_coverage']}
                outcome['passed'] = recordings['verdict'] == expected and native == expected_native
                if case == 'failed_and_missing':
                    outcome['passed'] &= bool(recordings['missing_coverage']) and bool(result['failed_assertions'])
                if case == 'positive' and caller != 'diagnostic':
                    outcome['passed'] &= result['verdict'] == 'Incomplete' and 'tool_bundle_changed' in result['failed_assertions']
                    outcome['passed'] &= any('kernel' in item for item in result['missing_coverage'])
                outcomes.append(outcome); write(root / 'results.json', outcomes)
                print(json.dumps({k: outcome[k] for k in ('chain', 'case', 'caller', 'observed', 'passed')}), flush=True)
                if case == 'positive' and caller == 'evaluate' and outcome['passed']:
                    common_comparisons(case_root, native_root, fixture / 'state', comparator)
                if case in ('equivalent_offset', 'one_ns', 'missing_event', 'extra_event', 'payload',
                            'balanced_prefix', 'wrong_component', 'wrong_pid', 'first_edge', 'last_edge'):
                    expected_common = {'raw': 0 if case == 'equivalent_offset' else 1,
                                       'final': 0 if case in ('equivalent_offset', 'balanced_prefix') else 1}
                    common_comparisons(case_root, native_root, fixture / 'state', comparator,
                                       (component,), (kind,), expected_common)
                assert members(fixture) == frozen and members(candidate) == candidate_members
            if case == 'positive':
                replay = case_root / 'replay-input'; copy_tree(original, replay)
                replay_argv = [sys.executable, '-B', diagnostic, '--tools', candidate, '--chain', chain,
                               '--input', replay / 'state', '--recordings-only', '--jfr-binary', jfr,
                               '--jfr-output', case_root / 'replay-native']
                native = run(case_root, 'replay', replay_argv, ((replay, original_members), (candidate, candidate_members)))
                replay_result = json_file(case_root / 'replay.stdout')
                first = json_file(case_root / 'diagnostic.stdout')
                same = lambda value: {key: item for key, item in value.items() if key != 'evidence_directory'}
                assert native == 0 and same(replay_result) == same(first)
                assert members(replay) == original_members
                write(case_root / 'replay-comparison.json', {'matched': True, 'native_status': native})
            assert members(original) == original_members
        write(root / (chain + '-preservation.json'), {'unchanged': members(original) == original_members})
    write(root / 'summary.json', {'cases': len(outcomes), 'passed': sum(row['passed'] for row in outcomes),
                                'failed': sum(not row['passed'] for row in outcomes)})
    return int(any(not row['passed'] for row in outcomes))


if __name__ == '__main__':
    raise SystemExit(main())
