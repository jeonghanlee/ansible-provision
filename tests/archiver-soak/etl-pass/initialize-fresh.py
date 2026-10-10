#!/usr/bin/env python3
"""Initialize fresh instrumentation and prepare observations from measured evidence."""

import argparse
import csv
import datetime
import grp
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import time
import xml.etree.ElementTree as ET

import collect
import contract
import journal_retention
import measure
import observe

ENV_SOURCE = Path('/opt/epicsarchiverap-env-src/epicsarchiverap-env')
SOURCE_PINS = {'env_head': '482cf2939ea997064e4a2df64e3cb420681f4566',
               'maven_head': '162269e7db97f527626ba0b387933a8c47e8bb57'}
INSTALL = Path('/opt/epicsarchiverap-maven')
STAMP = Path('/var/tmp/archiver-build.config')
LOGGER = 'org.epics.archiverappliance.etl.common.ETLPassDriver'
INITIALIZATION = 'fresh-initialization.json'
JFR_HOURS = 26
GC_FILE_MIB = 16
GC_ARCHIVES = 3
START_TIMEOUT = 180
USE_LIMIT = 85
TIMEOUTS = dict(zip(journal_retention.TIMEOUT_UNITS, (240, 2700, 2700)))


def fresh():
    if any((observe.OUT / name).exists() for name in
           ('observation.json', 'shutdown.json', 'abort.json', 'shutdown-started.json',
            'abort-started.json', 'abort-request.json', 'retest-preservation.json')):
        raise RuntimeError('Fresh initialization requires no prior observation or terminal operation')


def deployment():
    contract.deployment_pins(observe.TOOLS, {name.removesuffix('_head'): value
                                          for name, value in SOURCE_PINS.items()})
    hashes = observe.tool_hashes()
    pins = {name: observe.checked(['git', '-C', str(path), 'rev-parse', 'HEAD'])
            for name, path in (('env_head', ENV_SOURCE),
                               ('maven_head', ENV_SOURCE / 'epicsarchiverap-maven-src'))}
    if pins != SOURCE_PINS:
        raise RuntimeError('Fresh deployment source pins differ from the approved commits')
    if contract.digest(observe.TOOLS / 'pvs-all.csv') != contract.FIXTURE_SHA:
        raise RuntimeError('Fresh deployment fixture differs from the approved population')
    observe.checked(['systemctl', 'is-active', collect.UNIT, collect.IOC_UNIT, 'mariadb.service'])
    if observe.checked(['timedatectl', 'show', '-p', 'NTPSynchronized']) != 'NTPSynchronized=yes':
        raise RuntimeError('Fresh initialization requires synchronized time')
    for unit in (observe.SAMPLER + '.timer', observe.FINISH + '.timer'):
        state = observe.checked(['systemctl', 'show', unit, '--value', '-p', 'ActiveState'])
        if state in ('active', 'activating', 'deactivating'):
            raise RuntimeError('Observation timers must be inactive during fresh initialization')
    return {'source_pins': pins, 'tool_hashes': hashes, 'stamp': STAMP.read_text(),
            'configuration_sha256': contract.digest(INSTALL / 'archappl.conf'),
            'boot_id': observe.BOOT.read_text().strip()}


def unit_properties():
    properties = {}
    for unit, timeout in TIMEOUTS.items():
        values = collect.properties(observe.checked(['systemctl', 'show', unit,
            '-p', 'LoadState', '-p', 'TimeoutStartUSec', '-p', 'ExecStart']))
        if (values.get('LoadState') != 'loaded' or
                journal_retention.seconds(values.get('TimeoutStartUSec', '')) != timeout):
            raise RuntimeError('A real loaded measurement unit with the approved timeout is required: ' + unit)
        properties[unit] = values
    return properties


def load(raw):
    adjustment = collect.fixture_parameters(observe.OUT, observe.TOOLS)
    with (observe.TOOLS / 'pvs-all.csv').open(newline='') as stream:
        names = {row['pv'] for row in csv.DictReader(stream)}
    rows, _ = collect.request('getPVStatus?pv=AASOAK*', raw / 'pv-status.json')
    if (not isinstance(rows, list) or len(rows) != 903 or len(names) != 903 or
            {row.get('pvName') for row in rows} != names or
            any(row.get('status') != 'Being archived' or row.get('connectionState') != 'true'
                for row in rows)):
        raise RuntimeError('Fresh initialization requires all 903 approved PVs connected and archiving')
    return adjustment


def java_options():
    return ('-Xlog:gc=info,gc+heap=debug,safepoint=info:file=' + str(observe.OUT) +
            '/jvm/gc-%%p-%%t.log:utc,uptime,level,tags:filesize=' + str(GC_FILE_MIB) +
            'M,filecount=' + str(GC_ARCHIVES) + ' ' +
            '-XX:StartFlightRecording=name=etl-soak,settings=' + str(observe.TOOLS / 'heap.jfc') +
            ',disk=true,maxage=' + str(JFR_HOURS) + 'h,maxsize=' +
            str(measure.RECORDING_LIMIT_BYTES // 1024 ** 2) + 'm,duration=' +
            str(JFR_HOURS) + 'h,dumponexit=true,filename=' + str(observe.OUT) +
            '/jvm/recording-%%p-%%t.jfr')


def running_instruments(raw):
    pids = collect.resources.jvm_pids()
    if set(pids) != set(collect.INSTANCES):
        raise RuntimeError('Fresh instrumentation requires four actual JVMs')
    result = {}
    for component, pid in pids.items():
        arguments = Path('/proc/' + pid + '/cmdline').read_bytes().split(b'\0')
        if b'-Xms256M' not in arguments or b'-Xmx256M' not in arguments:
            raise RuntimeError('Fresh JVM heap differs from the approved 256M configuration')
        response = measure.command([str(measure.JAVA_BIN / 'jcmd'), pid, 'JFR.check', 'name=etl-soak'])
        (raw / (component + '-jfr-check.txt')).write_text(response)
        if 'name=etl-soak' not in response or '(running)' not in response:
            raise RuntimeError('The approved JFR recording is not running: ' + component)
        logs = list((observe.OUT / 'jvm').glob('gc-' + pid + '-*.log*'))
        if not logs or not any(path.stat().st_size for path in logs):
            raise RuntimeError('Actual GC logs are missing: ' + component)
        result[component] = {'pid': pid, 'gc_files': len(logs),
                             'gc_bytes': sum(path.stat().st_size for path in logs),
                             'jfr_check_sha256': contract.digest(raw / (component + '-jfr-check.txt'))}
    return result


def instruments():
    fresh()
    if any((observe.OUT / name).exists() for name in
           (INITIALIZATION, 'measurement-config.json', 'preparation.json', 'state.json')):
        raise RuntimeError('Fresh instruments are already recorded; refusing replacement')
    deployed = deployment()
    base = observe.UNITS / (observe.FINISH + '.service')
    sample = observe.UNITS / (observe.SAMPLER + '.service')
    finish_text = base.read_text()
    expected = 'ExecStart=/usr/bin/python3 ' + str(observe.TOOLS / 'observe.py') + ' finish'
    if expected not in finish_text.splitlines() or 'TimeoutStartSec=15min' not in finish_text.splitlines():
        raise RuntimeError('Unexpected existing fresh finish unit')
    if ('ExecStart=/usr/bin/python3 ' + str(observe.TOOLS / 'collect.py') + ' ' +
            str(observe.OUT) + ' ' + str(observe.TOOLS / 'pvs-all.csv')) not in sample.read_text().splitlines():
        raise RuntimeError('Unexpected existing fresh sample unit')
    dropin = observe.UNITS / (collect.UNIT + '.d') / '40-soak-measurement.conf'
    health = observe.UNITS / (collect.HEALTH_UNIT + '.d') / '50-soak-outcome.conf'
    abort = observe.UNITS / collect.ABORT_UNIT
    logging_path = observe.TOOLS / 'log4j2-soak.xml'
    if any(path.exists() for path in (dropin, health, abort, logging_path, observe.OUT / 'jvm')):
        raise RuntimeError('Fresh instrumentation destinations already exist; refusing replacement')
    configuration = (INSTALL / 'archappl.conf').read_text()
    if re.search(r'^(JAVA_TOOL_OPTIONS|LOG4J_CONFIGURATION_FILE)=', configuration, re.MULTILINE):
        raise RuntimeError('The appliance already defines instrumentation variables')
    xml = (INSTALL / 'etl/webapps/etl/WEB-INF/classes/log4j2.xml').read_text()
    if LOGGER in xml or xml.count('        <Root level=') != 1:
        raise RuntimeError('Unexpected appliance logging configuration')
    logging = xml.replace('        <Root level=',
        '        <Logger name="' + LOGGER + '" level="debug"/>\n        <Root level=')
    ET.fromstring(logging)
    ET.parse(observe.TOOLS / 'heap.jfc')
    filesystem = os.statvfs(observe.OUT)
    if filesystem.f_bavail * filesystem.f_frsize < measure.MINIMUM_FREE_BYTES + contract.CAPTURE_RESERVE:
        raise RuntimeError('Insufficient free space for fresh instruments and capture allowance')
    raw = observe.OUT / 'fresh-initialization-originals'
    raw.mkdir(mode=0o700)
    adjusted = load(raw)
    for path in (base, sample, INSTALL / 'archappl.conf'):
        shutil.copy2(path, raw / path.name)
    account = pwd.getpwnam('mid-srv')
    os.chown(observe.OUT, 0, grp.getgrnam('mid').gr_gid)
    observe.OUT.chmod(0o710)
    (observe.OUT / 'jvm').mkdir(mode=0o700)
    os.chown(observe.OUT / 'jvm', account.pw_uid, account.pw_gid)
    logging_path.write_text(logging)
    logging_path.chmod(0o644)
    dropin.parent.mkdir(mode=0o755, exist_ok=True)
    dropin.write_text('[Service]\nEnvironment="JAVA_TOOL_OPTIONS=' + java_options() + '"\n'
                     'Environment="LOG4J_CONFIGURATION_FILE=' + str(logging_path) + '"\n')
    dropin.chmod(0o644)
    health.parent.mkdir(mode=0o755, exist_ok=True)
    health.write_text('[Service]\nExecStopPost=/usr/bin/python3 ' + str(observe.TOOLS / 'health-event.py') + '\n')
    health.chmod(0o644)
    abort.write_text('[Unit]\nDescription=Preserve and abort the ETL soak\n[Service]\n'
                     'Type=oneshot\nTimeoutStartSec=45min\nUMask=0077\n'
                     'ExecStart=/usr/bin/python3 ' + str(observe.TOOLS / 'observe.py') + ' abort\n')
    abort.chmod(0o644)
    base.write_text(finish_text.replace('TimeoutStartSec=15min', 'TimeoutStartSec=45min'))
    observe.checked(['systemctl', 'daemon-reload'])
    observe.checked(['systemd-analyze', 'verify', str(base), str(sample), str(abort)])
    units = unit_properties()
    before = observe.unit_state()
    restart = observe.command(['systemctl', 'restart', collect.UNIT])
    collect.write_json(raw / 'restart-command.json', restart)
    if restart['rc']:
        raise RuntimeError('Fresh instrument restart failed; partial evidence retained')
    deadline = time.monotonic() + START_TIMEOUT
    while True:
        try:
            running = running_instruments(raw)
            break
        except (RuntimeError, FileNotFoundError, ProcessLookupError):
            if time.monotonic() >= deadline:
                raise
            time.sleep(2)
    after = observe.unit_state()
    if collect.properties(after).get('ActiveState') != 'active':
        raise RuntimeError('The instrumented appliance is not active')
    files = {str(path): contract.digest(path) for path in
             (base, sample, abort, dropin, health, logging_path, observe.TOOLS / 'heap.jfc')}
    config = {'files_sha256': deployed['tool_hashes'],
              'jfr_events': measure.EVENTS.split(','),
              'jfr_maxsize_mib_per_jvm': measure.RECORDING_LIMIT_BYTES // 1024 ** 2,
              'jfr_duration_hours': JFR_HOURS, 'gc_log_mib_per_file': GC_FILE_MIB,
              'gc_log_archives_per_jvm': GC_ARCHIVES,
              'jfr_snapshot_archive_limit_mib': measure.JFR_ARCHIVE_LIMIT_BYTES // 1024 ** 2,
              'snapshot_jfr_maxage_minutes': 10, 'snapshot_jfr_maxsize_mib': 8,
              'minimum_free_space_gib': measure.MINIMUM_FREE_BYTES // 1024 ** 3,
              'retrieval_workers': measure.RETRIEVAL_WORKERS,
              'freshness_interval_seconds': 300, 'freshness_window_seconds': measure.FRESHNESS_WINDOW_SECONDS,
              'representative_probe_count': len(measure.REPRESENTATIVES),
              'visibility_poll_seconds': measure.POLL_SECONDS,
              'visibility_timeout_seconds': measure.PROBE_TIMEOUT_SECONDS,
              'timestamp_precision_seconds': 0.000001, 'forced_gc': False}
    collect.write_json(observe.OUT / 'measurement-config.json', config)
    collect.write_json(observe.OUT / 'deployment-verification.json', deployed)
    record = {'schema': contract.SCHEMA, 'initialized_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'deployment': deployed, 'instrument_files_sha256': files,
              'measurement_config_sha256': contract.digest(observe.OUT / 'measurement-config.json'),
              'fixture_adjustment': adjusted, 'unit_before_restart': before,
              'unit_after_restart': after, 'units': units, 'jvms': running,
              'observation_started': False}
    collect.write_json(observe.OUT / INITIALIZATION, record)
    return record


def check(raw):
    fresh()
    deployed = deployment()
    initialized = json.loads((observe.OUT / INITIALIZATION).read_text())
    if (initialized.get('schema') != contract.SCHEMA or
            initialized['deployment']['boot_id'] != deployed['boot_id'] or
            initialized['deployment']['source_pins'] != deployed['source_pins'] or
            initialized['deployment']['stamp'] != deployed['stamp'] or
            initialized['deployment']['configuration_sha256'] != deployed['configuration_sha256']):
        raise RuntimeError('Fresh initialization belongs to another boot or deployment')
    if any(contract.digest(Path(path)) != digest for path, digest in initialized['instrument_files_sha256'].items()):
        raise RuntimeError('Fresh instrument configuration changed')
    if contract.digest(observe.OUT / 'measurement-config.json') != initialized['measurement_config_sha256']:
        raise RuntimeError('Fresh measurement configuration changed')
    return {'deployment': deployed, 'units': unit_properties(),
            'fixture_adjustment': load(raw), 'jvms': running_instruments(raw)}


def prepare(capacity_evidence, retention_evidence, duration, chain):
    fresh()
    contract.validate_duration(duration)
    configuration = contract.chain_configuration(chain)
    if (observe.OUT / 'preparation.json').exists() or (observe.OUT / 'state.json').exists():
        raise RuntimeError('Fresh preparation already exists; refusing replacement')
    if retention_evidence is None or capacity_evidence is None:
        raise RuntimeError('Actual retention and capacity measurement evidence is required')
    proof = journal_retention.validate(retention_evidence, observe.TOOLS)
    payload = journal_retention.preservation_payload(retention_evidence)
    required = contract.capacity_projection(capacity_evidence, duration, configuration)
    filesystem = os.statvfs(collect.STORE)
    total = filesystem.f_blocks * filesystem.f_frsize
    free = filesystem.f_bavail * filesystem.f_frsize
    if free - required < measure.MINIMUM_FREE_BYTES or 100 * (total - free + required) / total >= USE_LIMIT:
        raise RuntimeError('Fresh capacity projection violates the free-space or usage limit')
    raw = observe.OUT / ('fresh-preparation-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    raw.mkdir(mode=0o700)
    verified = check(raw)
    expected_source = contract.digest(capacity_evidence)
    capacity = json.loads(capacity_evidence.read_text())
    sources = [(capacity_evidence.parent / row['source_path']).read_bytes() for row in capacity['windows']]
    if (contract.digest(capacity_evidence) != expected_source or
            any(hashlib.sha256(data).hexdigest() != row['source_sha256']
                for row, data in zip(capacity['windows'], sources)) or
            contract.capacity_projection(capacity_evidence, duration, configuration) != required):
        raise RuntimeError('Capacity measurement inputs changed during fresh preparation')
    current = datetime.datetime.now(datetime.timezone.utc)
    journal_retention.install_payload(payload, observe.OUT / 'journal-retention-proof.json')
    directory = observe.OUT / 'capacity-sources'
    directory.mkdir(mode=0o700)
    for index, (row, data) in enumerate(zip(capacity['windows'], sources)):
        name = str(index) + '.json'
        (directory / name).write_bytes(data)
        row['source_path'] = directory.name + '/' + name
    collect.write_json(observe.OUT / 'capacity-input.json', capacity)
    collect.write_json(observe.OUT / 'capacity.json', {
        'observed_at': current.isoformat(), 'duration_seconds': duration, 'configuration': configuration,
        'projected_growth_bytes': required, 'measured_required_growth_bytes': required,
        'available_bytes': free, 'input_sha256': contract.digest(observe.OUT / 'capacity-input.json')})
    collect.write_json(observe.OUT / 'state.json', {
        key: current.strftime('%Y-%m-%d %H:%M:%S.%f UTC')
        for key in ('kernel_journal_since', 'health_journal_since', 'journal_since')})
    record = {'schema': contract.SCHEMA, 'duration_seconds': duration, 'configuration': configuration,
              'prepared_at': current.isoformat(), 'origin': 'fresh-initialization',
              'initialization_sha256': contract.digest(observe.OUT / INITIALIZATION),
              'existing_store_data_preserved': True, 'source_pins': verified['deployment']['source_pins'],
              'configuration_sha256': verified['deployment']['configuration_sha256'],
              'tool_hashes': observe.tool_hashes(), 'retention_checked_at': proof['checked_at']}
    collect.write_json(observe.OUT / 'preparation.json', record)
    return record


def measurements(directory, duration, chain):
    fresh()
    contract.validate_duration(duration)
    configuration = contract.chain_configuration(chain)
    directory.mkdir(mode=0o700)
    baseline = check(directory)
    hashes = baseline['deployment']['tool_hashes']
    capacity = directory / 'capacity'
    retention = directory / 'retention'
    capacity.mkdir(mode=0o700)
    retention.mkdir(mode=0o700)
    previous = None
    points = []
    for index in range(journal_retention.MINIMUM_INTERVALS + 1):
        if previous is not None:
            target = previous['monotonic'] + journal_retention.INTERVAL_SECONDS
            while time.monotonic() < target:
                time.sleep(min(5, target - time.monotonic()))
            if time.monotonic() - previous['monotonic'] > contract.SAMPLE_GAP_SECONDS:
                raise RuntimeError('Journal measurement interval exceeded its declared maximum')
        fresh()
        if observe.tool_hashes() != hashes:
            raise RuntimeError('Tool bundle changed during fresh measurements')
        unit_properties()
        snapshot = journal_retention.snapshot(require_load=True)
        journal_retention.save(retention / ('snapshot-' + str(index).zfill(3) + '.json'), snapshot)
        if index in (0, journal_retention.MINIMUM_INTERVALS // 2, journal_retention.MINIMUM_INTERVALS):
            path = capacity / ('point-' + str(index).zfill(3) + '.json')
            collect.write_json(path, contract.capacity_snapshot(observe.OUT, collect.STORE, INSTALL))
            points.append(path)
        raw = observe.OUT / 'raw' / ('measurement-' + str(index).zfill(3) + '-' +
              datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
        raw.mkdir(parents=True, mode=0o700)
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        gc = measure.gc(observe.OUT, raw, ts)
        latency = measure.latency(observe.OUT, raw, observe.TOOLS / 'pvs-all.csv', ts)
        collect.write_json(directory / ('progress-' + str(index).zfill(3) + '.json'), {
            'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'snapshot_sha256': contract.digest(retention / ('snapshot-' + str(index).zfill(3) + '.json')),
            'gc': gc, 'latency': latency, 'raw_directory': str(raw), 'snapshot_index': index})
        previous = snapshot
    windows = []
    for index, role in enumerate(('historical', 'current')):
        path = capacity / (role + '.json')
        collect.write_json(path, contract.capacity_window(points[index], points[index + 1]))
        windows.append({'role': role, 'source_path': path.name, 'source_sha256': contract.digest(path)})
    collect.write_json(capacity / 'input.json', {
        'schema': 1, 'duration_seconds': duration, 'configuration': configuration, 'windows': windows})
    required = contract.capacity_projection(capacity / 'input.json', duration, configuration)
    proof = journal_retention.prepare(retention, retention / 'proof.json', observe.TOOLS)
    record = {'schema': contract.SCHEMA, 'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'duration_seconds': duration, 'configuration': configuration, 'tool_hashes': hashes,
              'capacity_evidence': str(capacity / 'input.json'), 'required_growth_bytes': required,
              'retention_evidence': str(retention / 'proof.json'), 'budget': proof['budget'],
              'observation_started': False}
    collect.write_json(directory / 'measurements.json', record)
    return record


def main():
    os.umask(0o077)
    os.environ['PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('instruments', 'check', 'measure', 'prepare'))
    parser.add_argument('--measurements', type=Path)
    parser.add_argument('--capacity-evidence', type=Path)
    parser.add_argument('--journal-retention-evidence', type=Path)
    parser.add_argument('--duration-seconds', type=int, choices=contract.DURATIONS)
    parser.add_argument('--chain', choices=contract.CHAINS)
    args = parser.parse_args()
    if args.action == 'prepare' and any(value is None for value in
            (args.capacity_evidence, args.journal_retention_evidence, args.duration_seconds, args.chain)):
        parser.error('prepare requires both measurement inputs, duration and chain')
    if args.action == 'measure' and any(value is None for value in
            (args.measurements, args.duration_seconds, args.chain)):
        parser.error('measure requires a new measurement directory, duration and chain')
    with collect.locked(observe.OUT.parent / (observe.OUT.name + '.lifecycle.lock')):
        if args.action == 'instruments':
            record = instruments()
        elif args.action == 'check':
            fresh()
            raw = observe.OUT / ('fresh-check-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
            raw.mkdir(mode=0o700)
            record = check(raw)
        elif args.action == 'measure':
            record = measurements(args.measurements, args.duration_seconds, args.chain)
        else:
            record = prepare(args.capacity_evidence, args.journal_retention_evidence,
                             args.duration_seconds, args.chain)
    print(json.dumps({'action': args.action, 'schema': contract.SCHEMA,
                      'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      'jvm_count': len(record.get('jvms', {})), 'observation_started': False}))


if __name__ == '__main__':
    main()
