#!/usr/bin/env python3
"""Produce deterministic, portable numerical aggregates from retained evidence."""

import argparse
import collections
import datetime
import hashlib
import json
import math
from pathlib import Path
import re

import contract
import evidence
import evaluate

SCHEMA = 1
PRECISION = 6
SECOND = 1000000000
GC_CLASSES = {'G1New': 'young', 'G1Full': 'full', 'G1Old': 'concurrent'}
REQUIRED = ('observation.json', 'state.json', 'samples.csv', 'passes.jsonl',
            'gc-heap.csv', 'gc-collections.csv', 'gc-pauses.csv', 'jstat.csv',
            'processes.csv', 'latency.csv')


def number(value):
    result = float(str(value).replace(',', ''))
    if not math.isfinite(result):
        raise RuntimeError('A finite numerical value is required')
    return result


def statistics(values, unit):
    values = list(values)
    return {'unit': unit, 'count': len(values),
            **{key: round(value, PRECISION) if value is not None else None for key, value in
               (('last', values[-1] if values else None), ('minimum', min(values) if values else None),
                ('maximum', max(values) if values else None),
                ('mean', math.fsum(values) / len(values) if values else None),
                ('total', math.fsum(values) if values else None))}}


def weekly_usage(records, observed_ns):
    today = observed_ns // (SECOND * 86400)
    days = collections.defaultdict(int)
    for row in records:
        ended = evidence.timestamp_ns(row['endedAt'])
        day = ended // (SECOND * 86400)
        if today - 6 <= day <= today and ended <= observed_ns:
            days[day] += int(row['busyMillis'])
    denominator = observed_ns // SECOND - min(days) * 86400 if days else 0
    return {'busy_milliseconds': sum(days.values()), 'denominator_seconds': denominator,
            'percent': round(sum(days.values()) * 100 / (denominator * 1000), PRECISION) if denominator else 0,
            'counted_utc_days': sorted(days)}


def aggregate(out, result=None, evaluate_run=True):
    missing, failures, source_hashes = [], [], {}
    result = {} if result is None else result
    result.update({'schema': SCHEMA, 'numeric_precision_decimal_places': PRECISION,
              'failed_assertions': failures, 'missing_coverage': missing, 'sources_sha256': source_hashes,
              'tool_hashes': {}, 'transitions': {}, 'components': {}, 'event_rates': {}})

    def remember(path):
        relative = str(path.relative_to(out))
        source_hashes[relative] = contract.digest(path)
        return path

    def load(path):
        return evidence.load(remember(path))

    def csv(name):
        remember(out / name)
        return evidence.rows(out, name)

    def capture(label, action):
        try:
            return action()
        except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
            missing.append(label)
            result.setdefault('input_errors', {})[label] = type(error).__name__
            return None

    for name in REQUIRED:
        if not (out / name).is_file():
            missing.append(name)
        else:
            remember(out / name)
    manifest = capture('manifest', lambda: load(out / 'observation.json'))
    terminals = [out / name for name in ('shutdown.json', 'abort.json') if (out / name).is_file()]
    terminal = capture('terminal', lambda: load(terminals[0]) if len(terminals) == 1 else None)
    if not manifest or not terminal:
        missing.append('coherent_manifest_and_terminal')
        return finalize(result)
    if terminal.get('observation') != manifest:
        failures.append('terminal_manifest_mismatch')
    failures.extend(terminal.get('errors', []))
    start, end = evidence.timestamp_ns(manifest['started_at']), evidence.timestamp_ns(manifest['earliest_finish_at'])
    result['window'] = {'started_ns': start, 'ended_ns': end, 'duration_seconds': manifest['duration_seconds'],
                        'half_open': True, 'measurement_schema': manifest.get('measurement_schema')}
    result['load'] = {'fixture_sha256': manifest.get('fixture_sha256'),
                      'fixture_adjustment': manifest.get('fixture_adjustment'),
                      'configuration': manifest.get('configuration'), 'retrieval_workers': 2,
                      'freshness_window_seconds': 30, 'sample_preservation_verified': False}
    # Absolute paths and host identifiers are not aggregate output fields.
    adjustment = result['load']['fixture_adjustment']
    if adjustment:
        result['load']['fixture_adjustment'] = {key: adjustment.get(key) for key in
            ('override_sha256', 'verified_records', 'original_database_sha256')}
    result['tool_hashes'] = manifest.get('tool_hashes', {})
    result['aggregation_tool_hashes'] = contract.bundle_hashes(Path(__file__).parent)
    evaluation = capture('evaluation', lambda: evaluate.evaluate(out, terminal, aggregate_checks=False)) if evaluate_run else None
    if evaluation:
        result['evaluation'] = {key: value for key, value in evaluation.items() if key != 'evidence_error'}
        failures.extend(evaluation['failed_assertions'])
        missing.extend(evaluation['missing_coverage'])

    def inside(row, field='ts'):
        return start <= evidence.timestamp_ns(row[field]) < end

    sample_index = capture('sample_index', lambda: csv('samples.csv')) or []
    for row in sample_index:
        if not inside(row):
            continue
        def check_sample():
            path = evidence.path(out, row['raw_directory']) / 'sample.json'
            sample = load(path)
            if sample['observed_at'] != row['ts'] or len(sample['errors']) != int(row['error_count']):
                failures.append('sample_index_mismatch')
        capture('indexed_sample', check_sample)

    records = capture('pass_records', lambda: evaluate.pass_records(remember(out / 'passes.jsonl'))) or []
    invocation = dict(line.split('=', 1) for line in manifest['unit_before_observation'].splitlines()
                      if '=' in line).get('InvocationID')
    records = [row for row in records if row['invocation_id'] == invocation]
    selected = [row for row in records if inside(row, 'plannedAt')]
    result['passes'] = {'in_window': len(selected),
                        'startup': sum(evidence.timestamp_ns(row['plannedAt']) < start for row in records),
                        'final_capture': sum(evidence.timestamp_ns(row['plannedAt']) >= end for row in records),
                        'final_capture_aborted': sum(evidence.timestamp_ns(row['plannedAt']) >= end and
                                                     row['aborted'] == 'true' for row in records),
                        'shutdown_seconds': round(terminal.get('stop_elapsed_seconds', 0), PRECISION)}
    for transition in (0, 1):
        rows = sorted((row for row in selected if row['transition'] == transition),
                      key=lambda row: evidence.timestamp_ns(row['plannedAt']))
        adjusted = []
        for row in rows:
            began, planned = evidence.timestamp_ns(row['startedAt']), evidence.timestamp_ns(row['plannedAt'])
            blockers = [evidence.timestamp_ns(prior['endedAt']) for prior in records
                        if prior['transition'] < transition and evidence.timestamp_ns(prior['startedAt']) <= began
                        and evidence.timestamp_ns(prior['endedAt']) > planned]
            adjusted.append((began - max([planned, *blockers])) / SECOND)
        result['transitions'][str(transition)] = {
            'pass_count': len(rows), 'busy_seconds': statistics((int(row['busyMillis']) / 1000 for row in rows), 'seconds'),
            'planned_delay_seconds': statistics(((evidence.timestamp_ns(row['startedAt']) -
                evidence.timestamp_ns(row['plannedAt'])) / SECOND for row in rows), 'seconds'),
            'ordering_adjusted_delay_seconds': statistics(adjusted, 'seconds'),
            'overruns': sum(row['overrun'] != 'false' for row in rows),
            'aborted': sum(row['aborted'] != 'false' for row in rows),
            **{field: sum(int(row[field]) for row in rows) for field in
               ('jobsRun', 'jobsFailed', 'jobsAborted', 'jobsSkipped', 'partitionsMoved', 'bytesMoved')},
            'weekly_usage_snapshots': []}

    events, all_events = {}, {}
    result['deduplication'] = {}
    for kind, filename in (('heap', 'gc-heap.csv'), ('collection', 'gc-collections.csv'), ('pause', 'gc-pauses.csv')):
        value = capture('gc_' + kind, lambda: evidence.deduplicate(csv(filename), kind))
        if value:
            events[kind], result['deduplication'][kind] = value
            all_events[kind] = events[kind]
            events[kind] = [row for row in events[kind] if inside(row)]
    processes = capture('processes', lambda: csv('processes.csv')) or []
    jstat = capture('jstat', lambda: csv('jstat.csv')) or []
    result['gc_reconciliation'] = {}
    for component in evidence.COMPONENTS:
        identity = manifest.get('jvm_identity', {}).get(component, {})
        heaps = [row for row in events.get('heap', []) if row['component'] == component]
        collections_rows = [row for row in events.get('collection', []) if row['component'] == component]
        pauses = [row for row in events.get('pause', []) if row['component'] == component]
        process = [row for row in processes if row['name'] == component and inside(row)]
        stats = sorted((row for row in jstat if row['component'] == component and inside(row)), key=lambda row: row['ts'])
        all_rows = [*heaps, *collections_rows, *pauses, *process, *stats]
        if not identity or any(str(row['pid']) != str(identity.get('pid')) for row in all_rows) or any(
                int(row['start']) != identity.get('start') for row in process):
            failures.append('jvm_identity_' + component)
        after = sorted((row for row in heaps if row['when'] == 'After GC'), key=lambda row: evidence.timestamp_ns(row['ts']))
        pairs = collections.defaultdict(set)
        for row in all_events.get('heap', []):
            if row['component'] == component:
                pairs[row['gc_id']].add(row['when'])
        if any(pairs[row['gc_id']] != {'Before GC', 'After GC'} for row in heaps):
            missing.append('gc_pairs_' + component)
        if not heaps or not collections_rows or not pauses or not process or len(stats) < 2:
            missing.append('component_samples_' + component)
        gc = {}
        for name in ('young', 'full', 'concurrent'):
            group = [row for row in collections_rows if GC_CLASSES.get(row['name']) == name]
            gc[name] = statistics((evidence.duration_ns(row['duration']) / SECOND for row in group), 'seconds')
        if any(row['name'] not in GC_CLASSES for row in collections_rows):
            missing.append('unknown_gc_class_' + component)
        result['components'][component] = {
            'identity': identity, 'heap_event_bytes': statistics((int(row['heap_bytes']) for row in heaps), 'bytes'),
            'sampled_heap_bytes': statistics((number(row['heap_used_kb']) * 1024 for row in process if row['heap_used_kb']), 'bytes'),
            'post_gc_heap_bytes': statistics((int(row['heap_bytes']) for row in after), 'bytes'),
            'post_gc_endpoint_change_bytes': int(after[-1]['heap_bytes']) - int(after[0]['heap_bytes']) if after else None,
            'post_gc_trend_meaning': 'last minus first observed event; descriptive, not a leak estimate',
            'gc': gc, 'causes': dict(sorted(collections.Counter(row['cause'] for row in collections_rows).items())),
            'pauses': statistics((evidence.duration_ns(row['duration']) / SECOND for row in pauses), 'seconds'),
            'rss_bytes': statistics((number(row['rss_kb']) * 1024 for row in process), 'bytes'),
            'jstat': {field: {'unit': 'seconds' if field.endswith('T') else 'collections',
                'initial': number(stats[0][field]), 'final': number(stats[-1][field]),
                'delta': round(number(stats[-1][field]) - number(stats[0][field]), PRECISION)}
                for field in ('YGC', 'YGCT', 'FGC', 'FGCT', 'CGC', 'CGCT', 'GCT')
                if stats and stats[0].get(field) not in ('', '-') and stats[-1].get(field) not in ('', '-')}}
        for counter, gc_class in (('YGC', 'young'), ('FGC', 'full'), ('CGC', 'concurrent_pauses')):
            if len(stats) < 2:
                continue
            first, last = stats[0], stats[-1]
            low_start = evidence.timestamp_ns(first.get('request_started') or first['ts'])
            high_start = evidence.timestamp_ns(first.get('response_finished') or first['ts'])
            low_end = evidence.timestamp_ns(last.get('request_started') or last['ts'])
            high_end = evidence.timestamp_ns(last.get('response_finished') or last['ts'])
            group = ([row for row in pauses if row['name'] in ('Pause Remark', 'Pause Cleanup')]
                     if counter == 'CGC' else [row for row in collections_rows if GC_CLASSES.get(row['name']) == gc_class])
            def count(left, right):
                return sum(left < evidence.timestamp_ns(row['ts']) and
                           evidence.timestamp_ns(row['ts']) + evidence.duration_ns(row['duration']) <= right for row in group)
            minimum = count(high_start, low_end)
            maximum = sum(evidence.timestamp_ns(row['ts']) + evidence.duration_ns(row['duration']) > low_start and
                          evidence.timestamp_ns(row['ts']) <= high_end for row in group)
            delta = int(number(last[counter]) - number(first[counter]))
            result['gc_reconciliation'][component + '_' + counter] = {
                'jstat_delta': delta, 'jfr_minimum': minimum, 'jfr_maximum': maximum,
                'actual_request_bounds': bool(first.get('request_started') and last.get('response_finished'))}
            if not first.get('request_started') or not last.get('response_finished'):
                missing.append('jstat_request_bounds_' + component)
            elif not minimum <= delta <= maximum:
                failures.append('jstat_jfr_' + component + '_' + counter)

    rate_values = collections.defaultdict(list)
    request_ms, ages, visibility_upper, visibility_lower = [], [], [], []
    full_samples, rate_times, fresh_counts, reported_fresh_counts, request_count = 0, [], [], [], 0
    store_snapshots = []
    for sample_path in sorted((out / 'raw').glob('*/sample.json')):
        sample = capture('raw_sample', lambda: load(sample_path))
        if not sample or not inside(sample, 'observed_at'):
            continue
        failures.extend(error['check'] for error in sample.get('errors', []))
        kind = sample.get('sample_kind') or ('full' if 'expected_pvs' in sample else 'journal')
        if kind != 'full':
            if manifest.get('measurement_schema') == contract.SCHEMA:
                for filename in ('journal.jsonl', 'health-journal.jsonl', 'kernel-journal.jsonl'):
                    capture(filename + '_coverage', lambda: remember(sample_path.parent / filename))
            continue
        full_samples += 1
        raw = sample_path.parent
        store_snapshots.append({'observed_ns': evidence.timestamp_ns(sample['observed_at']),
                                'stores': sample.get('stores'), 'available_bytes': sample.get('disk', {}).get('available_bytes')})
        if manifest.get('measurement_schema') == contract.SCHEMA:
            for filename in ('journal.jsonl', 'health-journal.jsonl', 'kernel-journal.jsonl'):
                capture(filename + '_coverage', lambda: remember(raw / filename))
        metrics = capture('metrics', lambda: load(raw / 'metrics.json')) or []
        observed_ns = evidence.timestamp_ns(sample.get('metrics_observed_at', sample['observed_at']))
        rates = capture('rate_semantics', lambda: __import__('collect').event_rates(metrics, sample.get('metrics_observed_at', sample['observed_at'])))
        if rates and start <= observed_ns < end:
            rate_times.append(observed_ns)
            for row in rates:
                key = row['source'] + ':' + row['name']
                rate_values[key].append(row)
        for transition in (0, 1):
            name = 'Weekly usage in ETL(' + str(transition) + '&raquo;' + str(transition + 1) + ') (%)'
            metric = next((row for row in metrics if row['name'] == name), None)
            weekly = weekly_usage([row for row in records if row['transition'] == transition], observed_ns)
            weekly['observed_ns'] = observed_ns
            weekly['reported_percent'] = number(metric['value']) if metric else None
            result['transitions'][str(transition)]['weekly_usage_snapshots'].append(weekly)
            if metric is None:
                missing.append('weekly_usage_metric')
            elif abs(weekly['reported_percent'] - weekly['percent']) > 0.005001:
                failures.append('weekly_usage_reconciliation')
        freshness = capture('freshness', lambda: load(raw / 'freshness.json')) or []
        probes = capture('visibility', lambda: load(raw / 'visibility.json')) or []
        request_count += len(freshness) + sum(len(row.get('attempts', [])) for row in probes)
        reported_fresh_counts.append(sum(row.get('outcome') == 'observed' for row in freshness))
        def recent(row):
            if row.get('outcome') != 'observed' or row.get('latest_secs') is None:
                return False
            instant = int(row['latest_secs']) * SECOND + int(row['latest_nanos'])
            query_end = evidence.timestamp_ns(row.get('query_end') or row['request_started'])
            query_start = evidence.timestamp_ns(row['query_start']) if row.get('query_start') else query_end - 30 * SECOND
            return query_start <= instant <= query_end
        fresh_counts.append(sum(recent(row) for row in freshness))
        request_ms.extend(number(row['duration_ms']) for row in freshness if 'duration_ms' in row)
        ages.extend(number(row['sample_age_seconds']) for row in freshness if row.get('sample_age_seconds') is not None)
        visibility_upper.extend(number(row['visibility_upper_seconds']) for row in probes if row.get('outcome') == 'visible')
        visibility_lower.extend(number(row['visibility_lower_seconds']) for row in probes if row.get('outcome') == 'visible')
        if len(freshness) != 903 or len({row['pv'] for row in freshness}) != 903:
            missing.append('freshness_population')
        if fresh_counts[-1] != 903 or any(row.get('outcome') != 'visible' for row in probes):
            failures.append('retrieval_outcomes')
        if len(probes) != 6:
            missing.append('visibility_population')
    for key, rows in sorted(rate_values.items()):
        result['event_rates'][key] = {'samples': statistics((row['numeric_value'] for row in rows), rows[0]['unit']),
            **{field: rows[0][field] for field in ('averaging', 'interval', 'meaning', 'source_commit')},
            'mean_method': 'arithmetic mean of sampled cumulative rates', 'time_weighted_mean': None}
    rate_times.sort()
    result['rate_coverage'] = {'full_samples': full_samples, 'rate_samples': len(rate_times),
        'maximum_gap_seconds': round(max((right - left for left, right in
            zip([start, *rate_times], [*rate_times, end])), default=end - start) / SECOND, PRECISION)}
    if len(rate_times) != full_samples or not rate_times or result['rate_coverage']['maximum_gap_seconds'] > evaluate.SAMPLE_GAP_LIMIT:
        missing.append('sampled_rate_coverage')
    result['retrieval'] = {'request_latency': statistics(request_ms, 'milliseconds'),
        'sample_age': statistics(ages, 'seconds'), 'visibility_upper': statistics(visibility_upper, 'seconds'),
        'visibility_lower': statistics(visibility_lower, 'seconds'),
        'all_pv_freshness_counts': fresh_counts, 'full_samples': full_samples,
        'reported_freshness_counts': reported_fresh_counts,
        'historical_query_bound': 'request_started when explicit query bounds were not captured',
        'request_count': request_count, 'workers': 2,
        'visibility_meaning': 'sampled source timestamp visibility bounds; not exact ingestion latency'}
    result['store_snapshots'] = store_snapshots
    if manifest.get('measurement_schema') != contract.SCHEMA:
        missing.append('historical_coverage_contract')
    reconcile_logs(out, manifest, events.get('collection', []), result, remember)
    if manifest.get('measurement_schema') == contract.SCHEMA:
        for component, recording in terminal.get('complete_gc_recordings', {}).items():
            if isinstance(recording, dict) and recording.get('recording_path'):
                capture('complete_jfr_' + component, lambda: remember(evidence.path(out, recording['recording_path'])))
    return finalize(result)


def reconcile_logs(out, manifest, events, result, remember):
    pattern = re.compile(r'GC\((\d+)\) (Pause Young|Pause Full|Concurrent (?:(?:Mark|Undo) )?Cycle).*?([0-9.]+)ms\s*$')
    for component in evidence.COMPONENTS:
        pid = str(manifest.get('jvm_identity', {}).get(component, {}).get('pid', ''))
        files = sorted(out.glob('**/gc-' + pid + '-*.log*')) if pid else []
        ids = collections.defaultdict(set)
        for path in files:
            remember(path)
            for line in path.read_text().splitlines():
                match = pattern.search(line)
                if match:
                    category = 'young' if match[2] == 'Pause Young' else 'full' if match[2] == 'Pause Full' else 'concurrent'
                    ids[category].add(match[1])
        expected = collections.defaultdict(set)
        for row in events:
            if row['component'] == component and row['name'] in GC_CLASSES:
                expected[GC_CLASSES[row['name']]].add(row['gc_id'])
        result['gc_reconciliation'][component + '_logs'] = {category: {'jfr_ids': len(expected[category]),
            'covered_ids': len(expected[category] & ids[category])} for category in ('young', 'full', 'concurrent')}
        if not files:
            result['missing_coverage'].append('gc_logs_' + component)
        elif any(expected[category] - ids[category] for category in expected):
            result['missing_coverage'].append('gc_log_ids_' + component)


def finalize(result):
    result['failed_assertions'] = sorted(set(result['failed_assertions']))
    result['missing_coverage'] = sorted(set(result['missing_coverage']))
    result['verdict'] = 'Incomplete' if result['missing_coverage'] else 'Failed' if result['failed_assertions'] else 'Passed'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--compare', type=Path)
    args = parser.parse_args()
    result = {}
    try:
        result = aggregate(args.input, result)
    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
        result.setdefault('failed_assertions', [])
        result.setdefault('missing_coverage', []).append('malformed_required_input')
        result.update(schema=SCHEMA, input_error=type(error).__name__)
        finalize(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n')
    mismatch = False
    if args.compare:
        try:
            mismatch = json.loads(args.compare.read_text()) != result
        except (OSError, ValueError):
            mismatch = True
    print(json.dumps({'schema': SCHEMA, 'verdict': result['verdict'], 'comparison_mismatch': mismatch}))
    return mismatch or result['verdict'] != 'Passed'


if __name__ == '__main__':
    raise SystemExit(main())
