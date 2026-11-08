#!/usr/bin/env python3
"""Execute one preflight and conditionally start one fresh four-hour observation."""

import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/var/lib/buffer29')
TOOLS = Path('/usr/local/share/buffer29')
CONF = Path('/opt/epicsarchiverap-maven/archappl.conf')
SERVICE = 'epicsarchiverap-maven.service'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    os.environ['PATH'] = '/usr/sbin:/usr/bin:/sbin:/bin'
    os.umask(0o077)
    frozen = json.loads((ROOT / 'frozen-identities.json').read_text())
    for name, expected in frozen['files'].items():
        if digest(name) != expected:
            raise RuntimeError('Frozen tool or configuration identity changed')
    for name, expected in frozen['fixtures'].items():
        if digest('/usr/local/share/etl-soak/' + name) != expected:
            raise RuntimeError('Frozen shipped fixture identity changed')
    subprocess.run(['/usr/bin/python3', str(TOOLS / 'runner.py'), 'preflight'], check=True, timeout=1230)
    result = json.loads((ROOT / 'preflight/verdict.json').read_text())
    if result['result'] != 'Passed':
        raise RuntimeError('Main observation requires a Passed preflight')
    subprocess.run(['systemctl', 'stop', SERVICE], check=True, timeout=310)
    for name, expected in frozen['files'].items():
        if digest(name) != expected:
            raise RuntimeError('Identity changed during preflight')
    contents = CONF.read_text()
    old = '-Dbuffer29.output=/var/lib/buffer29/preflight'
    if contents.count(old) != 1:
        raise RuntimeError('Unexpected capture boundary configuration')
    CONF.write_text(contents.replace(old, '-Dbuffer29.output=/var/lib/buffer29/main'))
    (ROOT / 'main-configuration-sha256.txt').write_text(digest(CONF) + '\n')
    subprocess.run(['/usr/bin/python3', str(TOOLS / 'runner.py'), 'main'], check=True, timeout=16230)


if __name__ == '__main__':
    main()
