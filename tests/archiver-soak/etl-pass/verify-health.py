#!/usr/bin/env python3
"""Execute health and full collection twice before recording correction verification."""

import argparse
import datetime
import json
import os

import collect
import observe


def verify(cause, corrective_action):
    if not cause.strip() or not corrective_action.strip():
        raise RuntimeError('Documented cause and corrective action are required')
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('Health verification must precede the observation')
    evidence = []
    invocation_ids = set()
    for attempt in range(2):
        began = datetime.datetime.now(datetime.timezone.utc).isoformat()
        observe.checked(['systemctl', 'start', collect.HEALTH_UNIT])
        health = collect.health_properties()
        if not collect.health_succeeded(health):
            raise RuntimeError('The installed health command failed')
        invocation = observe.checked(['systemctl', 'show', collect.HEALTH_UNIT,
                                      '--value', '-p', 'InvocationID'])
        if not invocation or invocation in invocation_ids:
            raise RuntimeError('Distinct completed health invocations are required')
        invocation_ids.add(invocation)
        if collect.sample(observe.OUT, observe.TOOLS / 'pvs-all.csv'):
            raise RuntimeError('The actual full collector failed; evidence is retained')
        latest = json.loads((observe.OUT / 'latest-full.json').read_text())
        state = json.loads((observe.OUT / 'state.json').read_text())
        if invocation not in state.get('health_completed', {}):
            raise RuntimeError('The actual health outcome was not collected')
        evidence.append({'started_at': began, 'health': health, 'invocation_id': invocation,
                         'full_sample': latest['raw_directory']})
    record = {'cause': cause, 'corrective_action': corrective_action,
              'verified_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'boot_id': observe.BOOT.read_text().strip(), 'tool_hashes': observe.tool_hashes(),
              'successful_invocations': len(invocation_ids), 'executions': evidence}
    collect.write_json(observe.OUT / 'health-verification.json', record)
    print(json.dumps({'successful_invocations': len(invocation_ids), 'verified_at': record['verified_at']}))


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cause', required=True)
    parser.add_argument('--corrective-action', required=True)
    args = parser.parse_args()
    with collect.locked(observe.OUT.parent / (observe.OUT.name + '.lifecycle.lock')):
        verify(args.cause, args.corrective_action)


if __name__ == '__main__':
    main()
