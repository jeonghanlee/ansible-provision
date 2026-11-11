#!/usr/bin/env python3
"""Verify saved query bounds against real CA reads and received HTTP requests."""

import argparse
import collections
import csv
import datetime
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib
import json
import os
from pathlib import Path
import re
import signal
import socket
import subprocess
import sys
import threading
import time
import traceback
import urllib.parse

HERE = Path(__file__).resolve().parent
FIXTURES = HERE.parent / 'fixtures'
CASE_TIMEOUT_SECONDS = 90
READINESS_SECONDS = 20
STABILITY_SECONDS = 1.1
SAMPLE_PATTERN = re.compile(r'^(\S+)\s+(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+)\s+(.*)$')


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def run(args):
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    args.evidence_created = True
    tools, base = args.tools.resolve(), args.base.resolve()
    binary = base / 'bin/linux-x86_64'
    sys.path.insert(0, str(tools))
    measure = importlib.import_module('measure')
    contract = importlib.import_module('contract')
    sources = {name: digest(tools / name) for name in contract.BUNDLE_FILES}
    dependencies = {str(binary / name): digest(binary / name) for name in ('softIoc', 'caget', 'caRepeater')}
    fixtures = {name: digest(FIXTURES / name) for name in ('aasoak.db', 'load1.db', 'load2.db', 'pvs-all.csv')}
    save(output / 'sources.json', {'tools': sources, 'dependencies': dependencies, 'fixtures': fixtures,
                                 'test_sha256': digest(Path(__file__).resolve())})
    with (FIXTURES / 'pvs-all.csv').open(newline='') as stream:
        pvs = [row['pv'] for row in csv.DictReader(stream)]
    if len(pvs) != 903 or len(set(pvs)) != 903:
        raise RuntimeError('The shipped 903-PV fixture is required')
    commands = []

    def command(argv):
        began = time.monotonic()
        result = subprocess.run(argv, env=environment, capture_output=True, text=True, timeout=10)
        prefix = output / ('command-%03d' % len(commands))
        prefix.with_suffix('.stdout').write_text(result.stdout)
        prefix.with_suffix('.stderr').write_text(result.stderr)
        record = {'command': argv, 'returncode': result.returncode,
                  'elapsed_seconds': time.monotonic() - began}
        prefix.with_suffix('.json').write_text(json.dumps(record, indent=2) + '\n')
        commands.append(record)
        return result

    def capture():
        response = command([str(binary / 'caget'), '-w', '0.5', '-a', '-#', '1', *pvs])
        samples = {}
        for line in response.stdout.splitlines():
            match = SAMPLE_PATTERN.match(line)
            if match and match[1] in pvs:
                stamp = datetime.datetime.fromisoformat(match[2]).replace(tzinfo=datetime.timezone.utc)
                elapsed = stamp - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
                samples[match[1]] = {'secs': elapsed.days * 86400 + elapsed.seconds,
                                    'nanos': stamp.microsecond * 1000}
        return samples

    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        ca_port = probe.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        probe.bind(('127.0.0.1', 0))
        repeater_port = probe.getsockname()[1]
    environment = dict(os.environ, EPICS_CAS_INTF_ADDR_LIST='127.0.0.1',
                       EPICS_CAS_BEACON_ADDR_LIST='127.0.0.1', EPICS_CAS_AUTO_BEACON_ADDR_LIST='NO',
                       EPICS_CAS_SERVER_PORT=str(ca_port), EPICS_CA_SERVER_PORT=str(ca_port),
                       EPICS_CA_REPEATER_PORT=str(repeater_port),
                       EPICS_CA_ADDR_LIST='127.0.0.1', EPICS_CA_AUTO_ADDR_LIST='NO', TZ='UTC')
    old_port = os.environ.get('EPICS_CA_SERVER_PORT')
    old_repeater_port = os.environ.get('EPICS_CA_REPEATER_PORT')
    os.environ['EPICS_CA_SERVER_PORT'] = str(ca_port)
    os.environ['EPICS_CA_REPEATER_PORT'] = str(repeater_port)
    ioc, repeater, server, worker = None, None, None, None
    received = []
    checks = []
    started = time.monotonic()
    failure = None
    ioc_log = (output / 'ioc.stdout').open('w')
    ioc_errors = (output / 'ioc.stderr').open('w')
    repeater_log = (output / 'repeater.log').open('w')
    try:
        repeater = subprocess.Popen([str(binary / 'caRepeater')], env=environment,
                                    stdout=repeater_log, stderr=repeater_log)
        argv = [str(binary / 'softIoc'), '-D', str(base / 'dbd/softIoc.dbd')]
        for name in ('aasoak.db', 'load1.db', 'load2.db'):
            argv += ['-d', str(FIXTURES / name)]
        save(output / 'ioc-command.json', {'command': argv, 'ca_port': ca_port})
        ioc = subprocess.Popen(argv, env=environment, stdin=subprocess.PIPE,
                               stdout=ioc_log, stderr=ioc_errors, text=True, cwd=output)
        deadline = time.monotonic() + READINESS_SECONDS
        while True:
            samples = capture()
            if len(samples) == len(pvs):
                break
            if ioc.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError('Native IOC readiness was not established')
        record_names, scanning = [], []
        for name in ('aasoak.db', 'load1.db', 'load2.db'):
            text = (FIXTURES / name).read_text()
            for match in re.finditer(r'record\([^,]+,\s*"([^"]+)"\)\s*\{(.*?)\n\}', text, re.S):
                record_names.append(match[1])
                if 'field(SCAN,' in match[2]:
                    scanning.append(match[1])
        preparation = ''.join('dbpf("%s.SCAN", "Passive")\n' % name for name in scanning)
        preparation += ''.join('dbpf("%s.PROC", "1")\n' % name for name in record_names)
        preparation += 'epicsEnvSet("QUERY_FIXTURE_READY", "yes")\nepicsEnvShow("QUERY_FIXTURE_READY")\n'
        (output / 'fixture-prepare.iocsh').write_text(preparation)
        ioc.stdin.write(preparation)
        ioc.stdin.flush()
        deadline = time.monotonic() + READINESS_SECONDS
        while 'QUERY_FIXTURE_READY=yes' not in (output / 'ioc.stdout').read_text():
            if ioc.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError('Native fixture preparation did not finish')
            threading.Event().wait(0.05)
        samples = capture()
        if len(samples) != len(pvs) or any(not 0 <= time.time() - value['secs'] < 15 for value in samples.values()):
            raise RuntimeError('Native fixture lacks complete recent CA samples')
        stable_started = time.monotonic()
        threading.Event().wait(STABILITY_SECONDS)
        if samples != capture():
            raise RuntimeError('Native IOC samples did not remain stable after fixing SCAN')
        save(output / 'native-samples.json', samples)
        save(output / 'fixture-ready.json', {'actual_pvs': len(samples),
             'stable_elapsed_seconds': time.monotonic() - stable_started, 'ioc_pid': ioc.pid,
             'repeater_pid': repeater.pid, 'repeater_active': repeater.poll() is None})
        counts = collections.Counter()

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                pv, lower, upper = (parsed[key][0] for key in ('pv', 'from', 'to'))
                width = (datetime.datetime.fromisoformat(upper.replace('Z', '+00:00')) -
                         datetime.datetime.fromisoformat(lower.replace('Z', '+00:00'))).total_seconds()
                counts[pv] += int(width < 1)
                step = counts[pv]
                status = 503 if args.case == 'recovery' and width < 1 and step == 1 else 200
                empty = args.case == 'recovery' and width < 1 and step == 2
                payload = [] if empty or status != 200 else [{'data': [samples[pv]]}]
                body = json.dumps(payload).encode()
                received.append({'pv': pv, 'query_start': lower, 'query_end': upper,
                                 'status': status, 'body_sha256': hashlib.sha256(body).hexdigest(),
                                 'empty': empty, 'visibility': width < 1})
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *unused):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        worker = threading.Thread(target=server.serve_forever)
        worker.start()
        measure.CAGET = str(binary / 'caget')
        measure.RETRIEVAL = 'http://127.0.0.1:%d/retrieval/data/getData.json' % server.server_port
        raw = output / 'raw'
        raw.mkdir()
        summary = measure.latency(output, raw, FIXTURES / 'pvs-all.csv',
                                  datetime.datetime.now(datetime.timezone.utc).isoformat())
        save(output / 'native-summary.json', summary)
    except Exception as error:
        failure = error
        (output / 'execution-error.txt').write_text(traceback.format_exc())
    finally:
        if server is not None:
            server.shutdown()
            worker.join(timeout=5)
            server.server_close()
        if ioc is not None and ioc.poll() is None:
            try:
                ioc.stdin.write('exit\n')
                ioc.stdin.flush()
                ioc.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                ioc.terminate()
                ioc.wait(timeout=5)
                failure = failure or RuntimeError('Native IOC did not exit normally')
        if repeater is not None and repeater.poll() is None:
            repeater.terminate()
            repeater.wait(timeout=5)
        save(output / 'terminal.json', {'ioc_returncode': ioc.returncode if ioc else None,
             'repeater_returncode': repeater.returncode if repeater else None,
             'http_thread_stopped': worker is None or not worker.is_alive(),
             'elapsed_seconds': time.monotonic() - started})
        save(output / 'http-requests.json', received)
        ioc_log.close()
        ioc_errors.close()
        repeater_log.close()
        if old_port is None:
            os.environ.pop('EPICS_CA_SERVER_PORT', None)
        else:
            os.environ['EPICS_CA_SERVER_PORT'] = old_port
        if old_repeater_port is None:
            os.environ.pop('EPICS_CA_REPEATER_PORT', None)
        else:
            os.environ['EPICS_CA_REPEATER_PORT'] = old_repeater_port
    if failure:
        raise failure

    def check(condition, message):
        checks.append({'passed': bool(condition), 'assertion': message})
        save(output / 'checks.json', checks)
        if not condition:
            raise AssertionError(message)

    check(ioc.returncode == 0, 'IOC stopped normally')
    freshness = json.loads((output / 'raw/freshness.json').read_text())
    visibility = json.loads((output / 'raw/visibility.json').read_text())
    check(len(freshness) == 903, 'all shipped freshness PVs were measured')
    check(len(visibility) == len(measure.REPRESENTATIVES), 'all shipped visibility representatives were measured')
    for record in freshness:
        matches = [row for row in received if row['pv'] == record['pv'] and not row['visibility']]
        check(len(matches) == 1, 'one actual freshness request per PV')
        for field in ('query_start', 'query_end'):
            check(field in record, field + ' is required')
            check(record[field] == matches[0][field], field + ' differs from received URL')
    for record in visibility:
        matches = [row for row in received if row['pv'] == record['pv'] and row['visibility']]
        expected = 3 if args.case == 'recovery' else 1
        check(len(matches) == len(record['attempts']) == expected, 'actual attempt count matches saved attempts')
        check(record['outcome'] == 'visible', 'actual visibility recovered')
        for attempt, actual in zip(record['attempts'], matches):
            for field in ('query_start', 'query_end'):
                check(field in attempt, field + ' is required')
                check(attempt[field] == actual[field], field + ' differs from received URL')
        if args.case == 'recovery':
            check(matches[0]['status'] == 503 and record['attempts'][0].get('error_type') == 'HTTPError',
                  'actual HTTP 503 remains an error attempt')
            check(matches[1]['empty'] and record['attempts'][1]['matching_samples'] == 0,
                  'actual empty reply remains an unsuccessful attempt')
    check(all(digest(tools / name) == value for name, value in sources.items()), 'runtime source bytes unchanged')
    check(all(digest(FIXTURES / name) == value for name, value in fixtures.items()), 'shipped fixture bytes unchanged')
    check(all(digest(Path(name)) == value for name, value in dependencies.items()), 'native dependency bytes unchanged')
    save(output / 'result.json', {'result': 'Passed', 'assertions': len(checks), 'http_requests': len(received),
         'case': args.case, 'scope': 'Native IOC/CA and HTTP-boundary metadata regression; no appliance or historical replay claim'})
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tools', type=Path, default=HERE)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', choices=('positive', 'recovery'), default='positive')
    args = parser.parse_args()
    def deadline(signum, frame):
        raise TimeoutError('Native query regression exceeded its case limit')
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(CASE_TIMEOUT_SECONDS)
    try:
        return run(args)
    except Exception as error:
        if getattr(args, 'evidence_created', False):
            save(args.output / 'result.json', {'result': 'Failed' if isinstance(error, AssertionError) else 'Incomplete',
                                             'error_type': type(error).__name__, 'error': str(error)})
        traceback.print_exc()
        return 1 if isinstance(error, AssertionError) else 2
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    raise SystemExit(main())
