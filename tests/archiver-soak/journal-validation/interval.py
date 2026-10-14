"""Execute the actual shipped collector through its native output filesystem path."""

import argparse
import datetime
import json
import os
from pathlib import Path

import boot_coverage
import basic
import prepare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--window', type=Path, required=True)
    parser.add_argument('--context', type=Path, required=True)
    parser.add_argument('--attempt', type=Path, required=True)
    args = parser.parse_args()
    previous = json.loads(args.input.read_text())
    window = json.loads(args.window.read_text())['entry']
    context = json.loads(args.context.read_text())
    config = json.loads((args.context.parent / 'package/config.json').read_text())
    observation = {'started': basic.clock(), 'pid': os.getpid(),
                   'mount_namespace': os.readlink('/proc/self/ns/mnt'),
                   'host_mount_namespace': os.readlink('/proc/1/ns/mnt'),
                   'output': str(args.output), 'mountinfo': Path('/proc/self/mountinfo').read_text(),
                   'appliance': basic.service(config['appliance_unit'], args.attempt / 'appliance'),
                   'ioc': basic.service('journal-validation-ioc.service', args.attempt / 'ioc')}
    prepare.save(args.attempt / 'cli-entered.json', observation)
    started = basic.clock()
    args.output.mkdir(mode=0o700)
    prepare.save(args.output / 'input-state.json', previous)
    result = boot_coverage.collect(args.output, previous, datetime.datetime.now(datetime.timezone.utc), window, context)
    prepare.save(args.output / 'result.json', {'started': started, 'finished': basic.clock(), **result})
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
