#!/usr/bin/env python3
"""Portable evidence paths, exact event timestamps and overlapping GC exports."""

import collections
import concurrent.futures
import csv
import datetime
from decimal import Decimal
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import time

COMPONENTS = ('mgmt', 'engine', 'etl', 'retrieval')
STAMP = re.compile(r'^(.*T\d{2}:\d{2}:\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})$')
PASS_STAMP = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'
                        r'(?:\.[0-9]{1,9})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])$')
SPAN = re.compile(r'^PT(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?$')
EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
JITTER_NS = 2000
JOURNAL_BINARY = '/usr/bin/journalctl'
JOURNAL_TIMEOUT = 60
JOURNAL_ROLES = ('sampler', 'abort')
JFR_EVENTS = 'jdk.GCHeapSummary,jdk.GarbageCollection,jdk.GCPhasePause,jdk.DataLoss'
JFR_TIMEOUT = 120
JFR_JAVA_OPTIONS = ('-J-XX:-UsePerfData',)
GC_EXPORTS = {'heap': ('gc-heap.csv', 'heap_events'),
              'collection': ('gc-collections.csv', 'collection_events'),
              'pause': ('gc-pauses.csv', 'pause_events')}
GC_PAYLOADS = {'heap': ('when', 'heap_bytes'), 'pause': ('name', 'duration'),
               'collection': ('name', 'cause', 'duration', 'sumOfPauses', 'longestPause')}


class JournalInterrupted(BaseException):
    """Preserve an actual collector signal and any completed unit captures."""

    def __init__(self, number):
        self.number = number
        self.groups = []


def _journal_identity(process):
    root = Path('/proc') / str(process.pid)
    try:
        stat = (root / 'stat').read_text().rsplit(')', 1)[1].split()
        return {'pid': process.pid, 'start_ticks': stat[19], 'state': stat[0],
                'exe': os.readlink(root / 'exe'),
                'uid': root.stat().st_uid,
                'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
    except FileNotFoundError:
        return {'pid': process.pid, 'ended': True}


def _write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def case_journal_units():
    import collect
    import observe

    return {'sampler': observe.SAMPLER + '.service', 'abort': collect.ABORT_UNIT}


def select_case_journal(raw, lower):
    """Validate complete native JSON records without changing their occurrences."""
    records = []
    cursors = {}

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON field')
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError('Non-finite JSON value')

    lower_ns = pass_instant(lower)
    for line in raw.decode('utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line, object_pairs_hook=unique, parse_constant=invalid_constant)
        if not isinstance(row, dict):
            raise ValueError('Journal record must be an object')
        for field in ('__CURSOR', '_BOOT_ID'):
            if not isinstance(row.get(field), str) or not row[field]:
                raise ValueError('Missing journal identity: ' + field)
        stamp = row.get('__REALTIME_TIMESTAMP')
        if not isinstance(stamp, str) or not re.fullmatch(r'[0-9]+', stamp):
            raise ValueError('Invalid native microsecond timestamp')
        cursor = row['__CURSOR']
        if cursor in cursors and cursors[cursor] != row:
            raise ValueError('Conflicting journal cursor payload')
        cursors[cursor] = row
        if int(stamp) * 1000 >= lower_ns:
            records.append(row)
    return records


def _select_journal_capture(receipt, raw, errors, lower, destination, label):
    if receipt['returncode'] == 0 and not errors and receipt.get('capture_complete'):
        try:
            rows = select_case_journal(raw, lower)
            (destination / (label + '.selected.jsonl')).write_text(
                ''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows))
            receipt.update(verdict='Passed', reason='usable_capture', selected_records=len(rows))
        except (UnicodeError, ValueError, TypeError) as error:
            receipt.update(reason='unusable_capture', error_type=type(error).__name__, error=str(error))
    _write_json(destination / (label + '.json'), receipt)
    return receipt


def capture_case_journals(observation, output, variant, native_files=(),
                          binary=JOURNAL_BINARY, timeout=JOURNAL_TIMEOUT, captures=None, query_uid=None):
    """Read the observation and capture both production unit queries separately."""
    destination = Path(output)
    if variant not in ('run-etl-fault.py', 'run-etl-fault-v2.py'):
        raise ValueError('Unknown journal caller')
    try:
        manifest = _json(observation)
        lower = manifest['started_at']
        lower_ns = pass_instant(lower)
        since = (EPOCH + datetime.timedelta(seconds=lower_ns // 1000000000)).strftime(
            '%Y-%m-%d %H:%M:%S UTC')
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
        groups = [{'role': role, 'unit': unit, 'verdict': 'Incomplete', 'reason': 'unusable_bound',
                   'launched': False, 'returncode': None, 'error_type': type(error).__name__,
                   'error': str(error)} for role, unit in case_journal_units().items()]
        _write_json(destination / 'case-journals.json', groups)
        return groups
    groups = []
    for role, unit in case_journal_units().items():
        label = 'actual-' + ('sampler' if role == 'sampler' else 'abort-unit') + '-journal'
        arguments = [str(binary)]
        for path in native_files:
            arguments += ['--file', str(path)]
        arguments += ['-u', unit, '--since', since, '--no-pager', '--all', '-o', 'json']
        receipt = {'role': role, 'unit': unit, 'actual_arguments': arguments,
                   'precise_lower_bound': lower, 'query_lower_bound': since,
                   'observation_sha256': file_digest(observation),
                   'started_at': _now(), 'started_monotonic_ns': time.monotonic_ns(),
                   'timeout_seconds': timeout, 'returncode': None, 'launched': False,
                   'verdict': 'Incomplete', 'reason': 'capture', 'capture_complete': False,
                   'source_files': {str(path): file_digest(path) for path in native_files}}
        receipt.update(source_sha256=file_digest(__file__), effective_uid=os.geteuid(),
                       python=sys.version, boot_id=Path('/proc/sys/kernel/random/boot_id').read_text().strip())
        try:
            receipt['native_binary_sha256'] = file_digest(binary)
        except OSError as error:
            receipt['binary_identity_error'] = type(error).__name__
        if captures is not None:
            saved = captures[role]
            receipt.update(saved['receipt'])
            receipt.update(role=role, unit=unit, precise_lower_bound=lower, launched=False,
                           capture_only=True, verdict='Incomplete', reason='capture',
                           actual_capture_provenance=saved['provenance'])
            raw, errors = saved['stdout'].read_bytes(), saved['stderr'].read_bytes()
            (destination / (label + '.stdout')).write_bytes(raw)
            (destination / (label + '.stderr')).write_bytes(errors)
            groups.append(_select_journal_capture(receipt, raw, errors, lower, destination, label))
            continue
        raw, errors = b'', b''
        child = None
        interrupted = None
        previous = {}

        def interrupt(number, frame):
            raise JournalInterrupted(number)

        try:
            for number in (signal.SIGINT, signal.SIGTERM):
                previous[number] = signal.signal(number, interrupt)
            child = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     user=query_uid)
            receipt.update(launched=True, process=_journal_identity(child))
            _write_json(destination / (label + '.running.json'), receipt)
            receipt['communicate_started_monotonic_ns'] = time.monotonic_ns()
            receipt['deadline_monotonic_ns'] = receipt['communicate_started_monotonic_ns'] + int(timeout * 1000000000)
            raw, errors = child.communicate(timeout=timeout)
            receipt.update(returncode=child.returncode, capture_complete=True)
        except subprocess.TimeoutExpired as error:
            raw, errors = error.stdout or b'', error.stderr or b''
            receipt.update(launched=True, timed_out=True, error_type=type(error).__name__)
            receipt['timeout_observed_monotonic_ns'] = time.monotonic_ns()
        except JournalInterrupted as error:
            interrupted = error
            receipt.update(collector_signal=error.number)
        except OSError as error:
            receipt.update(error_type=type(error).__name__, error=str(error))
        finally:
            if child is not None:
                try:
                    if child.poll() is None:
                        current = _journal_identity(child)
                        receipt['finalization_identity'] = current
                        receipt['finalization_monotonic_ns'] = time.monotonic_ns()
                        original = receipt.get('process', {})
                        if current.get('start_ticks') != original.get('start_ticks'):
                            raise RuntimeError('Query process identity is not confirmed')
                        if current.get('state') in ('T', 't'):
                            child.send_signal(signal.SIGCONT)
                        child.terminate()
                    try:
                        raw, errors = child.communicate(timeout=5)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        raw, errors = child.communicate()
                    receipt.update(returncode=child.returncode, child_ended=True,
                                   capture_complete=not (receipt.get('timed_out') or interrupted))
                except (OSError, RuntimeError) as error:
                    receipt.update(child_ended=False, finalization_error=str(error))
            (destination / (label + '.stdout')).write_bytes(raw)
            (destination / (label + '.stderr')).write_bytes(errors)
            receipt.update(finished_at=_now(), finished_monotonic_ns=time.monotonic_ns(),
                           stdout_bytes=len(raw), stderr_bytes=len(errors))
            _write_json(destination / (label + '.json'), receipt)
            for number, handler in previous.items():
                signal.signal(number, handler)
        groups.append(_select_journal_capture(receipt, raw, errors, lower, destination, label))
        _write_json(destination / 'case-journals.json', groups)
        if interrupted is not None:
            interrupted.groups = groups
            raise interrupted
        if receipt.get('child_ended') is False:
            break
    return groups


def journal_component_main(contract_path, output, caller, payload):
    """Verify frozen inputs and compare each independently usable unit capture."""
    destination = Path(output)
    result = {'verdict': 'Incomplete', 'reason': 'invocation', 'groups': []}
    status = 2
    created = False
    try:
        if not Path(contract_path).is_absolute() or not destination.is_absolute():
            raise ValueError('Absolute contract and output paths are required')
        context = _json(contract_path)
        keys = ('candidate', 'inputs', 'native', 'comparison')
        if payload['mode'] == 'check-journal-capture':
            keys += ('captures',)
        roots = [Path(context[key]['root']).resolve() for key in keys]
        destination = destination.resolve()
        if any(destination == root or root in destination.parents or destination in root.parents
               for root in roots):
            raise ValueError('Output overlaps protected inputs or tools')
        destination.mkdir(mode=0o700)
        created = True
        result['reason'] = 'integrity'
        verified = {}
        for key in keys:
            if not Path(context[key]['root']).is_absolute() or not Path(context[key]['manifest']).is_absolute():
                raise ValueError('Absolute member roots and manifests are required')
            verified[key] = _verified_members(context[key])
        candidate = verified['candidate']
        inputs = verified['inputs']
        if (context['schema'] != 1 or payload['chain'] != context['chain']
                or payload['case'] != context['case']
                or Path(__file__).resolve() != candidate / 'etl-pass/evidence.py'
                or Path(caller).resolve() != candidate / 'etl-scenarios' / Path(caller).name):
            raise ValueError('Actual caller or context differs from the candidate')
        units = case_journal_units()
        if context['unit_roles'] != units:
            raise ValueError('Declared roles differ from production units')
        expected = _json(_member(inputs, context['expectation']))
        if expected['unit_roles'] != units:
            raise ValueError('Expected roles differ from production units')
        command = context['native_command']
        if (file_digest(command['path']) != command['sha256'] or os.geteuid() != command['uid']):
            raise ValueError('Native command identity or effective UID differs')
        timeout = context.get('timeout_seconds', JOURNAL_TIMEOUT)
        if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
                or not math.isfinite(timeout) or timeout <= 0):
            raise ValueError('A finite positive query deadline is required')
        native_files = sorted(path for path in verified['native'].rglob('*') if path.is_file())
        if not native_files:
            raise ValueError('No native source members')
        result['identities'] = {'contract_sha256': file_digest(contract_path), 'python': sys.version,
                                'source': file_digest(__file__), 'caller': file_digest(caller),
                                'native_command': command, 'boot_id': Path(
                                    '/proc/sys/kernel/random/boot_id').read_text().strip()}
        observation = _member(inputs, context['observation'])
        captures = None
        if payload['mode'] == 'check-journal-capture':
            captures = {}
            capture_root = verified['captures']
            for role in JOURNAL_ROLES:
                source = context['capture_roles'][role]
                receipt = _json(_member(capture_root, source['receipt']))
                provenance = _json(_member(capture_root, source['provenance']))
                if (receipt['returncode'] != provenance['original_returncode']
                        or receipt['unit'] != units[role]
                        or file_digest(_member(capture_root, source['receipt']))
                        != provenance['native_receipt_sha256']
                        or file_digest(_member(capture_root, source['native_stdout']))
                        != provenance['native_stdout_sha256']
                        or file_digest(_member(capture_root, source['native_stderr']))
                        != provenance['native_stderr_sha256']):
                    raise ValueError('Unusable native capture provenance')
                captures[role] = {'receipt': receipt, 'provenance': provenance,
                                  'stdout': _member(capture_root, source['stdout']),
                                  'stderr': _member(capture_root, source['stderr'])}
        groups = capture_case_journals(observation, destination, Path(caller).name, native_files,
                                      command['path'], timeout, captures,
                                      command.get('query_uid'))
        for group in groups:
            result['groups'].append(group)
            role = group['role']
            if group['verdict'] != 'Passed':
                _write_json(destination / 'result.json', result)
                continue
            label = 'actual-' + ('sampler' if role == 'sampler' else 'abort-unit') + '-journal'
            config = {'format': 'jsonl', 'keys': ['__CURSOR', '_BOOT_ID'], 'timestamps': [],
                      'numbers': {'__REALTIME_TIMESTAMP': 'epoch microseconds'},
                      'required': [], 'optional': [], 'fields': None,
                      'allow_empty': expected['allow_empty'][role]}
            config_path = destination / (role + '-comparison-config.json')
            _write_json(config_path, config)
            arguments = [sys.executable, '-B', str(_member(verified['comparison'], context['comparator'])),
                         '--config', str(config_path), '--expected',
                         str(_member(inputs, expected['records'][role])), '--actual',
                         str(destination / (label + '.selected.jsonl'))]
            started = _now()
            comparison = {'actual_arguments': arguments, 'started_at': started, 'returncode': None}
            raw, errors = b'', b''
            try:
                compared = subprocess.run(arguments, capture_output=True, timeout=JOURNAL_TIMEOUT)
                raw, errors = compared.stdout, compared.stderr
                comparison['returncode'] = compared.returncode
            except (OSError, subprocess.TimeoutExpired) as error:
                raw, errors = getattr(error, 'stdout', None) or b'', getattr(error, 'stderr', None) or b''
                comparison.update(error_type=type(error).__name__, error=str(error))
            finally:
                (destination / (role + '-comparison.stdout')).write_bytes(raw)
                (destination / (role + '-comparison.stderr')).write_bytes(errors)
                comparison['finished_at'] = _now()
                _write_json(destination / (role + '-comparison.json'), comparison)
                group['comparison'] = comparison
            try:
                parsed = json.loads(raw)
                if (comparison['returncode'] not in (0, 1, 2) or errors
                        or parsed['verdict'] != {0: 'Passed', 1: 'Failed', 2: 'Incomplete'}[
                            comparison['returncode']]):
                    raise ValueError('Unusable comparison command result')
                group['verdict'] = parsed['verdict']
                group['reason'] = 'selection_comparison'
            except (KeyError, TypeError, ValueError) as error:
                group.update(verdict='Incomplete', reason='unusable_comparison', error_type=type(error).__name__)
            if (group['precise_lower_bound'] != expected['lower_bound']
                    or group['unit'] != expected['unit_roles'][role]
                    or group['query_lower_bound'] != expected['query_lower_bound']):
                group.update(verdict='Failed', reason='production_arguments')
            _write_json(destination / 'result.json', result)
        for key in keys:
            _verified_members(context[key])
        verdicts = {group['verdict'] for group in result['groups']}
        result.update(verdict='Failed' if 'Failed' in verdicts else
                      'Incomplete' if 'Incomplete' in verdicts else 'Passed', reason='completed_checks')
        status = {'Passed': 0, 'Failed': 1, 'Incomplete': 2}[result['verdict']]
    except JournalInterrupted as error:
        result['groups'] = error.groups
        result.update(verdict='Incomplete', reason='collector_interrupted', signal=error.number)
        status = 128 + error.number
    except Exception as error:
        result.update(error_type=type(error).__name__, error=str(error))
        if any(group['verdict'] == 'Failed' for group in result['groups']):
            result['verdict'], status = 'Failed', 1
    result['native_exit_status'] = status
    if created:
        _write_json(destination / 'result.json', result)
    print(json.dumps({key: result[key] for key in ('verdict', 'reason', 'native_exit_status')},
                     sort_keys=True))
    return status


def timestamp_ns(value):
    match = STAMP.fullmatch(value)
    if not match or len(match[2] or '') > 9:
        raise RuntimeError('Invalid timezone-aware event timestamp')
    instant = datetime.datetime.fromisoformat(match[1] + match[3].replace('Z', '+00:00'))
    delta = instant - EPOCH
    return (delta.days * 86400 + delta.seconds) * 1000000000 + int((match[2] or '').ljust(9, '0'))


class PassCheckError(RuntimeError):
    """A declared pass-check outcome with known or unavailable match count."""

    def __init__(self, verdict, reason, count=None, selected=None):
        super().__init__(reason)
        self.result = {'verdict': verdict, 'reason': reason, 'match_count': count,
                       'selected_pass': selected}


def pass_instant(value):
    if not isinstance(value, str) or not PASS_STAMP.fullmatch(value):
        raise ValueError('Invalid timezone-aware pass timestamp or precision')
    return timestamp_ns(value)


def checked_pass(source, target, identity, began, ended):
    """Read the native pass source and verify one declared successful pass."""
    import evaluate
    import focused

    try:
        if (type(target['transition']) is not int or type(target['cadence']) is not int
                or target['transition'] < 0 or target['cadence'] <= 0
                or any(not isinstance(identity[key], str) or not identity[key]
                       for key in ('boot_id', 'invocation_id'))):
            raise ValueError('Invalid declared pass identity')
        planned = pass_instant(target['planned_at'])
        if pass_instant(began) > pass_instant(ended):
            raise ValueError('Invalid comparison interval')
        records = evaluate.pass_records(Path(source))
        for row in records:
            if (type(row['transition']) is not int or type(row['cadence']) is not int
                    or not isinstance(row['invocation_id'], str) or not row['invocation_id']):
                raise ValueError('Missing native pass identity')
            for key in ('plannedAt', 'startedAt', 'endedAt'):
                pass_instant(row[key])
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
        raise PassCheckError('Incomplete', 'unusable_pass_input') from error
    matches = [row for row in records if row['transition'] == target['transition']
               and row['cadence'] == target['cadence']
               and row['invocation_id'] == identity['invocation_id']
               and pass_instant(row['plannedAt']) == planned]
    if len(matches) != 1:
        raise PassCheckError('Failed', 'pass_count', len(matches))
    selected = matches[0]
    try:
        for key in ('pvCount', 'jobsRun', 'jobsFailed', 'jobsAborted', 'jobsSkipped',
                    'streamsDeletedForSpace'):
            if not re.fullmatch(r'[0-9]+', selected[key]):
                raise ValueError('Invalid pass execution count')
        if any(selected[key] not in ('true', 'false') for key in ('overrun', 'aborted')):
            raise ValueError('Invalid pass execution flag')
    except (KeyError, TypeError, ValueError) as error:
        raise PassCheckError('Incomplete', 'unusable_execution_fields', 1, selected) from error
    try:
        focused.successful_pass(selected)
    except RuntimeError as error:
        raise PassCheckError('Failed', 'execution_contract', 1, selected) from error
    if not (pass_instant(began) <= pass_instant(selected['startedAt'])
            <= pass_instant(selected['endedAt']) <= pass_instant(ended)):
        raise PassCheckError('Failed', 'pass_interval', 1, selected)
    return selected


def file_digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()


def _json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON field')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def _member(root, name):
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts or str(relative) != name:
        raise ValueError('Invalid evidence member path')
    result = root / relative
    if result.is_symlink() or root not in result.resolve().parents:
        raise ValueError('Evidence member escapes its declared root')
    return result


def _verified_members(specification):
    root = Path(specification['root'])
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Missing or linked evidence root')
    root = root.resolve()
    manifest = Path(specification['manifest'])
    if file_digest(manifest) != specification['sha256']:
        raise ValueError('Member manifest identity mismatch')
    members = _json(manifest)['members']
    if not isinstance(members, dict) or not members:
        raise ValueError('Empty member manifest')
    actual = set()
    for candidate in root.rglob('*'):
        if candidate.is_symlink():
            raise ValueError('Linked evidence member')
        if candidate.is_file():
            actual.add(str(candidate.relative_to(root)))
    if actual != set(members):
        raise ValueError('Evidence membership differs from its frozen manifest')
    for name, expected in members.items():
        if file_digest(_member(root, name)) != expected:
            raise ValueError('Evidence member checksum mismatch')
    return root


def _reference(root, reference):
    value = _json(_member(root, reference['path']))
    for field in reference['field']:
        value = value[field]
    return value


def retained_pass_main(contract_path, output, caller):
    """Verify separate original/candidate identities and assess retained inputs."""
    destination = Path(output).resolve()
    result = {'verdict': 'Incomplete', 'reason': 'invocation', 'checks': []}
    native = 2
    created = False
    context = None
    try:
        context = _json(contract_path)
        roots = [Path(context[key]['root']).resolve()
                 for key in ('original', 'candidate', 'inputs')]
        if any(destination == root or root in destination.parents for root in roots):
            raise ValueError('Output overlaps protected inputs or tools')
        destination.mkdir(mode=0o700)
        created = True
        result['reason'] = 'integrity'
        if context['schema'] != 1 or not context['checks']:
            raise ValueError('Invalid retained-pass contract')
        original = _verified_members(context['original'])
        candidate = _verified_members(context['candidate'])
        inputs = _verified_members(context['inputs'])
        if (Path(__file__).resolve().parent != candidate
                or file_digest(caller) != context['callers'][Path(caller).name]):
            raise ValueError('Actual checker source differs from its declared candidate')
        import contract
        original_hashes = contract.verify_bundle(original)
        candidate_hashes = contract.verify_bundle(candidate)
        result['identities'] = {'contract_sha256': file_digest(contract_path),
                                'original_bundle_sha256': file_digest(original / 'bundle.json'),
                                'candidate_bundle_sha256': file_digest(candidate / 'bundle.json'),
                                'python': sys.version, 'original_files': original_hashes,
                                'candidate_files': candidate_hashes,
                                'input_manifest_sha256': context['inputs']['sha256']}
        names = set()
        for check in context['checks']:
            if check['name'] in names:
                raise ValueError('Duplicate retained-pass check name')
            names.add(check['name'])
            try:
                declaration = _json(_member(inputs, check['declaration']))
                observation = _json(_member(inputs, check['observation']))
                if (declaration['tool_hashes'] != original_hashes
                        or observation['tool_hashes'] != original_hashes
                        or declaration['case'] != check['case']
                        or declaration['chain'] != check['chain']):
                    raise PassCheckError('Incomplete', 'observation_binding')
                identity = _reference(inputs, check['identity'])
                began = _reference(inputs, check['begin'])
                ended = _reference(inputs, check['end'])
                selected = checked_pass(_member(inputs, check['passes']),
                                        declaration['target_native_sts_pass'], identity, began, ended)
                outcome = {'verdict': 'Passed', 'reason': 'matched_pass', 'match_count': 1,
                           'selected_pass': selected}
            except PassCheckError as error:
                outcome = error.result
            except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
                outcome = {'verdict': 'Incomplete', 'reason': 'unusable_check_input',
                           'match_count': None, 'selected_pass': None,
                           'error_type': type(error).__name__}
            result['checks'].append({'name': check['name'], **outcome})
        verdicts = {row['verdict'] for row in result['checks']}
        result['verdict'] = ('Failed' if 'Failed' in verdicts else
                             'Incomplete' if 'Incomplete' in verdicts else 'Passed')
        result['reason'] = 'completed_checks'
        native = {'Passed': 0, 'Failed': 1, 'Incomplete': 2}[result['verdict']]
        for key in ('original', 'candidate', 'inputs'):
            _verified_members(context[key])
    except Exception as error:
        result.update(verdict='Incomplete', error_type=type(error).__name__)
        native = 2
    result['native_exit_status'] = native
    if created:
        (destination / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: result[key] for key in ('verdict', 'reason', 'native_exit_status')},
                     sort_keys=True))
    return native


def duration_ns(value, exact=False):
    match = SPAN.fullmatch(value)
    if not match or not any(match.groups()):
        raise RuntimeError('Invalid JFR duration')
    nanos = sum(Decimal(part or '0') * factor for part, factor in
                zip(match.groups(), (3600, 60, 1))) * 1000000000
    if exact and nanos != nanos.to_integral_value():
        raise RuntimeError('JFR duration is not an exact integer nanosecond value')
    return int(nanos)


def path(out, value):
    candidate = Path(value)
    if not candidate.is_absolute():
        resolved = (out / candidate).resolve()
        if out.resolve() not in resolved.parents:
            raise RuntimeError('Evidence path escapes its input directory')
        return resolved
    if 'raw' in candidate.parts:
        index = candidate.parts.index('raw')
        return path(out, str(Path(*candidate.parts[index:])))
    raise RuntimeError('Absolute evidence path cannot be rebased')


def load(path):
    return json.loads(path.read_text())


def rows(out, name, required=True):
    source = out / name
    if not source.exists() and not required:
        return []
    with source.open(newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise RuntimeError('Missing CSV header: ' + name)
        return list(reader)


def deduplicate(rows, kind):
    identity = ('component', 'pid', 'gc_id') + (('when',) if kind == 'heap' else ())
    payload = {'heap': ('heap_bytes',), 'pause': ('name', 'duration'),
               'collection': ('name', 'cause', 'duration', 'sumOfPauses', 'longestPause')}[kind]
    groups = collections.defaultdict(list)
    for row in rows:
        if not row.get('gc_id'):
            raise RuntimeError('GC event lacks identity')
        key = tuple(row[field] for field in identity)
        if kind == 'pause':
            key += (row['name'], row.get('phase_identity', 'jdk.GCPhasePause'))
        groups[key].append(row)
    result, max_jitter = [], 0
    for group in groups.values():
        ordered = sorted(group, key=lambda row: timestamp_ns(row['ts']))
        if kind != 'pause' and len({tuple(row[field] for field in payload) for row in ordered}) != 1:
            raise RuntimeError('Conflicting GC payloads')
        clusters = []
        for row in ordered:
            instant = timestamp_ns(row['ts'])
            if not clusters or instant - clusters[-1][0] > JITTER_NS:
                clusters.append([instant, [row]])
            else:
                clusters[-1][1].append(row)
        if kind != 'pause' and len(clusters) != 1:
            raise RuntimeError('Unsupported GC timestamp variation')
        for first, cluster in clusters:
            if len({tuple(row[field] for field in payload) for row in cluster}) != 1:
                raise RuntimeError('Ambiguous GC pause identity or conflicting payload')
            max_jitter = max(max_jitter, timestamp_ns(cluster[-1]['ts']) - first)
            result.append(cluster[0])
    result.sort(key=lambda row: (timestamp_ns(row['ts']), row['component'], row['pid'], row['gc_id']))
    return result, {'raw_events': len(rows), 'unique_events': len(result),
                    'duplicates': len(rows) - len(result), 'maximum_jitter_ns': max_jitter,
                    'maximum_cluster_span_ns': JITTER_NS}


def recording_arguments(parser):
    parser.add_argument('--recordings-only', action='store_true', help='Verify retained JFR exports only')
    parser.add_argument('--recording-component', choices=COMPONENTS, action='append')
    parser.add_argument('--jfr-binary', type=Path, help='Native JDK jfr executable')
    parser.add_argument('--jfr-output', type=Path, help='New directory for native command evidence')


def recording_options(args, parser):
    if args.recording_component and not args.recordings_only:
        parser.error('--recording-component requires --recordings-only')
    return {'components': args.recording_component or COMPONENTS,
            'jfr_binary': args.jfr_binary, 'destination': args.jfr_output}


def recording_terminal(out):
    terminals = [out / name for name in ('shutdown.json', 'abort.json') if (out / name).is_file()]
    if len(terminals) != 1:
        raise ValueError('Exactly one terminal record is required')
    return _json(terminals[0])


def _gc_csv(out, filename):
    with (out / filename).open(newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError('Missing or duplicate CSV header')
        result = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in result):
        raise ValueError('Invalid CSV row width')
    return result


def _gc_record(row, kind, identity):
    result = {**identity, 'kind': kind, 'ts': row['ts'], 'gc_id': str(int(row['gc_id']))}
    pass_instant(row['ts'])
    for field in GC_PAYLOADS[kind]:
        value = row[field]
        if field == 'heap_bytes':
            value = int(value)
        elif field in ('duration', 'sumOfPauses', 'longestPause'):
            value = duration_ns(value, exact=True)
        elif not isinstance(value, str) or not value:
            raise ValueError('Missing GC payload')
        result[field] = value
    if kind == 'pause':
        result['phase_identity'] = row.get('phase_identity', 'jdk.GCPhasePause')
    return result


def _gc_counter(records):
    return collections.Counter(json.dumps({**row, 'ts': pass_instant(row['ts'])}, sort_keys=True)
                               for row in records)


def _gc_jsonl(target, records):
    with target.open('w') as stream:
        for row in records:
            stream.write(json.dumps(row, sort_keys=True) + '\n')


def _native_gc(recorded, component, identity, decoder, destination):
    """Retain the real decoder's bytes and status before interpreting its events."""
    destination.mkdir()
    argv = [str(decoder), *JFR_JAVA_OPTIONS, 'print', '--json', '--events', JFR_EVENTS, str(recorded)]
    began, monotonic = _now(), time.monotonic()
    receipt = {'argv': argv, 'cwd': str(Path.cwd()), 'started_at': began,
               'input_sha256': file_digest(recorded), 'decoder_sha256': file_digest(decoder)}
    with (destination / 'stdout').open('wb') as stdout, (destination / 'stderr').open('wb') as stderr:
        try:
            native = subprocess.run(argv, stdout=stdout, stderr=stderr, timeout=JFR_TIMEOUT)
            receipt['returncode'] = native.returncode
        except (OSError, subprocess.TimeoutExpired) as error:
            receipt.update(returncode=None, error=type(error).__name__)
    receipt.update(finished_at=_now(), elapsed_seconds=time.monotonic() - monotonic)
    _write_json(destination / 'command.json', receipt)
    if receipt['returncode'] != 0:
        raise ValueError('Native JFR decode unavailable')
    decoded = _json(destination / 'stdout')['recording']['events']
    result = {kind: [] for kind in GC_EXPORTS}
    loss = 0
    for event in decoded:
        if event['type'] == 'jdk.DataLoss':
            loss += 1
            continue
        kind = {'jdk.GCHeapSummary': 'heap', 'jdk.GarbageCollection': 'collection',
                'jdk.GCPhasePause': 'pause'}[event['type']]
        values = event['values']
        row = {**values, 'ts': values['startTime'], 'gc_id': values['gcId']}
        if kind == 'heap':
            row['heap_bytes'] = values['heapUsed']
        result[kind].append(_gc_record(row, kind, identity))
    return result, loss


def compare_recordings(out, terminal=None, components=COMPONENTS, jfr_binary=None, destination=None):
    """Compare exact export occurrences within one proven JVM lifetime per component.

    Snapshot overlap belongs to the raw export population. The final append is
    compared separately with the final recording; observation deduplication has
    its own population and never removes occurrences from this comparison.
    """
    out = Path(out).resolve()
    result = {'verdict': 'Incomplete', 'failed_assertions': [], 'missing_coverage': [], 'components': {}}
    failures, missing = result['failed_assertions'], result['missing_coverage']
    try:
        if destination is None:
            destination = Path(tempfile.mkdtemp(prefix='etl-jfr-'))
        else:
            destination = Path(destination).resolve()
            if destination == out or out in destination.parents or destination in out.parents:
                raise ValueError('JFR output overlaps input')
            destination.mkdir(parents=True, exist_ok=False)
        result['evidence_directory'] = str(destination)
        terminal = recording_terminal(out) if terminal is None else terminal
        manifest = _json(out / 'observation.json')
        if terminal['observation'] != manifest:
            failures.append('jfr_terminal_manifest_mismatch')
        if not terminal['boot_unchanged']:
            failures.append('jfr_boot_changed')
        if not isinstance(manifest.get('boot_id'), str) or not manifest['boot_id']:
            raise ValueError('Missing boot identity')
        processes = _gc_csv(out, 'processes.csv')
        state = _json(out / 'state.json')
        samples = [_json(source) for source in sorted((out / 'raw').glob('*/sample.json'))]
        decoder = Path(jfr_binary or shutil.which('jfr') or '/usr/lib/jvm/java-21-openjdk/bin/jfr').resolve()
        result['decoder_sha256'] = file_digest(decoder)
        exports, export_errors = {}, {}
        for kind, (filename, _) in GC_EXPORTS.items():
            try:
                exports[kind] = _gc_csv(out, filename)
                if any(row.get('component') not in COMPONENTS or not row.get('pid') for row in exports[kind]):
                    failures.append('jfr_export_identity_' + kind)
            except (OSError, ValueError, csv.Error) as error:
                export_errors[kind] = type(error).__name__

        def compare_component(component):
            failed, absent = [], []
            summary = {'failed_assertions': failed, 'missing_coverage': absent, 'kinds': {}}
            def fail(label):
                failed.append('jfr_' + component + '_' + label)
            def unknown(label):
                absent.append('jfr_' + component + '_' + label)
            try:
                declared = manifest['jvm_identity'][component]
                pid, start = str(int(declared['pid'])), int(declared['start'])
                if int(pid) <= 0 or start < 0:
                    raise ValueError('Invalid process identity')
                identity = {'component': component, 'boot_id': manifest['boot_id'], 'pid': pid, 'start': start}
                summary['identity'] = identity
                same = [row for row in processes if row['name'] == component and row['pid'] == pid]
                starts = {int(row['start']) for row in same}
                if len(starts) > 1:
                    unknown('ambiguous_pid_reuse')
                    return summary
                if not starts:
                    unknown('process_evidence')
                    return summary
                if starts != {start}:
                    fail('process_start')
                    return summary
                final_state = state['processes'][component]
                if str(final_state['pid']) != pid or int(final_state['start']) != start:
                    fail('final_process_identity')
                recording = terminal['complete_gc_recordings'][component]
                if str(recording['pid']) != pid:
                    fail('recording_pid')
                    return summary
                if recording.get('coverage_complete') is not True:
                    unknown('complete_recording_coverage')
                expected_times = {pass_instant(row['ts']) for row in same}
                available_times = {pass_instant(sample['observed_at']) for sample in samples
                                   if sample.get('sample_kind') == 'full'}
                if expected_times - available_times:
                    unknown('snapshot_metadata')
                captures = []
                for sample in samples:
                    entry = sample.get('gc', {}).get(component)
                    if entry and str(entry['pid']) == pid:
                        captures.append(entry)
                    elif pass_instant(sample['observed_at']) in expected_times:
                        unknown('snapshot_metadata')
                captures.append(recording)
                raw_expected = {kind: [] for kind in GC_EXPORTS}
                native_final = None
                complete = not absent
                seen = set()
                component_out = destination / component
                component_out.mkdir()
                for index, capture in enumerate(captures):
                    try:
                        recorded = path(out, capture['recording_path'])
                        if recorded in seen:
                            fail('duplicate_snapshot')
                        seen.add(recorded)
                        if recorded.stat().st_size != capture['recording_bytes'] or file_digest(recorded) != capture['recording_sha256']:
                            fail('recording_integrity')
                            complete = False
                            continue
                        dump = (recorded.parent / (component + '-jfr-dump.txt')).read_text().splitlines()
                        if not dump or dump[0].strip() != pid + ':':
                            fail('dump_identity')
                        native, loss = _native_gc(recorded, component, identity, decoder,
                                                  component_out / ('capture-' + str(index)))
                        if loss or capture['data_loss_events'] != loss:
                            fail('data_loss')
                        for kind, (_, field) in GC_EXPORTS.items():
                            if capture[field] != len(native[kind]):
                                fail('declared_' + kind + '_count')
                            raw_expected[kind].extend(native[kind])
                        if index == len(captures) - 1:
                            native_final = native
                    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
                        unknown('capture_' + str(index) + '_' + type(error).__name__)
                        complete = False
                summary['captures'] = len(captures)
                for kind in GC_EXPORTS:
                    try:
                        if kind in export_errors:
                            raise ValueError(export_errors[kind])
                        own = [row for row in exports[kind] if row['component'] == component]
                        selected = [_gc_record(row, kind, identity) for row in own if row['pid'] == pid]
                        summary['kinds'][kind] = {'raw_events': len(selected),
                            'earlier_process_events': sum(row['pid'] != pid for row in own),
                            'native_raw_events': len(raw_expected[kind]),
                            'native_final_events': len(native_final[kind]) if native_final else None}
                        _gc_jsonl(component_out / (kind + '-raw-actual.jsonl'), selected)
                        _gc_jsonl(component_out / (kind + '-raw-expected.jsonl'), raw_expected[kind])
                        if complete and _gc_counter(selected) != _gc_counter(raw_expected[kind]):
                            fail(kind + '_raw_occurrences')
                        if native_final is not None:
                            count = len(native_final[kind])
                            final = selected[-count:] if count else []
                            _gc_jsonl(component_out / (kind + '-final-actual.jsonl'), final)
                            _gc_jsonl(component_out / (kind + '-final-expected.jsonl'), native_final[kind])
                            if _gc_counter(final) != _gc_counter(native_final[kind]):
                                fail(kind + '_final_events')
                    except (ValueError, TypeError, KeyError, RuntimeError) as error:
                        unknown(kind + '_export_' + type(error).__name__)
            except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
                unknown('identity_' + type(error).__name__)
            return summary

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(COMPONENTS)) as pool:
            summaries = pool.map(compare_component, components)
            for component, summary in zip(components, summaries):
                summary['verdict'] = ('Failed' if summary['failed_assertions'] else
                                      'Incomplete' if summary['missing_coverage'] else 'Passed')
                result['components'][component] = summary
                failures.extend(summary['failed_assertions'])
                missing.extend(summary['missing_coverage'])
    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
        missing.append('jfr_required_input_' + type(error).__name__)
    result['failed_assertions'] = sorted(set(failures))
    result['missing_coverage'] = sorted(set(missing))
    result['verdict'] = 'Failed' if failures else 'Incomplete' if missing else 'Passed'
    return result
