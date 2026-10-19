#!/usr/bin/env python3
"""Portable evidence paths, exact event timestamps and overlapping GC exports."""

import collections
import csv
import datetime
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

COMPONENTS = ('mgmt', 'engine', 'etl', 'retrieval')
STAMP = re.compile(r'^(.*T\d{2}:\d{2}:\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})$')
PASS_STAMP = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'
                        r'(?:\.[0-9]{1,9})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])$')
SPAN = re.compile(r'^PT(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?$')
EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
JITTER_NS = 2000


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


def duration_ns(value):
    match = SPAN.fullmatch(value)
    if not match or not any(match.groups()):
        raise RuntimeError('Invalid JFR duration')
    return int(sum(Decimal(part or '0') * factor for part, factor in
                   zip(match.groups(), (3600, 60, 1))) * 1000000000)


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
