"""Execute and verify real journal rotation outside native collector intervals."""

import json
import time

import basic
import journal_coverage
import prepare

POLL_SECONDS = 0.05
NANOSECONDS = 1000000000


class OutsideCollection:
    """Retain actual command, file identities and collection boundaries."""

    def __init__(self, directory, start, window, stopping):
        self.directory = directory
        self.start = start
        self.window = window
        self.stopping = stopping
        self.error = None

    def run(self):
        directory = self.directory / 'rotation'
        directory.mkdir(mode=0o700)
        try:
            begin = self.start['monotonic_ns'] + self.window[0] * NANOSECONDS
            end = self.start['monotonic_ns'] + self.window[1] * NANOSECONDS
            while time.monotonic_ns() < begin:
                if self.stopping.wait(POLL_SECONDS):
                    raise RuntimeError('Rotation was interrupted before its declared window')
            while True:
                intervals = list((self.directory / 'collector').glob('interval-*'))
                complete = [path for path in intervals if (path / 'result.json').is_file()]
                if complete and len(complete) == len(intervals):
                    break
                if self.stopping.wait(POLL_SECONDS) or time.monotonic_ns() >= end:
                    raise RuntimeError('A complete native interval was unavailable before rotation')
            previous = max(complete, key=lambda path: int(path.name.split('-')[-1]))
            collected = json.loads((previous / 'result.json').read_text())
            if not collected['coverage_complete']:
                raise RuntimeError('The preceding native collector did not prove complete coverage')
            if time.monotonic_ns() >= end:
                raise RuntimeError('Rotation missed its predeclared window')
            before = {'observed': basic.clock(), 'daemon': journal_coverage.daemon_identity(),
                      'files': journal_coverage.file_headers()}
            prepare.save(directory / 'before.json', before)
            command = basic.command(['journalctl', '--rotate'], directory / 'command')
            after = {'observed': basic.clock(), 'daemon': journal_coverage.daemon_identity(),
                     'files': journal_coverage.file_headers()}
            prepare.save(directory / 'after.json', after)
            prepare.save(directory / 'action.json', {'preceding_interval': previous.name,
                         'window_seconds': self.window, 'command': command})
            if command.get('returncode') != 0 or command.get('error'):
                raise RuntimeError('The actual journal rotation command failed')
        except Exception as error:
            self.error = str(error)
            prepare.save(directory / 'error.json', {'observed': basic.clock(), 'error': self.error})


def verify(directory, contract):
    rotation = directory / 'rotation'
    before = json.loads((rotation / 'before.json').read_text())
    after = json.loads((rotation / 'after.json').read_text())
    action = json.loads((rotation / 'action.json').read_text())
    command = json.loads((rotation / 'command.json').read_text())
    if (action['window_seconds'] != contract['rotation_window_seconds'] or action['command'] != command
            or command['command'] != ['journalctl', '--rotate']
            or command.get('returncode') != 0 or command.get('error')):
        raise RuntimeError('The actual rotation receipt does not match the declared action')
    for suffix in ('stdout', 'stderr'):
        if prepare.digest((rotation / ('command.' + suffix)).read_bytes()) != command[suffix + '_sha256']:
            raise RuntimeError('The rotation command output changed')
    if (rotation / 'command.stderr').read_bytes().strip():
        raise RuntimeError('The journal rotation command reported an unresolved diagnostic')
    first, last = contract['rotation_window_seconds']
    t0 = contract['start']['monotonic_ns']
    if not (t0 + first * NANOSECONDS <= command['started']['monotonic_ns']
            <= command['finished']['monotonic_ns'] <= t0 + last * NANOSECONDS):
        raise RuntimeError('The actual rotation occurred outside its declared window')
    if (before['daemon'] != after['daemon'] or
            not before['observed']['monotonic_ns'] <= command['started']['monotonic_ns']
            <= command['finished']['monotonic_ns'] <= after['observed']['monotonic_ns']):
        raise RuntimeError('Journal rotation identity or observation boundaries changed')
    old = {row['file_id']: row for row in before['files']}
    new = {row['file_id']: row for row in after['files']}
    populated = {key for key, value in old.items() if value['entries']}
    rotated = [key for key in populated & new.keys() if old[key]['file'] != new[key]['file']]
    if not populated <= new.keys() or not new.keys() - old.keys() or not rotated:
        raise RuntimeError('Journal file identities do not prove actual preserved rotation')
    intervals = sorted((directory / 'collector').glob('interval-*/result.json'),
                       key=lambda path: int(path.parent.name.split('-')[-1]))
    records = [(path.parent.name, json.loads(path.read_text())) for path in intervals]
    preceding = [(name, record) for name, record in records
                 if record['finished']['monotonic_ns'] <= command['started']['monotonic_ns']]
    following = [(name, record) for name, record in records
                 if record['started']['monotonic_ns'] >= command['finished']['monotonic_ns']]
    if not preceding or not following or preceding[-1][0] != action['preceding_interval']:
        raise RuntimeError('Rotation lacks successful preceding and subsequent native intervals')
    for name, record in records:
        if (record['started']['monotonic_ns'] < command['finished']['monotonic_ns']
                and record['finished']['monotonic_ns'] > command['started']['monotonic_ns']):
            raise RuntimeError('Rotation overlapped a native collector interval')
    return {'actual_rotation': 'Passed', 'outside_collection': 'Passed',
            'rotated_file_count': len(rotated), 'new_file_count': len(new.keys() - old.keys()),
            'preceding_interval': preceding[-1][0], 'subsequent_interval': following[0][0]}
