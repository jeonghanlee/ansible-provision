"""Exercise an actual unavailable pre-window checkpoint without removing required records."""

import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import threading
import time
import uuid

import basic
import journal_coverage
import prepare
import window_coverage

SETUP_TAG = 'JOURNAL_VALIDATION_SETUP'
HARDWARE_UUID = Path('/sys/class/dmi/id/product_uuid')
POLL_SECONDS = 0.05


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def read_query(path):
    receipt = json.loads(path.with_suffix(path.suffix + '.receipt.json').read_text())
    if (receipt.get('returncode') != 0 or receipt.get('stderr', '').strip() or receipt.get('error')
            or digest(path) != receipt['stdout_sha256']):
        raise RuntimeError('An obsolete-anchor query is unsuccessful or changed')
    return basic.load_rows(path)


def closed_file(candidate, destination):
    """Require a stable rotated file absent from journald descriptors and mappings."""
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    deadline = time.monotonic() + basic.VISIBILITY_WAIT
    attempts = []
    while True:
        began = basic.clock()
        daemon = journal_coverage.daemon_identity()
        metadata = candidate.stat()
        before = journal_coverage.read_header(candidate)
        process = Path('/proc') / daemon['pid']
        descriptors, mappings = [], []
        try:
            for descriptor in (process / 'fd').iterdir():
                value = descriptor.stat()
                if (value.st_dev, value.st_ino) == (metadata.st_dev, metadata.st_ino):
                    descriptors.append(descriptor.name)
            for line in (process / 'maps').read_text().splitlines():
                fields = line.split(None, 5)
                major, minor = (int(value, 16) for value in fields[3].split(':'))
                if (major, minor, int(fields[4])) == (os.major(metadata.st_dev), os.minor(metadata.st_dev), metadata.st_ino):
                    mappings.append(fields[:5])
            after = journal_coverage.read_header(candidate)
            stable = before == after and journal_coverage.daemon_identity() == daemon
        except FileNotFoundError:
            stable = False
            after = None
        attempt = {'started': began, 'finished': basic.clock(), 'daemon': daemon,
                   'candidate_inode': metadata.st_ino, 'candidate_device': metadata.st_dev,
                   'header_before': before, 'header_after': after, 'stable': stable,
                   'descriptor_matches': descriptors, 'mapping_matches': mappings}
        attempts.append(attempt)
        if stable and before['state'] in (0, 2) and not descriptors and not mappings:
            prepare.save(destination / 'closed-file-proof.json', {'attempts': attempts, 'closed': True})
            return attempt
        if time.monotonic() >= deadline:
            prepare.save(destination / 'closed-file-proof.json', {'attempts': attempts, 'closed': False})
            raise RuntimeError('The rotated checkpoint file is still active or unstable')
        time.sleep(POLL_SECONDS)


def prewindow(directory):
    destination = directory / 'obsolete-anchor'
    destination.mkdir(mode=0o700)
    native = destination / 'prewindow-native'
    native.mkdir(mode=0o700)
    began = basic.clock()
    since = datetime.datetime.fromisoformat(began['utc']).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    result = journal_coverage.collect(native, {'kernel_journal_since': since},
                                     datetime.datetime.now(datetime.timezone.utc))
    prepare.save(native / 'result.json', {'started': began, 'finished': basic.clock(), **result})
    checkpoint = result['checkpoint']
    boot = checkpoint['boot_id']
    stream, sequence = journal_coverage.coordinates(checkpoint['entry'], boot)
    before = journal_coverage.file_headers()
    prepare.save(destination / 'files-before-rotation.json', before)
    rotate = basic.command(['journalctl', '--rotate'], destination / 'prewindow-rotate')
    if rotate.get('returncode') != 0 or rotate.get('error'):
        raise RuntimeError('The actual pre-window rotation failed')
    candidates = [row for row in journal_coverage.file_headers()
                  if row['file'].startswith('system@') and row['entries']
                  and row['sequence_id'] == stream and row['first_sequence'] <= sequence <= row['last_sequence']]
    matched = []
    for number, header in enumerate(candidates):
        path = next(journal_coverage.JOURNAL_ROOT.glob('*/' + header['file']))
        records = journal_coverage.query(['--file', str(path), '--cursor', checkpoint['entry']['__CURSOR'], '--lines=1'],
                                         destination / ('candidate-probe-' + str(number) + '.jsonl'))
        if records == [checkpoint['entry']]:
            matched.append((path, header))
    if len(matched) != 1:
        raise RuntimeError('A unique closed file containing the real old checkpoint was not established')
    candidate, header = matched[0]
    if candidate.is_symlink() or candidate.resolve().parent.parent != journal_coverage.JOURNAL_ROOT.resolve():
        raise RuntimeError('The old checkpoint file is outside the dedicated live journal root')
    status = basic.command(['journalctl', '--no-pager', '--file', str(candidate), '--header'], destination / 'candidate-header')
    if status.get('returncode') != 0 or not re.search(r'^\s*State:\s+(OFFLINE|ARCHIVED)\s*$',
                                                   (destination / 'candidate-header.stdout').read_text(), re.MULTILINE):
        raise RuntimeError('The actual checkpoint file is not confirmed offline or archived')
    closed = closed_file(candidate, destination)
    header = closed['header_after']
    prior = [row for row in before if row['file_id'] == header['file_id']]
    after = journal_coverage.file_headers()
    active = [row for row in after if row['file'] == 'system.journal']
    if (len(prior) != 1 or prior[0]['file'] != 'system.journal' or len(active) != 1
            or active[0]['file_id'] == header['file_id']):
        raise RuntimeError('The old checkpoint file was not replaced by a new active journal file')
    prepare.save(destination / 'files-after-rotation.json', after)
    saved = destination / 'preserved.journal'
    original_hash = digest(candidate)
    shutil.copy2(candidate, saved)
    saved.chmod(0o600)
    with saved.open('rb+') as source:
        os.fsync(source.fileno())
    if digest(saved) != original_hash or digest(candidate) != original_hash:
        raise RuntimeError('The real closed-file copy is not byte-identical')
    journal_coverage.query(['--file', str(candidate)], destination / 'candidate-records.jsonl')
    token = uuid.uuid4().hex
    emitted = basic.command(['logger', '--tag', SETUP_TAG, '--', token], destination / 'new-window-anchor-emission')
    if emitted.get('returncode') != 0:
        raise RuntimeError('The real new-window setup anchor could not be emitted')
    deadline = time.monotonic() + basic.VISIBILITY_WAIT
    attempt = 0
    while True:
        records = journal_coverage.query(['--system', '-b', boot, 'SYSLOG_IDENTIFIER=' + SETUP_TAG,
                                         '_UID=0', 'MESSAGE=' + token],
                                        destination / ('new-window-anchor-' + str(attempt) + '.jsonl'))
        if len(records) == 1:
            anchor = records[0]
            break
        if time.monotonic() >= deadline:
            raise RuntimeError('The actual new-window setup anchor was not directly confirmed')
        time.sleep(basic.QUERY_PERIOD)
        attempt += 1
    anchor_stream, anchor_sequence = journal_coverage.coordinates(anchor, boot)
    if anchor_stream != stream or anchor_sequence <= header['last_sequence']:
        raise RuntimeError('The new required window does not follow the closed old file')
    metadata = candidate.stat()
    prepared = {'observed': basic.clock(), 'boot_id': boot, 'daemon': journal_coverage.daemon_identity(),
                'hardware_uuid': HARDWARE_UUID.read_text().strip().lower(), 'checkpoint': checkpoint,
                'candidate': str(candidate), 'header': header, 'candidate_sha256': original_hash,
                'candidate_inode': metadata.st_ino, 'candidate_device': metadata.st_dev,
                'copy_sha256': digest(saved), 'new_window_anchor': anchor,
                'files_before_rotation': before, 'files_after_rotation': after,
                'closed_file_proof_sha256': digest(destination / 'closed-file-proof.json'),
                'prewindow_rotation': rotate}
    prepare.save(destination / 'preparation.json', prepared)
    return prepared


class Collector:
    """Pass the actual pre-window checkpoint unchanged into every native interval."""

    def __init__(self, directory, checkpoint, required_anchor):
        self.directory, self.checkpoint, self.required_anchor = directory, checkpoint, required_anchor
        self.stopping = threading.Event()
        self.error = None

    def run(self):
        previous = {'system_journal_checkpoint': self.checkpoint}
        number = 0
        try:
            while True:
                terminal = self.stopping.wait(basic.COLLECTION_PERIOD)
                path = self.directory / ('interval-' + str(number))
                path.mkdir(mode=0o700)
                prepare.save(path / 'input-state.json', previous)
                started = basic.clock()
                result = window_coverage.collect(path, previous, datetime.datetime.now(datetime.timezone.utc),
                                                 self.required_anchor)
                prepare.save(path / 'result.json', {'started': started, 'finished': basic.clock(), **result})
                previous = {'system_journal_checkpoint': result['checkpoint']}
                number += 1
                if terminal:
                    return
        except Exception as exception:
            self.error = str(exception)
            prepare.save(self.directory / 'error.json', {'observed': basic.clock(), 'error': self.error})


class Remove:
    """Remove only the hashed closed pre-window file after independent baseline proof."""

    def __init__(self, directory, prepared, start, window, stopping):
        self.directory, self.prepared, self.start, self.window = directory, prepared, start, window
        self.stopping = stopping
        self.error = None

    def run(self):
        destination = self.directory / 'obsolete-anchor'
        try:
            first = self.start['monotonic_ns'] + self.window[0] * 1000000000
            last = self.start['monotonic_ns'] + self.window[1] * 1000000000
            while time.monotonic_ns() < first:
                if self.stopping.wait(POLL_SECONDS):
                    raise RuntimeError('The obsolete-anchor action was interrupted before removal')
            if time.monotonic_ns() >= last:
                raise RuntimeError('The obsolete-anchor removal missed its declared window')
            baseline = json.loads((self.directory / 'baseline.json').read_text())
            rows = read_query(destination / 'candidate-records.jsonl')
            stored = {(row['_BOOT_ID'], row['__CURSOR']) for row in rows}
            required = {(item['record']['_BOOT_ID'], item['record']['__CURSOR'])
                        for action in baseline['actions'] for item in action['records']}
            if stored & required:
                raise basic.ConfirmedViolation('The proposed old file contains a required baseline record')
            initial = read_query(self.directory / 'initial-anchor.jsonl')
            if len(initial) != 1:
                raise RuntimeError('The independent required-window anchor is unavailable')
            stream, number = journal_coverage.coordinates(initial[0], self.prepared['boot_id'])
            if stream != self.prepared['header']['sequence_id'] or number <= self.prepared['header']['last_sequence']:
                raise RuntimeError('The current live reader does not start after the closed old file')
            candidate = Path(self.prepared['candidate'])
            resolved = candidate.resolve(strict=True)
            current = candidate.stat()
            if (candidate.is_symlink() or resolved.parent.parent != journal_coverage.JOURNAL_ROOT.resolve()
                    or current.st_ino != self.prepared['candidate_inode'] or current.st_dev != self.prepared['candidate_device']
                    or digest(candidate) != self.prepared['candidate_sha256']
                    or digest(destination / 'preserved.journal') != self.prepared['copy_sha256']):
                raise RuntimeError('The exact closed-file removal target changed')
            if (HARDWARE_UUID.read_text().strip().lower() != self.prepared['hardware_uuid']
                    or journal_coverage.BOOT.read_text().strip().replace('-', '') != self.prepared['boot_id']
                    or journal_coverage.daemon_identity() != self.prepared['daemon']):
                raise RuntimeError('The dedicated host or journal identity changed before removal')
            if list((self.directory / 'collector').glob('interval-*')):
                raise RuntimeError('The old file removal did not precede the next native interval')
            closed_file(candidate, destination / 'before-removal')
            if digest(candidate) != self.prepared['candidate_sha256']:
                raise RuntimeError('The closed checkpoint file changed immediately before removal')
            plan = {'observed': basic.clock(), 'resolved_target': str(resolved), 'required_baseline_records_in_file': 0,
                    'candidate_sha256': self.prepared['candidate_sha256'], 'copy_sha256': self.prepared['copy_sha256'],
                    'retained_initial_checkpoint': self.prepared['checkpoint']}
            prepare.save(destination / 'removal-plan.json', plan)
            if time.monotonic_ns() >= last:
                raise RuntimeError('The closed-file checks exceeded the declared removal window')
            started = basic.clock()
            candidate.unlink()
            finished = basic.clock()
            checkpoint = self.prepared['checkpoint']['entry']
            remaining = journal_coverage.query(['--system', '-b', self.prepared['boot_id'],
                                                'SYSLOG_IDENTIFIER=' + journal_coverage.MARKER_TAG,
                                                '_UID=0', 'MESSAGE=' + checkpoint['MESSAGE']],
                                               destination / 'old-anchor-after-removal.jsonl')
            if remaining:
                raise RuntimeError('The original pre-window checkpoint remains available after removal')
            prepare.save(destination / 'action.json', {'started': started, 'finished': finished,
                         'target_absent': not candidate.exists(), 'old_anchor_matches_after_removal': len(remaining),
                         'window_seconds': self.window, 'original_checkpoint_retained': self.prepared['checkpoint']})
        except Exception as exception:
            self.error = str(exception)
            prepare.save(destination / 'error.json', {'observed': basic.clock(), 'error': self.error})


def verify_metadata(directory, contract):
    destination = directory / 'obsolete-anchor'
    prepared = json.loads((destination / 'preparation.json').read_text())
    if digest(destination / 'preparation.json') != contract['obsolete_anchor_preparation_sha256']:
        raise RuntimeError('The frozen pre-window preparation changed')
    if digest(destination / 'preserved.journal') != prepared['copy_sha256']:
        raise RuntimeError('The real pre-window journal-file copy changed')
    if digest(destination / 'closed-file-proof.json') != prepared['closed_file_proof_sha256']:
        raise RuntimeError('The actual closed-file proof changed')
    closed = json.loads((destination / 'closed-file-proof.json').read_text())
    final = closed['attempts'][-1]
    if (not closed['closed'] or not final['stable'] or final['descriptor_matches'] or final['mapping_matches']
            or final['header_before'] != final['header_after'] or final['header_after'] != prepared['header']
            or final['header_after']['state'] not in (0, 2)
            or final['candidate_inode'] != prepared['candidate_inode']
            or final['candidate_device'] != prepared['candidate_device']):
        raise RuntimeError('The checkpoint file was not proven closed before copying')
    before = [row for row in prepared['files_before_rotation'] if row['file_id'] == prepared['header']['file_id']]
    after = [row for row in prepared['files_after_rotation'] if row['file'] == 'system.journal']
    if len(before) != 1 or before[0]['file'] != 'system.journal' or len(after) != 1 or after[0]['file_id'] == before[0]['file_id']:
        raise RuntimeError('Actual file identities do not prove replacement of the old active file')
    removal_closed = json.loads((destination / 'before-removal/closed-file-proof.json').read_text())
    removal_proof = removal_closed['attempts'][-1]
    if (not removal_closed['closed'] or not removal_proof['stable']
            or removal_proof['descriptor_matches'] or removal_proof['mapping_matches']
            or removal_proof['header_before'] != prepared['header']
            or removal_proof['header_after'] != prepared['header']
            or removal_proof['daemon'] != prepared['daemon']
            or removal_proof['candidate_inode'] != prepared['candidate_inode']
            or removal_proof['candidate_device'] != prepared['candidate_device']):
        raise RuntimeError('The exact original checkpoint file was not closed immediately before removal')
    native = json.loads((destination / 'prewindow-native/result.json').read_text())
    if (native['checkpoint'] != prepared['checkpoint'] or not native['coverage_complete']
            or digest(destination / 'prewindow-native/journal-sequence.jsonl') != native['source_sha256']):
        raise RuntimeError('The pre-window state does not match its actual successful native collection')
    candidate = read_query(destination / 'candidate-records.jsonl')
    if prepared['checkpoint']['entry'] not in candidate:
        raise RuntimeError('The preserved actual old file lacks its declared checkpoint')
    action = json.loads((destination / 'action.json').read_text())
    if (action['window_seconds'] != contract['obsolete_anchor_removal_window_seconds']
            or action['original_checkpoint_retained'] != prepared['checkpoint'] or not action['target_absent']
            or action['old_anchor_matches_after_removal'] != 0 or read_query(destination / 'old-anchor-after-removal.jsonl')):
        raise RuntimeError('The actual obsolete-anchor action differs from its declared expectation')
    begin, end = contract['obsolete_anchor_removal_window_seconds']
    t0 = contract['start']['monotonic_ns']
    if not t0 + begin * 1000000000 <= action['started']['monotonic_ns'] <= action['finished']['monotonic_ns'] <= t0 + end * 1000000000:
        raise RuntimeError('The old file was not removed within its declared pre-collection window')
    previous = json.loads((directory / 'collector/interval-0/input-state.json').read_text())
    if previous != {'system_journal_checkpoint': prepared['checkpoint']}:
        raise RuntimeError('The original actual collector checkpoint was reset or changed')
    config = json.loads((directory / 'package/config.json').read_text())
    direct, first = basic.direct_records(directory / 'direct')
    index = basic.source_index(direct, config)
    final = {(row['_BOOT_ID'], row['__CURSOR']): row for row in read_query(directory / 'final-live.jsonl')}
    stored = {(row['_BOOT_ID'], row['__CURSOR']) for row in candidate}
    outcomes = {}
    for name in ('baseline-outcomes.jsonl', 'outcomes.jsonl'):
        for outcome in basic.load_rows(directory / name):
            if outcome['id'] in outcomes:
                raise basic.ConfirmedViolation('An obsolete-anchor producer outcome identity repeats')
            outcomes[outcome['id']] = outcome
    seen, required = set(), set()
    window_stream, window_number = journal_coverage.coordinates(prepared['new_window_anchor'], prepared['boot_id'])
    for name in ('baseline-schedule.jsonl', 'schedule.jsonl'):
        for source in basic.load_rows(directory / name):
            if source['id'] in seen:
                raise basic.ConfirmedViolation('An obsolete-anchor producer schedule identity repeats')
            seen.add(source['id'])
            outcome = outcomes.get(source['id'])
            if outcome is None:
                raise RuntimeError('The obsolete-anchor producer schedule is incomplete')
            if not outcome.get('executed') and not (source['path'] == 'appliance' and outcome.get('attempted')):
                raise basic.ConfirmedViolation('A required obsolete-anchor producer action was not executed')
            matched = basic.required_records(source, outcome, index, config)
            if len(matched) != (2 if source['path'] in ('appliance', 'health') else 1):
                raise RuntimeError('An obsolete-anchor required source set is missing or ambiguous')
            for row in matched:
                stream, number = journal_coverage.coordinates(row, prepared['boot_id'])
                if stream != window_stream or number <= window_number:
                    raise basic.ConfirmedViolation('A required record precedes the declared collector window')
                identity = (row['_BOOT_ID'], row['__CURSOR'])
                if identity in required:
                    raise basic.ConfirmedViolation('Obsolete-anchor actions claim the same required source identity')
                required.add(identity)
                if identity in stored or final.get(identity) != row:
                    raise basic.ConfirmedViolation('A current required record was removed or changed in the obsolete-anchor case')
    if set(outcomes) != seen:
        raise basic.ConfirmedViolation('Obsolete-anchor outcomes include an unscheduled action')
    return {'scope': 'obsolete-anchor-lifecycle-and-live-records-only', 'required_records_in_removed_file': 0,
            'all_required_records_directly_confirmed_and_still_live': True,
            'original_native_checkpoint_retained': True, 'real_closed_file_copy_preserved': True,
            'actual_required_record_count': len(required), 'complete_archive_acceptance_established': False}
