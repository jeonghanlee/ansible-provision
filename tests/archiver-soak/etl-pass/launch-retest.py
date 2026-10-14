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
import focused


def launch(target, duration, chain, cause=None, corrective_action=None):
    """Refresh readiness evidence and open the observation at the target.

    Every refresh step is run and its failure recorded in `launch-started.json`; only the start's
    own refusals (an existing observation, free space below the reserve) stop the launch.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    target = target or now
    if target.tzinfo is None or not 0 <= (target - now).total_seconds() <= 120:
        raise RuntimeError('Launch target must be within the next 120 seconds with a timezone')
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('An observation already exists')
    findings = []
    record = {'launch_started_at': now.isoformat(), 'target': target.isoformat(),
              'launcher_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'findings': findings}

    def recorded(name, action):
        try:
            return action()
        except Exception as error:
            findings.append({'check': name, 'type': type(error).__name__, 'message': str(error)})
            return None

    recorded('preparation', lambda: contract.preparation(observe.OUT, duration, chain))
    recorded('tool_bundle', observe.tool_hashes)
    collect.write_json(observe.OUT / 'launch-started.json', record)
    try:
        recorded('verify_chain', lambda: observe.checked(['/usr/bin/python3', str(observe.TOOLS / 'verify-chain.py'),
                                                          '--chain', chain, '--duration-seconds', str(duration)]))
        stored = recorded('health_verification', lambda: json.loads(
            (observe.OUT / 'health-verification.json').read_text())) or {}
        cause = cause or stored.get('cause')
        corrective_action = corrective_action or stored.get('corrective_action')
        if cause and corrective_action:
            recorded('verify_health', lambda: observe.checked(['/usr/bin/python3', str(observe.TOOLS / 'verify-health.py'),
                                                               '--cause', cause, '--corrective-action', corrective_action]))

        recorded('focused_continuity', lambda: focused.continuity(focused.ROOT / chain, chain))
        if recorded('readiness_sample', lambda: collect.sample(observe.OUT, observe.TOOLS / 'pvs-all.csv')):
            findings.append({'check': 'readiness_sample', 'message': 'Final launch readiness collection recorded errors'})
        collect.write_json(observe.OUT / 'launch-started.json', record)
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
    parser.add_argument('--cause', help='documented cause for an optional health verification, recorded only')
    parser.add_argument('--corrective-action', help='documented corrective action for the optional health verification')
    args = parser.parse_args()
    target = (datetime.datetime.fromisoformat(args.start_at.replace('Z', '+00:00')) if args.start_at
              else None)
    launch(target, args.duration_seconds, args.chain, args.cause, args.corrective_action)


if __name__ == '__main__':
    main()
