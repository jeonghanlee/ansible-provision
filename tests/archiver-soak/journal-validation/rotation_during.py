"""Observe actual native journal reads across a real journal rotation command."""

import json
import os
from pathlib import Path
import threading
import time

import basic
import journal_coverage
import prepare

POLL_SECONDS = 0.002
PROCESS_ROOT = Path('/proc')


def snapshot(pid):
    path = PROCESS_ROOT / str(pid)
    try:
        fields = (path / 'stat').read_text().rsplit(')', 1)[1].split()
        arguments = [value.decode() for value in (path / 'cmdline').read_bytes().split(b'\0') if value]
        counters = dict(line.split(':', 1) for line in (path / 'io').read_text().splitlines())
        return {'pid': int(pid), 'parent_pid': int(fields[1]), 'state': fields[0],
                'start_ticks': fields[19], 'arguments': arguments,
                'written_characters': int(counters['wchar']), 'observed': basic.clock()}
    except (OSError, ValueError, IndexError):
        return None


def is_sequence_query(process, parent):
    if process is None or process['parent_pid'] != parent or process['state'] not in ('R', 'S', 'D'):
        return False
    arguments = process['arguments']
    return (len(arguments) == 11 and Path(arguments[0]).name == 'journalctl'
            and arguments[1:6] == ['--no-pager', '--all', '-o', 'json', '-b']
            and arguments[7] == '--cursor' and arguments[9] == '--until')


def child_hints(parent, owner=None):
    tasks = (PROCESS_ROOT / str(parent) / 'task')
    paths = [tasks / str(owner) / 'children'] if owner is not None else tasks.glob('*/children')
    children = set()
    for path in paths:
        try:
            children.update(int(value) for value in path.read_text().split())
        except OSError:
            continue
    return sorted(children)


def is_rotation_process(process, parent):
    return bool(process and process['parent_pid'] == parent and process['state'] in ('R', 'S', 'D')
                and len(process['arguments']) == 2 and Path(process['arguments'][0]).name == 'journalctl'
                and process['arguments'][1] == '--rotate')


class Witness:
    """Record real rotation/query lifetimes around actual file-header observations."""

    def __init__(self, path, parent, owner, query_pid):
        self.path, self.parent, self.owner, self.query_pid = path, parent, owner, query_pid
        self.ready = threading.Event()
        self.stopping = threading.Event()
        self.error = None

    def run(self):
        try:
            with self.path.open('x') as output:
                self.ready.set()
                while not self.stopping.is_set():
                    for pid in child_hints(self.parent, self.owner):
                        rotation_before = snapshot(pid)
                        if not is_rotation_process(rotation_before, self.parent):
                            continue
                        query_before = snapshot(self.query_pid)
                        files, error = None, None
                        if is_sequence_query(query_before, self.parent):
                            try:
                                files = journal_coverage.file_headers()
                            except (OSError, RuntimeError) as exception:
                                error = str(exception)
                        files_observed = basic.clock()
                        query_after = snapshot(self.query_pid)
                        rotation_after = snapshot(pid)
                        sample = {'rotation_before': rotation_before, 'query_before': query_before,
                                  'files': files, 'files_error': error, 'files_observed': files_observed,
                                  'query_after': query_after, 'rotation_after': rotation_after}
                        output.write(json.dumps(sample, sort_keys=True) + '\n')
                    self.stopping.wait(POLL_SECONDS)
                output.flush()
                os.fsync(output.fileno())
        except Exception as exception:
            self.error = str(exception)
            self.ready.set()


def overlapping(attempt, parent):
    before, after = attempt.get('query_before'), attempt.get('query_after')
    command = attempt.get('command')
    return bool(command and command.get('returncode') == 0 and not command.get('error')
                and is_sequence_query(before, parent) and is_sequence_query(after, parent)
                and before['pid'] == after['pid'] and before['start_ticks'] == after['start_ticks']
                and before['arguments'] == after['arguments']
                and before['observed']['monotonic_ns'] <= command['started']['monotonic_ns']
                <= command['finished']['monotonic_ns'] <= after['observed']['monotonic_ns']
                and after['written_characters'] > before['written_characters'])


def file_change(before, after):
    old = {row['file_id']: row for row in before}
    new = {row['file_id']: row for row in after}
    populated = {key for key, value in old.items() if value['entries']}
    renamed = [key for key in populated & new.keys() if old[key]['file'] != new[key]['file']]
    return {'preserved': populated <= new.keys(), 'renamed': len(renamed),
            'new': len(new.keys() - old.keys())}


def rotation_files(before, after):
    change = file_change(before['files'], after['files'])
    if before['daemon'] != after['daemon'] or not change['preserved'] or not change['renamed'] or not change['new']:
        raise RuntimeError('The observed file identities do not prove preserved journal rotation')
    return change['renamed']


def witnessed(directory, number, attempt, parent, before):
    path = directory / ('witness-' + str(number) + '.jsonl')
    if prepare.digest(path.read_bytes()) != attempt['witness_sha256']:
        raise RuntimeError('The concurrent process/file observation changed')
    command = attempt['command']
    discovered = attempt['query_discovered']
    initial = attempt['query_before']
    if (not is_sequence_query(discovered, parent) or not is_sequence_query(initial, parent)
            or discovered['pid'] != initial['pid'] or discovered['start_ticks'] != initial['start_ticks']
            or discovered['arguments'] != initial['arguments']
            or not discovered['observed']['monotonic_ns'] <= before['observed']['monotonic_ns']
            <= before['finished']['monotonic_ns'] <= initial['observed']['monotonic_ns']
            <= command['started']['monotonic_ns']):
        return False
    for line in path.read_text().splitlines():
        sample = json.loads(line)
        rb, ra = sample['rotation_before'], sample['rotation_after']
        qb, qa = sample['query_before'], sample['query_after']
        if (not is_rotation_process(rb, parent) or not is_rotation_process(ra, parent)
                or rb['pid'] != ra['pid'] or rb['start_ticks'] != ra['start_ticks']
                or not is_sequence_query(qb, parent) or not is_sequence_query(qa, parent)
                or any(value['pid'] != initial['pid'] or value['start_ticks'] != initial['start_ticks']
                       or value['arguments'] != initial['arguments'] for value in (qb, qa))
                or qa['written_characters'] <= discovered['written_characters']
                or sample['files'] is None or sample['files_error']):
            continue
        stamps = [command['started']['monotonic_ns'], rb['observed']['monotonic_ns'],
                  qb['observed']['monotonic_ns'], sample['files_observed']['monotonic_ns'],
                  qa['observed']['monotonic_ns'], ra['observed']['monotonic_ns'],
                  command['finished']['monotonic_ns']]
        if stamps != sorted(stamps):
            continue
        change = file_change(before['files'], sample['files'])
        if change['preserved'] and change['renamed'] and change['new']:
            return True
    return False


class DuringCollection:
    """Observe up to three native query opportunities without substituting or delaying them."""

    def __init__(self, directory, indices, stopping):
        self.directory, self.indices, self.stopping = directory, indices, stopping
        self.error = None

    def run(self):
        destination = self.directory / 'rotation-during'
        destination.mkdir(mode=0o700)
        parent = os.getpid()
        driver = snapshot(parent)
        attempts = []
        try:
            if driver is None:
                raise RuntimeError('The actual scenario process identity is unavailable')
            for number in self.indices:
                interval = self.directory / 'collector' / ('interval-' + str(number))
                while not interval.exists():
                    if self.stopping.wait(POLL_SECONDS) or (self.directory / 'collector/error.json').is_file():
                        raise RuntimeError('The native collector did not reach a declared rotation opportunity')
                attempt = {'interval': interval.name, 'query_before': None, 'query_after': None,
                           'command': None, 'overlap_proven': False}
                attempts.append(attempt)
                prepare.save(destination / ('attempt-' + str(number) + '.json'), attempt)
                while not (interval / 'result.json').is_file():
                    if self.stopping.is_set() or (self.directory / 'collector/error.json').is_file():
                        raise RuntimeError('The native collector failed during a declared rotation opportunity')
                    found = None
                    for pid in child_hints(parent):
                        candidate = snapshot(pid)
                        if is_sequence_query(candidate, parent):
                            found = candidate
                            break
                    if found is None:
                        for process in PROCESS_ROOT.glob('[0-9]*'):
                            candidate = snapshot(process.name)
                            if is_sequence_query(candidate, parent):
                                found = candidate
                                break
                    if found is None:
                        self.stopping.wait(POLL_SECONDS)
                        continue
                    before = {'observed': basic.clock(), 'daemon': journal_coverage.daemon_identity(),
                              'files': journal_coverage.file_headers()}
                    before['finished'] = basic.clock()
                    query_before = snapshot(found['pid'])
                    if (not is_sequence_query(query_before, parent) or
                            query_before['start_ticks'] != found['start_ticks']):
                        continue
                    prepare.save(destination / ('before-' + str(number) + '.json'), before)
                    witness_path = destination / ('witness-' + str(number) + '.jsonl')
                    witness = Witness(witness_path, parent, threading.get_native_id(), found['pid'])
                    witness_worker = threading.Thread(target=witness.run)
                    witness_worker.start()
                    if not witness.ready.wait(basic.ACTION_TIMEOUT):
                        witness.stopping.set()
                        witness_worker.join()
                        raise RuntimeError('The concurrent process/file observer did not become ready')
                    if witness.error:
                        witness_worker.join()
                        prepare.save(destination / ('witness-error-' + str(number) + '.json'),
                                     {'observed': basic.clock(), 'error': witness.error})
                        raise RuntimeError('The concurrent process/file observer failed before rotation')
                    try:
                        command = basic.command(['journalctl', '--rotate'], destination / ('command-' + str(number)))
                    finally:
                        witness.stopping.set()
                        witness_worker.join()
                    query_after = snapshot(found['pid'])
                    after = {'observed': basic.clock(), 'daemon': journal_coverage.daemon_identity(),
                             'files': journal_coverage.file_headers()}
                    prepare.save(destination / ('after-' + str(number) + '.json'), after)
                    attempt.update(query_discovered=found, query_before=query_before, query_after=query_after,
                                   command=command, witness_sha256=prepare.digest(witness_path.read_bytes()))
                    prepare.save(destination / ('attempt-' + str(number) + '.json'), attempt)
                    if witness.error:
                        prepare.save(destination / ('witness-error-' + str(number) + '.json'),
                                     {'observed': basic.clock(), 'error': witness.error})
                        raise RuntimeError('The concurrent process/file observer failed')
                    physical_overlap = witnessed(destination, number, attempt, parent, before)
                    attempt['overlap_proven'] = overlapping(attempt, parent) or physical_overlap
                    attempt['physical_file_change_during_query'] = physical_overlap
                    prepare.save(destination / ('attempt-' + str(number) + '.json'), attempt)
                    if command.get('returncode') != 0 or command.get('error'):
                        raise RuntimeError('The actual during-query journal rotation failed')
                    rotation_files(before, after)
                    break
                prepare.save(destination / ('attempt-' + str(number) + '.json'), attempt)
                if attempt['overlap_proven']:
                    break
            if not any(attempt['overlap_proven'] for attempt in attempts):
                raise RuntimeError('No actual native query overlap was proved in the three declared opportunities')
        except Exception as error:
            self.error = str(error)
            prepare.save(destination / 'error.json', {'observed': basic.clock(), 'error': self.error})
        finally:
            prepare.save(destination / 'summary.json', {'driver': driver, 'attempts': attempts,
                         'declared_collection_indices': self.indices, 'observed': basic.clock()})


def verify(directory, contract):
    destination = directory / 'rotation-during'
    summary = json.loads((destination / 'summary.json').read_text())
    indices = contract['rotation_collection_indices']
    attempts = summary['attempts']
    if (summary['declared_collection_indices'] != indices or not 1 <= len(attempts) <= len(indices)
            or [item['interval'] for item in attempts] != ['interval-' + str(value) for value in indices[:len(attempts)]]):
        raise RuntimeError('The observed query opportunities differ from their frozen contract')
    proven, rotated, last_rotation = [], 0, None
    for number, attempt in zip(indices, attempts):
        if json.loads((destination / ('attempt-' + str(number) + '.json')).read_text()) != attempt:
            raise RuntimeError('A native query attempt differs from its summary')
        command = attempt['command']
        before = (json.loads((destination / ('before-' + str(number) + '.json')).read_text())
                  if command is not None else None)
        physical_overlap = (witnessed(destination, number, attempt, summary['driver']['pid'], before)
                            if command is not None else False)
        overlap = overlapping(attempt, summary['driver']['pid']) or physical_overlap
        if overlap != attempt['overlap_proven']:
            raise RuntimeError('The native query process evidence does not reproduce its overlap result')
        if command is not None and physical_overlap != attempt['physical_file_change_during_query']:
            raise RuntimeError('The physical file-change observation does not reproduce its result')
        if command is None:
            continue
        if (command != json.loads((destination / ('command-' + str(number) + '.json')).read_text())
                or command['command'] != ['journalctl', '--rotate']
                or command.get('returncode') != 0 or command.get('error')):
            raise RuntimeError('An actual during-query rotation command was unsuccessful or changed')
        for suffix in ('stdout', 'stderr'):
            path = destination / ('command-' + str(number) + '.' + suffix)
            if prepare.digest(path.read_bytes()) != command[suffix + '_sha256']:
                raise RuntimeError('An actual during-query rotation output changed')
        if (destination / ('command-' + str(number) + '.stderr')).read_bytes().strip():
            raise RuntimeError('A during-query rotation reported an unresolved diagnostic')
        after = json.loads((destination / ('after-' + str(number) + '.json')).read_text())
        rotated += rotation_files(before, after)
        interval = directory / 'collector' / attempt['interval']
        receipt = json.loads((interval / 'journal-sequence.jsonl.receipt.json').read_text())
        process = attempt['query_before']
        if (not is_sequence_query(process, summary['driver']['pid']) or
                process['arguments'] != receipt['command'] or receipt['returncode'] != 0 or receipt['stderr'].strip()
                or prepare.digest((interval / 'journal-sequence.jsonl').read_bytes()) != receipt['stdout_sha256']):
            raise RuntimeError('The observed process does not match the successful native archived query')
        result = json.loads((interval / 'result.json').read_text())
        if not (result['started']['monotonic_ns'] <= command['started']['monotonic_ns']
                <= command['finished']['monotonic_ns'] <= result['finished']['monotonic_ns']):
            raise RuntimeError('The rotation command did not occur within its actual native interval')
        last_rotation = command['finished']['monotonic_ns']
        if overlap:
            proven.append(attempt['interval'])
    if not proven:
        raise RuntimeError('No native query remained active and produced output across a real rotation')
    later = [json.loads(path.read_text()) for path in (directory / 'collector').glob('interval-*/result.json')]
    if not any(item['started']['monotonic_ns'] > last_rotation and item['coverage_complete'] for item in later):
        raise RuntimeError('A subsequent ordinary native interval was not verified after rotation')
    return {'actual_rotation': 'Passed', 'during_native_query': 'Passed',
            'proven_query_intervals': proven, 'recorded_opportunities': len(attempts),
            'rotated_file_count': rotated, 'subsequent_ordinary_collection': 'Passed'}
