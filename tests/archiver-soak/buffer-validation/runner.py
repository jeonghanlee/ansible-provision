#!/usr/bin/env python3
"""Run bounded real-appliance stress and retain independent native-path evidence."""

import collections
import csv
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import time
import urllib.request

TOOLS = Path('/usr/local/share/buffer29')
ROOT = Path('/var/lib/buffer29')
SERVICE = 'epicsarchiverap-maven.service'
IOC = 'etl-soak-ioc.service'
APP = Path('/opt/epicsarchiverap-maven')
JAVA = '/usr/bin/java'
CP = str(TOOLS / 'classes') + ':' + str(APP / 'engine/webapps/engine/WEB-INF/classes') + ':' + str(APP / 'engine/webapps/engine/WEB-INF/lib/*')
HEADER = struct.Struct('<IHHIIQQqQQ')
MAGIC = 0x42323931
NS = 1000000000
FAST = set((TOOLS / 'fast.txt').read_text().splitlines())
ROWS = list(csv.DictReader((Path('/usr/local/share/etl-soak') / 'pvs-all.csv').open()))
PVS = {r['pv']: r for r in ROWS}
assert len(FAST) == 110 and len(PVS) == 903
ACTIVE_CAPTURE = None


def now():
    return time.monotonic_ns()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def save(path, data):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(data, sort_keys=True, indent=2) + '\n')
    temporary.replace(path)


class Incomplete(RuntimeError):
    pass


class ProductFailure(RuntimeError):
    pass


def execute(args, deadline, log=None):
    remaining = (deadline - now()) / NS
    if remaining <= 0:
        raise Incomplete('Monotonic deadline exceeded')
    result = subprocess.run(args, stdout=log or subprocess.PIPE, stderr=log or subprocess.STDOUT,
                            timeout=remaining, text=True)
    if result.returncode:
        raise Incomplete('Command failed: ' + Path(args[0]).name + ', rc=' + str(result.returncode))
    return result.stdout or ''


def control(out, mode, origin, deadline):
    temporary = out / 'control.tmp'
    temporary.write_text('{} {} {}\n'.format(mode, origin, deadline))
    temporary.chmod(0o644)
    temporary.replace(out / 'control')


def validate_pass(pass_id, actual_pass, expected_first):
    """Validate actual native-write evidence for a completed pass."""
    writes = actual_pass['writes']
    injections = actual_pass['injections']
    phase = actual_pass['phase']
    if phase not in (2, 3, 4):
        if injections:
            raise Incomplete('Injection outside an eligible phase in pass {}'.format(pass_id))
        return
    if len(injections) != 1 or not writes:
        raise Incomplete('Missing or duplicate native injection in pass {}'.format(pass_id))
    injected = injections[0]
    if injected['wait'] < actual_pass['requested'] or injected['error']:
        raise Incomplete('Delay was not demonstrated in pass {}'.format(pass_id))
    expected_position = 0 if phase == 4 or expected_first else len(writes) - 1
    if injected['position'] != expected_position:
        raise Incomplete('First/last native-write alternation failed in pass {}'.format(pass_id))
    if expected_position != 0 and not injected.get('final_flush', False):
        raise Incomplete('Last-write injection did not occur in the final native flush')


class Capture:
    def __init__(self, out):
        self.out = out
        self.path = None
        self.stream = None
        self.offset = 0
        self.pid = None
        self.proc = None
        self.seen = collections.Counter()
        self.identities = {}
        self.lost = {}
        self.initial_lost = {}
        self.input_since = collections.Counter()
        self.swap = {}
        self.persisted = {}
        self.passes = {}
        self.coverage = collections.Counter()
        self.selection = []
        self.physical = {}
        self.config = None
        self.final_flush = False
        self.last_status_ns = 0
        self.ready = False
        self.targets = None
        self.errors = []
        self.exposures = (out / 'exposures.jsonl').open('a')
        self.pb_receipts = (out / 'pb-receipts.jsonl').open('a')
        self.pass_receipts = (out / 'passes.jsonl').open('a')
        (out / 'pb').mkdir()

    def identity(self):
        if self.pid is None:
            return
        stat = Path('/proc/{}/stat'.format(self.pid)).read_text()
        start_ticks = stat[stat.rfind(')') + 2:].split()[19]
        identity = (Path('/proc/sys/kernel/random/boot_id').read_text().strip(), start_ticks)
        if self.proc is None:
            self.proc = identity
            save(self.out / 'engine-identity.json', {'pid': self.pid, 'boot_id': identity[0], 'start_ticks': start_ticks})
        elif self.proc != identity:
            raise Incomplete('Engine process identity changed')

    def locate(self):
        if self.stream:
            return
        candidates = []
        for path in self.out.glob('trace-*.bin'):
            pid = int(path.stem.split('-')[1])
            try:
                args = Path('/proc/{}/cmdline'.format(pid)).read_bytes()
            except FileNotFoundError:
                continue
            if b'/engine' in args:
                candidates.append((path, pid))
        if len(candidates) > 1:
            raise Incomplete('Multiple engine traces')
        if candidates:
            self.path, self.pid = candidates[0]
            self.stream = self.path.open('rb')
            self.identity()

    def preserve(self, name, raw):
        if name not in FAST:
            return
        source = Path(raw.decode())
        if not source.is_absolute() or not str(source).startswith('/arch/sts/') or source.suffix != '.pb':
            raise Incomplete('Unexpected native PB source path')
        stat = source.stat()
        key = (stat.st_dev, stat.st_ino)
        if key in self.physical:
            if self.physical[key]['pv'] != name:
                raise Incomplete('Physical inode associated with conflicting PVs')
            return
        target = self.out / 'pb' / ('{}-{}.pb'.format(stat.st_dev, stat.st_ino))
        os.link(source, target)
        receipt = {'pv': name, 'source': str(source), 'preserved': str(target),
                   'device': stat.st_dev, 'inode': stat.st_ino, 'first_seen_mono_ns': now()}
        self.physical[key] = receipt
        self.pb_receipts.write(json.dumps(receipt, sort_keys=True) + '\n')
        self.pb_receipts.flush()

    def observe_counter(self, name, capacity, lost, identity):
        if name not in PVS:
            raise Incomplete('Unexpected input PV')
        expected = {0.1: 110, 1.0: 11, 10.0: 2}[float(PVS[name]['period'])]
        if capacity != expected:
            raise Incomplete('Effective capacity differs from the accepted configuration')
        if name in self.identities and self.identities[name] != identity:
            raise Incomplete('Sample buffer identity changed')
        if lost < self.lost.get(name, 0):
            raise Incomplete('Counter decreased')
        self.identities[name] = identity
        self.initial_lost.setdefault(name, lost)
        self.lost[name] = lost

    def record(self, values, name, payload):
        _, kind, _, _, capacity, stamp, pass_id, lost, first, second = values
        if kind in (1, 2):
            self.observe_counter(name, capacity, lost, second)
        if kind == 1:
            if name in FAST and not payload:
                raise Incomplete('Fast input payload missing')
            self.seen[name] += 1
            self.input_since[name] += 1
        elif kind == 2:
            previous = self.swap.get(name)
            count = self.input_since[name]
            self.input_since[name] = 0
            self.swap[name] = (stamp, pass_id)
            if previous and name in FAST:
                interval = stamp - previous[0]
                exposure = {'pv': name, 'mono_ns': stamp, 'previous_mono_ns': previous[0],
                            'pass': pass_id, 'interval_ns': interval, 'actual_inputs': count,
                            'capacity': capacity, 'counter': lost, 'qualified': False}
                actual_pass = self.passes.get(pass_id)
                if actual_pass:
                    exposure.update(phase=actual_pass['phase'], cycle=actual_pass['cycle'])
                    injection = actual_pass['injections']
                    level = actual_pass['phase']
                    if len(injection) == 1 and level in (2, 3):
                        low_time, low_count, delay = ((10400000000, 104, 500000000) if level == 2
                                                      else (10700000000, 107, 800000000))
                        exposure['qualified'] = (injection[0]['wait'] >= delay
                                                 and low_time <= interval <= 11000000000
                                                 and low_count <= count <= 110)
                        if exposure['qualified']:
                            self.coverage[(name, actual_pass['cycle'], level)] += 1
                self.exposures.write(json.dumps(exposure, sort_keys=True) + '\n')
        elif kind == 3:
            self.passes[pass_id] = {'start': stamp, 'phase': capacity, 'cycle': second,
                                    'requested': first, 'injections': [], 'writes': [], 'ended': False}
        elif kind == 4:
            actual_pass = self.passes[pass_id]
            actual_pass['ended'] = True
            actual_pass['end'] = stamp
            if lost:
                raise Incomplete('Native observer reported an error')
            writes = actual_pass['writes']
            injections = actual_pass['injections']
            if first != len(writes) or second != len(injections):
                raise Incomplete('Native pass evidence disagrees')
            try:
                validate_pass(pass_id, actual_pass, len(self.selection) % 2 == 0)
            except Incomplete as error:
                self.errors.append(str(error))
                control(self.out, 'off', now(), 0)
                raise
            if actual_pass['phase'] in (2, 3):
                self.selection.append(injections[0]['position'])
            for write in writes:
                swapped = self.swap.get(write['pv'])
                if swapped and swapped[1] == pass_id:
                    self.persisted[write['pv']] = swapped[0]
            if self.errors:
                control(self.out, 'off', now(), 0)
                raise Incomplete(self.errors[0])
            self.pass_receipts.write(json.dumps(dict(actual_pass, pass_id=pass_id), sort_keys=True) + '\n')
            self.pass_receipts.flush()
            actual_pass['write_count'] = len(writes)
            actual_pass['writes'] = writes[:1] + writes[-1:] if len(writes) > 1 else writes
            boundaries = actual_pass.get('io_boundaries', [])
            actual_pass['io_boundaries'] = boundaries[:1] + boundaries[-1:] if len(boundaries) > 1 else boundaries
        elif kind == 5:
            if lost or second == 0:
                raise Incomplete('Native PB write failed')
            actual_pass = self.passes[pass_id]
            actual_pass['writes'].append({'pv': name, 'position': capacity, 'mono_ns': stamp,
                                          'began': first, 'bytes': second, 'path': payload.decode()})
            self.preserve(name, payload)
        elif kind == 6:
            self.passes[pass_id]['injections'].append({'pv': name, 'position': capacity,
                                                       'requested': first, 'wait': second,
                                                       'error': lost, 'mono_ns': stamp,
                                                       'final_flush': self.final_flush})
        elif kind == 7:
            if second != HEADER.size:
                raise Incomplete('Trace header version mismatch')
            self.ready = True
        elif kind == 8:
            raise Incomplete('Java observer reported an error')
        elif kind == 9:
            actual = (struct.unpack('<d', struct.pack('<Q', first))[0],
                      struct.unpack('<d', struct.pack('<Q', second))[0])
            if actual != (10.0, 1.0):
                raise Incomplete('Effective write period or margin differs from the accepted configuration')
            self.config = actual
        elif kind == 10:
            self.final_flush = bool(capacity)
        elif kind == 11:
            if lost:
                raise Incomplete('Native filesystem inspection failed')
            self.passes[pass_id].setdefault('io_boundaries', []).append(
                {'pv': name, 'final_flush': bool(capacity), 'offset': first, 'size': second, 'mono_ns': stamp})
        else:
            raise Incomplete('Unknown native record type')

    def poll(self):
        self.locate()
        if self.stream is None:
            return
        self.identity()
        while True:
            self.stream.seek(self.offset)
            raw = self.stream.read(HEADER.size)
            if len(raw) < HEADER.size:
                break
            fields = HEADER.unpack(raw)
            magic, _, name_length, length = fields[:4]
            if magic != MAGIC or name_length >= 512 or length > 1048576:
                raise Incomplete('Invalid trace record')
            body = self.stream.read(name_length + length)
            if len(body) < name_length + length:
                break
            self.offset += HEADER.size + len(body)
            self.record(fields, body[:name_length].decode(), body[name_length:])
        self.exposures.flush()

    def summary(self):
        return {'input_pvs': len(self.seen), 'counter_pvs': len(self.lost), 'fast_input_pvs': len(FAST & set(self.seen)),
                'input_events': sum(self.seen.values()), 'lost_events': sum(self.lost.values()),
                'passes': len(self.passes), 'native_injections': sum(len(p['injections']) for p in self.passes.values()),
                'preserved_pb_files': len(self.physical), 'tool_findings': len(self.errors),
                'effective_write_period': self.config[0] if self.config else None,
                'effective_margin': self.config[1] if self.config else None}

    def freeze_targets(self):
        completed = [p for p in self.passes.values() if p['ended'] and p['writes']]
        if not completed:
            raise Incomplete('No complete native-write pass')
        first = completed[-1]['writes'][0]['pv']
        exception = first if first in FAST else None
        self.targets = FAST - ({exception} if exception else set())
        save(self.out / 'stress-targets.json', {'targets': sorted(self.targets), 'exception': exception,
                                               'reason': 'Only a fast PV at the first native write may precede every injection'})

    def assert_coverage(self, cycles):
        if self.errors:
            raise Incomplete(self.errors[0])
        if len(self.seen) != 903 or len(self.lost) != 903:
            raise Incomplete('Incomplete all-PV input/counter coverage')
        missing = [{'pv': pv, 'cycle': cycle, 'phase': level, 'count': self.coverage[(pv, cycle, level)]}
                   for pv in sorted(self.targets) for cycle in cycles for level in (2, 3)
                   if self.coverage[(pv, cycle, level)] < 1]
        save(self.out / 'coverage.json', {'counts': [{'pv': key[0], 'cycle': key[1], 'phase': key[2], 'count': value}
                                                   for key, value in sorted(self.coverage.items())], 'missing': missing})
        if missing:
            raise Incomplete('Measured stress exposure missing for {} target/cycle/level combinations'.format(len(missing)))


def wait_until(capture, boundary, deadline, condition=None):
    while True:
        if now() >= deadline:
            raise Incomplete('Monotonic deadline exceeded')
        capture.poll()
        if now() - capture.last_status_ns >= 5 * NS:
            path = capture.out / 'status.json'
            status = json.loads(path.read_text()) if path.exists() else {}
            status.update(capture.summary(), observed_mono_ns=now())
            save(path, status)
            capture.last_status_ns = now()
        if now() >= boundary and (condition is None or condition()):
            return
        time.sleep(0.2)


def drain(capture, cutoff, deadline):
    wait_until(capture, cutoff, deadline,
               lambda: all(capture.persisted.get(pv, 0) > cutoff for pv in FAST))


def compare(capture, label, windows, deadline, allow_loss=False, baseline=None):
    capture.poll()
    snapshot = capture.out / label
    snapshot.mkdir()
    trace = snapshot / 'trace.bin'
    with capture.path.open('rb') as source, trace.open('xb') as target:
        remaining = capture.offset
        while remaining:
            block = source.read(min(1048576, remaining))
            if not block:
                raise Incomplete('Trace snapshot was truncated')
            target.write(block)
            remaining -= len(block)
    physical = snapshot / 'pb'
    physical.mkdir()
    receipts = []
    for receipt in capture.physical.values():
        source = Path(receipt['preserved'])
        size = source.stat().st_size
        destination = physical / source.name
        with source.open('rb') as reader, destination.open('xb') as writer:
            remaining = size
            while remaining:
                block = reader.read(min(1048576, remaining))
                if not block:
                    raise Incomplete('Physical PB snapshot was truncated')
                writer.write(block)
                remaining -= len(block)
        receipts.append(dict(receipt, snapshot=str(destination), bytes=size, sha256=digest(destination)))
    save(snapshot / 'physical-manifest.json', receipts)
    with (snapshot / 'decode.raw.log').open('w') as log:
        for mode, source in [('inputs', trace), ('physical', physical)]:
            execute([JAVA, '-Xmx512m', '-cp', CP, 'PBDecode', mode, str(source), str(snapshot / (mode + '.tsv')),
                     str(TOOLS / 'fast.txt')], deadline, log)
    if re.search(r'\b(?:ERROR|WARN|Exception|PBParseException)\b', (snapshot / 'decode.raw.log').read_text()):
        raise Incomplete('Native decoder reported a parse or I/O diagnostic')
    return compare_decoded(snapshot, windows, capture.lost, deadline, allow_loss, baseline)


def compare_decoded(snapshot, windows, counters, deadline, allow_loss=False, baseline=None):
    """Reconcile native decoder output while retaining order and event multiplicity."""
    spools = {}
    for mode in ('inputs', 'physical'):
        directory = snapshot / mode
        directory.mkdir()
        handles = {pv: (directory / (str(i) + '.tsv')).open('w') for i, pv in enumerate(sorted(FAST))}
        spools[mode] = {pv: Path(handle.name) for pv, handle in handles.items()}
        try:
            with (snapshot / (mode + '.tsv')).open() as source:
                for line in source:
                    pv = line.split('\t', 1)[0]
                    handles[pv].write(line)
        finally:
            for handle in handles.values():
                handle.close()
    results = {}
    baseline = baseline or {pv: 0 for pv in FAST}
    for pv in sorted(FAST):
        inputs = [line.rstrip('\n').split('\t') for line in spools['inputs'][pv].read_text().splitlines()]
        stored = [tuple(line.split('\t')[2:]) for line in spools['physical'][pv].read_text().splitlines()]
        counter_delta = counters[pv] - baseline.get(pv, 0)
        per_window = []
        for start, end in windows:
            expected = [tuple(row[2:]) for row in inputs if start <= int(row[1]) < end]
            if not expected:
                raise Incomplete('Missing fast inputs in declared comparison window')
            stamps = [(int(row[0]), int(row[1])) for row in expected]
            if any(right < left for left, right in zip(stamps, stamps[1:])):
                raise Incomplete('Input timestamp order decreased')
            actual = [row for row in stored if stamps[0] <= (int(row[0]), int(row[1])) <= stamps[-1]]
            cursor = 0
            missing = 0
            conflict = 0
            for item in expected:
                if cursor < len(actual) and actual[cursor] == item:
                    cursor += 1
                else:
                    missing += 1
            conflict = len(actual) - cursor
            per_window.append({'start_mono_ns': start, 'end_mono_ns': end, 'inputs': len(expected),
                               'stored': len(actual), 'missing': missing, 'conflicting_or_extra': conflict})
        results[pv] = {'windows': per_window, 'counter_delta': counter_delta}
    save(snapshot / 'comparison.json', results)
    missing_total = sum(w['missing'] for r in results.values() for w in r['windows'])
    conflicts = sum(w['conflicting_or_extra'] for r in results.values() for w in r['windows'])
    if conflicts:
        raise ProductFailure('Native PB output contains conflicting or extra events')
    if allow_loss:
        if any(sum(w['missing'] for w in r['windows']) != r['counter_delta'] for r in results.values()):
            raise Incomplete('Expected-loss native PB gaps and buffer counters disagree')
        if missing_total == 0:
            raise Incomplete('Expected-loss control did not demonstrate loss')
    elif missing_total:
        raise ProductFailure('Actual inputs are missing from physical PB output')
    if now() >= deadline:
        raise Incomplete('Comparison exceeded the monotonic deadline')
    return {'fast_pvs': len(results), 'missing': missing_total, 'conflicts': conflicts,
            'input_events': sum(w['inputs'] for r in results.values() for w in r['windows'])}


def start_capture(mode, out, deadline):
    global ACTIVE_CAPTURE
    execute(['systemctl', 'start', IOC, SERVICE], deadline)
    capture = Capture(out)
    ACTIVE_CAPTURE = capture
    return capture


def registration(deadline, out):
    while now() < deadline:
        try:
            with urllib.request.urlopen('http://127.0.0.1:17665/mgmt/bpl/getAllPVs', timeout=2) as response:
                existing = json.load(response)
            if existing:
                raise Incomplete('Preflight requires an empty appliance')
            break
        except (OSError, ValueError):
            time.sleep(0.5)
    else:
        raise Incomplete('Management readiness deadline exceeded')
    with (out / 'registration.raw.log').open('w') as log:
        execute(['/usr/bin/python3', '/usr/local/share/etl-soak/register.py',
                 '/usr/local/share/etl-soak/pvs-all.csv', str(out)], deadline, log)
    rows = list(csv.DictReader((out / 'registered.csv').open()))
    if len(rows) != 903 or any(r['reply_status'] in ('', 'missing') for r in rows):
        raise Incomplete('Incomplete fixture registration replies')


def preflight(out, origin, deadline):
    readiness_deadline = origin + 300 * NS
    capture = start_capture('preflight', out, readiness_deadline)
    registration(readiness_deadline, out)
    wait_until(capture, origin, readiness_deadline,
               lambda: capture.ready and capture.config == (10.0, 1.0) and len(capture.seen) == 903
               and FAST <= set(capture.persisted))
    if any(capture.lost.values()):
        raise ProductFailure('Buffer-full losses occurred during registration/readiness')
    capture.freeze_targets()
    save(out / 'readiness.json', dict(capture.summary(), ready_mono_ns=now(), elapsed_seconds=(now() - origin) / NS))
    windows = []
    for mode in ('base', 'p500', 'p800'):
        start = now()
        end = start + 120 * NS
        control(out, mode, start, deadline)
        save(out / 'status.json', dict(capture.summary(), state='Preflight', stage=mode,
                                        stage_start_ns=start, stage_end_ns=end, deadline_ns=deadline))
        wait_until(capture, end, deadline)
        windows.append((start, end))
    control(out, 'off', now(), deadline)
    drain(capture, windows[-1][1], deadline)
    if any(capture.lost.values()):
        raise ProductFailure('Unexpected buffer-full loss in a normal or within-margin stage')
    capture.assert_coverage([0])
    normal = compare(capture, 'normal-frozen', windows, deadline)
    save(out / 'normal-verdict.json', {'result': 'Passed', 'comparison': normal, 'windows': windows,
                                      'frozen_mono_ns': now()})
    # Recovery inputs remain inside this full comparison; no interval is discarded.
    control_start = now()
    control(out, 'control', control_start, deadline)
    wait_until(capture, control_start, deadline,
               lambda: any(p['phase'] == 4 and p['ended'] and len(p['injections']) == 1
                           for p in capture.passes.values()))
    control(out, 'off', now(), deadline)
    cutoff = now() + 30 * NS
    wait_until(capture, cutoff, deadline)
    execute(['systemctl', 'stop', IOC], deadline)
    drain(capture, cutoff, deadline)
    full = compare(capture, 'full-preflight', [(windows[0][0], cutoff)], deadline, True)
    full['other_pv_buffer_full_events'] = sum(capture.lost[pv] for pv in set(PVS) - FAST)
    if capture.errors:
        raise Incomplete(capture.errors[0])
    save(out / 'verdict.json', {'result': 'Passed', 'normal': normal, 'expected_loss': full,
                               'origin_mono_ns': origin, 'finished_mono_ns': now(),
                               'deadline_mono_ns': deadline, 'summary': capture.summary()})
    return capture


def main_run(out, origin, deadline):
    preflight_result = json.loads((ROOT / 'preflight/verdict.json').read_text())
    if preflight_result['result'] != 'Passed':
        raise Incomplete('A Passed preflight is required')
    capture = start_capture('main', out, deadline)
    wait_until(capture, origin, deadline,
               lambda: capture.ready and capture.config == (10.0, 1.0) and len(capture.seen) == 903
               and FAST <= set(capture.persisted))
    if any(capture.lost.values()):
        raise ProductFailure('Fresh main execution already has buffer-full loss')
    frozen = json.loads((ROOT / 'preflight/stress-targets.json').read_text())
    capture.targets = set(frozen['targets'])
    save(out / 'stress-targets.json', frozen)
    start = now()
    cutoff = start + 14400 * NS
    control(out, 'main', start, cutoff)
    save(out / 'observation.json', {'start_mono_ns': start, 'end_mono_ns': cutoff,
                                    'duration_seconds': 14400, 'cycles': 24})
    for hour in (1, 2, 3, 4):
        wait_until(capture, start + hour * 3600 * NS, deadline)
        save(out / ('checkpoint-{}.json'.format(hour)), dict(capture.summary(), hours=hour,
                                                             observed_mono_ns=now()))
        save(out / 'status.json', dict(capture.summary(), state='Main observation', completed_hours=hour,
                                        start_mono_ns=start, cutoff_mono_ns=cutoff))
    control(out, 'off', cutoff, deadline)
    execute(['systemctl', 'stop', IOC], deadline)
    drain(capture, cutoff, deadline)
    if any(capture.lost.values()):
        raise ProductFailure('Buffer-full loss occurred in the positive observation')
    capture.assert_coverage(range(1, 25))
    result = compare(capture, 'final', [(start, cutoff)], deadline)
    save(out / 'verdict.json', {'result': 'Passed', 'comparison': result, 'summary': capture.summary(),
                               'start_mono_ns': start, 'cutoff_mono_ns': cutoff, 'finished_mono_ns': now()})
    return capture


def run():
    os.umask(0o077)
    mode = sys.argv[1]
    if mode not in ('preflight', 'main'):
        raise ValueError('Expected preflight or main')
    out = ROOT / mode
    if (out / 'attempt.json').exists():
        raise Incomplete('Refusing an automatic retry of an existing attempt')
    out.mkdir(exist_ok=True)
    shutil.chown(out, 'mid-srv', 'mid')
    out.chmod(0o770)
    origin = now()
    deadline = origin + (1200 if mode == 'preflight' else 16200) * NS
    control(out, 'off', origin, deadline)
    save(out / 'attempt.json', {'mode': mode, 'origin_mono_ns': origin, 'deadline_mono_ns': deadline})
    save(out / 'status.json', {'state': 'Starting', 'mode': mode, 'origin_mono_ns': origin})
    capture = None
    try:
        capture = preflight(out, origin, deadline) if mode == 'preflight' else main_run(out, origin, deadline)
        save(out / 'status.json', dict(capture.summary(), state='Passed', mode=mode))
    except BaseException as error:
        result = 'Failed' if isinstance(error, ProductFailure) else 'Incomplete'
        save(out / 'verdict.json', {'result': result, 'error_class': type(error).__name__,
                                   'reason': str(error) or type(error).__name__, 'finished_mono_ns': now(), 'deadline_mono_ns': deadline})
        save(out / 'status.json', {'state': result, 'mode': mode, 'reason': str(error) or type(error).__name__})
        raise
    finally:
        control(out, 'off', now(), 0)
        subprocess.run(['systemctl', 'stop', IOC], timeout=30, check=False)
        capture = capture or ACTIVE_CAPTURE
        if capture:
            try:
                capture.poll()
            except Exception:
                pass
            save(out / 'passes.json', capture.passes)
            save(out / 'final-counters.json', capture.lost)
            save(out / 'final-input-counts.json', capture.seen)


if __name__ == '__main__':
    run()
