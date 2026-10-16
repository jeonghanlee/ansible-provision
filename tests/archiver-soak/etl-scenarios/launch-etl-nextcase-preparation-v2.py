"""Start one fresh native preparation after the preceding case was preserved."""

import base64
import hashlib
import json
from pathlib import Path
import subprocess

assert ROLE == PAYLOAD['role'] == 'etl'
CHAIN, CASE, PREVIOUS = PAYLOAD['chain'], PAYLOAD['case'], PAYLOAD['previous_case']
assert CHAIN in ('shortened', 'default')
assert (PREVIOUS, CASE) in (('E1', 'E2'), ('E2', 'E3'), ('E3', 'E4'))
root = Path('/var/lib/etl-negative-orchestration')
reset = Path('/var/lib/etl-negative-resets') / (CHAIN + '-' + PREVIOUS + '-to-' + CASE) / 'result.json'
if 'reset_result' in PAYLOAD:
    reset = Path(PAYLOAD['reset_result'])
    assert CHAIN == 'shortened' and CASE == 'E2'
    assert reset == Path('/var/lib/etl-negative-resets/shortened-E1-to-E2-completion-001/result.json')
assert json.loads(reset.read_text())['state'] == 'Ready for native fresh instruments'
assert not Path('/var/lib/etl-soak/observation.json').exists()
assert not Path('/var/lib/etl-negative-preparation-' + CHAIN + '-' + CASE).exists()


def install(name, source_key, payload=None):
    source = base64.b64decode(PAYLOAD[source_key + '_source_base64'], validate=True)
    assert hashlib.sha256(source).hexdigest() == PAYLOAD[source_key + '_source_sha256']
    path = root / name
    assert not path.exists()
    prefix = b'' if payload is None else b"ROLE='etl'\nPAYLOAD=" + repr(payload).encode() + b'\n'
    path.write_bytes(prefix + source)
    path.chmod(0o600)
    return path


data = {'chain': CHAIN, 'case': CASE}
if CASE == 'E2':
    challenge = PAYLOAD['challenge_payload']
    assert challenge['chain'] == CHAIN and challenge['case'] == CASE
    data['challenge_script'] = str(install('challenge-' + CHAIN + '-' + CASE + '.py', 'challenge', challenge))
pipeline = install('prepare-' + CHAIN + '-' + CASE + '.py', 'pipeline', data)
unit = 'etl-negative-preparation-' + CHAIN + '-' + CASE + '.service'
command = ['systemd-run', '--no-block', '--unit', unit, '--property=Type=oneshot', '--property=UMask=0077',
           '--property=TimeoutStartSec=3h', '--property=TimeoutStopSec=300s', '/usr/bin/python3', '-B', str(pipeline)]
actual = subprocess.run(command, capture_output=True, timeout=30)
for suffix, content in (('stdout', actual.stdout), ('stderr', actual.stderr)):
    (root / ('prepare-launch-' + CHAIN + '-' + CASE + '.' + suffix)).write_bytes(content)
assert actual.returncode == 0
record = {'chain': CHAIN, 'case': CASE, 'unit': unit, 'native_preparation_started': True,
          'observation_started': False, 'pipeline_sha256': hashlib.sha256(pipeline.read_bytes()).hexdigest()}
(root / ('prepare-launch-' + CHAIN + '-' + CASE + '.json')).write_text(json.dumps(record, indent=2))
print(json.dumps(record, sort_keys=True))
