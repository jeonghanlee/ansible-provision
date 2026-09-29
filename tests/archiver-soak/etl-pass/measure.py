#!/usr/bin/env python3
"""Capture real GC events, retrieval freshness and bounded visibility probes."""

import concurrent.futures
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.parse
import urllib.request

import resource_helpers

JAVA_BIN = Path('/usr/lib/jvm/java-21-openjdk/bin')
CAGET = '/opt/epics/1.3.0/rocky-8.10/7.0.10/base/bin/linux-x86_64/caget'
RETRIEVAL = 'http://127.0.0.1:17668/retrieval/data/getData.json'
INSTANCES = ('mgmt', 'engine', 'etl', 'retrieval')
EVENTS = 'jdk.GCHeapSummary,jdk.GarbageCollection,jdk.GCPhasePause,jdk.DataLoss'
REPRESENTATIVES = ('AASOAK:S1:CH01', 'AASOAK:FAST:CH01', 'AASOAK:SLOW:CH01',
                   'AASOAK:WF:CH01', 'AASOAK:L2F:CH001', 'AASOAK:L2WF:CH01')
POLL_SECONDS = 1.0
PROBE_TIMEOUT_SECONDS = 30.0
FRESHNESS_WINDOW_SECONDS = 30
RETRIEVAL_WORKERS = 2
JFR_ARCHIVE_LIMIT_BYTES = 512 * 1024 * 1024
JFR_DUMP_RESERVE_BYTES = 72 * 1024 * 1024
MINIMUM_FREE_BYTES = 2 * 1024 * 1024 * 1024
JSTAT_FIELDS = ('S0C', 'S1C', 'S0U', 'S1U', 'EC', 'EU', 'OC', 'OU', 'MC', 'MU',
                'CCSC', 'CCSU', 'YGC', 'YGCT', 'FGC', 'FGCT', 'CGC', 'CGCT', 'GCT')


def command(args, timeout=90):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError('Command failed: ' + args[0] + ': ' + str(result.returncode))
    return result.stdout


def append(path, fields, rows):
    new = not path.exists()
    with path.open('a', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        if new:
            writer.writeheader()
        writer.writerows(rows)


def dump_jfr(out, raw, component, pid, complete=False):
    retained = sum(path.stat().st_size for path in (out / 'raw').rglob('*.jfr'))
    if not complete and retained > JFR_ARCHIVE_LIMIT_BYTES - JFR_DUMP_RESERVE_BYTES:
        raise RuntimeError('JFR snapshot archive limit reached')
    filesystem = os.statvfs(out)
    if filesystem.f_bavail * filesystem.f_frsize < MINIMUM_FREE_BYTES:
        raise RuntimeError('Insufficient free space for measurement')
    temporary = out / 'jvm' / (component + '-checkpoint.jfr')
    args = [str(JAVA_BIN / 'jcmd'), str(pid), 'JFR.dump', 'name=etl-soak',
            'filename=' + str(temporary)]
    if not complete:
        args += ['maxage=10m', 'maxsize=8m']
    response = command(args)
    if not temporary.exists() or not temporary.stat().st_size:
        raise RuntimeError('Missing JFR checkpoint: ' + component)
    destination = raw / (component + '.jfr')
    temporary.replace(destination)
    destination.chmod(0o600)
    (raw / (component + '-jfr-dump.txt')).write_text(response)
    return destination


def gc(out, raw, ts, complete=False):
    pids = resource_helpers.jvm_pids()
    if set(pids) != set(INSTANCES):
        raise RuntimeError('Expected four appliance JVMs')
    summary = {}
    for component in INSTANCES:
        pid = pids[component]
        data = command([str(JAVA_BIN / 'jstat'), '-gc', pid])
        (raw / (component + '-jstat.txt')).write_text(data)
        lines = data.splitlines()
        fields = dict(zip(lines[0].split(), lines[1].split()))
        row = {'ts': ts, 'component': component, 'pid': pid}
        for key in JSTAT_FIELDS:
            value = fields.get(key, '')
            if value and value != '-':
                float(value)
            row[key] = value
        append(out / 'jstat.csv', ['ts', 'component', 'pid', *JSTAT_FIELDS], [row])
        recording = dump_jfr(out, raw, component, pid, complete)
        data = command([str(JAVA_BIN / 'jfr'), 'print', '--json', '--events', EVENTS,
                        str(recording)])
        events = json.loads(data)['recording']['events']
        heaps, pauses, collections = [], [], []
        for event in events:
            values = event['values']
            kind = event['type']
            common = {'component': component, 'pid': pid, 'ts': values['startTime'],
                      'gc_id': values.get('gcId', '')}
            if kind == 'jdk.GCHeapSummary':
                heaps.append({**common, 'when': values['when'], 'heap_bytes': values['heapUsed']})
            elif kind == 'jdk.GCPhasePause':
                pauses.append({**common, 'name': values['name'], 'duration': values['duration']})
            elif kind == 'jdk.GarbageCollection':
                collections.append({**common, **{key: values[key] for key in
                    ('name', 'cause', 'duration', 'sumOfPauses', 'longestPause')}})
            elif kind == 'jdk.DataLoss':
                raise RuntimeError('JFR data loss: ' + component)
        append(out / 'gc-heap.csv', ['component', 'pid', 'ts', 'gc_id', 'when', 'heap_bytes'], heaps)
        append(out / 'gc-pauses.csv', ['component', 'pid', 'ts', 'gc_id', 'name', 'duration'], pauses)
        append(out / 'gc-collections.csv', ['component', 'pid', 'ts', 'gc_id', 'name', 'cause',
                                           'duration', 'sumOfPauses', 'longestPause'], collections)
        after = [row['heap_bytes'] for row in heaps if row['when'] == 'After GC']
        summary[component] = {'pid': pid, 'heap_events': len(heaps), 'pause_events': len(pauses),
                              'collection_events': len(collections),
                              'last_after_gc_bytes': after[-1] if after else None,
                              'max_observed_heap_bytes': max((row['heap_bytes'] for row in heaps), default=None),
                              'recording_bytes': recording.stat().st_size}
    return summary


def iso(epoch):
    return datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).isoformat().replace('+00:00', 'Z')


def request(pv, start, end):
    query = urllib.parse.urlencode({'pv': pv, 'from': iso(start), 'to': iso(end)})
    began, monotonic = time.time(), time.monotonic()
    with urllib.request.urlopen(RETRIEVAL + '?' + query, timeout=15) as response:
        status, body = response.status, response.read()
    ended, elapsed = time.time(), time.monotonic() - monotonic
    if status != 200:
        raise RuntimeError('Retrieval HTTP ' + str(status))
    decoded = json.loads(body)
    if not isinstance(decoded, list):
        raise RuntimeError('Unexpected retrieval response')
    samples = [sample for block in decoded for sample in block.get('data', [])
               if 'secs' in sample and 'nanos' in sample]
    return samples, {'request_started': iso(began), 'response_finished': iso(ended),
                     'http': status, 'duration_ms': round(elapsed * 1000, 3),
                     'response_bytes': len(body), 'response_sha256': hashlib.sha256(body).hexdigest()}


def timestamp(sample):
    return int(sample['secs']) + int(sample['nanos']) / 1e9


def freshness(row):
    pv = row['pv']
    ended = time.time()
    result = {'pv': pv, 'method': row['method'], 'period': row['period'], 'policy': row['policy']}
    try:
        samples, response = request(pv, ended - FRESHNESS_WINDOW_SECONDS, ended)
        result.update(response)
        latest = max(samples, key=timestamp) if samples else None
        result.update({'samples': len(samples), 'latest_secs': latest['secs'] if latest else None,
                       'latest_nanos': latest['nanos'] if latest else None,
                       'sample_age_seconds': round(datetime.datetime.fromisoformat(
                           response['response_finished'].replace('Z', '+00:00')).timestamp() -
                           timestamp(latest), 6) if latest else None,
                       'outcome': 'observed' if latest else 'no_sample_in_window'})
    except Exception as error:
        result.update({'outcome': 'error', 'error_type': type(error).__name__})
    return result


def visibility(pv):
    environment = dict(os.environ, EPICS_CA_ADDR_LIST='127.0.0.1', EPICS_CA_AUTO_ADDR_LIST='NO', TZ='UTC')
    began = time.time()
    result = subprocess.run([CAGET, '-w', '5', '-a', '-#', '1', pv], env=environment,
                            capture_output=True, text=True, timeout=10)
    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)', result.stdout)
    row = {'pv': pv, 'source_read_started': iso(began), 'poll_interval_seconds': POLL_SECONDS,
           'source_timestamp_precision_seconds': 0.000001, 'attempts': []}
    if result.returncode or not match:
        return {**row, 'outcome': 'source_error'}
    source = datetime.datetime.fromisoformat(match[1]).replace(tzinfo=datetime.timezone.utc).timestamp()
    row['source_timestamp'] = iso(source)
    deadline = time.monotonic() + PROBE_TIMEOUT_SECONDS
    last_negative_started = None
    while time.monotonic() < deadline:
        try:
            samples, response = request(pv, source - 0.001, source + 0.001)
            matching = [sample for sample in samples if abs(timestamp(sample) - source) <= 0.0000011]
            row['attempts'].append({**response, 'matching_samples': len(matching)})
            if matching:
                observed = datetime.datetime.fromisoformat(response['response_finished'].replace('Z', '+00:00')).timestamp()
                lower = max(0, last_negative_started - source) if last_negative_started is not None else 0
                return {**row, 'outcome': 'visible', 'visibility_lower_seconds': lower,
                        'visibility_upper_seconds': observed - source,
                        'archived_secs': matching[0]['secs'], 'archived_nanos': matching[0]['nanos']}
            last_negative_started = datetime.datetime.fromisoformat(response['request_started'].replace('Z', '+00:00')).timestamp()
        except Exception as error:
            row['attempts'].append({'error_type': type(error).__name__})
        time.sleep(POLL_SECONDS)
    return {**row, 'outcome': 'not_observed_within_probe'}


def latency(out, raw, fixture, ts):
    with fixture.open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    with concurrent.futures.ThreadPoolExecutor(max_workers=RETRIEVAL_WORKERS) as executor:
        results = list(executor.map(freshness, rows))
    (raw / 'freshness.json').write_text(json.dumps(results, indent=2) + '\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=RETRIEVAL_WORKERS) as executor:
        probes = list(executor.map(visibility, REPRESENTATIVES))
    (raw / 'visibility.json').write_text(json.dumps(probes, indent=2) + '\n')
    errors = sum(row['outcome'] == 'error' for row in results)
    failed = sum(row['outcome'] != 'visible' for row in probes)
    summary = {'ts': ts, 'queried_pvs': len(results), 'retrieval_errors': errors,
               'pvs_with_recent_samples': sum(row['outcome'] == 'observed' for row in results),
               'visibility_probes': len(probes), 'visible_probes': len(probes) - failed,
               'max_request_ms': max((row.get('duration_ms', 0) for row in results), default=0),
               'freshness_window_seconds': FRESHNESS_WINDOW_SECONDS,
               'retrieval_workers': RETRIEVAL_WORKERS}
    append(out / 'latency.csv', list(summary), [summary])
    if errors or failed:
        raise RuntimeError('Latency probe incomplete: retrieval=' + str(errors) + ', visibility=' + str(failed))
    return summary
