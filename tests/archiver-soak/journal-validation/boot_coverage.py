"""Collect declared live segments with explicit, independently evidenced boot transitions."""

import datetime
import json
from pathlib import Path
import subprocess
import threading
import time
import uuid

import basic
import journal_coverage as native
import prepare
import window_coverage as window

SETUP_TAG = 'JOURNAL_VALIDATION_SETUP'


def load(path):
    return json.loads(path.read_text())


def setup(directory, context):
    destination = directory / 'restart-window'
    destination.mkdir(mode=0o700)
    boot = native.BOOT.read_text().strip().replace('-', '')
    token = uuid.uuid4().hex
    emitted = basic.command(['logger', '--tag', SETUP_TAG, '--', token], destination / 'emission')
    if emitted.get('returncode') != 0:
        raise RuntimeError('The actual restart window boundary could not be emitted')
    deadline, number = time.monotonic() + basic.VISIBILITY_WAIT, 0
    while True:
        synced = basic.command(['journalctl', '--sync'], destination / ('sync-' + str(number)))
        if synced.get('returncode') != 0:
            raise RuntimeError('The actual restart window synchronization failed')
        query = 'anchor-' + str(number) + '.jsonl'
        rows = native.query(['--system', '-b', boot, 'SYSLOG_IDENTIFIER=' + SETUP_TAG,
                             '_UID=0', 'MESSAGE=' + token], destination / query)
        if len(rows) == 1:
            break
        if len(rows) > 1 or time.monotonic() >= deadline:
            raise RuntimeError('The actual restart window boundary is not uniquely readable')
        time.sleep(basic.QUERY_PERIOD)
        number += 1
    native.coordinates(rows[0], boot)
    result = {'entry': rows[0], 'query': query, 'observed': basic.clock(), 'daemon': native.daemon_identity(),
              'context_sha256': window.digest(directory / 'restart-input.json')}
    prepare.save(directory / 'restart-window.json', result)
    return rows[0]


def transition(context, checkpoint, boot):
    master = Path(context['master'])
    if master.parent != prepare.EVIDENCE or not master.name.startswith('restart-'):
        raise RuntimeError('The boot transition is outside its declared parent evidence')
    contract, before = load(master / 'contract.json'), load(master / 'before.json')
    requested, external = load(master / 'reboot-request.json'), load(master / 'external-boot-observation.json')
    if (window.digest(master / 'contract.json') != context['master_contract_sha256']
            or contract['pre_boot_id'] != checkpoint['boot_id'] or checkpoint['boot_id'] == boot
            or before['retained_checkpoint'] != checkpoint or contract['generation_during_reboot'] != 'paused'
            or requested['command_receipt'].get('returncode') != 0
            or requested['completed_before_service'] != {'MainPID': '0', 'Result': 'success'}
            or external['clock_domain'] != 'control-host' or external['old_boot_id'] != checkpoint['boot_id']
            or external['new_boot_id'] != boot or not external['probes']):
        raise RuntimeError('The old checkpoint lacks its actual declared normal reboot evidence')
    first = Path(contract['segments']['before'])
    if first.parent != prepare.EVIDENCE or load(first / 'result.json')['overall'] != 'Passed':
        raise RuntimeError('The pre-reboot live segment lacks complete native acceptance')
    if window.digest(first / 'result.json') != before['segment_result_sha256']:
        raise RuntimeError('The retained pre-reboot segment result changed')
    boundary = master / 'pre-reboot-boundary'
    confirmed = load(boundary / 'confirmation.json')
    old = boundary / 'native'
    proof = load(old / 'journal-coverage.json')
    if (window.digest(boundary / 'confirmation.json') != before['boundary_confirmation_sha256']
            or window.digest(old / 'result.json') != confirmed['native_result_sha256']
            or confirmed['checkpoint'] != checkpoint or proof['boot_id'] != checkpoint['boot_id']
            or proof['system_tail'] != checkpoint['entry']['__CURSOR'] or not proof['coverage_complete']):
        raise RuntimeError('The old checkpoint is not the actual complete pre-reboot native tail')
    verify(old, proof)
    return {'old_boot_id': checkpoint['boot_id'], 'new_boot_id': boot,
            'hardware_uuid': contract['hardware_uuid'], 'master_contract_sha256': window.digest(master / 'contract.json'),
            'before_result_sha256': window.digest(first / 'result.json'),
            'old_native_proof_sha256': window.digest(old / 'journal-coverage.json'),
            'reboot_request_sha256': window.digest(master / 'reboot-request.json'),
            'external_observation_sha256': window.digest(master / 'external-boot-observation.json'),
            'generation_during_reboot': 'paused'}


def collect(raw, previous, now, required_anchor, context):
    boot = native.BOOT.read_text().strip().replace('-', '')
    daemon = native.daemon_identity()
    version = subprocess.run(['systemctl', '--version'], capture_output=True, text=True, timeout=native.QUERY_TIMEOUT)
    if version.returncode or not version.stdout.startswith('systemd 239 '):
        raise RuntimeError('Boot coverage requires the approved systemd 239 environment')
    checkpoint = previous.get('system_journal_checkpoint')
    stream, minimum = native.coordinates(required_anchor, boot)
    window.save(raw / 'original-input-state.json', previous)
    window.save(raw / 'required-window.json', {'entry': required_anchor, 'context': context})
    visible = native.query(['--system', '-b', boot, '--cursor', required_anchor['__CURSOR'], '--lines=1'],
                           raw / 'required-window-anchor.jsonl')
    if visible != [required_anchor] or required_anchor.get('_UID') != '0':
        raise RuntimeError('The declared current-boot window is not actually readable and root-owned')
    crossing, mode = None, 'checkpoint'
    if checkpoint is None:
        if previous or context['phase'] != 'before':
            raise RuntimeError('Only a fresh before segment may establish an initial boot window')
        mode = 'initial-window'
        anchor = required_anchor
    elif checkpoint['boot_id'] != boot:
        if context['phase'] != 'after':
            raise RuntimeError('An undeclared boot change reached the collector')
        crossing = transition(context, checkpoint, boot)
        if Path('/sys/class/dmi/id/product_uuid').read_text().strip().lower() != crossing['hardware_uuid']:
            raise RuntimeError('The actual dedicated VM changed across the declared reboot')
        old = native.query(['--system', '-b', checkpoint['boot_id'], '--cursor', checkpoint['entry']['__CURSOR'], '--lines=1'],
                           raw / 'old-boot-checkpoint-live.jsonl')
        if old != [checkpoint['entry']]:
            raise RuntimeError('The original actual pre-reboot checkpoint is no longer live')
        mode, anchor = 'declared-boot-transition', required_anchor
    else:
        if checkpoint['daemon'] != daemon:
            raise RuntimeError('Journal daemon changed inside a declared live segment')
        old_stream, number = native.coordinates(checkpoint['entry'], boot)
        if old_stream != stream or number < minimum:
            raise RuntimeError('A same-boot checkpoint precedes its declared required window')
        anchor = checkpoint['entry']
    anchor_time = int(required_anchor['__REALTIME_TIMESTAMP'])
    boundary = checkpoint['through'] if mode == 'checkpoint' else datetime.datetime.fromtimestamp(
        anchor_time // 1000000, datetime.timezone.utc).replace(microsecond=anchor_time % 1000000).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    began = now.strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    if native.timestamp(boundary) > native.timestamp(began):
        raise RuntimeError('The declared boot collection boundary moved backwards')
    marker = uuid.uuid4().hex
    emitted = subprocess.run(['logger', '--tag', native.MARKER_TAG, '--', marker],
                             capture_output=True, text=True, timeout=native.QUERY_TIMEOUT)
    window.save(raw / 'journal-marker.json', {'marker': marker, 'returncode': emitted.returncode,
                'stdout': emitted.stdout, 'stderr': emitted.stderr})
    if emitted.returncode:
        raise RuntimeError('The actual boot checkpoint emission failed')
    tail, attempts = native.terminal_checkpoint(raw, boot, marker)
    ended = int(tail['__REALTIME_TIMESTAMP'])
    if ended < native.timestamp(began):
        raise RuntimeError('The actual boot checkpoint precedes its collection')
    end = datetime.datetime.fromtimestamp(ended // 1000000, datetime.timezone.utc).replace(
        microsecond=ended % 1000000).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    rows = native.query(['-b', boot, '--cursor', anchor['__CURSOR'], '--until', end], raw / 'journal-sequence.jsonl')
    interval = native.validate_interval(rows, anchor, tail, boot)
    first, last = native.coordinates(anchor, boot)[1], native.coordinates(tail, boot)[1]
    accounted = window.account(raw, boot, stream, first, last)
    if native.BOOT.read_text().strip().replace('-', '') != boot or native.daemon_identity() != daemon:
        raise RuntimeError('Boot or journald changed while collecting a declared live segment')
    required = [row for row in interval if native.timestamp(boundary) <= int(row['__REALTIME_TIMESTAMP']) <= ended
                and (mode != 'checkpoint' or row['__CURSOR'] != anchor['__CURSOR'])]
    kernel = [row for row in required if row.get('_TRANSPORT') == 'kernel']
    (raw / 'kernel-journal.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in kernel))
    if any(any(term in str(row.get('MESSAGE', '')).lower() for term in ('suppressed', 'missed')) for row in required):
        raise RuntimeError('Required live-segment records were suppressed or missed')
    holes = native.sequence_holes(interval, boot)
    proof = {'boot_id': boot, 'daemon': daemon, 'since': boundary, 'through': end,
             'sequence_id': stream, 'first_sequence': first, 'last_sequence': last,
             'sequence_records': len(interval), 'required_records': len(required), 'checkpoint_attempts': attempts,
             'sequence_holes': holes, 'sequence_missing': sum(end - start + 1 for start, end in holes),
             'sequence_accounting': accounted, 'system_anchor': anchor['__CURSOR'], 'system_tail': tail['__CURSOR'],
             'source_sha256': window.digest(raw / 'journal-sequence.jsonl'), 'coverage_complete': True,
             'required_window_entry': required_anchor, 'original_input_checkpoint': checkpoint,
             'boot_collection_mode': mode, 'declared_boot_transition': crossing,
             'coverage_scope': 'declared-live-segment-only', 'generation_pause_claimed_as_covered': False}
    window.save(raw / 'journal-coverage.json', proof)
    return {**proof, 'cursor': kernel[-1]['__CURSOR'] if kernel else None,
            'memory_events': sum(any(term in str(row.get('MESSAGE', '')).lower()
                                     for term in ('out of memory', 'oom-kill', 'killed process')) for row in kernel),
            'checkpoint': {'boot_id': boot, 'daemon': daemon, 'entry': tail, 'through': end}}


def verify(raw, proof):
    original = load(raw / 'original-input-state.json')
    declared = load(raw / 'required-window.json')
    anchor, context = declared['entry'], declared['context']
    checkpoint = original.get('system_journal_checkpoint')
    boot = proof['boot_id']
    stream, minimum = native.coordinates(anchor, boot)
    if checkpoint != proof['original_input_checkpoint'] or anchor != proof['required_window_entry']:
        raise RuntimeError('The actual boot collector input or declared window changed')
    if window.load_query(raw / 'required-window-anchor.jsonl') != [anchor]:
        raise RuntimeError('The actual current-boot window lacks its successful direct query')
    mode = proof['boot_collection_mode']
    if mode == 'initial-window':
        if original or context['phase'] != 'before':
            raise RuntimeError('A retained collector checkpoint was cleared at an initial window')
        first_entry = anchor
    elif mode == 'declared-boot-transition':
        if checkpoint is None or checkpoint['boot_id'] == boot or context['phase'] != 'after':
            raise RuntimeError('The actual old checkpoint does not establish a declared boot transition')
        if transition(context, checkpoint, boot) != proof['declared_boot_transition']:
            raise RuntimeError('The actual declared boot-transition evidence changed')
        if window.load_query(raw / 'old-boot-checkpoint-live.jsonl') != [checkpoint['entry']]:
            raise RuntimeError('The retained pre-reboot checkpoint lacks its actual later live confirmation')
        first_entry = anchor
    elif mode == 'checkpoint':
        if checkpoint is None or checkpoint['boot_id'] != boot or checkpoint['daemon'] != proof['daemon']:
            raise RuntimeError('The retained same-boot checkpoint identity changed')
        old_stream, number = native.coordinates(checkpoint['entry'], boot)
        if old_stream != stream or number < minimum:
            raise RuntimeError('The actual same-boot checkpoint is outside its declared window')
        first_entry = checkpoint['entry']
    else:
        raise RuntimeError('The boot collector mode is unsupported')
    rows = window.load_query(raw / 'journal-sequence.jsonl')
    tail = window.load_query(raw / 'system-journal-tail.jsonl')
    if len(tail) != 1:
        raise RuntimeError('The actual boot terminal checkpoint is ambiguous')
    native.validate_interval(rows, first_entry, tail[0], boot)
    stored = load(raw / 'journal-window-accounting.json')
    recomputed = window.accounting(raw, stored)
    if (not recomputed['passed'] or stored['result'] != recomputed or recomputed != proof['sequence_accounting']
            or stored['first_sequence'] != native.coordinates(first_entry, boot)[1]
            or stored['last_sequence'] != native.coordinates(tail[0], boot)[1]
            or stored['sequence_id'] != stream or stored['boot_id'] != boot):
        raise RuntimeError('Actual stored identities do not reproduce the declared boot window')
    if proof['coverage_scope'] != 'declared-live-segment-only' or proof['generation_pause_claimed_as_covered']:
        raise RuntimeError('The boot collector expanded acceptance beyond its declared live segment')
    return True


class Collector:
    """Keep actual checkpoint state through native per-boot collection intervals."""

    def __init__(self, directory, required_anchor, context):
        self.directory, self.required_anchor, self.context = directory, required_anchor, context
        self.stopping = threading.Event()
        self.error = None

    def run(self):
        previous = self.context.get('previous_state', {})
        number = 0
        try:
            while True:
                terminal = self.stopping.wait(basic.COLLECTION_PERIOD)
                path = self.directory / ('interval-' + str(number))
                path.mkdir(mode=0o700)
                prepare.save(path / 'input-state.json', previous)
                began = basic.clock()
                result = collect(path, previous, datetime.datetime.now(datetime.timezone.utc),
                                 self.required_anchor, self.context)
                prepare.save(path / 'result.json', {'started': began, 'finished': basic.clock(), **result})
                previous = {'system_journal_checkpoint': result['checkpoint']}
                number += 1
                if terminal:
                    return
        except Exception as error:
            self.error = str(error)
            prepare.save(self.directory / 'error.json', {'observed': basic.clock(), 'error': self.error})
