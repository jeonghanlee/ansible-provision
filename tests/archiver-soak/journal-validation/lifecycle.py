#!/usr/bin/env python3
"""Execute lifecycle scenarios through the real independent journal path."""

import argparse
import collections
import datetime
import json
import os
from pathlib import Path

import basic
import long
import prepare


def check_contract(scenario):
    prepare.verify(basic.PACKAGE)
    start = {'utc': datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc).isoformat(),
             'monotonic_ns': 1000000000}
    policy = long.observation_policy(long.SCENARIOS[scenario]['duration_seconds'], scenario)
    duration = policy['duration_seconds']
    actions = basic.schedule('0' * 32, {'retrieval_url': 'http://127.0.0.1/retrieval'},
                             start, duration, policy['quiet_kernel_windows'])
    kernel = [row for row in actions if row['path'] == 'kernel']
    for begin, end in policy['quiet_kernel_windows']:
        if (any(begin <= row['offset_seconds'] < end for row in kernel) or
                not any(row['offset_seconds'] < begin for row in kernel) or
                not any(row['offset_seconds'] >= end for row in kernel)):
            raise RuntimeError('The real producer schedule does not express the required quiet interval')
        for path in ('system', 'appliance', 'health'):
            if not any(row['path'] == path and begin <= row['offset_seconds'] < end for row in actions):
                raise RuntimeError('A continuing producer is absent from the quiet interval')
    if 'rotation_window_seconds' in policy:
        begin, end = policy['rotation_window_seconds']
        if not basic.COLLECTION_PERIOD < begin < end < 2 * basic.COLLECTION_PERIOD < duration:
            raise RuntimeError('The declared rotation window does not separate native collection intervals')
    if 'rotation_collection_indices' in policy:
        if (policy['rotation_collection_indices'] != [0, 1, 2] or
                duration <= 3 * basic.COLLECTION_PERIOD):
            raise RuntimeError('The declared native query opportunities do not match the bounded scenario')
    if 'obsolete_anchor_removal_window_seconds' in policy:
        begin, end = policy['obsolete_anchor_removal_window_seconds']
        if not (0 < begin < end < basic.COLLECTION_PERIOD < duration and policy['align_collection_with_t0']):
            raise RuntimeError('The obsolete-anchor action does not precede its next native interval')
    return {'scope': 'local-real-fixture-schedule-contract', 'scenario': scenario,
            'planned_actions_by_path': dict(collections.Counter(row['path'] for row in actions)),
            'runtime_acceptance_established': False}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='action', required=True)
    run = subparsers.add_parser('run')
    run.add_argument('scenario', choices=tuple(name for name in long.SCENARIOS
                     if not name.startswith('restart-') and name not in ('failure-termination', 'actual-loss')))
    run.add_argument('--config', type=Path, default=prepare.PREFIX / 'config.json')
    replay = subparsers.add_parser('replay')
    replay.add_argument('directory', type=Path)
    check = subparsers.add_parser('check-contract')
    check.add_argument('--scenario', choices=tuple(long.SCENARIOS), default='quiet-kernel')
    arguments = parser.parse_args()
    if arguments.action == 'check-contract':
        print(json.dumps(check_contract(arguments.scenario), sort_keys=True))
        return 0
    if arguments.action == 'run':
        policy = long.SCENARIOS[arguments.scenario]
        directory, result = long.run(arguments.config, policy['duration_seconds'], arguments.scenario)
    else:
        directory = arguments.directory
        result = long.replay(directory)
    print(json.dumps({'evidence': str(directory), 'result': result}, sort_keys=True))
    return 0 if result['overall'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
