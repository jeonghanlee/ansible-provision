#!/usr/bin/env python3
"""Check production startup receipt and capture paths with actual retained inputs."""

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
EVIDENCE = None
OUTPUT = None
RUNNER = None
REPLAY = None


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class StartupReplayTests(unittest.TestCase):
    def setUp(self):
        self.output = OUTPUT / self._testMethodName
        self.output.mkdir()
        self.data = EVIDENCE / 'case'
        self.config = RUNNER.load(self.data / 'configuration.json')
        self.runtime = RUNNER.load(self.data / 'runtime.json')

    def test_actual_startup_steps_are_consumed(self):
        REPLAY.validate_steps(self.data, self.config, self.runtime)

    def proof(self, data=None, manifest=None):
        REPLAY.validate_startup(data or self.data, self.config, self.runtime,
            manifest or RUNNER.load(EVIDENCE / 'state/observation.json'),
            RUNNER.load(self.data / 'challenge.json')['tool_hashes'])

    def derivative(self):
        path = self.output / 'case'
        shutil.copytree(self.data, path)
        return path

    def test_actual_startup_proof_is_consumed(self):
        self.proof()

    def test_missing_startup_state_is_refused(self):
        data = self.derivative()
        (data / 'startup-passes/state.json').rename(self.output / 'removed-state.json')
        with self.assertRaises(FileNotFoundError):
            self.proof(data)

    def test_unsuccessful_or_wrong_chain_startup_is_refused(self):
        data = self.derivative()
        path = data / 'startup-passes/state.json'
        original = RUNNER.load(path)
        for field, value in (('state', 'Incomplete'), ('chain', 'default')):
            with self.subTest(field=field):
                changed = {**original, field: value}
                RUNNER.save(path, changed)
                with self.assertRaisesRegex(RuntimeError, 'Successful same-chain startup evidence required'):
                    self.proof(data)

    def test_changed_startup_runtime_is_refused(self):
        data = self.derivative()
        path = data / 'startup-passes/state.json'
        startup = RUNNER.load(path)
        startup['actual_identity']['invocation_id'] += '-conflicting'
        RUNNER.save(path, startup)
        with self.assertRaisesRegex(RuntimeError, 'Startup source or runtime identity differs'):
            self.proof(data)

    def test_changed_native_source_is_refused(self):
        data = self.derivative()
        path = data / 'startup-passes/state.json'
        startup = RUNNER.load(path)
        startup['tool_hashes']['evaluate.py'] = '0' * 64
        RUNNER.save(path, startup)
        with self.assertRaisesRegex(RuntimeError, 'Startup source or runtime identity differs'):
            self.proof(data)

    def test_missing_capture_list_is_refused(self):
        data = self.derivative()
        path = data / 'startup-passes/state.json'
        startup = RUNNER.load(path)
        startup['captures'] = []
        RUNNER.save(path, startup)
        with self.assertRaisesRegex(RuntimeError, 'Actual startup captures required'):
            self.proof(data)

    def test_startup_at_observation_boundary_is_refused(self):
        startup = RUNNER.load(self.data / 'startup-passes/state.json')
        path = self.data / 'startup-passes' / ('capture-%04d' % (len(startup['captures']) - 1))
        passes = path / ('passes-' + startup['actual_identity']['invocation_id'] + '.jsonl')
        records = __import__('evaluate').pass_records(passes)
        first = max(records, key=lambda row: __import__('evidence').pass_instant(row['endedAt']))
        manifest = RUNNER.load(EVIDENCE / 'state/observation.json')
        manifest['started_at'] = first['endedAt']
        with self.assertRaisesRegex(RuntimeError, 'Startup transition does not precede observation'):
            self.proof(manifest=manifest)

    def test_conflicting_observation_identity_is_refused(self):
        manifest = RUNNER.load(EVIDENCE / 'state/observation.json')
        manifest['boot_id'] += '-conflicting'
        with self.assertRaisesRegex(RuntimeError, 'Startup observation identity differs'):
            self.proof(manifest=manifest)

    def test_changed_pass_capture_is_refused(self):
        data = self.derivative()
        startup = RUNNER.load(data / 'startup-passes/state.json')
        path = data / 'startup-passes' / ('capture-%04d' % (len(startup['captures']) - 1))
        passes = path / ('passes-' + startup['actual_identity']['invocation_id'] + '.jsonl')
        with passes.open('ab') as stream:
            stream.write(b'\n')
        with self.assertRaisesRegex(RuntimeError, 'Startup pass capture identity differs'):
            self.proof(data)

    def test_missing_transition_is_refused(self):
        data = self.derivative()
        state = data / 'startup-passes/state.json'
        startup = RUNNER.load(state)
        path = data / 'startup-passes' / ('capture-%04d' % (len(startup['captures']) - 1))
        passes = path / ('passes-' + startup['actual_identity']['invocation_id'] + '.jsonl')
        rows = passes.read_bytes().splitlines(keepends=True)
        retained = [row for row in rows if not json.loads(row)['MESSAGE'].startswith('ETL pass of transition 1 cadence ')]
        self.assertGreater(len(rows), len(retained), 'Actual second transition must be present')
        passes.write_bytes(b''.join(retained))
        startup['captures'][-1]['pass_sha256'] = digest(passes)
        RUNNER.save(state, startup)
        with self.assertRaisesRegex(RuntimeError, 'Required startup transition is missing: 1'):
            self.proof(data)

    def test_capture_retains_actual_startup_members(self):
        case = self.output / 'case'
        shutil.copytree(self.data, case)
        state = EVIDENCE / 'state'
        expected = RUNNER.members(self.data / 'startup-passes')
        self.assertTrue(expected, 'Actual startup input is required')
        RUNNER.freeze_evidence(case, state, EVIDENCE / 'native',
                               RUNNER.load(case / 'challenge.json'), state / 'abort.json')
        self.assertEqual(RUNNER.members(case / 'frozen/case/startup-passes'), expected,
                         'Frozen capture omits actual nested startup members')


def main():
    global SOURCE, EVIDENCE, OUTPUT, RUNNER, REPLAY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    SOURCE, EVIDENCE, OUTPUT = args.source_root.resolve(), args.evidence.resolve(), args.output.resolve()
    manifest_path = EVIDENCE / 'metadata/members.json'
    if digest(manifest_path) != args.manifest_sha256:
        parser.error('Retained original manifest identity differs')
    manifest = json.loads(manifest_path.read_text())['members']
    actual_files = {p.relative_to(EVIDENCE).as_posix(): digest(p)
                    for p in EVIDENCE.rglob('*') if p.is_file()}
    expected_files = {name: row['sha256'] for name, row in manifest.items()
                      if row['kind'] == 'file'}
    expected_files['metadata/members.json'] = args.manifest_sha256
    if actual_files != expected_files:
        parser.error('Retained original membership or bytes differ')
    os.umask(0o077)
    OUTPUT.mkdir(parents=True, exist_ok=False)
    RUNNER = load_module('startup_capture_runner', SOURCE / 'run-etl-independence-v3.py')
    REPLAY = load_module('startup_capture_replay', SOURCE / 'replay-etl-independence-v3.py')
    REPLAY.support.native(EVIDENCE / 'native')
    sources = {name: digest(SOURCE / name) for name in RUNNER.SCENARIO_FILES}
    sources[Path(__file__).name] = digest(Path(__file__))
    (OUTPUT / 'sources.json').write_text(json.dumps(sources, indent=2) + '\n')
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(StartupReplayTests))
    preserved = {p.relative_to(EVIDENCE).as_posix(): digest(p)
                 for p in EVIDENCE.rglob('*') if p.is_file()} == actual_files
    unchanged = all(digest(SOURCE / name) == value for name, value in sources.items()
                    if name != Path(__file__).name) and digest(Path(__file__)) == sources[Path(__file__).name]
    record = {'tests': result.testsRun, 'failures': len(result.failures),
              'errors': len(result.errors), 'skipped': len(result.skipped),
              'originals_unchanged': preserved, 'sources_unchanged': unchanged,
              'scope': 'Actual retained receipt and capture consumers only; no normal-finish or recipient acceptance',
              'result': 'Passed' if result.wasSuccessful() and preserved and unchanged else 'Failed'}
    (OUTPUT / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    return int(record['result'] != 'Passed')


if __name__ == '__main__':
    raise SystemExit(main())
