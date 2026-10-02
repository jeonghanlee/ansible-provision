#!/usr/bin/env python3
"""Refresh actual readiness and open the prepared observation at a UTC target."""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import time

import collect
import observe
import contract
import journal_retention


def launch(target, duration, chain):
    contract.preparation(observe.OUT, duration, chain)
    observe.tool_hashes()
    journal_retention.validate(observe.OUT / 'journal-retention-proof.json', observe.TOOLS)
    now = datetime.datetime.now(datetime.timezone.utc)
    target = target or now
    if target.tzinfo is None or not 0 <= (target - now).total_seconds() <= 120:
        raise RuntimeError('Launch target must be within the next 120 seconds with a timezone')
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('An observation already exists')
    record = {'launch_started_at': now.isoformat(), 'target': target.isoformat(),
              'launcher_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    collect.write_json(observe.OUT / 'launch-started.json', record)
    try:
        verification = json.loads((observe.OUT / 'health-verification.json').read_text())
        observe.checked(['/usr/bin/python3', str(observe.TOOLS / 'verify-chain.py'),
                         '--chain', chain, '--duration-seconds', str(duration)])
        observe.checked(['/usr/bin/python3', str(observe.TOOLS / 'verify-health.py'),
                         '--cause', verification['cause'], '--corrective-action', verification['corrective_action']])
        capacity_path = observe.OUT / 'capacity.json'
        capacity = json.loads(capacity_path.read_text())
        source = observe.OUT / 'capacity-input.json'
        if hashlib.sha256(source.read_bytes()).hexdigest() != capacity['input_sha256']:
            raise RuntimeError('Capacity projection input changed')
        minimum = contract.capacity_projection(source, duration, contract.chain_configuration(chain))
        if capacity['projected_growth_bytes'] < minimum:
            raise RuntimeError('Capacity projection no longer covers measured growth')
        filesystem = os.statvfs(collect.STORE)
        capacity.update({'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         'available_bytes': filesystem.f_bavail * filesystem.f_frsize})
        collect.write_json(capacity_path, capacity)
        remaining = (target - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
        if remaining > 0:
            time.sleep(remaining)
        with collect.locked(observe.OUT.parent / (observe.OUT.name + '.lifecycle.lock')):
            observe.start(duration, chain)
    except Exception as error:
        record.update({'failed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       'error': type(error).__name__, 'message': str(error)})
        collect.write_json(observe.OUT / 'launch-failed.json', record)
        raise


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start-at')
    parser.add_argument('--duration-seconds', required=True, type=int, choices=contract.DURATIONS)
    parser.add_argument('--chain', required=True, choices=contract.CHAINS)
    args = parser.parse_args()
    target = (datetime.datetime.fromisoformat(args.start_at.replace('Z', '+00:00')) if args.start_at
              else None)
    launch(target, args.duration_seconds, args.chain)


if __name__ == '__main__':
    main()
