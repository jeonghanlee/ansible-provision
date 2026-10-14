"""Retain exact deliberate loss and independently compare the remaining real records."""

import argparse
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import threading
import time
import uuid

import basic
import boot_coverage
import journal_coverage as native
import obsolete_anchor
import prepare
import window_coverage as window

DURATION = 900
REMOVAL_WINDOW = (120, 180)


def load(path):
    return json.loads(path.read_text())


def key(row):
    return json.dumps(basic.identity(row))


def since(anchor):
    timestamp = int(anchor['__REALTIME_TIMESTAMP'])
    return datetime.datetime.fromtimestamp(timestamp // 1000000, datetime.timezone.utc).replace(
        microsecond=timestamp % 1000000).strftime('%Y-%m-%d %H:%M:%S.%f UTC')


def required(directory, config):
    direct, _ = basic.direct_records(directory / 'direct')
    indexed = basic.source_index(direct, config)
    outcomes = {}
    for name in ('baseline-outcomes.jsonl', 'outcomes.jsonl'):
        if (directory / name).exists():
            for row in basic.load_rows(directory / name):
                if row['id'] in outcomes:
                    raise RuntimeError('A producer outcome repeats its actual identity')
                outcomes[row['id']] = row
    result = {}
    for name in ('baseline-schedule.jsonl', 'schedule.jsonl'):
        for action in basic.load_rows(directory / name):
            if action['id'] not in outcomes:
                continue
            outcome = outcomes[action['id']]
            matched = basic.required_records(action, outcome, indexed, config)
            if len(matched) != (2 if action['path'] in ('appliance', 'health') else 1):
                raise RuntimeError('An actual executed action lacks its independent direct source set')
            for row in matched:
                identity = key(row)
                if identity in result:
                    raise RuntimeError('Different producer actions claim the same actual required record')
                result[identity] = {'action_id': action['id'], 'path': action['path'], 'record': row}
    return result


def declare(directory, start):
    (directory / 'loss').mkdir(mode=0o700)
    prepare.save(directory / 'loss/contract.json', {'scope': 'actual-required-record-loss', 'start': start,
                 'duration_seconds': DURATION, 'removal_window_seconds': list(REMOVAL_WINDOW),
                 'first_collection_seconds': basic.COLLECTION_PERIOD,
                 'lost_ids_source': 'independent actual producer outcomes and direct journal records',
                 'complete_collection_expected': False, 'lost_ids_remain_required': True,
                 'post_loss_archive_mode': 'actual partial native capture without complete coverage'})


def ensure_producer_declaration(due, confirmed):
    recorded = {entry['action_id'] for entry in confirmed.values()}
    if not set(due) <= recorded:
        raise RuntimeError('Pre-removal producer declaration omitted actions due before closure')


class Remove:
    """Freeze actual required identities, copy one closed file and remove that file only."""

    def __init__(self, directory, config, start, stopping):
        self.root, self.config, self.start, self.stopping = directory, config, start, stopping
        self.error = None

    def run(self):
        import long
        destination = self.root / 'loss'
        try:
            while time.monotonic_ns() < self.start['monotonic_ns'] + REMOVAL_WINDOW[0] * 1_000_000_000:
                if self.stopping.wait(.05):
                    raise RuntimeError('The actual required-loss action was interrupted')
            baseline = load(self.root / 'baseline.json')
            probe = next(item['record'] for entry in baseline['actions'] for item in entry['records']
                         if item['record'].get('SYSLOG_IDENTIFIER') == basic.TAG)
            before = native.file_headers()
            prepare.save(destination / 'files-before.json', before)
            rotated = basic.command(['journalctl', '--rotate'], destination / 'rotate')
            if rotated.get('returncode') != 0:
                raise RuntimeError('The actual loss candidate could not be rotated')
            candidates = []
            for number, header in enumerate(native.file_headers()):
                stream, sequence = native.coordinates(probe, probe['_BOOT_ID'])
                if (not header['file'].startswith('system@') or not header['entries']
                        or header['boot_id'] != probe['_BOOT_ID'] or header['sequence_id'] != stream
                        or not header['first_sequence'] <= sequence <= header['last_sequence']):
                    continue
                path = next(native.JOURNAL_ROOT.glob('*/' + header['file']))
                actual = native.query(['--file', str(path), '--cursor', probe['__CURSOR'], '--lines=1'],
                                      destination / ('probe-' + str(number) + '.jsonl'))
                if actual == [probe]:
                    candidates.append(path)
            if len(candidates) != 1:
                raise RuntimeError('One actual closed journal file containing required records was not established')
            candidate = candidates[0]
            assert not candidate.is_symlink() and candidate.resolve().parent.parent == native.JOURNAL_ROOT.resolve()
            closed = obsolete_anchor.closed_file(candidate, destination / 'closed')
            rows = native.query(['--file', str(candidate)], destination / 'candidate-records.jsonl')
            stored = {key(row): row for row in rows}
            cutoff = closed['finished']['monotonic_ns']
            due = {row['id'] for name in ('baseline-schedule.jsonl', 'schedule.jsonl')
                   for row in basic.load_rows(self.root / name) if row['planned_monotonic_ns'] <= cutoff}
            deadline = self.start['monotonic_ns'] + REMOVAL_WINDOW[1] * 1_000_000_000
            while True:
                recorded = {row['id'] for name in ('baseline-outcomes.jsonl', 'outcomes.jsonl')
                            for row in basic.load_rows(self.root / name)}
                if not due <= recorded:
                    if time.monotonic_ns() >= deadline:
                        raise RuntimeError('Not every action due before file closure has its actual producer outcome')
                    self.stopping.wait(.1)
                    continue
                try:
                    confirmed = required(self.root, self.config)
                except (RuntimeError, ValueError):
                    if time.monotonic_ns() >= deadline:
                        raise
                    self.stopping.wait(.1)
                    continue
                queries = basic.load_rows(self.root / 'direct/queries.jsonl')
                tail_path = self.root / 'direct' / queries[-1]['file']
                live_tail = basic.load_rows(tail_path)
                if live_tail and key(live_tail[-1]) not in stored and queries[-1]['started']['monotonic_ns'] > rotated['finished']['monotonic_ns']:
                    ensure_producer_declaration(due, confirmed)
                    break
                if time.monotonic_ns() >= deadline:
                    raise RuntimeError('The direct reader did not advance beyond the rotated candidate before removal')
                self.stopping.wait(.1)
            lost = {identity: entry for identity, entry in confirmed.items() if identity in stored}
            if not lost or any(stored[identity] != entry['record'] for identity, entry in lost.items()):
                raise RuntimeError('The predeclared lost set is empty or differs from the actual closed file')
            if list((self.root / 'collector').glob('interval-*')):
                raise RuntimeError('A required loss candidate was already collected')
            snapshots = {}
            for name in ('baseline-outcomes.jsonl', 'outcomes.jsonl'):
                snapshot = destination / ('before-removal-' + name)
                snapshot.write_bytes((self.root / name).read_bytes())
                snapshots[snapshot.name] = window.digest(snapshot)
            query_snapshot = destination / 'before-removal-direct-queries.jsonl'
            query_snapshot.write_bytes((self.root / 'direct/queries.jsonl').read_bytes())
            snapshots[query_snapshot.name] = window.digest(query_snapshot)
            original_hash = window.digest(candidate)
            copy = destination / 'preserved-required.journal'
            shutil.copy2(candidate, copy)
            copy.chmod(0o600)
            if window.digest(copy) != original_hash:
                raise RuntimeError('The preserved actual required file is not byte-identical')
            metadata = candidate.stat()
            plan = {'observed': basic.clock(), 'target': str(candidate.resolve()), 'sha256': original_hash,
                    'inode': metadata.st_ino, 'device': metadata.st_dev, 'copy_sha256': window.digest(copy),
                    'closed_header': closed['header_after'], 'lost_required_records': lost,
                    'confirmed_required_records_before_removal': confirmed, 'previous_collections': 0,
                    'producer_cutoff_monotonic_ns': cutoff, 'due_before_closure_action_ids': sorted(due),
                    'actual_pre_removal_ledger_snapshots_sha256': snapshots,
                    'original_collector_window': load(self.root / 'restart-window.json')['entry']}
            prepare.save(destination / 'removal-plan.json', plan)
            obsolete_anchor.closed_file(candidate, destination / 'before-removal')
            if window.digest(candidate) != original_hash or time.monotonic_ns() >= deadline:
                raise RuntimeError('The exact closed required file changed or removal exceeded its declared window')
            started = basic.clock()
            candidate.unlink()
            finished = basic.clock()
            anchor = load(self.root / 'restart-window.json')['entry']
            post = destination / 'post-loss-live.jsonl'
            long.query(self.config, anchor['_BOOT_ID'], {'since': since(anchor)}, post)
            long.checked_query(post)
            remaining = {key(row): row for row in long.rows(post)}
            if set(lost) & remaining.keys():
                raise RuntimeError('A predeclared lost identity is still present after the actual removal')
            if any(remaining.get(identity) != entry['record'] for identity, entry in confirmed.items() if identity not in lost):
                raise RuntimeError('The removal affected another confirmed required record')
            prepare.save(destination / 'action.json', {'started': started, 'finished': finished,
                         'target_absent': not candidate.exists(), 'successful_post_loss_query': True,
                         'exact_predeclared_absence': True, 'removed_required_records': len(lost),
                         'collector_window_unchanged': load(self.root / 'restart-window.json')['entry'] == anchor})
        except Exception as error:
            self.error = str(error)
            prepare.save(destination / 'error.json', {'observed': basic.clock(), 'error': self.error})


class Collector:
    """Retain actual native refusal and collect remaining rows with explicit incomplete coverage."""

    def __init__(self, directory, anchor, context):
        self.root, self.anchor, self.context = directory, anchor, context
        self.stopping = threading.Event()
        self.error = None
        self.previous, self.seen = {}, {}

    def run(self):
        try:
            number = 0
            while True:
                terminal = self.stopping.wait(basic.COLLECTION_PERIOD)
                destination = self.root / 'collector' / ('interval-' + str(number))
                destination.mkdir(mode=0o700)
                attempt = destination / 'native'
                attempt.mkdir(mode=0o700)
                prepare.save(destination / 'input-state.json', self.previous)
                started = basic.clock()
                refusal = None
                try:
                    complete = boot_coverage.collect(attempt, self.previous, datetime.datetime.now(datetime.timezone.utc),
                                                     self.anchor, self.context)
                    prepare.save(attempt / 'result.json', complete)
                    raise RuntimeError('The real collector claimed complete coverage after required loss')
                except RuntimeError as error:
                    refusal = str(error)
                    prepare.save(attempt / 'actual-refusal.json', {'observed': basic.clock(), 'error': refusal})
                marker = uuid.uuid4().hex
                emitted = basic.command(['logger', '--tag', native.MARKER_TAG, '--', marker], destination / 'terminal-emission')
                if emitted.get('returncode') != 0:
                    raise RuntimeError('A real partial collection checkpoint could not be emitted')
                tail, attempts = native.terminal_checkpoint(destination, self.anchor['_BOOT_ID'], marker)
                end = since(tail)
                partial = native.query(['-b', self.anchor['_BOOT_ID'], '--since', since(self.anchor), '--until', end],
                                       destination / 'partial-source.jsonl')
                selected = []
                for row in partial:
                    identity = key(row)
                    if identity in self.seen:
                        if self.seen[identity] != row:
                            raise RuntimeError('A partial native capture changed an earlier actual identity')
                    else:
                        self.seen[identity] = row
                        selected.append(row)
                (destination / 'archive-new.jsonl').write_text(''.join(json.dumps(row, sort_keys=True) + '\n' for row in selected))
                prepare.save(destination / 'result.json', {'started': started, 'finished': basic.clock(),
                             'coverage_complete': False, 'actual_native_refusal': refusal,
                             'source_sha256': window.digest(destination / 'partial-source.jsonl'),
                             'archive_sha256': window.digest(destination / 'archive-new.jsonl'),
                             'original_checkpoint_unchanged': self.previous == {},
                             'partial_source_records': len(partial), 'actual_unique_new_records': len(selected),
                             'actual_terminal_entry': tail, 'checkpoint_attempts': attempts})
                number += 1
                if terminal:
                    return
        except Exception as error:
            self.error = str(error)
            prepare.save(self.root / 'collector/error.json', {'observed': basic.clock(), 'error': self.error})


def replay(directory, publish=False):
    import long
    result = {'scope': 'journal-actual-required-loss', 'overall': 'Incomplete', 'delivery': 'Incomplete',
              'later_live_read': 'Incomplete', 'collection': 'Incomplete', 'baseline_retention': 'Incomplete',
              'intermediate_live_reads': 'Incomplete', 'full_day_acceptance': 'Pending',
              'loss_detection_expectation': 'Incomplete', 'violations': [], 'unresolved': []}
    try:
        if long.inventory(directory) != load(directory / 'artifact-index.json'):
            raise RuntimeError('The original actual-loss evidence changed')
        prepare.verify(directory / 'package')
        for module in (basic, long, native, boot_coverage, window, obsolete_anchor):
            if window.digest(Path(module.__file__)) != window.digest(directory / 'package' / Path(module.__file__).name):
                raise RuntimeError('Actual-loss replay requires its original frozen helper modules')
        if window.digest(Path(__file__)) != window.digest(directory / 'package/loss.py'):
            raise RuntimeError('Actual-loss replay requires its original frozen loss code')
        standard, contract = load(directory / 'contract.json'), load(directory / 'loss/contract.json')
        state, config = load(directory / 'observation.json'), load(directory / 'package/config.json')
        if (state['state'] != 'Finished' or standard['scenario'] != 'actual-loss'
                or standard['duration_seconds'] != DURATION or standard['periods_seconds'] != basic.PERIODS
                or standard['collection_seconds'] != 300 or contract['removal_window_seconds'] != list(REMOVAL_WINDOW)
                or not contract['lost_ids_remain_required'] or state['errors']):
            raise RuntimeError('The full actual-loss contract or source operation was not established')
        for name, expected in standard['schedules_sha256'].items():
            if window.digest(directory / name) != expected:
                raise RuntimeError('An independent producer schedule changed')
        if window.digest(directory / 'baseline.json') != standard['baseline_sha256']:
            raise RuntimeError('The original independent baseline changed')
        for name in ('baseline', ''):
            prefix = name + '-' if name else ''
            schedule = basic.load_rows(directory / (prefix + 'schedule.jsonl'))
            outcomes = basic.load_rows(directory / (prefix + 'outcomes.jsonl'))
            if {row['id'] for row in schedule} != {row['id'] for row in outcomes} or len(schedule) != len(outcomes):
                raise RuntimeError('An actual producer schedule was not fully executed')
            if any(not row.get('executed') for row in outcomes):
                raise RuntimeError('An unrelated producer failed in the actual-loss scenario')
            indexed_outcomes = {row['id']: row for row in outcomes}
            if any(indexed_outcomes[row['id']]['started']['monotonic_ns'] < row['planned_monotonic_ns'] for row in schedule):
                raise RuntimeError('An actual producer action started before its independently frozen schedule')
            for path, period in basic.PERIODS.items():
                sequences = [row['sequence'] for row in schedule if row['path'] == path]
                if sequences != ([0] if name else basic.scheduled_sequences(DURATION, period)):
                    raise RuntimeError('The actual-loss producer frequencies changed')
        all_required = required(directory, config)
        baseline = load(directory / 'baseline.json')
        baseline_ids = {key(item['record']) for entry in baseline['actions'] for item in entry['records']}
        if any(item['first_confirmed']['monotonic_ns'] > standard['start']['monotonic_ns']
               for entry in baseline['actions'] for item in entry['records']):
            raise RuntimeError('An actual baseline was not directly confirmed before t0')
        plan, action = load(directory / 'loss/removal-plan.json'), load(directory / 'loss/action.json')
        closed = load(directory / 'loss/closed/closed-file-proof.json')['attempts'][-1]
        cutoff = closed['finished']['monotonic_ns']
        if plan['producer_cutoff_monotonic_ns'] != cutoff:
            raise RuntimeError('The producer completion boundary differs from actual closed-file proof')
        due_actions = {row['id']: row for name in ('baseline-schedule.jsonl', 'schedule.jsonl')
                       for row in basic.load_rows(directory / name) if row['planned_monotonic_ns'] <= cutoff}
        if plan['due_before_closure_action_ids'] != sorted(due_actions):
            raise RuntimeError('The pre-removal producer boundary omitted independently scheduled actions')
        for name, digest in plan['actual_pre_removal_ledger_snapshots_sha256'].items():
            if Path(name).name != name or window.digest(directory / 'loss' / name) != digest:
                raise RuntimeError('An actual pre-removal producer or direct-query ledger snapshot changed')
        pre_outcomes = {}
        for name in ('baseline-outcomes.jsonl', 'outcomes.jsonl'):
            current = {row['id']: row for row in basic.load_rows(directory / name)}
            for row in basic.load_rows(directory / 'loss' / ('before-removal-' + name)):
                if row['id'] in pre_outcomes or current.get(row['id']) != row:
                    raise RuntimeError('An actual pre-removal producer outcome differs from its original final ledger')
                pre_outcomes[row['id']] = row
        if not due_actions.keys() <= pre_outcomes.keys():
            raise RuntimeError('The lost-ID set was frozen before all due producer outcomes were recorded')
        pre_records = {}
        for entry in basic.load_rows(directory / 'loss/before-removal-direct-queries.jsonl'):
            path = directory / 'direct' / entry['file']
            if (window.digest(path) != entry['sha256']
                    or entry['finished']['monotonic_ns'] > plan['observed']['monotonic_ns']):
                raise RuntimeError('A pre-removal direct-query snapshot changed or occurred after the loss plan')
            for row in window.load_query(path):
                pre_records[basic.identity(row)] = row
        pre_index = basic.source_index(pre_records, config)
        independently_confirmed = {}
        for identity, scheduled in due_actions.items():
            matched = basic.required_records(scheduled, pre_outcomes[identity], pre_index, config)
            if len(matched) != (2 if scheduled['path'] in ('appliance', 'health') else 1):
                raise RuntimeError('An action due before closure lacks its actual pre-removal direct confirmation')
            for row in matched:
                independently_confirmed[key(row)] = {'action_id': identity, 'path': scheduled['path'], 'record': row}
        if window.digest(directory / 'loss/preserved-required.journal') != plan['copy_sha256'] or plan['sha256'] != plan['copy_sha256']:
            raise RuntimeError('The actual closed required file copy changed')
        candidate = {key(row): row for row in window.load_query(directory / 'loss/candidate-records.jsonl')}
        lost = plan['lost_required_records']
        exact = {identity: entry for identity, entry in all_required.items() if identity in candidate}
        pre_exact = {identity: entry for identity, entry in independently_confirmed.items() if identity in candidate}
        if pre_exact != lost:
            raise RuntimeError('The lost-ID declaration does not match the completed original pre-removal producer evidence')
        if not lost or lost != exact or plan['previous_collections'] != 0:
            raise RuntimeError('The actual required missing identities differ from the predeclared original set')
        for name in ('closed', 'before-removal'):
            proof = load(directory / 'loss' / name / 'closed-file-proof.json')
            tail = proof['attempts'][-1]
            if (not proof['closed'] or not tail['stable'] or tail['descriptor_matches'] or tail['mapping_matches']
                    or tail['header_before'] != tail['header_after'] or tail['header_after'] != plan['closed_header']):
                raise RuntimeError('The actual required file was not closed at both copy and removal')
        start = standard['start']['monotonic_ns']
        if not start + 120_000_000_000 <= action['started']['monotonic_ns'] <= action['finished']['monotonic_ns'] <= start + 180_000_000_000:
            raise RuntimeError('The actual removal missed its declared pre-collection window')
        if not action['target_absent'] or not action['collector_window_unchanged']:
            raise RuntimeError('The real removal or unchanged collector boundary is unproved')
        post = {key(row): row for row in window.load_query(directory / 'loss/post-loss-live.jsonl')}
        confirmed = plan['confirmed_required_records_before_removal']
        if (set(lost) & post.keys() or any(post.get(identity) != entry['record']
                for identity, entry in confirmed.items() if identity not in lost)):
            raise RuntimeError('The successful immediate query did not show exactly the predeclared loss')
        final = {key(row): row for row in window.load_query(directory / 'final-live.jsonl')}
        for number, offset in enumerate(standard['checkpoint_offsets_seconds']):
            path = directory / 'checkpoints' / ('checkpoint-' + str(number) + '.jsonl')
            receipt = long.checked_query(path)
            if receipt['started']['monotonic_ns'] < start + offset * 1_000_000_000:
                raise RuntimeError('An actual intermediate query preceded its declared boundary')
            actual = {key(row): row for row in basic.load_rows(path)}
            cutoff = native.timestamp(receipt['started']['utc']) - basic.VISIBILITY_WAIT * 1_000_000
            eligible = {identity: entry for identity, entry in all_required.items()
                        if int(entry['record']['__REALTIME_TIMESTAMP']) <= cutoff}
            if ({identity for identity in eligible if identity not in actual} != set(eligible) & set(lost)
                    or any(actual.get(identity) != entry['record'] for identity, entry in eligible.items() if identity not in lost)):
                raise RuntimeError('An actual intermediate query does not reproduce exactly the expected loss')
        intervals = sorted((directory / 'collector').glob('interval-*'))
        archived = {}
        if len(intervals) < 4:
            raise RuntimeError('The scheduled native intervals and final capture were not completed')
        for interval in intervals:
            proof = load(interval / 'result.json')
            if (proof['coverage_complete'] or not proof['original_checkpoint_unchanged']
                    or load(interval / 'input-state.json') != {}
                    or load(interval / 'native/original-input-state.json') != {}
                    or proof['actual_native_refusal'] != 'The declared current-boot window is not actually readable and root-owned'
                    or window.digest(interval / 'partial-source.jsonl') != proof['source_sha256']
                    or window.digest(interval / 'archive-new.jsonl') != proof['archive_sha256']):
                raise RuntimeError('The real collector refusal or partial archive evidence changed')
            partial = {key(row): row for row in window.load_query(interval / 'partial-source.jsonl')}
            queried = window.load_query(interval / 'native/required-window-anchor.jsonl')
            if queried == [plan['original_collector_window']]:
                raise RuntimeError('The real native refusal contradicts its actual required-window query')
            for row in basic.load_rows(interval / 'archive-new.jsonl'):
                identity = key(row)
                if identity in archived or partial.get(identity) != row:
                    raise RuntimeError('The actual partial archive repeated or changed a real source identity')
                archived[identity] = row
        missing_live = {identity for identity in all_required if identity not in final}
        missing_archive = {identity for identity in all_required if identity not in archived}
        if missing_live != set(lost) or missing_archive != set(lost):
            raise RuntimeError('The final missing record sets differ from the exact predeclared original identities')
        comparisons = []
        for identity, entry in sorted(all_required.items()):
            absent = identity in lost
            if not absent and (final.get(identity) != entry['record'] or archived.get(identity) != entry['record']):
                raise RuntimeError('A remaining required record changed in live storage or the actual archive')
            comparisons.append({'identity': json.loads(identity), 'action_id': entry['action_id'], 'path': entry['path'],
                                'required_before_and_after_loss': True, 'predeclared_missing': absent,
                                'live_present': identity in final, 'archive_present': identity in archived})
        encoded = ''.join(json.dumps(row, sort_keys=True) + '\n' for row in comparisons).encode()
        if publish:
            (directory / 'comparisons.jsonl').write_bytes(encoded)
        elif (directory / 'comparisons.jsonl').read_bytes() != encoded:
            raise RuntimeError('The replayed per-record missing comparisons differ from the originals')
        elapsed = (state['ended']['monotonic_ns'] - start) / 1e9
        utc_elapsed = (datetime.datetime.fromisoformat(state['ended']['utc']) - datetime.datetime.fromisoformat(standard['start']['utc'])).total_seconds()
        if elapsed < 960 or utc_elapsed < 960 or state['start_boot'] != state['end_boot'] or state['start_daemon'] != state['end_daemon']:
            raise RuntimeError('The full 900-second recording, final allowance or stable live identity is unproved')
        result.update(overall='Failed', delivery='Passed', later_live_read='Failed', collection='Failed',
                      baseline_retention='Failed' if baseline_ids & set(lost) else 'Passed',
                      intermediate_live_reads='Failed', loss_detection_expectation='Passed',
                      actual_required_records=len(all_required), exact_predeclared_missing_records=len(lost),
                      remaining_required_records_preserved=len(all_required) - len(lost),
                      complete_coverage_refused=True, missing_ids_remain_required=True,
                      planned_seconds=DURATION, actual_elapsed_seconds=elapsed, utc_elapsed_seconds=utc_elapsed,
                      comparisons_sha256=prepare.digest(encoded), native_collector_intervals=len(intervals),
                      violations=['Exactly the predeclared required records are absent from live storage and archive'])
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        result['unresolved'].append(str(error))
    return result


def main():
    import long
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('run', 'replay', 'check-declaration'))
    parser.add_argument('directory', type=Path, nargs='?')
    args = parser.parse_args()
    if args.action == 'check-declaration':
        closed = load(args.directory / 'loss/closed/closed-file-proof.json')['attempts'][-1]
        cutoff = closed['finished']['monotonic_ns']
        due = {row['id'] for name in ('baseline-schedule.jsonl', 'schedule.jsonl')
               for row in basic.load_rows(args.directory / name) if row['planned_monotonic_ns'] <= cutoff}
        ensure_producer_declaration(due, load(args.directory / 'loss/removal-plan.json')['confirmed_required_records_before_removal'])
        print(json.dumps({'scope': 'actual-retained-producer-declaration-only', 'complete_due_action_declaration': True,
                          'runtime_acceptance_established': False}, sort_keys=True))
        return 0
    if args.action == 'run':
        boots = subprocess.check_output(['journalctl', '--list-boots', '--no-pager'], text=True)
        directory, result = long.run(prepare.PREFIX / 'config.json', DURATION, 'actual-loss',
                                    restart_input={'phase': 'before', 'journal_boots': [line.split()[1] for line in boots.splitlines()]})
    else:
        directory = args.directory
        result = replay(directory)
    print(json.dumps({'evidence': str(directory), 'result': result}, sort_keys=True))
    return 0 if result['loss_detection_expectation'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
