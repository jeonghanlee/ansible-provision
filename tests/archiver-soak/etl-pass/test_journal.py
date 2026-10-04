#!/usr/bin/env python3
"""Check budget arithmetic and parse retained real inputs; live scenarios are separate."""

import datetime
import json
import os
from pathlib import Path
import unittest

import journal_coverage
import journal_retention as retention

REAL_INPUT = os.environ.get('ETL_SOAK_JOURNAL_SEQUENCE')
RETENTION_INPUT = os.environ.get('ETL_SOAK_RETENTION_EVIDENCE')
RUNTIME_INPUT = os.environ.get('ETL_SOAK_RUNTIME_RETENTION_EVIDENCE')
MTIME_INPUT = os.environ.get('ETL_SOAK_MTIME_RETENTION_EVIDENCE')
HOLES_INPUT = os.environ.get('ETL_SOAK_SEQUENCE_HOLE_EVIDENCE')
ACCOUNTING_INPUT = os.environ.get('ETL_SOAK_SEQUENCE_ACCOUNTING_EVIDENCE')
HEADER_INPUT = os.environ.get('ETL_SOAK_JOURNAL_HEADER_EVIDENCE')


class BudgetArithmeticTests(unittest.TestCase):
    def current(self, cap=1024 ** 3, duration=8 * 604800):
        return {'timeouts': dict(zip(retention.TIMEOUT_UNITS, (240, 2700, 2700))),
                'inventory': {}, 'caps': {'file_bytes': 128 * 1024 ** 2,
                'effective_bytes': cap, 'retention_seconds': duration,
                'maximum_files': 100, 'file_seconds': 2629800}}

    def test_retention_horizon_uses_terminal_timeout(self):
        result = retention.calculation(self.current(), {'system': 1000, 'user': 1000})
        self.assertEqual(result['periodic_gap_seconds'], 560)
        self.assertEqual(result['terminal_gap_seconds'], 3020)
        self.assertEqual(result['horizon_seconds'], 6040)
        self.assertEqual(result['required_bytes'], 4 * 128 * 1024 ** 2 + 12080000)
        self.assertTrue(result['passed'])

    def test_byte_and_time_failures_are_independent(self):
        bounds = {'system': 1000, 'user': 1000}
        self.assertFalse(retention.calculation(self.current(cap=1), bounds)['passed'])
        self.assertFalse(retention.calculation(self.current(duration=6039), bounds)['passed'])
        self.assertTrue(retention.calculation(self.current(duration=6040), bounds)['passed'])

    def test_user_retained_bytes_and_allocation_granularity_are_reserved(self):
        current = self.current()
        current['inventory'] = {'user-file': {'stream': 'user', 'bytes': 1,
                                            'allocated_bytes': 256 * 1024 ** 2}}
        result = retention.calculation(current, {'system': 0, 'user': 0})
        self.assertEqual(result['user_retained_bytes'], 256 * 1024 ** 2)
        self.assertEqual(result['file_bytes']['user'], 256 * 1024 ** 2)
        self.assertEqual(result['required_bytes'], 1024 ** 3)
        self.assertTrue(result['passed'])
        current['caps']['effective_bytes'] -= 1
        self.assertFalse(retention.calculation(current, {'system': 0, 'user': 0})['passed'])

    def test_invalid_rates_and_unbounded_timeouts_refuse_calculation(self):
        for value in (-1, float('inf'), float('nan')):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                retention.calculation(self.current(), {'system': value, 'user': 0})
        for value in (0, float('inf'), float('nan')):
            current = self.current()
            current['timeouts'][retention.TIMEOUT_UNITS[0]] = value
            with self.subTest(timeout=value), self.assertRaises(RuntimeError):
                retention.calculation(current, {'system': 1, 'user': 1})

    def test_file_count_and_rotation_can_refuse_an_otherwise_sufficient_byte_cap(self):
        current = self.current()
        current['caps']['maximum_files'] = 2
        self.assertFalse(retention.calculation(current, {'system': 1, 'user': 1})['passed'])
        current['caps']['maximum_files'] = 100
        current['caps']['file_seconds'] = 60
        self.assertFalse(retention.calculation(current, {'system': 1, 'user': 1})['passed'])

    def test_limit_parsers_reject_ambiguous_or_unbounded_values(self):
        self.assertEqual(retention.byte_size('1G'), 1024 ** 3)
        self.assertEqual(retention.seconds('45min'), 2700)
        self.assertEqual(retention.seconds('8week'), 8 * 604800)
        for value in ('infinity', '-1', 'unknown', '0'):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                retention.seconds(value)
        self.assertEqual(retention.seconds('0', allow_zero=True), 0)

    def test_oversized_retained_files_do_not_reduce_future_rotation_count(self):
        current = self.current()
        current['inventory'] = {'system.journal': {'stream': 'system', 'bytes': 1,
                                                  'allocated_bytes': 256 * 1024 ** 2}}
        result = retention.calculation(current, {'system': 128 * 1024 ** 2 / 6040, 'user': 0})
        self.assertEqual(result['file_bytes']['system'], 256 * 1024 ** 2)
        self.assertEqual(result['required_files'], 4)

    def snapshot(self, seconds, written, user_bytes, boot='b'):
        start = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
        return {'boot_id': boot, 'daemon': 'd', 'policy_sha256': 'p', 'monotonic': seconds,
                'observed_at': (start + datetime.timedelta(seconds=seconds)).isoformat(),
                'write_bytes': written, 'cancelled_write_bytes': 0,
                'inventory': {'system.journal': {'stream': 'system', 'bytes': 8 * 1024 ** 2,
                                                 'allocated_bytes': 8 * 1024 ** 2},
                              'user-1000.journal': {'stream': 'user', 'bytes': user_bytes,
                                                    'allocated_bytes': user_bytes}}}

    def test_shared_counter_is_counted_once_and_short_intervals_are_not_bounds(self):
        first = self.snapshot(0, 0, 8 * 1024 ** 2)
        later = self.snapshot(300, 3000000, 8 * 1024 ** 2 + 3000)
        self.assertEqual(retention.rates(first, later), {'system': 10000, 'user': 10})
        bounds = {'system': 1, 'user': 1}
        self.assertEqual(retention.bounded_interval(bounds, first, later), {'system': 10000, 'user': 10})
        burst = self.snapshot(304, 7000000, 8 * 1024 ** 2 + 3000)
        self.assertEqual(retention.bounded_interval(bounds, later, burst), bounds)
        with self.assertRaises(RuntimeError):
            retention.bounded_interval(bounds, later, self.snapshot(304, 7000000, 0, boot='other'))

    def test_modification_time_alone_is_not_unaccounted_growth(self):
        first = self.snapshot(0, 1000, 8 * 1024 ** 2)
        touched = self.snapshot(1, 1000, 8 * 1024 ** 2)
        touched['inventory']['system.journal']['mtime_ns'] = 1
        self.assertEqual(retention.rates(first, touched), {'system': 0, 'user': 0})
        grown = self.snapshot(1, 1000, 8 * 1024 ** 2 + 4096)
        with self.assertRaisesRegex(RuntimeError, 'lack write accounting'):
            retention.rates(first, grown)

    def test_interval_budget_skips_short_bounds_but_fails_long_gaps(self):
        first = {**self.current(), **self.snapshot(0, 0, 8 * 1024 ** 2)}
        burst = {**self.current(), **self.snapshot(9, 4000000, 8 * 1024 ** 2)}
        bounds = {'system': 1000, 'user': 0}
        self.assertEqual(retention.interval_budget(burst, bounds, first)['rates_bytes_per_second'], bounds)
        late = {**self.current(), **self.snapshot(561, 4000000, 8 * 1024 ** 2)}
        result = retention.interval_budget(late, bounds, first)
        self.assertGreater(result['rates_bytes_per_second']['system'], bounds['system'])
        self.assertFalse(result['passed'])
        self.assertTrue(retention.interval_budget(late, bounds, first, terminal=True)['passed'])

    def journal_file(self, name, first, last, entries):
        return {'file': name, 'first_sequence': first, 'last_sequence': last, 'entries': entries}

    def test_sequence_accounting_starts_at_the_oldest_retained_system_file(self):
        files = [self.journal_file('user-1000@old.journal', 5, 9, 2),
                 self.journal_file('system@a.journal', 20, 59, 38),
                 self.journal_file('system.journal', 60, 99, 39),
                 self.journal_file('user-1000.journal', 10, 100, 9),
                 self.journal_file('user-1001.journal', 0, 0, 0)]
        partial = {'user-1000.journal': {'returned': 9, 'returned_in_range': 4}}
        result = journal_coverage.accounting(files, partial, [[12, 13], [30, 31], [98, 98]])
        self.assertEqual((result['first_sequence'], result['last_sequence'], result['expected_entries']), (20, 100, 81))
        self.assertEqual((result['stored_entries_least'], result['stored_entries_most']), (81, 81))
        self.assertEqual((result['unreturned_in_range'], result['unreturned_outside_range']), (3, 2))
        self.assertFalse(result['passed'])
        self.assertTrue(journal_coverage.accounting(files, partial, [[30, 31], [98, 98]])['passed'])
        files[1]['entries'] -= 1
        self.assertFalse(journal_coverage.accounting(files, partial, [])['passed'])

    def test_unplaced_entries_of_a_partial_file_only_widen_the_accepted_count(self):
        files = [self.journal_file('system.journal', 20, 99, 76),
                 self.journal_file('user-1000.journal', 10, 100, 12)]
        partial = {'user-1000.journal': {'returned': 9, 'returned_in_range': 4}}
        result = journal_coverage.accounting(files, partial, [])
        self.assertEqual((result['stored_entries_least'], result['stored_entries_most']), (80, 83))
        self.assertTrue(result['passed'])
        files[0]['entries'] = 72
        self.assertFalse(journal_coverage.accounting(files, partial, [])['passed'])
        partial['user-1000.journal']['returned'] = 13
        with self.assertRaisesRegex(RuntimeError, 'returns more entries'):
            journal_coverage.accounting(files, partial, [])
        with self.assertRaisesRegex(RuntimeError, 'No retained system journal'):
            journal_coverage.accounting(files[1:], partial, [])

    def test_timestamp_conversion_preserves_microseconds_and_timezone(self):
        self.assertEqual(journal_coverage.timestamp('1970-01-01 00:00:01.000001 UTC'), 1000001)
        self.assertEqual(journal_coverage.timestamp('1970-01-01T01:00:01.000001+01:00'), 1000001)
        with self.assertRaises(RuntimeError):
            journal_coverage.timestamp('1970-01-01T00:00:01')


@unittest.skipUnless(REAL_INPUT, 'Retained actual journal input is required')
class RealJournalInputTests(unittest.TestCase):
    def setUp(self):
        self.rows = [json.loads(line) for line in Path(REAL_INPUT).read_text().splitlines()]
        self.assertTrue(self.rows)
        self.boot = self.rows[0]['_BOOT_ID']

    def test_actual_cursor_coordinates_are_parsed(self):
        for row in self.rows:
            identity, number = journal_coverage.coordinates(row, self.boot)
            self.assertEqual(len(identity), 32)
            self.assertGreater(number, 0)

    def test_other_boot_is_rejected_for_actual_records(self):
        other = '0' * 32 if self.boot != '0' * 32 else '1' * 32
        with self.assertRaisesRegex(RuntimeError, 'boot identity'):
            journal_coverage.coordinates(self.rows[0], other)

    def test_checkpoints_are_required_and_unreturned_numbers_are_counted(self):
        first = journal_coverage.coordinates(self.rows[0], self.boot)[1]
        last = journal_coverage.coordinates(self.rows[-1], self.boot)[1]
        result = journal_coverage.validate_interval(self.rows, self.rows[0], self.rows[-1], self.boot)
        holes = journal_coverage.sequence_holes(result, self.boot)
        missing = sum(end - start + 1 for start, end in holes)
        self.assertEqual(len(result) + missing, last - first + 1)
        for rows in (self.rows[1:], self.rows[:-1]):
            with self.assertRaisesRegex(RuntimeError, 'missing its system checkpoint'):
                journal_coverage.validate_interval(rows, self.rows[0], self.rows[-1], self.boot)
        if len(result) > 2:
            removed = journal_coverage.coordinates(result[1], self.boot)[1]
            shorter = journal_coverage.validate_interval(result[:1] + result[2:], result[0], result[-1], self.boot)
            counted = journal_coverage.sequence_holes(shorter, self.boot)
            self.assertEqual(sum(end - start + 1 for start, end in counted), missing + 1)
            self.assertTrue(any(start <= removed <= end for start, end in counted))


@unittest.skipUnless(HOLES_INPUT, 'A retained actual interval with unreturned sequence numbers is required')
class RealSequenceHoleInputTests(unittest.TestCase):
    def test_actual_interval_with_unreturned_numbers_is_accepted_and_counted(self):
        root = Path(HOLES_INPUT)
        rows = [json.loads(line) for line in (root / 'journal-sequence.jsonl').read_text().splitlines()]
        tail = json.loads((root / 'system-journal-tail.jsonl').read_text())
        boot = tail['_BOOT_ID']
        interval = journal_coverage.validate_interval(rows, rows[0], tail, boot)
        holes = journal_coverage.sequence_holes(interval, boot)
        missing = sum(end - start + 1 for start, end in holes)
        self.assertGreater(missing, 0)
        first = journal_coverage.coordinates(rows[0], boot)[1]
        last = journal_coverage.coordinates(tail, boot)[1]
        self.assertEqual(len(interval) + missing, last - first + 1)
        returned = {journal_coverage.coordinates(row, boot)[1] for row in interval}
        for start, end in holes:
            self.assertFalse(returned & set(range(start, end + 1)))


@unittest.skipUnless(ACCOUNTING_INPUT, 'Retained actual sequence accounting records are required')
class RealSequenceAccountingInputTests(unittest.TestCase):
    def test_actual_journal_files_store_one_entry_per_sequence_number(self):
        records = [json.loads(path.read_text()) for path in sorted(Path(ACCOUNTING_INPUT).glob('*.json'))]
        self.assertTrue(any(len(record['files']) > 2 for record in records))
        for record in records:
            result = journal_coverage.accounting(record['files'], record['partial_files'], [])
            self.assertTrue(result['passed'])
            self.assertEqual(result['stored_entries_least'], result['expected_entries'])
            self.assertEqual({key: record[key] for key in result}, result)
            lost = [dict(row) for row in record['files']]
            newest = max(lost, key=lambda row: row['last_sequence'])
            newest['entries'] -= 1
            self.assertFalse(journal_coverage.accounting(lost, record['partial_files'], [])['passed'])


@unittest.skipUnless(HEADER_INPUT, 'A retained actual journal file and its systemd 239 header listing are required')
class RealJournalHeaderInputTests(unittest.TestCase):
    def test_direct_header_read_matches_the_journalctl_listing(self):
        root = Path(HEADER_INPUT)
        listed = dict(line.split(': ', 1) for line in (root / 'header-239.txt').read_text().splitlines() if ': ' in line)
        row = journal_coverage.read_header(next(root.glob('*.journal')))
        self.assertEqual((row['file_id'], row['boot_id'], row['sequence_id']),
                         (listed['File ID'], listed['Boot ID'], listed['Sequential Number ID']))
        self.assertEqual((row['first_sequence'], row['last_sequence'], row['entries']),
                         (int(listed['Head Sequential Number'].split()[0]),
                          int(listed['Tail Sequential Number'].split()[0]), int(listed['Entry Objects'])))
        self.assertGreater(row['entries'], 0)
        with self.assertRaisesRegex(RuntimeError, 'Unsupported journal file header'):
            journal_coverage.read_header(root / 'header-239.txt')


@unittest.skipUnless(RETENTION_INPUT, 'Retained actual retention snapshots are required')
class RealRetentionInputTests(unittest.TestCase):
    def setUp(self):
        root = Path(RETENTION_INPUT)
        self.samples = [json.loads(path.read_text()) for path in sorted(root.glob('snapshot-*.json'))]
        self.latest = json.loads((root / 'proof.json').read_text())['latest']
        self.assertGreaterEqual(len(self.samples), retention.MINIMUM_INTERVALS + 1)

    def test_shared_write_counter_bounds_only_the_system_stream(self):
        for first, last in zip(self.samples, self.samples[1:]):
            writes = (last['write_bytes'] - first['write_bytes']) / retention.elapsed(first, last)
            measured = retention.rates(first, last)
            self.assertGreaterEqual(measured['system'], writes)
            self.assertLess(measured['user'], writes)

    def test_measured_load_fits_the_cap_without_the_final_short_interval(self):
        self.assertLess(retention.elapsed(self.samples[-1], self.latest), retention.INTERVAL_SECONDS)
        measured = retention.measured_bounds(self.samples)
        bounds = retention.bounded_interval(measured, self.samples[-1], self.latest)
        self.assertEqual(bounds, measured)
        self.assertTrue(retention.calculation(self.latest, bounds)['passed'])


@unittest.skipUnless(RUNTIME_INPUT, 'Retained actual consecutive runtime snapshots are required')
class RealRuntimeRetentionInputTests(unittest.TestCase):
    def test_back_to_back_full_samples_keep_the_prior_bound(self):
        root = Path(RUNTIME_INPUT)
        first = json.loads((root / 'first.json').read_text())
        second = json.loads((root / 'second.json').read_text())
        bounds = json.loads((root / 'first-budget.json').read_text())['rates_bytes_per_second']
        self.assertLess(retention.elapsed(first, second), retention.INTERVAL_SECONDS)
        self.assertGreater(retention.rates(first, second)['system'], bounds['system'])
        result = retention.interval_budget(second, bounds, first)
        self.assertEqual(result['rates_bytes_per_second'], bounds)
        self.assertEqual(result['actual_gap_seconds'], retention.elapsed(first, second))
        self.assertTrue(result['passed'])


@unittest.skipUnless(MTIME_INPUT, 'Retained actual snapshots with a modification-time-only change are required')
class RealModificationTimeInputTests(unittest.TestCase):
    def test_zero_write_interval_with_only_a_new_modification_time_passes(self):
        root = Path(MTIME_INPUT)
        first = json.loads((root / 'first.json').read_text())
        second = json.loads((root / 'second.json').read_text())
        self.assertEqual(second['write_bytes'], first['write_bytes'])
        self.assertNotEqual(first['inventory'], second['inventory'])
        self.assertEqual(retention.rates(first, second), {'system': 0, 'user': 0})
        bounds = {'system': 1000, 'user': 0}
        self.assertTrue(retention.interval_budget(second, bounds, first, terminal=True)['passed'])


if __name__ == '__main__':
    unittest.main()
