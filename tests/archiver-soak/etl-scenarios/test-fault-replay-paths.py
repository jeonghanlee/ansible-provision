#!/usr/bin/env python3
"""Verify fault replay native paths on complete independently pinned retained evidence."""

import argparse
import ast
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--dependencies', type=Path, required=True)
    parser.add_argument('--environment', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--legacy', action='store_true')
    args = parser.parse_args()
    source, output, retained = args.source_root.resolve(), args.output.resolve(), args.evidence.resolve()
    verify = module('actual_native_member_verifier', HERE.parent / 'etl-pass/test-terminal.py')
    digest, read = verify.digest, verify.read
    manifest = retained / 'metadata/members.json'
    if digest(manifest) != args.manifest_sha256:
        parser.error('Actual retained manifest identity differs')
    frozen = read(manifest)['members']
    for name in ('tools', 'state'):
        verify.verify(retained / name, frozen[name])
    dependencies = read(args.dependencies)
    jdk = Path(dependencies['root'])
    verify.verify(jdk, dependencies['members'])
    os.environ.update(read(args.environment))
    os.umask(0o077)
    output.mkdir(parents=True, exist_ok=False)
    temporary = output / 'tmp'
    temporary.mkdir()
    os.environ['TMPDIR'] = str(temporary)
    target = source / ('replay-etl-fault-v2.py' if args.legacy else 'replay-etl-fault-v3.py')
    sources = {str(path): digest(path) for path in (
        target, source / 'fault_support.py', source / 'run-etl-independence-v3.py',
        Path(__file__).resolve(), Path(sys.executable).resolve())}
    candidate = module('selected_fault_replay', target)
    legacy_calls = {}
    if args.legacy:
        text = target.read_text()
        for caller in ('evaluate', 'aggregate'):
            calls = [node for node in ast.walk(ast.parse(text))
                     if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                     and isinstance(node.func.value, ast.Name) and node.func.value.id == 'subprocess'
                     and node.func.attr == 'run' and node.args and isinstance(node.args[0], ast.List)
                     and (caller + '.py') in ast.get_source_segment(text, node.args[0])]
            if len(calls) != 1:
                parser.error('Exactly one actual legacy native argv required')
            legacy_calls[caller] = compile(ast.fix_missing_locations(ast.Expression(calls[0].args[0])),
                                           str(target), 'eval')
    verify.write(output / 'sources.json', {'sources': sources, 'legacy': args.legacy,
                 'manifest_sha256': args.manifest_sha256, 'jdk_members': len(dependencies['members']),
                 'python': sys.version})

    class NativePathTests(unittest.TestCase):
        def setUp(self):
            self.directory = output / self._testMethodName
            self.directory.mkdir()
            self.work = self.directory / 'canonical'
            self.work.mkdir()
            for old, new in (('tools', 'native'), ('state', 'input')):
                shutil.copytree(retained / old, self.work / new)
                verify.verify(self.work / new, frozen[old])

        def execute(self, caller, number):
            selected = self.directory / ('result-%d' % number)
            selected.mkdir()
            self.assertTrue(all(digest(Path(path)) == value for path, value in sources.items()))
            verify.verify(jdk, dependencies['members'])
            if args.legacy:
                argv = eval(legacy_calls[caller], {'__builtins__': {}, 'sys': sys, 'str': str,
                            'TOOLS': self.work / 'native', 'OUT': self.work / 'input',
                            'numerical_file': selected / 'aggregate.json'})
                receipt = verify.run(selected, 'native-' + caller, argv,
                    checks=((self.work / 'native', frozen['tools']),
                            (self.work / 'input', frozen['state']), (jdk, dependencies['members'])))
                value = read(selected / ('aggregate.json' if caller == 'aggregate' else 'native-evaluate.stdout'))
                status = receipt['returncode']
            else:
                receipt, value = candidate.replay_native(selected, self.work, caller)
                status = receipt['returncode']
            verify.verify(self.work / 'native', frozen['tools'])
            verify.verify(self.work / 'input', frozen['state'])
            verify.verify(jdk, dependencies['members'])
            self.assertEqual(status, 0 if value['verdict'] == 'Passed' else 1)
            self.assertTrue(all(digest(Path(path)) == value for path, value in sources.items()))
            return selected, value

        def declared(self, caller):
            _, value = self.execute(caller, 1)
            recording = self.work / (caller + '-jfr')
            self.assertTrue(recording.is_dir(), 'Native reader did not consume the declared JFR directory')
            if caller == 'evaluate':
                self.assertEqual(value['jfr_recordings']['evidence_directory'], str(recording))

        def repeat(self, caller):
            first, _ = self.execute(caller, 1)
            self.work.rename(self.directory / 'retained-first-work')
            self.work.mkdir()
            for old, new in (('tools', 'native'), ('state', 'input')):
                shutil.copytree(retained / old, self.work / new)
            second, _ = self.execute(caller, 2)
            names = [caller_name + suffix for caller_name in ('native-' + caller,)
                     for suffix in ('.stdout', '.stderr')]
            if caller == 'aggregate':
                names.append('aggregate.json')
            for name in names:
                with self.subTest(artifact=name):
                    self.assertEqual((first / name).read_bytes(), (second / name).read_bytes(),
                                     'Complete native bytes differ')

        def test_evaluate_declared_path(self):
            self.declared('evaluate')

        def test_aggregate_declared_path(self):
            self.declared('aggregate')

        def test_evaluate_complete_bytes(self):
            self.repeat('evaluate')

        def test_aggregate_complete_bytes(self):
            self.repeat('aggregate')

        def test_existing_work_is_preserved(self):
            roots = {'tools': retained / 'tools', 'input': retained / 'state', 'case': retained / 'case'}
            with self.assertRaisesRegex(RuntimeError, 'Existing replay work must be preserved'):
                candidate.validate_work_root(self.work, roots, self.directory / 'output')
            verify.verify(self.work / 'input', frozen['state'])

        def test_relative_work_is_refused(self):
            with self.assertRaisesRegex(RuntimeError, 'Canonical absolute work root required'):
                candidate.validate_work_root(Path('relative'), {'input': retained}, self.directory / 'output')

        def test_overlapping_work_is_refused(self):
            destination = self.directory / 'new-work'
            with self.assertRaisesRegex(RuntimeError, 'Replay work overlaps'):
                candidate.validate_work_root(destination, {'input': retained}, destination / 'output')

    names = unittest.defaultTestLoader.getTestCaseNames(NativePathTests)
    if args.legacy:
        names = [name for name in names if 'work' not in name]
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(NativePathTests(name) for name in names))
    for name in ('state', 'tools'):
        verify.verify(retained / name, frozen[name])
    verify.verify(jdk, dependencies['members'])
    unchanged = all(digest(Path(path)) == value for path, value in sources.items())
    record = {'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
              'skipped': len(result.skipped), 'failed_checks': [test.id() for test, _ in result.failures],
              'sources_unchanged': unchanged, 'originals_unchanged': True,
              'scope': 'Actual native paths and filesystem guards only; no positive fault lifecycle or recipient fixture',
              'result': 'Passed' if result.wasSuccessful() and unchanged else 'Failed'}
    verify.write(output / 'result.json', record)
    return 0 if record['result'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
