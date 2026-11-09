#!/usr/bin/env python3
"""Check the real pass validator against preserved full and compact preflight records."""

import argparse
import copy
import importlib.util
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runner', type=Path, required=True)
    parser.add_argument('--full', type=Path, required=True)
    parser.add_argument('--compact', type=Path, required=True)
    parser.add_argument('--initial', type=Path, required=True)
    parser.add_argument('--case')
    args = parser.parse_args()
    specification = importlib.util.spec_from_file_location('buffer_runner', args.runner)
    runner = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(runner)
    full = [json.loads(line) for line in args.full.read_text().splitlines()]
    compact = json.loads(args.compact.read_text())
    initial = json.loads(args.initial.read_text())
    require(full and compact and initial, 'Actual retained inputs are required')
    selected = []
    selection_count = 0
    for record in full:
        expected_first = selection_count % 2 == 0
        selected.append((record['pass_id'], record, expected_first))
        if record['phase'] in (2, 3):
            selection_count += 1
    last = next(item for item in selected if item[1]['phase'] in (2, 3) and not item[2])
    pass_id, last_full, expected_first = last
    last_compact = compact[str(pass_id)]
    cases = {}

    def accepted(records):
        rejected = []
        for identity, record, first in records:
            try:
                runner.validate_pass(identity, record, first)
            except runner.Incomplete as error:
                rejected.append({'pass_id': identity, 'reason': str(error)})
        require(not rejected, 'Valid retained records refused: ' + json.dumps(rejected))

    cases['full'] = lambda: accepted(selected)
    cases['compact'] = lambda: accepted(
        [(identity, compact[str(identity)], first) for identity, _, first in selected])

    def pairing():
        require(len(full) == len(compact) == len({item[0] for item in selected}),
                'Full and compact pass identities differ or repeat')
        require(set(compact) == {str(item[0]) for item in selected}, 'Pass membership differs')
        for identity, record, _ in selected:
            reduced = compact[str(identity)]
            writes = record['writes']
            boundaries = writes[:1] + writes[-1:] if len(writes) > 1 else writes
            require(reduced['write_count'] == len(writes), 'Observed write counts differ')
            require(reduced['writes'] == boundaries, 'Retained boundary writes differ')
            for field in ('phase', 'requested', 'injections', 'ended', 'start', 'end'):
                require(reduced[field] == record[field], 'Pass evidence differs: ' + field)

    cases['pairing'] = pairing

    def refused(record, prefix, identity=pass_id, first=expected_first):
        try:
            runner.validate_pass(identity, record, first)
        except runner.Incomplete as error:
            require(str(error).startswith(prefix), 'Unexpected refusal: ' + str(error))
        else:
            raise AssertionError('Invalid retained evidence accepted: ' + prefix)

    def actual_missing():
        record = initial['16']
        require(record['phase'] in (2, 3) and not record['injections'],
                'The actual initial missing-injection pass is required')
        refused(record, 'Missing or duplicate native injection', identity=16, first=False)

    cases['actual-missing'] = actual_missing

    def altered(name, change, prefix, formats=('full', 'compact')):
        def check():
            for form in formats:
                record = copy.deepcopy(last_full if form == 'full' else last_compact)
                change(record)
                refused(record, prefix)
        cases[name] = check

    altered('missing', lambda r: r['injections'].clear(), 'Missing or duplicate native injection')
    altered('duplicate', lambda r: r['injections'].append(copy.deepcopy(r['injections'][0])),
            'Missing or duplicate native injection')
    altered('short-delay', lambda r: r['injections'][0].update(wait=r['requested'] - 1),
            'Delay was not demonstrated')
    altered('native-error', lambda r: r['injections'][0].update(error=1), 'Delay was not demonstrated')
    altered('alternation', lambda r: r['injections'][0].update(position=0),
            'First/last native-write alternation failed')
    altered('final-flush', lambda r: r['injections'][0].update(final_flush=False),
            'Last-write injection did not occur')
    altered('count-type', lambda r: r.update(write_count=True), 'Invalid native-write count', ('compact',))
    altered('count-zero', lambda r: r.update(write_count=0), 'Invalid native-write count', ('compact',))
    altered('count-value', lambda r: r.update(write_count=r['write_count'] - 1),
            'Native-write positions disagree', ('compact',))
    altered('compact-length', lambda r: r['writes'].pop(), 'Native-write positions disagree', ('compact',))
    altered('compact-boundary', lambda r: r['writes'][-1].update(position=1),
            'Native-write positions disagree', ('compact',))
    altered('full-sequence', lambda r: r['writes'][1].update(position=0),
            'Native-write positions disagree', ('full',))
    if args.case:
        require(args.case in cases, 'Unknown case: ' + args.case)
        cases = {args.case: cases[args.case]}
    results = []
    for name, check in cases.items():
        try:
            check()
        except Exception as error:
            results.append({'case': name, 'result': 'Failed', 'reason': str(error)})
        else:
            results.append({'case': name, 'result': 'Passed'})
    failed = sum(result['result'] == 'Failed' for result in results)
    print(json.dumps({'results': results, 'failed': failed, 'full_passes': len(full),
                      'eligible_passes': sum(r['phase'] in (2, 3, 4) for r in full),
                      'main_revalidation': 'Incomplete: original pass inputs unavailable'}, sort_keys=True))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
