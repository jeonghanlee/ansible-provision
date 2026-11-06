#!/usr/bin/env python3
"""Verify kernel query receipts with the real collector and local journalctl."""

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

QUERY_TIMEOUT_SECONDS = 60
CLI_TIMEOUT_SECONDS = 90
TOOLS = Path(__file__).resolve().parent
OUTPUT = None
COLLECT = None


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def execute(command, destination):
    began = time.monotonic()
    started = utcnow().isoformat()
    result = subprocess.run(command, capture_output=True, timeout=CLI_TIMEOUT_SECONDS)
    destination.with_suffix('.stdout').write_bytes(result.stdout)
    destination.with_suffix('.stderr').write_bytes(result.stderr)
    save(destination.with_suffix('.json'), {
        'command': command, 'returncode': result.returncode, 'started_at': started,
        'finished_at': utcnow().isoformat(), 'elapsed_seconds': time.monotonic() - began})
    return result


class KernelQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        probe = execute(['journalctl', '-b', '--no-pager', '-o', 'json', '-n', '1'],
                        OUTPUT / 'anchor-probe')
        if probe.returncode or not probe.stdout.strip():
            raise RuntimeError('A readable current-boot journal record is required')
        cls.anchor = json.loads(probe.stdout.splitlines()[-1])
        cls.cursor = cls.anchor['__CURSOR']

    def setUp(self):
        self.directory = OUTPUT / self._testMethodName
        self.directory.mkdir()
        self.raw = self.directory / 'raw'
        self.raw.mkdir()
        self.now = utcnow()
        self.since = self.now.strftime('%Y-%m-%d %H:%M:%S UTC')
        self.previous = {'kernel_journal_cursor': self.cursor, 'kernel_journal_since': self.since}

    def command(self, cursor):
        return ['journalctl', '-b', '--no-pager', '--all', '-o', 'json', '--cursor', cursor]

    def reverse_command(self):
        return ['journalctl', '-b', '--no-pager', '-o', 'json', '--reverse',
                '--until', self.previous['kernel_journal_since'], '--lines=1']

    def call(self):
        save(self.directory / 'input.json', {'previous': self.previous, 'now': self.now.isoformat()})
        return COLLECT.collect_kernel(self.raw, self.previous, self.now)

    def receipt(self, name, command, status, cursor):
        path = self.raw / (name + '.jsonl.receipt.json')
        self.assertTrue(path.is_file(), 'query receipt exists')
        record = json.loads(path.read_text())
        self.assertEqual(record['command'], command, 'original argument array')
        self.assertEqual(record['returncode'], status, 'native return code')
        self.assertEqual(record['interval'], {
            'previous_cursor': self.previous.get('kernel_journal_cursor'),
            'since': self.previous['kernel_journal_since'],
            'sampled_at': self.now.isoformat(), 'query_cursor': cursor}, 'original query interval')
        self.assertEqual(record['timeout_seconds'], QUERY_TIMEOUT_SECONDS)
        start = datetime.datetime.fromisoformat(record['started_at'])
        finish = datetime.datetime.fromisoformat(record['finished_at'])
        self.assertLessEqual(self.now, start)
        self.assertLessEqual(start, finish)
        self.assertLessEqual(finish, utcnow())
        self.assertGreaterEqual(record['elapsed_seconds'], 0)
        self.assertLess(record['elapsed_seconds'], CLI_TIMEOUT_SECONDS)
        self.assertNotIn('error', record)
        return record

    def refused(self, name, command, cursor):
        native = execute(command, self.directory / 'independent-query')
        self.assertNotEqual(native.returncode, 0, 'fault reached native journalctl')
        with self.assertRaisesRegex(RuntimeError, 'Kernel journal collection failed'):
            self.call()
        self.receipt(name, command, native.returncode, cursor)
        self.assertEqual((self.raw / (name + '.jsonl')).read_bytes(), native.stdout, 'native stdout bytes')
        self.assertEqual((self.raw / (name + '.stderr')).read_bytes(), native.stderr, 'native stderr bytes')
        self.assertFalse((self.raw / 'kernel-journal.jsonl').exists())

    def test_cursor_refusal(self):
        self.previous['kernel_journal_cursor'] = 'invalid:' + self.cursor
        cursor = self.previous['kernel_journal_cursor']
        self.refused('kernel-checkpoint-journal', self.command(cursor), cursor)

    def test_initial_query_refusal(self):
        self.previous.pop('kernel_journal_cursor')
        self.previous['kernel_journal_since'] = 'invalid-kernel-query-time'
        self.refused('journal-retention-query', self.reverse_command(), None)

    def test_existing_cursor(self):
        result = self.call()
        self.receipt('kernel-checkpoint-journal', self.command(self.cursor), 0, self.cursor)
        rows = (self.raw / 'kernel-checkpoint-journal.jsonl').read_bytes().splitlines()
        self.assertEqual(json.loads(rows[0])['__CURSOR'], self.cursor)
        self.assertTrue(result['coverage_complete'])
        self.assertEqual(result['cursor'], json.loads(rows[-1])['__CURSOR'])
        self.assertEqual(result['previous_cursor'], self.cursor)

    def test_initial_query(self):
        self.previous.pop('kernel_journal_cursor')
        result = self.call()
        self.receipt('journal-retention-query', self.reverse_command(), 0, None)
        anchor = json.loads((self.raw / 'journal-retention-before.json').read_text())
        self.receipt('kernel-checkpoint-journal', self.command(anchor['__CURSOR']), 0, anchor['__CURSOR'])
        self.assertTrue(result['coverage_complete'])
        self.assertIsNone(result['previous_cursor'])

    def test_collector_cli_refusal(self):
        self.previous['kernel_journal_cursor'] = 'invalid:' + self.cursor
        self.previous['journal_since'] = self.since
        state = self.directory / 'state.json'
        save(state, self.previous)
        native = execute(self.command(self.previous['kernel_journal_cursor']),
                         self.directory / 'independent-query')
        self.assertNotEqual(native.returncode, 0, 'fault reached native journalctl')
        result = execute([sys.executable, '-B', str(TOOLS / 'collect.py'), str(self.directory),
                          str(TOOLS.parent / 'fixtures' / 'pvs-all.csv'), '--journal-only'],
                         self.directory / 'collector-cli')
        self.assertEqual(result.returncode, 1, 'collector reports unsuccessful sample')
        summary = json.loads((self.directory / 'latest.json').read_text())
        self.assertTrue(any(row['check'] == 'kernel_journal' for row in summary['errors']))
        self.assertNotIn('kernel_journal', summary)
        self.assertEqual(json.loads(state.read_text())['kernel_journal_cursor'],
                         self.previous['kernel_journal_cursor'], 'failed cursor is not advanced')
        self.raw = Path(summary['raw_directory'])
        self.now = datetime.datetime.fromisoformat(summary['observed_at'])
        self.receipt('kernel-checkpoint-journal', self.command(self.previous['kernel_journal_cursor']),
                     native.returncode, self.previous['kernel_journal_cursor'])
        self.assertEqual((self.raw / 'kernel-checkpoint-journal.stderr').read_bytes(), native.stderr)
        self.assertEqual((self.raw / 'kernel-checkpoint-journal.jsonl').read_bytes(), native.stdout)


def main():
    global TOOLS, OUTPUT, COLLECT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tools', type=Path, default=TOOLS)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', choices=unittest.defaultTestLoader.getTestCaseNames(KernelQueryTests))
    args = parser.parse_args()
    TOOLS, OUTPUT = args.tools.resolve(), args.output.resolve()
    os.umask(0o077)
    OUTPUT.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(TOOLS))
    COLLECT = importlib.import_module('collect')
    sources = {name: hashlib.sha256((TOOLS / name).read_bytes()).hexdigest()
               for name in COLLECT.contract.BUNDLE_FILES}
    save(OUTPUT / 'sources.json', {'tools': str(TOOLS), 'files': sources,
         'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    execute(['journalctl', '--version'], OUTPUT / 'journalctl-version')
    suite = (unittest.TestSuite([KernelQueryTests(args.case)]) if args.case else
             unittest.defaultTestLoader.loadTestsFromTestCase(KernelQueryTests))
    started, began = utcnow(), time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    unchanged = all(hashlib.sha256((TOOLS / name).read_bytes()).hexdigest() == digest
                    for name, digest in sources.items())
    save(OUTPUT / 'result.json', {
        'started_at': started.isoformat(), 'finished_at': utcnow().isoformat(),
        'elapsed_seconds': time.monotonic() - began, 'tests_run': result.testsRun,
        'failures': [(test.id(), detail) for test, detail in result.failures],
        'errors': [(test.id(), detail) for test, detail in result.errors],
        'sources_unchanged': unchanged,
        'scope': 'Local current-boot query receipts only; no rotation, timeout or historical interval proof',
        'result': 'Passed' if result.wasSuccessful() and unchanged else 'Failed'})
    return 0 if result.wasSuccessful() and unchanged else 1


if __name__ == '__main__':
    raise SystemExit(main())
