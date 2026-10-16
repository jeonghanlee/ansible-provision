#!/usr/bin/env python3
"""Observe real journal preservation with pre-window baselines and disk-backed replay."""

import argparse
import concurrent.futures
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import sqlite3
import subprocess
import tempfile
import threading
import time
import uuid

import basic
import failure
import boot_coverage
import journal_coverage
import obsolete_anchor
import prepare
import rotation
import rotation_during
import window_coverage

FULL_DAY = 86400
PROBE_SECONDS = 120
QUERY_TIMEOUT = 120
START_LEAD_SECONDS = {FULL_DAY: 30, PROBE_SECONDS: 3}
CHECKPOINTS = {FULL_DAY: (21600, 43200, 64800), PROBE_SECONDS: (40, 80)}
DERIVED = {'artifact-index.json', 'result.json', 'comparisons.jsonl', 'failure-result.json'}
SCENARIOS = {
    'actual-loss': {'duration_seconds': 900, 'quiet_kernel_windows': [],
                    'checkpoint_offsets_seconds': [300, 600], 'start_lead_seconds': 3,
                    'align_collection_with_t0': True},
    'failure-termination': {'duration_seconds': 900, 'quiet_kernel_windows': [],
                            'checkpoint_offsets_seconds': [300], 'start_lead_seconds': 3,
                            'align_collection_with_t0': True},
    'restart-before': {'duration_seconds': 300, 'quiet_kernel_windows': [],
                       'checkpoint_offsets_seconds': [150], 'start_lead_seconds': 3,
                       'align_collection_with_t0': True},
    'restart-after': {'duration_seconds': 300, 'quiet_kernel_windows': [],
                      'checkpoint_offsets_seconds': [150], 'start_lead_seconds': 3,
                      'align_collection_with_t0': True},
    'quiet-kernel': {'duration_seconds': 1200, 'quiet_kernel_windows': [[300, 900]],
                     'checkpoint_offsets_seconds': [300, 900], 'start_lead_seconds': 3},
    'rotation-outside': {'duration_seconds': 900, 'quiet_kernel_windows': [],
                         'checkpoint_offsets_seconds': [300, 600], 'start_lead_seconds': 3,
                         'rotation_window_seconds': [360, 480]},
    'rotation-during': {'duration_seconds': 1200, 'quiet_kernel_windows': [],
                        'checkpoint_offsets_seconds': [300, 900], 'start_lead_seconds': 3,
                        'rotation_collection_indices': [0, 1, 2], 'align_collection_with_t0': True},
    'obsolete-anchor': {'duration_seconds': 1200, 'quiet_kernel_windows': [],
                        'checkpoint_offsets_seconds': [300, 900], 'start_lead_seconds': 3,
                        'obsolete_anchor_removal_window_seconds': [120, 180], 'align_collection_with_t0': True},
}


def observation_policy(duration, scenario=None):
    if scenario is None:
        if duration not in CHECKPOINTS:
            raise RuntimeError('Unsupported positive observation duration')
        return {'duration_seconds': duration, 'quiet_kernel_windows': [],
                'checkpoint_offsets_seconds': list(CHECKPOINTS[duration]),
                'start_lead_seconds': START_LEAD_SECONDS[duration]}
    if scenario not in SCENARIOS or duration != SCENARIOS[scenario]['duration_seconds']:
        raise RuntimeError('Unsupported lifecycle scenario or duration')
    return SCENARIOS[scenario]


def digest_file(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def rows(path):
    with path.open() as stream:
        for line in stream:
            yield json.loads(line)


def inventory(directory):
    return {str(path.relative_to(directory)): {'sha256': digest_file(path), 'bytes': path.stat().st_size}
            for path in sorted(directory.rglob('*')) if path.is_file()
            and path.relative_to(directory).as_posix() not in DERIVED}


def query(config, boot, cursor, destination):
    boundary = ['--since', cursor['since']] if isinstance(cursor, dict) else ['--cursor', cursor]
    command = ['journalctl', '--no-pager', '--all', '-o', 'json', '-b', boot, *boundary,
               'SYSLOG_IDENTIFIER=' + basic.TAG, '+', '_TRANSPORT=kernel', '+',
               '_SYSTEMD_UNIT=' + config['appliance_unit'], '+', '_SYSTEMD_UNIT=' + basic.HEALTH_UNIT]
    receipt = {'command': command, 'started': basic.clock()}
    errors = destination.with_suffix(destination.suffix + '.stderr')
    try:
        with destination.open('wb') as output, errors.open('wb') as error_output:
            result = subprocess.run(command, stdout=output, stderr=error_output, timeout=QUERY_TIMEOUT)
        receipt['returncode'] = result.returncode
    except (OSError, subprocess.TimeoutExpired) as error:
        receipt['error'] = str(error)
    receipt.update(finished=basic.clock(), stdout_sha256=digest_file(destination),
                   stderr=errors.read_text(errors='replace'))
    prepare.save(destination.with_suffix(destination.suffix + '.receipt.json'), receipt)
    return receipt


class Index:
    """Preserve full observed row content while bounding replay memory by one row."""

    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix='journal-long-replay-'))
        self.db = sqlite3.connect(self.root / 'index.sqlite')
        self.db.execute('CREATE TABLE records(kind, identity, payload, first_utc, first_mono, message, unit, '
                        'invocation, transport, priority, pid, realtime, UNIQUE(kind,identity))')
        self.db.execute('CREATE INDEX messages ON records(kind,message)')
        self.db.execute('CREATE INDEX invocations ON records(kind,invocation,unit)')
        self.db.execute('CREATE TABLE applications(pv,begin,end,first,second)')
        self.db.execute('CREATE INDEX requests ON applications(pv,begin,end)')
        self.db.execute('CREATE TABLE outcomes(id PRIMARY KEY,payload)')
        self.db.execute('CREATE TABLE required(identity PRIMARY KEY,action_id)')

    def add(self, kind, row, observed=None, overlap=False):
        key = json.dumps(basic.identity(row))
        payload = json.dumps(row, sort_keys=True)
        previous = self.db.execute('SELECT payload FROM records WHERE kind=? AND identity=?', (kind, key)).fetchone()
        if previous:
            if not overlap or previous[0] != payload:
                raise basic.ConfirmedViolation('Unexpected repeated or changed journal identity: ' + kind)
            return
        self.db.execute('INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                        (kind, key, payload, observed['utc'] if observed else None,
                         observed['monotonic_ns'] if observed else None, row.get('MESSAGE'),
                         row.get('_SYSTEMD_UNIT'), row.get('_SYSTEMD_INVOCATION_ID'), row.get('_TRANSPORT'),
                         row.get('PRIORITY'), row.get('_PID'), int(row['__REALTIME_TIMESTAMP'])))

    def get(self, kind, key):
        value = self.db.execute('SELECT payload FROM records WHERE kind=? AND identity=?', (kind, key)).fetchone()
        return json.loads(value[0]) if value else None

    def sources(self, config):
        pending = {}
        for key, payload in self.db.execute('SELECT identity,payload FROM records WHERE kind=? AND unit=? '
                                           'AND transport=? AND priority=? ORDER BY realtime,rowid',
                                           ('direct', config['appliance_unit'], 'stdout', '7')):
            row = json.loads(payload)
            match = basic.APP_MESSAGE.fullmatch(str(row.get('MESSAGE')))
            if not match:
                continue
            thread, text = match.groups()
            context = (row.get('_PID'), thread)
            if text.startswith('pvName is '):
                pending[context] = (key, text.removeprefix('pvName is '))
            times = basic.APP_TIMES.fullmatch(text)
            if times and context in pending:
                first, pv = pending.pop(context)
                self.db.execute('INSERT INTO applications VALUES(?,?,?,?,?)', (pv, times[2], times[1], first, key))

    def required(self, action, outcome, config):
        if action['path'] == 'appliance':
            selected = {}
            for first, second in self.db.execute('SELECT first,second FROM applications WHERE pv=? AND begin=? AND end=?',
                                                 (action['pv'], action['start'], action['end'])):
                for key in (first, second):
                    selected[key] = self.get('direct', key)
        elif action['path'] == 'health':
            invocation = outcome.get('health', {}).get('invocation_id', '')
            marker = basic.HEALTH_PREFIX + json.dumps(outcome.get('health', {}), sort_keys=True)
            selected = dict((key, json.loads(payload)) for key, payload in self.db.execute(
                'SELECT identity,payload FROM records WHERE kind=? AND invocation=? AND unit=? '
                'UNION ALL SELECT identity,payload FROM records '
                'WHERE kind=? AND message=? AND unit=? AND invocation IS NULL',
                ('direct', invocation, basic.HEALTH_UNIT, 'direct', marker, basic.HEALTH_UNIT)))
        else:
            selected = dict((key, json.loads(payload)) for key, payload in self.db.execute(
                'SELECT identity,payload FROM records WHERE kind=? AND message=?', ('direct', action['message'])))
        native = {basic.identity(row): row for row in selected.values()}
        return basic.required_records(action, outcome, basic.source_index(native, config), config)


def checked_query(path):
    receipt = json.loads(path.with_suffix(path.suffix + '.receipt.json').read_text())
    if receipt.get('returncode') != 0 or receipt.get('stderr', '').strip() or receipt.get('error'):
        raise RuntimeError('A required live query did not complete successfully: ' + path.name)
    if digest_file(path) != receipt['stdout_sha256']:
        raise RuntimeError('A live query changed: ' + path.name)
    return receipt


def replay(directory, publish=False):
    if (directory / 'contract.json').is_file() and json.loads((directory / 'contract.json').read_text()).get('scenario') == 'actual-loss':
        import loss
        return loss.replay(directory, publish)
    result = {'scope': 'full-day-journal', 'delivery': 'Incomplete', 'later_live_read': 'Incomplete',
              'collection': 'Incomplete', 'baseline_retention': 'Incomplete', 'intermediate_live_reads': 'Incomplete',
              'overall': 'Incomplete', 'full_day_acceptance': 'Pending', 'violations': [], 'unresolved': [],
              'paths': {}, 'baseline_paths': {}}
    index = Index()
    try:
        if inventory(directory) != json.loads((directory / 'artifact-index.json').read_text()):
            raise RuntimeError('Original full-day evidence differs from its frozen index')
        prepare.verify(directory / 'package')
        for module in (basic, prepare, journal_coverage, rotation, rotation_during, obsolete_anchor, window_coverage, boot_coverage, failure):
            if digest_file(Path(module.__file__)) != digest_file(directory / 'package' / Path(module.__file__).name):
                raise RuntimeError('Replay must use the original frozen helper modules')
        if digest_file(Path(__file__)) != digest_file(directory / 'package/long.py'):
            raise RuntimeError('Replay must use the original frozen long-path tool')
        state = json.loads((directory / 'observation.json').read_text())
        contract = json.loads((directory / 'contract.json').read_text())
        if contract.get('restart_input_sha256') is not None:
            if digest_file(directory / 'restart-input.json') != contract['restart_input_sha256']:
                raise RuntimeError('The declared restart input state changed')
            if digest_file(directory / 'restart-window.json') != contract['restart_window_sha256']:
                raise RuntimeError('The actual restart window boundary changed')
            declared_window = json.loads((directory / 'restart-window.json').read_text())
            if (window_coverage.load_query(directory / 'restart-window' / declared_window['query']) != [declared_window['entry']]
                    or declared_window['context_sha256'] != contract['restart_input_sha256']):
                raise RuntimeError('The declared restart window lacks its actual original source query')
        config = json.loads((directory / 'package/config.json').read_text())
        duration = contract['duration_seconds']
        scenario = contract.get('scenario')
        policy = observation_policy(duration, scenario)
        result['planned_seconds'] = duration
        result['full_day_acceptance'] = 'Incomplete' if duration == FULL_DAY else 'Pending'
        result['scope'] = ('journal-' + scenario if scenario else
                           'full-day-journal' if duration == FULL_DAY else 'long-path-probe')
        if state['state'] != 'Finished':
            raise RuntimeError('An intact finished supported observation is required')
        if (contract['checkpoint_offsets_seconds'] != policy['checkpoint_offsets_seconds']
                or contract.get('quiet_kernel_windows', []) != policy['quiet_kernel_windows']
                or contract.get('rotation_window_seconds') != policy.get('rotation_window_seconds')
                or contract.get('rotation_collection_indices') != policy.get('rotation_collection_indices')
                or contract.get('align_collection_with_t0', False) != policy.get('align_collection_with_t0', False)
                or contract.get('obsolete_anchor_removal_window_seconds') != policy.get('obsolete_anchor_removal_window_seconds')
                or contract['periods_seconds'] != basic.PERIODS
                or contract['checkpoint_eligibility_guard_seconds'] != basic.VISIBILITY_WAIT):
            raise RuntimeError('The declared frequencies or intermediate query schedule changed')
        for name in ('schedule.jsonl', 'baseline-schedule.jsonl'):
            if digest_file(directory / name) != contract['schedules_sha256'][name]:
                raise RuntimeError('An independent producer schedule changed')
        if digest_file(directory / 'baseline.json') != contract['baseline_sha256']:
            raise RuntimeError('The independent baseline confirmation changed')
        for entry in rows(directory / 'direct/queries.jsonl'):
            path = directory / 'direct' / entry['file']
            checked_query(path)
            if digest_file(path) != entry['sha256']:
                raise RuntimeError('Direct-query receipt and ledger disagree')
            for row in rows(path):
                index.add('direct', row, entry['finished'], overlap=True)
        index.sources(config)
        if policy['quiet_kernel_windows']:
            quiet_counts = []
            for begin, end in policy['quiet_kernel_windows']:
                start_us = journal_coverage.timestamp(contract['start']['utc']) + begin * 1000000
                end_us = journal_coverage.timestamp(contract['start']['utc']) + end * 1000000
                count = index.db.execute(
                    'SELECT COUNT(*) FROM records WHERE kind=? AND transport=? AND realtime>=? AND realtime<?',
                    ('direct', 'kernel', start_us, end_us)).fetchone()[0]
                quiet_counts.append({'begin_seconds': begin, 'end_seconds': end,
                                     'actual_kernel_records': count})
                if count:
                    result['unresolved'].append('The declared quiet interval contained actual kernel events')
            result['quiet_kernel_intervals'] = quiet_counts
        final = directory / 'final-live.jsonl'
        final_receipt = checked_query(final)
        for row in rows(final):
            index.add('final', row, overlap=True)
        for number, offset in enumerate(contract['checkpoint_offsets_seconds']):
            path = directory / 'checkpoints' / ('checkpoint-' + str(number) + '.jsonl')
            receipt = checked_query(path)
            if receipt['started']['monotonic_ns'] < contract['start']['monotonic_ns'] + offset * 1000000000:
                raise RuntimeError('A planned intermediate query ran before its checkpoint')
            for row in rows(path):
                index.add('checkpoint-' + str(number), row, overlap=True)
        if 'obsolete_anchor_removal_window_seconds' in policy:
            result['obsolete_anchor'] = obsolete_anchor.verify_metadata(directory, contract)
        previous = None
        intervals = sorted((directory / 'collector').glob('interval-*'), key=lambda path: int(path.name.split('-')[-1]))
        if not intervals:
            raise RuntimeError('No native collector interval was retained')
        if policy.get('align_collection_with_t0'):
            first = json.loads((intervals[0] / 'result.json').read_text())
            if first['started']['monotonic_ns'] < contract['start']['monotonic_ns'] + basic.COLLECTION_PERIOD * 1000000000:
                raise RuntimeError('The first native collection preceded its declared t0 boundary')
        for interval in intervals:
            proof = json.loads((interval / 'journal-coverage.json').read_text())
            source = interval / 'journal-sequence.jsonl'
            if not proof.get('coverage_complete') or digest_file(source) != proof['source_sha256']:
                raise RuntimeError('A native collector interval lacks its unchanged coverage proof')
            if scenario in ('restart-before', 'restart-after', 'failure-termination'):
                boot_coverage.verify(interval, proof)
                if proof['required_window_entry'] != declared_window['entry']:
                    raise RuntimeError('A native boot interval used a different declared required window')
                retained = json.loads((interval / 'input-state.json').read_text())
                if retained.get('system_journal_checkpoint') != proof['original_input_checkpoint']:
                    raise RuntimeError('The actual boot collector changed its retained checkpoint input')
            if scenario == 'restart-after':
                original_state = json.loads((directory / 'restart-input.json').read_text())['previous_state']
                first_state = json.loads((intervals[0] / 'input-state.json').read_text())
                if first_state != original_state:
                    raise RuntimeError('The actual pre-reboot checkpoint was reset before post-reboot collection')
            if 'obsolete_anchor_removal_window_seconds' in policy:
                window_coverage.verify(interval, proof)
                prepared = json.loads((directory / 'obsolete-anchor/preparation.json').read_text())
                if proof['required_window_entry'] != prepared['new_window_anchor']:
                    raise RuntimeError('The actual native interval used a different required-window boundary')
                previous_state = json.loads((interval / 'input-state.json').read_text())
                if proof['original_input_checkpoint'] != previous_state['system_journal_checkpoint']:
                    raise RuntimeError('The native collector changed its retained input checkpoint')
                if previous is not None and previous_state['system_journal_checkpoint']['entry'] != previous:
                    raise RuntimeError('The required-window collector did not retain its preceding checkpoint')
            first, last = None, None
            for row in rows(source):
                if first is None:
                    first = row
                    if previous is not None:
                        if previous != first:
                            raise RuntimeError('Adjacent native collector checkpoints disagree')
                        last = row
                        continue
                index.add('archive', row)
                last = row
            if first is None or first['__CURSOR'] != proof['system_anchor'] or last['__CURSOR'] != proof['system_tail']:
                raise RuntimeError('Native collector rows and declared boundaries disagree')
            previous = last
        for name in ('baseline-outcomes.jsonl', 'outcomes.jsonl'):
            for outcome in rows(directory / name):
                try:
                    index.db.execute('INSERT INTO outcomes VALUES(?,?)', (outcome['id'], json.dumps(outcome)))
                except sqlite3.IntegrityError:
                    raise basic.ConfirmedViolation('Producer outcomes repeat an action identity')
        baseline = json.loads((directory / 'baseline.json').read_text())
        baseline_keys = {item['action_id']: item for item in baseline['actions']}
        if len(baseline_keys) != len(basic.PERIODS):
            raise RuntimeError('Exactly one independent baseline action per path is required')
        comparisons = index.root / 'comparisons.jsonl'
        seen = set()
        failed_actions, missing_sources, failed_live, failed_archive, failed_intermediate, short_baselines = [], [], [], [], [], []
        with comparisons.open('w') as output:
            for name, group in (('baseline-schedule.jsonl', 'baseline_paths'), ('schedule.jsonl', 'paths')):
                sequences = {path: [] for path in basic.PERIODS}
                for action in rows(directory / name):
                    if action['id'] in seen:
                        raise basic.ConfirmedViolation('The producer schedules repeat an identity')
                    seen.add(action['id'])
                    sequences[action['path']].append(action['sequence'])
                    if action['offset_seconds'] != action['sequence'] * basic.PERIODS[action['path']]:
                        raise RuntimeError('A scheduled action does not match its declared frequency')
                    if group == 'paths':
                        planned = contract['start']['monotonic_ns'] + action['offset_seconds'] * 1000000000
                        planned_utc = (datetime.datetime.fromisoformat(contract['start']['utc']) +
                                       datetime.timedelta(seconds=action['offset_seconds'])).isoformat()
                        if action['planned_monotonic_ns'] != planned or action['planned_utc'] != planned_utc:
                            raise RuntimeError('A producer action changed its predeclared time')
                    stats = result[group].setdefault(action['path'], {'planned': 0, 'executed': 0, 'confirmed': 0,
                                                                     'required_records': 0, 'http_errors': 0})
                    stats['planned'] += 1
                    record = index.db.execute('SELECT payload FROM outcomes WHERE id=?', (action['id'],)).fetchone()
                    if record is None:
                        result['unresolved'].append('Missing producer outcome: ' + action['id'])
                        missing_sources.append(action['id'])
                        continue
                    outcome = json.loads(record[0])
                    if not outcome.get('executed') and not (action['path'] == 'appliance' and outcome.get('attempted')):
                        result['violations'].append('A required action was not executed: ' + action['id'])
                        failed_actions.append(action['id'])
                        continue
                    matched = index.required(action, outcome, config)
                    if len(matched) != (2 if action['path'] in ('appliance', 'health') else 1):
                        result['unresolved'].append('Missing or ambiguous required source set: ' + action['id'])
                        missing_sources.append(action['id'])
                        continue
                    stats['executed'] += 1
                    stats['confirmed'] += 1
                    stats['required_records'] += len(matched)
                    stats['http_errors'] += bool(outcome.get('execution', {}).get('error')) if action['path'] == 'appliance' else 0
                    for row in matched:
                        if scenario in ('restart-before', 'restart-after'):
                            position = journal_coverage.coordinates(row, state['start_boot'])[1]
                            beginning = journal_coverage.coordinates(declared_window['entry'], state['start_boot'])[1]
                            if position <= beginning:
                                raise basic.ConfirmedViolation('A required restart record precedes its declared collector window')
                        key = json.dumps(basic.identity(row))
                        try:
                            index.db.execute('INSERT INTO required VALUES(?,?)', (key, action['id']))
                        except sqlite3.IntegrityError:
                            raise basic.ConfirmedViolation('Different actions claim the same required source identity')
                        direct = index.db.execute('SELECT first_utc,first_mono FROM records WHERE kind=? AND identity=?',
                                                  ('direct', key)).fetchone()
                        age = (final_receipt['finished']['monotonic_ns'] - direct[1]) / 1e9
                        utc_age = (datetime.datetime.fromisoformat(final_receipt['finished']['utc']) -
                                   datetime.datetime.fromisoformat(direct[0])).total_seconds()
                        if group == 'baseline_paths':
                            original = baseline_keys[action['id']]
                            expected = {json.dumps(basic.identity(item['record'])): item for item in original['records']}
                            if key not in expected or expected[key]['record'] != row or expected[key]['first_confirmed']['monotonic_ns'] != direct[1]:
                                raise basic.ConfirmedViolation('The pre-window baseline differs from its original direct confirmation')
                            if (direct[1] > contract['start']['monotonic_ns'] or
                                    datetime.datetime.fromisoformat(direct[0]) > datetime.datetime.fromisoformat(contract['start']['utc'])):
                                raise RuntimeError('A required baseline was not confirmed before t0')
                            if age < duration or utc_age < duration:
                                result['unresolved'].append('A baseline has not survived the planned duration: ' + action['id'])
                                short_baselines.append(action['id'])
                        for kind in ('final', 'archive'):
                            if index.get(kind, key) != row:
                                result['violations'].append('Missing or changed required record in ' + kind + ': ' + action['id'])
                                (failed_live if kind == 'final' else failed_archive).append(action['id'])
                        checkpoints = []
                        for number, offset in enumerate(contract['checkpoint_offsets_seconds']):
                            if group == 'baseline_paths' or action['offset_seconds'] < offset - basic.VISIBILITY_WAIT:
                                kind = 'checkpoint-' + str(number)
                                if index.get(kind, key) != row:
                                    result['violations'].append('Missing or changed required intermediate record: ' + action['id'])
                                    failed_intermediate.append(action['id'])
                                checkpoints.append(number)
                        output.write(json.dumps({'action_id': action['id'], 'path': action['path'],
                                                 'identity': basic.identity(row), 'message_sha256': prepare.digest(str(row['MESSAGE']).encode()),
                                                 'first_confirmed': {'utc': direct[0], 'monotonic_ns': direct[1]},
                                                 'age_at_final_read_seconds': age, 'utc_age_at_final_read_seconds': utc_age,
                                                 'baseline': group == 'baseline_paths', 'checkpoints': checkpoints}, sort_keys=True) + '\n')
                for path, period in basic.PERIODS.items():
                    quiet = policy['quiet_kernel_windows'] if path == 'kernel' and group == 'paths' else []
                    expected = ([0] if group == 'baseline_paths' else
                                basic.scheduled_sequences(duration, period, quiet))
                    if sequences[path] != expected:
                        raise RuntimeError('The independent schedule does not match its declared frequency')
        if index.db.execute('SELECT COUNT(*) FROM outcomes').fetchone()[0] != len(seen):
            raise basic.ConfirmedViolation('Producer outcomes contain unscheduled actions')
        if state['start_boot'] != state['end_boot'] or state['start_daemon'] != state['end_daemon']:
            result['violations'].append('Boot or journald identity changed during the positive observation')
        result['unresolved'].extend(state.get('errors', []))
        if 'rotation_window_seconds' in policy:
            try:
                result['rotation'] = rotation.verify(directory, contract)
            except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
                result['unresolved'].append(str(error))
        if 'rotation_collection_indices' in policy:
            try:
                result['rotation'] = rotation_during.verify(directory, contract)
            except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
                result['unresolved'].append(str(error))
        monotonic = (state['ended']['monotonic_ns'] - contract['start']['monotonic_ns']) / 1e9
        utc = (datetime.datetime.fromisoformat(state['ended']['utc']) -
               datetime.datetime.fromisoformat(contract['start']['utc'])).total_seconds()
        if monotonic < duration or utc < duration:
            result['unresolved'].append('The planned positive observation did not finish in both clocks')
        result.update(planned_seconds=duration, actual_elapsed_seconds=monotonic, utc_elapsed_seconds=utc,
                      comparisons_sha256=digest_file(comparisons), native_collector_intervals=len(intervals))
        verdict = 'Failed' if result['violations'] else 'Incomplete' if result['unresolved'] else 'Passed'
        complete_sources = not failed_actions and not missing_sources
        baseline_ids = set(baseline_keys)
        result.update(overall=verdict,
                      delivery='Failed' if failed_actions else 'Incomplete' if missing_sources else 'Passed',
                      later_live_read='Failed' if failed_live else 'Passed' if complete_sources else 'Incomplete',
                      collection='Failed' if failed_archive else 'Passed' if complete_sources else 'Incomplete',
                      baseline_retention='Failed' if baseline_ids.intersection(failed_live) else
                          'Incomplete' if short_baselines or baseline_ids.intersection(missing_sources + failed_actions) else 'Passed',
                      intermediate_live_reads='Failed' if failed_intermediate else 'Passed' if complete_sources else 'Incomplete',
                      full_day_acceptance=verdict if duration == FULL_DAY else 'Pending')
        if publish:
            shutil.copyfile(comparisons, directory / 'comparisons.jsonl')
        elif not (directory / 'comparisons.jsonl').exists() or digest_file(directory / 'comparisons.jsonl') != digest_file(comparisons):
            raise RuntimeError('The replayed per-event comparisons differ from the original')
    except basic.ConfirmedViolation as error:
        result['violations'].append(str(error))
        result['overall'] = 'Failed'
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, sqlite3.Error) as error:
        result['unresolved'].append(str(error))
        result['overall'] = 'Incomplete' if not result['violations'] else 'Failed'
    finally:
        index.db.close()
    if result['overall'] != 'Passed' and result.get('planned_seconds') == FULL_DAY:
        result['full_day_acceptance'] = result['overall']
    return result


def run(config_path, duration, scenario=None, restart_input=None, directory=None):
    policy = observation_policy(duration, scenario)
    if scenario in ('restart-before', 'restart-after', 'failure-termination', 'actual-loss') and restart_input is None:
        raise RuntimeError('A restart segment requires its declared parent input state')
    config = prepare.configuration(config_path)
    prepare.verify(basic.PACKAGE)
    prepare.RUNTIME.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (prepare.RUNTIME / 'basic.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        directory = directory or prepare.EVIDENCE / ('long-' + uuid.uuid4().hex)
        if (directory.parent != prepare.EVIDENCE or not directory.name.startswith('long-')
                or directory.exists() or directory.is_symlink()):
            raise RuntimeError('The new observation evidence path is invalid or already used')
        directory.mkdir(parents=True, mode=0o700)
        shutil.copytree(basic.PACKAGE, directory / 'package')
        prepare.save(directory / 'package/config.json', config)
        for name in ('readiness', 'actions', 'direct', 'collector', 'checkpoints'):
            (directory / name).mkdir(mode=0o700)
        if restart_input is not None:
            if scenario not in ('restart-before', 'restart-after', 'failure-termination', 'actual-loss'):
                raise RuntimeError('Restart input belongs only to a declared restart segment')
            prepare.save(directory / 'restart-input.json', restart_input)
        ready = basic.preflight(config, directory / 'readiness',
                                allowed_boots=restart_input['journal_boots'] if restart_input else None)
        if not ready['ready']:
            raise RuntimeError('The actual dedicated journal deployment is not ready')
        obsolete_preparation = (obsolete_anchor.prewindow(directory)
                                if 'obsolete_anchor_removal_window_seconds' in policy else None)
        restart_window = boot_coverage.setup(directory, restart_input) if restart_input is not None else None
        boot = journal_coverage.BOOT.read_text().strip().replace('-', '')
        anchor = journal_coverage.query(['--system', '-b', boot, '--reverse', '--lines=1'], directory / 'initial-anchor.jsonl')
        if len(anchor) != 1:
            raise RuntimeError('A unique initial live journal anchor is required')
        query_boundary = anchor[0]['__CURSOR']
        if scenario == 'actual-loss':
            query_boundary = {'since': datetime.datetime.fromtimestamp(int(restart_window['__REALTIME_TIMESTAMP']) / 1000000,
                              datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f UTC')}
        began = basic.clock()
        baseline_actions = basic.schedule(uuid.uuid4().hex, config, began, 1)
        with (directory / 'baseline-schedule.jsonl').open('w') as stream:
            stream.write(''.join(json.dumps(row, sort_keys=True) + '\n' for row in baseline_actions))
        reader = basic.DirectReader(directory / 'direct', config, boot, anchor[0]['__CURSOR'])
        collector = (obsolete_anchor.Collector(directory / 'collector', obsolete_preparation['checkpoint'],
                                              obsolete_preparation['new_window_anchor'])
                     if obsolete_preparation is not None else basic.Collector(directory / 'collector', began,
                         previous_checkpoint=restart_input.get('previous_state') if restart_input else None))
        if restart_input is not None:
            collector = boot_coverage.Collector(directory / 'collector', restart_window, restart_input)
        if scenario == 'failure-termination':
            collector = failure.Collector(directory, restart_window, restart_input)
        if scenario == 'actual-loss':
            import loss
            collector = loss.Collector(directory, restart_window, restart_input)
        threads = [threading.Thread(target=reader.run), threading.Thread(target=collector.run)]
        stopping = threading.Event()
        handlers = {number: signal.signal(number, lambda *_: stopping.set()) for number in (signal.SIGINT, signal.SIGTERM)}
        state = {'state': 'Confirming baselines', 'start_boot': boot,
                 'start_daemon': journal_coverage.daemon_identity(), 'errors': []}
        prepare.save(directory / 'observation.json', state)
        threads[0].start()
        collector_started = not policy.get('align_collection_with_t0', False)
        if collector_started:
            threads[1].start()
        workers = {path: concurrent.futures.ThreadPoolExecutor(max_workers=basic.WORKERS[path]) for path in basic.PERIODS}
        snapshots = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        pending, baseline_outcomes, checkpoint_tasks = {}, [], []
        rotation_action, rotation_worker = None, None
        obsolete_action, obsolete_worker = None, None
        loss_action, loss_worker = None, None
        try:
            for action in baseline_actions:
                outcome = basic.emit(action, config, directory / 'actions')
                basic.append(directory / 'baseline-outcomes.jsonl', outcome)
                baseline_outcomes.append(outcome)
                if not outcome.get('executed') and not (action['path'] == 'appliance' and outcome.get('attempted')):
                    raise RuntimeError('A required baseline action was not executed')
            deadline = time.monotonic() + basic.VISIBILITY_WAIT
            while True:
                try:
                    direct, first = basic.direct_records(directory / 'direct')
                    source_index = basic.source_index(direct, config)
                    baseline = []
                    for action, outcome in zip(baseline_actions, baseline_outcomes):
                        matched = basic.required_records(action, outcome, source_index, config)
                        if len(matched) != (2 if action['path'] in ('appliance', 'health') else 1):
                            break
                        baseline.append({'action_id': action['id'], 'records': [
                            {'record': row, 'first_confirmed': first[basic.identity(row)]} for row in matched]})
                    if len(baseline) == len(baseline_actions):
                        break
                except (OSError, ValueError, KeyError):
                    pass
                if stopping.is_set() or time.monotonic() >= deadline:
                    raise RuntimeError('Not every required baseline was directly confirmed before t0')
                stopping.wait(0.2)
            prepare.save(directory / 'baseline.json', {'actions': baseline, 'confirmed': basic.clock()})
            now = basic.clock()
            lead = policy['start_lead_seconds']
            start = {'utc': (datetime.datetime.fromisoformat(now['utc']) + datetime.timedelta(seconds=lead)).isoformat(),
                     'monotonic_ns': now['monotonic_ns'] + lead * 1000000000}
            actions = basic.schedule(uuid.uuid4().hex, config, start, duration,
                                     policy['quiet_kernel_windows'])
            baseline_requests = {(row['pv'], row['start'], row['end']) for row in baseline_actions if row['path'] == 'appliance'}
            if any((row['pv'], row['start'], row['end']) in baseline_requests for row in actions if row['path'] == 'appliance'):
                raise RuntimeError('Independent baseline and window request tuples collide')
            with (directory / 'schedule.jsonl').open('w') as stream:
                stream.write(''.join(json.dumps(row, sort_keys=True) + '\n' for row in actions))
                stream.flush()
                os.fsync(stream.fileno())
            prepare.save(directory / 'contract.json', {'schema': 1, 'scope': 'positive-live-preservation',
                         **({'restart_input_sha256': digest_file(directory / 'restart-input.json')}
                            if restart_input is not None else {}),
                         **({'restart_window_sha256': digest_file(directory / 'restart-window.json')}
                            if restart_input is not None else {}),
                         **({'scenario': scenario, 'quiet_kernel_windows': policy['quiet_kernel_windows']}
                            if scenario else {}),
                         **({'rotation_window_seconds': policy['rotation_window_seconds']}
                            if 'rotation_window_seconds' in policy else {}),
                         **({'rotation_collection_indices': policy['rotation_collection_indices']}
                            if 'rotation_collection_indices' in policy else {}),
                         **({'align_collection_with_t0': True} if policy.get('align_collection_with_t0') else {}),
                         **({'obsolete_anchor_removal_window_seconds': policy['obsolete_anchor_removal_window_seconds'],
                             'obsolete_anchor_preparation_sha256': digest_file(directory / 'obsolete-anchor/preparation.json')}
                            if obsolete_preparation is not None else {}),
                         'start': start, 'duration_seconds': duration, 'periods_seconds': basic.PERIODS,
                         'checkpoint_offsets_seconds': policy['checkpoint_offsets_seconds'],
                         'checkpoint_eligibility_guard_seconds': basic.VISIBILITY_WAIT,
                         'visibility_wait_seconds': basic.VISIBILITY_WAIT, 'direct_query_seconds': basic.QUERY_PERIOD,
                         'collection_seconds': basic.COLLECTION_PERIOD,
                         'workers_by_path': basic.WORKERS, 'appliance_logger': prepare.LOGGER,
                         'appliance_parser_source_commit': prepare.APPLIANCE_SOURCE,
                         'appliance_required_messages': ['pvName is {pv}',
                             'requestTimesOb is RequestTimes[end={end}, start={start}, requestTimes=...]'],
                         'baseline_sha256': digest_file(directory / 'baseline.json'),
                         'schedules_sha256': {name: digest_file(directory / name) for name in
                                              ('schedule.jsonl', 'baseline-schedule.jsonl')}})
            state.update(state='Running', t0=start)
            if scenario == 'failure-termination':
                failure.declare(directory, config, start)
            if scenario == 'actual-loss':
                loss.declare(directory, start)
            prepare.save(directory / 'observation.json', state)
            if time.monotonic_ns() >= start['monotonic_ns']:
                raise RuntimeError('The declared start elapsed before the schedule was frozen')
            if 'rotation_window_seconds' in policy:
                rotation_action = rotation.OutsideCollection(directory, start, policy['rotation_window_seconds'], stopping)
                rotation_worker = threading.Thread(target=rotation_action.run)
                rotation_worker.start()
            if 'rotation_collection_indices' in policy:
                rotation_action = rotation_during.DuringCollection(directory, policy['rotation_collection_indices'], stopping)
                rotation_worker = threading.Thread(target=rotation_action.run)
                rotation_worker.start()
            if obsolete_preparation is not None:
                obsolete_action = obsolete_anchor.Remove(directory, obsolete_preparation, start,
                                    policy['obsolete_anchor_removal_window_seconds'], stopping)
                obsolete_worker = threading.Thread(target=obsolete_action.run)
                obsolete_worker.start()
            if scenario == 'actual-loss':
                loss_action = loss.Remove(directory, config, start, stopping)
                loss_worker = threading.Thread(target=loss_action.run)
                loss_worker.start()
            next_checkpoint = 0
            for action in actions:
                while time.monotonic_ns() < action['planned_monotonic_ns']:
                    if collector.error:
                        raise RuntimeError('Actual collector failure detected: ' + collector.error)
                    stopping.wait(min(0.1, (action['planned_monotonic_ns'] - time.monotonic_ns()) / 1e9))
                    if stopping.is_set():
                        raise InterruptedError('Positive observation interrupted')
                if not collector_started:
                    threads[1].start()
                    collector_started = True
                if collector.error:
                    raise RuntimeError('Actual collector failure detected: ' + collector.error)
                while (next_checkpoint < len(policy['checkpoint_offsets_seconds']) and
                       time.monotonic_ns() >= start['monotonic_ns'] +
                       policy['checkpoint_offsets_seconds'][next_checkpoint] * 1000000000):
                    path = directory / 'checkpoints' / ('checkpoint-' + str(next_checkpoint) + '.jsonl')
                    checkpoint_tasks.append(snapshots.submit(query, config, boot, query_boundary, path))
                    next_checkpoint += 1
                for future in list(pending):
                    if future.done():
                        basic.append(directory / 'outcomes.jsonl', future.result())
                        del pending[future]
                late = time.monotonic_ns() - action['planned_monotonic_ns']
                active = sum(item['path'] == action['path'] for item in pending.values())
                if active >= basic.WORKERS[action['path']] or late >= basic.PERIODS[action['path']] * 1000000000:
                    basic.append(directory / 'outcomes.jsonl', {'id': action['id'], 'path': action['path'],
                                 'executed': False, 'skipped': True, 'observed': basic.clock()})
                else:
                    pending[workers[action['path']].submit(basic.emit, action, config, directory / 'actions')] = action
            while time.monotonic_ns() < start['monotonic_ns'] + duration * 1000000000:
                if stopping.wait(0.1):
                    raise InterruptedError('Positive observation interrupted')
        except BaseException as error:
            state['errors'].append(str(error))
            if scenario == 'failure-termination' and collector.error:
                completed = {row['id'] for row in basic.load_rows(directory / 'outcomes.jsonl')}
                submitted = {item['id'] for item in pending.values()}
                detected = basic.clock()
                prepare.save(directory / 'failure-detected.json', {'observed': detected, 'error': collector.error})
                for item in actions:
                    if item['id'] not in completed | submitted:
                        basic.append(directory / 'outcomes.jsonl', {'id': item['id'], 'path': item['path'],
                                     'executed': False, 'cancelled': True,
                                     'reason': 'Actual collector CLI failure', 'observed': detected})
        finally:
            for action, worker in ((rotation_action, rotation_worker), (obsolete_action, obsolete_worker), (loss_action, loss_worker)):
                if worker is not None and worker.ident is not None:
                    worker.join()
                    if action.error:
                        state['errors'].append(action.error)
            for worker in workers.values():
                worker.shutdown(wait=True)
            for future in pending:
                try:
                    basic.append(directory / 'outcomes.jsonl', future.result())
                except Exception as error:
                    state['errors'].append(str(error))
            stopping.wait(basic.VISIBILITY_WAIT)
            reader.stopping.set()
            threads[0].join()
            state['final_query'] = query(config, boot, query_boundary, directory / 'final-live.jsonl')
            collector.stopping.set()
            if not collector_started:
                threads[1].start()
                collector_started = True
            threads[1].join()
            if scenario == 'failure-termination' and collector.error:
                collector.recover()
            snapshots.shutdown(wait=True)
            for future in checkpoint_tasks:
                try:
                    future.result()
                except Exception as error:
                    state['errors'].append(str(error))
            state['errors'].extend(error for error in (reader.error, collector.error) if error)
            if scenario == 'failure-termination' and collector.error:
                failure.finish(directory)
            state.update(state='Finished', ended=basic.clock(), end_boot=journal_coverage.BOOT.read_text().strip().replace('-', ''),
                         end_daemon=journal_coverage.daemon_identity())
            prepare.save(directory / 'observation.json', state)
            for number, handler in handlers.items():
                signal.signal(number, handler)
        prepare.save(directory / 'artifact-index.json', inventory(directory))
        result = replay(directory, publish=True)
        prepare.save(directory / 'result.json', result)
        if scenario == 'failure-termination':
            prepare.save(directory / 'failure-result.json', failure.replay(directory))
        return directory, result


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    start = commands.add_parser('run')
    start.add_argument('--config', type=Path, default=basic.PACKAGE / 'config.json')
    start.add_argument('--seconds', type=int, choices=tuple(CHECKPOINTS), default=FULL_DAY)
    repeat = commands.add_parser('replay')
    repeat.add_argument('evidence', type=Path)
    args = parser.parse_args()
    if args.command == 'run':
        directory, result = run(args.config, args.seconds)
        print(json.dumps({'evidence': str(directory), **{key: result[key] for key in
              ('scope', 'delivery', 'later_live_read', 'collection', 'baseline_retention',
               'intermediate_live_reads', 'overall', 'full_day_acceptance')}}, sort_keys=True))
    else:
        result = replay(args.evidence)
        print(json.dumps(result, sort_keys=True))
    return 0 if result['overall'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
