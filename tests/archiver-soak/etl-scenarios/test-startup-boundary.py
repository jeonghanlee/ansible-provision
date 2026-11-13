#!/usr/bin/env python3
"""Check actual native startup completion against the observation boundary."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--observation', type=Path, required=True)
    parser.add_argument('--passes', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    os.umask(0o077)
    args.output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(args.tools.resolve()))
    import contract
    import evaluate
    import evidence
    import focused

    result = {'checks': [], 'errors': [], 'sources': {}}
    try:
        result['tools'] = contract.verify_bundle(args.tools)
        for name, path in (('observation', args.observation), ('passes', args.passes),
                           ('test', Path(__file__))):
            result['sources'][name] = {'path': str(path.resolve()),
                                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        manifest = json.loads(args.observation.read_text())
        configuration = contract.chain_configuration(manifest['configuration']['chain'])
        if manifest['configuration'] != configuration:
            raise RuntimeError('Observation configuration differs from the native chain')
        invocation = dict(line.split('=', 1) for line in manifest['unit_before_observation'].splitlines()
                          if '=' in line)['InvocationID']
        records = evaluate.pass_records(args.passes)
        began = evidence.pass_instant(manifest['started_at'])
        for transition, cadence in enumerate(configuration['cadences']):
            rows = [row for row in records if row['invocation_id'] == invocation
                    and row['transition'] == transition and row['cadence'] == cadence]
            if not rows:
                result['errors'].append('Missing actual startup transition: ' + str(transition))
                continue
            first = min(rows, key=lambda row: evidence.pass_instant(row['plannedAt']))
            focused.successful_pass(first)
            ended = evidence.pass_instant(first['endedAt'])
            result['checks'].append({'transition': transition, 'cadence': cadence,
                'startup': first, 'observation_started_at': manifest['started_at'],
                'margin_ns': began - ended, 'passed': ended < began})
    except (OSError, KeyError, ValueError, TypeError, RuntimeError) as error:
        result['errors'].append(type(error).__name__ + ': ' + str(error))
    failed = sum(not row['passed'] for row in result['checks'])
    result['verdict'] = 'Failed' if failed else 'Incomplete' if result['errors'] else 'Passed'
    result['failed'] = failed
    result['passed'] = sum(row['passed'] for row in result['checks'])
    (args.output / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: result[key] for key in ('verdict', 'passed', 'failed', 'errors')}, sort_keys=True))
    return {'Passed': 0, 'Failed': 1, 'Incomplete': 2}[result['verdict']]


if __name__ == '__main__':
    raise SystemExit(main())
