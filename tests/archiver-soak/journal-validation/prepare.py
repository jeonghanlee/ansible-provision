#!/usr/bin/env python3
"""Build and install the independent journal package without starting services."""

import argparse
import collections
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET

BASELINE = '649fee80561611f1494c1c3ce1f9546f6c619173'
APPLIANCE_SOURCE = '162269e7db97f527626ba0b387933a8c47e8bb57'
PREFIX = Path('/opt/journal-validation')
EVIDENCE = Path('/var/lib/journal-validation')
RUNTIME = Path('/run/journal-validation')
FIXTURES = ('pvs-all.csv', 'aasoak.db', 'load1.db', 'load2.db', 'retest-deadband.db')
LOGGER = 'org.epics.archiverappliance.retrieval.DataRetrievalServlet'
MODULES = {'journal_coverage.py': 'tests/archiver-soak/etl-pass/journal_coverage.py',
           'register.py': 'tests/archiver-soak/etl-pass/register.py'}
LOCAL_FILES = ('prepare.py', 'basic.py', 'long.py', 'lifecycle.py', 'rotation.py', 'rotation_during.py',
               'obsolete_anchor.py', 'window_coverage.py', 'boot_coverage.py', 'restart.py',
               'interval.py', 'failure.py', 'loss.py', 'README.md', 'config.example.json')
SAFE_TOKEN = re.compile(r'^[A-Za-z0-9_./:+-]+$')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def blob(repository, revision, name):
    return subprocess.check_output(['git', '-C', str(repository), 'show', revision + ':' + name])


def fixture_contract(data):
    rows = list(csv.DictReader(io.StringIO(data.decode())))
    periods = collections.Counter(row['period'] for row in rows)
    methods = collections.Counter(row['method'] for row in rows)
    if (len(rows) != 903 or len({row['pv'] for row in rows}) != 903 or
            periods != {'1.0': 783, '0.1': 110, '10.0': 10} or
            methods != {'MONITOR': 880, 'SCAN': 23}):
        raise RuntimeError('The immutable 903-PV fixture contract does not match')
    return {'pv_count': len(rows), 'periods': dict(periods), 'methods': dict(methods)}


def build(repository, appliance_source, destination):
    source = Path(__file__).resolve().parent
    payload = {name: (source / name).read_bytes() for name in LOCAL_FILES}
    provenance = {}
    for target, origin in {**MODULES, **{name: 'tests/archiver-soak/fixtures/' + name
                                     for name in FIXTURES}}.items():
        payload[target] = blob(repository, BASELINE, origin)
        provenance[target] = {'source': origin, 'commit': BASELINE,
                              'sha256': digest(payload[target])}
    contract = fixture_contract(payload['pvs-all.csv'])
    native = source / 'journal_coverage.py'
    if native.read_bytes() != payload['journal_coverage.py']:
        raise RuntimeError('The extracted collector differs from the immutable baseline')
    xml_path = 'src/resources/main/log4j2.xml'
    original = blob(appliance_source, APPLIANCE_SOURCE, xml_path)
    configuration = ET.fromstring(original)
    loggers = configuration.find('Loggers')
    if loggers is None or configuration.find('Appenders/Console') is None:
        raise RuntimeError('Expected the actual console log4j2 configuration')
    ET.SubElement(loggers, 'Logger', {'name': LOGGER, 'level': 'debug'})
    payload['log4j2.xml'] = ET.tostring(configuration, encoding='utf-8', xml_declaration=True)
    provenance['log4j2.xml'] = {'repository': 'jeonghanlee/epicsarchiverap-maven',
                                'commit': APPLIANCE_SOURCE, 'source': xml_path,
                                'source_sha256': digest(original), 'logger': LOGGER}
    payload['source.json'] = (json.dumps({'baseline_commit': BASELINE,
                                        'files': provenance, 'fixture': contract},
                                       indent=2, sort_keys=True) + '\n').encode()
    manifest = {'schema': 1, 'baseline_commit': BASELINE,
                'files': {name: digest(data) for name, data in sorted(payload.items())}}
    destination.mkdir(mode=0o700, parents=True, exist_ok=False)
    for name, data in payload.items():
        path = destination / name
        path.write_bytes(data)
        path.chmod(0o755 if name.endswith('.py') else 0o644)
    save(destination / 'manifest.json', manifest)
    return {'package': str(destination), 'fixture': contract,
            'manifest_sha256': digest((destination / 'manifest.json').read_bytes())}


def verify(package):
    manifest = json.loads((package / 'manifest.json').read_text())
    expected = set(LOCAL_FILES) | set(MODULES) | set(FIXTURES) | {'source.json', 'log4j2.xml'}
    if (manifest.get('schema') != 1 or manifest.get('baseline_commit') != BASELINE or
            set(manifest.get('files', {})) != expected):
        raise RuntimeError('The independent package manifest is incomplete')
    for name, expected_hash in manifest['files'].items():
        path = package / name
        if path.is_symlink() or not path.is_file() or digest(path.read_bytes()) != expected_hash:
            raise RuntimeError('Independent package member changed: ' + name)
    fixture_contract((package / 'pvs-all.csv').read_bytes())
    return manifest


def configuration(path):
    config = json.loads(path.read_text())
    for key in ('appliance_unit', 'softioc', 'user', 'group', 'health_script'):
        if not isinstance(config.get(key), str) or not SAFE_TOKEN.fullmatch(config[key]):
            raise RuntimeError('Missing or unsafe configuration value: ' + key)
    for key in ('softioc', 'health_script'):
        if not Path(config[key]).is_absolute():
            raise RuntimeError('An absolute executable path is required: ' + key)
    if not re.fullmatch(r'[A-Za-z0-9_.@-]+\.service', config['appliance_unit']):
        raise RuntimeError('An appliance service name is required')
    for key in ('user', 'group'):
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*', config[key]):
            raise RuntimeError('A local account name is required: ' + key)
    for key in ('retrieval_url', 'mgmt_url'):
        if not isinstance(config.get(key), str):
            raise RuntimeError('An explicit appliance URL is required: ' + key)
        url = urllib.parse.urlsplit(config[key])
        if (url.scheme not in ('http', 'https') or url.hostname not in ('127.0.0.1', 'localhost', '::1') or
                url.username or url.password or url.query or url.fragment):
            raise RuntimeError('A loopback appliance URL without credentials or query is required: ' + key)
    if config.get('deployment_role') != 'journal-validation':
        raise RuntimeError('Only a dedicated journal-validation deployment is supported')
    if (not isinstance(config.get('appliance_artifact'), str) or
            not Path(config['appliance_artifact']).is_absolute()):
        raise RuntimeError('An absolute deployed appliance artifact path is required')
    if (not isinstance(config.get('retrieval_catalina_base'), str) or
            not Path(config['retrieval_catalina_base']).is_absolute()):
        raise RuntimeError('An absolute retrieval Tomcat base is required')
    return config


def units(config):
    paths = ' '.join('-d ' + str(PREFIX / name) for name in FIXTURES if name.endswith('.db'))
    ioc = ('[Unit]\nDescription=Independent journal 903-PV fixture\n[Service]\nType=simple\n'
           'User=' + config['user'] + '\nGroup=' + config['group'] + '\n'
           'Environment=EPICS_CAS_INTF_ADDR_LIST=127.0.0.1\n'
           'Environment=EPICS_CAS_AUTO_BEACON_ADDR_LIST=NO\n'
           'Environment=EPICS_CAS_BEACON_ADDR_LIST=127.0.0.1\n'
           'Environment=EPICS_CA_MAX_ARRAY_BYTES=16384\n'
           'ExecStart=' + config['softioc'] + ' -S ' + paths + '\nRestart=no\n')
    health = ('[Unit]\nDescription=Independent journal actual appliance health execution\n'
              '[Service]\nType=oneshot\nUMask=0077\nExecStart=/bin/bash ' + config['health_script'] +
              ' health --systemd ' + config['appliance_unit'] + ' journal-validation-health.service 60\n'
              'SuccessExitStatus=3\nTimeoutStartSec=30s\n'
              'ExecStopPost=/usr/bin/python3 -B /opt/journal-validation/basic.py health-event\n')
    basic = ('[Unit]\nDescription=One-hour independent journal basic check\n[Service]\n'
             'Type=oneshot\nUMask=0077\n'
             'ExecStart=/usr/bin/python3 -B /opt/journal-validation/basic.py run-basic\n'
             'TimeoutStartSec=infinity\nTimeoutStopSec=300s\n')
    return {'journal-validation-ioc.service': ioc, 'journal-validation-health.service': health,
            'journal-validation-basic.service': basic}


def install(package, config_path, root):
    manifest = verify(package)
    config = configuration(config_path)
    root = root.resolve()
    if root == Path('/') and os.geteuid() != 0:
        raise RuntimeError('Live installation requires root on the dedicated journal deployment')
    destination = root / PREFIX.relative_to('/')
    if destination.exists() or destination.is_symlink():
        raise RuntimeError('An existing independent installation is never replaced')
    unit_root = root / 'etc/systemd/system'
    for name in units(config):
        unit = unit_root / name
        if unit.exists() or unit.is_symlink():
            raise RuntimeError('A journal-validation unit already exists: ' + name)
    dropin = unit_root / (config['appliance_unit'] + '.d') / 'journal-validation.conf'
    if dropin.exists() or dropin.is_symlink():
        raise RuntimeError('The dedicated appliance logging drop-in already exists')
    for directory in (EVIDENCE, RUNTIME):
        path = root / directory.relative_to('/')
        if path.exists() or path.is_symlink():
            raise RuntimeError('An independent state directory already exists: ' + str(directory))
    for path in (destination, unit_root, dropin, root / EVIDENCE.relative_to('/'),
                 root / RUNTIME.relative_to('/')):
        if os.path.commonpath((root, path.resolve())) != str(root):
            raise RuntimeError('A staged installation path resolves outside its root')
    shutil.copytree(package, destination)
    destination.chmod(0o755)
    save(destination / 'config.json', config)
    for directory in (EVIDENCE, RUNTIME):
        (root / directory.relative_to('/')).mkdir(mode=0o700, parents=True, exist_ok=True)
    unit_root.mkdir(parents=True, exist_ok=True)
    for name, content in units(config).items():
        (unit_root / name).write_text(content)
    dropin.parent.mkdir(parents=True, exist_ok=True)
    dropin.write_text('[Service]\nEnvironment=LOG4J_CONFIGURATION_FILE=/opt/journal-validation/log4j2.xml\n')
    return {'installed': str(destination), 'staged': root != Path('/'),
            'manifest_sha256': digest((package / 'manifest.json').read_bytes()),
            'services_started': False, 'members': len(manifest['files'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('build')
    make.add_argument('--repository', type=Path, required=True)
    make.add_argument('--appliance-source', type=Path, required=True)
    make.add_argument('--destination', type=Path, required=True)
    check = commands.add_parser('verify')
    check.add_argument('package', type=Path)
    deploy = commands.add_parser('install')
    deploy.add_argument('package', type=Path)
    deploy.add_argument('--config', type=Path, required=True)
    deploy.add_argument('--root', type=Path, default=Path('/'))
    args = parser.parse_args()
    if args.command == 'build':
        result = build(args.repository, args.appliance_source, args.destination)
    elif args.command == 'verify':
        result = verify(args.package)
    else:
        result = install(args.package, args.config, args.root)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
