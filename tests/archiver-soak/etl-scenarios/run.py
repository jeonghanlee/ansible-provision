#!/usr/bin/env python3
"""Run one preserved ETL scenario payload with explicit private configuration."""

import argparse
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent


def manifest():
    entries = {}
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        if name in entries or Path(name).name != name:
            raise RuntimeError('Invalid or duplicate scenario source path')
        entries[name] = expected
    for name, expected in entries.items():
        path = ROOT / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Preserved scenario source differs from its manifest: ' + name)
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--payload', type=Path, required=True)
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    entries = manifest()
    if args.source not in entries or not args.source.endswith('.py') or args.source == Path(__file__).name:
        parser.error('Select a preserved scenario Python source')
    payload = json.loads(args.payload.read_text())
    if not isinstance(payload, dict) or payload.get('role') != 'etl':
        parser.error('The private payload must declare role=etl')
    arguments = args.arguments[1:] if args.arguments[:1] == ['--'] else args.arguments
    sys.argv = [str(ROOT / args.source), *arguments]
    runpy.run_path(sys.argv[0], init_globals={'ROLE': 'etl', 'PAYLOAD': payload}, run_name='__main__')


if __name__ == '__main__':
    main()

