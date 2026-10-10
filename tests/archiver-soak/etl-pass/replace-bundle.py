#!/usr/bin/env python3
"""Replace the installed ETL soak tool bundle by a frozen bundle, keeping every other file.

This step is not a member of the frozen bundle. It stages a full copy of the installed
directory, overwrites only the frozen members and bundle.json there, verifies the staged
directory and swaps it in by two renames. It deletes nothing and never starts or stops a unit.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

INSTALLED = Path('/usr/local/share/etl-soak')
# The accepted bundle.json SHA256 is filled in after the bundle freeze and before this step is reviewed.
ACCEPTED_BUNDLE_SHA256 = '5168ca0e495ea8720704bada64f3297b8c12d48ae2037acfb4762f9cb237cd15'
INACTIVE_UNITS = ('etl-soak-sample.service', 'etl-soak-sample.timer', 'etl-soak-finish.service')
BUSY_STATES = ('active', 'activating', 'deactivating', 'reloading')
SCHEMA = 5


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def stamp():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def unit_state(unit):
    result = subprocess.run(['systemctl', 'show', unit, '--value', '-p', 'ActiveState'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode != 0:
        raise RuntimeError('Cannot read the unit state: ' + unit)
    return result.stdout.strip()


def unpack(bundle, scratch):
    """Return a directory holding the frozen bundle; an archive is unpacked into scratch."""
    bundle = Path(bundle)
    if bundle.is_dir():
        return bundle
    destination = Path(scratch) / 'bundle'
    destination.mkdir()
    with tarfile.open(bundle) as archive:
        members = archive.getmembers()
        for member in members:
            parts = Path(member.name).parts
            if (member.name.startswith('/') or '..' in parts or not (member.isfile() or member.isdir())):
                raise RuntimeError('Unsafe bundle archive member: ' + member.name)
        options = {'filter': 'data'} if hasattr(tarfile, 'data_filter') else {}
        archive.extractall(destination, members=members, **options)
    return destination


def frozen_members(directory, accepted):
    """Require the directory to be exactly the accepted frozen bundle and return its member names."""
    if not accepted:
        raise RuntimeError('The accepted bundle.json SHA256 is not filled in')
    path = Path(directory) / 'bundle.json'
    if not path.is_file() or digest(path) != accepted:
        raise RuntimeError('bundle.json differs from the accepted SHA256')
    frozen = json.loads(path.read_text())
    files = frozen.get('files')
    if frozen.get('schema') != SCHEMA or not isinstance(files, dict) or not files:
        raise RuntimeError('bundle.json is not a schema ' + str(SCHEMA) + ' frozen bundle')
    for name, expected in files.items():
        member = Path(directory) / name
        if '/' in name or not member.is_file() or digest(member) != expected:
            raise RuntimeError('Bundle member differs from the frozen bundle: ' + name)
    return sorted(files)


def tree(directory):
    """Map every relative file path of a directory to its digest, mode and timestamp."""
    found = {}
    for path in sorted(Path(directory).rglob('*')):
        if path.is_symlink():
            found[str(path.relative_to(directory))] = ('link', os.readlink(path))
        elif path.is_file():
            stat = path.stat()
            found[str(path.relative_to(directory))] = (digest(path), stat.st_mode, stat.st_mtime_ns,
                                                       stat.st_uid, stat.st_gid)
    return found


def replace(installed, bundle, accepted, units=INACTIVE_UNITS, now=None):
    installed = Path(installed)
    if not installed.is_dir():
        raise RuntimeError('The installed directory is missing: ' + str(installed))
    with tempfile.TemporaryDirectory() as scratch:
        directory = unpack(bundle, scratch)
        members = frozen_members(directory, accepted)
        staged = installed.parent / (installed.name + '.new-' + accepted[:8])
        preserved = installed.parent / (installed.name + '.prev-' + (now or stamp()))
        rejected = installed.parent / (installed.name + '.rejected-' + (now or stamp()))
        for path in (staged, preserved):
            if path.exists():
                raise RuntimeError('Refusing an existing sibling: ' + str(path))
        for unit in units:
            if unit_state(unit) in BUSY_STATES:
                raise RuntimeError('A unit that must be inactive is active: ' + unit)
        before = tree(installed)
        # A failure below leaves the staged sibling in place for inspection; nothing is deleted.
        subprocess.run(['cp', '-a', '--', str(installed), str(staged)], check=True)
        for name in (*members, 'bundle.json'):
            shutil.copyfile(Path(directory) / name, staged / name)
        frozen_members(staged, accepted)
        carried = {name: value for name, value in before.items() if name not in (*members, 'bundle.json')}
        after = tree(staged)
        if {name: after.get(name) for name in carried} != carried:
            raise RuntimeError('A file that is not a bundle member changed in the staged copy')
        commands = ['mv -T -- ' + str(installed) + ' ' + str(rejected),
                    'mv -T -- ' + str(preserved) + ' ' + str(installed)]
        print('Rollback commands, run in order:', flush=True)
        for command in commands:
            print('  ' + command, flush=True)
        installed.rename(preserved)
        staged.rename(installed)
    frozen_members(installed, accepted)
    return {'installed': str(installed), 'preserved': str(preserved), 'staged_name': staged.name,
            'bundle_json_sha256': accepted, 'members': members, 'rollback': commands}


def rollback(installed, preserved, now=None):
    installed, preserved = Path(installed), Path(preserved)
    rejected = installed.parent / (installed.name + '.rejected-' + (now or stamp()))
    if not preserved.is_dir() or not installed.is_dir() or rejected.exists():
        raise RuntimeError('Rollback needs the installed and preserved directories and a free rejected name')
    if preserved.parent != installed.parent or not preserved.name.startswith(installed.name + '.prev-'):
        raise RuntimeError('The preserved directory is not a sibling of this installation')
    installed.rename(rejected)
    preserved.rename(installed)
    return {'installed': str(installed), 'rejected': str(rejected)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('replace', 'rollback'))
    parser.add_argument('--bundle', help='replace: frozen bundle directory or tar archive')
    parser.add_argument('--preserved', help='rollback: the preserved sibling directory')
    parser.add_argument('--installed', default=str(INSTALLED))
    args = parser.parse_args()
    if args.action == 'replace':
        if not args.bundle:
            parser.error('replace requires --bundle')
        result = replace(args.installed, args.bundle, ACCEPTED_BUNDLE_SHA256)
    else:
        if not args.preserved:
            parser.error('rollback requires --preserved')
        result = rollback(args.installed, args.preserved)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        print('Refused: ' + str(error), file=sys.stderr)
        sys.exit(1)
