#!/usr/bin/env python3
"""Run shipped tools and fixtures with only external system boundaries replaced."""

import collections
import contextlib
import csv
import datetime
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import aggregate
import collect
import contract
import evidence
import evaluate
import observe

HERE = Path(__file__).resolve().parent
FIXTURES = HERE.parent / 'fixtures'
ARCHIVES = os.environ.get('ETL_SOAK_ARCHIVE_ROOT')
EXTRACTED = os.environ.get('ETL_SOAK_EXTRACTED_ROOT')


def module(name):
    source = HERE / (name + '.py')
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), source)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class ContractTests(unittest.TestCase):
    @unittest.skipUnless(EXTRACTED, 'Actual retained observation inputs are required')
    def test_fresh_initialization_refuses_real_prior_observation_without_changes(self):
        initializer = module('initialize-fresh')
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'out'
            shutil.copytree(Path(EXTRACTED) / 'shortened', out)
            before = {str(path.relative_to(out)): contract.digest(path)
                      for path in out.rglob('*') if path.is_file()}
            with patch.object(observe, 'OUT', out):
                with self.assertRaisesRegex(RuntimeError, 'no prior observation'):
                    initializer.instruments()
                with self.assertRaisesRegex(RuntimeError, 'no prior observation'):
                    initializer.prepare(None, None, 86400, 'shortened')
            after = {str(path.relative_to(out)): contract.digest(path)
                     for path in out.rglob('*') if path.is_file()}
            self.assertEqual(after, before)

    def test_fresh_preparation_refuses_absent_measurements_without_writing_files(self):
        initializer = module('initialize-fresh')
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            with patch.object(observe, 'OUT', out):
                with self.assertRaisesRegex(RuntimeError, 'measurement evidence is required'):
                    initializer.prepare(None, None, 86400, 'shortened')
            self.assertEqual(list(out.iterdir()), [])

    @unittest.skipUnless(EXTRACTED and ARCHIVES, 'Real completed deployment and fixture evidence is required')
    def test_prepare_refuses_missing_retention_proof_without_modifying_real_inputs(self):
        preparation = module('prepare-retest')
        original = Path(EXTRACTED) / 'shortened'
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'out'
            shutil.copytree(original, out)
            before = {str(path.relative_to(out)): contract.digest(path)
                      for path in out.rglob('*') if path.is_file()}
            with patch.object(observe, 'OUT', out):
                with self.assertRaisesRegex(RuntimeError, 'journal retention preparation evidence'):
                    preparation.prepare(HERE, contract.CAPTURE_RESERVE, out / 'capacity.json',
                                        86400, 'shortened')
            after = {str(path.relative_to(out)): contract.digest(path)
                     for path in out.rglob('*') if path.is_file()}
            self.assertEqual(after, before)
            self.assertEqual(list(out.parent.iterdir()), [out])

    def test_helper_and_jfr_changes_invalidate_frozen_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in contract.BUNDLE_FILES:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(HERE / name, target)
            contract.freeze(root)
            original = contract.verify_bundle(root)
            for name in ('resource_helpers.py', 'heap.jfc'):
                target = root / name
                data = target.read_bytes()
                target.write_bytes(data + b'\n')
                with self.assertRaisesRegex(RuntimeError, 'frozen complete bundle'):
                    contract.verify_bundle(root)
                target.write_bytes(data)
                self.assertEqual(contract.verify_bundle(root), original)
            frozen = json.loads((root / 'bundle.json').read_text())
            frozen['files']['unused.py'] = '0' * 64
            (root / 'bundle.json').write_text(json.dumps(frozen))
            with self.assertRaises(RuntimeError):
                contract.verify_bundle(root)

    def test_duration_and_chain_preparation_are_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for duration in contract.DURATIONS:
                for chain in contract.CHAINS:
                    (root / 'preparation.json').write_text(json.dumps({'schema': contract.SCHEMA, 'duration_seconds': duration,
                        'configuration': contract.chain_configuration(chain)}))
                    self.assertEqual(contract.preparation(root, duration, chain)['duration_seconds'], duration)
                    with self.assertRaises(RuntimeError):
                        contract.preparation(root, duration, 'default' if chain == 'shortened' else 'shortened')
                    with self.assertRaises(RuntimeError):
                        contract.preparation(root, 86400 if duration == 7200 else 7200, chain)
                    record = json.loads((root / 'preparation.json').read_text())
                    record['schema'] = 4
                    (root / 'preparation.json').write_text(json.dumps(record))
                    with self.assertRaisesRegex(RuntimeError, 'current schema'):
                        contract.preparation(root, duration, chain)

    def test_no_arbitrary_duration_is_accepted(self):
        for value in (7199, 86399, 86401, True, 86400.0):
            with self.assertRaises(RuntimeError):
                contract.validate_duration(value)

    def test_real_chain_verifier_queries_all_shipped_pvs_and_rejects_mismatch(self):
        verifier = module('verify-chain')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            out, tools = root / 'out', root / 'tools'
            out.mkdir(); tools.mkdir()
            shutil.copyfile(FIXTURES / 'pvs-all.csv', tools / 'pvs-all.csv')
            for name in contract.BUNDLE_FILES:
                target = tools / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(HERE / name, target)
            contract.freeze(tools)
            queried = set()
            class Response(io.BytesIO):
                status = 200
            def transport(url, **kwargs):
                import urllib.parse
                queried.add(urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)['pv'][0])
                stores = ['pb://localhost/arch/' + tier + '?partitionGranularity=' + granularity + '&hold=2'
                          for tier, granularity in zip(('sts', 'mts', 'lts'), contract.CHAINS['shortened'])]
                return Response(json.dumps({'dataStores': stores}).encode())
            with patch.object(observe, 'TOOLS', tools), patch.object(observe, 'OUT', out), \
                    patch('urllib.request.urlopen', side_effect=transport), contextlib.redirect_stdout(io.StringIO()):
                (out / 'preparation.json').write_text(json.dumps({'schema': contract.SCHEMA, 'duration_seconds': 86400,
                    'configuration': contract.chain_configuration('shortened')}))
                verifier.verify('shortened', 86400)
                self.assertEqual(len(queried), 903)
                before = (out / 'chain-verification.json').read_bytes()
                (out / 'preparation.json').write_text(json.dumps({'schema': contract.SCHEMA, 'duration_seconds': 86400,
                    'configuration': contract.chain_configuration('default')}))
                with self.assertRaisesRegex(RuntimeError, 'does not match selected chain'):
                    verifier.verify('default', 86400)
                self.assertEqual((out / 'chain-verification.json').read_bytes(), before)

    def test_capacity_projection_binds_measured_sources_and_current_age(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            end = datetime.datetime.now(datetime.timezone.utc)
            measurement = {'start': {'observed_at': (end - datetime.timedelta(seconds=300)).isoformat(),
                                     'boot_id': observe.BOOT.read_text().strip(),
                                     'bytes': dict.fromkeys(contract.GROWTH_FIELDS, 100)},
                           'end': {'observed_at': end.isoformat(), 'boot_id': observe.BOOT.read_text().strip(),
                                   'bytes': dict.fromkeys(contract.GROWTH_FIELDS, 400)}}
            measured = root / 'measured.json'
            measured.write_text(json.dumps(measurement))
            history = json.loads(json.dumps(measurement))
            for sample in ('start', 'end'):
                history[sample]['observed_at'] = (datetime.datetime.fromisoformat(history[sample]['observed_at']) -
                                                datetime.timedelta(days=1)).isoformat()
            historical = root / 'historical.json'
            historical.write_text(json.dumps(history))
            configuration = contract.chain_configuration('default')
            value = {'schema': 1, 'duration_seconds': 86400, 'configuration': configuration,
                     'windows': [{'role': role, 'source_path': path.name,
                                  'source_sha256': contract.digest(path)} for role, path in
                                 (('historical', historical), ('current', measured))]}
            source = root / 'capacity.json'
            source.write_text(json.dumps(value))
            self.assertEqual(contract.capacity_projection(source, 86400, configuration),
                             contract.CAPTURE_RESERVE + 5 * 86400)
            with self.assertRaisesRegex(RuntimeError, 'another duration'):
                contract.capacity_projection(source, 7200, configuration)
            measured.write_text(json.dumps(measurement) + '\n')
            with self.assertRaisesRegex(RuntimeError, 'source changed'):
                contract.capacity_projection(source, 86400, configuration)

    def test_gc_log_incremental_capture_preserves_rotated_file_and_rejects_truncation(self):
        import measure
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            (out / 'jvm').mkdir()
            source = out / 'jvm' / 'gc-123-test.log'
            source.write_bytes(b'first\npartial')
            raw = out / 'raw1'; raw.mkdir()
            measure.gc_logs(out, raw, '123', False)
            self.assertEqual((raw / source.name).read_bytes(), b'first\n')
            with source.open('ab') as stream:
                stream.write(b' complete\n')
            rotated = source.with_suffix('.log.0')
            source.rename(rotated)
            raw2 = out / 'raw2'; raw2.mkdir()
            measure.gc_logs(out, raw2, '123', False)
            self.assertEqual((raw2 / rotated.name).read_bytes(), b'partial complete\n')
            rotated.write_bytes(b'changed\n')
            raw3 = out / 'raw3'; raw3.mkdir()
            with self.assertRaisesRegex(RuntimeError, 'truncated'):
                measure.gc_logs(out, raw3, '123', False)

    def test_initial_application_then_existing_verification_preserves_real_fixture(self):
        installer, application = module('install-fixture'), module('apply-fixture')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tools, units, out = (root / name for name in ('tools', 'units', 'out'))
            for path in (tools, units, out):
                path.mkdir()
            for name in ('aasoak.db', 'load1.db', 'load2.db', 'pvs-all.csv'):
                shutil.copyfile(FIXTURES / name, tools / name)
            config = root / 'archappl.conf'
            config.write_text('EPICS_CA_ADDR_LIST="original"\nEPICS_CA_AUTO_ADDR_LIST="YES"\n')
            calls = []

            def transport(args, **kwargs):
                calls.append(args)
                stdout = ''
                if args[0] == 'mysql':
                    stdout = '0'
                elif args[0] == application.measure.CAGET:
                    stdout = ' '.join(['-1'] * 20)
                    self.assertEqual(args[-20:], [name + suffix for name in
                        ['AASOAK:DB:CH' + str(n).zfill(2) for n in range(1, 11)] for suffix in ('.MDEL', '.ADEL')])
                elif args[:2] == ['systemctl', 'show']:
                    base = (units / collect.IOC_UNIT).read_text()
                    command = next(line[len('ExecStart='):] for line in base.splitlines() if line.startswith('ExecStart='))
                    stdout = '{ path=' + installer.SOFTIOC + ' ; argv[]=' + command + ' -d ' + str(tools / application.OVERRIDE_NAME) + ' ; }'
                elif args[0] not in ('systemctl', 'systemd-analyze'):
                    raise AssertionError('Unexpected external command')
                if kwargs.get('stdout') == subprocess.PIPE and not kwargs.get('text'):
                    stdout = stdout.encode()
                return subprocess.CompletedProcess(args, 0, stdout, '')

            with patch.object(installer, 'TOOLS', tools), patch.object(installer, 'OUT', out), \
                    patch.object(installer, 'UNITS', units), patch.object(installer, 'CONF', config), \
                    patch.object(observe, 'TOOLS', tools), patch.object(observe, 'OUT', out), \
                    patch.object(observe, 'UNITS', units), patch('subprocess.run', side_effect=transport), \
                    contextlib.redirect_stdout(io.StringIO()):
                installer.main()
                application.apply(FIXTURES / 'retest-deadband.db')
                hashes = {str(path.relative_to(root)): contract.digest(path) for path in root.rglob('*') if path.is_file()}
                application.verify_existing(FIXTURES / 'retest-deadband.db')
                application.verify_existing(FIXTURES / 'retest-deadband.db')
                self.assertEqual({name: contract.digest(root / name) for name in hashes}, hashes)
                with self.assertRaisesRegex(RuntimeError, 'refusing replacement'):
                    application.apply(FIXTURES / 'retest-deadband.db')
                original = (out / 'fixture-adjustment.json').read_bytes()
                override = tools / application.OVERRIDE_NAME
                override.write_bytes(override.read_bytes() + b'\n')
                with self.assertRaisesRegex(RuntimeError, 'conflicts'):
                    application.verify_existing(FIXTURES / 'retest-deadband.db')
                self.assertEqual((out / 'fixture-adjustment.json').read_bytes(), original)
                self.assertEqual(json.loads((out / 'fixture-verification.json').read_text())['verified']['verified_records'], 10)

    def test_kernel_cursor_crosses_midnight_and_loss_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory)
            previous = {'kernel_journal_cursor': 'prior-day-cursor', 'kernel_journal_since': '2026-09-29 23:59:00 UTC'}
            rows = [{'__CURSOR': 'prior-day-cursor', 'MESSAGE': 'previous'},
                    {'__CURSOR': 'new-day-cursor', '__REALTIME_TIMESTAMP': '1790726401000000', 'MESSAGE': 'normal'}]
            def transport(args, **kwargs):
                self.assertIn('prior-day-cursor', args)
                self.assertNotIn('--since', args)
                return subprocess.CompletedProcess(args, 0, '\n'.join(json.dumps(row) for row in rows), '')
            with patch('subprocess.run', side_effect=transport):
                result = collect.collect_kernel(raw, previous, datetime.datetime(2026, 9, 30, tzinfo=datetime.timezone.utc))
                self.assertTrue(result['coverage_complete'])
                self.assertEqual(result['cursor'], 'new-day-cursor')
                rows.pop(0)
                with self.assertRaisesRegex(RuntimeError, 'cursor is unavailable'):
                    collect.collect_kernel(raw, previous, datetime.datetime.now(datetime.timezone.utc))

    def test_initial_kernel_boundary_requires_reverse_journal_lookup(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory)
            boundary = datetime.datetime(2026, 9, 30, tzinfo=datetime.timezone.utc)
            before = {'__CURSOR': 'retained-before-window',
                      '__REALTIME_TIMESTAMP': str(int(boundary.timestamp() - 1) * 1000000)}
            event = {'__CURSOR': 'in-window-kernel', 'MESSAGE': 'normal'}
            def transport(args, **kwargs):
                if '--until' in args:
                    output = json.dumps(before) if '--reverse' in args else ''
                else:
                    output = json.dumps(event)
                return subprocess.CompletedProcess(args, 0, output, '')
            with patch('subprocess.run', side_effect=transport):
                result = collect.collect_kernel(raw, {'kernel_journal_since': '2026-09-30 00:00:00 UTC'}, boundary)
            self.assertTrue(result['coverage_complete'])
            self.assertEqual(result['cursor'], 'in-window-kernel')
            self.assertEqual(json.loads((raw / 'journal-retention-before.json').read_text()), before)

    def test_invalid_aggregate_cli_has_nonzero_status_and_json(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'aggregate.json'
            result = subprocess.run([sys.executable, '-B', str(HERE / 'aggregate.py'), '--input', directory,
                                     '--output', str(out)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            value = json.loads(out.read_text())
            self.assertEqual(value['verdict'], 'Incomplete')
            self.assertIn('manifest', value['missing_coverage'])


@unittest.skipUnless(ARCHIVES, 'ETL_SOAK_ARCHIVE_ROOT must name retained real 24-hour archives')
class RetainedExportsTests(unittest.TestCase):
    def inputs(self, label, name):
        with tarfile.open(Path(ARCHIVES) / ('analysis-24h-' + label + '.tar')) as archive:
            return archive.extractfile(name).read()

    def test_actual_two_chain_schedules_match_pinned_grid(self):
        for label, counts in (('shortened', (288, 24)), ('default', (24, 3))):
            manifest = json.loads(self.inputs(label, 'observation.json'))
            start = datetime.datetime.fromisoformat(manifest['started_at'])
            end = datetime.datetime.fromisoformat(manifest['earliest_finish_at'])
            expected = contract.expected_firings(start, end, contract.chain_configuration(label))
            self.assertEqual(tuple(sum(row['transition'] == index for row in expected) for index in (0, 1)), counts)
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'passes.jsonl'
                path.write_bytes(self.inputs(label, 'passes.jsonl'))
                actual = evaluate.pass_records(path)
            selected = {(row['transition'], row['cadence'], evidence.timestamp_ns(row['plannedAt']))
                        for row in actual if evidence.timestamp_ns(manifest['started_at']) <=
                        evidence.timestamp_ns(row['plannedAt']) < evidence.timestamp_ns(manifest['earliest_finish_at'])}
            self.assertEqual(selected, {(row['transition'], row['cadence'], evidence.timestamp_ns(row['planned_at'])) for row in expected})

    def test_real_overlap_deduplication_preserves_events_and_pause_totals(self):
        for label in ('shortened', 'default'):
            for kind, filename in (('heap', 'gc-heap.csv'), ('collection', 'gc-collections.csv'), ('pause', 'gc-pauses.csv')):
                rows = list(csv.DictReader(io.StringIO(self.inputs(label, filename).decode())))
                unique, report = evidence.deduplicate(rows, kind)
                again, repeated = evidence.deduplicate(rows + rows, kind)
                self.assertEqual(unique, again)
                self.assertEqual(repeated['unique_events'], report['unique_events'])
                self.assertLessEqual(report['maximum_jitter_ns'], 2000)
                exact = len({tuple(sorted(row.items())) for row in rows})
                if kind == 'heap':
                    self.assertGreater(exact, report['unique_events'])
                    independent = {tuple(row[field] for field in ('component', 'pid', 'gc_id', 'when', 'heap_bytes')) for row in rows}
                    self.assertEqual(len(unique), len(independent))
                if kind == 'pause':
                    self.assertEqual(sum(evidence.duration_ns(row['duration']) for row in unique),
                                     sum(evidence.duration_ns(row['duration']) for row in again))

    def test_conflicting_real_heap_event_is_incomplete(self):
        rows = list(csv.DictReader(io.StringIO(self.inputs('shortened', 'gc-heap.csv').decode())))
        conflict = dict(rows[0], heap_bytes=str(int(rows[0]['heap_bytes']) + 1))
        with self.assertRaisesRegex(RuntimeError, 'Conflicting GC payloads'):
            evidence.deduplicate([*rows, conflict], 'heap')

    def test_actual_rates_keep_cumulative_semantics_and_exclude_benchmarks(self):
        with tarfile.open(Path(ARCHIVES) / 'analysis-24h-default.tar') as archive:
            path = next(row.name for row in archive.getmembers() if row.name.endswith('/metrics.json'))
            metrics = json.load(archive.extractfile(path))
        rates = collect.event_rates(metrics, '2026-09-29T01:10:00+00:00')
        self.assertEqual(len(rates), 2)
        self.assertTrue(all(row['numeric_value'] > 0 for row in rates))
        self.assertTrue(all('connection-dependent' in row['interval'] for row in rates))
        self.assertFalse(any('Benchmark' in row['name'] for row in rates))


@unittest.skipUnless(EXTRACTED, 'ETL_SOAK_EXTRACTED_ROOT must name coherent retained real evidence')
class AggregateReplayTests(unittest.TestCase):
    def test_real_aggregate_cli_is_reproducible_and_retains_original_failures(self):
        for label in ('shortened', 'default'):
            with tempfile.TemporaryDirectory() as directory:
                first, second = Path(directory) / 'first.json', Path(directory) / 'second.json'
                command = [sys.executable, '-B', str(HERE / 'aggregate.py'), '--input', str(Path(EXTRACTED) / label)]
                run = subprocess.run([*command, '--output', str(first)], capture_output=True, text=True)
                self.assertNotEqual(run.returncode, 0)
                value = json.loads(first.read_text())
                self.assertEqual(value['verdict'], 'Incomplete')
                self.assertGreater(value['rate_coverage']['full_samples'], 280)
                self.assertIn('retrieval_outcomes', value['failed_assertions'])
                self.assertEqual(value['transitions']['0']['pass_count'], 288 if label == 'shortened' else 24)
                self.assertEqual(value['transitions']['1']['pass_count'], 24 if label == 'shortened' else 3)
                for component in evidence.COMPONENTS:
                    for row in value['gc_reconciliation'][component + '_logs'].values():
                        self.assertEqual(row['jfr_ids'], row['covered_ids'])
                replay = subprocess.run([*command, '--output', str(second), '--compare', str(first)], capture_output=True, text=True)
                self.assertNotEqual(replay.returncode, 0)
                self.assertFalse(json.loads(replay.stdout)['comparison_mismatch'])
                self.assertEqual(json.loads(second.read_text()), value)
                changed = dict(value, schema=-1)
                first.write_text(json.dumps(changed))
                mismatch = subprocess.run([*command, '--output', str(second), '--compare', str(first)], capture_output=True, text=True)
                self.assertTrue(json.loads(mismatch.stdout)['comparison_mismatch'])


    def test_cli_missing_input_preserves_preceding_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            source = Path(EXTRACTED) / 'shortened'
            for name in ('observation.json', 'shutdown.json', 'passes.jsonl'):
                shutil.copyfile(source / name, out / name)
            terminal = json.loads((out / 'shutdown.json').read_text())
            terminal.setdefault('errors', []).append('retained_terminal_failure')
            (out / 'shutdown.json').write_text(json.dumps(terminal))
            output = out / 'aggregate.json'
            run = subprocess.run([sys.executable, '-B', str(HERE / 'aggregate.py'), '--input', str(out), '--output', str(output)],
                                 capture_output=True, text=True)
            value = json.loads(output.read_text())
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('retained_terminal_failure', value['failed_assertions'])
            self.assertIn('gc-heap.csv', value['missing_coverage'])


if __name__ == '__main__':
    unittest.main()
