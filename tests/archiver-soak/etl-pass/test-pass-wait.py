#!/usr/bin/env python3
"""Check retained-pass waiting through the real collector and local diagnostic failures."""

import argparse
import datetime
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

COMMAND_TIMEOUT_SECONDS = 90
WAIT_TIMEOUT_SECONDS = 0
TOOLS = Path(__file__).resolve().parent
INPUT = None
OUTPUT = None
OBSERVER = None


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def execute(command, destination):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    began = time.monotonic()
    result = subprocess.run(command, capture_output=True, timeout=COMMAND_TIMEOUT_SECONDS)
    destination.with_suffix('.stdout').write_bytes(result.stdout)
    destination.with_suffix('.stderr').write_bytes(result.stderr)
    save(destination.with_suffix('.json'), {
        'command': command, 'returncode': result.returncode, 'started_at': started,
        'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'elapsed_seconds': time.monotonic() - began})
    return result


class PassWaitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if OBSERVER.collect.resources.jvm_pids():
            raise RuntimeError('Use a control host without running appliance JVMs')
        cls.original_manifest = json.loads((INPUT / 'observation.json').read_text())
        if cls.original_manifest.get('measurement_schema') != OBSERVER.contract.SCHEMA:
            raise RuntimeError('Actual retained input must use the current observation schema')
        cls.original_passes = (INPUT / 'passes.jsonl').read_bytes()
        invocation = OBSERVER.collect.properties(cls.original_manifest['unit_before_observation'])['InvocationID']
        records = [row for row in OBSERVER.evaluate.pass_records(INPUT / 'passes.jsonl')
                   if row['invocation_id'] == invocation]
        if not records:
            raise RuntimeError('An actual retained pass from the observation invocation is required')
        for row in records:
            planned = datetime.datetime.fromisoformat(row['plannedAt'].replace('Z', '+00:00'))
            ended = planned + datetime.timedelta(seconds=1)
            expected = OBSERVER.contract.expected_firings(planned, ended, cls.original_manifest['configuration'])
            if (len(expected) == 1 and expected[0]['transition'] == row['transition']
                    and expected[0]['cadence'] == row['cadence']
                    and OBSERVER.evaluate.epoch(expected[0]['planned_at']) == OBSERVER.evaluate.epoch(row['plannedAt'])):
                break
        else:
            raise RuntimeError('The retained input must contain an actual scheduled firing')
        cls.manifest = dict(cls.original_manifest, started_at=planned.isoformat(),
                            earliest_finish_at=ended.isoformat())
        save(OUTPUT / 'selected-interval.json', {
            'source': str(INPUT), 'original_manifest_sha256': hashlib.sha256(
                (INPUT / 'observation.json').read_bytes()).hexdigest(),
            'original_passes_sha256': hashlib.sha256(cls.original_passes).hexdigest(),
            'started_at': planned.isoformat(), 'ended_at': ended.isoformat(), 'expected_firings': expected,
            'scope': 'A selected retained firing interval, not a rewritten original or whole observation'})
        probe = execute(['journalctl', '-b', '--no-pager', '-o', 'json', '-n', '1'], OUTPUT / 'anchor-probe')
        if probe.returncode or not probe.stdout.strip():
            raise RuntimeError('A readable current-boot journal record is required')
        cls.cursor = json.loads(probe.stdout.splitlines()[-1])['__CURSOR']

    def setUp(self):
        self.directory = OUTPUT / self._testMethodName
        self.directory.mkdir()
        self.passes = self.directory / 'passes.jsonl'
        self.passes.write_bytes(self.original_passes)
        self.state = {
            'journal_since': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
            'kernel_journal_cursor': 'invalid:' + self.cursor}
        save(self.directory / 'state.json', self.state)
        self.manifest = dict(type(self).manifest)
        save(self.directory / 'wait-input.json', self.manifest)
        OBSERVER.OUT = self.directory
        OBSERVER.TOOLS = TOOLS
        OBSERVER.PASS_WAIT_SECONDS = WAIT_TIMEOUT_SECONDS

    def latest(self):
        return json.loads((self.directory / 'latest.json').read_text())

    def wait(self):
        return OBSERVER.wait_passes(self.manifest)

    def assert_native_diagnostics(self):
        sample = self.latest()
        self.assertEqual(sample['sample_kind'], 'journal')
        self.assertIsNotNone(sample.get('journal'), 'actual application journal capture succeeded')
        self.assertIn('kernel_journal', [row['check'] for row in sample['errors']])
        self.assertFalse(any(row['check'] in OBSERVER.evaluate.scheduler_checks(self.manifest)
                             for row in sample['errors']), 'only non-deciding diagnostics failed')
        raw = Path(sample['raw_directory'])
        receipt = json.loads((raw / 'kernel-checkpoint-journal.jsonl.receipt.json').read_text())
        self.assertNotEqual(receipt['returncode'], 0, 'failure reached native journalctl')
        self.assertEqual(receipt['interval']['previous_cursor'], self.state['kernel_journal_cursor'])
        self.assertTrue((raw / 'kernel-checkpoint-journal.stderr').read_bytes())

    def test_retained_pass_survives_native_diagnostic_failure(self):
        result = self.wait()
        self.assertEqual((result['required'], result['completed']), (1, 1))
        self.assert_native_diagnostics()
        self.assertEqual(self.passes.read_bytes(), self.original_passes, 'retained native pass bytes unchanged')
        save(self.directory / 'wait-result.json', result)

    def test_missing_pass_still_reaches_the_deadline(self):
        self.passes.write_bytes(b'')
        with self.assertRaisesRegex(RuntimeError, 'did not close before the bounded deadline'):
            self.wait()
        self.assert_native_diagnostics()
        self.assertEqual(self.passes.read_bytes(), b'')

    def test_required_journal_failure_refuses_retained_pass(self):
        self.state['journal_cursor'] = 'invalid:' + self.cursor
        save(self.directory / 'state.json', self.state)
        with self.assertRaisesRegex(RuntimeError, 'could not collect complete journals'):
            self.wait()
        self.assertIn('journal', [row['check'] for row in self.latest()['errors']])
        self.assertEqual(self.passes.read_bytes(), self.original_passes)

    def test_recorded_abort_policy_remains_decisive(self):
        self.manifest['abort_policy'] = dict(self.manifest['abort_policy'])
        self.manifest['abort_policy']['checks'] = [*self.manifest['abort_policy']['checks'], 'kernel_journal']
        save(self.directory / 'wait-input.json', self.manifest)
        with self.assertRaisesRegex(RuntimeError, 'could not collect complete journals'):
            self.wait()
        self.assertIn('kernel_journal', [row['check'] for row in self.latest()['errors']])

    def failed_collector_with_prior_sample(self, mode):
        native = execute(['/usr/bin/python3', '-B', str(TOOLS / 'collect.py'), str(self.directory),
                          str(TOOLS / 'pvs-all.csv'), '--journal-only'], self.directory / 'initial-collector')
        self.assertEqual(native.returncode, 1)
        self.assert_native_diagnostics()
        latest = self.directory / 'latest.json'
        if mode == 'absent':
            latest.rename(self.directory / 'preserved-latest.json')
        elif mode == 'malformed':
            latest.rename(self.directory / 'preserved-latest.json')
            latest.write_bytes(b'{')
        before = latest.read_bytes() if latest.exists() else None
        (self.directory / 'raw').rename(self.directory / 'preserved-raw')
        (self.directory / 'raw').write_text('The collector cannot create a raw sample directory here.\n')
        with self.assertRaises((RuntimeError, ValueError, OSError)):
            self.wait()
        after = latest.read_bytes() if latest.exists() else None
        self.assertEqual(after, before, 'failed collector supplied no new sample')
        self.assertEqual(self.passes.read_bytes(), self.original_passes)

    def test_stale_sample_cannot_hide_collector_failure(self):
        self.failed_collector_with_prior_sample('stale')

    def test_absent_sample_cannot_hide_collector_failure(self):
        self.failed_collector_with_prior_sample('absent')

    def test_malformed_sample_cannot_hide_collector_failure(self):
        self.failed_collector_with_prior_sample('malformed')


def main():
    global TOOLS, INPUT, OUTPUT, OBSERVER
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tools', type=Path, default=TOOLS)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', choices=unittest.defaultTestLoader.getTestCaseNames(PassWaitTests))
    args = parser.parse_args()
    TOOLS, INPUT, OUTPUT = args.tools.resolve(), args.input.resolve(), args.output.resolve()
    os.umask(0o077)
    OUTPUT.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(TOOLS))
    OBSERVER = importlib.import_module('observe')
    sources = {name: hashlib.sha256((TOOLS / name).read_bytes()).hexdigest()
               for name in OBSERVER.contract.BUNDLE_FILES}
    inputs = {name: hashlib.sha256((INPUT / name).read_bytes()).hexdigest()
              for name in ('observation.json', 'passes.jsonl')}
    save(OUTPUT / 'identities.json', {'tools': str(TOOLS), 'sources': sources, 'input': str(INPUT),
         'inputs': inputs, 'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    suite = (unittest.TestSuite([PassWaitTests(args.case)]) if args.case else
             unittest.defaultTestLoader.loadTestsFromTestCase(PassWaitTests))
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    began = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    unchanged = (all(hashlib.sha256((TOOLS / name).read_bytes()).hexdigest() == digest
                     for name, digest in sources.items()) and
                 all(hashlib.sha256((INPUT / name).read_bytes()).hexdigest() == digest
                     for name, digest in inputs.items()))
    save(OUTPUT / 'result.json', {
        'started_at': started, 'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'elapsed_seconds': time.monotonic() - began, 'tests_run': result.testsRun,
        'failures': [(test.id(), detail) for test, detail in result.failures],
        'errors': [(test.id(), detail) for test, detail in result.errors],
        'sources_and_inputs_unchanged': unchanged,
        'scope': 'Retained-pass wait and real local collector only; no appliance lifecycle or whole-observation replay',
        'result': 'Passed' if result.wasSuccessful() and unchanged else 'Failed'})
    return 0 if result.wasSuccessful() and unchanged else 1


if __name__ == '__main__':
    raise SystemExit(main())
