#!/usr/bin/env python3
"""Archive bounded journal intervals with system-only checkpoints and sequence evidence."""

import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import uuid

BOOT = Path('/proc/sys/kernel/random/boot_id')
QUERY_TIMEOUT = 60
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
    if (selected.get(first) != anchor or selected.get(last) != tail or
            len(selected) != last - first + 1):
        raise RuntimeError('Required journal interval is missing records or its system checkpoint')
    ordered = [selected[number] for number in sorted(selected)]
    times = [int(row['__REALTIME_TIMESTAMP']) for row in ordered]
    if times != sorted(times):
        raise RuntimeError('Journal realtime moved backwards within the required interval')
    return ordered


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
