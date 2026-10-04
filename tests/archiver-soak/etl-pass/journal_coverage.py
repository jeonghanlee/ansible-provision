#!/usr/bin/env python3
"""Archive bounded journal intervals with system-only checkpoints and sequence evidence."""

import datetime
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import time
import uuid

BOOT = Path('/proc/sys/kernel/random/boot_id')
QUERY_TIMEOUT = 60
ENUMERATION_TIMEOUT = 120
ACCOUNTING_ATTEMPTS = 600
ACCOUNTING_SETTLE_SECONDS = 0.005
ACCOUNTING_RETRY_SECONDS = 0.05
# signature, flags, state, reserved, file/machine/boot/sequence ids, sizes and offsets, object and entry
# counts, tail and head sequence numbers.
HEADER = struct.Struct('<8s8xB7x16s16s16s16s64xQQQ')
JOURNAL_ROOT = Path('/var/log/journal')
VOLATILE_ROOT = Path('/run/log/journal')
MARKER_TAG = 'ETL_SOAK_COVERAGE'
COORDINATES = re.compile(r'^s=([0-9a-f]{32});i=([0-9a-f]+);b=([0-9a-f]{32});')


def timestamp(value):
    parsed = datetime.datetime.fromisoformat(value.replace(' UTC', '+00:00').replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise RuntimeError('Journal boundary requires a timezone')
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    delta = parsed - epoch
    return (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds


def coordinates(entry, boot):
    match = COORDINATES.match(entry.get('__CURSOR', ''))
    if not match or match[3] != boot or entry.get('_BOOT_ID') != boot:
        raise RuntimeError('Unsupported journal cursor or changed boot identity')
    number = int(match[2], 16)
    if number <= 0:
        raise RuntimeError('Invalid journal sequence number')
    return match[1], number


def query(arguments, destination):
    command = ['journalctl', '--no-pager', '--all', '-o', 'json', *arguments]
    result = subprocess.run(command, capture_output=True, text=True, timeout=QUERY_TIMEOUT)
    destination.write_text(result.stdout)
    destination.with_suffix(destination.suffix + '.receipt.json').write_text(json.dumps({
        'command': command, 'returncode': result.returncode, 'stderr': result.stderr,
        'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest()}, indent=2) + '\n')
    if result.returncode or result.stderr.strip():
        raise RuntimeError('Journal query failed or reported incomplete access')
    return [json.loads(line) for line in result.stdout.splitlines()]


def daemon_identity():
    result = subprocess.run(['systemctl', 'show', 'systemd-journald.service',
                             '--value', '-p', 'MainPID'], capture_output=True, text=True,
                            timeout=QUERY_TIMEOUT)
    pid = result.stdout.strip()
    if result.returncode or not pid.isdigit() or int(pid) <= 0:
        raise RuntimeError('Journal daemon identity is unavailable')
    fields = Path('/proc/' + pid + '/stat').read_text().rsplit(')', 1)[1].split()
    return {'pid': pid, 'start_ticks': fields[19]}


def validate_interval(rows, anchor, tail, boot):
    identity, first = coordinates(anchor, boot)
    tail_identity, last = coordinates(tail, boot)
    if tail_identity != identity or last < first:
        raise RuntimeError('Journal sequence identity changed or moved backwards')
    selected = {}
    for row in rows:
        stream, number = coordinates(row, boot)
        if first <= number <= last:
            if number in selected and selected[number] != row:
                raise RuntimeError('Conflicting journal sequence payloads')
            selected[number] = row
    if selected.get(first) != anchor or selected.get(last) != tail:
        raise RuntimeError('Required journal interval is missing its system checkpoint')
    ordered = [selected[number] for number in sorted(selected)]
    times = [int(row['__REALTIME_TIMESTAMP']) for row in ordered]
    if times != sorted(times):
        raise RuntimeError('Journal realtime moved backwards within the required interval')
    return ordered


def sequence_holes(interval, boot):
    # journalctl before systemd 248 does not return an entry whose timestamp and content equal the one
    # before it, so an unreturned number is evidence to account for, not proof of a lost record.
    numbers = [coordinates(row, boot)[1] for row in interval]
    return [[before + 1, after - 1] for before, after in zip(numbers, numbers[1:]) if after - before > 1]


def read_header(path):
    # Fixed little-endian header of the journal file format; reading it directly keeps two reads close enough
    # to tell whether the daemon appended in between.
    with path.open('rb') as stream:
        data = stream.read(HEADER.size)
    if len(data) != HEADER.size or data[:8] != b'LPKSHHRH':
        raise RuntimeError('Unsupported journal file header: ' + path.name)
    fields = HEADER.unpack(data)
    return {'file': path.name, 'file_id': fields[2].hex(), 'boot_id': fields[4].hex(),
            'sequence_id': fields[5].hex(), 'state': fields[1],
            'first_sequence': fields[8], 'last_sequence': fields[7], 'entries': fields[6]}


def file_headers(root=None):
    return [read_header(path) for path in sorted((root or JOURNAL_ROOT).glob('*/*.journal'))]


def stable_headers(root=None):
    # Equal reads a few milliseconds apart mean no entry was appended while the files were read.
    # A file being created or rotated can be unreadable for one attempt; a lasting failure is reported.
    failure = RuntimeError('Journal files kept changing during the sequence accounting')
    for attempt in range(ACCOUNTING_ATTEMPTS):
        try:
            files = file_headers(root)
            time.sleep(ACCOUNTING_SETTLE_SECONDS)
            if file_headers(root) == files:
                return files
        except (OSError, RuntimeError) as error:
            failure = RuntimeError('Journal file headers stayed unreadable: ' + str(error))
        time.sleep(ACCOUNTING_RETRY_SECONDS)
    raise failure


def returned_entries(path, first, last):
    process = subprocess.Popen(['journalctl', '--no-pager', '--file', str(path), '-o', 'json',
                                '--output-fields=_BOOT_ID'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        output, errors = process.communicate(timeout=ENUMERATION_TIMEOUT)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        raise RuntimeError('Journal file enumeration exceeded its deadline: ' + path.name)
    if process.returncode or errors.strip():
        raise RuntimeError('Journal file enumeration failed: ' + path.name)
    numbers = [int(COORDINATES.match(json.loads(line)['__CURSOR'])[2], 16) for line in output.splitlines()]
    return {'returned': sum(number <= last for number in numbers),
            'returned_in_range': sum(first <= number <= last for number in numbers)}


def retained_range(files):
    present = [row for row in files if row['entries']]
    system = [row for row in present if row['file'].startswith('system')]
    if not system:
        raise RuntimeError('No retained system journal file holds entries')
    return (min(row['first_sequence'] for row in system), max(row['last_sequence'] for row in present))


def accounting(files, partial, holes):
    # Old files are removed oldest first, so the oldest retained system file starts the range in which every
    # journal file is still present. There, one stored entry per sequence number shows that the numbers
    # journalctl does not return were written. A file that begins before the range contributes the entries
    # it returns inside it; its unreturned entries cannot be placed and widen the accepted count.
    first, last = retained_range(files)
    least = most = 0
    for row in files:
        if not row['entries'] or row['last_sequence'] < first:
            continue
        if row['first_sequence'] >= first:
            least, most = least + row['entries'], most + row['entries']
            continue
        counts = partial[row['file']]
        unplaced = row['entries'] - counts['returned']
        if unplaced < 0:
            raise RuntimeError('Journal file returns more entries than it stores: ' + row['file'])
        least, most = least + counts['returned_in_range'], most + counts['returned_in_range'] + unplaced
    expected = last - first + 1
    inside = sum(max(0, min(end, last) - max(start, first) + 1) for start, end in holes)
    outside = sum(end - start + 1 for start, end in holes) - inside
    return {'first_sequence': first, 'last_sequence': last, 'expected_entries': expected,
            'stored_entries_least': least, 'stored_entries_most': most,
            'unreturned_in_range': inside, 'unreturned_outside_range': outside,
            'passed': least <= expected <= most and not outside}


def account(raw, boot, holes, tail_number):
    if any(VOLATILE_ROOT.glob('*/*.journal')):
        raise RuntimeError('Volatile journal files are outside the sequence accounting')
    files = stable_headers()
    first = retained_range(files)[0]
    partial = {row['file']: returned_entries(next(JOURNAL_ROOT.glob('*/' + row['file'])), first, row['last_sequence'])
               for row in files if row['entries'] and row['first_sequence'] < first <= row['last_sequence']}
    record = {'boot_id': boot, 'files': files, 'partial_files': partial, **accounting(files, partial, holes)}
    (raw / 'journal-sequence-accounting.json').write_text(json.dumps(record, indent=2) + '\n')
    if any(row['boot_id'] != boot for row in files if row['entries']):
        raise RuntimeError('Sequence accounting requires journal files of the current boot only')
    if record['last_sequence'] < tail_number:
        raise RuntimeError('Journal files end before the terminal checkpoint')
    if not record['passed']:
        raise RuntimeError('Stored journal entries do not account for every sequence number in the retained range')
    return {key: value for key, value in record.items() if key not in ('files', 'partial_files')}


def collect(raw, previous, now):
    boot = BOOT.read_text().strip().replace('-', '')
    daemon = daemon_identity()
    version = subprocess.run(['systemctl', '--version'], capture_output=True, text=True, timeout=QUERY_TIMEOUT)
    if version.returncode or not version.stdout.startswith('systemd 239 '):
        raise RuntimeError('Journal sequence coverage requires the approved systemd 239 environment')
    checkpoint = previous.get('system_journal_checkpoint')
    if checkpoint and checkpoint.get('boot_id') != boot:
        raise RuntimeError('Journal checkpoint belongs to another boot')
    if checkpoint and checkpoint.get('daemon') != daemon:
        raise RuntimeError('Journal daemon changed since the previous checkpoint')
    began = now.strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    boundary = checkpoint['through'] if checkpoint else previous.get('kernel_journal_since', began)
    if timestamp(boundary) > timestamp(began):
        raise RuntimeError('Journal collection boundary moved backwards')
    if checkpoint:
        anchor = checkpoint['entry']
    else:
        anchors = query(['--system', '-b', boot, '--reverse', '--lines=1', '--until', boundary],
                        raw / 'system-journal-initial-anchor.jsonl')
        if len(anchors) != 1 or int(anchors[0]['__REALTIME_TIMESTAMP']) > timestamp(boundary):
            raise RuntimeError('System retention begins after the collection boundary')
        anchor = anchors[0]
    marker = uuid.uuid4().hex
    emitted = subprocess.run(['logger', '--tag', MARKER_TAG, '--', marker],
                             capture_output=True, text=True, timeout=QUERY_TIMEOUT)
    (raw / 'journal-marker.json').write_text(json.dumps({'marker': marker,
        'returncode': emitted.returncode, 'stdout': emitted.stdout, 'stderr': emitted.stderr}) + '\n')
    if emitted.returncode:
        raise RuntimeError('System journal checkpoint emission failed')
    synced = subprocess.run(['journalctl', '--sync'], capture_output=True, text=True, timeout=QUERY_TIMEOUT)
    if synced.returncode or synced.stderr.strip():
        raise RuntimeError('System journal checkpoint synchronization failed')
    tails = query(['--system', '-b', boot, 'SYSLOG_IDENTIFIER=' + MARKER_TAG,
                   'MESSAGE=' + marker], raw / 'system-journal-tail.jsonl')
    if len(tails) != 1 or tails[0].get('_UID') != '0':
        raise RuntimeError('System journal has no unique root-owned terminal checkpoint')
    tail = tails[0]
    ended = int(tail['__REALTIME_TIMESTAMP'])
    if ended < timestamp(began):
        raise RuntimeError('System journal checkpoint precedes collection start')
    end = datetime.datetime.fromtimestamp(ended // 1000000, datetime.timezone.utc).replace(
        microsecond=ended % 1000000).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    rows = query(['-b', boot, '--cursor', anchor['__CURSOR'], '--until', end],
                 raw / 'journal-sequence.jsonl')
    interval = validate_interval(rows, anchor, tail, boot)
    holes = sequence_holes(interval, boot)
    accounted = account(raw, boot, holes, coordinates(tail, boot)[1])
    if BOOT.read_text().strip().replace('-', '') != boot or daemon_identity() != daemon:
        raise RuntimeError('Boot or journal daemon changed while collecting the interval')
    required = [row for row in interval if timestamp(boundary) <= int(row['__REALTIME_TIMESTAMP'])
                <= timestamp(end)]
    if checkpoint:
        required = [row for row in required if row['__CURSOR'] != anchor['__CURSOR']]
    kernel = [row for row in required if row.get('_TRANSPORT') == 'kernel']
    (raw / 'kernel-journal.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in kernel))
    if any(any(term in str(row.get('MESSAGE', '')).lower() for term in ('suppressed', 'missed'))
           for row in required):
        raise RuntimeError('Journal records were suppressed or missed')
    proof = {'boot_id': boot, 'daemon': daemon, 'since': boundary, 'through': end,
             'sequence_id': coordinates(anchor, boot)[0],
             'first_sequence': coordinates(anchor, boot)[1],
             'last_sequence': coordinates(tail, boot)[1],
             'sequence_records': len(interval), 'required_records': len(required),
             'sequence_holes': holes, 'sequence_missing': sum(last - first + 1 for first, last in holes),
             'sequence_accounting': accounted,
             'stream_sequence_ids': sorted({coordinates(row, boot)[0] for row in interval}),
             'system_anchor': anchor['__CURSOR'], 'system_tail': tail['__CURSOR'],
             'source_sha256': hashlib.sha256((raw / 'journal-sequence.jsonl').read_bytes()).hexdigest(),
             'coverage_complete': True}
    (raw / 'journal-coverage.json').write_text(json.dumps(proof, indent=2) + '\n')
    return {**proof, 'cursor': kernel[-1]['__CURSOR'] if kernel else None,
            'memory_events': sum(any(term in str(row.get('MESSAGE', '')).lower()
                                     for term in ('out of memory', 'oom-kill', 'killed process'))
                                 for row in kernel),
            'checkpoint': {'boot_id': boot, 'daemon': daemon, 'entry': tail, 'through': end}}
