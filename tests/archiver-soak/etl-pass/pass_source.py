#!/usr/bin/env python3
"""Preserve actual appliance file events and normalize their observed source identities."""

import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import time
import xml.etree.ElementTree as ET

INSTALL = Path('/opt/epicsarchiverap-maven')
FILENAME = 'etl-validation.jsonl'
APPENDER = 'IndependentEtlEvidence'
PATTERN = ('{"source":"appliance-file","time_millis":%d{UNIX_MILLIS},"pid":"%pid",'
           '"invocation_id":"${env:INVOCATION_ID}","message":"%enc{%m}{JSON}",'
           '"throwable":"%enc{%xEx}{JSON}"}%n')


def configure(tree):
    appenders, root = tree.find('Appenders'), tree.find('Loggers/Root')
    if appenders is None or root is None or any(row.get('name') == APPENDER for row in appenders):
        raise RuntimeError('Unexpected independent application file configuration')
    target = ET.SubElement(appenders, 'File', name=APPENDER,
                           fileName='${sys:catalina.base}/logs/' + FILENAME,
                           append='true', immediateFlush='true', bufferedIo='false')
    ET.SubElement(target, 'PatternLayout', pattern=PATTERN, charset='UTF-8', alwaysWriteExceptions='false')
    ET.SubElement(root, 'AppenderRef', ref=APPENDER)


def configured(pid):
    environment = dict(item.split(b'=', 1) for item in Path('/proc/' + str(pid) + '/environ').read_bytes().split(b'\0')
                       if b'=' in item)
    value = environment.get(b'LOG4J_CONFIGURATION_FILE')
    if not value:
        return False
    tree = ET.fromstring(Path(os.fsdecode(value)).read_bytes())
    return any(row.get('name') == APPENDER for row in tree.findall('Appenders/File'))


def read(component, destination, previous=None):
    path = INSTALL / component / 'logs' / FILENAME
    started = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'monotonic_ns': time.monotonic_ns()}
    if path.is_symlink():
        raise RuntimeError('An application evidence file cannot be a symlink')
    with path.open('rb') as stream:
        before = os.fstat(stream.fileno())
        data = stream.read(before.st_size)
        after = os.fstat(stream.fileno())
    if (len(data) != before.st_size or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
            or after.st_size < before.st_size):
        raise RuntimeError('Application evidence file changed identity or shrank during capture')
    receipt_path = destination.with_suffix(destination.suffix + '.receipt.json')
    prior = destination if destination.exists() or receipt_path.exists() else previous
    if prior is not None:
        prior = Path(prior)
        captured = prior.read_bytes()
        receipt = json.loads(prior.with_suffix(prior.suffix + '.receipt.json').read_text())
        if (receipt['sha256'] != hashlib.sha256(captured).hexdigest()
                or (receipt['device'], receipt['inode']) != (before.st_dev, before.st_ino)
                or len(data) < len(captured) or data[:len(captured)] != captured):
            raise RuntimeError('Previously captured application file bytes or identity changed')
    destination.write_bytes(data)
    complete = data[:data.rfind(b'\n') + 1]
    rows, offset = [], 0
    for line in complete.splitlines(keepends=True):
        event = json.loads(line)
        if (event.get('source') != 'appliance-file' or type(event.get('time_millis')) is not int
                or event['time_millis'] <= 0 or not re.fullmatch(r'[1-9][0-9]*', event.get('pid', ''))
                or not re.fullmatch(r'[0-9a-f]{32}', event.get('invocation_id', ''))
                or not isinstance(event.get('message'), str) or not isinstance(event.get('throwable'), str)):
            raise RuntimeError('An actual application event lacks its required source fields')
        rows.append({'__CURSOR': 'file:' + str(before.st_dev) + ':' + str(before.st_ino) + ':' + str(offset),
                     '__REALTIME_TIMESTAMP': str(event['time_millis'] * 1000),
                     '_PID': event['pid'], '_SYSTEMD_INVOCATION_ID': event['invocation_id'],
                     'MESSAGE': event['message'], 'EXCEPTION': event['throwable'],
                     '_TRANSPORT': 'appliance-file', 'timestamp_precision': 'milliseconds',
                     'source_file': str(path), 'source_offset': offset,
                     'source_line_sha256': hashlib.sha256(line).hexdigest()})
        offset += len(line)
    receipt = {'source': 'appliance-file', 'path': str(path), 'device': before.st_dev, 'inode': before.st_ino,
               'bytes': len(data), 'complete_bytes': len(complete), 'trailing_bytes': len(data) - len(complete),
               'sha256': hashlib.sha256(data).hexdigest(), 'records': len(rows), 'started': started,
               'finished': {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            'monotonic_ns': time.monotonic_ns()}}
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    return rows
