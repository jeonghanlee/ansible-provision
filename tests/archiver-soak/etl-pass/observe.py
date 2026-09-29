#!/usr/bin/env python3
"""Start a bounded observation or preserve a measured whole-unit stop."""

import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import time

import collect
import measure

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')
UNITS = Path('/etc/systemd/system')
SAMPLER = 'etl-soak-sample'
FINISH = 'etl-soak-finish'
DURATION = 24 * 60 * 60
BOOT = Path('/proc/sys/kernel/random/boot_id')


def command(args, timeout=600):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return {'command': args, 'rc': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


def checked(args):
    result = command(args)
    if result['rc']:
        raise RuntimeError('Command failed: ' + ' '.join(args))
    return result['stdout'].strip()


def unit_state():
    return checked(['systemctl', 'show', collect.UNIT, '-p', 'ActiveState', '-p', 'SubState',
                    '-p', 'Result', '-p', 'ExecMainStatus', '-p', 'TimeoutStopUSec',
                    '-p', 'MainPID', '-p', 'InvocationID'])


def start():
    manifest = OUT / 'observation.json'
    if manifest.exists():
        raise RuntimeError('An observation is already recorded; refusing to replace it')
    latest = json.loads((OUT / 'latest.json').read_text())
    now = datetime.datetime.now(datetime.timezone.utc)
    sampled = datetime.datetime.fromisoformat(latest['observed_at'])
    if latest['errors'] or (now - sampled).total_seconds() > 120:
        raise RuntimeError('A recent successful full sample is required')
    if latest.get('archiving_pvs') != 903 or not (OUT / 'passes.jsonl').stat().st_size:
        raise RuntimeError('The full fixture and real pass evidence are required')
    if latest['clock'] != 'NTPSynchronized=yes':
        raise RuntimeError('The clock must be synchronized')
    for component in collect.INSTANCES:
        evidence = latest.get('gc', {}).get(component, {})
        if not evidence.get('heap_events') or not evidence.get('pause_events'):
            raise RuntimeError('Real heap and pause events are required: ' + component)
    latency = latest.get('latency', {})
    if latency.get('queried_pvs') != 903 or latency.get('visible_probes') != len(measure.REPRESENTATIVES):
        raise RuntimeError('Real retrieval and visibility evidence is required')
    checked(['systemctl', 'is-active', collect.UNIT, collect.IOC_UNIT, 'mariadb.service'])
    end = now + datetime.timedelta(seconds=DURATION)
    record = {'started_at': now.isoformat(), 'earliest_finish_at': end.isoformat(),
              'duration_seconds': DURATION, 'boot_id': BOOT.read_text().strip(),
              'monotonic_start': time.monotonic(), 'fixture_sha256': latest['fixture_sha256'],
              'readiness_sample': latest['raw_directory'], 'unit_before_observation': unit_state(),
              'measurement_schema': 2, 'existing_store_data_preserved': True,
              'jvm_identity': {name: {key: value[key] for key in ('pid', 'start')}
                               for name, value in json.loads((OUT / 'state.json').read_text())['processes'].items()
                               if name in collect.INSTANCES}}
    timer = '[Unit]\nDescription=Finish the ETL soak observation\n[Timer]\n'
    timer += 'OnCalendar=' + end.strftime('%Y-%m-%d %H:%M:%S UTC') + '\n'
    timer += 'AccuracySec=1s\nPersistent=true\n[Install]\nWantedBy=timers.target\n'
    (UNITS / (FINISH + '.timer')).write_text(timer)
    collect.write_json(manifest, record)
    checked(['systemctl', 'daemon-reload'])
    checked(['systemctl', 'enable', '--now', SAMPLER + '.timer', FINISH + '.timer'])
    print(json.dumps(record))


def finish():
    manifest = json.loads((OUT / 'observation.json').read_text())
    if (OUT / 'shutdown.json').exists():
        raise RuntimeError('A shutdown measurement already exists')
    end = datetime.datetime.fromisoformat(manifest['earliest_finish_at'])
    remaining = (end - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    if remaining > 2:
        raise RuntimeError('The observation window has not elapsed')
    if remaining > 0:
        time.sleep(remaining)
    result = {'observation': manifest, 'finish_started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'boot_unchanged': BOOT.read_text().strip() == manifest['boot_id'],
              'monotonic_elapsed_seconds': time.monotonic() - manifest['monotonic_start']}
    checked(['systemctl', 'stop', SAMPLER + '.timer'])
    result['final_sample'] = command(['systemctl', 'start', SAMPLER + '.service'])
    final_gc = OUT / 'final-gc'
    final_gc.mkdir()
    try:
        result['complete_gc_recordings'] = measure.gc(OUT, final_gc,
            datetime.datetime.now(datetime.timezone.utc).isoformat(), complete=True)
    except Exception as error:
        result['complete_gc_recordings'] = {'error': type(error).__name__, 'message': str(error)}
    result['before'] = unit_state()
    collect.write_json(OUT / 'shutdown-started.json', result)
    began = time.monotonic()
    try:
        result['stop'] = command(['systemctl', 'stop', collect.UNIT])
    except subprocess.TimeoutExpired:
        result['stop'] = {'rc': None, 'error': 'systemctl stop did not return within 600 seconds'}
    result['stop_elapsed_seconds'] = time.monotonic() - began
    result['after'] = unit_state()
    result['final_journal'] = command(['/usr/bin/python3', str(TOOLS / 'collect.py'), str(OUT),
                                       str(TOOLS / 'pvs-all.csv'), '--journal-only'])
    result['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    collect.write_json(OUT / 'shutdown.json', result)
    print(json.dumps({'finished_at': result['finished_at'], 'stop_elapsed_seconds': result['stop_elapsed_seconds'],
                      'stop_rc': result['stop']['rc'], 'after': result['after']}))


def main():
    os.umask(0o077)
    os.environ['PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'finish'])
    args = parser.parse_args()
    {'start': start, 'finish': finish}[args.action]()


if __name__ == '__main__':
    main()
