#!/usr/bin/env python3
"""Preserve an observation and restart the appliance with bounded instruments."""

import datetime
import grp
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')
UNIT = 'epicsarchiverap-maven.service'
UNITS = Path('/etc/systemd/system')
INSTALL = Path('/opt/epicsarchiverap-maven')
FILES = ('measure.py', 'heap.jfc', 'collect.py', 'observe.py')
LOGGER = 'org.epics.archiverappliance.etl.common.ETLPassDriver'


def run(args, timeout=600):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError('Command failed: ' + args[0] + ': ' + str(result.returncode))
    return result.stdout.strip()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def state():
    return run(['systemctl', 'show', UNIT, '-p', 'ActiveState', '-p', 'Result',
                '-p', 'ExecMainStatus', '-p', 'InvocationID', '-p', 'TimeoutStopUSec'])


def main():
    os.umask(0o077)
    os.environ['PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
    files = json.load(sys.stdin)
    if set(files) != set(FILES):
        raise RuntimeError('Unexpected measurement bundle')
    previous = json.loads((OUT / 'observation.json').read_text())
    if previous.get('measurement_schema') == 2 or (OUT / 'shutdown.json').exists():
        raise RuntimeError('Refusing to replace a new or finished observation')
    filesystem = os.statvfs(OUT)
    if filesystem.f_bavail * filesystem.f_frsize < 10 * 1024 ** 3:
        raise RuntimeError('Restart requires at least 10 GiB free')
    before = state()
    if 'ActiveState=active' not in before:
        raise RuntimeError('The appliance must be active')
    config = (INSTALL / 'archappl.conf').read_text()
    if re.search(r'^(JAVA_TOOL_OPTIONS|LOG4J_CONFIGURATION_FILE)=', config, re.MULTILINE):
        raise RuntimeError('Runtime configuration already sets instrumentation variables')
    for name in ('measure.py', 'collect.py', 'observe.py'):
        compile(files[name], name, 'exec')
    ET.fromstring(files['heap.jfc'])
    xml = (INSTALL / 'etl/webapps/etl/WEB-INF/classes/log4j2.xml').read_text()
    if LOGGER in xml or xml.count('        <Root level=') != 1:
        raise RuntimeError('Unexpected appliance logging configuration')
    logging = xml.replace('        <Root level=',
        '        <Logger name="' + LOGGER + '" level="debug"/>\n        <Root level=')
    ET.fromstring(logging)
    dropin_dir = UNITS / (UNIT + '.d')
    dropin = dropin_dir / '40-soak-measurement.conf'
    if dropin.exists():
        raise RuntimeError('Measurement drop-in already exists')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    archive = OUT.with_name(OUT.name + '-superseded-' + stamp)
    if archive.exists():
        raise RuntimeError('Archive already exists')
    run(['systemctl', 'stop', 'etl-soak-finish.timer', 'etl-soak-sample.timer'])
    deadline = time.monotonic() + 250
    while run(['systemctl', 'show', 'etl-soak-sample.service', '--value', '-p', 'ActiveState']) == 'activating':
        if time.monotonic() > deadline:
            raise RuntimeError('Sampler did not finish before preservation')
        time.sleep(1)
    run(['/usr/bin/python3', str(TOOLS / 'collect.py'), str(OUT), str(TOOLS / 'pvs-all.csv')])
    began = time.monotonic()
    run(['systemctl', 'stop', UNIT])
    elapsed = time.monotonic() - began
    after = state()
    if 'ActiveState=inactive' not in after or 'Result=success' not in after:
        raise RuntimeError('Appliance stop was not successful')
    run(['/usr/bin/python3', str(TOOLS / 'collect.py'), str(OUT), str(TOOLS / 'pvs-all.csv'), '--journal-only'])
    cursor = json.loads((OUT / 'state.json').read_text()).get('journal_cursor')
    record = {'superseded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'reason': 'Restart with accepted GC and latency measurements',
              'previous_observation': previous, 'before': before, 'after': after,
              'stop_seconds': elapsed, 'completed_24_hours': False,
              'archive_directory': str(archive), 'existing_stores_preserved': True}
    write_json(OUT / 'superseded.json', record)
    shutil.copytree(TOOLS, OUT / 'measurement-tools-before-restart')
    OUT.rename(archive)
    archive.chmod(0o700)
    identity = pwd.getpwnam('mid-srv')
    OUT.mkdir(mode=0o710)
    os.chown(OUT, 0, grp.getgrnam('mid').gr_gid)
    OUT.chmod(0o710)
    (OUT / 'jvm').mkdir(mode=0o700)
    os.chown(OUT / 'jvm', identity.pw_uid, identity.pw_gid)
    write_json(OUT / 'restart.json', record)
    write_json(OUT / 'state.json', {'journal_cursor': cursor})
    if (archive / 'deployment-verification.json').exists():
        shutil.copy2(archive / 'deployment-verification.json', OUT / 'deployment-verification.json')
    for name, contents in files.items():
        (TOOLS / name).write_text(contents)
        (TOOLS / name).chmod(0o644)
    (TOOLS / 'log4j2-soak.xml').write_text(logging)
    (TOOLS / 'log4j2-soak.xml').chmod(0o644)
    options = ('-Xlog:gc=info,gc+heap=debug,safepoint=info:file=/var/lib/etl-soak/jvm/gc-%%p-%%t.log:'
               'utc,uptime,level,tags:filesize=16M,filecount=3 '
               '-XX:StartFlightRecording=name=etl-soak,settings=/usr/local/share/etl-soak/heap.jfc,'
               'disk=true,maxage=26h,maxsize=64m,duration=26h,dumponexit=true,'
               'filename=/var/lib/etl-soak/jvm/recording-%%p-%%t.jfr')
    dropin_dir.mkdir(exist_ok=True, mode=0o755)
    dropin.write_text('[Service]\nEnvironment="JAVA_TOOL_OPTIONS=' + options + '"\n'
                     'Environment="LOG4J_CONFIGURATION_FILE=/usr/local/share/etl-soak/log4j2-soak.xml"\n')
    dropin.chmod(0o644)
    write_json(OUT / 'measurement-config.json', {
        'files_sha256': {name: hashlib.sha256(contents.encode()).hexdigest() for name, contents in files.items()},
        'jfr_events': ['jdk.GCHeapSummary', 'jdk.GarbageCollection', 'jdk.GCPhasePause', 'jdk.DataLoss'],
        'jfr_maxsize_mib_per_jvm': 64, 'jfr_duration_hours': 26,
        'gc_log_mib_per_file': 16, 'gc_log_archives_per_jvm': 3,
        'jfr_snapshot_archive_limit_mib': 512, 'snapshot_jfr_maxage_minutes': 10,
        'snapshot_jfr_maxsize_mib': 8, 'minimum_free_space_gib': 2,
        'retrieval_workers': 2, 'freshness_interval_seconds': 300,
        'freshness_window_seconds': 30, 'representative_probe_count': 6,
        'visibility_poll_seconds': 1, 'visibility_timeout_seconds': 30,
        'timestamp_precision_seconds': 0.000001, 'forced_gc': False})
    run(['systemctl', 'daemon-reload'])
    run(['systemd-analyze', 'verify', str(UNITS / 'etl-soak-sample.service'),
         str(UNITS / 'etl-soak-finish.service')])
    run(['systemctl', 'start', UNIT])
    print(json.dumps({'archive_directory': str(archive), 'restart_requested': True,
                      'previous_stop_seconds': elapsed, 'observation_started': False}))


if __name__ == '__main__':
    main()
