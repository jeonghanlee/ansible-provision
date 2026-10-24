#!/usr/bin/env python3
"""Retain real lifecycle command receipts and replay complete terminal evidence."""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time

INSTALLED_INPUT = Path('/var/lib/etl-soak')
INSTALLED_TOOLS = Path('/usr/local/share/etl-soak')
TERMINALS = ('shutdown.json', 'abort.json')
RECORDS = ('observation.json', 'shutdown-started.json', 'abort-started.json', *TERMINALS)
SEMANTIC_FIELDS = ('verdict', 'failed_assertions', 'missing_coverage', 'scheduler_verdict',
                   'scheduler_failed_assertions', 'scheduler_missing_coverage')
RECORDING_FIELDS = ('verdict', 'failed_assertions', 'missing_coverage')


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def read(path):
    return json.loads(path.read_text())


def inventory(root):
    result = {}
    for path in [root, *sorted(root.rglob('*'))]:
        metadata = path.lstat()
        name = str(path.relative_to(root))
        item = {'mode': stat.S_IMODE(metadata.st_mode)}
        if stat.S_ISREG(metadata.st_mode):
            item.update(kind='file', bytes=metadata.st_size, sha256=digest(path))
        elif stat.S_ISDIR(metadata.st_mode):
            item['kind'] = 'directory'
        else:
            raise ValueError('Only regular files and directories are supported: ' + str(path))
        result[name] = item
    return result


def verify(root, expected):
    if inventory(root) != expected:
        raise RuntimeError('Complete membership, modes or bytes changed: ' + str(root))


def run(output, name, argv, checks=()):
    for root, expected in checks:
        verify(root, expected)
    receipt = {'argv': [str(value) for value in argv], 'cwd': str(output),
               'started_at': now(), 'verified_roots': [str(root) for root, _ in checks]}
    destination = output / (name + '.command.json')
    write(destination, receipt)
    began = time.monotonic()
    with (output / (name + '.stdout')).open('wb') as stdout, \
            (output / (name + '.stderr')).open('wb') as stderr:
        child = subprocess.Popen(receipt['argv'], cwd=output, stdout=stdout, stderr=stderr,
                                 env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        receipt['pid'] = child.pid
        write(destination, receipt)
        try:
            child.wait()
        finally:
            receipt.update(returncode=child.poll(), ended_at=now(),
                           elapsed_seconds=time.monotonic() - began)
            write(destination, receipt)
    receipt.update(stdout_sha256=digest(output / (name + '.stdout')),
                   stderr_sha256=digest(output / (name + '.stderr')))
    write(destination, receipt)
    return receipt


def copy_tree(source, target, output, name, expected):
    receipt = run(output, name, ['cp', '-a', '--reflink=auto', source, target])
    if receipt['returncode']:
        raise RuntimeError('Evidence copy failed; retained receipt: ' + name)
    verify(target, expected)


def semantic(value):
    result = {name: value[name] for name in SEMANTIC_FIELDS if name in value}
    if 'jfr_recordings' in value:
        result['jfr_recordings'] = {name: value['jfr_recordings'][name]
                                   for name in RECORDING_FIELDS if name in value['jfr_recordings']}
    return result


def terminal(root):
    paths = [root / name for name in TERMINALS if (root / name).is_file()]
    if len(paths) != 1:
        raise ValueError('Exactly one actual terminal record is required for replay')
    return paths[0], read(paths[0])


def replay(args):
    original_terminal, record = terminal(args.input)
    inputs, tools = inventory(args.input), inventory(args.tools)
    write(args.output / 'input-members.json', inputs)
    write(args.output / 'tool-members.json', tools)
    write(args.output / 'terminal-facts.json', {key: value for key, value in record.items()
                                               if key not in ('evaluation', 'verdict')})
    summary = {'claim': 'Retained-input replay, not start-to-terminal acceptance',
               'started_at': now(), 'input': str(args.input), 'tools': str(args.tools),
               'terminal_sha256': digest(original_terminal), 'commands': {},
               'input_files': sum(item['kind'] == 'file' for item in inputs.values()),
               'input_bytes': sum(item.get('bytes', 0) for item in inputs.values()),
               'runtime_semantics': semantic(record.get('evaluation', {})),
               'semantic_fields': list(SEMANTIC_FIELDS), 'recording_fields': list(RECORDING_FIELDS),
               'unexecuted': ['start-to-terminal', 'first-save capture', 'fault exposure',
                              'concurrent lifecycle', 'installed preparation-proof consumption']}
    write(args.output / 'summary.json', summary)
    failures = []
    for consumer in ('evaluate', 'aggregate'):
        case = args.output / consumer
        case.mkdir()
        state, package = case / 'input', case / 'tools'
        copy_tree(args.input, state, case, 'copy-input', inputs)
        copy_tree(args.tools, package, case, 'copy-tools', tools)
        argv = [sys.executable, '-B', package / (consumer + '.py'), '--input', state,
                '--jfr-binary', args.jfr_binary, '--jfr-output', case / 'jfr']
        if consumer == 'aggregate':
            argv += ['--output', case / 'result.json']
        receipt = run(case, consumer, argv, ((state, inputs), (package, tools)))
        value = read(case / ('result.json' if consumer == 'aggregate' else 'evaluate.stdout'))
        expected_status = int(value['verdict'] != 'Passed')
        if receipt['returncode'] != expected_status:
            failures.append(consumer + ': native status does not match its verdict')
        if not set(record.get('errors', [])) <= set(value['failed_assertions']):
            failures.append(consumer + ': original terminal errors are absent')
        if 'coherent_manifest_and_terminal' in value['missing_coverage']:
            failures.append(consumer + ': persisted terminal is not readable')
        verify(state, inputs)
        verify(package, tools)
        observed = semantic(value)
        compared = semantic(value if consumer == 'evaluate' else {**value.get('evaluation', {}), **value})
        agreement = compared == summary['runtime_semantics']
        if args.expect_runtime_agreement and not agreement:
            failures.append(consumer + ': runtime and offline semantic fields differ')
        summary['commands'][consumer] = {'returncode': receipt['returncode'],
                                         'elapsed_seconds': receipt['elapsed_seconds'],
                                         'observed_semantics': observed,
                                         'comparison_semantics': compared,
                                         'runtime_agreement': agreement,
                                         'input_and_tool_copies_unchanged': True}
        write(args.output / 'summary.json', summary)
    verify(args.input, inputs)
    verify(args.tools, tools)
    summary.update(original_input_and_tools_unchanged=True, completed_at=now(),
                   replay_assertion_failures=failures,
                   replay_verdict='Failed' if failures else 'Passed',
                   lifecycle_verdict='Incomplete')
    write(args.output / 'summary.json', summary)
    print(json.dumps({'output': str(args.output), 'replay_verdict': summary['replay_verdict'],
                      'lifecycle_verdict': 'Incomplete'}))
    return int(bool(failures))


def capture_records(source, destination):
    destination.mkdir()
    for name in RECORDS:
        path = source / name
        if path.is_file():
            shutil.copy2(path, destination / name)


def lifecycle(args):
    tools = inventory(args.tools)
    write(args.output / 'tool-members.json', tools)
    copy_tree(args.tools, args.output / 'tools', args.output, 'copy-tools', tools)
    capture_records(args.input, args.output / 'before')
    argv = [sys.executable, '-B', args.tools / 'observe.py', args.action]
    if args.action == 'start':
        argv += ['--duration-seconds', str(args.duration_seconds), '--chain', args.chain]
    if args.reason:
        argv += ['--reason', args.reason]
    receipt = run(args.output, 'lifecycle', argv, ((args.tools, tools),))
    capture_records(args.input, args.output / 'after')
    verify(args.tools, tools)
    write(args.output / 'summary.json', {
        'action': args.action, 'returncode': receipt['returncode'], 'completed_at': now(),
        'claim': 'Actual lifecycle command receipt; not complete lifecycle acceptance',
        'coverage_verdict': 'Incomplete',
        'unverified': ['first-save bytes at evaluation entry', 'fault exposure',
                       'independent service-stop count', 'offline agreement'],
        'records': inventory(args.output / 'after'), 'tool_sources_unchanged': True})
    print(json.dumps({'output': str(args.output), 'returncode': receipt['returncode'],
                      'coverage_verdict': 'Incomplete'}))
    return receipt['returncode'] if receipt['returncode'] >= 0 else 128 - receipt['returncode']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--action', choices=('replay', 'start', 'finish', 'abort'), required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--jfr-binary', type=Path)
    parser.add_argument('--expect-runtime-agreement', action='store_true')
    parser.add_argument('--duration-seconds', type=int, choices=(7200, 86400))
    parser.add_argument('--chain', choices=('shortened', 'default'))
    parser.add_argument('--reason')
    args = parser.parse_args()
    for name in ('input', 'tools', 'output'):
        setattr(args, name, getattr(args, name).resolve())
    paths = (args.input, args.tools, args.output)
    if any(left == right or left in right.parents or right in left.parents
           for index, left in enumerate(paths) for right in paths[index + 1:]):
        parser.error('Input, tools and output directories must not overlap')
    if not args.input.is_dir() or not args.tools.is_dir():
        parser.error('Existing actual input and tool directories are required')
    if args.output.exists():
        parser.error('Output must be a new directory')
    if args.action != 'start' and (args.duration_seconds is not None or args.chain is not None):
        parser.error('Duration and chain are valid only for start')
    if args.action != 'abort' and args.reason is not None:
        parser.error('Reason is valid only for abort')
    if args.action != 'replay' and (args.jfr_binary is not None or args.expect_runtime_agreement):
        parser.error('JFR and runtime-agreement options are valid only for replay')
    if args.action == 'replay':
        if args.jfr_binary is None or not args.jfr_binary.is_file() or not os.access(args.jfr_binary, os.X_OK):
            parser.error('Replay requires an actual --jfr-binary executable')
        args.jfr_binary = args.jfr_binary.resolve()
        terminal(args.input)
    elif args.input != INSTALLED_INPUT or args.tools != INSTALLED_TOOLS:
        parser.error('Lifecycle actions require the actual installed input and tool paths')
    if args.action == 'start' and (args.duration_seconds is None or args.chain is None):
        parser.error('Start requires --duration-seconds and --chain')
    if args.action == 'abort' and not args.reason:
        parser.error('Abort requires an explicit --reason')
    os.umask(0o077)
    args.output.mkdir(parents=True)
    dependencies = {'python': {'path': str(Path(sys.executable).resolve()),
                               'sha256': digest(Path(sys.executable).resolve()), 'version': sys.version},
                    'runner_sha256': digest(Path(__file__))}
    if args.jfr_binary:
        dependencies['jfr'] = {'path': str(args.jfr_binary), 'sha256': digest(args.jfr_binary)}
    write(args.output / 'dependencies.json', dependencies)
    try:
        return replay(args) if args.action == 'replay' else lifecycle(args)
    except Exception as error:
        failure = {'type': type(error).__name__, 'message': str(error), 'at': now(),
                   'coverage_verdict': 'Incomplete'}
        if args.action == 'replay':
            for name, source in (('input', args.input), ('tool', args.tools)):
                recorded = args.output / (name + '-members.json')
                if recorded.is_file():
                    try:
                        failure[name + '_unchanged'] = inventory(source) == read(recorded)
                    except (OSError, ValueError) as inspection:
                        failure[name + '_inspection_error'] = str(inspection)
        write(args.output / 'execution-error.json', failure)
        raise


if __name__ == '__main__':
    raise SystemExit(main())
