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


if __name__ == '__main__':
    unittest.main()
