"""Start one runtime case after its own new invocation preparation is complete."""

import base64
import hashlib
import json
from pathlib import Path
import subprocess

assert ROLE == PAYLOAD['role'] == 'etl'
CHAIN, CASE = PAYLOAD['chain'], PAYLOAD['case']
assert CHAIN in ('shortened', 'default') and CASE in ('E1', 'E2', 'E3', 'E4')
root = Path('/var/lib/etl-negative-orchestration')
prepared = json.loads(Path('/var/lib/etl-negative-preparation-' + CHAIN + '-' + CASE + '/state.json').read_text())
assert prepared['stage'] == 'Prepared for runtime verification' and prepared['seven_measurement_rounds_complete']
assert prepared['native_retained_original_continuity_verified']
unit = 'etl-negative-preparation-' + CHAIN + '-' + CASE + '.service'
assert subprocess.check_output(['systemctl', 'show', unit, '-p', 'MainPID', '--value'], text=True).strip() == '0'
assert not Path('/var/lib/etl-soak/observation.json').exists()


def install(name, key, data=None):
    source = base64.b64decode(PAYLOAD[key + '_source_base64'], validate=True)
    assert hashlib.sha256(source).hexdigest() == PAYLOAD[key + '_source_sha256']
    path = root / name
    assert not path.exists()
    prefix = b'' if data is None else b"ROLE='etl'\nPAYLOAD=" + repr(data).encode() + b'\n'
    path.write_bytes(prefix + source)
    path.chmod(0o600)
    return path


data = {'chain': CHAIN, 'case': CASE}
if CASE in ('E3', 'E4'):
    data['native_preflight_script'] = str(install('native-preflight-' + CHAIN + '-' + CASE + '.py', 'preflight'))
    boundary = {'chain': CHAIN, 'case': CASE, 'wrapper_source_base64': PAYLOAD['wrapper_source_base64'],
                'wrapper_source_sha256': PAYLOAD['wrapper_source_sha256']}
    data['boundary_preflight_script'] = str(install('boundary-preflight-' + CHAIN + '-' + CASE + '.py', 'boundary', boundary))
    replay = root / 'replay-etl-fault.py'
    if replay.exists():
        assert hashlib.sha256(replay.read_bytes()).hexdigest() == PAYLOAD['replay_source_sha256']
    else:
        install('replay-etl-fault.py', 'replay')
suffix = '-recovery-003' if CHAIN == 'shortened' and CASE == 'E1' else ''
runtime = install('runtime-' + CHAIN + '-' + CASE + suffix + '.py', 'runtime', data)
unit = 'etl-negative-' + CHAIN + '-' + CASE + suffix + '.service'
command = ['systemd-run', '--no-block', '--unit', unit, '--property=Type=oneshot', '--property=UMask=0077',
           '--property=TimeoutStartSec=4h', '--property=TimeoutStopSec=300s', '/usr/bin/python3', '-B', str(runtime)]
actual = subprocess.run(command, capture_output=True, timeout=30)
for suffix, content in (('stdout', actual.stdout), ('stderr', actual.stderr)):
    (root / ('runtime-launch-' + CHAIN + '-' + CASE + ('-recovery-003' if CHAIN == 'shortened' and CASE == 'E1' else '') + '.' + suffix)).write_bytes(content)
assert actual.returncode == 0
record = {'chain': CHAIN, 'case': CASE, 'unit': unit, 'runtime_worker_started': True,
          'runtime_sha256': hashlib.sha256(runtime.read_bytes()).hexdigest()}
(root / ('runtime-launch-' + CHAIN + '-' + CASE + ('-recovery-003' if CHAIN == 'shortened' and CASE == 'E1' else '') + '.json')).write_text(json.dumps(record, indent=2))
print(json.dumps(record, sort_keys=True))
