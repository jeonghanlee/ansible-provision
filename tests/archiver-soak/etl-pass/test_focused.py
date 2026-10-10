#!/usr/bin/env python3
"""Check focused evidence parsing; these tests do not execute deployed ETL."""

import copy
import datetime
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
from pathlib import Path
import tempfile
import tarfile
import unittest
from unittest.mock import patch

import collect
import contract
import focused


class OfflinePreparationTests(unittest.TestCase):
    """Exercise real filesystem preservation; these tests do not run appliance ETL."""

    def storage(self, directory):
        base = Path(directory)
        evidence = base / 'evidence'
        evidence.mkdir()
        roots = [base / name for name in ('sts', 'mts', 'lts')]
        source = Path(focused.__file__).parent.parent / 'fixtures/pvs-all.csv'
        for path in roots:
            path.mkdir(mode=0o750)
            shutil.copyfile(source, path / 'registered-input.csv')
        return evidence, roots

    def test_archive_and_rename_preserve_bytes_and_empty_active_roots(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence, roots = self.storage(directory)
            originals = [focused.tree_manifest(path) for path in roots]
            proof = focused.preserve_stores(evidence, roots)
            self.assertEqual(proof['manifests'], originals)
            self.assertEqual(focused.verify_preserved_stores(evidence), proof)
            for path, manifest in zip(roots, originals):
                self.assertEqual(focused.tree_manifest(path), {'.': manifest['.']})
            preserved = Path(proof['moved'][0]['destination']) / 'registered-input.csv'
            with preserved.open('ab') as stream:
                stream.write(b'changed')
            with self.assertRaisesRegex(RuntimeError, 'preparation storage changed'):
                focused.verify_preserved_stores(evidence)

    def test_existing_archive_overlap_and_symlink_are_rejected_before_move(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence, roots = self.storage(directory)
            before = [focused.tree_manifest(path) for path in roots]
            (evidence / 'preparation-stores.tar.gz').write_bytes(b'occupied')
            with self.assertRaisesRegex(RuntimeError, 'destination already exists'):
                focused.preserve_stores(evidence, roots)
            self.assertEqual([focused.tree_manifest(path) for path in roots], before)
            with self.assertRaisesRegex(RuntimeError, 'overlap'):
                focused.preserve_stores(roots[0], roots)
            (roots[0] / 'linked-input').symlink_to(roots[1] / 'registered-input.csv')
            with self.assertRaisesRegex(RuntimeError, 'Unsupported storage entry'):
                focused.tree_manifest(roots[0])

    def test_partial_filesystem_failure_retains_each_original_location(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence, roots = self.storage(directory)
            originals = [focused.tree_manifest(path) for path in roots]
            rename = Path.rename
            def failing_rename(path, target):
                if path == roots[1]:
                    raise OSError('Injected outer filesystem failure')
                return rename(path, target)
            with patch.object(Path, 'rename', failing_rename):
                with self.assertRaisesRegex(OSError, 'outer filesystem failure'):
                    focused.preserve_stores(evidence, roots)
            proof = json.loads((evidence / 'storage-preservation.json').read_text())
            self.assertEqual(len(proof['moved']), 1)
            self.assertEqual(proof['empty_roots'], [])
            self.assertFalse(roots[0].exists())
            self.assertEqual(focused.tree_manifest(evidence / 'preparation-stores/sts'), originals[0])
            for path, manifest in zip(roots[1:], originals[1:]):
                self.assertEqual(focused.tree_manifest(path), manifest)
            with self.assertRaisesRegex(RuntimeError, 'incomplete or changed'):
                focused.verify_preserved_stores(evidence)


class FocusedContractTests(unittest.TestCase):
    def test_empty_pass_poll_is_valid_and_malformed_journal_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(focused.observe.subprocess, 'run', return_value=
                              subprocess.CompletedProcess(['journalctl'], 0, '', '')):
                self.assertEqual(focused.passes(root, 'empty'), [])
                self.assertEqual((root / 'passes-empty.jsonl').read_text(), '')
            with patch.object(focused.observe.subprocess, 'run', return_value=
                              subprocess.CompletedProcess(['journalctl'], 0, 'invalid', '')):
                with self.assertRaises(json.JSONDecodeError):
                    focused.passes(root, 'invalid')

    @unittest.skipUnless(os.environ.get('FOCUSED_LOGGING_SOURCE'), 'Shipped logging configuration required')
    def test_logging_configuration_reuses_only_the_exact_dropin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install = root / 'install'
            source = install / 'etl/webapps/etl/WEB-INF/classes/log4j2.xml'
            source.parent.mkdir(parents=True)
            source.write_bytes(Path(os.environ['FOCUSED_LOGGING_SOURCE']).read_bytes())
            units = root / 'units'
            run = root / 'run'
            run.mkdir()
            with patch.object(focused, 'INSTALL', install), patch.object(focused.observe, 'UNITS', units), \
                    patch.object(focused.observe.subprocess, 'run', return_value=
                                 subprocess.CompletedProcess(['systemctl', 'daemon-reload'], 0, '', '')):
                focused.configure_debug(run)
                first = json.loads((run / 'logging-configuration.json').read_text())
                self.assertFalse(first['reused'])
                focused.configure_debug(run)
                second = json.loads((run / 'logging-configuration.json').read_text())
                self.assertTrue(second['reused'])
                self.assertEqual(first['dropin_sha256'], second['dropin_sha256'])
                self.assertEqual(first['configuration_sha256'], second['configuration_sha256'])
                Path(second['dropin']).write_text('[Service]\nEnvironment="LOG4J_CONFIGURATION_FILE=/elsewhere"\n')
                with self.assertRaisesRegex(RuntimeError, 'differs from the required path'):
                    focused.configure_debug(run)

    def test_missing_incomplete_and_stale_continuity_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            proof_path = root / 'readiness-continuity.json'
            with patch.object(focused.observe, 'OUT', root), patch.object(focused, 'ROOT', root):
                with self.assertRaises(FileNotFoundError):
                    focused.require_continuity('default')
                for proof in (
                    {'result': 'Incomplete', 'observed_at': focused.now()},
                    {'result': 'Passed', 'chain': 'shortened', 'observed_at': focused.now()},
                    {'result': 'Passed', 'chain': 'default', 'observed_at':
                     (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=121)).isoformat()},
                ):
                    proof_path.write_text(json.dumps(proof))
                    with self.assertRaisesRegex(RuntimeError, 'continuity evidence'):
                        focused.require_continuity('default')

    def test_effective_store_modes_require_real_roots_and_gather(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stores = ['pb://localhost?rootFolder=' + str(root / tier / 'ArchiverStore')
                      + '&partitionGranularity=' + granularity + '&hold=2&gather=1'
                      for tier, granularity in zip(('sts', 'mts', 'lts'), contract.CHAINS['default'])]
            with patch.object(collect, 'STORE', root):
                value = focused.settings('default', {'dataStores': stores}, {})
                self.assertEqual(value['modes'][0]['gather'], '1')
                for invalid, expected in (('&gather=0', 'gather'),
                                          ('&gather=1&hold=3', 'hold')):
                    changed = stores.copy()
                    changed[0] = changed[0].replace('&gather=1', invalid)
                    with self.assertRaisesRegex(RuntimeError, expected):
                        focused.settings('default', {'dataStores': changed}, {})
                changed = stores.copy()
                changed[0] += '&compress=GZIP'
                with self.assertRaisesRegex(RuntimeError, 'uncompressed'):
                    focused.settings('default', {'dataStores': changed}, {})

    def test_regular_pass_requires_every_transition_and_unique_grid_identity(self):
        # Parser input represents journal fields, not a substituted ETL execution.
        rows = []
        start = 1791331200
        config = contract.chain_configuration('default')
        def stamp(seconds):
            return datetime.datetime.fromtimestamp(seconds, datetime.timezone.utc).isoformat()
        for transition, (cadence, offset) in enumerate(zip(config['cadences'], config['offsets'])):
            planned = ((start - offset) // cadence + 1) * cadence + offset
            row = {'transition': transition, 'cadence': cadence, 'invocation_id': 'current',
                   'pvCount': '903', 'jobsRun': '903', 'overrun': 'false', 'aborted': 'false',
                   'plannedAt': stamp(planned), 'startedAt': stamp(planned + 1),
                   'endedAt': stamp(planned + 2), 'processingTime': stamp(planned - 59),
                   'jobsFailed': '0', 'jobsAborted': '0', 'jobsSkipped': '0', 'streamsDeletedForSpace': '0'}
            startup = dict(row, plannedAt=stamp(start - 30), startedAt=stamp(start),
                           endedAt=stamp(start + 1), processingTime=stamp(start - 60))
            rows.extend((startup, row))
        self.assertEqual(len(focused.regular_passes(rows, 'default', 'current')), 2)
        self.assertIsNone(focused.regular_passes(rows[:2], 'default', 'current'))
        self.assertIsNone(focused.regular_passes(rows, 'default', 'previous'))
        for key in ('jobsFailed', 'jobsAborted', 'jobsSkipped', 'streamsDeletedForSpace'):
            changed = copy.deepcopy(rows)
            changed[-1][key] = '1'
            with self.assertRaisesRegex(RuntimeError, 'execution contract'):
                focused.regular_passes(changed, 'default', 'current')
        with self.assertRaisesRegex(RuntimeError, 'Duplicate'):
            focused.regular_passes(rows + [dict(rows[-1])], 'default', 'current')
        changed = copy.deepcopy(rows)
        changed[-1]['processingTime'] = changed[-1]['plannedAt']
        with self.assertRaisesRegex(RuntimeError, 'margin'):
            focused.regular_passes(changed, 'default', 'current')


@unittest.skipUnless(os.environ.get('FOCUSED_RETAINED_ROOT'), 'Actual retained PB/HTTP evidence required')
class RetainedFocusedCheckerTests(unittest.TestCase):
    """Replay actual decoded records; this does not rerun ETL or prove deployment."""

    def setUp(self):
        self.root = Path(os.environ['FOCUSED_RETAINED_ROOT'])
        self.specs = json.loads((self.root / 'manifest.json').read_text())['pvs']
        self.baseline = json.loads((self.root / 'physical-baseline.json').read_text())
        self.after = json.loads((self.root / 'physical-after-scheduled.json').read_text())

    def test_real_paths_reject_empty_window_events_and_ca_order_uses_nanoseconds(self):
        with self.assertRaisesRegex(RuntimeError, 'Actual PB paths remain'):
            focused.empty_paths(self.specs, self.baseline)
        outside = copy.deepcopy(self.baseline)
        for spec in self.specs:
            for tier in outside[spec['pv']]:
                for file in tier:
                    file['events'] = []
        with self.assertRaisesRegex(RuntimeError, 'Actual PB paths remain'):
            focused.empty_paths(self.specs, outside)
        samples = {spec['pv']: dict(max(spec['input'], key=lambda row: (row['secs'], row['nanos'])))
                   for spec in self.specs}
        self.assertFalse(focused.later_ca_samples(self.specs, samples))
        for sample in samples.values():
            sample['nanos'] += 1
        self.assertTrue(focused.later_ca_samples(self.specs, samples))
        with self.assertRaisesRegex(RuntimeError, 'inventory differs'):
            focused.later_ca_samples(self.specs, {})

    def test_already_closed_bins_do_not_wait_or_timeout(self):
        expected = [(spec['input'][-1]['secs'] // (spec['interval'] or 60) + 1)
                    * (spec['interval'] or 60) for spec in self.specs]
        with patch.object(focused.time, 'time', return_value=max(expected) + 1000), \
                patch.object(focused.time, 'sleep', side_effect=AssertionError('Closed bins must not wait')):
            self.assertEqual(focused.closed_bin_ends(self.specs), expected)

    def test_open_bins_wait_until_the_settle_time(self):
        expected = [(spec['input'][-1]['secs'] // (spec['interval'] or 60) + 1)
                    * (spec['interval'] or 60) for spec in self.specs]
        clock = [max(expected)]
        def advance(seconds):
            clock[0] += seconds
        with patch.object(focused.time, 'time', side_effect=lambda: clock[0]), \
                patch.object(focused.time, 'sleep', side_effect=advance):
            self.assertEqual(focused.closed_bin_ends(self.specs), expected)
        self.assertEqual(clock[0], max(expected) + focused.BIN_SETTLE_SECONDS)

    def test_physical_loss_duplicates_timestamp_and_alarm_are_rejected(self):
        self.assertEqual(len(focused.compare_physical(self.specs, self.baseline, self.after)), 8)
        spec = self.specs[0]
        begin = spec['old']
        for mutation in ('loss', 'duplicate', 'nanos', 'status', 'severity', 'raw'):
            changed = copy.deepcopy(self.after)
            rows = next(file['events'] for file in changed[spec['pv']][2]
                        if any(begin <= event['secs'] < begin + 300 for event in file['events']))
            index = next(index for index, row in enumerate(rows) if begin <= row['secs'] < begin + 300)
            if mutation == 'loss':
                rows.pop(index)
            elif mutation == 'duplicate':
                rows.insert(index, dict(rows[index]))
            elif mutation == 'raw':
                rows[index]['raw'] = rows[index]['raw'] + 'AA=='
            else:
                rows[index][mutation] += 1
            with self.subTest(mutation=mutation), self.assertRaisesRegex(RuntimeError, 'Physical LTS events differ'):
                focused.compare_physical(self.specs, self.baseline, changed)

    def test_retained_http_and_transport_errors(self):
        expected = focused.compare_physical(self.specs, self.baseline, self.after)
        spec = self.specs[0]
        original = json.loads((self.root / ('scheduled-http-' + spec['pv'].replace(':', '_') + '.json')).read_text())
        def transport(payload):
            stream = io.BytesIO(json.dumps(payload).encode())
            stream.status = 200
            return stream
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(focused.CLIENT, 'open', side_effect=lambda *args, **kwargs: transport(original)):
                focused.compare_http(root, expected, [spec], 'retained')
            for mutation in ('loss', 'duplicate', 'nanos', 'status', 'severity'):
                changed = copy.deepcopy(original)
                if mutation == 'loss':
                    changed[0]['data'].pop()
                elif mutation == 'duplicate':
                    changed[0]['data'].append(dict(changed[0]['data'][0]))
                else:
                    changed[0]['data'][0][mutation] += 1
                with patch.object(focused.CLIENT, 'open', side_effect=lambda *args, **kwargs: transport(changed)):
                    with self.subTest(mutation=mutation), self.assertRaisesRegex(RuntimeError, 'HTTP events differ'):
                        focused.compare_http(root, expected, [spec], 'invalid')
            with patch.object(focused.CLIENT, 'open', side_effect=TimeoutError('HTTP unavailable')):
                with self.assertRaises(TimeoutError):
                    focused.compare_http(root, expected, [spec], 'failed')

    def test_remaining_source_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'retained-source.pb'
            path.touch()
            baseline = copy.deepcopy(self.baseline)
            spec = self.specs[0]
            file = next(file for file in baseline[spec['pv']][0] if any(
                spec['old'] <= row['secs'] < spec['old'] + 300 for row in file['events']))
            file['path'] = str(path)
            with self.assertRaisesRegex(RuntimeError, 'Historical source files remain'):
                focused.compare_physical(self.specs, baseline, self.after)

    def test_focused_source_and_helper_hash_changes_are_rejected(self):
        # This exercises only proof-file validation, never grants ETL acceptance.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = {'manifest.json': self.root / 'manifest.json',
                      'baseline.json': self.root / 'physical-baseline.json',
                      'physical.json': self.root / 'physical-after-scheduled.json',
                      'PBFixture.class': self.root / 'helper-classes/PBFixture.class'}
            for name, path in inputs.items():
                (root / name).write_bytes(path.read_bytes())
            result = {'result': 'Passed', 'chain': 'default',
                      'source_manifest_sha256': contract.digest(root / 'manifest.json'),
                      'baseline_sha256': contract.digest(root / 'baseline.json'),
                      'evidence_sha256': {str(root / 'physical.json'): contract.digest(root / 'physical.json')},
                      'helper_sha256': {str(root / 'PBFixture.class'): contract.digest(root / 'PBFixture.class')}}
            (root / 'result.json').write_text(json.dumps(result))
            focused.verified_focused_result(root, 'default')
            for name in inputs:
                path = root / name
                original = path.read_bytes()
                path.write_bytes(original + b' ')
                with self.subTest(file=name), self.assertRaisesRegex(RuntimeError, 'changed'):
                    focused.verified_focused_result(root, 'default')
                path.write_bytes(original)
            for invalid in ({'result': 'Incomplete'}, {'result': 'Passed', 'chain': 'shortened'}):
                (root / 'result.json').write_text(json.dumps(invalid))
                with self.assertRaisesRegex(RuntimeError, 'matching focused proof'):
                    focused.verified_focused_result(root, 'default')

    def test_aged_bin_uses_actual_source_neighbours_and_rejects_duplicates(self):
        # Actual recorded two-hop output supplies the aged-bin data, not a simulated ETL.
        summary = json.loads((self.root / 'verification-summary.json').read_text())
        for chain in contract.CHAINS:
            original = [spec for spec in self.specs if spec['chain'] == chain]
            specs = copy.deepcopy(original)
            proof = {}
            for spec in specs:
                first = spec['input'][0]
                middle = spec['input'][7]
                width = spec['interval'] or 60
                begin = first['secs'] // width * width
                source = focused.events(self.baseline, spec['pv'], 0, begin, begin + width)
                self.assertGreater(len(source), 1)
                spec['input'] = [middle, first]
                proof[spec['pv']] = {'begin': begin, 'end': begin + width, 'source': source,
                                     'reduced': [max(source, key=lambda row: (row['secs'], row['nanos']))]
                                     if spec['interval'] else source}
            cadences = contract.chain_configuration(chain)['cadences']
            records = [dict(next(row for row in summary['pass_records']
                                 if row['transition'] == index and row['cadence_seconds'] == cadence),
                            invocation_id='retained') for index, cadence in enumerate(cadences)]
            output = focused.retention(specs, self.after, records, chain, 'retained', proof)
            for spec in specs:
                self.assertEqual(output[spec['pv']]['expected'], proof[spec['pv']]['reduced'])
                if spec['interval']:
                    self.assertNotEqual(output[spec['pv']]['expected'][0]['nanos'], spec['input'][-1]['nanos'])
            changed = copy.deepcopy(self.after)
            pv = specs[0]['pv']
            file = next(file for file in changed[pv][2] if any(
                proof[pv]['begin'] <= row['secs'] < proof[pv]['end'] for row in file['events']))
            file['events'].append(dict(output[pv]['expected'][0]))
            with self.assertRaisesRegex(RuntimeError, 'Closed recent bin differs'):
                focused.retention(specs, changed, records, chain, 'retained', proof)


@unittest.skipUnless(os.environ.get('FOCUSED_SHUTDOWN_ROOT'), 'Actual stopped deployment evidence required')
class ShutdownPreservationCheckerTests(unittest.TestCase):
    """Check retained shutdown records without substituting an ETL execution."""

    def records(self):
        root = Path(os.environ['FOCUSED_SHUTDOWN_ROOT'])
        for suffix, chain in (('b', 'shortened'), ('d', 'default')):
            with tarfile.open(root / ('failed-focused-' + suffix + '-r1.tar.gz')) as archive:
                def read(name):
                    return json.load(archive.extractfile(chain + '/' + name))
                yield read('manifest.json')['pvs'], read('before-stop.json'), read('before-seed.json')

    def test_actual_normal_shutdown_allows_empty_sts_and_new_events(self):
        for specs, before, after in self.records():
            self.assertTrue(all(not after[spec['pv']][0] for spec in specs))
            self.assertEqual(len(focused.shutdown_preservation(specs, before, after)), 4)

    def test_known_loss_duplicate_timestamp_value_alarm_and_raw_are_rejected(self):
        for specs, before, after in self.records():
            spec = specs[0]
            first = before[spec['pv']][0][0]['events'][0]
            for mutation in ('loss', 'duplicate', 'secs', 'nanos', 'val', 'status', 'severity', 'raw', 'lts'):
                changed = copy.deepcopy(after)
                rows = next(file['events'] for file in changed[spec['pv']][1] if first in file['events'])
                index = rows.index(first)
                if mutation == 'loss':
                    rows.pop(index)
                elif mutation == 'duplicate':
                    rows.append(dict(first))
                elif mutation == 'lts':
                    changed[spec['pv']][2].append({'path': 'invalid-tier', 'events': [rows.pop(index)]})
                elif mutation == 'raw':
                    rows[index]['raw'] += 'AA=='
                else:
                    rows[index][mutation] += 1
                with self.subTest(mutation=mutation), self.assertRaisesRegex(RuntimeError, 'shutdown source events differ'):
                    focused.shutdown_preservation(specs, before, changed)

    def test_unsupported_shutdown_settings_and_missing_source_are_rejected(self):
        for specs, before, after in self.records():
            for tier, query in ((0, '&consolidateOnShutdown=false'),
                                (1, '&consolidateOnShutdown=true'), (1, '&reducedata=lastSample_10')):
                changed = copy.deepcopy(specs)
                changed[0]['stores'][tier] += query
                with self.subTest(tier=tier, query=query), self.assertRaisesRegex(RuntimeError, 'Unsupported shutdown'):
                    focused.shutdown_preservation(changed, before, after)
            changed = copy.deepcopy(before)
            changed[specs[0]['pv']][0] = []
            with self.assertRaisesRegex(RuntimeError, 'pre-stop STS events'):
                focused.shutdown_preservation(specs, changed, after)


@unittest.skipUnless(os.environ.get('FOCUSED_RESUME_ROOT'), 'Actual prepared resume archives required')
class ResumeSourceCheckerTests(unittest.TestCase):
    """Validate actual frozen input files and process identities, without running ETL."""

    def records(self):
        directory = Path(os.environ['FOCUSED_RESUME_ROOT'])
        for suffix, chain in (('b', 'shortened'), ('d', 'default')):
            with tarfile.open(directory / ('prepared-resume-' + suffix + '-r1.tar.gz')) as archive:
                guard = json.load(archive.extractfile(chain + '/resume-guard.json'))
                yield archive, chain, guard

    def test_original_source_and_preserved_copy_hash_changes_are_rejected(self):
        for archive, chain, guard in self.records():
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name in guard['source_hashes']:
                    for prefix in ('', 'resume-source/'):
                        path = root / prefix / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(archive.extractfile(chain + '/' + prefix + name).read())
                focused.check_resume_files(root, guard)
                for name in ('manifest.json', 'baseline.json', 'result.json', 'helper-classes/PBFixture.class'):
                    for prefix in ('', 'resume-source/'):
                        path = root / prefix / name
                        original = path.read_bytes()
                        path.write_bytes(original + b' ')
                        with self.subTest(name=name, prefix=prefix), self.assertRaisesRegex(RuntimeError, 'resume source changed'):
                            focused.check_resume_files(root, guard)
                        path.write_bytes(original)

    def test_boot_invocation_pid_and_start_changes_are_rejected(self):
        for archive, chain, guard in self.records():
            actual = guard['identity']
            focused.check_resume_identity(guard, actual)
            for key in ('boot_id', 'invocation_id', 'pid', 'start'):
                changed = copy.deepcopy(actual)
                if key in ('boot_id', 'invocation_id'):
                    changed[key] += '-different'
                else:
                    component = next(iter(changed['jvms']))
                    changed['jvms'][component][key] = str(int(changed['jvms'][component][key]) + 1)
                with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'JVM identity changed'):
                    focused.check_resume_identity(guard, changed)

    def test_final_source_check_allows_only_live_outputs_to_change(self):
        for archive, chain, guard in self.records():
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name in guard['source_hashes']:
                    for prefix in ('', 'resume-source/'):
                        path = root / prefix / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(archive.extractfile(chain + '/' + prefix + name).read())
                outputs = ('result.json', 'passes-' + guard['identity']['invocation_id'] + '.jsonl')
                for name in outputs:
                    (root / name).write_text('Updated live output\n')
                focused.check_resume_files(root, guard, outputs_changed=True)
                for name in guard['source_hashes']:
                    prefixes = ('resume-source/',) if name in outputs else ('', 'resume-source/')
                    for prefix in prefixes:
                        path = root / prefix / name
                        original = path.read_bytes()
                        path.write_bytes(original + b' ')
                        with self.subTest(name=name, prefix=prefix), self.assertRaisesRegex(RuntimeError, 'resume source changed'):
                            focused.check_resume_files(root, guard, outputs_changed=True)
                        path.write_bytes(original)

    def test_final_completion_rejects_changed_runtime_tools_and_configuration(self):
        for archive, chain, guard in self.records():
            recorded = json.load(archive.extractfile(chain + '/inventory.json'))
            final = copy.deepcopy(recorded)
            final['identity'] = guard['identity']
            approved_tools = dict(recorded['tools'], **{'focused.py': contract.digest(Path(focused.__file__))})
            final['tools'] = approved_tools
            focused.check_completion(recorded, final, guard['identity'], guard['identity'], approved_tools)
            for key in ('pvs', 'flags', 'artifacts', 'tools', 'identity'):
                changed = copy.deepcopy(final)
                changed[key] = None
                with self.subTest(key=key), self.assertRaises(RuntimeError):
                    focused.check_completion(recorded, changed, guard['identity'], guard['identity'], approved_tools)
            for key in ('boot_id', 'invocation_id', 'pid', 'start'):
                changed = copy.deepcopy(guard['identity'])
                if key in ('boot_id', 'invocation_id'):
                    changed[key] += '-different'
                else:
                    component = next(iter(changed['jvms']))
                    changed['jvms'][component][key] = str(int(changed['jvms'][component][key]) + 1)
                with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'focused completion'):
                    focused.check_completion(recorded, final, guard['identity'], changed, approved_tools)


@unittest.skipUnless(os.environ.get('FOCUSED_INVENTORY'), 'Actual deployed inventory required')
class DeployedConfigurationCheckerTests(unittest.TestCase):
    def test_artifact_flags_settings_and_tool_changes_are_rejected(self):
        actual = json.loads(Path(os.environ['FOCUSED_INVENTORY']).read_text())
        focused.compare_configuration(actual, actual)
        for key in ('artifacts', 'pvs', 'flags', 'tools'):
            changed = copy.deepcopy(actual)
            changed[key] = None
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'current ' + key):
                focused.compare_configuration(changed, actual)


@unittest.skipUnless(os.environ.get('FOCUSED_COLD_ROOT') and os.environ.get('FOCUSED_EXPECTED_KEYS'),
                     'Actual cold execution records and deployed converter output required')
class InitialChunkKeyTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ['FOCUSED_COLD_ROOT'])
        self.recorded = json.loads((self.root / 'inventory.json').read_text())
        self.final = json.loads((self.root / 'final-inspection/inventory.json').read_text())
        self.keys = json.loads(Path(os.environ['FOCUSED_EXPECTED_KEYS']).read_text())

    def test_actual_initial_keys_and_physical_paths(self):
        focused.check_chunk_keys(self.recorded, self.final, self.keys)
        focused.check_chunk_keys(self.final, self.final, self.keys)
        specs = json.loads((self.root / 'manifest.json').read_text())['pvs']
        snapshots = [json.loads((self.root / name).read_text())
                     for name in ('baseline.json', 'startup.json', 'repeat.json')]
        focused.check_chunk_paths(specs, snapshots, self.keys)
        changed = copy.deepcopy(self.keys)
        changed[specs[0]['pv']] += 'wrong'
        with self.assertRaisesRegex(RuntimeError, 'Physical PB path differs'):
            focused.check_chunk_paths(specs, snapshots, changed)

    def test_unexpected_keys_pv_inventory_and_configuration_are_rejected(self):
        for mutation in ('null', 'empty', 'wrong', 'missing', 'duplicate', 'order', 'settings', 'type'):
            changed = copy.deepcopy(self.final)
            row = changed['pvs'][0]
            if mutation in ('null', 'empty', 'wrong'):
                row['typeinfo']['chunkKey'] = {'null': None, 'empty': '', 'wrong': 'wrong:'}[mutation]
            elif mutation == 'missing':
                changed['pvs'].pop()
            elif mutation == 'duplicate':
                changed['pvs'][1] = copy.deepcopy(row)
            elif mutation == 'order':
                changed['pvs'].reverse()
            elif mutation == 'settings':
                row['effective']['urls'][0] += '&hold=0'
            else:
                row['typeinfo']['DBRType'] = 'DBR_SCALAR_STRING'
            with self.subTest(mutation=mutation), self.assertRaises(RuntimeError):
                focused.check_chunk_keys(self.recorded, changed, self.keys)
        changed = copy.deepcopy(self.final)
        changed['pvs'][0]['typeinfo']['chunkKey'] += 'changed'
        with self.assertRaisesRegex(RuntimeError, 'Unexpected chunk key change'):
            focused.check_chunk_keys(self.final, changed, self.keys)
        for key in ('flags', 'artifacts', 'tools', 'identity'):
            changed = copy.deepcopy(self.final)
            changed[key] = None
            with self.subTest(key=key), self.assertRaises(RuntimeError):
                focused.check_completion(self.recorded, changed, self.final['identity'], self.final['identity'],
                                         expected_keys=self.keys)


@unittest.skipUnless(os.environ.get('FOCUSED_RECHECK_ARCHIVES'),
                     'Retained final and recheck evidence archives required')
class RecheckProofConsumerTests(unittest.TestCase):
    """Local rehearsal of the recheck proof consumer on the retained records.

    Only conditions decided from retained files run here. The fresh-inventory comparison against
    a live appliance, identity stability during a readback and the continuity binding need a guest.
    """

    CHAINS = {'shortened': 'c', 'default': 'd'}
    HERE = Path(__file__).resolve().parent

    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.TemporaryDirectory()
        cls.base = Path(cls.scratch.name)
        archives = Path(os.environ['FOCUSED_RECHECK_ARCHIVES'])
        for chain, suffix in cls.CHAINS.items():
            for prefix in ('final', 'recheck'):
                with tarfile.open(archives / (prefix + '-evidence-' + suffix + '-r1.tar.gz')) as archive:
                    members = archive.getmembers()
                    for member in members:
                        parts = Path(member.name).parts
                        if (member.name.startswith('/') or '..' in parts or parts[0] != chain
                                or member.issym() or member.islnk() or member.isdev()):
                            raise RuntimeError('Unsafe archive member: ' + member.name)
                    options = {'filter': 'data'} if hasattr(tarfile, 'data_filter') else {}
                    archive.extractall(cls.base, members=members, **options)

    @classmethod
    def tearDownClass(cls):
        cls.scratch.cleanup()

    def root(self, chain):
        return self.base / chain

    def relative(self, chain):
        return Path(focused.RECHECK_APPROVED['proofs'][chain]['path']).relative_to(focused.ROOT / chain)

    def variant(self, chain, changes=None, deleted=()):
        """Hard-linked copy of one chain tree in which changed files are replaced, never edited."""
        destination = Path(tempfile.mkdtemp(dir=self.base)) / chain
        source = self.root(chain)
        for path in source.rglob('*'):
            target = destination / path.relative_to(source)
            if path.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(path, target)
        for name, content in (changes or {}).items():
            target = destination / name
            target.unlink()
            target.write_bytes(content)
        for name in deleted:
            (destination / name).unlink()
        return destination

    def reproof(self, chain, files=None, fields=None):
        """A variant whose changed recheck files and proof fields carry a consistent proof hash."""
        entry = focused.RECHECK_APPROVED['proofs'][chain]
        relative = self.relative(chain)
        proof = json.loads((self.root(chain) / relative).read_text())
        changes = {}
        for name, content in (files or {}).items():
            changes[str(relative.parent / name)] = content
            proof['recheck_evidence_sha256'][str(Path(entry['path']).parent / name)] = hashlib.sha256(content).hexdigest()
        proof.update(fields or {})
        data = json.dumps(proof, sort_keys=True).encode()
        changes[str(relative)] = data
        approved = copy.deepcopy(focused.RECHECK_APPROVED)
        approved['proofs'][chain]['sha256'] = hashlib.sha256(data).hexdigest()
        return self.variant(chain, changes), approved

    def bundle_copy(self, name, changes=None, freeze=True):
        destination = Path(tempfile.mkdtemp(dir=self.base)) / name
        destination.mkdir()
        for member in (*contract.BUNDLE_FILES, 'bundle.json'):
            shutil.copyfile(self.HERE / member, destination / member)
        for member, content in (changes or {}).items():
            (destination / member).write_bytes(content)
        if freeze:
            contract.freeze(destination)
        return destination

    def test_both_chains_are_accepted_from_the_retained_records(self):
        for chain in self.CHAINS:
            with self.subTest(chain=chain):
                original = focused.file_digest(self.root(chain) / 'result.json')
                acceptance = focused.recheck_acceptance(self.root(chain), chain)
                self.assertEqual(acceptance['proof_sha256'], focused.RECHECK_APPROVED['proofs'][chain]['sha256'])
                self.assertEqual(acceptance['original_result_sha256'], original)
                self.assertEqual(len(acceptance['inventory']['pvs']), 903)
                self.assertEqual(acceptance['identity'], acceptance['inventory']['identity'])
                accepted = focused.accepted_focused_result(self.root(chain), chain)
                self.assertIsNone(accepted['result'])
                self.assertEqual(accepted['recheck']['proof_sha256'], acceptance['proof_sha256'])
                self.assertEqual(focused.file_digest(self.root(chain) / 'result.json'), original)

    def test_tools_comparison_allows_only_the_approved_replacements(self):
        acceptance = focused.recheck_acceptance(self.root('shortened'), 'shortened')
        tools = acceptance['inventory']['tools']
        delivered = self.bundle_copy('delivered')
        self.assertEqual(set(focused.check_recheck_tools(tools, delivered)), set(contract.BUNDLE_FILES))
        cases = {'PBFixture.java': b'// changed helper source\n', 'contract.py': b'# changed tool\n'}
        for name, content in cases.items():
            original = (self.HERE / name).read_bytes()
            with self.subTest(changed=name):
                refrozen = self.bundle_copy('refrozen-' + name, {name: original + content})
                with self.assertRaisesRegex(RuntimeError, 'approved replacements changed: ' + name):
                    focused.check_recheck_tools(tools, refrozen)
        unfrozen = self.bundle_copy('unfrozen', {'measure.py': (self.HERE / 'measure.py').read_bytes() + b'\n'},
                                    freeze=False)
        with self.assertRaisesRegex(RuntimeError, 'Installed bundle differs from the frozen complete bundle'):
            focused.check_recheck_tools(tools, unfrozen)
        approved = copy.deepcopy(focused.RECHECK_APPROVED)
        approved['helper'] = '0' * 64
        with self.assertRaisesRegex(RuntimeError, 'approved replacements changed: PBFixture.java'):
            focused.check_recheck_tools(tools, delivered, approved)

    def test_original_result_condition_rejects_changed_result(self):
        chain = 'shortened'
        original = json.loads((self.root(chain) / 'result.json').read_text())
        for field, value in (('error', original['error'] + ' again'), ('result', 'Passed'), ('chain', 'default')):
            changed = dict(original, **{field: value})
            data = json.dumps(changed, sort_keys=True).encode()
            with self.subTest(field=field):
                variant = self.variant(chain, {'result.json': data})
                with self.assertRaisesRegex(RuntimeError, 'retained final configuration comparison failure'):
                    focused.recheck_acceptance(variant, chain)

    def test_proof_pin_condition_rejects_wrong_hash_missing_entry_and_other_chain(self):
        chain = 'shortened'
        wrong = copy.deepcopy(focused.RECHECK_APPROVED)
        wrong['proofs'][chain]['sha256'] = '0' * 64
        with self.assertRaisesRegex(RuntimeError, 'differs from the approved proof'):
            focused.recheck_acceptance(self.root(chain), chain, wrong)
        absent = copy.deepcopy(focused.RECHECK_APPROVED)
        del absent['proofs'][chain]
        with self.assertRaisesRegex(RuntimeError, 'No approved recheck proof'):
            focused.recheck_acceptance(self.root(chain), chain, absent)
        other = copy.deepcopy(focused.RECHECK_APPROVED)
        other['proofs']['default'] = other['proofs']['shortened']
        with self.assertRaisesRegex(RuntimeError, 'outside the chain root'):
            focused.recheck_acceptance(self.root('default'), 'default', other)

    def test_evidence_set_condition_rejects_altered_and_missing_files(self):
        chain = 'shortened'
        relative = self.relative(chain)
        source_file = (self.root(chain) / 'baseline.json').read_bytes() + b' '
        recheck_file = (self.root(chain) / relative.parent / 'inventory.json').read_bytes() + b' '
        cases = (('altered source file', {'baseline.json': source_file}, (), 'Retained recheck evidence changed'),
                 ('altered recheck file', {str(relative.parent / 'inventory.json'): recheck_file}, (),
                  'Retained recheck evidence changed'),
                 ('missing source file', {}, ('repeat.json',), 'is missing'))
        for label, changes, deleted, message in cases:
            with self.subTest(case=label):
                variant = self.variant(chain, changes, deleted)
                with self.assertRaisesRegex(RuntimeError, message):
                    focused.recheck_acceptance(variant, chain)

    def test_producing_version_and_key_conditions_reject_each_change(self):
        chain = 'shortened'
        directory = self.root(chain) / self.relative(chain).parent
        key_input = json.loads((directory / 'key-input.json').read_text())
        key_input['pvs'][0]['pv'] += 'X'
        keys = json.loads((directory / 'expected-keys.json').read_text())
        first = sorted(keys)[0]
        keys[first] += 'x'
        keys_data = json.dumps(keys, sort_keys=True).encode()
        cases = (
            ('checker hash', {}, {'checker_sha256': '0' * 64}, 'approved producing version'),
            ('helper hash', {}, {'helper_source_sha256': '0' * 64}, 'approved producing version'),
            ('key input name', {'key-input.json': json.dumps(key_input).encode()}, {}, 'Chunk key input differs'),
            ('properties hash', {'archappl.properties': b'changed=1\n'}, {}, 'properties differ'),
            ('expected keys hash', {}, {'expected_keys_sha256': '0' * 64}, 'Expected chunk keys differ'),
            ('expected key value', {'expected-keys.json': keys_data},
             {'expected_keys_sha256': hashlib.sha256(keys_data).hexdigest()}, 'Unexpected chunk key change'),
            ('proof identity', {}, {'identity': {'boot_id': 'other', 'invocation_id': 'other', 'jvms': {}}},
             'identity differs'))
        for label, files, fields, message in cases:
            with self.subTest(case=label):
                variant, approved = self.reproof(chain, files, fields)
                with self.assertRaisesRegex(RuntimeError, message):
                    focused.recheck_acceptance(variant, chain, approved)

    def test_configuration_comparison_is_strict_on_the_real_final_inventory(self):
        """The real final inspection stands in for a fresh inventory; the guest runs compare a live one."""
        chain = 'default'
        acceptance = focused.recheck_acceptance(self.root(chain), chain)
        final = json.loads((self.root(chain) / 'final-inspection/inventory.json').read_text())
        focused.check_recheck_configuration(acceptance, final)
        for key in ('artifacts', 'pvs', 'flags'):
            changed = copy.deepcopy(final)
            if key == 'pvs':
                changed['pvs'][0]['typeinfo']['chunkKey'] = None
            elif key == 'flags':
                changed['flags']['__extra'] = True
            else:
                changed['artifacts']['heads']['maven'] = '0' * 40
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'differs from the recheck inventory: ' + key):
                focused.check_recheck_configuration(acceptance, changed)


class BundleReplacementTests(unittest.TestCase):
    """Run the real replacement step on real directories; only systemctl is replaced.

    The security context of copied files is not exercised here; the guest delivery check compares it.
    """

    HERE = Path(__file__).resolve().parent

    def setUp(self):
        spec = importlib.util.spec_from_file_location('replace_bundle', self.HERE / 'replace-bundle.py')
        self.step = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.step)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.installed = self.base / 'etl-soak'
        self.installed.mkdir()
        for member in contract.BUNDLE_FILES:
            shutil.copyfile(self.HERE / member, self.installed / member)
        contract.freeze(self.installed)
        extras = {'pvs-all.csv': (self.HERE.parent / 'fixtures/pvs-all.csv').read_bytes(),
                  'aasoak.db': b'record(ai, "X") {}\n', 'register.py': b'print(1)\n',
                  '_inputs/retest-deadband.db': b'record(ai, "Y") {}\n'}
        for name, content in extras.items():
            path = self.installed / name
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(content)
        (self.installed / 'register.py').chmod(0o750)
        os.utime(self.installed / 'aasoak.db', ns=(1_700_000_000_000_000_000, 1_700_000_000_000_000_000))
        self.candidate = self.base / 'candidate'
        self.candidate.mkdir()
        for member in contract.BUNDLE_FILES:
            shutil.copyfile(self.HERE / member, self.candidate / member)
        (self.candidate / 'focused.py').write_bytes((self.HERE / 'focused.py').read_bytes() + b'\n# candidate\n')
        contract.freeze(self.candidate)
        self.accepted = focused.file_digest(self.candidate / 'bundle.json')
        self.before = self.step.tree(self.installed)

    def systemctl(self, states=None):
        real = subprocess.run

        def transport(args, **kwargs):
            if args[0] == 'systemctl':
                return subprocess.CompletedProcess(args, 0, (states or {}).get(args[2], 'inactive') + '\n', '')
            return real(args, **kwargs)
        return patch('subprocess.run', side_effect=transport)

    def siblings(self):
        return sorted(path.name for path in self.base.iterdir())

    def test_swap_replaces_only_the_members_and_carries_every_other_file(self):
        with self.systemctl():
            result = self.step.replace(self.installed, self.candidate, self.accepted, now='20261010T000000Z')
        self.assertEqual(self.step.frozen_members(self.installed, self.accepted), sorted(contract.BUNDLE_FILES))
        after = self.step.tree(self.installed)
        members = set(contract.BUNDLE_FILES) | {'bundle.json'}
        self.assertEqual({name: value for name, value in after.items() if name not in members},
                         {name: value for name, value in self.before.items() if name not in members})
        self.assertNotEqual(after['focused.py'][0], self.before['focused.py'][0])
        preserved = Path(result['preserved'])
        self.assertEqual(self.step.tree(preserved), self.before)
        self.assertEqual(self.siblings(), ['candidate', 'etl-soak', 'etl-soak.prev-20261010T000000Z'])

    def test_rollback_needs_two_renames_and_restores_the_preserved_tree(self):
        with self.systemctl():
            result = self.step.replace(self.installed, self.candidate, self.accepted, now='20261010T000000Z')
        outcome = self.step.rollback(self.installed, result['preserved'], now='20261010T000100Z')
        self.assertEqual(self.step.tree(self.installed), self.before)
        self.assertEqual(self.step.frozen_members(Path(outcome['rejected']), self.accepted),
                         sorted(contract.BUNDLE_FILES))
        self.assertEqual(self.siblings(), ['candidate', 'etl-soak', 'etl-soak.rejected-20261010T000100Z'])
        with self.assertRaisesRegex(RuntimeError, 'installed and preserved directories'):
            self.step.rollback(self.installed, self.base / 'etl-soak.prev-missing', now='20261010T000200Z')

    def test_refusals_leave_the_installed_directory_and_siblings_untouched(self):
        broken = self.base / 'broken'
        shutil.copytree(self.candidate, broken)
        (broken / 'measure.py').write_bytes((broken / 'measure.py').read_bytes() + b'\n')
        cases = (('wrong accepted hash', self.candidate, '0' * 64, {}, 'differs from the accepted SHA256'),
                 ('hash not filled in', self.candidate, None, {}, 'not filled in'),
                 ('member changed after the freeze', broken, self.accepted_of(broken), {},
                  'Bundle member differs from the frozen bundle: measure.py'),
                 ('unit active', self.candidate, self.accepted, {'etl-soak-sample.timer': 'active'},
                  'must be inactive is active'),
                 ('finish unit activating', self.candidate, self.accepted, {'etl-soak-finish.service': 'activating'},
                  'must be inactive is active'))
        for label, bundle, accepted, states, message in cases:
            with self.subTest(case=label), self.systemctl(states):
                with self.assertRaisesRegex(RuntimeError, message):
                    self.step.replace(self.installed, bundle, accepted, now='20261010T000000Z')
                self.assertEqual(self.step.tree(self.installed), self.before)
                self.assertEqual(self.siblings(), ['broken', 'candidate', 'etl-soak'])
        (self.base / ('etl-soak.new-' + self.accepted[:8])).mkdir()
        with self.systemctl(), self.assertRaisesRegex(RuntimeError, 'Refusing an existing sibling'):
            self.step.replace(self.installed, self.candidate, self.accepted, now='20261010T000000Z')
        self.assertEqual(self.step.tree(self.installed), self.before)

    def accepted_of(self, directory):
        return focused.file_digest(directory / 'bundle.json')

    def test_archive_bundle_is_unpacked_and_unsafe_members_are_rejected(self):
        archive = self.base / 'bundle.tar'
        with tarfile.open(archive, 'w') as handle:
            for member in (*contract.BUNDLE_FILES, 'bundle.json'):
                handle.add(self.candidate / member, arcname=member)
        with self.systemctl():
            self.step.replace(self.installed, archive, self.accepted, now='20261010T000000Z')
        self.assertEqual(self.step.frozen_members(self.installed, self.accepted), sorted(contract.BUNDLE_FILES))
        unsafe = self.base / 'unsafe.tar'
        with tarfile.open(unsafe, 'w') as handle:
            info = tarfile.TarInfo('../outside')
            info.size = 0
            handle.addfile(info, io.BytesIO(b''))
        with self.systemctl(), self.assertRaisesRegex(RuntimeError, 'Unsafe bundle archive member'):
            self.step.replace(self.base / 'etl-soak', unsafe, self.accepted, now='20261010T000300Z')


if __name__ == '__main__':
    unittest.main()
