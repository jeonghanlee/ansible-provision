#!/usr/bin/env python3
"""Install the original fixture and collector without registering PVs."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')
UNITS = Path('/etc/systemd/system')
CONF = Path('/opt/epicsarchiverap-maven/archappl.conf')
SOFTIOC = '/opt/epics/1.3.0/rocky-8.10/7.0.10/base/bin/linux-x86_64/softIoc'
FIXTURE_SHA = '037a92691bc23a6dcac37ec3613ad19c9f80b93b689209ec8dc403b519eaf594'


def main():
    os.umask(0o022)
    os.environ['PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
    if (OUT / 'observation.json').exists():
        raise RuntimeError('An observation has already started')
    if hashlib.sha256((TOOLS / 'pvs-all.csv').read_bytes()).hexdigest() != FIXTURE_SHA:
        raise RuntimeError('Unexpected fixture digest')
    count = subprocess.check_output(['mysql', '--protocol=SOCKET', '-N', '-B', 'archappl',
                                     '-e', 'SELECT COUNT(*) FROM PVTypeInfo'], text=True).strip()
    if count != '0':
        raise RuntimeError('Fixture installation requires the empty appliance')
    OUT.mkdir(mode=0o700, exist_ok=True)
    backup = OUT / 'archappl.conf.before-fixture'
    if not backup.exists():
        backup.write_bytes(CONF.read_bytes())
        backup.chmod(0o600)
    config = CONF.read_text()
    for key, value in [('EPICS_CA_ADDR_LIST', '127.0.0.1'), ('EPICS_CA_AUTO_ADDR_LIST', 'NO')]:
        config, count = re.subn(r'^' + key + r'=.*$', key + '="' + value + '"', config, flags=re.MULTILINE)
        if count != 1:
            raise RuntimeError('Expected exactly one configuration key: ' + key)
    CONF.write_text(config)
    ioc = '[Unit]\nDescription=ETL soak 903-PV fixture\n[Service]\nType=simple\nUser=mid-srv\nGroup=mid\n'
    for key, value in [('EPICS_CAS_INTF_ADDR_LIST', '127.0.0.1'), ('EPICS_CA_ADDR_LIST', '127.0.0.1'),
                       ('EPICS_CA_AUTO_ADDR_LIST', 'NO'), ('EPICS_CAS_AUTO_BEACON_ADDR_LIST', 'NO'),
                       ('EPICS_CAS_BEACON_ADDR_LIST', '127.0.0.1'), ('EPICS_CA_MAX_ARRAY_BYTES', '16384')]:
        ioc += 'Environment=' + key + '=' + value + '\n'
    ioc += 'ExecStart=' + SOFTIOC + ' -S'
    for name in ['aasoak.db', 'load1.db', 'load2.db']:
        ioc += ' -d ' + str(TOOLS / name)
    ioc += '\nRestart=no\n[Install]\nWantedBy=multi-user.target\n'
    (UNITS / 'etl-soak-ioc.service').write_text(ioc)
    (UNITS / 'etl-soak-sample.service').write_text(
        '[Unit]\nDescription=Capture real ETL soak evidence\n[Service]\nType=oneshot\nUMask=0077\n'
        'Environment=PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin\n'
        'ExecStart=/usr/bin/python3 /usr/local/share/etl-soak/collect.py /var/lib/etl-soak '
        '/usr/local/share/etl-soak/pvs-all.csv\nTimeoutStartSec=240s\n')
    (UNITS / 'etl-soak-sample.timer').write_text(
        '[Unit]\nDescription=Sample the ETL soak every five minutes\n[Timer]\n'
        'OnCalendar=*-*-* *:0/5:00 UTC\nAccuracySec=1s\nPersistent=true\n[Install]\nWantedBy=timers.target\n')
    (UNITS / 'etl-soak-finish.service').write_text(
        '[Unit]\nDescription=Measure whole-unit shutdown after the ETL soak\n[Service]\n'
        'Type=oneshot\nUMask=0077\nExecStart=/usr/bin/python3 /usr/local/share/etl-soak/observe.py finish\n'
        'TimeoutStartSec=15min\n')
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', 'enable', '--now', 'etl-soak-ioc.service'], check=True)
    subprocess.run(['systemctl', 'restart', 'epicsarchiverap-maven.service'], check=True)
    print(json.dumps({'fixture_sha256': FIXTURE_SHA, 'ca_address': '127.0.0.1', 'ca_auto_address': 'NO'}))


if __name__ == '__main__':
    main()
