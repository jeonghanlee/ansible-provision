#!/usr/bin/env python3
"""Observe real evaluator calls while executing an unchanged Python CLI."""

import argparse
import ast
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import runpy
import socket
import sys
import time


FUNCTIONS = ('evaluate', '_evaluate_observation')
MAXIMUM_HOLD_SECONDS = 60


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def write(path, value):
    with path.open('w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def overlaps(left, right):
    return left == right or left in right.parents or right in left.parents


class Observer:
    def __init__(self, args):
        self.args = args
        self.began = time.monotonic()
        self.sequence = 0
        self.frames = {}
        self.calls = {name: 0 for name in FUNCTIONS}
        parsed = ast.parse((args.tools / 'evaluate.py').read_text())
        selected = [node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name in FUNCTIONS]
        if len(selected) != len(FUNCTIONS) or {node.name for node in selected} != set(FUNCTIONS):
            raise RuntimeError('Selected evaluator definitions are not unique')
        self.lines = {node.name: min([node.lineno] + [item.lineno for item in node.decorator_list])
                      for node in selected}
        self.held = False
        self.listener = None
        self.events = (args.output / 'events.jsonl').open('x', buffering=1)
        self.receipt = {
            'argv': sys.argv, 'script_argv': [str(args.script), *args.arguments],
            'cwd': os.getcwd(), 'started_at': now(), 'pid': os.getpid(),
            'start_ticks': Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
            'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
            'python': sys.version, 'script_sha256': digest(args.script),
            'evaluate_sha256': digest(args.tools / 'evaluate.py'),
            'observer_sha256': digest(Path(__file__).resolve()),
            'selected_firstlineno': self.lines,
            'native_returncode': None, 'error': None,
            'claim': 'Interpreter observation; fault and lifecycle claims require independent receipts'}
        self.save()
        if args.hold:
            self.listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.listener.bind(str(args.control_socket))
            os.chmod(args.control_socket, 0o600)
            self.listener.listen(1)
            self.listener.settimeout(args.hold_seconds)
        self.event('observer-active', process={key: self.receipt[key]
                   for key in ('pid', 'start_ticks', 'boot_id')})

    def save(self):
        write(self.args.output / 'command.json', self.receipt)

    def event(self, kind, **values):
        self.sequence += 1
        row = {'kind': kind, 'sequence': self.sequence, 'at': now(),
               'elapsed_seconds': time.monotonic() - self.began, **values}
        self.events.write(json.dumps(row, sort_keys=True) + '\n')
        self.events.flush()
        return row

    def snapshot(self, frame):
        prefix = 'entry-' + str(self.sequence + 1)
        argument = frame.f_locals.get('terminal')
        argument_path = self.args.output / (prefix + '.argument.json')
        write(argument_path, argument)
        row = {'argument_file': argument_path.name, 'argument_sha256': digest(argument_path),
               'terminal_path': str(self.args.terminal), 'terminal_exists': self.args.terminal.exists(),
               'aggregate_preloaded': 'aggregate' in sys.modules}
        if row['terminal_exists']:
            content = self.args.terminal.read_bytes()
            saved = self.args.output / (prefix + '.terminal.json')
            saved.write_bytes(content)
            row.update(terminal_file=saved.name, terminal_sha256=digest(saved),
                       argument_equals_terminal=json.loads(content) == argument)
        return row

    def hold(self, boundary):
        if self.args.hold != boundary or self.held:
            return
        self.held = True
        deadline = time.monotonic() + self.args.hold_seconds
        row = self.event('hold', boundary=boundary, pid=os.getpid(),
                         start_ticks=self.receipt['start_ticks'])
        connection, _ = self.listener.accept()
        with connection:
            connection.settimeout(max(0.001, deadline - time.monotonic()))
            connection.sendall((json.dumps(row) + '\n').encode())
            incoming = b''
            while not incoming.endswith(b'\n') and len(incoming) <= 1024:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('Evaluator hold deadline expired')
                connection.settimeout(remaining)
                block = connection.recv(1024)
                if not block:
                    break
                incoming += block
            if incoming != b'release\n':
                raise RuntimeError('Expected exact release acknowledgement')
        self.event('released', boundary=boundary)

    def trace(self, frame, kind, value):
        if (Path(frame.f_code.co_filename).resolve() != self.args.tools / 'evaluate.py' or
                frame.f_code.co_name not in FUNCTIONS):
            return None
        try:
            function = frame.f_code.co_name
            if kind == 'call':
                if frame.f_code.co_firstlineno != self.lines[function]:
                    raise RuntimeError('Selected evaluator code location differs')
                self.calls[function] += 1
                if self.calls[function] != 1:
                    raise RuntimeError('Duplicate selected evaluator entry')
                frame.f_trace_lines = False
                self.frames[id(frame)] = {'exceptions': 0}
                self.event('call', function=function, filename=frame.f_code.co_filename,
                           firstlineno=frame.f_code.co_firstlineno,
                           caller={'file': frame.f_back.f_code.co_filename,
                                   'function': frame.f_back.f_code.co_name},
                           **self.snapshot(frame))
                self.hold('entry' if function == 'evaluate' else 'nested')
            elif kind == 'exception':
                self.frames[id(frame)]['exceptions'] += 1
                self.event('exception', function=function, type=value[0].__name__, message=str(value[1]))
            elif kind == 'return':
                state = self.frames.pop(id(frame))
                completed = isinstance(value, dict) and 'verdict' in value
                record = {'function': function, 'completed_dict_return': completed,
                          'exception_events': state['exceptions'],
                          'exception_unwind': value is None and state['exceptions'] > 0,
                          'aggregate_file': getattr(sys.modules.get('aggregate'), '__file__', None)}
                if completed:
                    path = self.args.output / ('return-' + str(self.sequence + 1) + '.json')
                    write(path, value)
                    record.update(result_file=path.name, result_sha256=digest(path))
                self.event('return', **record)
                if function == 'evaluate' and completed:
                    self.hold('return')
            return self.trace
        except BaseException as error:
            self.receipt['error'] = {'type': type(error).__name__, 'message': str(error)}
            self.receipt['native_returncode'] = 125
            self.receipt['ended_at'] = now()
            self.save()
            self.event('observer-error', **self.receipt['error'])
            os._exit(125)

    def run(self):
        native = 0
        sys.argv = [str(self.args.script), *self.args.arguments]
        sys.path[0:1] = [str(self.args.script.parent)]
        self.receipt['script_sys_path'] = list(sys.path)
        self.save()
        try:
            sys.settrace(self.trace)
            runpy.run_path(str(self.args.script), run_name='__main__')
        except SystemExit as error:
            native = int(error.code) if isinstance(error.code, int) else 0 if error.code is None else 1
            raise
        except BaseException:
            native = 1
            raise
        finally:
            sys.settrace(None)
            self.receipt.update(native_returncode=native, ended_at=now(),
                                elapsed_seconds=time.monotonic() - self.began,
                                hold_reached=self.held)
            self.save()
            self.event('observer-ended', native_returncode=native)
            self.events.close()
            if self.listener is not None:
                self.listener.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path, required=True)
    parser.add_argument('--script-sha256', required=True)
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--evaluate-sha256', required=True)
    parser.add_argument('--terminal', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--hold', choices=('entry', 'nested', 'return'))
    parser.add_argument('--control-socket', type=Path)
    parser.add_argument('--hold-seconds', type=float, default=MAXIMUM_HOLD_SECONDS)
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.arguments[:1] == ['--']:
        args.arguments = args.arguments[1:]
    if (sys.implementation.name != 'cpython' or sys.platform != 'linux' or
            sys.version_info < (3, 9) or not math.isfinite(args.hold_seconds) or
            not 0 < args.hold_seconds <= MAXIMUM_HOLD_SECONDS):
        parser.error('Linux CPython 3.9+ and a finite hold of at most 60 seconds are required')
    if os.path.lexists(args.output) or args.output.absolute() != args.output.resolve():
        parser.error('Output must be absent with no symlink or ambiguous components')
    for name in ('script', 'tools', 'terminal', 'output'):
        setattr(args, name, getattr(args, name).resolve())
    if (not args.script.is_file() or not (args.tools / 'evaluate.py').is_file() or
            digest(args.script) != args.script_sha256 or
            digest(args.tools / 'evaluate.py') != args.evaluate_sha256):
        parser.error('Script and evaluator must match their explicit source hashes')
    if (overlaps(args.output, args.tools) or overlaps(args.output, args.terminal.parent) or
            overlaps(args.output, args.script)):
        parser.error('Output must be disjoint from tools, script and terminal input directory')
    if bool(args.hold) != bool(args.control_socket):
        parser.error('A hold requires an explicit absent control socket and vice versa')
    if args.hold:
        path = args.control_socket
        if (os.path.lexists(path) or path.absolute() != path.resolve() or
                not path.parent.is_dir() or len(os.fsencode(path)) >= 108 or
                overlaps(path, args.tools) or overlaps(path, args.terminal.parent)):
            parser.error('Control socket must be absent, short, and disjoint from input/tools')
    os.umask(0o077)
    args.output.mkdir(parents=True)
    try:
        observer = Observer(args)
    except BaseException as error:
        write(args.output / 'tool-error.json', {'at': now(), 'type': type(error).__name__,
                                              'message': str(error), 'native_returncode': 125})
        raise SystemExit(125)
    observer.run()


if __name__ == '__main__':
    main()
