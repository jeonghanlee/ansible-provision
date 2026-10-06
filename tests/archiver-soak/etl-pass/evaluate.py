#!/usr/bin/env python3
"""Evaluate retained observation evidence without discarding failed assertions."""

import collections
import csv
import datetime
import json
from pathlib import Path
import re
import argparse

import contract
import evidence
import journal_coverage
import journal_retention

PASS = re.compile(r'ETL pass of transition (\d+) cadence (\d+) s: ETLPassRecord\[(.*)\]')
TIMING_TOLERANCE = 5.0
SAMPLE_GAP_LIMIT = contract.SAMPLE_GAP_SECONDS
HEALTH_GAP_LIMIT = 120


def epoch(value):
    value = re.sub(r'(\.\d{6})\d+(?=Z$|[+-]\d\d:\d\d$)', r'\1', value)
    return datetime.datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def pass_records(path):
    seen, records = set(), []
    for line in path.read_text().splitlines():
        entry = json.loads(line)
        cursor = entry['__CURSOR']
        if cursor in seen:
            continue
        seen.add(cursor)
        match = PASS.search(entry['MESSAGE'])
        if not match:
            raise RuntimeError('Unparsed completed ETL pass')
        fields = dict(part.split('=', 1) for part in re.split(r', (?=[a-zA-Z]+=)', match[3]))
        records.append({'transition': int(match[1]), 'cadence': int(match[2]),
                        'invocation_id': entry.get('_SYSTEMD_INVOCATION_ID', ''), **fields})
    return records


def journal_checks(out, manifest, samples, missing, budget_failed):
    prepared = manifest.get('journal_retention')
    if not prepared or prepared.get('tool_hashes') != manifest.get('tool_hashes'):
        missing.append('journal_retention_preparation')
        return
    try:
        checked = journal_retention.validate(out / 'journal-retention-proof.json', Path(__file__).parent,
                                             current=prepared['current'], fresh=False)
        if checked != prepared:
            raise RuntimeError('Manifest retention preparation differs from its actual source calculation')
    except (OSError, KeyError, ValueError, TypeError, RuntimeError):
        missing.append('journal_retention_preparation')
        return
    previous = None
    prior_snapshot = prepared['current']
    peak = dict(prepared['current_budget']['rates_bytes_per_second'])
    for sample in sorted(samples, key=lambda row: epoch(row['observed_at'])):
        raw = evidence.path(out, sample['raw_directory'])
        try:
            proof = json.loads((raw / 'journal-coverage.json').read_text())
            boot = manifest['boot_id'].replace('-', '')
            rows = [json.loads(line) for line in (raw / 'journal-sequence.jsonl').read_text().splitlines()]
            anchor = next(row for row in rows if row['__CURSOR'] == proof['system_anchor'])
            tails = [json.loads(line) for line in (raw / 'system-journal-tail.jsonl').read_text().splitlines()]
            if len(tails) != 1 or tails[0]['__CURSOR'] != proof['system_tail'] or tails[0].get('_UID') != '0':
                raise RuntimeError('Missing system terminal checkpoint')
            marker = json.loads((raw / 'journal-marker.json').read_text())
            if (marker['returncode'] != 0 or not re.fullmatch(r'[0-9a-f]{32}', marker['marker']) or
                    tails[0].get('MESSAGE') != marker['marker'] or
                    tails[0].get('SYSLOG_IDENTIFIER') != journal_coverage.MARKER_TAG):
                raise RuntimeError('Terminal checkpoint differs from the emitted system marker')
            commands = {
                'system-journal-tail.jsonl': ['--system', '-b', boot,
                    'SYSLOG_IDENTIFIER=' + journal_coverage.MARKER_TAG, 'MESSAGE=' + marker['marker']],
                'journal-sequence.jsonl': ['-b', boot, '--cursor', proof['system_anchor'], '--until', proof['through']]}
            if (raw / 'system-journal-initial-anchor.jsonl').exists():
                commands['system-journal-initial-anchor.jsonl'] = ['--system', '-b', boot,
                    '--reverse', '--lines=1', '--until', proof['since']]
                anchors = [json.loads(line) for line in (raw / 'system-journal-initial-anchor.jsonl').read_text().splitlines()]
                if anchors != [anchor]:
                    raise RuntimeError('Initial system anchor differs from its system-only query')
            elif previous is None:
                prior_raw = sorted((out / 'raw').glob('*/journal-coverage.json'))
                if not any(json.loads(path.read_text()).get('system_tail') == proof['system_anchor']
                           and path.parent != raw for path in prior_raw):
                    raise RuntimeError('Initial carried system checkpoint lacks its archived source')
            for name, arguments in commands.items():
                receipt = json.loads((raw / (name + '.receipt.json')).read_text())
                if (receipt['returncode'] != 0 or receipt['stderr'].strip() or
                        receipt['stdout_sha256'] != contract.digest(raw / name) or
                        receipt['command'] != ['journalctl', '--no-pager', '--all', '-o', 'json', *arguments]):
                    raise RuntimeError('Journal query receipt differs from its archived source or required scope')
            interval = journal_coverage.validate_interval(rows, anchor, tails[0], boot)
            required = [row for row in interval if journal_coverage.timestamp(proof['since']) <=
                        int(row['__REALTIME_TIMESTAMP']) <= journal_coverage.timestamp(proof['through'])]
            if not (raw / 'system-journal-initial-anchor.jsonl').exists():
                required = [row for row in required if row['__CURSOR'] != proof['system_anchor']]
            kernel_rows = [row for row in required if row.get('_TRANSPORT') == 'kernel']
            archived_kernel = [json.loads(line) for line in (raw / 'kernel-journal.jsonl').read_text().splitlines()]
            if (kernel_rows != archived_kernel or proof['required_records'] != len(required) or
                    any(any(term in str(row.get('MESSAGE', '')).lower() for term in ('suppressed', 'missed'))
                        for row in required)):
                raise RuntimeError('Required journal rows differ from the archived interval')
            holes = journal_coverage.sequence_holes(interval, boot)
            record = json.loads((raw / 'journal-sequence-accounting.json').read_text())
            accounted = journal_coverage.accounting(record['files'], record['partial_files'], holes)
            if (any(record[key] != value for key, value in accounted.items()) or not accounted['passed'] or
                    record['boot_id'] != boot or proof['sequence_accounting'] != {'boot_id': boot, **accounted} or
                    any(row['boot_id'] != boot for row in record['files'] if row['entries']) or
                    accounted['last_sequence'] < journal_coverage.coordinates(tails[0], boot)[1]):
                raise RuntimeError('Stored journal entries do not account for the interval')
            if (proof['boot_id'] != boot or len(interval) != proof['sequence_records'] or
                    proof['sequence_holes'] != holes or
                    proof['sequence_missing'] != sum(last - first + 1 for first, last in holes) or
                    contract.digest(raw / 'journal-sequence.jsonl') != proof['source_sha256'] or
                    not proof['coverage_complete'] or
                    proof['daemon'] != prepared['current']['daemon'] or
                    proof['sequence_id'] != journal_coverage.coordinates(anchor, boot)[0] or
                    proof['first_sequence'] != journal_coverage.coordinates(anchor, boot)[1] or
                    proof['last_sequence'] != journal_coverage.coordinates(tails[0], boot)[1] or
                    journal_coverage.timestamp(proof['through']) != int(tails[0]['__REALTIME_TIMESTAMP'])):
                raise RuntimeError('Conflicting journal interval proof')
            if previous:
                if (proof['since'] != previous['through'] or proof['system_anchor'] != previous['system_tail'] or
                        proof['daemon'] != previous['daemon']):
                    raise RuntimeError('Journal intervals do not join')
            elif journal_coverage.timestamp(proof['since']) > journal_coverage.timestamp(manifest['started_at']):
                raise RuntimeError('Journal coverage begins after the observation')
            if journal_coverage.timestamp(proof['through']) < journal_coverage.timestamp(sample['observed_at']):
                raise RuntimeError('Journal coverage ends before the sample')
            previous = proof
            snapshot = json.loads((raw / 'journal-retention-snapshot.json').read_text())
            budget = json.loads((raw / 'journal-retention-budget.json').read_text())
            if snapshot['daemon'] != proof['daemon'] or snapshot['boot_id'] != boot:
                raise RuntimeError('Journal coverage and retention identities differ')
            gap = journal_retention.elapsed(prior_snapshot, snapshot)
            peak = journal_retention.bounded_interval(peak, prior_snapshot, snapshot)
            peak = {stream: max(peak[stream], budget['rates_bytes_per_second'][stream]) for stream in peak}
            if any(budget['rates_bytes_per_second'][stream] < peak[stream] for stream in peak):
                raise RuntimeError('Journal rate budget omits a measured higher rate')
            prior_snapshot = snapshot
            recalculated = journal_retention.calculation(snapshot, budget['rates_bytes_per_second'])
            if any(budget.get(key) != value for key, value in recalculated.items() if key != 'passed'):
                raise RuntimeError('Journal retention calculation differs from its inputs')
            if budget.get('actual_gap_seconds') != gap:
                raise RuntimeError('Journal retention gap differs from its actual snapshots')
            terminal_starts = [json.loads((out / name).read_text())['finish_started_at']
                               for name in ('shutdown-started.json', 'abort-started.json') if (out / name).exists()]
            is_terminal = any(epoch(value) <= epoch(sample['observed_at']) for value in terminal_starts)
            gap_limit = recalculated['terminal_gap_seconds' if is_terminal else 'periodic_gap_seconds']
            if budget['passed'] != (recalculated['passed'] and gap <= gap_limit):
                raise RuntimeError('Journal retention verdict differs from its limits')
            if not budget['passed']:
                budget_failed.add(sample['observed_at'])
        except (OSError, StopIteration, KeyError, ValueError, TypeError, RuntimeError):
            missing.append('journal_interval_or_budget_coverage')


def _evaluate(out, terminal, failures):
    manifest = terminal['observation']
    start, end = epoch(manifest['started_at']), epoch(manifest['earliest_finish_at'])
    missing = []
    budget_failed = set()
    duration = manifest.get('duration_seconds')
    configuration = manifest.get('configuration', {})
    try:
        contract.validate_duration(duration)
        if configuration != contract.chain_configuration(configuration.get('chain')):
            failures.append('chain_configuration')
        started = datetime.datetime.fromisoformat(manifest['started_at'])
        ended = datetime.datetime.fromisoformat(manifest['earliest_finish_at'])
        expected_grid = contract.expected_firings(started, ended, configuration)
        if end - start != duration or terminal.get('monotonic_elapsed_seconds', -1) < duration:
            failures.append('observation_duration')
        if epoch(terminal['finish_started_at']) - start < duration:
            failures.append('observation_duration')
        if duration == 86400 and started.astimezone(datetime.timezone.utc).date() == ended.astimezone(datetime.timezone.utc).date():
            failures.append('utc_midnight')
        if manifest.get('expected_firings') != expected_grid:
            failures.append('manifest_schedule')
        if set(manifest.get('tool_hashes', {})) != set(contract.BUNDLE_FILES):
            missing.append('complete_bundle_hashes')
        else:
            try:
                if manifest['tool_hashes'] != contract.verify_bundle(Path(__file__).parent):
                    failures.append('tool_bundle_changed')
            except (OSError, RuntimeError):
                missing.append('installed_bundle_integrity')
        verified = manifest.get('chain_verification', {})
        if verified.get('configuration') != configuration or verified.get('verified_pvs') != 903:
            missing.append('verified_store_configuration')
    except (RuntimeError, KeyError, TypeError, ValueError):
        expected_grid = []
        failures.append('observation_contract')
    if terminal['terminal_kind'] == 'abort':
        missing.append('aborted_observation')
    if not terminal['boot_unchanged']:
        failures.append('boot_changed')
    summaries = [json.loads(path.read_text()) for path in (out / 'raw').glob('*/sample.json')]
    window = sorted((row for row in summaries if start <= epoch(row['observed_at']) <= epoch(terminal['finished_at'])),
                    key=lambda row: row['observed_at'])
    full = [row for row in window if row.get('sample_kind') == 'full']
    for row in window:
        for error in row['errors']:
            if error['check'] == contract.JOURNAL_BUDGET_CHECK:
                budget_failed.add(row['observed_at'])
            else:
                failures.append(error['check'])
        if row.get('sample_kind') == 'full':
            if row.get('latency', {}).get('pvs_with_recent_samples') != 903:
                failures.append('all_pv_freshness')
            if row.get('disk', {}).get('available_bytes', 0) < 2 * 1024 ** 3:
                failures.append('disk_reserve')
    initial_path = evidence.path(out, manifest.get('initial_sample_record', 'initial-sample.json'))
    if not initial_path.exists() or evidence.load(initial_path).get('rc') != 0:
        missing.append('explicit_initial_sample')
    boundaries = [start, *[epoch(row['observed_at']) for row in full], end]
    if not full or any(right - left > SAMPLE_GAP_LIMIT for left, right in zip(boundaries, boundaries[1:])):
        missing.append('full_sample_coverage')
    if not full or epoch(full[0]['observed_at']) - start > 120:
        missing.append('initial_full_sample')
    if not terminal.get('final_full_sample'):
        missing.append('final_full_sample')
    state = json.loads((out / 'state.json').read_text())
    health = sorted((event for event in state.get('health_completed', {}).values()
                     if start <= epoch(event['observed_at']) <= epoch(terminal['finished_at'])),
                    key=lambda event: event['observed_at'])
    health_end = epoch(terminal.get('health_coverage_ended_at', terminal['finished_at']))
    health_times = [start, *[epoch(event['observed_at']) for event in health], health_end]
    if (not health or state.get('health_starts') != len(state.get('health_completed', {})) or
            any(right - left > HEALTH_GAP_LIMIT for left, right in zip(health_times, health_times[1:]))):
        missing.append('health_coverage')
    health_contract = manifest['health_verification']['executions'][-1]['health']
    accepted = {'0', *health_contract.get('SuccessExitStatus', '').split()}
    if any(event['result'] != 'success' or event['exit_code'] != 'exited' or
           event['exit_status'] not in accepted for event in health):
        failures.append('health_invocation')
    records = pass_records(out / 'passes.jsonl')
    invocation = dict(line.split('=', 1) for line in manifest['unit_before_observation'].splitlines()
                      if '=' in line).get('InvocationID')
    if not invocation:
        missing.append('appliance_invocation_identity')
    records = [row for row in records if row['invocation_id'] == invocation]
    expected = {(row['transition'], row['cadence'], epoch(row['planned_at'])) for row in expected_grid}
    actual = collections.Counter((row['transition'], row['cadence'], epoch(row['plannedAt']))
                                 for row in records if start <= epoch(row['plannedAt']) < end)
    absent = expected - actual.keys()
    duplicates = [key for key, count in actual.items() if count != 1]
    unexpected = actual.keys() - expected
    if absent:
        missing.append('scheduled_pass_coverage')
    if duplicates or unexpected:
        failures.append('scheduled_pass_identity')
    for row in records:
        if not start <= epoch(row['plannedAt']) < end:
            continue
        if (row['overrun'] != 'false' or row['aborted'] != 'false' or int(row['pvCount']) != 903 or
                int(row['jobsRun']) != 903 or any(int(row[key]) for key in
                    ('jobsFailed', 'jobsAborted', 'jobsSkipped', 'streamsDeletedForSpace'))):
            failures.append('etl_jobs')
        began, planned = epoch(row['startedAt']), epoch(row['plannedAt'])
        blockers = [prior for prior in records if prior['transition'] < row['transition'] and
                    epoch(prior['startedAt']) <= began and epoch(prior['endedAt']) > planned]
        ready = max([planned, *[epoch(prior['endedAt']) for prior in blockers]])
        if not 0 <= began - ready <= TIMING_TOLERANCE:
            failures.append('etl_timing_or_ordering')
    snapshots = [(row, json.loads(evidence.path(out, row['raw_directory']).joinpath('metrics.json').read_text()))
                 for row in full if evidence.path(out, row['raw_directory']).joinpath('metrics.json').exists()]
    if len(snapshots) != len(full):
        missing.append('metric_snapshot_coverage')
    baseline = json.loads(evidence.path(out, manifest['counter_baseline']).read_text())
    for transition in (0, 1):
        metric = 'Passes so far in ETL(' + str(transition) + '&raquo;' + str(transition + 1) + ')'
        values = [next((int(row['value']) for row in snapshot if row['name'] == metric), None)
                  for snapshot in [baseline, *[value for row, value in snapshots]]]
        if any(value is None for value in values):
            missing.append('metric_counter_coverage')
        elif full and values[-1] - values[0] != sum(row['transition'] == transition for row in records
                if epoch(manifest['baseline_observed_at']) < epoch(row['endedAt']) <= epoch(full[-1]['metrics_observed_at'])):
            failures.append('metric_counter_reconciliation')
        for summary, snapshot in snapshots:
            closed = sorted((row for row in records if row['transition'] == transition and
                             epoch(row['endedAt']) <= epoch(summary['metrics_observed_at'])),
                            key=lambda row: epoch(row['endedAt']))
            if not closed:
                missing.append('metric_pass_record_coverage')
                continue
            label = 'ETL(' + str(transition) + '&raquo;' + str(transition + 1) + ')'
            metrics = {row['name']: row['value'] for row in snapshot}
            if int(metrics.get('Passes so far in ' + label, -1)) != len(closed):
                failures.append('metric_snapshot_counter')
            last = closed[-1]
            for suffix, field in (('PVs', 'pvCount'), ('jobs failed', 'jobsFailed'),
                                  ('jobs aborted', 'jobsAborted'), ('jobs skipped', 'jobsSkipped'),
                                  ('partitions moved', 'partitionsMoved'), ('bytes moved', 'bytesMoved'),
                                  ('max partitions moved by one PV', 'maxPartitionsMovedByOnePv')):
                value = metrics.get('Last pass in ' + label + ' ' + suffix)
                if value is None:
                    missing.append('metric_field_coverage')
                elif int(value) != int(last[field]):
                    failures.append('metric_last_pass')
            for name, expected_value in (
                    ('Last pass in ' + label + ' busy time (s)', int(last['busyMillis']) / 1000),
                    ('Average busy time per pass in ' + label + ' (s)',
                     sum(int(row['busyMillis']) for row in closed) / (1000 * len(closed)))):
                if name not in metrics:
                    missing.append('metric_field_coverage')
                elif abs(float(metrics[name]) - expected_value) > 0.005001:
                    failures.append('metric_busy_time')
    pairs = collections.defaultdict(set)
    window_pairs = set()
    heap, _ = evidence.deduplicate(evidence.rows(out, 'gc-heap.csv'), 'heap')
    collections_rows, _ = evidence.deduplicate(evidence.rows(out, 'gc-collections.csv'), 'collection')
    pauses, _ = evidence.deduplicate(evidence.rows(out, 'gc-pauses.csv'), 'pause')
    for component in evidence.COMPONENTS:
        for label, events in (('heap', heap), ('collections', collections_rows), ('pauses', pauses)):
            if not any(row['component'] == component and start <= epoch(row['ts']) <= epoch(terminal['finished_at']) for row in events):
                missing.append('gc_' + label + '_coverage')
    for row in heap:
        key = (row['component'], row['pid'], row['gc_id'])
        pairs[key].add(row['when'])
        if start <= epoch(row['ts']) <= epoch(terminal['finished_at']):
            window_pairs.add(key)
    incomplete_pairs = sum(pairs[key] != {'Before GC', 'After GC'} for key in window_pairs)
    if incomplete_pairs:
        missing.append('gc_pair_coverage')
    for sample in window:
        journal = evidence.path(out, sample['raw_directory']) / 'journal.jsonl'
        if not journal.exists():
            missing.append('appliance_journal_coverage')
            continue
        for line in journal.read_text().splitlines():
            entry = json.loads(line)
            message = str(entry.get('MESSAGE', '')).lower()
            if any(term in message for term in ('outofmemoryerror', 'killing process', 'sigkill', 'stop-sigterm timed out')):
                failures.append('appliance_oom_or_forced_termination')
    # The complete recordings must be present independently of periodic snapshots.
    if set(terminal.get('complete_gc_recordings', {})) != {'mgmt', 'engine', 'etl', 'retrieval'}:
        missing.append('complete_gc_recordings')
    for component, recording in terminal.get('complete_gc_recordings', {}).items():
        if (not isinstance(recording, dict) or not recording.get('recording_bytes') or
                not recording.get('coverage_complete')):
            missing.append('jfr_recording_coverage')
        else:
            recorded = evidence.path(out, recording['recording_path'])
            if recorded.stat().st_size != recording['recording_bytes'] or contract.digest(recorded) != recording['recording_sha256']:
                failures.append('jfr_recording_integrity')
            for kind, field, events in (('heap', 'heap_events', heap), ('collection', 'collection_events', collections_rows),
                                        ('pause', 'pause_events', pauses)):
                count = sum(row['component'] == component for row in events)
                if count != recording[field]:
                    missing.append('jfr_export_' + kind + '_coverage')
    for sample in window:
        if not sample.get('kernel_journal', {}).get('coverage_complete'):
            missing.append('kernel_journal_coverage')
        if sample.get('sample_kind') == 'full' and not sample.get('event_rates'):
            missing.append('event_rate_coverage')
    journal_checks(out, manifest, window, missing, budget_failed)
    for component in evidence.COMPONENTS:
        if not terminal.get('complete_gc_recordings', {}).get(component, {}).get('gc_logs'):
            missing.append('gc_log_coverage')
    if not terminal.get('required_pass_wait'):
        missing.append('required_pass_wait')
    if not terminal.get('etl_state_before_stop'):
        missing.append('shutdown_work_state')
    verdict = 'Incomplete' if missing else 'Failed' if failures else 'Passed'
    return {'verdict': verdict, 'failed_assertions': sorted(set(failures)), 'journal_budget_failed_samples': len(budget_failed),
            'missing_coverage': sorted(set(missing)), 'full_samples': len(full),
            'health_invocations': len(health), 'expected_passes': len(expected),
            'missing_passes': len(absent), 'duplicate_passes': len(duplicates),
            'unexpected_passes': len(unexpected), 'incomplete_gc_pairs': incomplete_pairs}


def evaluate(out, terminal, aggregate_checks=True):
    schema = terminal.get('observation', {}).get('measurement_schema')
    if schema != contract.SCHEMA:
        return {'verdict': 'Incomplete', 'failed_assertions': list(terminal.get('errors', [])),
                'missing_coverage': ['unsupported_observation_schema']}
    failures = list(terminal.get('errors', []))
    try:
        result = _evaluate(out, terminal, failures)
        if aggregate_checks:
            import aggregate
            numerical = {}
            try:
                numerical = aggregate.aggregate(out, numerical, evaluate_run=False)
            except (OSError, KeyError, ValueError, TypeError, RuntimeError):
                numerical.setdefault('missing_coverage', []).append('numerical_evidence')
            result['failed_assertions'] = sorted(set(result['failed_assertions'] + numerical.get('failed_assertions', [])))
            result['missing_coverage'] = sorted(set(result['missing_coverage'] + numerical.get('missing_coverage', [])))
            result['verdict'] = 'Incomplete' if result['missing_coverage'] else 'Failed' if result['failed_assertions'] else 'Passed'
        return result
    except (OSError, KeyError, ValueError, TypeError, RuntimeError) as error:
        return {'verdict': 'Incomplete', 'failed_assertions': sorted(set(failures)),
                'missing_coverage': ['unreadable_or_conflicting_evidence'],
                'evidence_error': type(error).__name__ + ': ' + str(error)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    paths = [args.input / name for name in ('shutdown.json', 'abort.json') if (args.input / name).is_file()]
    if len(paths) != 1:
        parser.error('Exactly one terminal record is required')
    result = evaluate(args.input, json.loads(paths[0].read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result['verdict'] != 'Passed')
