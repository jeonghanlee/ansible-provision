"""Detect a real collector-only filesystem failure and retain one terminal stop."""

import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import threading
import uuid

import basic
import boot_coverage
import journal_coverage as native
import prepare
import window_coverage as window

DURATION = 900
COMMAND_TIMEOUT = 180
STOP_TIMEOUT = 300
IDENTITY_FIELDS = ('MainPID', 'InvocationID', 'ExecMainStartTimestampMonotonic')


def load(path):
    return json.loads(path.read_text())


def same_source(first, second):
    return (first['ActiveState'] == second['ActiveState'] == 'active'
            and first['MainPID'] != '0'
            and all(first[key] == second[key] for key in IDENTITY_FIELDS))


def declare(directory, config, start):
    prepare.save(directory / 'failure-contract.json', {
        'scope': 'collector-filesystem-failure-termination', 'start': start,
        'positive_observation_seconds': DURATION,
        'first_collection_seconds': basic.COLLECTION_PERIOD,
        'failed_collection_seconds': 2 * basic.COLLECTION_PERIOD,
        'denied_output': str(directory / 'collector/interval-1'),
        'read_only_parent': str(directory / 'collector'),
        'fault_boundary': 'ReadOnlyPaths in the actual collector CLI service only',
        'terminal_target': config['appliance_unit'], 'stop_timeout_seconds': STOP_TIMEOUT,
        'repeat_behavior': 'refuse-without-any-write-or-second-stop',
        'positive_retention_acceptance_expected': False})


class Collector:
    """Run the shipped interval CLI in real transient collector services."""

    def __init__(self, directory, anchor, context):
        self.root, self.anchor, self.context = directory, anchor, context
        self.stopping = threading.Event()
        self.error = None
        self.previous, self.number = {}, 0
        (directory / 'collector-attempts').mkdir(mode=0o700)

    def invoke(self, name, readonly):
        attempt = self.root / 'collector-attempts' / name
        attempt.mkdir(mode=0o700)
        prepare.save(attempt / 'input-state.json', self.previous)
        output = self.root / 'collector' / ('interval-' + str(self.number))
        unit = 'journal-validation-interval-' + uuid.uuid4().hex + '.service'
        command = ['systemd-run', '--quiet', '--wait', '--pipe', '--unit', unit,
                   '--property=TimeoutStartSec=180s', '--property=TimeoutStopSec=30s']
        if readonly:
            command += ['--property=ReadOnlyPaths=' + str(output.parent)]
        command += ['/usr/bin/python3', '-B', str(self.root / 'package/interval.py'),
                    '--output', str(output), '--input', str(attempt / 'input-state.json'),
                    '--window', str(self.root / 'restart-window.json'),
                    '--context', str(self.root / 'restart-input.json'), '--attempt', str(attempt)]
        prepare.save(attempt / 'declared-command.json', {'command': command, 'readonly': readonly,
                     'output': str(output), 'observed': basic.clock()})
        receipt = basic.command(command, attempt / 'command', timeout=COMMAND_TIMEOUT)
        properties = basic.service(unit, attempt / 'unit')
        prepare.save(attempt / 'service.json', properties)
        if receipt.get('returncode') != 0:
            config = load(self.root / 'package/config.json')
            health = {'appliance': basic.service(config['appliance_unit'], attempt / 'after-appliance'),
                      'ioc': basic.service('journal-validation-ioc.service', attempt / 'after-ioc'),
                      'journald': native.daemon_identity(), 'observed': basic.clock()}
            prepare.save(attempt / 'sources-after-failure.json', health)
            with (output.parent / ('host-write-proof-' + uuid.uuid4().hex)).open('x') as stream:
                stream.write('Collector namespace restriction did not deny the host writer.\n')
            self.error = 'Actual collector CLI returned ' + str(receipt.get('returncode'))
            prepare.save(self.root / 'collector/error.json', {'observed': basic.clock(), 'error': self.error,
                         'actual_attempt': str(attempt), 'command_sha256': window.digest(attempt / 'command.json')})
            return False
        result = load(output / 'result.json')
        boot_coverage.verify(output, load(output / 'journal-coverage.json'))
        self.previous = {'system_journal_checkpoint': result['checkpoint']}
        self.number += 1
        return True

    def run(self):
        try:
            if self.stopping.wait(basic.COLLECTION_PERIOD):
                raise RuntimeError('The first required collector boundary was interrupted')
            if not self.invoke('first-success', False):
                return
            if self.stopping.wait(basic.COLLECTION_PERIOD):
                raise RuntimeError('The predeclared failed collector boundary was interrupted')
            if self.invoke('actual-denial', True):
                raise RuntimeError('The real filesystem boundary unexpectedly permitted collection')
        except Exception as error:
            self.error = str(error)
            prepare.save(self.root / 'collector/error.json', {'observed': basic.clock(), 'error': self.error})

    def recover(self):
        original = self.error
        if not self.invoke('restored-final', False):
            raise RuntimeError('The ordinary collector did not recover after its private fault ended')
        self.error = original
        prepare.save(self.root / 'filesystem-restored.json', {'observed': basic.clock(),
                     'original_failure_retained': True, 'complete_recovery_interval': self.number - 1,
                     'source_checkpoint_retained': True})


def finish(directory):
    directory = directory.resolve()
    if directory.parent != prepare.EVIDENCE or not directory.name.startswith('long-'):
        raise RuntimeError('The terminal target is outside dedicated journal evidence')
    guard = prepare.RUNTIME / (directory.name + '-terminal.lock')
    with guard.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        terminal = directory / 'terminal'
        if terminal.exists():
            return {'accepted': False, 'reason': 'Terminal operation already claimed', 'stop_dispatched': False}
        contract = load(directory / 'failure-contract.json')
        if not (directory / 'failure-detected.json').is_file():
            raise RuntimeError('No actual collector failure was detected for termination')
        terminal.mkdir(mode=0o700)
        before = basic.service(contract['terminal_target'], terminal / 'before')
        if before['MainPID'] == '0' or before['ActiveState'] != 'active':
            raise RuntimeError('The declared terminal target was not active')
        prepare.save(terminal / 'claim.json', {'observed': basic.clock(), 'target': contract['terminal_target'],
                     'before': before, 'maximum_stop_dispatches': 1})
        receipt = basic.command(['systemctl', 'stop', contract['terminal_target']], terminal / 'stop',
                                timeout=contract['stop_timeout_seconds'])
        after = basic.service(contract['terminal_target'], terminal / 'after')
        prepare.save(terminal / 'result.json', {'observed': basic.clock(), 'target': contract['terminal_target'],
                     'stop_dispatches': 1, 'returncode': receipt.get('returncode'), 'before': before, 'after': after})
        return {'accepted': True, 'stop_dispatched': True, 'returncode': receipt.get('returncode')}


def replay(directory):
    import long
    result = {'scope': 'collector-filesystem-failure-termination', 'expectation': 'Incomplete',
              'positive_observation_acceptance': False, 'unresolved': []}
    try:
        if long.inventory(directory) != load(directory / 'artifact-index.json'):
            raise RuntimeError('Original failed observation evidence changed')
        prepare.verify(directory / 'package')
        if window.digest(Path(__file__)) != window.digest(directory / 'package/failure.py'):
            raise RuntimeError('Failure replay requires the actual frozen lifecycle code')
        contract = load(directory / 'failure-contract.json')
        standard = load(directory / 'contract.json')
        if (standard['scenario'] != 'failure-termination' or standard['duration_seconds'] != DURATION
                or standard['periods_seconds'] != basic.PERIODS
                or contract['denied_output'] != str(directory / 'collector/interval-1')
                or contract['read_only_parent'] != str(directory / 'collector')
                or contract['failed_collection_seconds'] != 600):
            raise RuntimeError('The predeclared fault or actual signal schedule changed')
        first = directory / 'collector-attempts/first-success'
        failed = directory / 'collector-attempts/actual-denial'
        recovery = directory / 'collector-attempts/restored-final'
        first_receipt, failed_receipt = load(first / 'command.json'), load(failed / 'command.json')
        entered = load(failed / 'cli-entered.json')
        declared = load(failed / 'declared-command.json')
        original_source = load(first / 'cli-entered.json')
        after_source = load(failed / 'sources-after-failure.json')
        if (first_receipt.get('returncode') != 0 or failed_receipt.get('returncode') in (None, 0)
                or not declared['readonly'] or '--property=ReadOnlyPaths=' + contract['read_only_parent'] not in declared['command']
                or entered['output'] != contract['denied_output']
                or entered['mount_namespace'] == entered['host_mount_namespace']
                or 'Read-only file system' not in (failed / 'command.stderr').read_text()
                or not any(line.split()[4] == contract['read_only_parent'] and 'ro' in line.split()[5].split(',')
                           for line in entered['mountinfo'].splitlines())
                or not all(same_source(original_source[key], entered[key]) and same_source(entered[key], after_source[key])
                           for key in ('appliance', 'ioc'))):
            raise RuntimeError('The actual failed CLI does not prove a collector-only filesystem denial')
        original_input = load(failed / 'input-state.json')
        if (original_input != {'system_journal_checkpoint': load(directory / 'collector/interval-0/result.json')['checkpoint']}
                or original_input != load(recovery / 'input-state.json')
                or load(recovery / 'command.json').get('returncode') != 0):
            raise RuntimeError('The real failed checkpoint was reset or ordinary collection did not recover')
        for interval in sorted((directory / 'collector').glob('interval-*')):
            boot_coverage.verify(interval, load(interval / 'journal-coverage.json'))
        detected = load(directory / 'failure-detected.json')
        if not 0 <= detected['observed']['monotonic_ns'] - failed_receipt['finished']['monotonic_ns'] < 2_000_000_000:
            raise RuntimeError('The lifecycle driver did not detect the actual CLI failure promptly')
        schedule = list(long.rows(directory / 'schedule.jsonl'))
        outcomes = list(long.rows(directory / 'outcomes.jsonl'))
        mapped = {row['id']: row for row in outcomes}
        if len(mapped) != len(outcomes) or set(mapped) != {row['id'] for row in schedule}:
            raise RuntimeError('Not every scheduled action has an independent executed or cancelled outcome')
        cancelled = [row for row in outcomes if row.get('cancelled')]
        if not cancelled or any(row.get('executed') or row.get('reason') != 'Actual collector CLI failure'
                                or row['observed'] != detected['observed'] for row in cancelled):
            raise RuntimeError('Unexecuted scheduled actions were not explicitly reconciled')
        executed = [row for row in outcomes if not row.get('cancelled')]
        if any(not row.get('executed') for row in executed):
            raise RuntimeError('An unrelated producer failure occurred before termination')
        verified_actions = {row['action_id'] for row in long.rows(directory / 'comparisons.jsonl')}
        if not {row['id'] for row in executed}.issubset(verified_actions):
            raise RuntimeError('Actual executed inputs lack independent direct source confirmation')
        queries = list(long.rows(directory / 'direct/queries.jsonl'))
        for entry in queries:
            long.checked_query(directory / 'direct' / entry['file'])
        if not any(entry['finished']['monotonic_ns'] > failed_receipt['finished']['monotonic_ns'] for entry in queries):
            raise RuntimeError('The independent direct reader was not healthy after the failed CLI')
        terminal = load(directory / 'terminal/result.json')
        stop = load(directory / 'terminal/stop.json')
        if (terminal['stop_dispatches'] != 1 or terminal['returncode'] != 0
                or terminal['after']['MainPID'] != '0' or terminal['after']['ActiveState'] != 'inactive'
                or stop['command'] != ['systemctl', 'stop', contract['terminal_target']]
                or stop['finished']['monotonic_ns'] - stop['started']['monotonic_ns'] > STOP_TIMEOUT * 1_000_000_000
                or len(list((directory / 'terminal').glob('stop.json'))) != 1):
            raise RuntimeError('The bounded terminal operation did not stop the actual target exactly once')
        original = load(directory / 'result.json')
        repeated = long.replay(directory)
        if repeated != original or original['overall'] not in ('Failed', 'Incomplete'):
            raise RuntimeError('The failed original observation verdict was changed or cannot be reproduced')
        if any('Missing or changed required record in' in message for message in original['violations']):
            raise RuntimeError('An executed required record was lost independently of cancelled future actions')
        result.update(expectation='Passed', original_observation=original['overall'],
                      original_result_sha256=window.digest(directory / 'result.json'),
                      actual_executed_actions=len(executed), explicitly_cancelled_actions=len(cancelled),
                      actual_failed_cli_returncode=failed_receipt['returncode'], stop_dispatches=1,
                      failed_checkpoint_retained=True, filesystem_access_restored=True,
                      independent_direct_reader_healthy=True, source_identities_unchanged=True)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        result['unresolved'].append(str(error))
    return result


def main():
    import long
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('run', 'finish', 'replay'))
    parser.add_argument('directory', type=Path, nargs='?')
    args = parser.parse_args()
    if args.action == 'run':
        boots = subprocess.check_output(['journalctl', '--list-boots', '--no-pager'], text=True)
        allowed = [line.split()[1] for line in boots.splitlines()]
        directory, original = long.run(prepare.PREFIX / 'config.json', DURATION, 'failure-termination',
                                      restart_input={'phase': 'before', 'journal_boots': allowed})
        result = load(directory / 'failure-result.json')
    elif args.action == 'finish':
        result = finish(args.directory)
        print(json.dumps(result, sort_keys=True))
        return 0 if result['accepted'] else 2
    else:
        result = replay(args.directory)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['expectation'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
