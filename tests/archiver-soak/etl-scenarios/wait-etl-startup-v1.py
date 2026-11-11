#!/usr/bin/env python3
"""Wait for both actual native startup transitions before continuity inspection."""

import argparse
import json
import os
from pathlib import Path
import sys
import time

TOOLS = Path('/usr/local/share/etl-soak')
POLL_SECONDS = 5


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chain', choices=('shortened', 'default'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.output.is_absolute() and args.output.is_relative_to('/var/lib')
    assert not args.output.exists()
    os.umask(0o077)
    args.output.mkdir(parents=True, mode=0o700)
    sys.path.insert(0, str(TOOLS))
    import contract
    import focused

    identity = focused.identity()
    hashes = contract.verify_bundle(TOOLS)
    cadences = contract.chain_configuration(args.chain)['cadences']
    started = time.monotonic()
    deadline = started + focused.START_TIMEOUT
    state = {'state': 'Waiting for actual startup transitions', 'chain': args.chain,
             'started_at': focused.now(), 'native_timeout_seconds': focused.START_TIMEOUT,
             'actual_identity': identity, 'tool_hashes': hashes, 'captures': []}
    try:
        while True:
            assert focused.identity() == identity and contract.verify_bundle(TOOLS) == hashes
            directory = args.output / ('capture-' + str(len(state['captures'])).zfill(4))
            directory.mkdir(mode=0o700)
            records = focused.passes(directory, identity['invocation_id'])
            for row in records:
                focused.successful_pass(row)
                assert row['cadence'] == cadences[row['transition']]
            state['captures'].append({'observed_at': focused.now(),
                'transitions': sorted({row['transition'] for row in records}),
                'actual_pass_count': len(records),
                'pass_sha256': contract.digest(directory / ('passes-' + identity['invocation_id'] + '.jsonl'))})
            if {row['transition'] for row in records} == {0, 1}:
                state.update(state='Ready', observed_at=focused.now(), elapsed_seconds=time.monotonic() - started)
                break
            assert time.monotonic() < deadline, 'The actual native startup transitions did not complete'
            (args.output / 'state.json').write_text(json.dumps(state, indent=2))
            time.sleep(min(POLL_SECONDS, max(0, deadline - time.monotonic())))
    except BaseException as error:
        state.update(state='Incomplete', observed_at=focused.now(), error_type=type(error).__name__, error=str(error))
        raise
    finally:
        (args.output / 'state.json').write_text(json.dumps(state, indent=2))
    print(json.dumps({key: state[key] for key in ('state', 'chain', 'observed_at', 'elapsed_seconds')}, sort_keys=True))


if __name__ == '__main__':
    main()
