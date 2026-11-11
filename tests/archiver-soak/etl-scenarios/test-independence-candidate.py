#!/usr/bin/env python3
"""Exercise local candidate boundaries; live normal-finish acceptance is separate."""

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
ROOT = None
OUTPUT = None
TERMINAL = None
RUNNER = None
REPLAY = None
CONTRACT = None
COMMANDS = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.root = OUTPUT / self._testMethodName
        self.root.mkdir()
        self.tools = self.root / 'native'
        self.tools.mkdir()
        for name in (*CONTRACT.BUNDLE_FILES, 'bundle.json'):
            shutil.copy2(HERE.parent / 'etl-pass' / name, self.tools / name)
        self.study = self.root / 'study.py'
        shutil.copy2(HERE.parent / 'journal-validation/journal_coverage.py', self.study)
        self.original = self.study.read_bytes()
        self.config = {'role': 'etl', 'chain': 'shortened', 'study_state': 'changed',
            'duration_seconds': 7200, 'timeout_seconds': 10800, 'preparation_mode': 'fresh',
            'tools': str(self.tools), 'state_directory': str(self.root / 'state'),
            'case_directory': str(self.root / 'case'), 'study_path': str(self.study),
            'original_sha256': digest(self.study)}

    def command(self, argv):
        prefix = self.root / ('command-%03d' % len(COMMANDS))
        began = time.monotonic()
        result = subprocess.run(argv, capture_output=True, timeout=60)
        prefix.with_suffix('.stdout').write_bytes(result.stdout)
        prefix.with_suffix('.stderr').write_bytes(result.stderr)
        receipt = {'command': argv, 'returncode': result.returncode,
                   'elapsed_seconds': time.monotonic() - began}
        prefix.with_suffix('.json').write_text(json.dumps(receipt, indent=2) + '\n')
        COMMANDS.append(receipt)
        return result

    def action(self, action, expected=0):
        path = self.root / 'config.json'
        save(path, self.config)
        result = self.command([sys.executable, '-B', str(ROOT / 'run-etl-independence-v3.py'), action,
                               '--config', str(path)])
        self.assertEqual(result.returncode, expected, result.stderr.decode())
        return result

    def exercise_challenge(self, state):
        self.config['study_state'] = state
        self.action('check')
        self.action('challenge')
        case = Path(self.config['case_directory'])
        record = json.loads((case / 'challenge.json').read_text())
        self.assertEqual(record['study_state'], state)
        self.assertEqual(record['challenged_import_returncode'] == 0, state == 'changed')
        self.assertEqual(self.study.exists(), state != 'absent')
        if state == 'absent':
            self.assertIsNone(record['challenged_sha256'])
        else:
            self.assertEqual(digest(self.study), record['challenged_sha256'])
        self.action('restore')
        self.assertEqual(self.study.read_bytes(), self.original)
        before = RUNNER.members(case)
        self.action('restore')
        self.assertEqual(RUNNER.members(case), before)
        self.assertEqual(self.study.read_bytes(), self.original)

    def test_absent_challenge(self):
        self.exercise_challenge('absent')

    def test_failing_challenge(self):
        self.exercise_challenge('failing')

    def test_changed_challenge(self):
        self.exercise_challenge('changed')

    def test_wrong_original_hash_is_refused(self):
        self.config['original_sha256'] = '0' * 64
        self.action('challenge', 2)
        self.assertEqual(self.study.read_bytes(), self.original)
        self.assertFalse(Path(self.config['case_directory']).exists())

    def test_changed_native_dependency_is_refused(self):
        (self.tools / 'collect.py').write_text('# Invalid native dependency\n')
        result = self.action('check', 2)
        self.assertIn(b'frozen complete bundle', result.stderr)
        self.assertEqual(self.study.read_bytes(), self.original)

    def test_existing_case_is_preserved(self):
        case = Path(self.config['case_directory'])
        case.mkdir()
        (case / 'original.txt').write_text('Preserve this existing record\n')
        before = RUNNER.members(case)
        self.action('challenge', 2)
        self.assertEqual(RUNNER.members(case), before)
        self.assertEqual(self.study.read_bytes(), self.original)

    def test_restore_refuses_unexpected_study_change(self):
        self.action('challenge')
        self.study.write_text('# Unexpected independent change\n')
        changed = self.study.read_bytes()
        self.action('restore', 2)
        self.assertEqual(self.study.read_bytes(), changed)
        self.assertEqual((Path(self.config['case_directory']) / 'study-backup.py').read_bytes(), self.original)

    def test_live_run_requires_actual_installed_paths(self):
        result = self.action('run', 2)
        self.assertIn(b'Installed native paths differ', result.stderr)
        self.assertFalse(Path(self.config['case_directory']).exists())
        self.assertEqual(self.study.read_bytes(), self.original)

    def test_legacy_terminal_is_not_a_candidate_capture(self):
        output = self.root / 'replay'
        result = self.command([sys.executable, '-B', str(ROOT / 'replay-etl-independence-v2.py'),
                               '--case', str(TERMINAL.parent), '--output', str(output)])
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'capture.json', result.stderr)
        self.assertFalse(output.exists())

    def test_replay_preserves_existing_output(self):
        output = self.root / 'replay'
        output.mkdir()
        (output / 'original.txt').write_text('Preserve this existing output\n')
        before = RUNNER.members(output)
        result = self.command([sys.executable, '-B', str(ROOT / 'replay-etl-independence-v2.py'),
                               '--case', str(TERMINAL.parent), '--output', str(output)])
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'Output already exists', result.stderr)
        self.assertEqual(RUNNER.members(output), before)

    def test_candidate_help_through_preserved_dispatcher(self):
        payload = self.root / 'payload.json'
        save(payload, {'role': 'etl'})
        for source in RUNNER.SCENARIO_FILES:
            result = self.command([sys.executable, '-B', str(ROOT / 'run.py'), '--source', source,
                                   '--payload', str(payload), '--', '--help'])
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertIn(b'usage:', result.stdout)

    def test_terminal_kind_guard(self):
        terminal = json.loads(TERMINAL.read_text())
        status = 0 if terminal['verdict'] == 'Passed' else 1
        RUNNER.validate_terminal(terminal, status)
        changed = copy.deepcopy(terminal)
        changed['terminal_kind'] = 'abort'
        with self.assertRaisesRegex(RuntimeError, 'Normal-finish terminal required'):
            RUNNER.validate_terminal(changed, status)

    def test_terminal_status_guard(self):
        terminal = json.loads(TERMINAL.read_text())
        status = 0 if terminal['verdict'] == 'Passed' else 1
        RUNNER.validate_terminal(terminal, status)
        with self.assertRaisesRegex(RuntimeError, 'Native status differs from saved verdict'):
            RUNNER.validate_terminal(terminal, 1 - status)

    def test_controller_requires_actual_run_success(self):
        self.action('run', 2)
        receipt = {**COMMANDS[-1], 'source_sha256': digest(ROOT / 'run-etl-independence-v3.py'),
                   'configuration_sha256': digest(self.root / 'config.json')}
        with self.assertRaisesRegex(RuntimeError, 'Actual controller exit 0 is required'):
            REPLAY.validate_controller(receipt, receipt['source_sha256'], receipt['configuration_sha256'])

    def test_controller_rejects_a_check_receipt(self):
        self.action('check')
        receipt = {**COMMANDS[-1], 'source_sha256': digest(ROOT / 'run-etl-independence-v3.py'),
                   'configuration_sha256': digest(self.root / 'config.json')}
        with self.assertRaisesRegex(RuntimeError, 'Receipt does not identify the actual normal controller'):
            REPLAY.validate_controller(receipt, receipt['source_sha256'], receipt['configuration_sha256'])


def main():
    global ROOT, OUTPUT, TERMINAL, RUNNER, REPLAY, CONTRACT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--terminal', type=Path, required=True)
    parser.add_argument('--terminal-sha256', required=True)
    parser.add_argument('--case', choices=unittest.defaultTestLoader.getTestCaseNames(CandidateTests))
    args = parser.parse_args()
    ROOT, OUTPUT, TERMINAL = args.source_root.resolve(), args.output.resolve(), args.terminal.resolve()
    if OUTPUT.exists():
        parser.error('Existing evidence must be preserved')
    if digest(TERMINAL) != args.terminal_sha256:
        parser.error('Retained actual terminal identity differs')
    os.umask(0o077)
    OUTPUT.mkdir(parents=True)
    spec = importlib.util.spec_from_file_location('candidate_runner', ROOT / 'run-etl-independence-v3.py')
    RUNNER = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(RUNNER)
    spec = importlib.util.spec_from_file_location('candidate_replay', ROOT / 'replay-etl-independence-v2.py')
    REPLAY = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(REPLAY)
    CONTRACT = RUNNER.native(HERE.parent / 'etl-pass')
    sources = {name: digest(ROOT / name) for name in (*RUNNER.SCENARIO_FILES, 'run.py')}
    sources['test-independence-candidate.py'] = digest(Path(__file__))
    native = CONTRACT.verify_bundle(HERE.parent / 'etl-pass')
    save(OUTPUT / 'sources.json', {'scenario': sources, 'native': native,
         'terminal_sha256': digest(TERMINAL), 'python': sys.version})
    suite = (unittest.TestSuite([CandidateTests(args.case)]) if args.case else
             unittest.defaultTestLoader.loadTestsFromTestCase(CandidateTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if any(digest(ROOT / name) != value for name, value in sources.items() if name != 'test-independence-candidate.py'):
        raise RuntimeError('Candidate sources changed during local verification')
    if digest(Path(__file__)) != sources['test-independence-candidate.py']:
        raise RuntimeError('Local test source changed during verification')
    if CONTRACT.verify_bundle(HERE.parent / 'etl-pass') != native or digest(TERMINAL) != args.terminal_sha256:
        raise RuntimeError('Original native sources or retained terminal changed')
    save(OUTPUT / 'result.json', {'tests': result.testsRun, 'failures': len(result.failures),
         'errors': len(result.errors), 'skipped': len(result.skipped),
         'result': 'Passed' if result.wasSuccessful() else 'Failed', 'commands': COMMANDS,
         'scope': 'Local candidate boundaries only; no VM, normal-finish scenario or recipient acceptance'})
    return int(not result.wasSuccessful())


if __name__ == '__main__':
    raise SystemExit(main())
