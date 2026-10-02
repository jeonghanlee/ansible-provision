#!/usr/bin/env python3
"""Check budget arithmetic and parse retained real inputs; live scenarios are separate."""

import json
import os
from pathlib import Path
import unittest

import journal_coverage
import journal_retention as retention

REAL_INPUT = os.environ.get('ETL_SOAK_JOURNAL_SEQUENCE')


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


if __name__ == '__main__':
    unittest.main()
