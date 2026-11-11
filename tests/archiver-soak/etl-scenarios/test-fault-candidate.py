#!/usr/bin/env python3
"""Exercise local fault candidate boundaries without a service or lifecycle substitute."""

import argparse
import base64
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import unittest

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=Path(__file__).parent)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--terminal', type=Path, required=True)
    parser.add_argument('--terminal-sha256', required=True)
    parser.add_argument('--case')
    args = parser.parse_args()
    root, output = args.source_root.resolve(), args.output.resolve()
    if output.exists():
        parser.error('Preserve existing test output')
    spec = importlib.util.spec_from_file_location('fault_candidate', root / 'fault_support.py')
    candidate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    candidate.require(candidate.digest(args.terminal) == args.terminal_sha256, 'Actual terminal fixture differs')
    terminal = candidate.load(args.terminal)
    source_before = candidate.members(root)
    output.mkdir(parents=True, mode=0o700)
    candidate.save(output / 'sources.json', {'scenario': source_before,
                   'test_sha256': candidate.digest(Path(__file__)), 'terminal_sha256': args.terminal_sha256,
                   'python': sys.version})
    commands = []

    class CandidateTests(unittest.TestCase):
        def setUp(self):
            self.directory = output / self._testMethodName
            self.directory.mkdir()
            wrapper = root / 'etl-fault-sampler.py'
            self.config = {'role': 'etl', 'chain': 'shortened', 'case': 'E3', 'timeout_seconds': 21600,
                           'native_preflight_script': str(root / 'etl-native-preflight-v2.py'),
                           'boundary_preflight_script': str(root / 'preflight-etl-fault-boundary.py'),
                           'scenario_sha256': {name: candidate.digest(root / name) for name in candidate.FILES},
                           'wrapper_source_sha256': candidate.digest(wrapper),
                           'wrapper_source_base64': base64.b64encode(wrapper.read_bytes()).decode()}
            for name in ('native_preflight_script', 'boundary_preflight_script'):
                self.config[name + '_sha256'] = candidate.digest(Path(self.config[name]))

        def run_controller(self, config=None, action='check', label='controller'):
            path = self.directory / (label + '-config.json')
            candidate.save(path, self.config if config is None else config)
            receipt = candidate.execute(self.directory, label,
                [sys.executable, '-B', str(root / 'run-etl-fault-v3.py'), '--config', str(path), action], 30)
            commands.append(receipt)
            return path, receipt

        def replay(self, extra, label='replay'):
            receipt = candidate.execute(self.directory, label,
                [sys.executable, '-B', str(root / 'replay-etl-fault-v2.py'), *map(str, extra)], 30)
            commands.append(receipt)
            return receipt

        def test_configuration_four_cells(self):
            for chain in ('shortened', 'default'):
                for case in ('E3', 'E4'):
                    config = {**self.config, 'chain': chain, 'case': case}
                    _, receipt = self.run_controller(config, label=chain + '-' + case)
                    self.assertEqual(receipt['returncode'], 0)
                    value = candidate.load(self.directory / (chain + '-' + case + '.stdout'))
                    self.assertEqual(value, {'configuration': 'Valid', 'runtime': 'Not run'})

        def test_invalid_role(self):
            _, receipt = self.run_controller({**self.config, 'role': 'invalid'})
            self.assertNotEqual(receipt['returncode'], 0)
            self.assertIn('Configuration requires role=etl', (self.directory / 'controller.stderr').read_text())

        def test_invalid_chain(self):
            _, receipt = self.run_controller({**self.config, 'chain': 'invalid'})
            self.assertNotEqual(receipt['returncode'], 0)
            self.assertIn('Unsupported fault chain or case', (self.directory / 'controller.stderr').read_text())

        def test_nonfinite_timeout(self):
            _, receipt = self.run_controller({**self.config, 'timeout_seconds': float('inf')})
            self.assertNotEqual(receipt['returncode'], 0)
            self.assertIn('Finite positive controller timeout required', (self.directory / 'controller.stderr').read_text())

        def test_preflight_source_mismatch(self):
            _, receipt = self.run_controller({**self.config, 'native_preflight_script_sha256': '0' * 64})
            self.assertNotEqual(receipt['returncode'], 0)
            self.assertIn('Preflight source identity differs', (self.directory / 'controller.stderr').read_text())

        def test_candidate_source_mismatch(self):
            config = copy.deepcopy(self.config)
            config['scenario_sha256']['fault_support.py'] = '0' * 64
            _, receipt = self.run_controller(config)
            self.assertNotEqual(receipt['returncode'], 0)
            self.assertIn('Candidate source identity differs', (self.directory / 'controller.stderr').read_text())

        def test_sampler_source_mismatch(self):
            _, receipt = self.run_controller({**self.config, 'wrapper_source_base64': ''})
            self.assertNotEqual(receipt['returncode'], 0)
            self.assertIn('Actual shipped namespace sampler required', (self.directory / 'controller.stderr').read_text())

        def test_controller_requires_actual_success(self):
            path, receipt = self.run_controller({**self.config, 'role': 'invalid'}, action='run')
            self.assertNotEqual(receipt['returncode'], 0)
            receipt.update(source_sha256=self.config['scenario_sha256']['run-etl-fault-v3.py'],
                           configuration_sha256=candidate.digest(path))
            with self.assertRaisesRegex(RuntimeError, 'Actual fault controller exit 0 required'):
                candidate.controller(receipt, self.config['scenario_sha256'], candidate.digest(path))

        def test_successful_check_is_not_runtime(self):
            path, receipt = self.run_controller()
            self.assertEqual(receipt['returncode'], 0)
            receipt.update(source_sha256=self.config['scenario_sha256']['run-etl-fault-v3.py'],
                           configuration_sha256=candidate.digest(path))
            with self.assertRaisesRegex(RuntimeError, 'Actual fault run command required'):
                candidate.controller(receipt, self.config['scenario_sha256'], candidate.digest(path))

        def test_replay_requires_real_capture(self):
            destination = self.directory / 'new-replay'
            receipt = self.replay(['--case', self.directory, '--output', destination, '--record-baseline'])
            self.assertEqual(receipt['returncode'], 2)
            self.assertIn('Complete frozen roots', (self.directory / 'replay.stderr').read_text())
            self.assertFalse(destination.exists())

        def test_replay_preserves_existing_output(self):
            destination = self.directory / 'existing'
            destination.mkdir()
            shutil.copy2(args.terminal, destination / 'actual-abort.json')
            before = candidate.members(destination)
            receipt = self.replay(['--case', self.directory / 'case', '--tools', self.directory / 'tools',
                '--input', self.directory / 'input', '--output', destination, '--members', self.directory / 'members.json',
                '--members-sha256', '0' * 64, '--controller-receipt', self.directory / 'controller.json',
                '--controller-receipt-sha256', '0' * 64, '--record-baseline'])
            self.assertEqual(receipt['returncode'], 2)
            self.assertIn('Output exists or overlaps', (self.directory / 'replay.stderr').read_text())
            self.assertEqual(candidate.members(destination), before)

        def test_terminal_kind(self):
            candidate.terminal(terminal, 1)
            value = copy.deepcopy(terminal)
            value['terminal_kind'] = 'finish'
            with self.assertRaisesRegex(RuntimeError, 'Actual abort terminal required'):
                candidate.terminal(value, 1)

        def test_terminal_native_status(self):
            candidate.terminal(terminal, 1)
            with self.assertRaisesRegex(RuntimeError, 'Short native observation must remain Incomplete with exit 1'):
                candidate.terminal(terminal, 0)

        def test_terminal_stop_failure(self):
            value = copy.deepcopy(terminal)
            value['stop']['rc'] = 1
            with self.assertRaisesRegex(RuntimeError, 'Complete same-boot abort capture'):
                candidate.terminal(value, 1)

        def test_recorded_path_traversal(self):
            with self.assertRaisesRegex(RuntimeError, 'Recorded input path contains traversal'):
                candidate.source_path(str(candidate.OUT / '../other'), candidate.OUT, self.directory)

        def freeze_actual_files(self):
            roots = {}
            for name, source in (('tools', root / 'etl-fault-sampler.py'), ('input', args.terminal),
                                 ('case', root / 'run-etl-fault-v2.py')):
                roots[name] = self.directory / name
                roots[name].mkdir()
                shutil.copy2(source, roots[name] / source.name)
            manifest = self.directory / 'members.json'
            candidate.freeze(roots, manifest)
            return roots, manifest, candidate.digest(manifest)

        def test_complete_frozen_membership(self):
            roots, manifest, expected = self.freeze_actual_files()
            self.assertEqual(candidate.verified(roots, manifest, expected),
                             {name: candidate.members(path) for name, path in roots.items()})

        def test_frozen_member_change(self):
            roots, manifest, expected = self.freeze_actual_files()
            with (roots['input'] / args.terminal.name).open('ab') as stream:
                stream.write(b'\n')
            with self.assertRaisesRegex(RuntimeError, 'Frozen input membership or bytes differ'):
                candidate.verified(roots, manifest, expected)

        def test_stage_complete_sources(self):
            command = [sys.executable, '-B', str(root / 'prepare-vm-batch.py'), '--source-root', str(root.parent),
                       '--output', str(self.directory / 'staged')]
            receipt = candidate.execute(self.directory, 'stage', command, 60)
            commands.append(receipt)
            self.assertEqual(receipt['returncode'], 0)
            metadata = candidate.load(self.directory / 'staged/batch.json')
            self.assertEqual(len(metadata['runtime_claims']), 7)
            self.assertFalse(metadata['runtime_verified'])

        def test_stage_preserves_existing_output(self):
            receipt = candidate.execute(self.directory, 'stage', [sys.executable, '-B', str(root / 'prepare-vm-batch.py'),
                '--source-root', str(root.parent), '--output', str(self.directory)], 30)
            commands.append(receipt)
            self.assertEqual(receipt['returncode'], 2)
            self.assertIn('Output exists or overlaps', (self.directory / 'stage.stderr').read_text())

    names = [args.case] if args.case else unittest.defaultTestLoader.getTestCaseNames(CandidateTests)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(CandidateTests(name) for name in names))
    candidate.require(candidate.members(root) == source_before, 'Original scenario sources changed')
    candidate.save(output / 'result.json', {'tests': result.testsRun, 'failures': len(result.failures),
                   'errors': len(result.errors), 'skipped': len(result.skipped), 'commands': commands,
                   'scope': 'Local candidate boundaries only; no VM, fault exposure, normal/abort lifecycle or recipient acceptance',
                   'result': 'Passed' if result.wasSuccessful() else 'Failed'})
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
