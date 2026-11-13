#!/usr/bin/env python3
"""Verify stable analysis paths through real native readers on retained evidence."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = None
STATE = None
OUTPUT = None
MEMBERS = None
REPLAY = None
VERIFY = None
TOOLS = None
SOURCES = None


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class ReplayPathTests(unittest.TestCase):
    def setUp(self):
        self.output = OUTPUT / self._testMethodName
        self.output.mkdir()
        VERIFY.verify(STATE, MEMBERS)
        self.canonical = self.output / 'canonical'
        self.frozen = self.output / 'inputs'
        native = self.frozen / 'native'
        native.mkdir(parents=True)
        expected = json.loads((TOOLS / 'bundle.json').read_text())['files']
        for name in (*expected, 'bundle.json'):
            shutil.copy2(TOOLS / name, native / name)
        self.assertEqual({name: digest(native / name) for name in expected}, expected)
        shutil.copytree(STATE, self.frozen / 'state')
        VERIFY.verify(self.frozen / 'state', MEMBERS)

    def execute(self, caller, number):
        receipts = self.output / ('round-%d' % number)
        receipts.mkdir()
        recording = self.canonical / (caller + '-jfr')
        receipt, value = REPLAY.replay_native(receipts, self.canonical, self.frozen, caller)
        VERIFY.verify(self.canonical / caller / 'state', MEMBERS)
        self.assertIn(value['verdict'], ('Passed', 'Failed', 'Incomplete'))
        self.assertEqual(receipt['returncode'], 0 if value['verdict'] == 'Passed' else 1)
        return receipts, value, recording, receipt['returncode']

    def declared_path(self, caller):
        _, value, expected, _ = self.execute(caller, 1)
        self.assertTrue(expected.is_dir(), 'Native reader did not create the declared recording path')
        if caller == 'evaluate':
            self.assertEqual(value['jfr_recordings']['evidence_directory'], str(expected),
                             'Native reader did not consume the declared recording path')

    def repeat(self, caller):
        first, _, _, first_status = self.execute(caller, 1)
        self.canonical.rename(self.output / 'retained-round-1')
        second, _, _, second_status = self.execute(caller, 2)
        self.assertEqual(first_status, second_status)
        for name in (caller + '.stdout', caller + '.stderr', *(['aggregate-result.json'] if caller == 'aggregate' else [])):
            with self.subTest(artifact=name):
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes(),
                                 'Complete native output bytes differ: ' + name)

    def test_evaluate_declared_path(self):
        self.declared_path('evaluate')

    def test_aggregate_declared_path(self):
        self.declared_path('aggregate')

    def test_evaluate_complete_bytes(self):
        self.repeat('evaluate')

    def test_aggregate_complete_bytes(self):
        self.repeat('aggregate')


def main():
    global SOURCE, STATE, OUTPUT, MEMBERS, REPLAY, VERIFY, TOOLS, SOURCES
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    SOURCE, OUTPUT = args.source_root.resolve(), args.output.resolve()
    evidence = args.evidence.resolve()
    manifest = evidence / 'metadata/members.json'
    if digest(manifest) != args.manifest_sha256:
        parser.error('Actual retained manifest identity differs')
    MEMBERS = json.loads(manifest.read_text())['members']['state']
    STATE = evidence / 'state'
    TOOLS = HERE.parent / 'etl-pass'
    VERIFY = module('actual_state_verifier', TOOLS / 'test-terminal.py')
    VERIFY.verify(STATE, MEMBERS)
    REPLAY = module('stable_path_replay', SOURCE / 'replay-etl-independence-v3.py')
    SOURCES = {name: digest(SOURCE / name) for name in ('replay-etl-independence-v3.py', *REPLAY.support.SCENARIO_FILES)}
    test_sha = digest(Path(__file__))
    os.umask(0o077)
    OUTPUT.mkdir(parents=True, exist_ok=False)
    (OUTPUT / 'sources.json').write_text(json.dumps({'scenario': SOURCES, 'test_sha256': test_sha,
        'native_bundle': json.loads((TOOLS / 'bundle.json').read_text()), 'python': sys.version}, indent=2) + '\n')
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReplayPathTests))
    VERIFY.verify(STATE, MEMBERS)
    unchanged = digest(Path(__file__)) == test_sha and all(digest(SOURCE / name) == value for name, value in SOURCES.items())
    record = {'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
              'skipped': len(result.skipped), 'sources_unchanged': unchanged, 'originals_unchanged': True,
              'scope': 'Real native output-path consumption and complete raw-byte repeatability only; original unsuccessful outcomes remain; no scenario or recipient acceptance',
              'result': 'Passed' if result.wasSuccessful() and unchanged else 'Failed'}
    (OUTPUT / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    return int(record['result'] != 'Passed')


if __name__ == '__main__':
    raise SystemExit(main())
