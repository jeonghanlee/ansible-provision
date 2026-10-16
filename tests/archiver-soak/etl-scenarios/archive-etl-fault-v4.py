"""Preserve a terminal case and its real native replay inputs without replacement."""

import hashlib
import json
import os
from pathlib import Path
import pwd
import subprocess
import tarfile

assert ROLE == 'etl'
CHAIN, CASE = PAYLOAD['chain'], PAYLOAD['case']
assert CHAIN in ('shortened', 'default') and CASE in ('E3', 'E4')
case = Path('/var/lib/etl-negative-cases') / (CHAIN + '-' + CASE)
root = Path('/var/lib/etl-negative-archives') / (CHAIN + '-' + CASE)
assert not root.exists()
os.umask(0o077)
root.mkdir(parents=True, mode=0o700)
tools = Path('/usr/local/share/etl-soak')
out = Path('/var/lib/etl-soak')
units = ('etl-soak-sample.timer', 'etl-soak-sample.service', 'etl-soak-finish.timer',
         'etl-soak-finish.service', 'etl-soak-abort.service', 'epicsarchiverap-maven.service',
         'etl-negative-' + CHAIN + '-' + CASE + '.service')
states = {}
for unit in units:
    text = subprocess.check_output(['systemctl', 'show', unit, '-p', 'MainPID', '-p', 'ActiveState'], text=True)
    values = dict(line.split('=', 1) for line in text.splitlines())
    assert values.get('MainPID', '0' if unit.endswith('.timer') else None) == '0' and values['ActiveState'] not in ('active', 'activating', 'deactivating')
    states[unit] = values
(root / 'actual-unit-states.json').write_text(json.dumps(states, indent=2))
replay = Path('/var/lib/etl-negative-orchestration/replay-etl-fault.py')
assert hashlib.sha256(replay.read_bytes()).hexdigest() == PAYLOAD['replay_sha256']
actual = subprocess.run(['/usr/bin/python3', '-B', str(replay), '--case', str(case),
                         '--output', str(root / 'guest-replay')], capture_output=True, timeout=1500)
(root / 'replay.stdout').write_bytes(actual.stdout)
(root / 'replay.stderr').write_bytes(actual.stderr)
assert actual.returncode == 0, 'The real guest replay failed'
result = json.loads((root / 'guest-replay/result.json').read_text())
archive_path = Path('/var/tmp/etl-negative-' + CHAIN + '-' + CASE + '.tar')
assert not archive_path.exists()
paths = [tools, out, case, Path('/var/lib/etl-focused'), root,
         Path('/var/lib/etl-negative-orchestration'), Path('/var/lib/etl-negative-study'),
         Path('/var/lib/etl-negative-file-logging'), Path('/var/lib/etl-negative-preparation-' + CHAIN),
         Path('/etc/systemd/system'), Path('/arch'), Path('/var/tmp/archiver-build.config')]
terminal_proof = json.loads((out / 'terminal-path-verification.json').read_text())
probe = Path(terminal_proof['probe_directory'])
assert probe.parent == out.parent and probe.name.startswith('etl-soak-terminal-probe-')
paths.append(probe)

additional_preparation = Path('/var/lib/etl-negative-preparation-' + CHAIN + '-' + CASE)
if additional_preparation.exists():
    paths.append(additional_preparation)
for pattern in ('etl-negative-preparation-' + CHAIN + '*', 'etl-negative-check-followup-*', 'etl-negative-failed-preflight-*'):
    for path in sorted(Path('/var/lib').glob(pattern)):
        if path not in paths:
            paths.append(path)
with tarfile.open(archive_path, 'x', dereference=True) as archive:
    for path in paths:
        assert path.exists()
        archive.add(path, arcname=str(path.relative_to('/')))
digest = hashlib.sha256()
with archive_path.open('rb') as stream:
    for block in iter(lambda: stream.read(1048576), b''):
        digest.update(block)
account = pwd.getpwnam('vmadmin')
os.chown(archive_path, account.pw_uid, account.pw_gid)
archive_path.chmod(0o600)
record = {'case': CASE, 'chain': CHAIN, 'archive': str(archive_path),
          'bytes': archive_path.stat().st_size, 'sha256': digest.hexdigest(),
          'guest_real_frozen_replay_complete': True, 'expectation': result['expectation'],
          'terminal_sha256': result['terminal_sha256'], 'replay_sha256': PAYLOAD['replay_sha256']}
(root / 'archive.json').write_text(json.dumps(record, indent=2))
print(json.dumps(record, sort_keys=True))
