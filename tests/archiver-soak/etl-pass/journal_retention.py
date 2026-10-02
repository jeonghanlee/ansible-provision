#!/usr/bin/env python3
"""Measure journal write bounds and enforce hash-bound preparation and runtime budgets."""

import argparse
import csv
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import time

import contract
import journal_coverage

INTERVAL_SECONDS = 300
MINIMUM_INTERVALS = 6
PROOF_MAX_AGE = 120
SAFETY_FACTOR = 2
SAMPLE_GAP_SECONDS = contract.SAMPLE_GAP_SECONDS
JOURNAL_ROOT = Path('/var/log/journal')
OBSERVATION = Path('/var/lib/etl-soak')
SERVICE = 'systemd-journald.service'
TIMEOUT_UNITS = ('etl-soak-sample.service', 'etl-soak-finish.service', 'etl-soak-abort.service')
BYTE_UNITS = {'': 1, 'K': 1024, 'M': 1024 ** 2, 'G': 1024 ** 3, 'T': 1024 ** 4}
TIME_UNITS = {'': 1, 'us': 0.000001, 'ms': 0.001, 's': 1, 'sec': 1,
              'min': 60, 'h': 3600, 'hour': 3600, 'd': 86400, 'day': 86400,
              'week': 604800, 'month': 2629800, 'year': 31557600}


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(arguments):
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=60)
    if result.returncode or result.stderr.strip():
        raise RuntimeError('Retention measurement failed: ' + arguments[0])
    return result.stdout


def byte_size(value):
    match = re.fullmatch(r'(\d+)([KMGT]?)', value.strip())
    if not match:
        raise RuntimeError('Unresolved journal byte limit')
    return int(match[1]) * BYTE_UNITS[match[2]]


def seconds(value, allow_zero=False):
    pieces = re.findall(r'(\d+(?:\.\d+)?)([a-z]*)', value.replace(' ', ''))
    if not pieces or ''.join(number + unit for number, unit in pieces) != value.replace(' ', ''):
        raise RuntimeError('Unresolved or unbounded timeout')
    if any(unit not in TIME_UNITS for _, unit in pieces):
        raise RuntimeError('Unsupported time unit')
    result = sum(float(number) * TIME_UNITS[unit] for number, unit in pieces)
    if not math.isfinite(result) or result < 0 or (result == 0 and not allow_zero):
        raise RuntimeError('Unbounded or invalid timeout')
    return result


def settings(text):
    values, section = {}, None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(('#', ';')):
            continue
        if line.startswith('['):
            section = line
        elif section == '[Journal]':
            if '=' not in line or line.endswith('\\'):
                raise RuntimeError('Unsupported journal configuration syntax')
            key, value = line.split('=', 1)
            values[key.strip()] = value.strip()
    return values


def fixture_source():
    root = Path(__file__).parent
    fixture = root / 'pvs-all.csv'
    if not fixture.exists():
        fixture = root.parent / 'fixtures' / 'pvs-all.csv'
    if digest(fixture) != contract.FIXTURE_SHA:
        raise RuntimeError('Journal measurement fixture differs from the approved population')
    with fixture.open(newline='') as stream:
        names = {row['pv'] for row in csv.DictReader(stream)}
    adjustment = OBSERVATION / 'fixture-adjustment.json'
    return fixture, names, digest(adjustment)


def validate_load(sample):
    source = sample['load']
    rows = json.loads(source['raw_pv_status'])
    if hashlib.sha256(source['raw_pv_status'].encode()).hexdigest() != source['response_sha256']:
        raise RuntimeError('Journal load response digest differs')
    names = {row['pvName'] for row in rows}
    if (source['fixture_sha256'] != contract.FIXTURE_SHA or len(rows) != 903 or
            len(names) != 903 or names != set(source['fixture_pvs']) or
            any(row.get('status') != 'Being archived' or row.get('connectionState') != 'true' for row in rows) or
            source['adjustment'].get('verified_records') != 10):
        raise RuntimeError('Journal measurement lacks the actual approved 903-PV load')


def snapshot(require_load=False):
    version = command(['systemctl', '--version']).splitlines()[0]
    if not version.startswith('systemd 239 '):
        raise RuntimeError('Journal accounting requires the approved systemd 239 environment')
    boot = journal_coverage.BOOT.read_text().strip().replace('-', '')
    daemon = journal_coverage.daemon_identity()
    command(['journalctl', '--sync'])
    config = command(['systemd-analyze', 'cat-config', 'systemd/journald.conf'])
    values = settings(config)
    process_fields = Path('/proc/' + daemon['pid'] + '/stat').read_text().rsplit(')', 1)[1].split()
    boot_epoch = next(int(line.split()[1]) for line in Path('/proc/stat').read_text().splitlines()
                      if line.startswith('btime '))
    process_epoch = boot_epoch + int(process_fields[19]) / os.sysconf('SC_CLK_TCK')
    config_paths = [Path(line[2:].strip()) for line in config.splitlines()
                    if line.startswith('# /') and line.rstrip().endswith('.conf')]
    if not config_paths or any(path.stat().st_mtime > process_epoch for path in config_paths):
        raise RuntimeError('Journal configuration application to the running daemon is unverified')
    if values.get('Storage') != 'persistent':
        raise RuntimeError('Persistent journal storage must be explicitly verified')
    if not JOURNAL_ROOT.is_dir():
        raise RuntimeError('Persistent journal directory is unavailable')
    inventory = {}
    for path in sorted(JOURNAL_ROOT.rglob('*')):
        if not path.is_file() or path.suffix not in ('.journal', '.journal~'):
            continue
        if path.suffix == '.journal~':
            raise RuntimeError('Unresolved journal corruption or replacement file')
        stat = path.stat()
        stream = ('system' if path.name.startswith('system') else
                  'user' if path.name.startswith('user-') else 'other')
        inventory[str(path)] = {'inode': stat.st_ino, 'device': stat.st_dev,
            'bytes': stat.st_size, 'allocated_bytes': stat.st_blocks * 512,
            'mtime_ns': stat.st_mtime_ns, 'stream': stream}
    if not inventory or not any(row['stream'] == 'system' for row in inventory.values()):
        raise RuntimeError('System journal inventory is missing')
    filesystem = os.statvfs(JOURNAL_ROOT)
    total = filesystem.f_blocks * filesystem.f_frsize
    available = filesystem.f_bavail * filesystem.f_frsize
    used = sum(row['allocated_bytes'] for row in inventory.values())
    other = sum(row['allocated_bytes'] for row in inventory.values() if row['stream'] == 'other')
    maximum = byte_size(values['SystemMaxUse']) if values.get('SystemMaxUse') else min(total // 10, 4 * 1024 ** 3)
    keep_free = byte_size(values['SystemKeepFree']) if values.get('SystemKeepFree') else min(total * 15 // 100, 4 * 1024 ** 3)
    file_size = byte_size(values['SystemMaxFileSize']) if values.get('SystemMaxFileSize') else min(maximum // 8, 128 * 1024 ** 2)
    if not maximum or not file_size:
        raise RuntimeError('Journal byte/file limits are unbounded')
    retention = seconds(values.get('MaxRetentionSec') or '0', allow_zero=True)
    maximum_files = int(values.get('SystemMaxFiles') or '100')
    file_seconds = seconds(values.get('MaxFileSec') or '1month', allow_zero=True)
    if maximum_files <= 0:
        raise RuntimeError('Journal file-count limit is unresolved')
    timeout_values = {}
    for unit in TIMEOUT_UNITS:
        unit_values = command(['systemctl', 'show', unit, '-p', 'LoadState', '-p', 'TimeoutStartUSec'])
        unit_properties = dict(line.split('=', 1) for line in unit_values.splitlines() if '=' in line)
        if unit_properties.get('LoadState') != 'loaded':
            raise RuntimeError('Retention measurement requires a loaded sample/finish/abort unit')
        timeout_values[unit] = unit_properties.get('TimeoutStartUSec', '')
    timeouts = {unit: seconds(value) for unit, value in timeout_values.items()}
    service_policy = command(['systemctl', 'show', 'epicsarchiverap-maven.service',
                              '-p', 'LogRateLimitIntervalUSec', '-p', 'LogRateLimitBurst'])
    fixture, names, adjustment_sha = fixture_source()
    io_text = Path('/proc/' + daemon['pid'] + '/io').read_text()
    io = {key: int(value.strip()) for key, value in
          (line.split(':', 1) for line in io_text.splitlines())}
    if journal_coverage.daemon_identity() != daemon or journal_coverage.BOOT.read_text().strip().replace('-', '') != boot:
        raise RuntimeError('Journal identity changed during measurement')
    result = {'schema': 1, 'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'monotonic': time.monotonic(), 'boot_id': boot, 'daemon': daemon,
        'systemd_version': version, 'configuration': config, 'service_policy': service_policy,
        'policy_sha256': hashlib.sha256((version + config + service_policy + adjustment_sha +
                                        contract.FIXTURE_SHA + json.dumps(timeout_values, sort_keys=True)).encode()).hexdigest(),
        'config_files_sha256': {str(path): digest(path) for path in config_paths},
        'accounting': 'Synchronized daemon write_bytes is a conservative upper bound for each stream; allocation growth is also bounded',
        'write_bytes': io['write_bytes'], 'cancelled_write_bytes': io['cancelled_write_bytes'],
        'inventory': inventory, 'available_bytes': available, 'filesystem_bytes': total,
        'caps': {'effective_bytes': max(0, min(maximum, used + max(0, available - keep_free)) - other),
                 'maximum_bytes': maximum, 'keep_free_bytes': keep_free,
                 'file_bytes': file_size, 'retention_seconds': retention,
                 'maximum_files': maximum_files, 'file_seconds': file_seconds},
        'timeouts': timeouts}
    if require_load:
        import collect
        raw_status = command(['curl', '--fail', '--silent', '--show-error', '--max-time', '30',
                              collect.MGMT + '/getPVStatus?pv=AASOAK*'])
        result['load'] = {'raw_pv_status': raw_status, 'response_sha256': hashlib.sha256(raw_status.encode()).hexdigest(),
                          'fixture_sha256': digest(fixture), 'fixture_pvs': sorted(names),
                          'adjustment': collect.fixture_parameters(OBSERVATION)}
        validate_load(result)
    if journal_coverage.daemon_identity() != daemon or journal_coverage.BOOT.read_text().strip().replace('-', '') != boot:
        raise RuntimeError('Journal identity changed before completing the snapshot')
    return result


def elapsed(first, last):
    if any(first[key] != last[key] for key in ('boot_id', 'daemon', 'policy_sha256')):
        raise RuntimeError('Journal boot, process or logging policy changed')
    wall = (datetime.datetime.fromisoformat(last['observed_at']) -
            datetime.datetime.fromisoformat(first['observed_at'])).total_seconds()
    duration = last['monotonic'] - first['monotonic']
    if duration <= 0 or abs(wall - duration) > 2:
        raise RuntimeError('Invalid journal measurement interval')
    return duration


def rates(first, last):
    duration = elapsed(first, last)
    writes = last['write_bytes'] - first['write_bytes']
    cancellations = last['cancelled_write_bytes'] - first['cancelled_write_bytes']
    if writes < 0 or cancellations < 0:
        raise RuntimeError('Journal write accounting reset')
    if writes == 0 and first['inventory'] != last['inventory']:
        raise RuntimeError('Changed journal files lack write accounting')
    result = {}
    for stream in ('system', 'user'):
        allocation = sum(max(0, row['allocated_bytes'] - first['inventory'].get(path, {}).get('allocated_bytes', 0))
                         for path, row in last['inventory'].items() if row['stream'] == stream)
        result[stream] = max(writes, allocation) / duration
    return result


def calculation(current, bounds):
    if set(bounds) != {'system', 'user'} or any(not math.isfinite(value) or value < 0 for value in bounds.values()):
        raise RuntimeError('Journal rates must be finite nonnegative bounds')
    limits = current['timeouts']
    if any(not math.isfinite(limits[unit]) or limits[unit] <= 0 for unit in TIMEOUT_UNITS):
        raise RuntimeError('Journal timeout bounds must be finite and positive')
    periodic = SAMPLE_GAP_SECONDS + limits[TIMEOUT_UNITS[0]]
    terminal = SAMPLE_GAP_SECONDS + max(limits[unit] for unit in TIMEOUT_UNITS[1:])
    horizon = SAFETY_FACTOR * max(periodic, terminal)
    user_bytes = sum(row['allocated_bytes'] for row in current['inventory'].values() if row['stream'] == 'user')
    files = {stream: max([current['caps']['file_bytes']] +
             [max(row['bytes'], row['allocated_bytes']) for row in current['inventory'].values()
              if row['stream'] == stream]) for stream in ('system', 'user')}
    budget = {stream: math.ceil(bounds[stream] * horizon) + 2 * files[stream]
              for stream in ('system', 'user')}
    budget['user'] += user_bytes
    required = sum(budget.values())
    cap = current['caps']['effective_bytes']
    retention = current['caps']['retention_seconds']
    time_rotations = math.ceil(horizon / current['caps']['file_seconds']) if current['caps']['file_seconds'] else 0
    retained_user_files = sum(row['stream'] == 'user' for row in current['inventory'].values())
    other_files = sum(row['stream'] == 'other' for row in current['inventory'].values())
    user_groups = {Path(name).name.split('@', 1)[0].split('.', 1)[0] for name, row in
                   current['inventory'].items() if row['stream'] == 'user'}
    file_budget = other_files + retained_user_files + 2 + time_rotations + sum(
        math.ceil(bounds[stream] * horizon / current['caps']['file_bytes']) for stream in bounds)
    file_budget += len(user_groups) * (2 + time_rotations)
    passed = (required <= cap and (not retention or horizon <= retention) and
              file_budget <= current['caps']['maximum_files'])
    return {'periodic_gap_seconds': periodic, 'terminal_gap_seconds': terminal,
        'horizon_seconds': horizon, 'safety_factor': SAFETY_FACTOR,
        'rates_bytes_per_second': bounds, 'file_bytes': files, 'user_retained_bytes': user_bytes,
        'budget_bytes': budget, 'required_bytes': required, 'effective_cap_bytes': cap,
        'retention_seconds': retention, 'required_files': file_budget,
        'maximum_files': current['caps']['maximum_files'], 'passed': passed}


def measured_bounds(samples):
    if len(samples) < MINIMUM_INTERVALS + 1:
        raise RuntimeError('Six consecutive five-minute journal intervals are required')
    bounds = {'system': 0, 'user': 0}
    for sample in samples:
        validate_load(sample)
    for first, last in zip(samples, samples[1:]):
        duration = elapsed(first, last)
        if not INTERVAL_SECONDS <= duration <= SAMPLE_GAP_SECONDS:
            raise RuntimeError('Journal measurements must use consecutive five-minute intervals')
        measured = rates(first, last)
        bounds = {stream: max(bounds[stream], measured[stream]) for stream in bounds}
    return bounds


def load_sources(proof, root):
    samples = []
    for source in proof['sources']:
        relative = Path(source['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise RuntimeError('Journal measurement paths must remain within the evidence directory')
        path = root / relative
        if root.resolve() not in path.resolve().parents:
            raise RuntimeError('Journal measurement source escapes its evidence directory')
        if digest(path) != source['sha256']:
            raise RuntimeError('Journal measurement source changed')
        samples.append(json.loads(path.read_text()))
    return samples


def historical_bounds(proof, root, first, bounds):
    for group in proof.get('historical_sources', []):
        samples = load_sources({'sources': group}, root)
        measured = measured_bounds(samples)
        if (samples[-1]['policy_sha256'] != first['policy_sha256'] or
                datetime.datetime.fromisoformat(samples[-1]['observed_at']) >
                datetime.datetime.fromisoformat(first['observed_at'])):
            raise RuntimeError('Historical journal evidence overlaps or belongs to another policy')
        bounds = {stream: max(bounds[stream], measured[stream]) for stream in bounds}
    return bounds


def prepare(directory, output, tools, histories=()):
    paths = sorted(directory.glob('snapshot-*.json'))
    samples = [json.loads(path.read_text()) for path in paths]
    bounds = measured_bounds(samples)
    history_groups = []
    for path in histories:
        history = json.loads(path.read_text())
        for group in [history['sources'], *history.get('historical_sources', [])]:
            historical = load_sources({'sources': group}, path.parent)
            measured_bounds(historical)
            history_groups.append([{'path': os.path.relpath(path.parent / row['path'], output.parent),
                                    'sha256': row['sha256']} for row in group])
    bounds = historical_bounds({'historical_sources': history_groups}, output.parent, samples[0], bounds)
    current = snapshot()
    elapsed(samples[-1], current)
    bounds = {stream: max(bounds[stream], rates(samples[-1], current)[stream]) for stream in bounds}
    budget = calculation(current, bounds)
    proof = {'schema': contract.SCHEMA, 'observed_at': current['observed_at'],
        'boot_id': current['boot_id'], 'daemon': current['daemon'],
        'policy_sha256': current['policy_sha256'], 'tool_hashes': contract.verify_bundle(tools),
        'sources': [{'path': os.path.relpath(path, output.parent), 'sha256': digest(path)} for path in paths],
        'historical_sources': history_groups, 'latest': current, 'budget': budget}
    load_sources(proof, output.parent)
    save(output, proof)
    if not budget['passed']:
        raise RuntimeError('Journal retention budget does not satisfy byte/time limits')
    return proof


def validate(proof_path, tools, current=None, fresh=True):
    proof = json.loads(proof_path.read_text())
    if proof.get('schema') != contract.SCHEMA or proof.get('tool_hashes') != contract.verify_bundle(tools):
        raise RuntimeError('Journal retention proof belongs to another bundle or schema')
    samples = load_sources(proof, proof_path.parent)
    baseline = measured_bounds(samples)
    baseline = historical_bounds(proof, proof_path.parent, samples[0], baseline)
    latest = proof['latest']
    if any(proof.get(key) != latest.get(key) for key in ('boot_id', 'daemon', 'policy_sha256')):
        raise RuntimeError('Journal retention proof identity is inconsistent')
    measured = rates(samples[-1], latest)
    baseline = {stream: max(baseline[stream], measured[stream]) for stream in baseline}
    if proof['budget'] != calculation(latest, baseline) or not proof['budget']['passed']:
        raise RuntimeError('Journal retention calculation is inconsistent or failed')
    current = current or snapshot()
    elapsed(latest, current)
    age = (datetime.datetime.now(datetime.timezone.utc) -
           datetime.datetime.fromisoformat(current['observed_at'])).total_seconds()
    if fresh and not 0 <= age <= PROOF_MAX_AGE:
        raise RuntimeError('Journal retention proof is stale')
    bounds = rates(latest, current)
    result = calculation(current, {stream: max(baseline[stream], bounds[stream]) for stream in baseline})
    if not result['passed']:
        raise RuntimeError('Current journal retention budget failed')
    return {**proof, 'checked_at': current['observed_at'], 'current': current, 'current_budget': result}


def preservation_payload(source):
    proof = json.loads(source.read_text())
    groups = [proof['sources'], *proof.get('historical_sources', [])]
    contents = []
    for group in groups:
        load_sources({'sources': group}, source.parent)
        for row in group:
            data = (source.parent / row['path']).read_bytes()
            if hashlib.sha256(data).hexdigest() != row['sha256']:
                raise RuntimeError('Journal source changed during preservation')
            contents.append(data)
    return proof, contents


def install_payload(payload, destination):
    proof, contents = payload
    directory = destination.parent / 'journal-retention-sources'
    directory.mkdir()
    rows = [row for group in [proof['sources'], *proof.get('historical_sources', [])] for row in group]
    for index, (row, data) in enumerate(zip(rows, contents)):
        name = 'snapshot-' + str(index).zfill(3) + '.json'
        (directory / name).write_bytes(data)
        row['path'] = directory.name + '/' + name
    save(destination, proof)


def install_proof(source, destination):
    install_payload(preservation_payload(source), destination)


def runtime(out, raw, tools, previous, terminal=False):
    current = snapshot()
    save(raw / 'journal-retention-snapshot.json', current)
    proof_path = out / 'journal-retention-proof.json'
    checked = validate(proof_path, tools, current=current, fresh=False)
    result = calculation(current, {stream: max(value,
        previous.get('journal_retention_bounds', {}).get(stream, 0))
        for stream, value in checked['current_budget']['rates_bytes_per_second'].items()})
    old = previous.get('journal_retention_snapshot')
    if old:
        gap = elapsed(old, current)
        observed = rates(old, current)
        bounds = {stream: max(result['rates_bytes_per_second'][stream], observed[stream]) for stream in observed}
        result = calculation(current, bounds)
        gap_limit = result['terminal_gap_seconds'] if terminal else result['periodic_gap_seconds']
        result['actual_gap_seconds'] = gap
        if gap > gap_limit:
            result['passed'] = False
    save(raw / 'journal-retention-budget.json', result)
    if not result['passed']:
        raise RuntimeError('In-window journal retention budget or collection gap failed')
    return {'snapshot': current, 'budget': result, 'proof_sha256': digest(proof_path)}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('snapshot', 'prepare', 'check'))
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--measurements', type=Path)
    parser.add_argument('--history-evidence', type=Path, action='append', default=[])
    parser.add_argument('--tools', type=Path, default=Path('/usr/local/share/etl-soak'))
    args = parser.parse_args()
    if args.action == 'snapshot':
        save(args.output, snapshot(require_load=True))
    elif args.action == 'prepare':
        if not args.measurements:
            parser.error('--measurements is required')
        prepare(args.measurements, args.output, args.tools, args.history_evidence)
    else:
        validate(args.output, args.tools)


if __name__ == '__main__':
    main()
