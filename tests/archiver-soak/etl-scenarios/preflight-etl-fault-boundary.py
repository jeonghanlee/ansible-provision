"""Verify a declared systemd filesystem boundary before applying it to the sampler."""

import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

assert ROLE == 'etl'
CHAIN, CASE = PAYLOAD['chain'], PAYLOAD['case']
assert CHAIN in ('shortened', 'default') and CASE in ('E3', 'E4')
TOOLS = Path('/usr/local/share/etl-soak')
ROOT = Path('/var/lib/etl-negative-cases') / (CHAIN + '-' + CASE)
assert ROOT.exists() and not (ROOT / 'fault-sampler.json').exists()
sys.path.insert(0, str(TOOLS))
import contract
import focused
import observe
import pass_source

os.umask(0o077)
assert not (observe.OUT / 'observation.json').exists()
hashes = contract.verify_bundle(TOOLS)
identity = focused.identity()
assert all(pass_source.configured(row['pid']) for row in identity['jvms'].values())
journalctl = Path(shutil.which('journalctl')).resolve()
assert journalctl == Path('/usr/bin/journalctl') and journalctl.is_file()
paths = [journalctl]
files = [pass_source.INSTALL / component / 'logs' / pass_source.FILENAME for component in focused.COMPONENTS]
if CASE == 'E4':
    paths.extend(path.parent for path in files)
declared = {'chain': CHAIN, 'case': CASE, 'journalctl': str(journalctl),
            'tool_hashes': hashes, 'inaccessible_paths': list(map(str, paths))}
(ROOT / 'fault-sampler.json').write_text(json.dumps(declared, indent=2))
source = base64.b64decode(PAYLOAD['wrapper_source_base64'], validate=True)
assert hashlib.sha256(source).hexdigest() == PAYLOAD['wrapper_source_sha256']
wrapper = ROOT / 'fault-sampler.py'
wrapper.write_bytes(source)
wrapper.chmod(0o600)
before = {}
for component, path in zip(focused.COMPONENTS, files):
    destination = ROOT / ('preflight-file-before-' + component + '.jsonl')
    rows = pass_source.read(component, destination)
    assert rows
    before[component] = destination
unit = 'etl-negative-fs-preflight-' + CHAIN + '-' + CASE + '.service'
arguments = ['systemd-run', '--wait', '--unit', unit, '--property=Type=oneshot',
             '--property=UMask=0077', '--property=TimeoutStartSec=60s',
             '--property=InaccessiblePaths=' + ' '.join(map(str, paths)),
             '/usr/bin/python3', '-B', str(wrapper), str(ROOT / 'fault-sampler.json'), '--probe-only']
actual = subprocess.run(arguments, capture_output=True, timeout=90)
(ROOT / 'boundary-preflight.stdout').write_bytes(actual.stdout)
(ROOT / 'boundary-preflight.stderr').write_bytes(actual.stderr)
assert actual.returncode == 0, 'The real filesystem boundary preflight failed'
probes = list((ROOT / 'namespace-probes').glob('*/receipt.json'))
assert len(probes) == 1
probe = json.loads(probes[0].read_text())
assert probe['mount_namespace'] != os.readlink('/proc/self/ns/mnt')
assert all(row['available'] == (CASE == 'E3') for row in probe['files'].values())
assert focused.identity() == identity and contract.verify_bundle(TOOLS) == hashes
for component in focused.COMPONENTS:
    assert pass_source.read(component, ROOT / ('preflight-file-after-' + component + '.jsonl'), before[component])
properties = subprocess.check_output(['systemctl', 'show', unit, '-p', 'MainPID', '-p', 'Result',
                                      '-p', 'InaccessiblePaths', '-p', 'InvocationID'], text=True)
(ROOT / 'boundary-preflight-unit.txt').write_text(properties)
assert 'MainPID=0\n' in properties and 'Result=success\n' in properties
record = {'chain': CHAIN, 'case': CASE, 'actual_boundary_preflight': 'Passed',
          'sampler_collection_executed_by_preflight': False,
          'native_collector_unchanged': True, 'actual_identity_unchanged': identity,
          'wrapper_source_sha256': PAYLOAD['wrapper_source_sha256'],
          'journalctl_denied_in_probe_namespace': True,
          'file_availability_in_probe_namespace': CASE == 'E3',
          'all_files_available_outside_probe_namespace': True,
          'observed_at': focused.now()}
(ROOT / 'boundary-preflight.json').write_text(json.dumps(record, indent=2))
print(json.dumps({key: value for key, value in record.items() if key != 'actual_identity_unchanged'}, sort_keys=True))
