#!/usr/bin/env python3
"""Exercise actual journal delivery and collector preservation on a dedicated host."""

import argparse
import concurrent.futures
import csv
import datetime
import fcntl
import json
import math
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

sys.dont_write_bytecode = True
import journal_coverage
import prepare

UTC = datetime.timezone.utc
PACKAGE = Path(__file__).resolve().parent
PERIODS = {'system': 1, 'kernel': 10, 'appliance': 1, 'health': 60}
QUERY_PERIOD = 1
COLLECTION_PERIOD = 300
VISIBILITY_WAIT = 60
ACTION_TIMEOUT = 30
WORKERS = {'system': 1, 'kernel': 1, 'appliance': 2 * ACTION_TIMEOUT + 1, 'health': 1}
TAG = 'JOURNAL_VALIDATION'
HEALTH_UNIT = 'journal-validation-health.service'
HEALTH_PREFIX = 'JOURNAL_VALIDATION_HEALTH '
HEALTH_REQUEST = prepare.RUNTIME / 'health-request.json'
HEALTH_RECEIPT = prepare.RUNTIME / 'health-receipt.json'
SOURCE_FIELDS = ('_BOOT_ID', '__CURSOR', '_TRANSPORT', '_SYSTEMD_UNIT',
                 '_SYSTEMD_INVOCATION_ID', '_PID', '_COMM', 'SYSLOG_IDENTIFIER')
APP_MESSAGE = re.compile(r'^(?:<7>)?DEBUG\s+\[([^]]+)\] ' + re.escape(prepare.LOGGER) + r' - (.*)$')
APP_TIMES = re.compile(r'^requestTimesOb is RequestTimes\[end=([^,]+), start=([^,]+), requestTimes=.*\]$')
HEALTH_MESSAGES = {
    '0': re.compile(r'^health PRESENT all-four-processes-verified; application-readiness-not-checked$'),
    '1': re.compile(r'^(health (FAIL|STARTING) .+|FAIL appliance-.+)$'),
    '2': re.compile(r'^(health ERROR .+|scheduled ERROR .+|ERROR .+)$'),
    '3': re.compile(r'^(scheduled SKIP .+|SKIP .+)$')}


class ConfirmedViolation(RuntimeError):
    """An observed identity or content violation prevents successful acceptance."""


def clock():
    return {'utc': datetime.datetime.now(UTC).isoformat(), 'monotonic_ns': time.monotonic_ns()}


def append(path, value):
    with path.open('a') as stream:
        stream.write(json.dumps(value, sort_keys=True) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def load_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def identity(row):
    journal_coverage.coordinates(row, row['_BOOT_ID'])
    return tuple(row.get(key) for key in SOURCE_FIELDS)


def command(arguments, destination, timeout=ACTION_TIMEOUT):
    receipt = {'command': arguments, 'started': clock()}
    try:
        result = subprocess.run(arguments, capture_output=True, timeout=timeout)
        destination.with_suffix('.stdout').write_bytes(result.stdout)
        destination.with_suffix('.stderr').write_bytes(result.stderr)
        receipt.update(returncode=result.returncode,
                       stdout_sha256=prepare.digest(result.stdout),
                       stderr_sha256=prepare.digest(result.stderr))
    except (OSError, subprocess.TimeoutExpired) as error:
        receipt['error'] = str(error)
        for suffix, data in (('stdout', getattr(error, 'output', None)),
                             ('stderr', getattr(error, 'stderr', None))):
            data = data or b''
            if isinstance(data, str):
                data = data.encode()
            destination.with_suffix('.' + suffix).write_bytes(data)
            receipt[suffix + '_sha256'] = prepare.digest(data)
    receipt['finished'] = clock()
    prepare.save(destination.with_suffix('.json'), receipt)
    return receipt


def request(url, destination):
    receipt = {'url': url, 'started': clock()}
    body = bytearray()
    try:
        try:
            response = urllib.request.build_opener(urllib.request.ProxyHandler({})).open(url, timeout=ACTION_TIMEOUT)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            receipt['status'] = response.code
            while True:
                if time.monotonic_ns() - receipt['started']['monotonic_ns'] > ACTION_TIMEOUT * 1000000000:
                    raise TimeoutError('HTTP response exceeded the action deadline')
                chunk = response.read(65536)
                if not chunk:
                    break
                body.extend(chunk)
    except (OSError, ValueError) as error:
        receipt['error'] = str(error)
    destination.with_suffix('.body').write_bytes(body)
    receipt['body_sha256'] = prepare.digest(body)
    receipt['finished'] = clock()
    prepare.save(destination.with_suffix('.json'), receipt)
    return receipt


def service(unit, destination):
    receipt = command(['systemctl', 'show', unit, '-p', 'ActiveState', '-p', 'MainPID',
                       '-p', 'InvocationID', '-p', 'ExecMainPID', '-p', 'ExecMainCode', '-p', 'ExecMainStatus',
                       '-p', 'ExecMainStartTimestampMonotonic', '-p', 'StandardOutput',
                       '-p', 'FragmentPath', '-p', 'DropInPaths', '-p', 'ControlGroup', '-p', 'ExecStart'], destination)
    if receipt.get('returncode') != 0:
        raise RuntimeError('Service properties are unavailable: ' + unit)
    return dict(line.split('=', 1) for line in destination.with_suffix('.stdout').read_text().splitlines()
                if '=' in line)


def preflight(config, evidence, allowed_boots=None):
    checks = {}
    checks['python_39_or_later'] = sys.version_info >= (3, 9)
    try:
        prepare.verify(PACKAGE)
        checks['package'] = True
    except (OSError, ValueError, RuntimeError) as error:
        checks['package'] = str(error)
    checks['root'] = os.geteuid() == 0
    checks['systemd_pid1'] = Path('/proc/1/comm').read_text().strip() == 'systemd'
    version = command(['systemctl', '--version'], evidence / 'systemd-version')
    checks['systemd_239'] = (version.get('returncode') == 0 and
                            (evidence / 'systemd-version.stdout').read_text().startswith('systemd 239 '))
    journal_version = command(['journalctl', '--version'], evidence / 'journalctl-version')
    checks['journalctl_239'] = (journal_version.get('returncode') == 0 and
                              (evidence / 'journalctl-version.stdout').read_text().startswith('systemd 239 '))
    binaries = {}
    for name in ('systemctl', 'journalctl', 'logger', 'python3'):
        located = shutil.which(name)
        if located:
            path = Path(located).resolve()
            binaries[name] = {'path': str(path), 'sha256': prepare.digest(path.read_bytes())}
    prepare.save(evidence / 'runtime-binaries.json', binaries)
    files = {}
    for base in ('/usr/lib/systemd', '/usr/local/lib/systemd', '/run/systemd', '/etc/systemd'):
        for path in [Path(base) / 'journald.conf', *sorted((Path(base) / 'journald.conf.d').glob('*.conf'))]:
            if path.is_file():
                try:
                    data = path.read_bytes()
                    files[str(path)] = {'sha256': prepare.digest(data), 'content': data.decode()}
                except (OSError, ValueError) as error:
                    files[str(path)] = {'error': str(error)}
    prepare.save(evidence / 'journald-configuration-sources.json', files)
    checks['persistent_journal'] = bool(list(journal_coverage.JOURNAL_ROOT.glob('*/*.journal')))
    checks['no_volatile_journal'] = not any(journal_coverage.VOLATILE_ROOT.glob('*/*.journal'))
    for key in ('softioc', 'health_script', 'appliance_artifact'):
        path = Path(config[key])
        checks[key] = path.is_file()
        if path.is_file():
            prepare.save(evidence / (key + '-identity.json'),
                         {'path': str(path), 'sha256': prepare.digest(path.read_bytes())})
    checks['kernel_device_writable'] = os.access('/dev/kmsg', os.W_OK)
    if checks['systemd_pid1']:
        try:
            for key, unit in (('appliance', config['appliance_unit']),
                              ('fixture', 'journal-validation-ioc.service')):
                properties = service(unit, evidence / (key + '-service'))
                checks[key + '_active'] = properties.get('ActiveState') == 'active'
                if key == 'fixture':
                    invocation = properties.get('ExecStart', '')
                    checks['fixture_command_matches'] = (config['softioc'] in invocation and all(
                        str(PACKAGE / name) in invocation for name in prepare.FIXTURES if name.endswith('.db')))
                if key == 'appliance':
                    checks['appliance_stdout_journal'] = properties.get('StandardOutput') in ('journal', 'journal+console')
                    candidates = []
                    argument = ('-Dcatalina.base=' + config['retrieval_catalina_base']).encode()
                    group = properties.get('ControlGroup')
                    for process in Path('/proc').glob('[0-9]*'):
                        try:
                            if argument not in (process / 'cmdline').read_bytes().split(b'\0'):
                                continue
                            groups = [line.split(':', 2)[2] for line in (process / 'cgroup').read_text().splitlines()]
                            if not group or not any(value == group or value.startswith(group + '/') for value in groups):
                                continue
                            environment = (process / 'environ').read_bytes().split(b'\0')
                            configured = b'LOG4J_CONFIGURATION_FILE=' + str(PACKAGE / 'log4j2.xml').encode()
                            candidates.append({'pid': process.name, 'catalina_base': config['retrieval_catalina_base'],
                                               'environment': {value.split(b'=', 1)[0].decode(): value.split(b'=', 1)[1].decode()
                                                               for value in environment if b'=' in value and
                                                               value.split(b'=', 1)[0] in (
                                                                   b'LOG4J_CONFIGURATION_FILE', b'EPICS_CA_ADDR_LIST',
                                                                   b'EPICS_CA_AUTO_ADDR_LIST', b'EPICS_CA_MAX_ARRAY_BYTES')},
                                               'logging_configuration_matches': configured in environment})
                        except FileNotFoundError:
                            continue
                    prepare.save(evidence / 'retrieval-process.json', candidates)
                    checks['appliance_logging_environment'] = len(candidates) == 1 and candidates[0]['logging_configuration_matches']
            checks['journal_daemon'] = bool(journal_coverage.daemon_identity())
            headers = journal_coverage.file_headers()
            boot = journal_coverage.BOOT.read_text().strip().replace('-', '')
            if allowed_boots is None:
                checks['current_boot_files_only'] = bool(headers) and all(
                    row['boot_id'] == boot for row in headers if row['entries'])
            else:
                if not allowed_boots or not all(re.fullmatch(r'[0-9a-f]{32}', value) for value in allowed_boots):
                    raise RuntimeError('The declared journal boot identities are invalid')
                checks['declared_boot_files_only'] = (boot in allowed_boots and bool(headers) and all(
                    row['boot_id'] in allowed_boots for row in headers if row['entries']))
                prepare.save(evidence / 'declared-journal-boots.json', {'current': boot, 'allowed': allowed_boots})
            prepare.save(evidence / 'journal-headers.json', headers)
        except (OSError, ValueError, RuntimeError) as error:
            checks['runtime_identity'] = str(error)
    if checks.get('appliance_active'):
        response = request(config['mgmt_url'].rstrip('/') + '/getAllPVs?limit=-1', evidence / 'registered-pvs')
        try:
            registered = json.loads((evidence / 'registered-pvs.body').read_text())
            wanted = {row['pv'] for row in csv.DictReader((PACKAGE / 'pvs-all.csv').open())}
            checks['registered_903_fixture'] = (response.get('status') == 200 and not response.get('error') and
                                               isinstance(registered, list) and wanted <= set(registered))
        except (OSError, ValueError, TypeError) as error:
            checks['registered_903_fixture'] = str(error)
    ready = all(value is True for value in checks.values())
    ready = ready and all(key in checks for key in ('appliance_active', 'fixture_active',
                                                   'registered_903_fixture', 'journal_daemon'))
    result = {'observed': clock(), 'ready': ready, 'checks': checks,
              'fixture': prepare.fixture_contract((PACKAGE / 'pvs-all.csv').read_bytes())}
    prepare.save(evidence / 'preflight.json', result)
    return result


def health_event():
    action = json.loads(HEALTH_REQUEST.read_text())
    result = {'action_id': action['id'], 'observed': clock(),
              'invocation_id': os.environ.get('INVOCATION_ID'),
              'service_result': os.environ.get('SERVICE_RESULT'),
              'exit_code': os.environ.get('EXIT_CODE'), 'exit_status': os.environ.get('EXIT_STATUS')}
    result['service_at_completion'] = service(HEALTH_UNIT, prepare.RUNTIME / 'health-completion-service')
    prepare.save(HEALTH_RECEIPT, result)
    print(HEALTH_PREFIX + json.dumps(result, sort_keys=True), flush=True)


def emit(action, config, evidence):
    path = evidence / action['id']
    result = {'id': action['id'], 'path': action['path'], 'started': clock()}
    try:
        if action['path'] == 'system':
            result['execution'] = command(['logger', '--tag', TAG, '--priority', 'user.info',
                                            '--', action['message']], path)
            result['executed'] = result['execution'].get('returncode') == 0
        elif action['path'] == 'kernel':
            with open('/dev/kmsg', 'wb', buffering=0) as stream:
                payload = ('<6>' + action['message'] + '\n').encode()
                count = stream.write(payload)
            result.update(executed=count == len(payload), bytes_written=count)
        elif action['path'] == 'appliance':
            result['attempted'] = True
            result['execution'] = request(action['url'], path)
            result['executed'] = isinstance(result['execution'].get('status'), int) and not result['execution'].get('error')
        else:
            prepare.save(HEALTH_REQUEST, action)
            HEALTH_RECEIPT.unlink(missing_ok=True)
            result['execution'] = command(['systemctl', 'start', HEALTH_UNIT], path, timeout=45)
            result['service'] = service(HEALTH_UNIT, path.with_name(path.name + '-service'))
            receipt = json.loads(HEALTH_RECEIPT.read_text())
            result['health'] = receipt
            properties = receipt['service_at_completion']
            result['executed'] = (receipt['action_id'] == action['id'] and bool(receipt['invocation_id']) and
                                  bool(receipt['service_result']) and receipt['exit_code'] == 'exited' and
                                  int(properties.get('ExecMainPID', '0')) > 0 and
                                  properties.get('ExecMainStatus') == receipt['exit_status'] and
                                  properties.get('InvocationID') == receipt['invocation_id'] and
                                  int(properties.get('ExecMainStartTimestampMonotonic', '0')) >
                                  result['started']['monotonic_ns'] // 1000)
    except Exception as error:
        result.update(executed=False, error=str(error))
    result['finished'] = clock()
    prepare.save(path.with_name(path.name + '-outcome.json'), result)
    return result


def scheduled_sequences(duration, period, quiet_windows=()):
    for begin, end in quiet_windows:
        if (type(begin) is not int or type(end) is not int or
                not 0 <= begin < end <= duration):
            raise RuntimeError('A quiet interval must have valid declared elapsed boundaries')
    return [sequence for sequence in range(math.ceil(duration / period))
            if not any(begin <= sequence * period < end for begin, end in quiet_windows)]


def schedule(run_id, config, began, duration, quiet_kernel_windows=()):
    pvs = [row['pv'] for row in csv.DictReader((PACKAGE / 'pvs-all.csv').open())]
    epoch = 300000000 + int(run_id[:8], 16) % 500000000
    actions = []
    for path, period in PERIODS.items():
        quiet = quiet_kernel_windows if path == 'kernel' else ()
        for sequence in scheduled_sequences(duration, period, quiet):
            offset = sequence * period
            action_id = run_id + '-' + path + '-' + str(sequence)
            action = {'id': action_id, 'path': path, 'sequence': sequence, 'offset_seconds': offset,
                      'planned_monotonic_ns': began['monotonic_ns'] + offset * 1000000000,
                      'planned_utc': (datetime.datetime.fromisoformat(began['utc']) +
                                      datetime.timedelta(seconds=offset)).isoformat()}
            if path in ('system', 'kernel'):
                action['message'] = TAG + ' ' + json.dumps({'id': action_id, 'sequence': sequence}, sort_keys=True)
            elif path == 'appliance':
                start = datetime.datetime.fromtimestamp(epoch + sequence * 2, UTC)
                action.update(pv=pvs[sequence % len(pvs)],
                              start=start.isoformat().replace('+00:00', 'Z'),
                              end=(start + datetime.timedelta(seconds=1)).isoformat().replace('+00:00', 'Z'))
                action['url'] = config['retrieval_url'] + '?' + urllib.parse.urlencode(
                    {'pv': action['pv'], 'from': action['start'], 'to': action['end']})
            actions.append(action)
    return sorted(actions, key=lambda action: (action['planned_monotonic_ns'], action['path']))


class DirectReader:
    """Retain independent raw queries and source records before archive comparison."""

    def __init__(self, directory, config, boot, cursor):
        self.directory, self.config, self.boot, self.cursor = directory, config, boot, cursor
        self.stopping = threading.Event()
        self.error = None

    def read(self, number):
        started = clock()
        path = self.directory / ('query-' + str(number) + '.jsonl')
        rows = journal_coverage.query(['-b', self.boot, '--cursor', self.cursor,
                                       'SYSLOG_IDENTIFIER=' + TAG, '+', '_TRANSPORT=kernel', '+',
                                       '_SYSTEMD_UNIT=' + self.config['appliance_unit'], '+',
                                       '_SYSTEMD_UNIT=' + HEALTH_UNIT], path)
        finished = clock()
        for row in rows:
            identity(row)
        if rows:
            self.cursor = rows[-1]['__CURSOR']
        append(self.directory / 'queries.jsonl', {'file': path.name, 'started': started,
                                                 'finished': finished, 'records': len(rows),
                                                 'sha256': prepare.digest(path.read_bytes())})

    def run(self):
        number = 0
        try:
            while not self.stopping.is_set():
                self.read(number)
                number += 1
                self.stopping.wait(QUERY_PERIOD)
            self.read(number)
        except Exception as error:
            self.error = str(error)
            prepare.save(self.directory / 'error.json', {'observed': clock(), 'error': self.error})


class Collector:
    """Run the unchanged shipped collector with private ordered checkpoint state."""

    def __init__(self, directory, began, previous_checkpoint=None):
        self.directory, self.began, self.previous_checkpoint = directory, began, previous_checkpoint
        self.stopping = threading.Event()
        self.error = None

    def run(self):
        boundary = datetime.datetime.fromisoformat(self.began['utc']).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
        previous = self.previous_checkpoint or {'kernel_journal_since': boundary}
        number = 0
        try:
            while True:
                terminal = self.stopping.wait(COLLECTION_PERIOD)
                path = self.directory / ('interval-' + str(number))
                path.mkdir(mode=0o700)
                prepare.save(path / 'input-state.json', previous)
                started = clock()
                result = journal_coverage.collect(path, previous, datetime.datetime.now(UTC))
                prepare.save(path / 'result.json', {'started': started, 'finished': clock(), **result})
                previous = {'system_journal_checkpoint': result['checkpoint']}
                number += 1
                if terminal:
                    return
        except Exception as error:
            self.error = str(error)
            prepare.save(self.directory / 'error.json', {'observed': clock(), 'error': self.error})


def direct_records(directory):
    records = {}
    observed = {}
    for query in load_rows(directory / 'queries.jsonl'):
        path = directory / query['file']
        if prepare.digest(path.read_bytes()) != query['sha256']:
            raise RuntimeError('A direct query changed: ' + path.name)
        receipt = json.loads(path.with_suffix(path.suffix + '.receipt.json').read_text())
        if receipt['returncode'] != 0 or receipt['stderr'].strip() or receipt['stdout_sha256'] != query['sha256']:
            raise RuntimeError('A direct query did not complete successfully')
        for row in load_rows(path):
            key = identity(row)
            if key in records and records[key] != row:
                raise ConfirmedViolation('Direct query overlap contains conflicting content')
            records[key] = row
            observed.setdefault(key, query['finished'])
    return records, observed


def archive_records(directory):
    combined = {}
    previous_tail = None
    intervals = sorted(directory.glob('interval-*'), key=lambda path: int(path.name.split('-')[-1]))
    if not intervals:
        raise RuntimeError('No completed collector interval exists')
    for path in intervals:
        proof = json.loads((path / 'journal-coverage.json').read_text())
        raw = path / 'journal-sequence.jsonl'
        if proof.get('coverage_complete') is not True or prepare.digest(raw.read_bytes()) != proof['source_sha256']:
            raise RuntimeError('Collector interval has no unchanged complete proof: ' + path.name)
        rows = load_rows(raw)
        if not rows or rows[0]['__CURSOR'] != proof['system_anchor'] or rows[-1]['__CURSOR'] != proof['system_tail']:
            raise RuntimeError('Collector interval boundaries do not match its raw records')
        if previous_tail is not None and rows[0] != previous_tail:
            raise RuntimeError('Adjacent collector intervals lack an identical shared checkpoint')
        for index, row in enumerate(rows):
            key = identity(row)
            if previous_tail is not None and index == 0:
                continue
            if key in combined:
                raise ConfirmedViolation('Collector archive repeats an identity outside the declared checkpoint overlap')
            combined[key] = row
        previous_tail = rows[-1]
    return combined


def source_index(records, config):
    messages, application, pending = {}, {}, {}
    for row in sorted(records.values(), key=lambda entry: int(entry['__REALTIME_TIMESTAMP'])):
        message = row.get('MESSAGE')
        if isinstance(message, str):
            messages.setdefault(message, []).append(row)
        if (row.get('_SYSTEMD_UNIT') != config['appliance_unit'] or row.get('_TRANSPORT') != 'stdout' or
                row.get('PRIORITY') != '7'):
            continue
        match = APP_MESSAGE.fullmatch(str(message))
        if not match:
            continue
        thread, text = match.groups()
        context = (row.get('_PID'), thread)
        if text.startswith('pvName is '):
            pending[context] = row
        times = APP_TIMES.fullmatch(text)
        if times:
            pv = pending.pop(context, None)
            if pv is not None:
                name = APP_MESSAGE.fullmatch(pv['MESSAGE'])[2].removeprefix('pvName is ')
                key = (name, times[2], times[1])
                application.setdefault(key, []).extend((pv, row))
    return messages, application


def required_records(action, outcome, indexed_sources, config):
    messages, application = indexed_sources
    rows = messages.get(action.get('message'), [])
    if action['path'] in ('system', 'kernel'):
        transport = 'syslog' if action['path'] == 'system' else 'kernel'
        return [row for row in rows if row.get('MESSAGE') == action['message'] and
                row.get('_TRANSPORT') == transport and
                (transport == 'kernel' or (row.get('SYSLOG_IDENTIFIER') == TAG and row.get('_UID') == '0'))]
    if action['path'] == 'health':
        health = outcome.get('health', {})
        wanted = HEALTH_PREFIX + json.dumps(health, sort_keys=True)
        markers = [row for row in messages.get(wanted, []) if
                row.get('_TRANSPORT') == 'stdout' and row.get('_SYSTEMD_UNIT') == HEALTH_UNIT and
                row.get('_SYSTEMD_INVOCATION_ID') == health.get('invocation_id')]
        pattern = HEALTH_MESSAGES.get(health.get('exit_status'))
        main_pid = health.get('service_at_completion', {}).get('ExecMainPID')
        actual = [row for text, rows in messages.items() if pattern and pattern.fullmatch(text)
                  for row in rows if row.get('_TRANSPORT') == 'stdout' and
                  row.get('_SYSTEMD_UNIT') == HEALTH_UNIT and main_pid and row.get('_PID') == main_pid and
                  row.get('_SYSTEMD_INVOCATION_ID') == health.get('invocation_id')]
        return markers + actual if len(markers) == 1 and len(actual) == 1 else []
    begin = journal_coverage.timestamp(outcome['started']['utc'])
    end = journal_coverage.timestamp(outcome['finished']['utc']) + VISIBILITY_WAIT * 1000000
    return [row for row in application.get((action['pv'], action['start'], action['end']), [])
            if begin <= int(row['__REALTIME_TIMESTAMP']) <= end]


def inventory(directory):
    return {str(path.relative_to(directory)): {'sha256': prepare.digest(path.read_bytes()),
                                             'bytes': path.stat().st_size}
            for path in sorted(directory.rglob('*')) if path.is_file() and
            path.relative_to(directory).as_posix() not in ('artifact-index.json', 'result.json')}


def replay(directory):
    result = {'scope': 'basic-delivery-query-collection', 'full_day_acceptance': 'Pending',
              'one_hour_basic_acceptance': 'Incomplete',
              'delivery': 'Incomplete', 'later_live_read': 'Incomplete', 'collection': 'Incomplete',
              'overall': 'Incomplete', 'paths': {}, 'violations': [], 'unresolved': []}
    try:
        expected_index = json.loads((directory / 'artifact-index.json').read_text())
        if inventory(directory) != expected_index:
            raise RuntimeError('Saved evidence differs from the frozen artifact index')
        state = json.loads((directory / 'observation.json').read_text())
        if state['state'] != 'Finished':
            raise RuntimeError('The basic run did not finish: ' + state['state'])
        contract = json.loads((directory / 'contract.json').read_text())
        if contract['duration_seconds'] < 3600:
            result['scope'] = 'short-basic-probe'
        config = json.loads((directory / 'package/config.json').read_text())
        actions = load_rows(directory / 'schedule.jsonl')
        if prepare.digest((directory / 'schedule.jsonl').read_bytes()) != contract['schedule_sha256']:
            raise RuntimeError('The producer schedule differs from its frozen contract')
        outcomes = load_rows(directory / 'outcomes.jsonl')
        indexed = {row['id']: row for row in outcomes}
        if len(indexed) != len(outcomes) or set(indexed) - {row['id'] for row in actions}:
            raise RuntimeError('Producer outcomes repeat or contain unscheduled IDs')
        if len({action['id'] for action in actions}) != len(actions):
            raise RuntimeError('The frozen producer schedule repeats an ID')
        initial, first_seen = direct_records(directory / 'direct')
        indexed_sources = source_index(initial, config)
        final_path = directory / 'final-live.jsonl'
        final_receipt = json.loads((directory / 'final-live.jsonl.receipt.json').read_text())
        final = None
        if (final_receipt['returncode'] == 0 and not final_receipt['stderr'].strip() and
                final_receipt['stdout_sha256'] == prepare.digest(final_path.read_bytes())):
            final = {identity(row): row for row in load_rows(final_path)}
        else:
            result['unresolved'].append('The final live query did not complete successfully')
        archive = None
        archive_violation = False
        try:
            archive = archive_records(directory / 'collector')
        except ConfirmedViolation as error:
            archive_violation = True
            result['violations'].append(str(error))
        except (OSError, ValueError, KeyError, RuntimeError) as error:
            result['unresolved'].append(str(error))
        for path, period in PERIODS.items():
            planned = [action for action in actions if action['path'] == path]
            stats = {'planned': len(planned), 'attempted': 0, 'executed': 0, 'confirmed': 0, 'required_records': 0,
                     'missing_initial_ids': [], 'missing_later_ids': [], 'archive_missing_ids': [],
                     'live_changed_ids': [], 'archive_changed_ids': [], 'action_errors': [],
                     'http_errors': [], 'evidence': []}
            result['paths'][path] = stats
            if (len(planned) != math.ceil(contract['duration_seconds'] / period) or
                    [action['sequence'] for action in planned] != list(range(len(planned))) or
                    any(action['offset_seconds'] != action['sequence'] * period for action in planned)):
                raise RuntimeError('The producer schedule does not match the frozen frequencies')
            for action in planned:
                outcome = indexed.get(action['id'])
                if outcome is None:
                    result['unresolved'].append('No producer outcome: ' + action['id'])
                    continue
                if 'started' in outcome:
                    stats['attempted'] += 1
                if not outcome.get('executed') and not (path == 'appliance' and outcome.get('attempted')):
                    stats['action_errors'].append(action['id'])
                    result['violations'].append('Required action did not execute: ' + action['id'])
                    continue
                if path == 'appliance' and outcome.get('execution', {}).get('error'):
                    stats['http_errors'].append({'action_id': action['id'], **outcome['execution']})
                matched = required_records(action, outcome, indexed_sources, config)
                expected = 2 if path in ('appliance', 'health') else 1
                if len(matched) != expected:
                    stats['executed'] += bool(outcome.get('executed'))
                    stats['missing_initial_ids'].append(action['id'])
                    result['unresolved'].append('Required source-message set is missing or ambiguous: ' + action['id'])
                    continue
                stats['executed'] += 1
                stats['confirmed'] += 1
                stats['required_records'] += len(matched)
                for row in matched:
                    key = identity(row)
                    item = {'cursor': row['__CURSOR'], 'boot_id': row['_BOOT_ID'],
                            'source': {field: row.get(field) for field in SOURCE_FIELDS},
                            'first_confirmed': first_seen[key],
                            'journal_realtime_microseconds': row['__REALTIME_TIMESTAMP'],
                            'first_observed_delay_bound_seconds': (
                                first_seen[key]['monotonic_ns'] - outcome['started']['monotonic_ns']) / 1e9,
                            'message_sha256': prepare.digest(str(row['MESSAGE']).encode())}
                    if final is not None:
                        if key not in final:
                            stats['missing_later_ids'].append(action['id'])
                        elif final[key] != row:
                            stats['live_changed_ids'].append(action['id'])
                        item['age_at_final_read_seconds'] = (
                            state['final_query']['finished']['monotonic_ns'] - first_seen[key]['monotonic_ns']) / 1e9
                    if archive is not None:
                        if key not in archive:
                            stats['archive_missing_ids'].append(action['id'])
                        elif archive[key] != row:
                            stats['archive_changed_ids'].append(action['id'])
                    stats['evidence'].append({'action_id': action['id'], **item})
            for key in ('missing_later_ids', 'archive_missing_ids', 'live_changed_ids', 'archive_changed_ids'):
                if stats[key]:
                    result['violations'].append(path + ': ' + key + ': ' + ','.join(sorted(set(stats[key]))))
        if state.get('errors'):
            result['unresolved'].extend(state['errors'])
        if state['start_boot'] != state['end_boot'] or state['start_daemon'] != state['end_daemon']:
            result['violations'].append('Boot or journald identity changed during the basic check')
        elapsed = (state['ended']['monotonic_ns'] - contract['start']['monotonic_ns']) / 1e9
        utc_elapsed = (journal_coverage.timestamp(state['ended']['utc']) -
                       journal_coverage.timestamp(contract['start']['utc'])) / 1e6
        result.update(actual_elapsed_seconds=elapsed, utc_elapsed_seconds=utc_elapsed,
                      planned_seconds=contract['duration_seconds'])
        if elapsed < contract['duration_seconds'] or utc_elapsed < contract['duration_seconds']:
            result['unresolved'].append('The planned basic observation did not finish')
        delivery_ok = all(stats['confirmed'] == stats['planned'] for stats in result['paths'].values())
        result['delivery'] = ('Failed' if any(stats['action_errors'] for stats in result['paths'].values())
                              else 'Passed' if delivery_ok else 'Incomplete')
        result['later_live_read'] = ('Failed' if any(stats['missing_later_ids'] or stats['live_changed_ids']
                                                    for stats in result['paths'].values())
                                     else 'Passed' if delivery_ok and final is not None else 'Incomplete')
        result['collection'] = ('Failed' if archive_violation or any(stats['archive_missing_ids'] or stats['archive_changed_ids']
                                                for stats in result['paths'].values())
                                else 'Passed' if delivery_ok and archive is not None else 'Incomplete')
        result['overall'] = ('Failed' if result['violations'] else 'Incomplete' if result['unresolved'] else 'Passed')
        result['one_hour_basic_acceptance'] = (result['overall'] if contract['duration_seconds'] >= 3600 else 'Incomplete')
    except ConfirmedViolation as error:
        result['violations'].append(str(error))
        result['overall'] = 'Failed'
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        result['unresolved'].append(str(error))
    return result


def run_basic(config_path, duration):
    if duration < 1:
        raise RuntimeError('A positive basic-check duration is required')
    config = prepare.configuration(config_path)
    prepare.verify(PACKAGE)
    prepare.RUNTIME.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (prepare.RUNTIME / 'basic.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run_id = uuid.uuid4().hex
        directory = prepare.EVIDENCE / ('basic-' + run_id)
        directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        shutil.copytree(PACKAGE, directory / 'package')
        prepare.save(directory / 'package/config.json', config)
        for name in ('actions', 'direct', 'collector', 'readiness'):
            (directory / name).mkdir(mode=0o700)
        ready = preflight(config, directory / 'readiness')
        if not ready['ready']:
            prepare.save(directory / 'observation.json', {'state': 'Not ready', 'observed': clock()})
            prepare.save(directory / 'artifact-index.json', inventory(directory))
            result = replay(directory)
            prepare.save(directory / 'result.json', result)
            return directory, result
        boot = journal_coverage.BOOT.read_text().strip().replace('-', '')
        daemon = journal_coverage.daemon_identity()
        anchor = journal_coverage.query(['--system', '-b', boot, '--reverse', '--lines=1'],
                                        directory / 'initial-anchor.jsonl')
        if len(anchor) != 1:
            raise RuntimeError('A unique initial journal anchor is required')
        now = clock()
        began = {'utc': (datetime.datetime.fromisoformat(now['utc']) + datetime.timedelta(seconds=3)).isoformat(),
                 'monotonic_ns': now['monotonic_ns'] + 3000000000}
        actions = schedule(run_id, config, began, duration)
        with (directory / 'schedule.jsonl').open('w') as stream:
            stream.write(''.join(json.dumps(action, sort_keys=True) + '\n' for action in actions))
            stream.flush()
            os.fsync(stream.fileno())
        prepare.save(directory / 'contract.json', {'schema': 1, 'scope': 'basic-check', 'run_id': run_id,
                     'start': began, 'duration_seconds': duration, 'periods_seconds': PERIODS,
                     'direct_query_seconds': QUERY_PERIOD, 'collection_seconds': COLLECTION_PERIOD,
                     'visibility_wait_seconds': VISIBILITY_WAIT, 'appliance_logger': prepare.LOGGER,
                     'workers_by_path': WORKERS,
                     'appliance_execution_confirmation': 'A dispatched request and its unique actual source-message set; HTTP outcome is separate',
                     'appliance_parser_source_commit': prepare.APPLIANCE_SOURCE,
                     'appliance_required_messages': ['pvName is {pv}',
                                                    'requestTimesOb is RequestTimes[end={end}, start={start}, requestTimes=...]'],
                     'health_required_messages': {'terminal_patterns_by_exit_status': {
                         status: pattern.pattern for status, pattern in HEALTH_MESSAGES.items()},
                         'invocation_result': HEALTH_PREFIX + '{actual invocation and service outcome}'},
                     'schedule_sha256': prepare.digest((directory / 'schedule.jsonl').read_bytes())})
        reader = DirectReader(directory / 'direct', config, boot, anchor[0]['__CURSOR'])
        collector = Collector(directory / 'collector', began)
        threads = [threading.Thread(target=reader.run), threading.Thread(target=collector.run)]
        interrupted = threading.Event()
        old_handlers = {number: signal.signal(number, lambda *_: interrupted.set())
                        for number in (signal.SIGTERM, signal.SIGINT)}
        state = {'state': 'Running', 'start_boot': boot, 'start_daemon': daemon, 'errors': []}
        prepare.save(directory / 'observation.json', state)
        workers = {path: concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS[path]) for path in PERIODS}
        pending = {}
        for thread in threads:
            thread.start()
        try:
            for action in actions:
                while time.monotonic_ns() < action['planned_monotonic_ns']:
                    interrupted.wait(min(0.1, (action['planned_monotonic_ns'] - time.monotonic_ns()) / 1e9))
                    if interrupted.is_set():
                        raise InterruptedError('Basic check interrupted before all scheduled actions finished')
                path = action['path']
                for future in list(pending):
                    if future.done():
                        try:
                            append(directory / 'outcomes.jsonl', future.result())
                        except Exception as error:
                            state['errors'].append('Producer outcome: ' + str(error))
                        del pending[future]
                late = time.monotonic_ns() - action['planned_monotonic_ns']
                active = sum(item['path'] == path for item in pending.values())
                if active >= WORKERS[path] or late >= PERIODS[path] * 1000000000:
                    append(directory / 'outcomes.jsonl', {'id': action['id'], 'path': path,
                           'executed': False, 'skipped': True, 'reason': 'busy path or expired schedule slot',
                           'observed': clock()})
                else:
                    future = workers[path].submit(emit, action, config, directory / 'actions')
                    pending[future] = action
            end = began['monotonic_ns'] + duration * 1000000000
            while time.monotonic_ns() < end and not interrupted.is_set():
                interrupted.wait(0.1)
            if interrupted.is_set():
                raise InterruptedError('Basic check interrupted')
        except Exception as error:
            state['errors'].append(str(error))
        finally:
            for worker in workers.values():
                worker.shutdown(wait=True)
            for future in pending:
                try:
                    append(directory / 'outcomes.jsonl', future.result())
                except Exception as error:
                    state['errors'].append('Producer outcome: ' + str(error))
            interrupted.wait(VISIBILITY_WAIT)
            reader.stopping.set()
            threads[0].join()
            state['final_query'] = {'started': clock()}
            try:
                journal_coverage.query(['-b', boot, '--cursor', anchor[0]['__CURSOR'],
                                        'SYSLOG_IDENTIFIER=' + TAG, '+', '_TRANSPORT=kernel', '+',
                                        '_SYSTEMD_UNIT=' + config['appliance_unit'], '+',
                                        '_SYSTEMD_UNIT=' + HEALTH_UNIT], directory / 'final-live.jsonl')
            except Exception as error:
                state['errors'].append('Final live query: ' + str(error))
            state['final_query']['finished'] = clock()
            collector.stopping.set()
            threads[1].join()
            state['errors'].extend(error for error in (reader.error, collector.error) if error)
            state['ended'] = clock()
            state['end_boot'] = journal_coverage.BOOT.read_text().strip().replace('-', '')
            try:
                state['end_daemon'] = journal_coverage.daemon_identity()
            except Exception as error:
                state['end_daemon'] = None
                state['errors'].append(str(error))
            state['state'] = 'Finished'
            prepare.save(directory / 'observation.json', state)
            for number, handler in old_handlers.items():
                signal.signal(number, handler)
        prepare.save(directory / 'artifact-index.json', inventory(directory))
        result = replay(directory)
        prepare.save(directory / 'result.json', result)
        return directory, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('preflight')
    check.add_argument('--config', type=Path, default=PACKAGE / 'config.json')
    check.add_argument('--evidence', type=Path, required=True)
    run = commands.add_parser('run-basic')
    run.add_argument('--config', type=Path, default=PACKAGE / 'config.json')
    run.add_argument('--seconds', type=int, default=3600)
    repeat = commands.add_parser('replay')
    repeat.add_argument('evidence', type=Path)
    commands.add_parser('health-event')
    args = parser.parse_args()
    if args.command == 'health-event':
        health_event()
        return 0
    if args.command == 'preflight':
        args.evidence.mkdir(mode=0o700, parents=True, exist_ok=False)
        result = preflight(prepare.configuration(args.config), args.evidence)
        print(json.dumps(result, sort_keys=True))
        return 0 if result['ready'] else 1
    if args.command == 'replay':
        result = replay(args.evidence)
        print(json.dumps(result, sort_keys=True))
    else:
        directory, result = run_basic(args.config, args.seconds)
        print(json.dumps({'evidence': str(directory),
                          **{key: result[key] for key in ('scope', 'delivery', 'later_live_read',
                                                         'collection', 'overall', 'one_hour_basic_acceptance',
                                                         'full_day_acceptance')}}, sort_keys=True))
    return 0 if result['overall'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
