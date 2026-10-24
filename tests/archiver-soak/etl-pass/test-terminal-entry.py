#!/usr/bin/env python3
"""Rehearse interpreter observation with real retained readers and writer calls."""

import argparse
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time


SEMANTIC_FIELDS = ('verdict', 'failed_assertions', 'missing_coverage',
                   'scheduler_verdict', 'scheduler_failed_assertions', 'scheduler_missing_coverage')
CHILD_TIMEOUT = 180
SUITE_TIMEOUT = 1800
WRITER = '''import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import collect
collect.write_json(Path(sys.argv[4]), json.loads(Path(sys.argv[2]).read_text()))
collect.write_json(Path(sys.argv[4]), json.loads(Path(sys.argv[3]).read_text()))
'''


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            result.update(block)
    return result.hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def load(path):
    return json.loads(path.read_text())


def inventory(root):
    result = {}
    for path in [root, *sorted(root.rglob('*'))]:
        if path.is_symlink():
            raise RuntimeError('Symlink input is unsupported: ' + str(path))
        row = {'mode': path.stat().st_mode & 0o7777,
               'kind': 'directory' if path.is_dir() else 'file'}
        if path.is_file():
            row.update(bytes=path.stat().st_size, sha256=digest(path))
        result[str(path.relative_to(root))] = row
    return result


def semantic(value):
    return {**{key: value.get(key) for key in SEMANTIC_FIELDS},
            'jfr_recordings': {key: value.get('jfr_recordings', {}).get(key)
                               for key in ('verdict', 'failed_assertions', 'missing_coverage')}}


class Suite:
    def __init__(self, args):
        self.args = args
        self.began = time.monotonic()
        self.results = []
        self.observer = Path(__file__).with_name('trace-terminal-entry.py').resolve()
        self.originals = {'input': inventory(args.input), 'tools': inventory(args.tools),
                          'second_input_sha256': digest(args.second_input),
                          'observer_sha256': digest(self.observer), 'driver_sha256': digest(Path(__file__))}
        write(args.output / 'originals.json', self.originals)

    def copied(self, name):
        root = self.args.output / name
        root.mkdir()
        state, tools = root / 'state', root / 'tools'
        shutil.copytree(self.args.input, state, copy_function=shutil.copy2)
        shutil.copytree(self.args.tools, tools, copy_function=shutil.copy2)
        assert inventory(state) == self.originals['input']
        assert inventory(tools) == self.originals['tools']
        write(root / 'prelaunch-members.json', {'state': inventory(state), 'tools': inventory(tools)})
        terminal = [p for p in (state / 'abort.json', state / 'shutdown.json') if p.is_file()]
        if len(terminal) != 1:
            raise RuntimeError('Exactly one genuine retained terminal is required')
        return root, state, tools, terminal[0]

    def observed(self, tools, terminal, output, script=None, arguments=None, hold=None):
        script = script or tools / 'evaluate.py'
        command = [sys.executable, '-B', str(self.observer), '--script', str(script),
                   '--script-sha256', digest(script), '--tools', str(tools),
                   '--evaluate-sha256', digest(tools / 'evaluate.py'),
                   '--terminal', str(terminal), '--output', str(output)]
        control = None
        if hold:
            directory = Path(tempfile.mkdtemp(prefix='m35-entry-'))
            control = directory / 'control.sock'
            command += ['--hold', hold, '--control-socket', str(control), '--hold-seconds', '60']
        return command + ['--', *(arguments or ['--input', str(terminal.parent)])], control

    def run(self, name, command, hold=None, action=None):
        if time.monotonic() - self.began >= SUITE_TIMEOUT:
            raise RuntimeError('Declared 30-minute rehearsal bound reached')
        root = self.args.output / 'receipts' / name
        root.mkdir(parents=True)
        row = {'argv': command, 'cwd': str(Path.cwd()),
               'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'timeout_seconds': CHILD_TIMEOUT, 'native_returncode': None, 'error': None}
        began = time.monotonic()
        with (root / 'stdout').open('wb') as stdout, (root / 'stderr').open('wb') as stderr:
            child = subprocess.Popen(command, stdout=stdout, stderr=stderr, start_new_session=True)
            row['pid'] = child.pid
            row['start_ticks'] = Path('/proc/' + str(child.pid) + '/stat').read_text().rsplit(')', 1)[1].split()[19]
            write(root / 'receipt.json', row)
            try:
                if hold:
                    deadline = time.monotonic() + 60
                    connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    while True:
                        try:
                            connection.connect(str(hold))
                            break
                        except (FileNotFoundError, ConnectionRefusedError):
                            if child.poll() is not None or time.monotonic() >= deadline:
                                raise RuntimeError('Actual child did not expose its control socket')
                            time.sleep(0.02)
                    with connection:
                        connection.settimeout(60)
                        message = b''
                        while not message.endswith(b'\n'):
                            block = connection.recv(4096)
                            if not block:
                                raise RuntimeError('Control socket closed before observed hold')
                            message += block
                        row['hold'] = json.loads(message)
                        assert row['hold']['pid'] == child.pid
                        assert row['hold']['start_ticks'] == row['start_ticks']
                        if action == 'kill':
                            os.kill(child.pid, signal.SIGKILL)
                            row['signal_sent'] = signal.SIGKILL
                        else:
                            if callable(action):
                                action(row)
                            connection.sendall(b'release\n')
                row['native_returncode'] = child.wait(timeout=max(1, CHILD_TIMEOUT - (time.monotonic() - began)))
            except BaseException as error:
                row['error'] = {'type': type(error).__name__, 'message': str(error)}
                if child.poll() is None:
                    os.killpg(child.pid, signal.SIGKILL)
                    row['cleanup_signal_sent'] = signal.SIGKILL
                row['native_returncode'] = child.wait()
        row.update(ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   elapsed_seconds=time.monotonic() - began,
                   stdout_sha256=digest(root / 'stdout'), stderr_sha256=digest(root / 'stderr'))
        write(root / 'receipt.json', row)
        return row, root

    def result(self, name, assertions, incomplete=None):
        row = {'case': name, 'assertions': assertions, 'incomplete': incomplete,
               'verdict': 'Failed' if not all(assertions.values()) else 'Incomplete' if incomplete else 'Passed'}
        self.results.append(row)
        write(self.args.output / (name + '.result.json'), row)
        print(json.dumps(row), flush=True)

    def events(self, output):
        path = output / 'events.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []

    def execute(self):
        root, state, tools, terminal = self.copied('direct')
        direct, receipt = self.run('direct', [sys.executable, '-B', str(tools / 'evaluate.py'), '--input', str(state)])
        direct_value = load(receipt / 'stdout')
        root, state, tools, terminal = self.copied('observed')
        output = root / 'observer'
        command, _ = self.observed(tools, terminal, output)
        observed, receipt = self.run('observed', command)
        events = self.events(output)
        calls = [x for x in events if x['kind'] == 'call' and x['function'] == 'evaluate']
        returns = [x for x in events if x['kind'] == 'return' and x['function'] == 'evaluate']
        self.result('L01', {'native_agrees': observed['native_returncode'] == direct['native_returncode'],
                    'semantics_agree': semantic(load(receipt / 'stdout')) == semantic(direct_value),
                    'actual_call_and_normal_return': len(calls) == len(returns) == 1 and returns[0]['completed_dict_return'],
                    'copies_unchanged': inventory(state) == self.originals['input'] and inventory(tools) == self.originals['tools']})
        self.result('L02', {'disk_argument_identity': len(calls) == 1 and calls[0]['argument_equals_terminal'],
                    'saved_disk_bytes': (output / calls[0]['terminal_file']).read_bytes() == terminal.read_bytes(),
                    'activation_recorded': events[0]['kind'] == 'observer-active',
                    'exact_code_location': calls[0]['firstlineno'] == load(output / 'command.json')['selected_firstlineno']['evaluate']})
        rejected = root / 'wrong-source'
        command, _ = self.observed(tools, terminal, rejected)
        command[command.index('--script-sha256') + 1] = '0' * 64
        native, _ = self.run('wrong-source', command)
        checks = {'source_refused': native['native_returncode'] == 2, 'no_output': not rejected.exists()}
        script = root / 'duplicate-entry.py'
        script.write_text('import json, sys\nfrom pathlib import Path\n'
                          'sys.path.insert(0, sys.argv[1])\nimport evaluate\n'
                          'state = Path(sys.argv[2])\nterminal = json.loads(Path(sys.argv[3]).read_text())\n'
                          'evaluate.evaluate(state, terminal)\nevaluate.evaluate(state, terminal)\n')
        duplicate_output = root / 'duplicate-entry'
        command, _ = self.observed(tools, terminal, duplicate_output, script,
                                  [str(tools), str(state), str(terminal)])
        duplicate, _ = self.run('duplicate-entry', command)
        checks['duplicate_entry_refused'] = duplicate['native_returncode'] == 125 and any(
            row['kind'] == 'observer-error' and row.get('message') == 'Duplicate selected evaluator entry'
            for row in self.events(duplicate_output))
        checks['copies_unchanged'] = inventory(state) == self.originals['input'] and inventory(tools) == self.originals['tools']
        self.result('L03', checks)
        checks = {}
        for name, target in (('occupied', output), ('overlap', state / 'observer')):
            command, _ = self.observed(tools, terminal, target)
            native, _ = self.run(name, command)
            checks[name + '_refused'] = native['native_returncode'] == 2
        checks['input_unchanged'] = inventory(state) == self.originals['input']
        self.result('L04', checks)
        for label, boundary, action in (('L05', 'entry', None), ('L06', 'nested', 'kill'), ('L07', 'entry', 'dependency')):
            root, state, tools, terminal = self.copied(label)
            output = root / 'observer'
            command, control = self.observed(tools, terminal, output, hold=boundary)
            moved = []
            def dependency(row):
                current = self.events(output)
                assert not next(x for x in current if x['kind'] == 'call')['aggregate_preloaded']
                backup = root / 'dependency-backup'
                backup.mkdir()
                for source in [tools / 'aggregate.py', *tools.glob('aggregate.pyc'), *tools.glob('__pycache__/aggregate*.pyc')]:
                    destination = backup / source.relative_to(tools)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
                    assert digest(source) == digest(destination)
                    source.rename(source.with_name(source.name + '.fault-unavailable'))
                    moved.append(source)
                row['unavailable_files'] = [str(p) for p in moved]
            native, receipt = self.run(label, command, hold=control,
                                       action=dependency if action == 'dependency' else action)
            for path in moved:
                path.with_name(path.name + '.fault-unavailable').rename(path)
            events = self.events(output)
            top_returns = [x for x in events if x['kind'] == 'return' and x['function'] == 'evaluate']
            checks = {'actual_hold': native.get('hold', {}).get('boundary') == boundary,
                      'input_unchanged': inventory(state) == self.originals['input'],
                      'tools_restored': inventory(tools) == self.originals['tools']}
            if native['error']:
                self.result(label, {key: checks[key] for key in ('input_unchanged', 'tools_restored')},
                            native['error'])
                continue
            if label == 'L05':
                checks.update(actual_return=any(x['completed_dict_return'] for x in top_returns),
                              native_agrees=native['native_returncode'] == direct['native_returncode'],
                              semantics_agree=semantic(load(receipt / 'stdout')) == semantic(direct_value))
            elif label == 'L06':
                checks.update(actual_sigkill=native['native_returncode'] == -signal.SIGKILL,
                              no_completed_return=not any(x['completed_dict_return'] for x in top_returns),
                              first_file_readable=isinstance(load(terminal), dict))
            else:
                checks.update(actual_import_exception=any(x['kind'] == 'exception' and x.get('type') == 'ModuleNotFoundError' for x in events),
                              unwind_not_completed=bool(top_returns) and all(x['exception_unwind'] and not x['completed_dict_return'] for x in top_returns),
                              native_nonzero=native['native_returncode'] != 0)
            self.result(label, checks, native['error'])
        checks = {}
        root, state, tools, terminal = self.copied('native-status')
        for name, code, expected in (('zero', 'raise SystemExit(0)', 0), ('one', 'raise SystemExit(1)', 1),
                                     ('term', 'import os, signal; os.kill(os.getpid(), signal.SIGTERM)', -signal.SIGTERM)):
            script = root / (name + '.py')
            script.write_text(code + '\n')
            command, _ = self.observed(tools, terminal, root / name, script, [])
            native, _ = self.run(name, command)
            checks[name] = native['native_returncode'] == expected
        self.result('L08', checks)
        for label, mode in (('L09', 'observe'), ('L10', 'eio-first'), ('L11', 'eio-final'), ('L12', 'kill-after-first')):
            root, state, tools, retained = self.copied(label)
            savedir = root / 'save'
            savedir.mkdir()
            terminal = savedir / 'terminal.json'
            script = root / 'writer.py'
            script.write_text(WRITER)
            command, _ = self.observed(tools, terminal, root / 'observer', script,
                                       [str(tools), str(retained), str(self.args.second_input), str(terminal)])
            argv = [sys.executable, '-B', str(tools / 'terminal-boundary.py'), '--terminal', str(terminal),
                    '--output', str(root / 'trace'), '--mode', mode, '--timeout-seconds', '60', '--', *command]
            native, _ = self.run(label, argv)
            summary = load(root / 'trace/summary.json') if (root / 'trace/summary.json').is_file() else {}
            unavailable = native['error'] or summary.get('error') or (None if summary else 'Missing supervisor summary')
            if unavailable:
                self.result(label, {'input_unchanged': inventory(state) == self.originals['input'],
                                    'tools_unchanged': inventory(tools) == self.originals['tools']}, unavailable)
                continue
            first = (json.dumps(load(retained), indent=2) + '\n').encode()
            second = (json.dumps(load(self.args.second_input), indent=2) + '\n').encode()
            expected_native = 0 if mode == 'observe' else -9 if mode == 'kill-after-first' else 1
            checks = {'helper_coverage': native['native_returncode'] == 0 and summary.get('coverage_verdict') == 'Passed',
                      'real_child_native': summary.get('native_returncode') == expected_native,
                      'no_unreaped': summary.get('unreaped_pids') == [],
                      'distinct_retained_payloads': first != second,
                      'actual_file': not terminal.exists() if mode == 'eio-first' else terminal.read_bytes() == (second if mode == 'observe' else first),
                      'no_evaluator_substitute': not any(x['kind'] == 'call' for x in self.events(root / 'observer'))}
            if mode in ('eio-first', 'eio-final'):
                checks['retained_temporary'] = terminal.with_suffix('.json.tmp').read_bytes() == (first if mode == 'eio-first' else second) if terminal.with_suffix('.json.tmp').exists() else False
            self.result(label, checks)

    def finish(self, error=None):
        unchanged = (inventory(self.args.input) == self.originals['input'] and
                     inventory(self.args.tools) == self.originals['tools'] and
                     digest(self.args.second_input) == self.originals['second_input_sha256'])
        counts = dict(collections.Counter(row['verdict'] for row in self.results))
        complete = len(self.results) == 12 and not error
        verdict = 'Failed' if not unchanged or counts.get('Failed') else 'Incomplete' if not complete or counts.get('Incomplete') else 'Passed'
        summary = {'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'elapsed_seconds': time.monotonic() - self.began, 'declared_cases': 12,
                   'counts': counts, 'results': self.results, 'error': error,
                   'originals_unchanged': unchanged, 'verdict': verdict,
                   'claim': 'Actual reader/observer and writer mechanics only; no live lifecycle acceptance'}
        write(self.args.output / 'summary.json', summary)
        print(json.dumps({key: value for key, value in summary.items() if key != 'results'}))
        return 0 if verdict == 'Passed' else 1 if verdict == 'Failed' else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('input', 'second-input', 'tools', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    if os.path.lexists(args.output) or args.output.absolute() != args.output.resolve():
        parser.error('Output must be absent without symlink or ambiguous components')
    for name in ('input', 'second_input', 'tools', 'output'):
        setattr(args, name, getattr(args, name).resolve())
    if not args.input.is_dir() or not args.tools.is_dir() or not args.second_input.is_file():
        parser.error('Actual retained input/tools and a second terminal record are required')
    if any(args.output == p or args.output in p.parents or p in args.output.parents
           for p in (args.input, args.tools, args.second_input.parent)):
        parser.error('Output must not overlap retained inputs/tools')
    os.umask(0o077)
    args.output.mkdir(parents=True)
    suite = Suite(args)
    error = None
    try:
        suite.execute()
    except BaseException as failure:
        error = {'type': type(failure).__name__, 'message': str(failure)}
    return suite.finish(error)


if __name__ == '__main__':
    raise SystemExit(main())
