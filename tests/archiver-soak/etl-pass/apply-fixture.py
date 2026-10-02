#!/usr/bin/env python3
"""Preserve the IOC inputs and apply the approved ten-record retest override."""

import argparse
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import re
import shlex

import collect
import measure
import observe
import contract

ORIGINAL_DATABASES = ('aasoak.db', 'load1.db', 'load2.db')
OVERRIDE_NAME = 'retest-deadband.db'


def approved_records(source):
    if contract.digest(observe.TOOLS / 'pvs-all.csv') != contract.FIXTURE_SHA:
        raise RuntimeError('Original registration fixture changed')
    with (observe.TOOLS / 'pvs-all.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    names = sorted(row['pv'] for row in rows if row['group'] == 'deadband')
    if names != ['AASOAK:DB:CH' + str(number).zfill(2) for number in range(1, 11)]:
        raise RuntimeError('Unexpected deadband fixture population')
    expected = '\n'.join('record(calc, "' + name + '") {\n    field(MDEL, "-1")\n'
                         '    field(ADEL, "-1")\n}\n' for name in names)
    if source.read_text().strip() != expected.strip():
        raise RuntimeError('Unexpected approved override source')
    return names


def verify_existing(source):
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('Fixture verification must precede the observation')
    names = approved_records(source)
    adjustment = json.loads((observe.OUT / 'fixture-adjustment.json').read_text())
    override = observe.TOOLS / OVERRIDE_NAME
    if (adjustment.get('records') != names or adjustment.get('override_name') != OVERRIDE_NAME or
            adjustment.get('MDEL') != -1 or adjustment.get('ADEL') != -1 or
            adjustment.get('override_sha256') != hashlib.sha256(source.read_bytes()).hexdigest() or
            override.read_bytes() != source.read_bytes() or
            set(adjustment.get('original_database_sha256', {})) != set(ORIGINAL_DATABASES)):
        raise RuntimeError('Existing fixture adjustment conflicts with the approved inputs')
    for name, digest in adjustment['original_database_sha256'].items():
        if hashlib.sha256((observe.TOOLS / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Original fixture database changed')
    base = observe.UNITS / collect.IOC_UNIT
    commands = [line for line in base.read_text().splitlines() if line.startswith('ExecStart=')]
    if len(commands) != 1 or not all(' -d ' + str(observe.TOOLS / name) in commands[0]
                                   for name in ORIGINAL_DATABASES):
        raise RuntimeError('Unexpected base IOC command')
    dropin = observe.UNITS / (collect.IOC_UNIT + '.d') / '50-retest-deadband.conf'
    expected_dropin = '[Service]\nExecStart=\n' + commands[0] + ' -d ' + str(override) + '\n'
    if dropin.read_text() != expected_dropin:
        raise RuntimeError('Existing IOC drop-in conflicts with the approved command')
    effective = observe.checked(['systemctl', 'show', collect.IOC_UNIT, '--value', '-p', 'ExecStart'])
    match = re.search(r'argv\[\]=(.*?)\s+;', effective)
    if not match or shlex.split(match[1]) != shlex.split(commands[0][len('ExecStart='):] + ' -d ' + str(override)):
        raise RuntimeError('Effective IOC command differs from the preserved command')
    verified = collect.fixture_parameters(observe.OUT, observe.TOOLS)
    collect.write_json(observe.OUT / 'fixture-verification.json', {
        'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'mode': 'verify-existing', 'verified': verified,
        'adjustment_sha256': hashlib.sha256((observe.OUT / 'fixture-adjustment.json').read_bytes()).hexdigest(),
        'base_unit_sha256': hashlib.sha256(base.read_bytes()).hexdigest(),
        'dropin_sha256': hashlib.sha256(dropin.read_bytes()).hexdigest()})
    print(json.dumps(verified))


def apply(source):
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('Fixture adjustment must precede the observation')
    names = approved_records(source)
    contents = source.read_text()
    base = observe.UNITS / collect.IOC_UNIT
    commands = [line for line in base.read_text().splitlines() if line.startswith('ExecStart=')]
    if len(commands) != 1 or not all(' -d ' + str(observe.TOOLS / name) in commands[0]
                                   for name in ORIGINAL_DATABASES):
        raise RuntimeError('Unexpected base IOC command')
    dropin = observe.UNITS / (collect.IOC_UNIT + '.d') / '50-retest-deadband.conf'
    if dropin.exists() or (observe.OUT / 'fixture-adjustment.json').exists():
        raise RuntimeError('Fixture adjustment already exists; refusing replacement')
    destination = observe.TOOLS / OVERRIDE_NAME
    if destination.exists():
        raise RuntimeError('Override destination already exists')
    archive = observe.OUT / 'fixture-before-retest'
    if archive.exists():
        raise RuntimeError('Fixture preservation destination already exists')
    archive.mkdir(mode=0o700)
    shutil.copy2(base, archive / collect.IOC_UNIT)
    hashes = {}
    for name in ORIGINAL_DATABASES:
        shutil.copy2(observe.TOOLS / name, archive / name)
        hashes[name] = hashlib.sha256((observe.TOOLS / name).read_bytes()).hexdigest()
    destination.write_text(contents)
    destination.chmod(0o644)
    dropin.parent.mkdir(mode=0o755, exist_ok=True)
    dropin.write_text('[Service]\nExecStart=\n' + commands[0] + ' -d ' + str(destination) + '\n')
    dropin.chmod(0o644)
    observe.checked(['systemctl', 'daemon-reload'])
    observe.checked(['systemd-analyze', 'verify', str(base)])
    observe.checked(['systemctl', 'restart', collect.IOC_UNIT])
    environment = dict(os.environ, EPICS_CA_ADDR_LIST='127.0.0.1', EPICS_CA_AUTO_ADDR_LIST='NO')
    fields = [name + suffix for name in names for suffix in ('.MDEL', '.ADEL')]
    result = subprocess.run([measure.CAGET, '-w', '5', '-t', *fields], env=environment,
                            capture_output=True, text=True, timeout=15)
    values = result.stdout.split()
    record = {'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'override_name': OVERRIDE_NAME, 'override_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
              'original_database_sha256': hashes, 'records': names,
              'MDEL': -1, 'ADEL': -1, 'scan_and_sampling_unchanged': True,
              'field_verification_rc': result.returncode, 'field_values': values}
    collect.write_json(observe.OUT / 'fixture-adjustment.json', record)
    if result.returncode or len(values) != 20 or any(float(value) != -1 for value in values):
        raise RuntimeError('Actual IOC field verification failed; evidence retained')
    print(json.dumps({'records': len(names), 'fields_verified': len(values),
                      'override_sha256': record['override_sha256']}))


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--verify-existing', action='store_true')
    args = parser.parse_args()
    with collect.locked(observe.OUT.parent / (observe.OUT.name + '.lifecycle.lock')):
        if args.verify_existing:
            verify_existing(args.source)
        else:
            apply(args.source)


if __name__ == '__main__':
    main()
