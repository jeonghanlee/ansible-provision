#!/usr/bin/env python3
"""Check external syscall mechanics with the shipped writer and retained JSON input."""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import time


EXIT_ATTEMPTS = 20
EARLY_ATTEMPTS = 32
EARLY_THREADS = 128
C_SOURCE = '''#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
static void *work(void *argument) { return argument; }
int main(int argc, char **argv) {
    int count = argc == 2 ? atoi(argv[1]) : 0;
    if (count < 1 || count > 128) return 2;
    pthread_t threads[128];
    for (int i = 0; i < count; i++) {
        int error = pthread_create(&threads[i], NULL, work, NULL);
        if (error) { fprintf(stderr, "pthread_create: %d\\n", error); return 3; }
    }
    for (int i = 0; i < count; i++) {
        int error = pthread_join(threads[i], NULL);
        if (error) { fprintf(stderr, "pthread_join: %d\\n", error); return 4; }
    }
    printf("joined %d\\n", count);
    return 0;
}
'''
THREAD_CHILD = '''import os, sys, threading, time
ready = threading.Barrier(17)
def work():
    ready.wait()
    for _ in range(100):
        os.getpid()
        time.sleep(0.0001)
threads = [threading.Thread(target=work) for _ in range(16)]
for thread in threads: thread.start()
ready.wait()
print("threads-ready", flush=True)
if sys.argv[1] == "group": os._exit(0)
if sys.argv[1] == "kill":
    while True: time.sleep(1)
for thread in threads: thread.join()
'''
JAVA_SOURCE = '''class ProbeTarget {
 public static void main(String[] args) throws Exception {
  System.out.println(ProcessHandle.current().pid());
  System.out.flush();
  System.in.read();
 }
}
'''

WRITER = '''import json, os, signal, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import collect
value = json.loads(Path(sys.argv[2]).read_text())
second = json.loads(Path(sys.argv[3]).read_text())
target = Path(sys.argv[4])
variant = sys.argv[5]
handled = []
if variant == "signal":
    signal.signal(signal.SIGUSR1, lambda number, frame: handled.append(number))
def deliver(expected):
    if variant == "signal":
        os.kill(os.getpid(), signal.SIGUSR1)
        assert len(handled) == expected
        print(json.dumps({'handled_signals': len(handled)}), flush=True)
if variant in ("joined", "group", "kill"):
    child = subprocess.Popen([sys.executable, "-B", "-c", sys.argv[9], variant],
                             stdout=subprocess.PIPE, text=True)
    line = child.stdout.readline()
    assert line == "threads-ready\\n", repr(line)
    print(json.dumps({'child_pid': child.pid, 'ready': line.strip()}), flush=True)
    if variant == "kill":
        os.kill(child.pid, signal.SIGKILL)
    result = child.wait(timeout=10)
    print(json.dumps({'child_pid': child.pid, 'native_returncode': result}), flush=True)
    assert result == (-signal.SIGKILL if variant == "kill" else 0)
if variant == "jstat":
    child = subprocess.Popen([sys.argv[6], sys.argv[8]], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, text=True)
    try:
        line = child.stdout.readline()
        assert int(line) == child.pid
        print(json.dumps({'jvm_pid': child.pid, 'ready': line.strip()}), flush=True)
        subprocess.run([sys.argv[7], "-gc", line.strip()], check=True)
        child.stdin.close()
        result = child.wait(timeout=10)
        print(json.dumps({'jvm_pid': child.pid, 'native_returncode': result}), flush=True)
        assert result == 0
    finally:
        if child.poll() is None:
            child.kill()
            child.wait()
if variant == "early":
    subprocess.run([sys.argv[10], str(sys.argv[11])], check=True)
if variant == "jdk":
    subprocess.run([sys.argv[6], "-version"], check=True)
if variant == "timeout":
    time.sleep(10)
if variant == "relative":
    os.chdir(target.parent)
    target = Path(target.name)
if variant == "child":
    subprocess.run([sys.executable, "-B", "-c", "raise SystemExit(7)"], check=False)
if variant in ("unrelated", "missing"):
    collect.write_json(target.with_name("unrelated.json"), value)
    collect.write_json(target.with_name("unrelated.json"), value)
if variant != "missing":
    try:
        deliver(1)
        collect.write_json(target, value)
        deliver(2)
        collect.write_json(target, second)
    except OSError:
        if variant == "remove-temporary":
            target.with_suffix(target.suffix + ".tmp").unlink()
        raise
if variant == "remove-final":
    target.unlink()
if variant == "remove-first":
    (target.parent.parent / "trace" / "first-terminal.json").unlink()
'''


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def files(directory):
    result = {}
    for path in [directory, *sorted(directory.rglob('*'))]:
        item = {'mode': path.stat().st_mode & 0o7777}
        if path.is_symlink():
            raise ValueError('Tool snapshots must not contain symlinks')
        if path.is_file():
            item.update(sha256=digest(path))
        elif path.is_dir():
            item.update(directory=True)
        else:
            raise ValueError('Unsupported tool member: ' + str(path))
        result[str(path.relative_to(directory))] = item
    return result


def run(directory, argv):
    receipt = {'argv': [str(value) for value in argv], 'cwd': str(directory), 'started_at': now()}
    began = time.monotonic()
    write(directory / 'command.json', receipt)
    with (directory / 'command.stdout').open('wb') as stdout, \
            (directory / 'command.stderr').open('wb') as stderr:
        child = subprocess.Popen(receipt['argv'], cwd=directory, stdout=stdout, stderr=stderr,
                                 env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        receipt['pid'] = child.pid
        write(directory / 'command.json', receipt)
        receipt['native_returncode'] = child.wait()
    receipt.update(ended_at=now(), elapsed_seconds=time.monotonic() - began,
                   stdout_sha256=digest(directory / 'command.stdout'),
                   stderr_sha256=digest(directory / 'command.stderr'))
    write(directory / 'command.json', receipt)
    return receipt


def read(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--second-input', type=Path, required=True)
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--java-binary', type=Path, required=True)
    parser.add_argument('--jstat-binary', type=Path, required=True)
    parser.add_argument('--cc-binary', type=Path, required=True)
    args = parser.parse_args()
    if os.path.lexists(args.output) or args.output.absolute() != args.output.resolve():
        parser.error('Output must have no existing entry or symlink component')
    for name in ('input', 'second_input', 'tools', 'output', 'java_binary', 'jstat_binary', 'cc_binary'):
        setattr(args, name, getattr(args, name).resolve())
    if not args.input.is_file() or not args.second_input.is_file() or not args.tools.is_dir() or args.output.exists():
        parser.error('Actual input/tools and a new output directory are required')
    for dependency in (args.java_binary, args.jstat_binary, args.cc_binary):
        if not dependency.is_file() or not os.access(dependency, os.X_OK):
            parser.error('Executable real JDK java/jstat and C compiler binaries are required')
    if any(left == right or left in right.parents or right in left.parents
           for left, right in ((args.input.parent, args.output), (args.second_input.parent, args.output),
                               (args.tools, args.output))):
        parser.error('Output must not overlap input or tools')
    input_value = read(args.input)
    second_value = read(args.second_input)
    expected_bytes = (json.dumps(input_value, indent=2) + '\n').encode()
    expected_second = (json.dumps(second_value, indent=2) + '\n').encode()
    if expected_bytes == expected_second:
        parser.error('Two distinct actual retained JSON records are required')
    original = {'input_sha256': digest(args.input), 'second_input_sha256': digest(args.second_input),
                'input_path': str(args.input), 'second_input_path': str(args.second_input), 'tools': files(args.tools),
                'java_path': str(args.java_binary), 'java_sha256': digest(args.java_binary),
                'jstat_path': str(args.jstat_binary), 'jstat_sha256': digest(args.jstat_binary),
                'cc_path': str(args.cc_binary), 'cc_sha256': digest(args.cc_binary)}
    os.umask(0o077)
    args.output.mkdir(parents=True)
    write(args.output / 'originals.json', original)
    (args.output / 'retained-input.json').write_bytes(args.input.read_bytes())
    (args.output / 'retained-second-input.json').write_bytes(args.second_input.read_bytes())
    frozen_tools = args.output / 'frozen-tools'
    shutil.copytree(args.tools, frozen_tools)
    if files(frozen_tools) != original['tools']:
        raise RuntimeError('Frozen tool membership, modes or bytes differ')
    write(args.output / 'dependencies.json', {'python': sys.version, 'executable': sys.executable,
                                             'sha256': digest(Path(sys.executable).resolve()),
                                             'java_path': str(args.java_binary),
                                             'java_sha256': original['java_sha256'],
                                             'jstat_path': str(args.jstat_binary),
                                             'jstat_sha256': original['jstat_sha256']})
    helper = frozen_tools / 'terminal-boundary.py'
    java_source = args.output / 'ProbeTarget.java'
    java_source.write_text(JAVA_SOURCE)
    java_source_sha256 = digest(java_source)
    native_source, native_binary = args.output / 'threads.c', args.output / 'threads'
    native_source.write_text(C_SOURCE)
    native_source_sha256 = digest(native_source)
    compiler = args.output / 'compiler'
    compiler.mkdir()
    run(compiler, [args.cc_binary, '--version'])
    compiled = args.output / 'compile'
    compiled.mkdir()
    compilation = run(compiled, [args.cc_binary, '-pthread', '-O2', '-o', native_binary, native_source])
    if compilation['native_returncode'] != 0:
        result = {'verdict': 'Incomplete', 'cases': [], 'reason': 'Native workload compilation failed',
                  'receipt': str(compiled / 'command.json'), 'lifecycle_verdict': 'Incomplete'}
        write(args.output / 'summary.json', result)
        print(json.dumps(result))
        return 2
    native_binary_sha256 = digest(native_binary)
    write(args.output / 'native-workload.json', {'compiler': str(args.cc_binary),
        'compiler_sha256': original['cc_sha256'], 'source_sha256': native_source_sha256,
        'binary_sha256': native_binary_sha256, 'threads': EARLY_THREADS})
    rows = []
    exit_exposures = 0
    early_exposures = 0
    early_attempts = 0
    definitions = [('observe', 'plain'), ('eio-first', 'plain'), ('eio-final', 'plain'),
                   ('kill-after-first', 'plain'), ('observe', 'unrelated'),
                   ('observe', 'relative'), ('observe', 'child'), ('observe', 'missing'),
                   ('observe', 'timeout'), ('observe', 'remove-final'), ('observe', 'remove-first'),
                   ('eio-first', 'remove-temporary'), ('eio-final', 'remove-temporary'),
                   ('observe', 'signal'), ('eio-first', 'signal'), ('eio-final', 'signal'),
                   ('kill-after-first', 'signal'), ('observe', 'jdk'), ('observe', 'joined'),
                   *[('observe', 'group')] * EXIT_ATTEMPTS, ('observe', 'kill'), ('observe', 'jstat'),
                   *[('observe', 'early')] * EARLY_ATTEMPTS]
    for index, (mode, variant) in enumerate(definitions):
        if variant == 'early':
            if early_exposures:
                continue
            early_attempts += 1
        case = args.output / ('case-' + str(index + 1).zfill(2) + '-' + mode + '-' + variant)
        state = case / 'state'
        state.mkdir(parents=True)
        terminal, trace = state / 'terminal.json', case / 'trace'
        argv = [sys.executable, '-B', helper, '--terminal', terminal, '--output', trace,
                '--timeout-seconds', '0.1' if variant == 'timeout' else '30',
                '--mode', mode, '--', sys.executable, '-B', '-c', WRITER,
                frozen_tools, args.output / 'retained-input.json', args.output / 'retained-second-input.json',
                terminal, variant, args.java_binary, args.jstat_binary, java_source, THREAD_CHILD, native_binary, str(EARLY_THREADS)]
        if files(frozen_tools) != original['tools']:
            raise RuntimeError('Frozen tools changed before launch')
        if digest(args.output / 'retained-input.json') != original['input_sha256']:
            raise RuntimeError('Frozen first input changed before launch')
        if digest(args.output / 'retained-second-input.json') != original['second_input_sha256']:
            raise RuntimeError('Frozen second input changed before launch')
        if (digest(args.java_binary) != original['java_sha256'] or
                digest(args.jstat_binary) != original['jstat_sha256'] or
                digest(java_source) != java_source_sha256 or
                digest(args.cc_binary) != original['cc_sha256'] or
                digest(native_source) != native_source_sha256 or digest(native_binary) != native_binary_sha256):
            raise RuntimeError('JDK dependency or diagnostic source changed before launch')
        receipt = run(case, argv)
        summary = read(trace / 'summary.json') if (trace / 'summary.json').is_file() else None
        assertions = {}
        if summary is not None and summary.get('error') and not (
                variant == 'timeout' and summary['error'].get('type') == 'TimeoutError'):
            row = {'case': case.name, 'result': 'Incomplete', 'error': summary['error'],
                   'receipt': str(case / 'command.json')}
            rows.append(row)
            write(case / 'result.json', row)
            continue
        if variant == 'timeout' and summary is not None:
            assertions = {'timeout_recorded': (summary.get('error') or {}).get('type') == 'TimeoutError',
                          'supervisor_status': receipt['native_returncode'] == 2,
                          'target_killed': summary['native_returncode'] == -signal.SIGKILL,
                          'children_reaped': summary['unreaped_pids'] == [],
                          'no_terminal': not terminal.exists(),
                          'incomplete': summary['coverage_verdict'] == 'Incomplete'}
            row = {'case': case.name, 'result': 'Passed' if all(assertions.values()) else 'Failed',
                   'assertions': assertions, 'receipt': str(case / 'command.json')}
            rows.append(row)
            write(case / 'result.json', row)
            continue
        missing_case = variant in ('missing', 'remove-final', 'remove-first', 'remove-temporary')
        assertions['supervisor_status'] = receipt['native_returncode'] == (2 if missing_case else 0)
        if summary is None:
            assertions['summary_available'] = False
        else:
            assertions['coverage'] = summary['coverage_verdict'] == ('Incomplete' if missing_case else 'Passed')
            assertions['lifecycle_unverified'] = summary['lifecycle_verdict'] == 'Incomplete'
            expected_native = -signal.SIGKILL if mode == 'kill-after-first' else 1 if mode.startswith('eio-') else 0
            assertions['target_native_status'] = summary['native_returncode'] == expected_native
            assertions['children_reaped'] = summary['unreaped_pids'] == []
            snapshots = ('first-terminal.json', 'last-terminal.json')
            if mode == 'eio-first' or variant == 'missing':
                assertions['no_terminal'] = not terminal.exists()
                assertions['no_first_snapshot'] = not (trace / snapshots[0]).exists()
            else:
                final_bytes = expected_second if mode == 'observe' else expected_bytes
                assertions['terminal_bytes'] = (not terminal.exists() if variant == 'remove-final' else
                                                terminal.is_file() and terminal.read_bytes() == final_bytes)
                assertions['first_snapshot_bytes'] = (not (trace / snapshots[0]).exists() if variant == 'remove-first' else
                                                      (trace / snapshots[0]).is_file() and
                                                      (trace / snapshots[0]).read_bytes() == expected_bytes)
                assertions['last_snapshot_bytes'] = (not (trace / snapshots[1]).exists() if variant == 'remove-final' else
                                                     (trace / snapshots[1]).is_file() and
                                                     (trace / snapshots[1]).read_bytes() == final_bytes)
            expected_missing = {'remove-final': ['last_terminal'], 'remove-first': ['first_terminal'],
                                'remove-temporary': ['last_temporary']}.get(variant)
            if expected_missing is not None:
                assertions['missing_evidence_named'] = summary['missing_evidence'] == expected_missing
            if mode.startswith('eio-'):
                temporary_bytes = expected_bytes if mode == 'eio-first' else expected_second
                assertions['temporary_preserved'] = (not (trace / 'last-temporary.json').exists()
                    if variant == 'remove-temporary' else (trace / 'last-temporary.json').is_file() and
                    (trace / 'last-temporary.json').read_bytes() == temporary_bytes)
                events = [json.loads(line) for line in (trace / 'events.jsonl').read_text().splitlines()]
                failures = [item for item in events if item['kind'] == 'replacement-exit' and item['result'] == -5]
                assertions['exact_fault_receipt'] = len(failures) == 1 and failures[0]['simulated_syscall_errno'] == 5
                assertions['fault_target'] = bool(failures) and failures[0]['destination'] == str(terminal)
            if variant == 'child':
                child_exec = [item for item in read(trace / 'execs.json')
                              if item['argv'][-1:] == ['raise SystemExit(7)']]
                assertions['child_exec_outcome'] = (len(child_exec) == 1 and child_exec[0]['exec_confirmed'] and
                                                     child_exec[0]['native_returncode'] == 7)
            if variant == 'signal':
                count = 1 if mode in ('eio-first', 'kill-after-first') else 2
                actual = [json.loads(line) for line in (trace / 'command.stdout').read_text().splitlines()]
                assertions['handler_invocations'] = actual == [{'handled_signals': index} for index in range(1, count + 1)]
                events = [json.loads(line) for line in (trace / 'events.jsonl').read_text().splitlines()]
                root = read(trace / 'command.json')['process']['pid']
                returns = [item for item in events if item['kind'] == 'signal-return' and item['pid'] == root]
                assertions['native_signal_returns'] = (len(returns) == count and all(
                    item['number'] == 15 and item['restored_orig_rax'] == (1 << 64) - 1 for item in returns))
            if variant == 'jdk':
                java_exec = [item for item in read(trace / 'execs.json')
                             if item['argv'] == [str(args.java_binary), '-version']]
                assertions['java_exec_outcome'] = (len(java_exec) == 1 and java_exec[0]['exec_confirmed'] and
                                                    java_exec[0]['native_returncode'] == 0)
                events = [json.loads(line) for line in (trace / 'events.jsonl').read_text().splitlines()]
                assertions['java_threads_observed'] = any(item['kind'] == 'process-created' and
                    item['event'] == 3 and java_exec and item['parent'] == java_exec[0]['pid'] for item in events)
                assertions['java_version_retained'] = bool((trace / 'command.stderr').read_bytes())
            if variant in ('joined', 'group', 'kill', 'jstat'):
                events = [json.loads(line) for line in (trace / 'events.jsonl').read_text().splitlines()]
                unavailable = [item for item in events if item['kind'] == 'ptrace-unavailable']
                confirmed = [item for item in events if item['kind'] == 'tracee-exit-confirmed']
                assertions['deferred_exits_confirmed'] = all(
                    len([item for item in confirmed if item['pid'] == failed['pid'] and
                         item['pending_exit'] == {key: failed[key] for key in (
                             'operation', 'pid', 'errno', 'wait_context', 'task_state')}]) == 1
                    and failed['wait_context']['known_task'] and failed['wait_context']['stopped']
                    and os.WIFSTOPPED(failed['wait_context']['wait_status'])
                    and failed['operation'] in (12, 24) for failed in unavailable)
                assertions['no_unexplained_exit_confirmation'] = len(confirmed) == len(unavailable)
                if variant == 'group':
                    exit_exposures += len(unavailable)
                actual = [json.loads(line) for line in (trace / 'command.stdout').read_text().splitlines()
                          if line.startswith('{')]
                key = 'jvm_pid' if variant == 'jstat' else 'child_pid'
                expected_child = -signal.SIGKILL if variant == 'kill' else 0
                assertions['actual_child_ready_and_exit'] = (len(actual) == 2 and key in actual[0] and
                    actual[1].get(key) == actual[0][key] and
                    actual[1].get('native_returncode') == expected_child)
                execs = read(trace / 'execs.json')
                target_exec = [item for item in execs if actual and item['pid'] == actual[0].get(key) and
                               item['exec_confirmed']]
                assertions['child_exec_native'] = (len(target_exec) == 1 and
                                                    target_exec[0]['native_returncode'] == expected_child)
                if variant == 'jstat':
                    jstat_exec = [item for item in execs if item['argv'][:2] == [str(args.jstat_binary), '-gc']
                                  and item['exec_confirmed']]
                    assertions['jstat_exec_native'] = (len(jstat_exec) == 1 and
                                                       jstat_exec[0]['native_returncode'] == 0)
            if variant == 'early':
                events = [json.loads(line) for line in (trace / 'events.jsonl').read_text().splitlines()]
                held = [item for item in events if item['kind'] == 'newborn-held']
                valid = True
                for item in held:
                    created = [event for event in events if event['kind'] == 'process-created' and
                               event['pid'] == item['pid'] and event['start_ticks'] == item['start_ticks']]
                    resumed = [event for event in events if event['kind'] == 'newborn-resumed' and
                               event['pid'] == item['pid'] and event['start_ticks'] == item['start_ticks']]
                    exits = [event for event in events if event['kind'] == 'process-exit' and
                             event.get('identity') == {'pid': item['pid'], 'start_ticks': item['start_ticks']}]
                    valid = valid and len(created) == len(resumed) == len(exits) == 1
                    if len(created) == len(resumed) == len(exits) == 1:
                        valid = valid and (item['sequence'] < created[0]['sequence'] <
                            resumed[0]['sequence'] < exits[0]['sequence'] and
                            created[0]['parent'] == resumed[0]['parent'] and
                            exits[0]['native_returncode'] == 0 and os.WIFEXITED(exits[0]['wait_status']))
                assertions['held_lifetime_associated_resumed_exited_once'] = valid
                assertions['native_threads_joined'] = ((trace / 'command.stdout').read_text() ==
                                                       'joined ' + str(EARLY_THREADS) + '\n')
                if all(assertions.values()):
                    early_exposures += len(held)
        row = {'case': case.name, 'result': 'Passed' if all(assertions.values()) else 'Failed',
               'assertions': assertions, 'receipt': str(case / 'command.json')}
        rows.append(row)
        write(case / 'result.json', row)
    for name in ('existing-terminal', 'overlapping-output', 'dangling-terminal', 'dangling-temporary', 'dangling-output'):
        case = args.output / name
        state = case / 'state'
        state.mkdir(parents=True)
        terminal = state / 'terminal.json'
        output = case / 'trace' if name == 'existing-terminal' else state / 'trace'
        if name == 'existing-terminal':
            terminal.write_bytes(args.input.read_bytes())
        link = None
        unrelated = case / 'unrelated-destination'
        if name.startswith('dangling-'):
            output = case / 'trace'
            link = {'dangling-terminal': terminal, 'dangling-temporary': terminal.with_suffix('.json.tmp'),
                    'dangling-output': output}[name]
            link.symlink_to(unrelated)
        argv = [sys.executable, '-B', helper, '--terminal', terminal, '--output', output,
                '--mode', 'observe', '--', sys.executable, '-B', '-c', WRITER,
                frozen_tools, args.output / 'retained-input.json', args.output / 'retained-second-input.json',
                terminal, 'plain']
        receipt = run(case, argv)
        passed = receipt['native_returncode'] == 2 and not output.exists()
        if terminal.exists():
            passed = passed and digest(terminal) == original['input_sha256']
        if link is not None:
            passed = passed and link.is_symlink() and os.readlink(link) == str(unrelated) and not unrelated.exists()
            if link != terminal:
                passed = passed and not terminal.exists()
        row = {'case': name, 'result': 'Passed' if passed else 'Failed', 'receipt': str(case / 'command.json')}
        rows.append(row)
        write(case / 'result.json', row)
    rows.append({'case': 'group-exit-exposure', 'result': 'Passed' if exit_exposures else 'Incomplete',
                 'actual_esrch_events': exit_exposures, 'attempts': EXIT_ATTEMPTS,
                 'claim': 'Actual ESRCH exposure; zero observed errors does not exercise recovery'})
    rows.append({'case': 'early-child-exposure', 'result': 'Passed' if early_exposures else 'Incomplete',
                 'actual_held_lifetimes': early_exposures, 'attempts': early_attempts,
                 'maximum_attempts': EARLY_ATTEMPTS, 'threads_per_attempt': EARLY_THREADS,
                 'claim': 'Observed held-newborn ordering; writer success alone does not establish exposure'})
    unchanged = (original['input_sha256'] == digest(args.input) and
                 original['second_input_sha256'] == digest(args.second_input) and
                 original['java_sha256'] == digest(args.java_binary) and
                 original['jstat_sha256'] == digest(args.jstat_binary) and
                 java_source_sha256 == digest(java_source) and
                 original['cc_sha256'] == digest(args.cc_binary) and
                 native_source_sha256 == digest(native_source) and
                 native_binary_sha256 == digest(native_binary) and
                 original['tools'] == files(args.tools) == files(frozen_tools))
    verdict = ('Failed' if not unchanged or any(row['result'] == 'Failed' for row in rows) else
               'Incomplete' if any(row['result'] == 'Incomplete' for row in rows) else 'Passed')
    result = {'verdict': verdict, 'cases': rows, 'originals_unchanged': unchanged,
              'claim': 'Real writer and external syscall mechanics only', 'lifecycle_verdict': 'Incomplete',
              'completed_at': now()}
    write(args.output / 'summary.json', result)
    print(json.dumps({'output': str(args.output), **result}))
    return 0 if verdict == 'Passed' else 1 if verdict == 'Failed' else 2


if __name__ == '__main__':
    raise SystemExit(main())
