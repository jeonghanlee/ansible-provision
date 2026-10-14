#!/usr/bin/env python3
"""Local boundary tests; real VM integration remains a separate acceptance check."""

import contextlib
import datetime
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

import collect
import contract
import measure
import observe
import evaluate

HERE = Path(__file__).resolve().parent
DU_RACE = os.environ.get('ETL_SOAK_DU_RACE_EVIDENCE')
FIXTURE = HERE.parent / 'fixtures' / 'pvs-all.csv'


class StoreSizeTests(unittest.TestCase):
    def test_other_du_failures_still_fail_the_measurement(self):
        total = '4096\t/arch/sts\n'
        self.assertEqual(collect.tolerated_du(0, total, ''), 4096)
        for code, out, err in ((1, total, "du: cannot read directory '/arch/sts': Permission denied\n"),
                               (1, total, ''), (2, total, ''), (1, '', "du: cannot access 'x': No such file or directory\n"),
                               (0, '', '')):
            with self.subTest(code=code, err=err), self.assertRaisesRegex(RuntimeError, 'du'):
                collect.tolerated_du(code, out, err)

    def test_real_directory_walk_that_races_a_removal_is_counted(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'kept').write_text('x' * 100)
            self.assertGreaterEqual(collect.directory_bytes(directory), 100)

    @unittest.skipUnless(DU_RACE, 'A retained actual du result from a racing removal is required')
    def test_actual_du_result_from_a_racing_removal_is_accepted(self):
        result = json.loads(Path(DU_RACE).read_text())
        self.assertEqual(result['returncode'], 1)
        self.assertIn('No such file or directory', result['stderr'])
        self.assertEqual(collect.tolerated_du(result['returncode'], result['stdout'], result['stderr']),
                         int(result['stdout'].split()[0]))
        # The generic runner, which the measurement used before, rejects the same actual result.
        with self.assertRaisesRegex(RuntimeError, 'command failed'):
            collect.run(['sh', '-c', 'exit ' + str(result['returncode'])])


class RetestTests(unittest.TestCase):
    def test_empty_http_200_fails_all_fixture_freshness(self):
        class Response(io.BytesIO):
            status = 200

        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            raw = out / 'raw'
            raw.mkdir()
            with patch('urllib.request.urlopen', side_effect=lambda *a, **k: Response(b'[]')), \
                    patch('subprocess.run', return_value=subprocess.CompletedProcess([], 1, '', '')):
                with self.assertRaisesRegex(RuntimeError, 'retrieval=0, missing=903'):
                    measure.latency(out, raw, FIXTURE, '2026-09-30T06:00:00+00:00')
            results = json.loads((raw / 'freshness.json').read_text())
            self.assertEqual(len(results), 903)
            self.assertEqual({row['outcome'] for row in results}, {'no_sample_in_window'})
            self.assertEqual({row['http'] for row in results}, {200})

    def health_event(self, status='3', result='success'):
        environment = dict(os.environ, INVOCATION_ID='local-test-invocation',
                           SERVICE_RESULT=result, EXIT_CODE='exited', EXIT_STATUS=status)
        message = subprocess.check_output(['python3', str(HERE / 'health-event.py')],
                                          env=environment, text=True).strip()
        started = json.dumps({'__CURSOR': 'start-cursor', '_PID': '1',
                              'MESSAGE_ID': '7d4958e842da4a758f6c1cdc7b36dcc5',
                              'MESSAGE': 'Starting EPICS Archiver Appliance process observation...'})
        return started + '\n' + json.dumps({'__CURSOR': 'completion-cursor', '_PID': '123',
                                            '_SYSTEMD_INVOCATION_ID': 'local-test-invocation', 'MESSAGE': message})

    def test_http_200_with_old_last_known_data_is_not_recent(self):
        class Response(io.BytesIO):
            status = 200

        payload = json.dumps([{'data': [{'secs': int(time.time()) - 100, 'nanos': 0}]}]).encode()
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            raw = out / 'raw'
            raw.mkdir()
            with patch('urllib.request.urlopen', side_effect=lambda *a, **k: Response(payload)), \
                    patch('subprocess.run', return_value=subprocess.CompletedProcess([], 1, '', '')):
                with self.assertRaisesRegex(RuntimeError, 'retrieval=0, missing=903'):
                    measure.latency(out, raw, FIXTURE, '2026-09-30T06:00:00+00:00')
            results = json.loads((raw / 'freshness.json').read_text())
            self.assertEqual({row['returned_samples'] for row in results}, {1})
            self.assertEqual({row['out_of_window_samples'] for row in results}, {1})

    def collect_transport(self, health_journal, health_properties=None):
        def transport(args, **kwargs):
            if args[0] == 'journalctl':
                if '--until' in args:
                    stdout = json.dumps({'__CURSOR': 'boot-cursor', '__REALTIME_TIMESTAMP': '1'})
                elif '--cursor' in args and '-u' not in args:
                    stdout = json.dumps({'__CURSOR': 'boot-cursor', '__REALTIME_TIMESTAMP': '1'})
                else:
                    stdout = health_journal if collect.HEALTH_UNIT in args else ''
            elif collect.HEALTH_UNIT in args:
                stdout = health_properties or ('Result=success\nExecMainCode=1\nExecMainStatus=3\n'
                          'SuccessExitStatus=3\nExecMainExitTimestamp=Wed 2026-09-30 06:00:00 UTC')
            else:
                raise AssertionError('Unexpected transport request: ' + str(args))
            return subprocess.CompletedProcess(args, 0, stdout, '')
        return transport

    def test_real_recorder_and_collector_accept_unit_status_three(self):
        event = self.health_event()
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            with patch('subprocess.run', side_effect=self.collect_transport(event)), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(collect.sample(out, FIXTURE, journal_only=True))
            state = json.loads((out / 'state.json').read_text())
            self.assertEqual(state['health_completed']['local-test-invocation']['exit_status'], '3')

    def test_running_health_uses_recent_completed_invocation(self):
        event = self.health_event()
        properties = ('Result=success\nExecMainCode=0\nExecMainStatus=0\n'
                      'SuccessExitStatus=3\nExecMainExitTimestamp=\nActiveState=activating')
        self.assertFalse(collect.health_succeeded(collect.properties(properties)))
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            with patch('subprocess.run', side_effect=self.collect_transport(event, properties)), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(collect.sample(out, FIXTURE, journal_only=True))
            summary = json.loads((out / 'latest.json').read_text())
            self.assertEqual(summary['health_completion']['exit_status'], '3')
            self.assertEqual(summary['errors'], [])

    def test_pending_health_does_not_replace_completed_health_evidence(self):
        event = self.health_event()
        pending = json.dumps({'__CURSOR': 'pending-cursor', '_PID': '1',
                              'MESSAGE_ID': '7d4958e842da4a758f6c1cdc7b36dcc5',
                              'MESSAGE': 'Starting EPICS Archiver Appliance process observation...'})
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            raw = out / 'raw'
            raw.mkdir()
            with patch('subprocess.run', side_effect=self.collect_transport(event + '\n' + pending)):
                journal = collect.collect_health(out, raw, {}, datetime.datetime.now(datetime.timezone.utc))
            self.assertEqual(journal['starts'] - journal['completed_total'], 1)
            now = datetime.datetime.now(datetime.timezone.utc)
            self.assertEqual(collect.health_completion(journal, now)['exit_status'], '3')
            finished = datetime.datetime.fromisoformat(
                journal['completed']['local-test-invocation']['observed_at'])
            self.assertEqual(collect.health_completion(
                journal, finished + datetime.timedelta(seconds=120))['exit_status'], '3')
            with self.assertRaisesRegex(RuntimeError, 'freshness bound'):
                collect.health_completion(journal, now + datetime.timedelta(seconds=121))
            with self.assertRaisesRegex(RuntimeError, 'freshness bound'):
                collect.health_completion(journal, finished - datetime.timedelta(seconds=1))

    def test_absent_health_completion_fails_collection(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            with patch('subprocess.run', side_effect=self.collect_transport('')), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertTrue(collect.sample(out, FIXTURE, journal_only=True))
            summary = json.loads((out / 'latest.json').read_text())
            self.assertIn('health_completion', [error['check'] for error in summary['errors']])

    def test_rocky_systemd_exit_contract_uses_actual_dbus_format(self):
        outputs = [subprocess.CompletedProcess([], 0,
                   'Result=success\nExecMainCode=1\nExecMainStatus=3\nSuccessExitStatus=[unprintable]\n'
                   'ExecMainExitTimestamp=Tue 2026-09-29 23:16:11 PDT', ''),
                   subprocess.CompletedProcess([], 0, 'o "/org/freedesktop/systemd1/unit/epicsarchiverap_2dmaven_2dhealth_2eservice"', ''),
                   subprocess.CompletedProcess([], 0, '(aiai) 1 3 0', '')]
        with patch('subprocess.run', side_effect=outputs):
            health = collect.health_properties()
        self.assertTrue(collect.health_succeeded(health))
        self.assertEqual(health['SuccessExitStatus'], '3')

    def test_failed_health_invocation_is_retained(self):
        event = self.health_event('1', 'exit-code')
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            with patch('subprocess.run', side_effect=self.collect_transport(event)), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertTrue(collect.sample(out, FIXTURE, journal_only=True))
            summary = json.loads((out / 'latest.json').read_text())
            self.assertIn('health_invocation', [error['check'] for error in summary['errors']])
            self.assertIn('health_completion', [error['check'] for error in summary['errors']])
            self.assertIn('exit-code', (out / 'health-invocations.csv').read_text())

    def test_unavailable_health_cursor_prevents_success(self):
        event = self.health_event()
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            collect.write_json(out / 'state.json', {'health_journal_cursor': 'missing-cursor'})
            with patch('subprocess.run', side_effect=self.collect_transport(event)), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertTrue(collect.sample(out, FIXTURE, journal_only=True))
            summary = json.loads((out / 'latest.json').read_text())
            self.assertIn('health_coverage', [error['check'] for error in summary['errors']])

    def test_sampler_lock_rejects_overlap(self):
        with tempfile.TemporaryDirectory() as directory:
            with collect.locked(Path(directory) / '.sample.lock'):
                with self.assertRaises(BlockingIOError):
                    collect.sample(Path(directory), FIXTURE, journal_only=True)

    def test_two_real_collection_exceptions_request_abort_and_keep_full_pointer(self):
        event = self.health_event()
        original_transport = self.collect_transport(event)
        requests = []

        def transport(args, **kwargs):
            if collect.ABORT_UNIT in args:
                requests.append(args)
                return subprocess.CompletedProcess(args, 0, '', '')
            return original_transport(args, **kwargs)

        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            collect.write_json(out / 'observation.json', {'abort_policy': {'consecutive_failures': 2}})
            with patch('subprocess.run', side_effect=transport), contextlib.redirect_stdout(io.StringIO()):
                self.assertTrue(collect.sample(out, out / 'absent-fixture.csv'))
                self.assertFalse((out / 'abort-request.json').exists())
                self.assertTrue(collect.sample(out, out / 'absent-fixture.csv'))
                self.assertEqual(len(requests), 1)
                before = (out / 'latest-full.json').read_bytes()
                collect.sample(out, FIXTURE, journal_only=True)
                self.assertEqual((out / 'latest-full.json').read_bytes(), before)
            request = json.loads((out / 'abort-request.json').read_text())
            self.assertEqual(request['reason'], 'consecutive_sample_failures')
            sample = json.loads(Path(request['trigger_sample']).read_text())
            self.assertEqual(sample['errors'][0]['type'], 'FileNotFoundError')

    def test_schedule_contains_exact_two_hour_grid(self):
        started = datetime.datetime(2026, 9, 30, 6, 54, 30, tzinfo=datetime.timezone.utc)
        expected = observe.expected_firings(started, started + datetime.timedelta(seconds=7200))
        self.assertEqual(sum(row['transition'] == 0 for row in expected), 24)
        self.assertEqual(sum(row['transition'] == 1 for row in expected), 2)
        self.assertTrue(all(row['planned_at'] < '2026-09-30T08:54:30+00:00' for row in expected))

    def test_finish_guard_and_abort_preserve_errors_and_refuse_repeat(self):
        self.terminal_boundary(aborted=True)

    def test_elapsed_finish_preserves_errors_and_refuses_repeat(self):
        self.terminal_boundary(aborted=False)

    def test_normal_finish_waits_for_complete_monotonic_duration(self):
        self.terminal_boundary(aborted=False, remaining=0.25)

    def test_abort_before_launch_skips_the_unloaded_finish_timer(self):
        record = self.terminal_boundary(aborted=True, finish_timer='not-found')
        self.assertNotIn('cancel_timers', record['errors'])
        self.assertEqual(record['cancel_timers']['command'],
                         ['systemctl', 'stop', observe.SAMPLER + '.timer'])
        self.assertEqual(record['cancel_timers']['load_states'][observe.FINISH + '.timer'], 'not-found')

    def test_failed_stop_of_a_loaded_timer_remains_an_error(self):
        record = self.terminal_boundary(aborted=True, timer_stop_rc=1)
        self.assertIn('cancel_timers', record['errors'])

    def terminal_boundary(self, aborted, remaining=None, finish_timer='loaded', timer_stop_rc=0):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            now = datetime.datetime.now(datetime.timezone.utc)
            collect.write_json(out / 'observation.json', {
                'started_at': now.isoformat(), 'earliest_finish_at': (now + datetime.timedelta(seconds=7200)).isoformat(),
                'duration_seconds': 7200, 'boot_id': observe.BOOT.read_text().strip(),
                'monotonic_start': time.monotonic()})
            stops = []

            def transport(args, **kwargs):
                stdout, rc = '', 0
                if args[:2] == ['systemctl', 'show']:
                    if 'LoadState' in args:
                        stdout = finish_timer if observe.FINISH + '.timer' in args else 'loaded'
                    elif 'TimeoutStopUSec' in args:
                        stdout = '5min'
                    elif observe.SAMPLER + '.service' in args:
                        stdout = 'inactive'
                    else:
                        stdout = 'ActiveState=' + ('inactive' if stops else 'active') + '\nResult=success'
                elif args[:3] == ['systemctl', 'stop', collect.UNIT]:
                    stops.append(args)
                elif args[:2] == ['systemctl', 'stop'] and observe.SAMPLER + '.timer' in args:
                    rc = 5 if finish_timer != 'loaded' and observe.FINISH + '.timer' in args else timer_stop_rc
                elif args[0] == '/usr/bin/python3':
                    rc = 1
                elif args[0] == 'pgrep':
                    rc = 1
                return subprocess.CompletedProcess(args, rc, stdout, '')

            with patch.object(observe, 'OUT', out), patch.object(collect, 'STORE', out), \
                    patch('subprocess.run', side_effect=transport), \
                    contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(RuntimeError, 'window has not elapsed'):
                    observe.finish()
                self.assertFalse(stops)
                if not aborted:
                    manifest = json.loads((out / 'observation.json').read_text())
                    manifest['started_at'] = (now - datetime.timedelta(seconds=7201)).isoformat()
                    manifest['earliest_finish_at'] = (now - datetime.timedelta(seconds=1)).isoformat()
                    collect.write_json(out / 'observation.json', manifest)
                    with self.assertRaisesRegex(RuntimeError, 'monotonic observation duration'):
                        observe.finish()
                    self.assertFalse(stops)
                    manifest['monotonic_start'] = time.monotonic() - 7200 + (remaining if remaining is not None else -1)
                    collect.write_json(out / 'observation.json', manifest)
                with contextlib.ExitStack() as clock_boundary:
                    if remaining is not None:
                        clock = [manifest['monotonic_start'] + 7200 - remaining]
                        clock_boundary.enter_context(patch('time.monotonic', side_effect=lambda: clock[0]))
                        clock_boundary.enter_context(patch('time.sleep', side_effect=lambda seconds:
                                                           clock.__setitem__(0, clock[0] + seconds)))
                    self.assertTrue(observe.terminal(aborted=aborted, reason='local_boundary_test'))
                self.assertEqual(len(stops), 1)
                record = json.loads((out / ('abort.json' if aborted else 'shutdown.json')).read_text())
                self.assertEqual(record['verdict'], 'Incomplete')
                self.assertEqual(record['terminal_kind'], 'abort' if aborted else 'finish')
                if not aborted:
                    self.assertGreaterEqual(record['monotonic_elapsed_seconds'], 7200)
                self.assertFalse((out / ('shutdown.json' if aborted else 'abort.json')).exists())
                self.assertIn('final_sample', record['errors'])
                self.assertIn('complete_gc_recordings', record['errors'])
                with self.assertRaisesRegex(RuntimeError, 'terminal operation'):
                    observe.finish()
                self.assertEqual(len(stops), 1)
                return record

    def test_installed_timeout_parser(self):
        self.assertEqual(observe.timeout_seconds('5min'), 300)
        self.assertEqual(observe.timeout_seconds('1min 500ms'), 60.5)
        with self.assertRaises(RuntimeError):
            observe.timeout_seconds('infinity')

    def test_java_nanosecond_timestamp_is_readable_on_python_three_nine(self):
        value = evaluate.epoch('2026-09-30T06:00:00.123456789Z')
        self.assertEqual(value, datetime.datetime(2026, 9, 30, 6, 0, 0, 123456,
                                                  tzinfo=datetime.timezone.utc).timestamp())


class AbortPolicyTests(unittest.TestCase):
    """The shipped counters and abort decision, driven by real sample summaries at the systemd boundary."""

    def summary(self, raw, *checks):
        """Each check is a name or a (name, message) pair, as collect.py records them."""
        errors = [(check, check) if isinstance(check, str) else check for check in checks]
        return {'sample_kind': 'full', 'completed_at': '2026-10-12T12:35:04+00:00', 'raw_directory': str(raw),
                'disk': {'available_bytes': 20 * 1024 ** 3},
                'errors': [{'check': check, 'type': 'RuntimeError', 'message': message} for check, message in errors]}

    def run_samples(self, out, samples):
        """Apply the shipped counters and abort decision to consecutive full samples; return the abort requests."""
        requests = []

        def transport(args, **kwargs):
            requests.append(args)
            return subprocess.CompletedProcess(args, 0, '', '')

        state = {}
        policy = collect.abort_policy(out)
        for index, checks_failed in enumerate(samples):
            raw = out / 'raw' / ('sample-' + str(index))
            raw.mkdir(parents=True)
            summary = self.summary(raw, *checks_failed)
            collect.write_json(raw / 'sample.json', summary)
            state.update(collect.failure_counters(state, summary, **policy))
            with patch('subprocess.run', side_effect=transport):
                collect.abort_if_required(out, summary, state)
        return requests, state

    def observation(self, out):
        collect.write_json(out / 'observation.json',
                           {'abort_policy': {'consecutive_failures': 2, 'checks': list(contract.ABORT_CHECKS),
                                             'jvms': list(contract.ABORT_JVMS)}})

    def test_instrument_failures_never_request_abort_and_stay_counted(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            self.observation(out)
            requests, state = self.run_samples(out, [('gc',), ('gc',), ('gc', 'latency'), ('journal_retention_budget',)])
            self.assertEqual(requests, [])
            self.assertFalse((out / 'abort-request.json').exists())
            self.assertEqual(state['consecutive_failures'], 4)
            self.assertEqual(state['consecutive_abort_failures'], 0)

    def test_two_consecutive_abort_listed_failures_request_abort(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            self.observation(out)
            requests, state = self.run_samples(out, [('pv_status',), ('gc', 'appliance')])
            self.assertEqual(len(requests), 1)
            self.assertIn(collect.ABORT_UNIT, requests[0])
            request = json.loads((out / 'abort-request.json').read_text())
            self.assertEqual(request['reason'], 'consecutive_sample_failures')
            self.assertTrue(request['trigger_sample'].endswith('sample-1/sample.json'))
            self.assertEqual(state['consecutive_abort_failures'], 2)

    def test_an_instrument_failure_between_two_abort_listed_failures_resets_the_count(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            self.observation(out)
            requests, state = self.run_samples(out, [('pv_status',), ('gc',), (('jvm_restart', 'etl'),)])
            self.assertEqual(requests, [])
            self.assertEqual(state['consecutive_failures'], 3)
            self.assertEqual(state['consecutive_abort_failures'], 1)

    def test_disk_reserve_still_requests_abort_at_once(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            self.observation(out)
            raw = out / 'raw' / 'low'
            raw.mkdir(parents=True)
            summary = dict(self.summary(raw), disk={'available_bytes': measure.MINIMUM_FREE_BYTES - 1})
            requests = []
            with patch('subprocess.run', side_effect=lambda args, **k: requests.append(args) or
                       subprocess.CompletedProcess(args, 0, '', '')):
                collect.abort_if_required(out, summary, collect.failure_counters({}, summary, contract.ABORT_CHECKS))
            self.assertEqual(len(requests), 1)
            self.assertEqual(json.loads((out / 'abort-request.json').read_text())['reason'], 'disk_reserve')

    def test_manifest_without_a_check_list_uses_the_contract_default(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            collect.write_json(out / 'observation.json', {'abort_policy': {'consecutive_failures': 2}})
            self.assertEqual(collect.abort_checks(out), set(contract.ABORT_CHECKS))
            requests, _ = self.run_samples(out, [('collection',), ('collection',)])
            self.assertEqual(len(requests), 1)

    def test_abort_listed_checks_are_the_evidence_stopping_ones(self):
        self.assertEqual(set(contract.ABORT_CHECKS),
                         {'appliance', 'journal', 'collection', 'jvm_restart', 'instances', 'pv_status'})
        self.assertEqual(set(contract.ABORT_JVMS), {'engine', 'etl'})
        self.assertTrue(set(contract.ABORT_CHECKS) <= set(contract.SCHEDULER_CHECKS))
        for name in ('mgmt', 'pv_status_request', 'metrics_request', 'clock', 'tool_bundle', 'fixture_adjustment',
                     'health_invocation'):
            self.assertIn(name, contract.SCHEDULER_CHECKS)
            self.assertNotIn(name, contract.ABORT_CHECKS)
        self.assertEqual(set(contract.SCHEDULER_CHECKS) & {'gc', 'latency', 'journal_retention_budget',
                                                            'kernel_journal', 'heap', 'process', 'metrics',
                                                            'event_rates'}, set())

    def test_verdict_deciding_but_not_abort_listed_checks_never_request_abort(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            self.observation(out)
            requests, state = self.run_samples(out, [('mgmt', 'pv_status_request'), ('metrics_request', 'clock'),
                                                     ('health_invocation',), ('tool_bundle', 'fixture_adjustment')])
            self.assertEqual(requests, [])
            self.assertEqual(state['consecutive_abort_failures'], 0)

    def test_jvm_identity_errors_count_only_for_the_etl_and_engine_jvms(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            self.observation(out)
            requests, state = self.run_samples(out, [(('jvm_restart', 'mgmt'),),
                                                     (('instances', 'expected four live JVMs; missing: retrieval'),)])
            self.assertEqual(requests, [])
            self.assertEqual(state['consecutive_abort_failures'], 0)
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            self.observation(out)
            requests, state = self.run_samples(out, [(('jvm_restart', 'etl'),),
                                                     (('instances', 'expected four live JVMs; missing: engine,retrieval'),)])
            self.assertEqual(len(requests), 1)
            self.assertEqual(state['consecutive_abort_failures'], 2)


class RecordOnlyStartTests(unittest.TestCase):
    """The shipped observe.start with only a preparation and a readiness sample, at the systemd boundary."""

    def prepared_out(self, out):
        configuration = contract.chain_configuration('shortened')
        collect.write_json(out / 'preparation.json', {'schema': contract.SCHEMA, 'duration_seconds': 86400,
                                                      'configuration': configuration})
        collect.write_json(out / 'latest-full.json', {
            'sample_kind': 'full', 'errors': [{'check': 'gc', 'message': 'instrument'}],
            'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'raw_directory': str(out / 'raw' / 'readiness'), 'metrics_observed_at': '2026-10-12T23:00:00+00:00',
            'archiving_pvs': 903, 'connected_pvs': 903, 'fixture_sha256': contract.FIXTURE_SHA,
            'live_instances': list(collect.INSTANCES), 'clock': 'NTPSynchronized=yes'})
        collect.write_json(out / 'state.json', {'processes': {name: {'pid': str(100 + index), 'start': '1'}
                                                            for index, name in enumerate(collect.INSTANCES)}})
        (out / 'passes.jsonl').write_text('{}\n')

    def systemd(self, calls):
        def run(args, **kwargs):
            calls.append(args)
            rc = 1 if args[:2] == ['systemctl', 'start'] else 0
            return subprocess.CompletedProcess(args, rc, 'ActiveState=active\nInvocationID=abc\n', '')
        return run

    def test_readiness_only_reports_findings_without_starting_or_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            out, units = Path(directory) / 'out', Path(directory) / 'units'
            out.mkdir()
            units.mkdir()
            self.prepared_out(out)
            before = {path.name: path.read_bytes() for path in out.iterdir()}
            calls = []
            with patch.object(observe, 'OUT', out), patch.object(observe, 'UNITS', units), \
                    patch.object(collect, 'STORE', out), patch('subprocess.run', side_effect=self.systemd(calls)):
                report = observe.start(86400, 'shortened', readiness_only=True)
            self.assertIn('readiness_sample', {row['check'] for row in report['start_findings']})
            self.assertFalse(any('journal_retention' in row['check'] for row in report['start_findings']))
            self.assertEqual({path.name: path.read_bytes() for path in out.iterdir()}, before)
            self.assertEqual(list(units.iterdir()), [])
            self.assertFalse(any(args[:2] in (['systemctl', 'start'], ['systemctl', 'stop'],
                                             ['systemctl', 'enable'], ['systemctl', 'daemon-reload'])
                                 for args in calls))

    def test_missing_proofs_are_recorded_and_the_observation_opens(self):
        with tempfile.TemporaryDirectory() as directory:
            out, units = Path(directory) / 'out', Path(directory) / 'units'
            out.mkdir()
            units.mkdir()
            self.prepared_out(out)
            calls = []
            with patch.object(observe, 'OUT', out), patch.object(observe, 'UNITS', units), \
                    patch.object(collect, 'STORE', out), patch('subprocess.run', side_effect=self.systemd(calls)), \
                    contextlib.redirect_stdout(io.StringIO()):
                observe.start(86400, 'shortened')
            manifest = json.loads((out / 'observation.json').read_text())
            recorded = {row['check'] for row in manifest['start_findings']}
            for name in ('readiness_sample', 'tool_bundle', 'health_verification', 'runtime_proofs',
                         'chain_verification', 'focused_continuity'):
                self.assertIn(name, recorded)
            self.assertNotIn('capacity', recorded)
            self.assertEqual(len(manifest['expected_firings']), 312)
            self.assertEqual(json.loads((out / 'initial-sample.json').read_text())['rc'], 1)
            self.assertTrue((units / (observe.FINISH + '.timer')).exists())
            self.assertIn(['systemctl', 'enable', '--now', observe.SAMPLER + '.timer', observe.FINISH + '.timer'], calls)

    def test_free_space_below_the_reserve_still_refuses_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            out, units = Path(directory) / 'out', Path(directory) / 'units'
            out.mkdir()
            units.mkdir()
            self.prepared_out(out)
            with patch.object(observe, 'OUT', out), patch.object(observe, 'UNITS', units), \
                    patch.object(collect, 'STORE', out), patch.object(measure, 'MINIMUM_FREE_BYTES', 10 ** 18), \
                    patch('subprocess.run', side_effect=self.systemd([])):
                with self.assertRaisesRegex(RuntimeError, 'below the 2 GiB reserve'):
                    observe.start(86400, 'shortened')
            self.assertFalse((out / 'observation.json').exists())
            self.assertEqual(list(units.iterdir()), [])

    def test_an_existing_observation_is_never_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            collect.write_json(out / 'observation.json', {'started_at': 'kept'})
            with patch.object(observe, 'OUT', out), self.assertRaisesRegex(RuntimeError, 'refusing to replace'):
                observe.start(86400, 'shortened')
            self.assertEqual(json.loads((out / 'observation.json').read_text()), {'started_at': 'kept'})


class RecordOnlyMeasurementTests(unittest.TestCase):
    """The shipped measurement on a host without the appliance: every step fails and is recorded."""

    def initializer(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('initialize_fresh', HERE / 'initialize-fresh.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_failed_steps_are_recorded_and_the_measurement_record_is_written(self):
        initializer = self.initializer()
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'out'
            out.mkdir()
            target = Path(directory) / 'measurements'
            with patch.object(observe, 'OUT', out), patch.object(collect, 'STORE', out), \
                    patch.object(initializer, 'MEASUREMENT_INTERVAL_SECONDS', 0), \
                    patch('subprocess.run', return_value=subprocess.CompletedProcess([], 1, '', 'unavailable')):
                record = initializer.measurements(target, 86400, 'shortened')
            written = json.loads((target / 'measurements.json').read_text())
            self.assertEqual(written, record)
            checks = {row['check'] for row in record['findings']}
            for name in ('check', 'gc', 'latency'):
                self.assertIn(name, checks)
            self.assertFalse(any(name.startswith('capacity') for name in checks))
            self.assertNotIn('required_growth_bytes', record)
            self.assertEqual(len(list(target.glob('progress-*.json'))), initializer.MEASUREMENT_INTERVALS + 1)

    def test_snapshots_are_spaced_from_the_previous_snapshot_not_from_the_pass_start(self):
        initializer = self.initializer()
        import itertools

        class Clock:
            now = 0.0

            def monotonic(self):
                return self.now

            def sleep(self, seconds):
                self.now += seconds

        clock = Clock()
        preamble = itertools.cycle((0.17, 0.07, 0.16, 0.07, 0.12, 0.07, 0.10))

        def transport(args, **kwargs):
            clock.now += next(preamble)
            return subprocess.CompletedProcess(args, 1, '', 'unavailable')

        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'out'
            out.mkdir()
            target = Path(directory) / 'measurements'
            with patch.object(observe, 'OUT', out), patch.object(collect, 'STORE', out), \
                    patch.object(initializer, 'time', clock), \
                    patch('subprocess.run', side_effect=transport):
                record = initializer.measurements(target, 86400, 'shortened')
            files = sorted(target.glob('progress-*.json'))
            self.assertEqual(len(files), initializer.MEASUREMENT_INTERVALS + 1)
            times = [json.loads(path.read_text())['monotonic'] for path in files]
            spacing = [later - earlier for earlier, later in zip(times, times[1:])]
            self.assertTrue(all(gap >= initializer.MEASUREMENT_INTERVAL_SECONDS for gap in spacing), spacing)
            self.assertNotIn('measurement_interval', {row['check'] for row in record['findings']})

    def test_free_space_below_the_reserve_refuses_the_measurement(self):
        initializer = self.initializer()
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'out'
            out.mkdir()
            target = Path(directory) / 'measurements'
            with patch.object(observe, 'OUT', out), patch.object(collect, 'STORE', out), \
                    patch.object(measure, 'MINIMUM_FREE_BYTES', 10 ** 18):
                with self.assertRaisesRegex(RuntimeError, 'below the 2 GiB reserve'):
                    initializer.measurements(target, 86400, 'shortened')
            self.assertFalse(target.exists())


class SnapshotArchiveTests(unittest.TestCase):
    def test_snapshot_dump_is_not_refused_by_the_size_of_the_retained_archive(self):
        self.assertFalse(hasattr(measure, 'JFR_ARCHIVE_LIMIT_BYTES'))
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            raw = out / 'raw' / 'now'
            raw.mkdir(parents=True)
            (out / 'jvm').mkdir()
            earlier = out / 'raw' / 'earlier'
            earlier.mkdir()
            with (earlier / 'engine.jfr').open('wb') as stream:
                stream.truncate(600 * 1024 ** 2)

            def jcmd(args, timeout=90):
                Path(args[args.index('filename=' + str(out / 'jvm' / 'engine-checkpoint.jfr'))][9:]).write_bytes(b'JFR')
                return 'Dumped recording'

            with patch.object(measure, 'command', side_effect=jcmd):
                destination = measure.dump_jfr(out, raw, 'engine', '4242')
            self.assertEqual(destination, raw / 'engine.jfr')
            self.assertEqual(destination.read_bytes(), b'JFR')
            self.assertIn('Dumped recording', (raw / 'engine-jfr-dump.txt').read_text())


if __name__ == '__main__':
    unittest.main()
