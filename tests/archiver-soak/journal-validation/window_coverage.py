"""Collect a declared required window while retaining its original checkpoint input."""

import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import uuid

import journal_coverage as native


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def load_query(path):
    receipt = json.loads(path.with_suffix(path.suffix + '.receipt.json').read_text())
    if receipt['returncode'] != 0 or receipt['stderr'].strip() or digest(path) != receipt['stdout_sha256']:
        raise RuntimeError('The required-window query failed or changed')
    return [json.loads(line) for line in path.read_text().splitlines()]


def accounting(raw, record):
    """Account actual stored sequence identities only within the declared interval."""
    first, last, stream, boot = (record[key] for key in ('first_sequence', 'last_sequence', 'sequence_id', 'boot_id'))
    numbers = set()
    file_counts = []
    for item in record['files']:
        header = item['header']
        entries = load_query(raw / item['query'])
        stored = set()
        for entry in entries:
            entry_stream, number = native.coordinates(entry, entry['_BOOT_ID'])
            if entry_stream != header['sequence_id']:
                raise RuntimeError('A real file enumeration has a different sequence stream')
            if number > header['last_sequence']:
                continue
            if number < header['first_sequence'] or number in stored:
                raise RuntimeError('A real file enumeration repeats or precedes its stored header range')
            stored.add(number)
            if first <= number <= last:
                if entry['_BOOT_ID'] != boot or number in numbers:
                    raise RuntimeError('The required sequence range has mixed or repeated identities')
                numbers.add(number)
        if len(stored) != header['entries']:
            raise RuntimeError('The actual file enumeration does not account for its stored entries')
        file_counts.append({'file_id': header['file_id'], 'stored_entries': len(stored),
                            'required_range_entries': sum(first <= number <= last for number in stored)})
    expected = last - first + 1
    passed = bool(numbers) and min(numbers) == first and max(numbers) == last and len(numbers) == expected
    return {'first_sequence': first, 'last_sequence': last, 'expected_entries': expected,
            'stored_sequence_count': len(numbers), 'files': file_counts, 'passed': passed}


def account(raw, boot, stream, first, last):
    if any(native.VOLATILE_ROOT.glob('*/*.journal')):
        raise RuntimeError('Volatile journal files are outside the required-window accounting')
    files = native.stable_headers()
    selected = [row for row in files if row['entries']
                and row['first_sequence'] <= last and row['last_sequence'] >= first]
    record = {'boot_id': boot, 'sequence_id': stream, 'first_sequence': first,
              'last_sequence': last, 'observed_headers': files, 'files': []}
    for number, header in enumerate(selected):
        path = next(native.JOURNAL_ROOT.glob('*/' + header['file']))
        destination = raw / ('window-file-' + str(number) + '.jsonl')
        native.query(['--file', str(path), '--output-fields=_BOOT_ID'], destination)
        record['files'].append({'header': header, 'query': destination.name})
    result = accounting(raw, record)
    save(raw / 'journal-window-accounting.json', {**record, 'result': result})
    if not result['passed']:
        raise RuntimeError('Actual stored identities do not cover the required sequence window')
    return result


def collect(raw, previous, now, required_anchor):
    """Preserve previous state and exclude only a proved strictly earlier missing anchor."""
    boot = native.BOOT.read_text().strip().replace('-', '')
    daemon = native.daemon_identity()
    version = subprocess.run(['systemctl', '--version'], capture_output=True, text=True, timeout=native.QUERY_TIMEOUT)
    if version.returncode or not version.stdout.startswith('systemd 239 '):
        raise RuntimeError('Required-window coverage requires the approved systemd 239 environment')
    checkpoint = previous['system_journal_checkpoint']
    if checkpoint['boot_id'] != boot:
        raise RuntimeError('Journal checkpoint belongs to another boot')
    if checkpoint['daemon'] != daemon:
        raise RuntimeError('Journal daemon changed since the previous checkpoint')
    stream, minimum = native.coordinates(required_anchor, boot)
    anchor_stream, anchor_number = native.coordinates(checkpoint['entry'], boot)
    if anchor_stream != stream:
        raise RuntimeError('The required window and previous checkpoint have different streams')
    window_time = int(required_anchor['__REALTIME_TIMESTAMP'])
    if required_anchor.get('_UID') != '0':
        raise RuntimeError('The declared required-window boundary is not root-owned')
    save(raw / 'original-input-state.json', previous)
    save(raw / 'required-window.json', {'entry': required_anchor})
    visible = native.query(['--system', '-b', boot, '--cursor', required_anchor['__CURSOR'], '--lines=1'],
                           raw / 'required-window-anchor.jsonl')
    if visible != [required_anchor]:
        raise RuntimeError('The declared required-window boundary is not directly readable')
    began = now.strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    if native.timestamp(checkpoint['through']) > native.timestamp(began):
        raise RuntimeError('Journal collection boundary moved backwards')
    excluded = anchor_number < minimum
    if excluded:
        if (native.timestamp(checkpoint['through']) > window_time
                or int(checkpoint['entry']['__REALTIME_TIMESTAMP']) > window_time):
            raise RuntimeError('The excluded previous checkpoint is not strictly before the required window')
        old = native.query(['--system', '-b', boot, '--cursor', checkpoint['entry']['__CURSOR'], '--lines=1'],
                           raw / 'previous-anchor-availability.jsonl')
        anchor = required_anchor
        boundary = datetime.datetime.fromtimestamp(window_time // 1000000, datetime.timezone.utc).replace(
            microsecond=window_time % 1000000).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    else:
        old = None
        anchor = checkpoint['entry']
        boundary = checkpoint['through']
    marker = uuid.uuid4().hex
    emitted = subprocess.run(['logger', '--tag', native.MARKER_TAG, '--', marker],
                             capture_output=True, text=True, timeout=native.QUERY_TIMEOUT)
    save(raw / 'journal-marker.json', {'marker': marker, 'returncode': emitted.returncode,
                                     'stdout': emitted.stdout, 'stderr': emitted.stderr})
    if emitted.returncode:
        raise RuntimeError('System journal checkpoint emission failed')
    tail, attempts = native.terminal_checkpoint(raw, boot, marker)
    ended = int(tail['__REALTIME_TIMESTAMP'])
    if ended < native.timestamp(began):
        raise RuntimeError('System journal checkpoint precedes collection start')
    end = datetime.datetime.fromtimestamp(ended // 1000000, datetime.timezone.utc).replace(
        microsecond=ended % 1000000).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    rows = native.query(['-b', boot, '--cursor', anchor['__CURSOR'], '--until', end],
                        raw / 'journal-sequence.jsonl')
    interval = native.validate_interval(rows, anchor, tail, boot)
    first_number = native.coordinates(anchor, boot)[1]
    last_number = native.coordinates(tail, boot)[1]
    accounted = account(raw, boot, stream, first_number, last_number)
    if native.BOOT.read_text().strip().replace('-', '') != boot or native.daemon_identity() != daemon:
        raise RuntimeError('Boot or journal daemon changed while collecting the required window')
    required = [row for row in interval if native.timestamp(boundary) <= int(row['__REALTIME_TIMESTAMP']) <= ended]
    if not excluded:
        required = [row for row in required if row['__CURSOR'] != anchor['__CURSOR']]
    kernel = [row for row in required if row.get('_TRANSPORT') == 'kernel']
    (raw / 'kernel-journal.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in kernel))
    if any(any(term in str(row.get('MESSAGE', '')).lower() for term in ('suppressed', 'missed')) for row in required):
        raise RuntimeError('Journal records were suppressed or missed')
    holes = native.sequence_holes(interval, boot)
    proof = {'boot_id': boot, 'daemon': daemon, 'since': boundary, 'through': end,
             'sequence_id': stream, 'first_sequence': first_number, 'last_sequence': last_number,
             'sequence_records': len(interval), 'required_records': len(required),
             'checkpoint_attempts': attempts, 'sequence_holes': holes,
             'sequence_missing': sum(last - first + 1 for first, last in holes),
             'sequence_accounting': accounted, 'system_anchor': anchor['__CURSOR'], 'system_tail': tail['__CURSOR'],
             'stream_sequence_ids': sorted({native.coordinates(row, boot)[0] for row in interval}),
             'source_sha256': digest(raw / 'journal-sequence.jsonl'), 'coverage_complete': True,
             'required_window_entry': required_anchor, 'original_input_checkpoint': checkpoint,
             'pre_window_checkpoint_excluded': excluded,
             'pre_window_checkpoint_available': old == [checkpoint['entry']] if old is not None else None,
             'accounting_kind': 'actual-required-window-sequence-identities'}
    save(raw / 'journal-coverage.json', proof)
    return {**proof, 'cursor': kernel[-1]['__CURSOR'] if kernel else None,
            'memory_events': sum(any(term in str(row.get('MESSAGE', '')).lower()
                                     for term in ('out of memory', 'oom-kill', 'killed process')) for row in kernel),
            'checkpoint': {'boot_id': boot, 'daemon': daemon, 'entry': tail, 'through': end}}


def verify(raw, proof):
    original = json.loads((raw / 'original-input-state.json').read_text())
    window = json.loads((raw / 'required-window.json').read_text())['entry']
    if original['system_journal_checkpoint'] != proof['original_input_checkpoint'] or window != proof['required_window_entry']:
        raise RuntimeError('The real required-window input state changed')
    if load_query(raw / 'required-window-anchor.jsonl') != [window]:
        raise RuntimeError('The required-window boundary lacks its actual direct confirmation')
    boot = proof['boot_id']
    stream, minimum = native.coordinates(window, boot)
    checkpoint = proof['original_input_checkpoint']
    if checkpoint['boot_id'] != boot or checkpoint['daemon'] != proof['daemon']:
        raise RuntimeError('The original required-window checkpoint has a different boot or daemon')
    old_stream, number = native.coordinates(checkpoint['entry'], boot)
    excluded = number < minimum
    if old_stream != stream or proof['pre_window_checkpoint_excluded'] != excluded:
        raise RuntimeError('The checkpoint exclusion differs from its actual sequence positions')
    anchor = window if excluded else checkpoint['entry']
    if excluded:
        if (native.timestamp(checkpoint['through']) > int(window['__REALTIME_TIMESTAMP'])
                or int(checkpoint['entry']['__REALTIME_TIMESTAMP']) > int(window['__REALTIME_TIMESTAMP'])):
            raise RuntimeError('The excluded checkpoint reaches the required window')
        old = load_query(raw / 'previous-anchor-availability.jsonl')
        if proof['pre_window_checkpoint_available'] != (old == [checkpoint['entry']]):
            raise RuntimeError('The original checkpoint availability differs from its real query')
    records = load_query(raw / 'journal-sequence.jsonl')
    tail = load_query(raw / 'system-journal-tail.jsonl')
    if len(tail) != 1:
        raise RuntimeError('The required-window terminal checkpoint is ambiguous')
    native.validate_interval(records, anchor, tail[0], boot)
    stored = json.loads((raw / 'journal-window-accounting.json').read_text())
    recomputed = accounting(raw, stored)
    if (not recomputed['passed'] or stored['result'] != recomputed or proof['sequence_accounting'] != recomputed
            or stored['first_sequence'] != native.coordinates(anchor, boot)[1]
            or stored['last_sequence'] != native.coordinates(tail[0], boot)[1]
            or stored['boot_id'] != boot or stored['sequence_id'] != stream):
        raise RuntimeError('The real stored sequence identities do not reproduce required-window coverage')
    return True
