#!/usr/bin/env python3
"""Observe exact terminal replacements and retain external syscall fault evidence."""

import argparse
import ctypes
import datetime
import errno
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import signal
import struct
import sys
import time


TRACEME, PEEKDATA, GETREGS, SETREGS, SYSCALL = 0, 2, 12, 13, 24
SETOPTIONS, GETEVENTMSG = 0x4200, 0x4201
FORK, VFORK, CLONE, EXEC = 1, 2, 3, 4
OPTIONS = 1 | (1 << FORK) | (1 << VFORK) | (1 << CLONE) | (1 << EXEC) | (1 << 20)
WALL = 0x40000000
MASK = (1 << 64) - 1
AT_FDCWD = -100
RENAME, RENAMEAT, RENAMEAT2 = 82, 264, 316
EXECVE, EXECVEAT = 59, 322
RT_SIGRETURN = 15
MAX_STRING_BYTES = 131072
MAX_ARGUMENTS = 4096
REGISTER_NAMES = ('r15 r14 r13 r12 rbp rbx r11 r10 r9 r8 rax rcx rdx rsi rdi '
                  'orig_rax rip cs eflags rsp ss fs_base gs_base ds es fs gs').split()


class Registers(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in REGISTER_NAMES]


LIBC = ctypes.CDLL(None, use_errno=True) if sys.platform == 'linux' else None
if LIBC is not None:
    LIBC.ptrace.restype = ctypes.c_long
    LIBC.ptrace.argtypes = (ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def ptrace(operation, pid, address=0, data=0):
    ctypes.set_errno(0)
    result = LIBC.ptrace(operation, pid, address, data)
    error = ctypes.get_errno()
    if result == -1 and error:
        failure = OSError(error, 'ptrace operation ' + str(operation) + ': ' + os.strerror(error))
        failure.ptrace_operation = operation
        failure.ptrace_pid = pid
        raise failure
    return result


def registers(pid):
    value = Registers()
    ptrace(GETREGS, pid, data=ctypes.byref(value))
    if value.cs != 0x33:
        raise RuntimeError('Only the native Linux x86_64 syscall ABI is supported')
    return value


def signed(value):
    return ctypes.c_longlong(value).value


def string(pid, address):
    result = bytearray()
    for offset in range(0, MAX_STRING_BYTES, 8):
        block = struct.pack('<Q', ptrace(PEEKDATA, pid, address + offset) & MASK)
        result.extend(block.split(b'\0', 1)[0])
        if b'\0' in block:
            return os.fsdecode(bytes(result))
    raise RuntimeError('Tracee string exceeds the supported complete capture bound')


def arguments(pid, address):
    result = []
    for index in range(MAX_ARGUMENTS):
        pointer = ptrace(PEEKDATA, pid, address + index * 8) & MASK
        if not pointer:
            return result
        result.append(string(pid, pointer))
    raise RuntimeError('Tracee argument array exceeds the supported complete capture bound')


def resolved(pid, name, directory=AT_FDCWD):
    path = Path(name)
    if path.is_absolute():
        return str(path.resolve())
    descriptor = ctypes.c_int(directory).value
    root = Path('/proc') / str(pid) / ('cwd' if descriptor == AT_FDCWD else 'fd/' + str(descriptor))
    return str((Path(os.readlink(root)) / path).resolve())


def identity(pid):
    source = Path('/proc') / str(pid)
    status = (source / 'stat').read_text()
    return {'pid': pid, 'start_ticks': status.rsplit(')', 1)[1].split()[19]}


def deadline(signum, frame):
    raise TimeoutError('Supervisor deadline reached; lifecycle outcome remains unverified')


class Supervisor:
    def __init__(self, args):
        self.args = args
        self.processes = {}
        self.root = None
        self.attempts = 0
        self.successes = 0
        self.injected = 0
        self.killed = False
        self.first = None
        self.native = None
        self.execs = []
        self.sequence = 0
        self.wait_context = None
        self.started = time.monotonic()
        self.receipt = {'argv': args.command, 'cwd': str(Path.cwd()), 'started_at': now(),
                        'mode': args.mode, 'terminal': str(args.terminal),
                        'platform': platform.platform(), 'machine': platform.machine(),
                        'python': sys.version, 'supervisor_sha256': digest(__file__),
                        'claim': 'External syscall mechanics only; lifecycle acceptance is unverified'}
        self.events = (args.output / 'events.jsonl').open('w', buffering=1)

    def event(self, kind, **values):
        self.sequence += 1
        record = {'sequence': self.sequence, 'at': now(), 'elapsed_seconds': time.monotonic() - self.started,
                  'kind': kind, **values}
        self.events.write(json.dumps(record, sort_keys=True) + '\n')

    def save_command(self):
        write(self.args.output / 'command.json', self.receipt)

    def snapshot(self, name, source):
        if not os.path.lexists(source):
            return None
        if not source.is_file() or source.is_symlink():
            raise RuntimeError('Snapshot source must be a regular file: ' + str(source))
        destination = self.args.output / name
        destination.write_bytes(source.read_bytes())
        result = {'file': name, 'bytes': destination.stat().st_size, 'sha256': digest(destination)}
        self.event('snapshot', **result)
        return result

    def start(self):
        if sys.platform != 'linux' or platform.machine() != 'x86_64' or ctypes.sizeof(ctypes.c_void_p) != 8:
            raise RuntimeError('Supervisor requires 64-bit Linux x86_64')
        self.save_command()
        with (self.args.output / 'command.stdout').open('wb') as stdout, \
                (self.args.output / 'command.stderr').open('wb') as stderr:
            pid = os.fork()
            if pid == 0:
                try:
                    os.setsid()
                    os.dup2(stdout.fileno(), 1)
                    os.dup2(stderr.fileno(), 2)
                    ptrace(TRACEME, 0)
                    os.kill(os.getpid(), signal.SIGSTOP)
                    os.execvpe(self.args.command[0], self.args.command,
                               {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                except BaseException as error:
                    os.write(2, (type(error).__name__ + ': ' + str(error) + '\n').encode())
                    os._exit(125)
        self.root = pid
        self.receipt['process'] = identity(pid)
        self.save_command()
        self.processes[pid] = {'entry': True, 'call': None, 'newborn': False, 'exec': None,
                               'identity': self.receipt['process']}
        _, status = os.waitpid(pid, 0)
        if not os.WIFSTOPPED(status) or os.WSTOPSIG(status) != signal.SIGSTOP:
            self.finished(pid, status)
            raise RuntimeError('Tracee did not reach its initial ptrace stop; inspect command.stderr')
        ptrace(SETOPTIONS, pid, data=OPTIONS)
        self.event('trace-start', **self.receipt['process'])
        ptrace(SYSCALL, pid)

    def entered(self, pid, state, regs):
        number = regs.orig_rax
        if number >= 0x40000000:
            raise RuntimeError('Unsupported syscall ABI or unexpected entry register state')
        call = {'number': number}
        if number in (RENAME, RENAMEAT, RENAMEAT2):
            if number == RENAME:
                source = resolved(pid, string(pid, regs.rdi))
                target = resolved(pid, string(pid, regs.rsi))
            else:
                source = resolved(pid, string(pid, regs.rsi), regs.rdi)
                target = resolved(pid, string(pid, regs.r10), regs.rdx)
            selected = target == str(self.args.terminal)
            if selected and (pid != self.root or source != str(self.args.temporary)):
                raise RuntimeError('Unexpected writer or temporary path for the selected destination')
            if selected:
                self.attempts += 1
                call.update(selected=True, attempt=self.attempts, source=source, destination=target)
                if number == RENAMEAT2 and regs.r8:
                    raise RuntimeError('Selected renameat2 flags are unsupported')
                inject = ((self.args.mode == 'eio-first' and self.attempts == 1) or
                          (self.args.mode == 'eio-final' and self.attempts == 2))
                if inject:
                    regs.orig_rax = MASK
                    ptrace(SETREGS, pid, data=ctypes.byref(regs))
                    call['simulated_syscall_errno'] = errno.EIO
                self.event('replacement-entry', pid=pid, **call)
        elif number in (EXECVE, EXECVEAT):
            path = resolved(pid, string(pid, regs.rdi if number == EXECVE else regs.rsi),
                            AT_FDCWD if number == EXECVE else regs.rdi)
            argv = arguments(pid, regs.rsi if number == EXECVE else regs.rdx)
            record = {'pid': pid, 'executable': path, 'argv': argv, 'entry_at': now(),
                      'exec_confirmed': False, 'native_returncode': None}
            self.execs.append(record)
            call['exec_index'] = len(self.execs) - 1
            self.event('exec-entry', **record)
        state['call'] = call

    def exited(self, pid, state, regs):
        call = state['call']
        if call is None:
            self.event('newborn-syscall-exit', pid=pid, number=regs.orig_rax, result=signed(regs.rax))
            return
        expected = MASK if 'simulated_syscall_errno' in call else call['number']
        if call['number'] == RT_SIGRETURN and regs.orig_rax == MASK:
            self.event('signal-return', **identity(pid), number=RT_SIGRETURN,
                       restored_orig_rax=regs.orig_rax, restored_rax=signed(regs.rax), rip=regs.rip)
            state['call'] = None
            return
        if regs.orig_rax != expected:
            self.event('syscall-mismatch', **identity(pid), expected_orig_rax=expected,
                       registers={name: getattr(regs, name) for name in REGISTER_NAMES},
                       state=state)
            raise RuntimeError('Syscall entry/exit identity mismatch for PID ' + str(pid))
        if 'simulated_syscall_errno' in call:
            regs.rax = (-call['simulated_syscall_errno']) & MASK
            ptrace(SETREGS, pid, data=ctypes.byref(regs))
            self.injected += 1
        result = signed(regs.rax)
        if call.get('selected'):
            self.event('replacement-exit', pid=pid, result=result, **call)
            if result == 0:
                self.successes += 1
                if self.successes == 1:
                    self.first = self.snapshot('first-terminal.json', self.args.terminal)
                    if self.args.mode == 'kill-after-first':
                        self.event('signal-request', pid=pid, signal=signal.SIGKILL,
                                   boundary='successful-first-replacement-exit')
                        os.kill(pid, signal.SIGKILL)
                        self.killed = True
        if 'exec_index' in call:
            self.execs[call['exec_index']]['syscall_result'] = result
        state['call'] = None

    def finished(self, pid, status):
        if os.WIFEXITED(status):
            native = os.WEXITSTATUS(status)
        elif os.WIFSIGNALED(status):
            native = -os.WTERMSIG(status)
        else:
            raise RuntimeError('Unexpected nonterminal wait status')
        state = self.processes.pop(pid, {})
        if state.get('pending_exit') is not None:
            self.event('tracee-exit-confirmed', pid=pid, wait_status=status, native_returncode=native,
                       pending_exit=state['pending_exit'])
        if state.get('exec') is not None:
            self.execs[state['exec']]['native_returncode'] = native
        if pid == self.root:
            self.native = native
        self.event('process-exit', pid=pid, wait_status=status, native_returncode=native,
                   identity=state.get('identity'))

    def observe(self):
        while self.processes:
            pid, status = os.waitpid(-1, WALL)
            known = pid in self.processes
            self.wait_context = {'pid': pid, 'wait_status': status, 'known_task': known,
                                 'stopped': os.WIFSTOPPED(status),
                                 'task_state': json.loads(json.dumps(self.processes.get(pid)))}
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                unassociated = not known or self.processes[pid].get('held_newborn')
                self.finished(pid, status)
                if unassociated:
                    raise RuntimeError('Task exited before its parent creation event established identity')
                continue
            if not os.WIFSTOPPED(status):
                raise RuntimeError('Unsupported wait status')
            stopped, event = os.WSTOPSIG(status), status >> 16
            if not known:
                if stopped != signal.SIGSTOP or event:
                    raise RuntimeError('Unknown task did not report an initial newborn stop')
                child_identity = identity(pid)
                self.processes[pid] = {'entry': None, 'call': None, 'newborn': False, 'exec': None,
                                       'identity': child_identity, 'held_newborn': True}
                self.event('newborn-held', wait_status=status, **child_identity)
                continue
            state = self.processes[pid]
            if state.get('held_newborn'):
                raise RuntimeError('Held newborn stopped again before parent association')
            if state.get('pending_exit') is not None:
                raise RuntimeError('Tracee stopped again after an unresolved ptrace ESRCH')
            try:
                deliver = 0
                if event in (FORK, VFORK, CLONE):
                    child = ctypes.c_ulonglong()
                    ptrace(GETEVENTMSG, pid, data=ctypes.byref(child))
                    child_identity = identity(child.value)
                    child_state = self.processes.get(child.value)
                    if child_state is not None:
                        if not child_state.get('held_newborn') or child_state['identity'] != child_identity:
                            raise RuntimeError('Child creation event conflicts with a tracked task lifetime')
                    else:
                        child_state = {'entry': None, 'call': None, 'newborn': True, 'exec': None,
                                       'identity': child_identity}
                        self.processes[child.value] = child_state
                    self.event('process-created', parent=pid, event=event, **child_identity)
                    if child_state.pop('held_newborn', False):
                        ptrace(SYSCALL, child.value)
                        self.event('newborn-resumed', parent=pid, **child_identity)
                elif event == EXEC:
                    former = ctypes.c_ulonglong()
                    ptrace(GETEVENTMSG, pid, data=ctypes.byref(former))
                    if former.value != pid:
                        raise RuntimeError('Nonleader thread exec is unsupported; descendant coverage is incomplete')
                    call = state.get('call') or {}
                    if 'exec_index' not in call:
                        raise RuntimeError('Exec event has no captured argument entry')
                    state['exec'] = call['exec_index']
                    self.execs[state['exec']]['exec_confirmed'] = True
                    self.event('exec-confirmed', pid=pid, exec_index=state['exec'])
                elif event:
                    raise RuntimeError('Unsupported ptrace event: ' + str(event))
                elif stopped == (signal.SIGTRAP | 0x80):
                    regs = registers(pid)
                    if state['entry'] is None:
                        state['entry'] = signed(regs.rax) == -errno.ENOSYS
                    if state['entry']:
                        if signed(regs.rax) != -errno.ENOSYS:
                            raise RuntimeError('Unexpected syscall-entry register state')
                        self.entered(pid, state, regs)
                    else:
                        self.exited(pid, state, regs)
                    state['entry'] = not state['entry']
                elif stopped == signal.SIGSTOP and state['newborn']:
                    state['newborn'] = False
                    self.event('newborn-stop', pid=pid)
                elif stopped in (signal.SIGSTOP, signal.SIGTSTP, signal.SIGTTIN, signal.SIGTTOU):
                    raise RuntimeError('External group stops are unsupported')
                else:
                    deliver = stopped
                    self.event('signal-delivery', pid=pid, signal=deliver)
                ptrace(SYSCALL, pid, data=deliver)
            except ProcessLookupError as failure:
                context = {'operation': getattr(failure, 'ptrace_operation', None),
                           'pid': getattr(failure, 'ptrace_pid', None), 'errno': failure.errno,
                           'wait_context': self.wait_context,
                           'task_state': json.loads(json.dumps(state))}
                self.event('ptrace-unavailable', **context)
                call = state.get('call') or {}
                if (not known or context['pid'] != pid or
                        context['operation'] not in (GETREGS, SYSCALL) or call.get('selected')):
                    raise
                state['pending_exit'] = context
                self.event('tracee-exit-pending', pid=pid)

    def cleanup(self):
        for pid in list(self.processes):
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        until = time.monotonic() + 5
        while self.processes and time.monotonic() < until:
            try:
                pid, status = os.waitpid(-1, WALL | os.WNOHANG)
            except ChildProcessError:
                break
            if not pid:
                time.sleep(0.01)
                continue
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                self.finished(pid, status)
            elif os.WIFSTOPPED(status):
                try:
                    ptrace(SYSCALL, pid, data=signal.SIGKILL)
                except ProcessLookupError:
                    pass
        if self.processes:
            self.event('cleanup-incomplete', unreaped_pids=sorted(self.processes))

    def run(self):
        error = None
        previous_alarm = signal.signal(signal.SIGALRM, deadline)
        signal.setitimer(signal.ITIMER_REAL, self.args.timeout_seconds)
        try:
            self.start()
            self.observe()
        except BaseException as failure:
            signal.setitimer(signal.ITIMER_REAL, 0)
            error = {'type': type(failure).__name__, 'message': str(failure),
                     'wait_context': self.wait_context}
            if hasattr(failure, 'ptrace_operation'):
                error['ptrace_context'] = {'operation': failure.ptrace_operation,
                                           'pid': failure.ptrace_pid, 'errno': failure.errno}
            self.event('supervisor-error', **error)
            self.cleanup()
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_alarm)
        try:
            final = self.snapshot('last-terminal.json', self.args.terminal)
            temporary = self.snapshot('last-temporary.json', self.args.temporary)
        except (OSError, RuntimeError) as failure:
            error = error or {'type': type(failure).__name__, 'message': str(failure)}
            final, temporary = None, None
        expected = {'observe': (2, 2, 0, False), 'eio-first': (1, 0, 1, False),
                    'eio-final': (2, 1, 1, False), 'kill-after-first': (1, 1, 0, True)}
        observed = (self.attempts, self.successes, self.injected, self.killed)
        retained = {'first_terminal': self.first, 'last_terminal': final, 'last_temporary': temporary}
        required = ['first_terminal', 'last_terminal'] if self.args.mode != 'eio-first' or self.successes else []
        if self.args.mode.startswith('eio-'):
            required.append('last_temporary')
        missing = []
        for name in required:
            record = retained[name]
            path = self.args.output / record['file'] if record else None
            try:
                intact = (path is not None and path.is_file() and not path.is_symlink() and
                          path.stat().st_size == record['bytes'] and digest(path) == record['sha256'])
            except OSError:
                intact = False
            if not intact:
                missing.append(name)
        unexpected_terminal = self.args.mode == 'eio-first' and final is not None
        complete = (not error and not missing and not unexpected_terminal and not self.processes and
                    observed == expected[self.args.mode] and self.native is not None)
        self.receipt.update(ended_at=now(), elapsed_seconds=time.monotonic() - self.started,
                            native_returncode=self.native, status_convention='negative signal, nonnegative exit',
                            stdout_sha256=digest(self.args.output / 'command.stdout') if self.root else None,
                            stderr_sha256=digest(self.args.output / 'command.stderr') if self.root else None)
        self.save_command()
        summary = {'coverage_verdict': 'Passed' if complete else 'Incomplete', 'error': error,
                   'native_returncode': self.native, 'replacement_attempts': self.attempts,
                   'successful_replacements': self.successes, 'simulated_EIO_count': self.injected,
                   'signal_requested': self.killed, **retained, 'missing_evidence': missing,
                   'unexpected_terminal': unexpected_terminal,
                   'unreaped_pids': sorted(self.processes),
                   'lifecycle_verdict': 'Incomplete', 'unverified': ['evaluator entry', 'service-stop count',
                       'real lifecycle', 'power-loss durability'], 'expected_boundary_reached': complete}
        write(self.args.output / 'execs.json', self.execs)
        write(self.args.output / 'summary.json', summary)
        self.events.close()
        print(json.dumps({'output': str(self.args.output), **summary}))
        return 0 if complete else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--terminal', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mode', choices=('observe', 'kill-after-first', 'eio-first', 'eio-final'), required=True)
    parser.add_argument('--timeout-seconds', type=float, default=3600)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command[:1] == ['--']:
        args.command = args.command[1:]
    if sys.platform != 'linux' or platform.machine() != 'x86_64' or ctypes.sizeof(ctypes.c_void_p) != 8:
        parser.error('Supervisor requires 64-bit Linux x86_64')
    if not args.command or not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
        parser.error('An actual command and positive timeout are required')
    if any(os.path.lexists(path) for path in (args.terminal, args.output)):
        parser.error('Terminal and output destinations must have no existing filesystem entry')
    if any(path.absolute() != path.resolve() for path in (args.terminal, args.output)):
        parser.error('Destination paths must not contain symlinks or ambiguous parent components')
    args.terminal = args.terminal.resolve()
    args.output = args.output.resolve()
    args.temporary = args.terminal.with_suffix(args.terminal.suffix + '.tmp')
    parent = args.terminal.parent
    if not parent.is_dir() or any(os.path.lexists(path) for path in (args.terminal, args.temporary)):
        parser.error('An existing parent and absent terminal/temporary destinations are required')
    if os.path.lexists(args.output) or parent == args.output or parent in args.output.parents or args.output in parent.parents:
        parser.error('Output must be new and must not overlap the terminal directory')
    os.umask(0o077)
    args.output.mkdir(parents=True)
    return Supervisor(args).run()


if __name__ == '__main__':
    raise SystemExit(main())
