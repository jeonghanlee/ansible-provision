#!/usr/bin/env python3
"""Obtain current native runtime proofs without opening an observation."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

TOOLS = Path('/usr/local/share/etl-soak')
STARTUP_WAITER = Path('/var/lib/etl-negative-orchestration/wait-etl-startup-v1.py')
STARTUP_WAITER_SHA256 = 'd6e2dfdaec47c1ad89859a9c6ce7a720c2cffde18cd33b2cd701df80e0758219'



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chain', choices=('shortened', 'default'), required=True)
    parser.add_argument('--case', choices=('E3', 'E4'), required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(TOOLS))
    import contract
    import focused
    import observe
    root = Path('/var/lib/etl-negative-cases') / (args.chain + '-' + args.case) / 'native-preflight'
    root.mkdir(mode=0o700)
    assert not (observe.OUT / 'observation.json').exists()
    prepared = contract.preparation(observe.OUT, 86400, args.chain)
    assert not prepared['findings']
    state = {'stage': 'Starting', 'steps': []}

    def run(label, arguments, timeout=600):
        state['stage'] = label
        (root / 'state.json').write_text(json.dumps(state, indent=2))
        proof = observe.OUT / 'health-verification.json'
        if label.startswith('health-') and proof.exists():
            shutil.copy2(proof, root / (label + '-previous-proof.json'))
        began = focused.now()
        actual = subprocess.run([sys.executable, '-B', *map(str, arguments)], capture_output=True, timeout=timeout)
        (root / (label + '.stdout')).write_bytes(actual.stdout)
        (root / (label + '.stderr')).write_bytes(actual.stderr)
        state['steps'].append({'name': label, 'started_at': began, 'finished_at': focused.now(),
                               'returncode': actual.returncode})
        assert actual.returncode == 0, 'An actual native runtime proof failed: ' + label

    def health(label):
        run(label, [TOOLS / 'verify-health.py', '--cause', 'Verify the current case before a declared filesystem fault',
            '--corrective-action', 'Execute two actual health invocations with unchanged native full capture'])

    try:
        health('health-before-empty')
        run('negative-readiness', [TOOLS / 'verify-runtime.py', 'empty', '--duration-seconds', '86400', '--chain', args.chain])
        health('health-before-terminal')
        run('actual-installed-terminal', [TOOLS / 'verify-runtime.py', 'abort', '--duration-seconds', '86400',
            '--chain', args.chain], 1200)
        deadline = time.monotonic() + 300
        while not focused.ready():
            assert time.monotonic() < deadline, 'The actual post-terminal appliance did not recover'
            time.sleep(2)
        health('health-after-terminal')
        assert contract.digest(STARTUP_WAITER) == STARTUP_WAITER_SHA256
        run('wait-actual-post-terminal-startup-passes', [STARTUP_WAITER, '--chain', args.chain,
            '--output', root / 'startup-after-terminal'], focused.START_TIMEOUT + 60)
        run('actual-current-physical-http-continuity', [TOOLS / 'focused.py', 'continuity', '--chain', args.chain])
        run('actual-current-chain', [TOOLS / 'verify-chain.py', '--duration-seconds', '86400', '--chain', args.chain])
        health('health-final')
        readiness = observe.start(86400, args.chain, readiness_only=True)
        (root / 'actual-native-readiness.json').write_text(json.dumps(readiness, indent=2))
        assert not readiness['start_findings']
        state.update(stage='Ready', tool_hashes=contract.verify_bundle(TOOLS), observed_at=focused.now())
    except BaseException as error:
        state.update(stage='Incomplete', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        (root / 'state.json').write_text(json.dumps(state, indent=2))


if __name__ == '__main__':
    main()
