#!/usr/bin/env python3
"""Record actual namespace access and execute the unchanged native collector."""

import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')
INSTANCES = ('mgmt', 'engine', 'etl', 'retrieval')
CONFIGURATION = Path(sys.argv[1])
configuration = json.loads(CONFIGURATION.read_text())
assert configuration['case'] in ('E3', 'E4')
assert configuration['chain'] in ('shortened', 'default')
case = Path('/var/lib/etl-negative-cases') / (configuration['chain'] + '-' + configuration['case'])
assert CONFIGURATION == case / 'fault-sampler.json'
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
root = case / 'namespace-probes' / stamp
root.mkdir(parents=True, mode=0o700)
sys.path.insert(0, str(TOOLS))
import contract
hashes = contract.verify_bundle(TOOLS)
assert hashes == configuration['tool_hashes']
record = {'case': configuration['case'], 'chain': configuration['chain'],
          'pid': os.getpid(), 'mount_namespace': os.readlink('/proc/self/ns/mnt'),
          'probe_only': len(sys.argv) == 3 and sys.argv[2] == '--probe-only',
          'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'native_collector_sha256': hashes['collect.py'], 'files': {}}
arguments = [configuration['journalctl'], '--no-pager', '-n', '1', '-o', 'json']
try:
    actual = subprocess.run(arguments, capture_output=True, timeout=10)
    (root / 'journal.stdout').write_bytes(actual.stdout)
    (root / 'journal.stderr').write_bytes(actual.stderr)
    record['journal_query'] = {'returncode': actual.returncode, 'actual_command': arguments}
    assert actual.returncode != 0
except OSError as error:
    record['journal_query'] = {'error_type': type(error).__name__, 'errno': error.errno,
                               'actual_command': arguments}
    assert error.errno in (1, 2, 13)
for component in INSTANCES:
    path = Path('/opt/epicsarchiverap-maven') / component / 'logs/etl-validation.jsonl'
    try:
        with path.open('rb') as stream:
            metadata = os.fstat(stream.fileno())
            data = stream.read(1)
        record['files'][component] = {'available': True, 'device': metadata.st_dev,
                                      'inode': metadata.st_ino, 'size': metadata.st_size,
                                      'one_byte_sha256': hashlib.sha256(data).hexdigest()}
        assert configuration['case'] == 'E3'
    except OSError as error:
        record['files'][component] = {'available': False, 'error_type': type(error).__name__, 'errno': error.errno}
        assert configuration['case'] == 'E4' and error.errno in (1, 2, 13, 20)
native = ['/usr/bin/python3', '-B', str(TOOLS / 'collect.py'), str(OUT), str(TOOLS / 'pvs-all.csv')]
record['native_exec_arguments'] = native
(root / 'receipt.json').write_text(json.dumps(record, indent=2))
if len(sys.argv) == 3 and sys.argv[2] == '--probe-only':
    raise SystemExit(0)
assert len(sys.argv) == 2
os.execv(native[0], native)
