#!/usr/bin/env python3
"""Exercise diagnostic isolation through real readers and complete retained inputs."""

import argparse
import datetime
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ARGS = None
SUPPORT = None
INPUT_MEMBERS = None
TOOL_MEMBERS = None
CANDIDATE = None
SAMPLES = None
FAULT_RAW = None


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


class RetainedDiagnostics(unittest.TestCase):
    def run_reader(self, fault=None, caller='evaluate'):
        original = ARGS.export_root / 'state'
        SUPPORT.verify(original, INPUT_MEMBERS)
        SUPPORT.verify(ARGS.export_root / 'tools', TOOL_MEMBERS)
        root = ARGS.output / self._testMethodName
        root.mkdir()
        state, tools = root / 'state', root / 'tools'
        shutil.copytree(original, state)
        SUPPORT.verify(state, INPUT_MEMBERS)
        tools.mkdir()
        for name in (*CANDIDATE['files'], 'bundle.json'):
            shutil.copy2(ARGS.candidate_tools / name, tools / name)
        faults = []
        if fault == 'metrics':
            target = state / FAULT_RAW / 'metrics.json'
            shutil.copy2(target, root / 'original-metrics.json')
            target.write_bytes(b'')
            faults.append(str(target.relative_to(state)))
        elif fault == 'journal':
            target = state / FAULT_RAW / 'journal.jsonl'
            target.rename(root / 'removed-journal.jsonl')
            faults.append(str(target.relative_to(state)))
        elif fault == 'passes':
            (state / 'passes.jsonl').rename(root / 'removed-passes.jsonl')
            faults.append('passes.jsonl')
        inputs, package = SUPPORT.inventory(state), SUPPORT.inventory(tools)
        save(root / 'input-members.json', inputs)
        save(root / 'tool-members.json', package)
        command = [sys.executable, '-B', str(tools / (caller + '.py')), '--input', str(state),
                   '--jfr-binary', str(ARGS.jfr_binary), '--jfr-output', str(root / 'jfr')]
        if caller == 'aggregate':
            command += ['--output', str(root / 'aggregate.json')]
        receipt = {'command': command, 'started_at': SUPPORT.now(), 'faults': faults}
        save(root / 'command.json', receipt)
        SUPPORT.verify(state, inputs)
        SUPPORT.verify(tools, package)
        began = time.monotonic()
        with (root / 'stdout').open('xb') as output, (root / 'stderr').open('xb') as errors:
            child = subprocess.Popen(command, stdout=output, stderr=errors, start_new_session=True)
            receipt['pid'] = child.pid
            save(root / 'command.json', receipt)
            try:
                receipt['returncode'] = child.wait(timeout=600)
            except subprocess.TimeoutExpired:
                receipt['timeout'] = True
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
                receipt['returncode'] = child.returncode
        receipt.update(finished_at=SUPPORT.now(), elapsed_seconds=time.monotonic() - began,
                       stdout_sha256=SUPPORT.digest(root / 'stdout'),
                       stderr_sha256=SUPPORT.digest(root / 'stderr'))
        save(root / 'command.json', receipt)
        SUPPORT.verify(state, inputs)
        SUPPORT.verify(tools, package)
        SUPPORT.verify(original, INPUT_MEMBERS)
        self.assertEqual(receipt['returncode'], 1, 'The actual unsuccessful verdict must remain visible')
        value = read(root / ('aggregate.json' if caller == 'aggregate' else 'stdout'))
        return value.get('evaluation', value)

    def assert_diagnostic_isolated(self, result):
        self.assertEqual(result['scheduler_verdict'], 'Failed')
        self.assertIn('scheduled_pass_identity', result['scheduler_failed_assertions'])
        self.assertNotIn('unreadable_or_conflicting_evidence', result['scheduler_missing_coverage'],
                         'A diagnostic error must not replace the scheduler result')
        self.assertIn('gc_evidence', result['missing_coverage'])
        self.assertEqual(result['full_samples'], SAMPLES)
        self.assertEqual(result['missing_passes'], 0)
        self.assertEqual(result['duplicate_passes'], 0)
        self.assertGreater(result['unexpected_passes'], 0)
        self.assertNotIn('incomplete_gc_pairs', result, 'Unavailable GC pair counts are not zero')
        if CANDIDATE['files'] != read(ARGS.export_root / 'tools/bundle.json')['files']:
            self.assertIn('tool_bundle_changed', result['scheduler_failed_assertions'])

    def test_real_gc_error_preserves_schedule_failure(self):
        result = self.run_reader()
        self.assert_diagnostic_isolated(result)
        self.assertIn('Unsupported GC timestamp variation', result['evidence_error'])

    def test_malformed_metrics_are_diagnostic(self):
        result = self.run_reader('metrics')
        self.assert_diagnostic_isolated(result)
        self.assertIn('metric_evidence', result['missing_coverage'])
        self.assertIn('JSONDecodeError', result['evidence_error'])

    def test_missing_journal_remains_critical_after_gc_error(self):
        result = self.run_reader('journal')
        self.assertEqual(result['scheduler_verdict'], 'Incomplete')
        self.assertIn('appliance_journal_coverage', result['scheduler_missing_coverage'])
        self.assertIn('gc_evidence', result['missing_coverage'])

    def test_missing_passes_remain_critical(self):
        result = self.run_reader('passes')
        self.assertEqual(result['scheduler_verdict'], 'Incomplete')
        self.assertIn('unreadable_or_conflicting_evidence', result['scheduler_missing_coverage'])

    def test_real_aggregate_retains_diagnostic_scope(self):
        self.assert_diagnostic_isolated(self.run_reader(caller='aggregate'))


def main():
    global ARGS, SUPPORT, INPUT_MEMBERS, TOOL_MEMBERS, CANDIDATE, SAMPLES, FAULT_RAW
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export-root', type=Path, required=True)
    parser.add_argument('--export-record', type=Path, required=True)
    parser.add_argument('--candidate-tools', type=Path, default=HERE)
    parser.add_argument('--jfr-binary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', choices=unittest.defaultTestLoader.getTestCaseNames(RetainedDiagnostics))
    ARGS = parser.parse_args()
    for name in ('export_root', 'export_record', 'candidate_tools', 'jfr_binary', 'output'):
        setattr(ARGS, name, getattr(ARGS, name).resolve())
    spec = importlib.util.spec_from_file_location('retained_terminal', HERE / 'test-terminal.py')
    SUPPORT = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(SUPPORT)
    original = read(ARGS.export_record)
    manifest = ARGS.export_root / 'metadata/members.json'
    if SUPPORT.digest(manifest) != original['members_sha256']:
        parser.error('Original export manifest identity differs')
    frozen = read(manifest)
    for name, members in frozen['members'].items():
        SUPPORT.verify(ARGS.export_root / name, members)
    INPUT_MEMBERS, TOOL_MEMBERS = frozen['members']['state'], frozen['members']['tools']
    terminal = read(ARGS.export_root / 'state/shutdown.json')
    expected_decoder = terminal['evaluation']['jfr_recordings']['decoder_sha256']
    if SUPPORT.digest(ARGS.jfr_binary) != expected_decoder:
        parser.error('Actual JFR decoder differs from the original runtime')
    CANDIDATE = read(ARGS.candidate_tools / 'bundle.json')
    for name, expected in CANDIDATE['files'].items():
        if SUPPORT.digest(ARGS.candidate_tools / name) != expected:
            parser.error('Candidate bundle differs: ' + name)
    begin = datetime.datetime.fromisoformat(terminal['observation']['started_at'])
    finish = datetime.datetime.fromisoformat(terminal['finished_at'])
    samples = [(p, read(p)) for p in sorted((ARGS.export_root / 'state/raw').glob('*/sample.json'))]
    full = [(p, row) for p, row in samples if row.get('sample_kind') == 'full' and
            begin <= datetime.datetime.fromisoformat(row['observed_at']) <= finish]
    if not full:
        parser.error('Actual in-window full samples are required')
    SAMPLES = len(full)
    FAULT_RAW = full[0][0].parent.relative_to(ARGS.export_root / 'state')
    os.umask(0o077)
    ARGS.output.mkdir(exist_ok=False)
    save(ARGS.output / 'preflight.json', {'manifest_sha256': original['members_sha256'],
         'candidate': CANDIDATE, 'jfr_sha256': expected_decoder,
         'test_sha256': SUPPORT.digest(Path(__file__)), 'full_samples': SAMPLES,
         'fault_sample_directory': str(FAULT_RAW),
         'scope': 'Retained-input correction only; original controller and verdict are unchanged'})
    suite = (unittest.TestSuite([RetainedDiagnostics(ARGS.case)]) if ARGS.case else
             unittest.defaultTestLoader.loadTestsFromTestCase(RetainedDiagnostics))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    for name, members in frozen['members'].items():
        SUPPORT.verify(ARGS.export_root / name, members)
    save(ARGS.output / 'result.json', {'tests': result.testsRun, 'failures': len(result.failures),
         'errors': len(result.errors), 'skips': len(result.skipped),
         'originals_unchanged': True, 'finished_at': SUPPORT.now(),
         'scope': 'Diagnostic isolation, not live scenario acceptance'})
    print('[VERDICT] ' + ('Passed' if result.wasSuccessful() else 'Failed'))
    return int(not result.wasSuccessful())


if __name__ == '__main__':
    raise SystemExit(main())
