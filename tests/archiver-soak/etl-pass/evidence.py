#!/usr/bin/env python3
"""Portable evidence paths, exact event timestamps and overlapping GC exports."""

import collections
import csv
import datetime
from decimal import Decimal
import json
from pathlib import Path
import re

COMPONENTS = ('mgmt', 'engine', 'etl', 'retrieval')
STAMP = re.compile(r'^(.*T\d{2}:\d{2}:\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})$')
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
