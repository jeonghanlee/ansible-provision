#!/usr/bin/env python3
"""Check shipped health matchers against retained records and explicit negative derivatives."""

import argparse
import copy
import datetime
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--result', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.package))
    import basic
    import long
    import prepare

    prepare.verify(args.package)
    result = json.loads(args.result.read_text())
    prefix = 'Missing or ambiguous required source set: '
    wanted = {value[len(prefix):] for value in result['unresolved'] if value.startswith(prefix)}
    if not wanted:
        raise RuntimeError('An actual unresolved source-set result is required')
    outcomes = {row['id']: row for row in long.rows(args.evidence / 'outcomes.jsonl') if row['id'] in wanted}
    actions = {row['id']: row for row in long.rows(args.evidence / 'schedule.jsonl') if row['id'] in wanted}
    if set(outcomes) != wanted or set(actions) != wanted or any(row['path'] != 'health' for row in actions.values()):
        raise RuntimeError('Every selected case must have its actual health action and outcome')
    config = json.loads((args.evidence / 'package/config.json').read_text())
    cases = {}
    for name, outcome in outcomes.items():
        health = outcome['health']
        cases[name] = {'action': actions[name], 'outcome': outcome, 'records': {},
                       'marker': basic.HEALTH_PREFIX + json.dumps(health, sort_keys=True),
                       'begin': datetime.datetime.fromisoformat(outcome['started']['utc']).timestamp(),
                       'end': datetime.datetime.fromisoformat(outcome['finished']['utc']).timestamp()}
    for entry in long.rows(args.evidence / 'direct/queries.jsonl'):
        stamp = datetime.datetime.fromisoformat(entry['finished']['utc']).timestamp()
        selected = [case for case in cases.values() if case['begin'] - 5 <= stamp <= case['end'] + 90]
        if not selected:
            continue
        for row in long.rows(args.evidence / 'direct' / entry['file']):
            if row.get('_SYSTEMD_UNIT') != basic.HEALTH_UNIT:
                continue
            for case in selected:
                invocation = case['outcome']['health']['invocation_id']
                if row.get('_SYSTEMD_INVOCATION_ID') == invocation or row.get('MESSAGE') == case['marker']:
                    key = basic.identity(row)
                    previous = case['records'].get(key)
                    if previous is not None and previous[0] != row:
                        raise RuntimeError('Retained direct queries disagree about one source identity')
                    case['records'].setdefault(key, (row, entry['finished']))
    checks = []

    def check(case, records, expected, label):
        native = {basic.identity(row): row for row, observed in records}
        direct = basic.required_records(case['action'], case['outcome'],
                                        basic.source_index(native, config), config)
        index = long.Index()
        try:
            for row, observed in records:
                index.add('direct', row, observed)
            indexed = index.required(case['action'], case['outcome'], config)
        finally:
            index.db.close()
        for route, actual in (('direct matcher', len(direct)), ('disk-backed matcher', len(indexed))):
            checks.append({'sequence': case['action']['sequence'], 'case': label,
                           'route': route, 'expected': expected, 'actual': actual,
                           'result': 'Passed' if actual == expected else 'Failed'})

    samples = list(cases.values())
    for number, case in enumerate(samples):
        records = list(case['records'].values())
        markers = [item for item in records if item[0].get('MESSAGE') == case['marker']]
        primary = [item for item in records if basic.HEALTH_MESSAGES[case['outcome']['health']['exit_status']].fullmatch(
            str(item[0].get('MESSAGE', '')))]
        if len(markers) != 1 or len(primary) != 1 or '_SYSTEMD_INVOCATION_ID' in markers[0][0]:
            raise RuntimeError('The actual missing-marker-metadata fixture was not preserved')
        other = samples[(number + 1) % len(samples)]
        other_marker = next(item for item in other['records'].values() if item[0].get('MESSAGE') == other['marker'])
        other_primary = next(item for item in other['records'].values() if item[0].get('MESSAGE') != other['marker'])
        marker, marker_observed = markers[0]
        actual, actual_observed = primary[0]
        check(case, records, 2, 'Unchanged actual marker without journal invocation metadata')
        check(case, [primary[0]], 0, 'Missing completion marker')
        changed = copy.deepcopy(marker)
        changed['_SYSTEMD_INVOCATION_ID'] = other['outcome']['health']['invocation_id']
        check(case, [primary[0], (changed, marker_observed)], 0, 'Conflicting marker invocation metadata')
        changed = copy.deepcopy(marker)
        changed['_SYSTEMD_INVOCATION_ID'] = None
        check(case, [primary[0], (changed, marker_observed)], 0, 'Explicit null marker invocation metadata')
        changed = copy.deepcopy(marker)
        changed['MESSAGE'] = other_marker[0]['MESSAGE']
        check(case, [primary[0], (changed, marker_observed)], 0, 'Marker body from another real action')
        changed = copy.deepcopy(actual)
        changed['_PID'] = other_primary[0]['_PID']
        check(case, [markers[0], (changed, actual_observed)], 0, 'Primary message with another real PID')
        changed = copy.deepcopy(actual)
        changed.pop('_SYSTEMD_INVOCATION_ID')
        check(case, [markers[0], (changed, actual_observed)], 0, 'Primary message without invocation identity')
        changed = copy.deepcopy(other_marker[0])
        changed['MESSAGE'] = marker['MESSAGE']
        changed.pop('_SYSTEMD_INVOCATION_ID', None)
        check(case, records + [(changed, other_marker[1])], 0, 'Distinct source identity duplicating the marker body')
    failed = [check for check in checks if check['result'] != 'Passed']
    print(json.dumps({'result': 'Failed' if failed else 'Passed',
                      'scope': 'retained-record matcher regression; no live observation or source mutation',
                      'actual_cases': len(cases), 'checks': len(checks),
                      'passed': len(checks) - len(failed), 'failures': failed}, sort_keys=True))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
