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

PASS = re.compile(r'ETL pass of transition (\d+) cadence (\d+) s: ETLPassRecord\[(.*)\]')
TIMING_TOLERANCE = 5.0
SAMPLE_GAP_LIMIT = contract.SAMPLE_GAP_SECONDS
HEALTH_GAP_LIMIT = 120
# The scheduler verdict reads only the items that describe the observation contract, the appliance,
# the fixture population, the pass records and the sampler's own coverage, plus the abort-listed
# sample checks of the manifest. Metric, GC, latency, journal and health-journal items stay in the
# overall verdict and are reported beside it; they never decide the scheduler verdict.
SCHEDULER_FAILURES = frozenset((
    'chain_configuration', 'observation_duration', 'utc_midnight', 'manifest_schedule', 'tool_bundle_changed',
    'observation_contract', 'boot_changed', 'all_pv_freshness', 'disk_reserve', 'health_invocation',
    'scheduled_pass_identity', 'etl_jobs', 'etl_timing_or_ordering', 'appliance_oom_or_forced_termination',
    'orderly_stop', 'appliance_not_active_before_stop', 'stop_timeout_unavailable', 'etl_state_before_stop',
    'missing_final_full_sample'))
SCHEDULER_MISSING = frozenset((
    'complete_bundle_hashes', 'installed_bundle_integrity', 'verified_store_configuration', 'aborted_observation',
    'explicit_initial_sample', 'full_sample_coverage', 'initial_full_sample', 'final_full_sample',
    'appliance_invocation_identity', 'scheduled_pass_coverage', 'appliance_journal_coverage', 'required_pass_wait',
    'shutdown_work_state', 'unsupported_observation_schema', 'unreadable_or_conflicting_evidence'))
TERMINAL_SAMPLE_ERRORS = {'final_sample': 'full', 'final_journal': 'journal'}


def abort_checks(manifest):
    return set(manifest.get('abort_policy', {}).get('checks', contract.ABORT_CHECKS))


def scheduler_checks(manifest):
    """The sample checks that decide the scheduler verdict: the contract list plus the recorded abort list."""
    return set(contract.SCHEDULER_CHECKS) | abort_checks(manifest)


def metric_variants(closed, summary):
    """Return the pass lists a metrics snapshot may reflect.

    The appliance reads its counters at an unobservable instant inside the metrics request, so a pass
    that ended between the request start and the response may or may not be counted; both readings
    are accepted and the ambiguity is counted.
    """
    request_start = epoch(summary['metrics_observed_at']) - float(summary.get('metrics_ms') or 0) / 1000
    ambiguous = sum(epoch(row['endedAt']) >= request_start for row in closed)
    return [closed, closed[:len(closed) - ambiguous]] if ambiguous else [closed]


def terminal_sample_failures(terminal, window, checks):
    """Map a failed final collection to the scheduler verdict by the recorded sample's errors, not its name."""
    mapped = []
    finish = epoch(terminal['finish_started_at'])
    for name, kind in TERMINAL_SAMPLE_ERRORS.items():
        if name not in terminal.get('errors', []):
            continue
        samples = [row for row in window if row.get('sample_kind') == kind and epoch(row['observed_at']) >= finish]
        if not samples or any(error.get('check') in checks for row in samples for error in row['errors']):
            mapped.append(name)
    return mapped


def scheduler_result(failures, missing, checks, mapped_terminal=()):
    decisive = SCHEDULER_FAILURES | set(checks)
    failed = sorted({name for name in failures if name in decisive} | set(mapped_terminal))
    absent = sorted({name for name in missing if name in SCHEDULER_MISSING})
    return {'scheduler_verdict': 'Incomplete' if absent else 'Failed' if failed else 'Passed',
            'scheduler_failed_assertions': failed, 'scheduler_missing_coverage': absent,
            'scheduler_checks': sorted(checks)}


def epoch(value):
    value = re.sub(r'(\.\d{6})\d+(?=Z$|[+-]\d\d:\d\d$)', r'\1', value)
    return datetime.datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def pass_records(path):
    seen, records = {}, []
    for line in path.read_text().splitlines():
        entry = json.loads(line)
        cursor = entry['__CURSOR']
        if cursor in seen:
            if seen[cursor] != entry:
                raise RuntimeError('Conflicting ETL evidence at the same source position')
            continue
        seen[cursor] = entry
        match = PASS.search(entry['MESSAGE'])
        if not match:
            raise RuntimeError('Unparsed completed ETL pass')
        fields = dict(part.split('=', 1) for part in re.split(r', (?=[a-zA-Z]+=)', match[3]))
        records.append({'transition': int(match[1]), 'cadence': int(match[2]),
                        'invocation_id': entry.get('_SYSTEMD_INVOCATION_ID', ''), **fields})
    return records


def _evaluate(out, terminal, failures):
    manifest = terminal['observation']
    start, end = epoch(manifest['started_at']), epoch(manifest['earliest_finish_at'])
    missing = []
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
            failures.append(error['check'])
        if row.get('sample_kind') == 'full':
            if row.get('latency', {}).get('pvs_with_recent_samples') != 903:
                failures.append('all_pv_freshness')
            if row.get('disk', {}).get('available_bytes', 0) < 2 * 1024 ** 3:
                failures.append('disk_reserve')
    # The initial sample must have run; its own errors are judged from the sample in the window.
    initial_path = evidence.path(out, manifest.get('initial_sample_record', 'initial-sample.json'))
    if not initial_path.exists():
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
    executions = (manifest.get('health_verification') or {}).get('executions') or [{}]
    health_contract = executions[-1].get('health') or manifest.get('health_contract') or {}
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
    # A start no longer requires a clean readiness sample, so its metrics baseline may be absent:
    # that is missing metric coverage in the overall verdict, never an unreadable evaluation.
    try:
        baseline = json.loads(evidence.path(out, manifest['counter_baseline']).read_text())
        baseline_at = epoch(manifest['baseline_observed_at'])
    except (OSError, KeyError, TypeError, ValueError):
        baseline, baseline_at = None, None
        missing.append('metric_counter_coverage')
    ambiguities = 0
    for transition in (0, 1):
        metric = 'Passes so far in ETL(' + str(transition) + '&raquo;' + str(transition + 1) + ')'
        values = [next((int(row['value']) for row in snapshot if row['name'] == metric), None)
                  for snapshot in [baseline or [], *[value for row, value in snapshots]]]
        if any(value is None for value in values):
            missing.append('metric_counter_coverage')
        elif full and baseline_at is not None:
            ended = sorted((row for row in records if row['transition'] == transition and
                            baseline_at < epoch(row['endedAt']) <= epoch(full[-1]['metrics_observed_at'])),
                           key=lambda row: epoch(row['endedAt']))
            counts = {len(rows) for rows in metric_variants(ended, full[-1])}
            if values[-1] - values[0] not in counts:
                failures.append('metric_counter_reconciliation')
        for summary, snapshot in snapshots:
            closed = sorted((row for row in records if row['transition'] == transition and
                             epoch(row['endedAt']) <= epoch(summary['metrics_observed_at'])),
                            key=lambda row: epoch(row['endedAt']))
            if not closed:
                missing.append('metric_pass_record_coverage')
                continue
            variants = metric_variants(closed, summary)
            ambiguities += len(variants) - 1
            label = 'ETL(' + str(transition) + '&raquo;' + str(transition + 1) + ')'
            metrics = {row['name']: row['value'] for row in snapshot}
            if not any(int(metrics.get('Passes so far in ' + label, -1)) == len(rows) for rows in variants):
                failures.append('metric_snapshot_counter')
            for suffix, field in (('PVs', 'pvCount'), ('jobs failed', 'jobsFailed'),
                                  ('jobs aborted', 'jobsAborted'), ('jobs skipped', 'jobsSkipped'),
                                  ('partitions moved', 'partitionsMoved'), ('bytes moved', 'bytesMoved'),
                                  ('max partitions moved by one PV', 'maxPartitionsMovedByOnePv')):
                value = metrics.get('Last pass in ' + label + ' ' + suffix)
                if value is None:
                    missing.append('metric_field_coverage')
                elif not any(int(value) == int(rows[-1][field]) for rows in variants if rows):
                    failures.append('metric_last_pass')
            for name, expected_values in (
                    ('Last pass in ' + label + ' busy time (s)',
                     [int(rows[-1]['busyMillis']) / 1000 for rows in variants if rows]),
                    ('Average busy time per pass in ' + label + ' (s)',
                     [sum(int(row['busyMillis']) for row in rows) / (1000 * len(rows)) for rows in variants if rows])):
                if name not in metrics:
                    missing.append('metric_field_coverage')
                elif not any(abs(float(metrics[name]) - expected_value) <= 0.005001 for expected_value in expected_values):
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
            message = (str(entry.get('MESSAGE', '')) + '\n' + str(entry.get('EXCEPTION', ''))).lower()
            if any(term in message for term in ('outofmemoryerror', 'killing process', 'sigkill', 'stop-sigterm timed out')):
                failures.append('appliance_oom_or_forced_termination')
    for sample in window:
        if not sample.get('kernel_journal', {}).get('coverage_complete'):
            missing.append('kernel_journal_coverage')
        if sample.get('sample_kind') == 'full' and not sample.get('event_rates'):
            missing.append('event_rate_coverage')
    for component in evidence.COMPONENTS:
        if not terminal.get('complete_gc_recordings', {}).get(component, {}).get('gc_logs'):
            missing.append('gc_log_coverage')
    if not terminal.get('required_pass_wait'):
        missing.append('required_pass_wait')
    if not terminal.get('etl_state_before_stop'):
        missing.append('shutdown_work_state')
    verdict = 'Incomplete' if missing else 'Failed' if failures else 'Passed'
    checks = scheduler_checks(manifest)
    return {'verdict': verdict, 'failed_assertions': sorted(set(failures)),
            'missing_coverage': sorted(set(missing)), 'full_samples': len(full),
            'health_invocations': len(health), 'expected_passes': len(expected),
            'missing_passes': len(absent), 'duplicate_passes': len(duplicates),
            'unexpected_passes': len(unexpected), 'incomplete_gc_pairs': incomplete_pairs,
            'metric_window_ambiguities': ambiguities,
            **scheduler_result(failures, missing, checks, terminal_sample_failures(terminal, window, checks))}


def _evaluate_observation(out, terminal, aggregate_checks=True):
    schema = terminal.get('observation', {}).get('measurement_schema')
    checks = scheduler_checks(terminal.get('observation', {}))
    if schema != contract.SCHEMA:
        failures = list(terminal.get('errors', []))
        return {'verdict': 'Incomplete', 'failed_assertions': failures,
                'missing_coverage': ['unsupported_observation_schema'],
                **scheduler_result(failures, ['unsupported_observation_schema'], checks)}
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
            # Of the aggregate items only the manifest identity of the terminal record is observation contract.
            if 'terminal_manifest_mismatch' in numerical.get('failed_assertions', []):
                result['scheduler_failed_assertions'] = sorted(set(result['scheduler_failed_assertions']) |
                                                               {'terminal_manifest_mismatch'})
                if result['scheduler_verdict'] == 'Passed':
                    result['scheduler_verdict'] = 'Failed'
        return result
    except (OSError, KeyError, ValueError, TypeError, RuntimeError) as error:
        return {'verdict': 'Incomplete', 'failed_assertions': sorted(set(failures)),
                'missing_coverage': ['unreadable_or_conflicting_evidence'],
                'evidence_error': type(error).__name__ + ': ' + str(error),
                **scheduler_result(failures, ['unreadable_or_conflicting_evidence'], checks)}


def evaluate(out, terminal, aggregate_checks=True, recording_result=None, **recording_options):
    recordings = (recording_result if recording_result is not None else
                  evidence.compare_recordings(out, terminal, **recording_options))
    result = _evaluate_observation(out, terminal, aggregate_checks)
    result['jfr_recordings'] = recordings
    result['failed_assertions'] = sorted(set(result['failed_assertions'] + recordings['failed_assertions']))
    result['missing_coverage'] = sorted(set(result['missing_coverage'] + recordings['missing_coverage']))
    result['verdict'] = 'Incomplete' if result['missing_coverage'] else 'Failed' if result['failed_assertions'] else 'Passed'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    evidence.recording_arguments(parser)
    args = parser.parse_args()
    options = evidence.recording_options(args, parser)
    paths = [args.input / name for name in ('shutdown.json', 'abort.json') if (args.input / name).is_file()]
    if len(paths) != 1:
        parser.error('Exactly one terminal record is required')
    terminal = json.loads(paths[0].read_text())
    result = (evidence.compare_recordings(args.input, terminal, **options) if args.recordings_only else
              evaluate(args.input, terminal, **options))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(({'Passed': 0, 'Failed': 1, 'Incomplete': 2}[result['verdict']])
                     if args.recordings_only else result['verdict'] != 'Passed')
