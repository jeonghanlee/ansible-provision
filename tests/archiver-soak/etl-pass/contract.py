#!/usr/bin/env python3
"""Versioned observation, deployed-store and immutable tool-bundle contracts."""

import datetime
import argparse
import hashlib
import json
import re
from pathlib import Path
import urllib.parse
import subprocess

SCHEMA = 5
DURATIONS = (7200, 86400)
FIXTURE_SHA = '037a92691bc23a6dcac37ec3613ad19c9f80b93b689209ec8dc403b519eaf594'
CHAINS = {
    'shortened': ('PARTITION_5MIN', 'PARTITION_HOUR', 'PARTITION_DAY'),
    'default': ('PARTITION_HOUR', 'PARTITION_DAY', 'PARTITION_YEAR'),
}
PARTITION_SECONDS = {'PARTITION_5MIN': 300, 'PARTITION_HOUR': 3600,
                     'PARTITION_DAY': 86400, 'PARTITION_YEAR': 31536000}
MAX_CADENCE = 28800
# A failed in-window journal budget is a finding about the journal settings, not about the observed ETL.
JOURNAL_BUDGET_CHECK = 'journal_retention_budget'
OFFSETS = (300, 600)
GROWTH_FIELDS = ('data', 'application_logs', 'journal', 'jfr', 'measurement')
CAPTURE_RESERVE = 512 * 1024 ** 2
SAMPLE_GAP_SECONDS = 320
BUNDLE_FILES = ('contract.py', 'aggregate.py', 'evidence.py', 'observe.py', 'collect.py',
                'measure.py', 'health-event.py', 'prepare-retest.py', 'verify-health.py',
                'verify-runtime.py', 'verify-chain.py', 'launch-retest.py',
                'apply-fixture.py', 'evaluate.py', 'heap.jfc', 'resource_helpers.py',
                'rate-semantics.json', 'journal_coverage.py', 'journal_retention.py', 'initialize-fresh.py',
                'focused.py', 'PBFixture.java', 'common.yml', 'install-fixture.py')


def deployment_pins(directory, expected):
    configuration = (Path(directory) / 'common.yml').read_text()
    fields = {'env': 'archiver_env_ref', 'maven': 'archiver_maven_src_tag'}
    variables = {}
    document_started = False
    for line in configuration.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line == '---' and not document_started:
            document_started = True
            continue
        document_started = True
        match = re.fullmatch(r'([a-z][a-z0-9_]*):[ \t]+"([^"\\\r\n]*)"[ \t]*', line)
        if not match:
            raise RuntimeError('Deployment variables require plain double-quoted scalar entries')
        field, value = match.groups()
        if field in variables:
            raise RuntimeError('Exactly one full deployment commit is required; duplicate key: ' + field)
        variables[field] = value
    actual = {}
    for name, field in fields.items():
        value = variables.get(field, '')
        if not re.fullmatch(r'[0-9a-f]{40}', value):
            raise RuntimeError('Exactly one full deployment commit is required: ' + field)
        actual[name] = value
    if actual != expected:
        raise RuntimeError('Deployment variables differ from approved source pins')
    return actual


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bundle_hashes(directory):
    return {name: digest(directory / name) for name in BUNDLE_FILES}


def verify_bundle(directory):
    frozen = json.loads((directory / 'bundle.json').read_text())
    hashes = bundle_hashes(directory)
    if frozen.get('schema') != SCHEMA or frozen.get('files') != hashes:
        raise RuntimeError('Installed bundle differs from the frozen complete bundle')
    return hashes


def validate_duration(duration):
    if type(duration) is not int or duration not in DURATIONS:
        raise RuntimeError('Duration must be 7200 or 86400 seconds')
    return duration


def chain_configuration(chain):
    if chain not in CHAINS:
        raise RuntimeError('Chain must be shortened or default')
    return {'chain': chain, 'granularities': list(CHAINS[chain]), 'source_holds': [2, 2],
            'cadences': [min(PARTITION_SECONDS[value], MAX_CADENCE)
                         for value in CHAINS[chain][:2]], 'offsets': list(OFFSETS)}


def deployed_configuration(chain, urls):
    expected = chain_configuration(chain)
    if not isinstance(urls, list) or len(urls) != 3:
        raise RuntimeError('Exactly three deployed data stores are required')
    parsed = [urllib.parse.parse_qs(urllib.parse.urlsplit(url).query,
                                   keep_blank_values=True) for url in urls]
    for index, row in enumerate(parsed):
        if row.get('partitionGranularity') != [expected['granularities'][index]]:
            raise RuntimeError('Deployed partition granularity does not match selected chain')
        if index < 2 and row.get('hold') != ['2']:
            raise RuntimeError('Deployed source hold must be two partitions')
        if index < 2 and row.get('gather') != ['1']:
            raise RuntimeError('Deployed source gather must be one partition')
    return expected


def expected_firings(start, end, configuration):
    if start.tzinfo is None or end.tzinfo is None or end <= start:
        raise RuntimeError('A forward timezone-aware observation interval is required')
    rows = []
    for transition, (cadence, offset) in enumerate(zip(configuration['cadences'], configuration['offsets'])):
        planned = ((int(start.timestamp()) - offset) // cadence) * cadence + offset
        while planned < end.timestamp():
            if planned >= start.timestamp():
                rows.append({'transition': transition, 'cadence': cadence,
                             'planned_at': datetime.datetime.fromtimestamp(
                                 planned, datetime.timezone.utc).isoformat()})
            planned += cadence
    return rows


def preparation(out, duration, chain):
    validate_duration(duration)
    record = json.loads((out / 'preparation.json').read_text())
    if record.get('duration_seconds') != duration or record.get('configuration') != chain_configuration(chain):
        raise RuntimeError('Duration or chain differs from the prepared observation')
    if record.get('schema') != SCHEMA:
        raise RuntimeError('Prepared observation requires the current schema')
    return record


def capacity_projection(source, duration, configuration):
    value = json.loads(source.read_text())
    if (value.get('schema') != 1 or value.get('duration_seconds') != duration or
            value.get('configuration') != configuration):
        raise RuntimeError('Capacity evidence belongs to another duration or chain')
    windows = value.get('windows', [])
    if {row.get('role') for row in windows} != {'historical', 'current'}:
        raise RuntimeError('Historical and current measured growth are required')
    rates = {field: [] for field in GROWTH_FIELDS}
    historical_ends, current_starts = [], []
    for window in windows:
        path = source.parent / window['source_path']
        if digest(path) != window['source_sha256']:
            raise RuntimeError('Capacity measurement source changed')
        measured = json.loads(path.read_text())
        start, end = measured['start'], measured['end']
        if not start.get('boot_id') or start['boot_id'] != end.get('boot_id'):
            raise RuntimeError('Growth measurement boot identity is missing or changed')
        elapsed = (datetime.datetime.fromisoformat(end['observed_at']) -
                   datetime.datetime.fromisoformat(start['observed_at'])).total_seconds()
        if elapsed <= 0 or set(start['bytes']) != set(GROWTH_FIELDS) or set(end['bytes']) != set(GROWTH_FIELDS):
            raise RuntimeError('Capacity measurement interval or categories are incomplete')
        if window['role'] == 'current':
            current_starts.append(datetime.datetime.fromisoformat(start['observed_at']))
            if end['boot_id'] != Path('/proc/sys/kernel/random/boot_id').read_text().strip():
                raise RuntimeError('Current growth belongs to another boot')
            age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(end['observed_at'])).total_seconds()
            if not 0 <= age <= 600:
                raise RuntimeError('Current capacity growth measurement is stale')
        else:
            historical_ends.append(datetime.datetime.fromisoformat(end['observed_at']))
        for field in GROWTH_FIELDS:
            if any(type(sample['bytes'][field]) is not int or sample['bytes'][field] < 0 for sample in (start, end)):
                raise RuntimeError('Capacity measurements must be nonnegative integer bytes')
            growth = end['bytes'][field] - start['bytes'][field]
            if growth < 0:
                raise RuntimeError('Capacity growth was interrupted by a reset or rotation')
            rates[field].append(growth / elapsed)
    if max(historical_ends) > min(current_starts):
        raise RuntimeError('Historical and current growth windows must be separate')
    import math
    return CAPTURE_RESERVE + sum(math.ceil(max(values) * duration) for values in rates.values())


def freeze(directory):
    value = {'schema': SCHEMA, 'files': bundle_hashes(directory)}
    (directory / 'bundle.json').write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    return value


def capacity_snapshot(observation, store, appliance):
    def size(path):
        result = subprocess.run(['du', '-sb', str(path)], capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise RuntimeError('Capacity byte measurement failed')
        return int(result.stdout.split()[0])
    if not observation.is_dir() or not store.is_dir() or not appliance.is_dir():
        raise RuntimeError('Actual store, appliance and observation directories are required')
    sizes = dict.fromkeys(GROWTH_FIELDS, 0)
    sizes['data'] = size(store)
    for component in ('mgmt', 'engine', 'etl', 'retrieval'):
        logs = appliance / component / 'logs'
        if logs.is_dir():
            sizes['application_logs'] += size(logs)
    for root in (Path('/var/log/journal'), Path('/run/log/journal')):
        if root.is_dir():
            sizes['journal'] += size(root)
    for path in observation.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix == '.jfr':
            category = 'jfr'
        elif 'journal' in path.name:
            category = 'journal'
        elif path.name.startswith('gc-') and '.log' in path.name:
            category = 'application_logs'
        else:
            category = 'measurement'
        sizes[category] += path.stat().st_size
    return {'schema': 1, 'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
            'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'bytes': sizes,
            'meaning': 'retained physical bytes; resets or rotations require a new supported measurement window'}


def capacity_window(start, end):
    first, last = json.loads(start.read_text()), json.loads(end.read_text())
    if not first.get('boot_id') or first.get('boot_id') != last.get('boot_id'):
        raise RuntimeError('Capacity snapshots must belong to the same boot')
    return {'schema': 1, 'start': first, 'end': last,
            'snapshots_sha256': {'start': digest(start), 'end': digest(end)}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('--freeze', type=Path)
    operation.add_argument('--capacity-snapshot', type=Path)
    operation.add_argument('--capacity-window', nargs=2, type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--observation', type=Path, default=Path('/var/lib/etl-soak'))
    parser.add_argument('--store', type=Path, default=Path('/arch'))
    parser.add_argument('--appliance', type=Path, default=Path('/opt/epicsarchiverap-maven'))
    args = parser.parse_args()
    if args.freeze:
        freeze(args.freeze)
    elif args.capacity_snapshot:
        args.capacity_snapshot.write_text(json.dumps(capacity_snapshot(args.observation, args.store, args.appliance),
                                                    indent=2, sort_keys=True) + '\n')
    else:
        if not args.output:
            parser.error('--output is required with --capacity-window')
        args.output.write_text(json.dumps(capacity_window(*args.capacity_window), indent=2, sort_keys=True) + '\n')
