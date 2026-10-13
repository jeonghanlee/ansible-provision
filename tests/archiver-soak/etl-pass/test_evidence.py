#!/usr/bin/env python3
"""Replay real completed evidence at the filesystem boundary without internal mocks."""

import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import contract

import evaluate

EVIDENCE = os.environ.get('ETL_SOAK_EVIDENCE')


@unittest.skipUnless(EVIDENCE, 'ETL_SOAK_EVIDENCE must name retained completed runtime evidence')
class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.out = Path(self.workspace.name) / 'evidence'
        shutil.copytree(Path(EVIDENCE), self.out)
        self.terminal = json.loads((self.out / 'shutdown.json').read_text())
        baseline = Path(self.terminal['observation']['counter_baseline'])
        relative = Path('raw') / baseline.parent.name / baseline.name
        self.terminal['observation']['counter_baseline'] = str(self.out / relative)
        for path in (self.out / 'raw').glob('*/sample.json'):
            row = json.loads(path.read_text())
            row['raw_directory'] = str(path.parent)
            self.write(path, row)

    def write(self, path, value):
        path.write_text(json.dumps(value))

    def result(self):
        return evaluate.evaluate(self.out, self.terminal)

    def window_samples(self):
        start = evaluate.epoch(self.terminal['observation']['started_at'])
        end = evaluate.epoch(self.terminal['finished_at'])
        return [(path, row) for path in (self.out / 'raw').glob('*/sample.json')
                if (row := json.loads(path.read_text())).get('sample_kind') == 'full'
                and start <= evaluate.epoch(row['observed_at']) <= end]

    def test_one_failed_full_sample_prevents_passed(self):
        self.schema_four_negative()
        path, row = self.window_samples()[0]
        row['errors'].append({'check': 'retained_sample_failure'})
        self.write(path, row)
        result = self.result()
        self.assertNotEqual(result['verdict'], 'Passed')
        self.assertIn('retained_sample_failure', result['failed_assertions'])

    def test_stale_pv_prevents_passed(self):
        self.schema_four_negative()
        path, row = self.window_samples()[0]
        row['latency']['pvs_with_recent_samples'] -= 1
        self.write(path, row)
        result = self.result()
        self.assertNotEqual(result['verdict'], 'Passed')
        self.assertIn('all_pv_freshness', result['failed_assertions'])

    def test_one_failed_health_invocation_prevents_passed(self):
        self.schema_four_negative()
        path = self.out / 'state.json'
        state = json.loads(path.read_text())
        start = evaluate.epoch(self.terminal['observation']['started_at'])
        event = next(row for row in state['health_completed'].values()
                     if evaluate.epoch(row['observed_at']) >= start)
        event.update(result='exit-code', exit_status='1')
        self.write(path, state)
        result = self.result()
        self.assertNotEqual(result['verdict'], 'Passed')
        self.assertIn('health_invocation', result['failed_assertions'])

    def test_missing_final_sample_retains_failures_as_incomplete(self):
        self.schema_four_negative()
        self.terminal.pop('final_full_sample')
        self.terminal['errors'].append('final_sample')
        result = self.result()
        self.assertEqual(result['verdict'], 'Incomplete')
        self.assertIn('final_sample', result['failed_assertions'])

    def schema_four_negative(self):
        manifest = self.terminal['observation']
        manifest['measurement_schema'] = contract.SCHEMA
        manifest['configuration'] = contract.chain_configuration('shortened')
        manifest['tool_hashes'] = contract.bundle_hashes(Path(evaluate.__file__).parent)
        self.write(self.out / 'initial-sample.json', manifest['initial_sample'])

    def test_new_contract_independently_rejects_short_monotonic_duration(self):
        self.schema_four_negative()
        result = self.result()
        self.assertNotEqual(result['verdict'], 'Passed')
        self.assertIn('observation_duration', result['failed_assertions'])

    def test_new_contract_independently_rejects_changed_expected_grid(self):
        self.schema_four_negative()
        self.terminal['observation']['expected_firings'].pop()
        result = self.result()
        self.assertNotEqual(result['verdict'], 'Passed')
        self.assertIn('manifest_schedule', result['failed_assertions'])

    def test_new_contract_does_not_accept_a_two_hour_window_as_twenty_four_hours(self):
        self.schema_four_negative()
        self.terminal['observation']['duration_seconds'] = 86400
        result = self.result()
        self.assertNotEqual(result['verdict'], 'Passed')
        self.assertIn('observation_duration', result['failed_assertions'])
        self.assertIn('utc_midnight', result['failed_assertions'])

    def test_new_contract_keeps_sample_failure_when_gc_input_is_malformed(self):
        self.schema_four_negative()
        path, row = self.window_samples()[0]
        row['errors'].append({'check': 'retained_sample_failure'})
        self.write(path, row)
        (self.out / 'gc-heap.csv').write_text('invalid\ninvalid\n')
        result = self.result()
        self.assertEqual(result['verdict'], 'Incomplete')
        self.assertIn('retained_sample_failure', result['failed_assertions'])


class SchedulerVerdictTests(unittest.TestCase):
    """The scheduler verdict and the metrics request-window tolerance on the shipped evaluator."""

    def passes(self, *ended):
        return [{'endedAt': value, 'busyMillis': '100', 'pvCount': '903'} for value in ended]

    def test_a_pass_ending_inside_the_metrics_request_is_accepted_either_way(self):
        summary = {'metrics_observed_at': '2026-10-12T08:35:02.123121+00:00', 'metrics_ms': 48.999}
        closed = self.passes('2026-10-12T08:30:02.295678+00:00', '2026-10-12T08:35:02.096940+00:00')
        variants = evaluate.metric_variants(closed, summary)
        self.assertEqual([len(rows) for rows in variants], [2, 1])
        before = self.passes('2026-10-12T08:30:02.295678+00:00', '2026-10-12T08:35:02.070000+00:00')
        self.assertEqual([len(rows) for rows in evaluate.metric_variants(before, summary)], [2])
        self.assertEqual([len(rows) for rows in evaluate.metric_variants(closed[1:], summary)], [1, 0])

    def test_instrument_findings_never_decide_the_scheduler_verdict(self):
        checks = contract.SCHEDULER_CHECKS
        result = evaluate.scheduler_result(['gc', 'latency', 'metric_snapshot_counter', 'kernel_journal',
                                            'journal_retention_budget'], ['gc_pair_coverage', 'kernel_journal_coverage'],
                                           checks)
        self.assertEqual(result['scheduler_verdict'], 'Passed')
        self.assertEqual(result['scheduler_failed_assertions'], [])
        self.assertEqual(result['scheduler_checks'], sorted(checks))
        for name in ('pv_status', 'etl_jobs', 'boot_changed', 'orderly_stop', 'health_invocation', 'jvm_restart'):
            with self.subTest(failure=name):
                self.assertEqual(evaluate.scheduler_result(['gc', name], [], checks)['scheduler_failed_assertions'], [name])
        for name in ('aborted_observation', 'scheduled_pass_coverage', 'full_sample_coverage',
                     'appliance_invocation_identity', 'required_pass_wait'):
            with self.subTest(missing=name):
                self.assertEqual(evaluate.scheduler_result([], ['gc_pair_coverage', name], checks)['scheduler_verdict'],
                                 'Incomplete')

    def test_failed_final_collections_enter_by_their_recorded_errors(self):
        terminal = {'finish_started_at': '2026-10-12T12:35:04+00:00', 'errors': ['final_sample', 'final_journal']}
        window = [{'sample_kind': 'full', 'observed_at': '2026-10-12T12:35:04.252780+00:00',
                   'errors': [{'check': 'gc'}]},
                  {'sample_kind': 'journal', 'observed_at': '2026-10-12T12:35:20+00:00', 'errors': []}]
        self.assertEqual(evaluate.terminal_sample_failures(terminal, window, contract.SCHEDULER_CHECKS), [])
        window[0]['errors'].append({'check': 'pv_status'})
        self.assertEqual(evaluate.terminal_sample_failures(terminal, window, contract.SCHEDULER_CHECKS), ['final_sample'])
        self.assertEqual(evaluate.terminal_sample_failures(terminal, window[:1], contract.SCHEDULER_CHECKS),
                         ['final_sample', 'final_journal'])


@unittest.skipUnless(EVIDENCE, 'ETL_SOAK_EVIDENCE must name retained completed runtime evidence')
class SchedulerVerdictEvidenceTests(unittest.TestCase):
    setUp = EvidenceTests.setUp
    write = EvidenceTests.write
    result = EvidenceTests.result
    window_samples = EvidenceTests.window_samples
    schema_four_negative = EvidenceTests.schema_four_negative

    def test_sample_instrument_error_fails_the_overall_verdict_only(self):
        self.schema_four_negative()
        path, row = self.window_samples()[0]
        row['errors'].append({'check': 'gc', 'type': 'RuntimeError', 'message': 'JFR snapshot archive limit reached'})
        self.write(path, row)
        result = self.result()
        self.assertNotEqual(result['verdict'], 'Passed')
        self.assertIn('gc', result['failed_assertions'])
        self.assertNotIn('gc', result['scheduler_failed_assertions'])
        self.assertEqual(result['scheduler_checks'], sorted(set(contract.SCHEDULER_CHECKS) | set(contract.ABORT_CHECKS)))

    def test_sample_abort_listed_error_fails_both_verdicts(self):
        self.schema_four_negative()
        path, row = self.window_samples()[0]
        row['errors'].append({'check': 'pv_status', 'message': 'fixture population is not fully archiving'})
        self.write(path, row)
        result = self.result()
        self.assertIn('pv_status', result['failed_assertions'])
        self.assertIn('pv_status', result['scheduler_failed_assertions'])
        self.assertNotEqual(result['scheduler_verdict'], 'Passed')


if __name__ == '__main__':
    unittest.main()
