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
                'inventory': {'system.journal': {'stream': 'system', 'allocated_bytes': 8 * 1024 ** 2},
                              'user-1000.journal': {'stream': 'user', 'allocated_bytes': user_bytes}}}

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

    def test_complete_sequence_requires_every_actual_entry(self):
        first = journal_coverage.coordinates(self.rows[0], self.boot)[1]
        last = journal_coverage.coordinates(self.rows[-1], self.boot)[1]
        unique = {journal_coverage.coordinates(row, self.boot)[1] for row in self.rows}
        if len(unique) == last - first + 1:
            result = journal_coverage.validate_interval(self.rows, self.rows[0], self.rows[-1], self.boot)
            self.assertEqual(len(result), last - first + 1)
            if len(result) > 2:
                with self.assertRaisesRegex(RuntimeError, 'missing records'):
                    journal_coverage.validate_interval(result[:1] + result[2:], result[0], result[-1], self.boot)
        else:
            with self.assertRaisesRegex(RuntimeError, 'missing records'):
                journal_coverage.validate_interval(self.rows, self.rows[0], self.rows[-1], self.boot)


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


if __name__ == '__main__':
    unittest.main()
