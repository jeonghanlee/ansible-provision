#!/usr/bin/env python3
"""Verify automatic ETL on installed classes and retain physical/HTTP evidence."""

import argparse
import base64
import concurrent.futures
import collections
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import time
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

import collect
import contract
import evaluate
import observe

INSTALL = Path('/opt/epicsarchiverap-maven')
SOURCE = Path('/opt/epicsarchiverap-env-src/epicsarchiverap-env')
MAVEN_HEAD = '162269e7db97f527626ba0b387933a8c47e8bb57'
ENV_HEAD = '482cf2939ea997064e4a2df64e3cb420681f4566'
ROOT = Path('/var/lib/etl-focused')
LOGGER = 'org.epics.archiverappliance.etl.common.ETLPassDriver'
START_TIMEOUT = 300
ORDER_MARGIN = 600
BIN_SETTLE_SECONDS = 30
SHUTDOWN_SAMPLE_SECONDS = 60
COMPONENTS = ('mgmt', 'engine', 'etl', 'retrieval')
POLICIES = (('', 0), ('VeryFast', 10), ('Fast', 30), ('Medium', 60))
REDUCTIONS = {policy: 'lastSample_' + str(interval) if interval else '' for policy, interval in POLICIES}
FIELDS = ('secs', 'nanos', 'val', 'status', 'severity')
CLIENT = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def save(root, name, value):
    collect.write_json(root / name, value)


def request(path, retrieval=False, **params):
    base = 'http://127.0.0.1:17668/retrieval' if retrieval else collect.MGMT
    url = base + '/' + path
    if params:
        url += '?' + urllib.parse.urlencode(params)
    with CLIENT.open(url, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError('HTTP request failed: ' + path)
        result = json.load(response)
    if isinstance(result, dict) and result.get('status') == 'error':
        raise RuntimeError('Appliance returned an error: ' + path)
    return result


def protect():
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('An existing observation cannot be changed')
    for unit in (observe.SAMPLER + '.timer', observe.FINISH + '.timer'):
        state = observe.checked(['systemctl', 'show', unit, '--value', '-p', 'ActiveState'])
        if state in ('active', 'activating', 'deactivating'):
            raise RuntimeError('Observation timers must be inactive')


def identity():
    unit = collect.properties(observe.unit_state())
    pids = collect.resources.jvm_pids()
    if unit.get('ActiveState') != 'active' or not unit.get('InvocationID') or set(pids) != set(COMPONENTS):
        raise RuntimeError('An active unit and all four JVMs are required')
    jvms = {}
    for component, pid in pids.items():
        stat = collect.resources.proc_stat(pid)
        if not stat:
            raise RuntimeError('Missing JVM process identity')
        jvms[component] = {'pid': str(pid), 'start': stat['start']}
    return {'boot_id': observe.BOOT.read_text().strip(), 'invocation_id': unit['InvocationID'], 'jvms': jvms}


def environment():
    values = {}
    for line in (INSTALL / 'archappl.conf').read_text().splitlines():
        match = re.fullmatch(r'(?:export )?([A-Z_][A-Z_0-9]*)=(.*)', line)
        if match:
            tokens = shlex.split(match[2], comments=True)
            if len(tokens) == 1:
                values[match[1]] = tokens[0]
    return values


def settings(chain, typeinfo, values):
    urls = list(typeinfo['dataStores'])
    for index, url in enumerate(urls):
        for key, value in values.items():
            url = url.replace('${' + key + '}', value)
        if '${' in url:
            raise RuntimeError('Unresolved store environment macro')
        urls[index] = url
    contract.deployed_configuration(chain, urls)
    modes = []
    for index, url in enumerate(urls):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query, keep_blank_values=True)
        if any(len(value) != 1 for value in query.values()):
            raise RuntimeError('Ambiguous store configuration')
        mode = {key: value[0] for key, value in query.items()}
        mode.setdefault('compress', 'NONE')
        mode.setdefault('backupFilesBeforeETL', 'false')
        mode.setdefault('etlIntoStoreIf', '')
        mode.setdefault('etlOutofStoreIf', '')
        mode.setdefault('reducedata', '')
        if mode['compress'] != 'NONE' or mode['backupFilesBeforeETL'] != 'false':
            raise RuntimeError('Focused fixture supports uncompressed direct append only')
        if not Path(mode['rootFolder']).is_absolute():
            raise RuntimeError('An absolute source root is required')
        expected = collect.STORE / ('sts', 'mts', 'lts')[index] / 'ArchiverStore'
        if Path(mode['rootFolder']).resolve() != expected.resolve():
            raise RuntimeError('Store root differs from the installed store')
        modes.append(mode)
    return {'urls': urls, 'modes': modes}


def artifacts():
    contract.deployment_pins(observe.TOOLS, {'env': ENV_HEAD, 'maven': MAVEN_HEAD})
    heads = {name: observe.checked(['git', '-C', str(path), 'rev-parse', 'HEAD'])
             for name, path in (('env', SOURCE), ('maven', SOURCE / 'epicsarchiverap-maven-src'))}
    if heads != {'env': ENV_HEAD, 'maven': MAVEN_HEAD}:
        raise RuntimeError('Installed source pins differ from the approved commits')
    files = {}
    for component in COMPONENTS:
        webapps = INSTALL / component / 'webapps'
        wars = sorted((SOURCE / 'epicsarchiverap-maven-src/target').glob('*' + component + '.war'))
        if len(wars) != 1:
            raise RuntimeError('Exactly one built WAR is required: ' + component)
        war = wars[0]
        files[str(war)] = contract.digest(war)
        classes = webapps / component / 'WEB-INF'
        found = [*classes.rglob('*.class'), *classes.glob('lib/*.jar')]
        if not found:
            raise RuntimeError('Running class files missing: ' + component)
        with zipfile.ZipFile(war) as archive:
            expected = {name for name in archive.namelist() if name.startswith('WEB-INF/')
                        and (name.endswith('.class') or name.startswith('WEB-INF/lib/') and name.endswith('.jar'))}
            actual = {str(path.relative_to(webapps / component)) for path in found}
            if expected != actual:
                raise RuntimeError('Installed class/JAR inventory differs from built WAR: ' + component)
            for path in sorted(found):
                digest = contract.digest(path)
                member = str(path.relative_to(webapps / component))
                if digest != hashlib.sha256(archive.read(member)).hexdigest():
                    raise RuntimeError('Installed payload differs from built WAR: ' + str(path))
                files[str(path)] = digest
    properties = INSTALL / 'etl/webapps/etl/WEB-INF/classes/archappl.properties'
    values = environment()
    configured = values.get('ARCHAPPL_PROPERTIES_FILENAME')
    if configured:
        properties = Path(configured)
    policy = INSTALL / 'mgmt/webapps/mgmt/WEB-INF/classes/policies.py'
    if values.get('ARCHAPPL_POLICIES'):
        policy = Path(values['ARCHAPPL_POLICIES'])
    files[str(properties)] = contract.digest(properties)
    files[str(policy)] = contract.digest(policy)
    parsed = {}
    for line in properties.read_text().splitlines():
        match = re.fullmatch(r'\s*([^#!\s][^=]*?)\s*=\s*(.*?)\s*', line)
        if match:
            parsed[match[1]] = match[2]
    space = parsed.get('org.epics.archiverappliance.etl.common.OutOfSpaceHandling',
                       'DELETE_SRC_STREAMS_IF_FIRST_DEST_WHEN_OUT_OF_SPACE')
    if space not in ('SKIP_ETL_WHEN_OUT_OF_SPACE', 'DELETE_SRC_STREAMS_WHEN_OUT_OF_SPACE',
                     'DELETE_SRC_STREAMS_IF_FIRST_DEST_WHEN_OUT_OF_SPACE'):
        raise RuntimeError('Unrecognized installed out-of-space policy')
    return {'heads': heads, 'files': files, 'properties_sha256': contract.digest(properties),
            'policy_sha256': contract.digest(policy), 'out_of_space': space,
            'stamp_sha256': contract.digest(Path('/var/tmp/archiver-build.config'))}


def inventory(root, chain, name='inventory.json', bundle_root=None):
    protect()
    before = identity()
    fixture = observe.TOOLS / 'pvs-all.csv'
    if contract.digest(fixture) != contract.FIXTURE_SHA:
        raise RuntimeError('Unexpected fixture digest')
    rows = list(csv.DictReader(fixture.open()))
    if len(rows) != 903 or len({row['pv'] for row in rows}) != 903:
        raise RuntimeError('Exactly 903 unique fixture PVs are required')
    values = environment()
    def query(row):
        info = request('getPVTypeInfo', pv=row['pv'])
        effective = settings(chain, info, values)
        if (row['policy'] not in REDUCTIONS or any(mode['reducedata'] for mode in effective['modes'][:2])
                or effective['modes'][2]['reducedata'] != REDUCTIONS[row['policy']]):
            raise RuntimeError('Reduction differs from the shipped fixture policy: ' + row['pv'])
        return {'pv': row['pv'], 'fixture_policy': row['policy'],
                'typeinfo': {key: info.get(key) for key in ('DBRType', 'chunkKey')}, 'effective': effective}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        observed = list(executor.map(query, rows))
    flags = request('getAllNamedFlags')
    tools = contract.verify_bundle(Path(bundle_root)) if bundle_root else observe.tool_hashes()
    result = {'observed_at': now(), 'identity': before, 'chain': chain, 'pvs': observed,
              'flags': flags, 'artifacts': artifacts(), 'tools': tools}
    if identity() != before:
        raise RuntimeError('Appliance restarted during configuration inspection')
    save(root, name, result)
    return result


def selected(inventory_record):
    chosen = []
    for policy, interval in POLICIES:
        matches = [row for row in inventory_record['pvs'] if row['fixture_policy'] == policy
                   and row['typeinfo'].get('DBRType') == 'DBR_SCALAR_DOUBLE']
        if not matches:
            raise RuntimeError('No scalar-double fixture PV for policy ' + policy)
        row = matches[0]
        modes = row['effective']['modes']
        if any(mode['etlIntoStoreIf'] or mode['etlOutofStoreIf'] for mode in modes):
            raise RuntimeError('Selected fixture must not have conditional store flags')
        expected = REDUCTIONS[policy]
        if modes[2].get('reducedata', '') != expected:
            raise RuntimeError('Reduction differs from the independent fixture contract')
        chosen.append((row, interval))
    return chosen


def specifications(record, timestamp):
    day = timestamp // 86400 * 86400
    old = day - 5 * 86400
    if dt.datetime.fromtimestamp(old, dt.timezone.utc).year != dt.datetime.fromtimestamp(timestamp, dt.timezone.utc).year:
        raise RuntimeError('This focused writer fixture requires samples in the current year')
    middle = ((timestamp // 3600 - 1) * 3600 + 1 if record['chain'] == 'shortened' else day - 86400 + 1)
    specs = []
    for row, interval in selected(record):
        width = interval or 60
        points = [(old, 0, 1), (old + width - 1, 999999999, 2), (old + width, 0, 3),
                  (old + width, 1, 4), (old + 2 * width - 1, 999999999, 5),
                  (old + 2 * width, 0, 6), (old + 2 * width, 1, 7), (old + 4 * width, 123456789, 8),
                  (middle, 0, 901), (timestamp, 123456789, 902)]
        inputs = [{'secs': seconds, 'nanos': nanos, 'val': value, 'status': value % 3, 'severity': value % 2}
                  for seconds, nanos, value in points]
        specs.append({'pv': row['pv'], 'chunkKey': row['typeinfo'].get('chunkKey'), 'stores': row['effective']['urls'],
                      'interval': interval, 'old': old, 'middle': middle, 'input': inputs,
                      'snapshot_windows': [[old, old + 300], [middle, middle + 1],
                                           [timestamp // width * width, (timestamp // width + 1) * width],
                                           [(timestamp // SHUTDOWN_SAMPLE_SECONDS - 1) * SHUTDOWN_SAMPLE_SECONDS,
                                            timestamp // SHUTDOWN_SAMPLE_SECONDS * SHUTDOWN_SAMPLE_SECONDS]],
                      'expected_old_indices': list(range(8)) if not interval else [1, 4, 6, 7]})
    return specs


def compile_helper(root):
    classes = root / 'helper-classes'
    classes.mkdir()
    webinf = INSTALL / 'etl/webapps/etl/WEB-INF'
    classpath = str(webinf / 'classes') + ':' + str(webinf / 'lib/*')
    source = observe.TOOLS / 'PBFixture.java'
    subprocess.run(['javac', '-proc:none', '-cp', classpath, '-d', str(classes), str(source)], check=True, timeout=120)
    return str(classes) + ':' + classpath


def pb(root, classpath, mode, name):
    with (root / (name + '.log')).open('w') as log:
        subprocess.run(['java', '-Xmx256m', '-cp', classpath, 'PBFixture', mode,
                        str(root / 'manifest.json'), str(root / name)], cwd=root,
                       stdout=log, stderr=subprocess.STDOUT, check=True, timeout=120)
    return json.loads((root / name).read_text())


def events(snapshot, pv, store, begin, end):
    return sorted([event for file in snapshot[pv][store] for event in file['events']
                   if begin <= event['secs'] < end], key=lambda row: (row['secs'], row['nanos'], row['raw']))


def baseline_check(specs, snapshot, seeded=False, require_live=True):
    for spec in specs:
        if not seeded:
            if any(Path(path).exists() for path in snapshot[spec['pv'] + '#seedDestinations']):
                raise RuntimeError('Historical source partition already exists')
            if require_live and not snapshot[spec['pv']][0]:
                raise RuntimeError('Registered live source files must be readable before seeding')
            continue
        for expected in spec['input']:
            actual = events(snapshot, spec['pv'], 0, expected['secs'], expected['secs'] + 1)
            if sum(all(row[key] == expected[key] for key in FIELDS) for row in actual) != 1:
                raise RuntimeError('Physical writer baseline is incomplete or duplicated')
        if len(events(snapshot, spec['pv'], 0, spec['old'], spec['old'] + 300)) != 8:
            raise RuntimeError('Unexpected historical baseline multiplicity')


def empty_paths(specs, snapshot, seeded=False):
    for spec in specs:
        stores = snapshot[spec['pv']]
        if len(stores) != 3 or any(stores[index] for index in range(1 if seeded else 0, 3)):
            raise RuntimeError('Actual PB paths remain in an empty fixture tier: ' + spec['pv'])


def file_digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def tree_manifest(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir() or root.resolve() != root:
        raise RuntimeError('A real absolute storage directory is required: ' + str(root))
    entries = {}
    for path in [root, *sorted(root.rglob('*'))]:
        metadata = path.lstat()
        if not (stat.S_ISDIR(metadata.st_mode) or stat.S_ISREG(metadata.st_mode)):
            raise RuntimeError('Unsupported storage entry: ' + str(path))
        row = {'kind': 'directory' if path.is_dir() else 'file', 'uid': metadata.st_uid,
               'gid': metadata.st_gid, 'mode': stat.S_IMODE(metadata.st_mode),
               'xattrs': {name: base64.b64encode(os.getxattr(path, name)).decode('ascii')
                         for name in sorted(os.listxattr(path))}}
        if path.is_file():
            row.update(size=metadata.st_size, sha256=file_digest(path))
        entries[str(path.relative_to(root))] = row
    return entries


def offline():
    for unit in (collect.UNIT, collect.IOC_UNIT):
        state = observe.checked(['systemctl', 'show', unit, '--value', '-p', 'ActiveState'])
        if state != 'inactive':
            raise RuntimeError('Offline preparation requires an inactive unit: ' + unit)
    if collect.resources.jvm_pids():
        raise RuntimeError('Offline preparation has remaining JVMs')


def database_snapshot(root, name):
    destination = root / name
    with destination.open('xb') as stream:
        subprocess.run(['mysqldump', '--protocol=SOCKET', '--skip-comments', '--compact',
                        '--skip-extended-insert', '--no-create-info', 'archappl'],
                       stdout=stream, check=True, timeout=120)
    return file_digest(destination)


def preserve_stores(root, roots):
    roots = [Path(path) for path in roots]
    destination = root / 'preparation-stores'
    archive_path = root / 'preparation-stores.tar.gz'
    if len(roots) != 3 or len(set(roots)) != 3:
        raise RuntimeError('Three distinct active storage roots are required')
    for path in [root, *roots]:
        if path.resolve() != path or path.is_symlink():
            raise RuntimeError('Storage preservation requires resolved real paths')
    for index, path in enumerate(roots):
        if (root == path or root.is_relative_to(path) or path.is_relative_to(root)
                or any(path.is_relative_to(other) or other.is_relative_to(path)
                       for other in roots[index + 1:])):
            raise RuntimeError('Storage preservation roots overlap')
        if path.stat().st_dev != root.stat().st_dev:
            raise RuntimeError('Storage preservation requires the same filesystem')
    if destination.exists() or archive_path.exists():
        raise RuntimeError('Storage preservation destination already exists')
    manifests = [tree_manifest(path) for path in roots]
    proof = {'observed_at': now(), 'roots': [str(path) for path in roots],
             'archive': str(archive_path), 'manifests': manifests, 'moved': [], 'empty_roots': []}
    save(root, 'storage-preservation.json', proof)
    with tarfile.open(archive_path, 'x:gz') as archive:
        for tier, path, manifest in zip(('sts', 'mts', 'lts'), roots, manifests):
            for relative in manifest:
                archive.add(path / relative, arcname=str(Path(tier) / relative), recursive=False)
    expected = {str(Path(tier) / relative): metadata
                for tier, manifest in zip(('sts', 'mts', 'lts'), manifests)
                for relative, metadata in manifest.items()}
    with tarfile.open(archive_path, 'r:gz') as archive:
        members = archive.getmembers()
        if len(members) != len(expected) or {member.name for member in members} != set(expected):
            raise RuntimeError('Storage archive file inventory differs')
        for member in members:
            metadata = expected[member.name]
            if ((member.isdir() if metadata['kind'] == 'directory' else member.isfile()) is not True
                    or (member.uid, member.gid, member.mode) !=
                    (metadata['uid'], metadata['gid'], metadata['mode'])):
                raise RuntimeError('Storage archive entry metadata differs')
            if member.isfile():
                value = hashlib.sha256()
                with archive.extractfile(member) as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        value.update(block)
                if member.size != metadata['size'] or value.hexdigest() != metadata['sha256']:
                    raise RuntimeError('Storage archive bytes differ')
    proof['archive_sha256'] = file_digest(archive_path)
    destination.mkdir(mode=0o700)
    for tier, path, manifest in zip(('sts', 'mts', 'lts'), roots, manifests):
        if tree_manifest(path) != manifest:
            raise RuntimeError('Active storage changed before preservation')
        preserved = destination / tier
        if preserved.exists():
            raise RuntimeError('Preserved storage destination already exists')
        path.rename(preserved)
        proof['moved'].append({'source': str(path), 'destination': str(preserved)})
        save(root, 'storage-preservation.json', proof)
        if tree_manifest(preserved) != manifest:
            raise RuntimeError('Moved storage differs from the original')
    for path, manifest in zip(roots, manifests):
        metadata = manifest['.']
        path.mkdir(mode=metadata['mode'])
        os.chown(path, metadata['uid'], metadata['gid'])
        path.chmod(metadata['mode'])
        for name, value in metadata['xattrs'].items():
            os.setxattr(path, name, base64.b64decode(value))
        current = tree_manifest(path)
        if current != {'.': metadata}:
            raise RuntimeError('Empty active root differs from its required metadata')
        proof['empty_roots'].append(str(path))
        save(root, 'storage-preservation.json', proof)
    return proof


def verify_preserved_stores(root):
    proof = json.loads((root / 'storage-preservation.json').read_text())
    if (len(proof['moved']) != 3 or proof['empty_roots'] != proof['roots']
            or file_digest(Path(proof['archive'])) != proof['archive_sha256']):
        raise RuntimeError('Storage preservation is incomplete or changed')
    for move, manifest in zip(proof['moved'], proof['manifests']):
        if tree_manifest(Path(move['destination'])) != manifest:
            raise RuntimeError('Preserved preparation storage changed')
    return proof


def later_ca_samples(specs, samples):
    if set(samples) != {spec['pv'] for spec in specs}:
        raise RuntimeError('CA sample inventory differs from selected PVs')
    for spec in specs:
        sample = samples[spec['pv']]
        if not 0 <= sample['nanos'] < 1000000000:
            raise RuntimeError('Invalid CA nanoseconds')
        if (sample['secs'], sample['nanos']) <= max((row['secs'], row['nanos']) for row in spec['input']):
            return False
    return True


def shutdown_modes(specs):
    for spec in specs:
        modes = [urllib.parse.parse_qs(urllib.parse.urlsplit(url).query) for url in spec['stores']]
        if (modes[0].get('consolidateOnShutdown') != ['true']
                or modes[1].get('consolidateOnShutdown', ['false']) != ['false']
                or any(mode.get('reducedata') for mode in modes[:2])):
            raise RuntimeError('Unsupported shutdown transfer settings: ' + spec['pv'])


def shutdown_preservation(specs, before, after):
    shutdown_modes(specs)
    proof = {}
    for spec in specs:
        pv = spec['pv']
        source = [row for file in before[pv][0] for row in file['events']]
        if not source:
            raise RuntimeError('Readable pre-stop STS events are required: ' + pv)
        timestamps = {(row['secs'], row['nanos']) for row in source}
        def known(snapshot, tiers):
            return [row for tier in tiers for file in snapshot[pv][tier] for row in file['events']
                    if (row['secs'], row['nanos']) in timestamps]
        def counts(rows):
            return collections.Counter(tuple(row[key] for key in (*FIELDS, 'raw')) for row in rows)
        expected = counts(known(before, (0, 1)))
        observed = counts(known(after, (0, 1)))
        if observed != expected or known(before, (2,)) or known(after, (2,)):
            raise RuntimeError('Known shutdown source events differ: ' + pv)
        proof[pv] = {'source_occurrences': len(source), 'known_occurrences': sum(expected.values()),
                     'result': 'Passed'}
    return proof


def compare_physical(specs, baseline, snapshot):
    output = {}
    for spec in specs:
        pv, begin, end = spec['pv'], spec['old'], spec['old'] + 300
        original = events(baseline, pv, 0, begin, end)
        expected = [original[index] for index in spec['expected_old_indices']]
        actual = events(snapshot, pv, 2, begin, end)
        if actual != expected:
            raise RuntimeError('Physical LTS events differ: ' + pv)
        if events(snapshot, pv, 0, begin, end) or events(snapshot, pv, 1, begin, end):
            raise RuntimeError('Historical source events remain: ' + pv)
        paths = [file['path'] for file in baseline[pv][0]
                 if any(begin <= row['secs'] < end for row in file['events'])]
        if not paths or any(Path(path).exists() for path in paths) or Path(snapshot[pv + '#oldMTSPath']).exists():
            raise RuntimeError('Historical source files remain: ' + pv)
        output[pv] = expected
    return output


def http_interval(output, pv, begin, end):
    if len(output) != 1 or output[0].get('meta', {}).get('name') != pv:
        raise RuntimeError('HTTP response must identify the requested PV')
    return [{key: row[key] for key in FIELDS} for row in output[0].get('data', [])
            if begin <= row['secs'] < end]


def compare_http(root, expected, specs, label):
    hashes = {}
    for spec in specs:
        begin = dt.datetime.fromtimestamp(spec['old'], dt.timezone.utc).isoformat()
        end = dt.datetime.fromtimestamp(spec['old'] + 300, dt.timezone.utc).isoformat()
        result = request('data/getData.json', retrieval=True, pv=spec['pv'], **{'from': begin, 'to': end})
        name = label + '-http-' + spec['pv'].replace(':', '_') + '.json'
        save(root, name, result)
        hashes[str(root / name)] = contract.digest(root / name)
        wanted = [{key: row[key] for key in FIELDS} for row in expected[spec['pv']]]
        if http_interval(result, spec['pv'], spec['old'], spec['old'] + 300) != wanted:
            raise RuntimeError('HTTP events differ from the independent physical expectation')
    return hashes


def closed_bin_ends(specs):
    ends = [(spec['input'][-1]['secs'] // (spec['interval'] or 60) + 1)
            * (spec['interval'] or 60) for spec in specs]
    settled_at = max(ends) + BIN_SETTLE_SECONDS
    remaining = settled_at - time.time()
    if remaining > 0:
        wait_until('recent bins closed', lambda: time.time() >= settled_at, remaining + START_TIMEOUT)
    return ends


def capture_recent_bins(root, classpath, specs):
    ends = closed_bin_ends(specs)
    snapshot = pb(root, classpath, 'snapshot', 'recent-bin-source.json')
    proof = {}
    for spec, end in zip(specs, ends):
        begin = end - (spec['interval'] or 60)
        source = sorted(events(snapshot, spec['pv'], 0, begin, end)
                        + events(snapshot, spec['pv'], 1, begin, end),
                        key=lambda row: (row['secs'], row['nanos'], row['raw']))
        marker = spec['input'][-1]
        if (not source or events(snapshot, spec['pv'], 2, begin, end)
                or sum(all(row[key] == marker[key] for key in FIELDS) for row in source) != 1):
            raise RuntimeError('Closed recent bin must be captured before reduction with one original marker')
        if len({(row['secs'], row['nanos']) for row in source}) != len(source):
            raise RuntimeError('Ambiguous timestamp multiplicity in closed recent bin')
        output = request('data/getData.json', retrieval=True, pv=spec['pv'], **{
            'from': dt.datetime.fromtimestamp(begin, dt.timezone.utc).isoformat(),
            'to': dt.datetime.fromtimestamp(end, dt.timezone.utc).isoformat()})
        save(root, 'recent-source-http-' + spec['pv'].replace(':', '_') + '.json', output)
        wanted = [{key: row[key] for key in FIELDS} for row in source]
        if http_interval(output, spec['pv'], begin, end) != wanted:
            raise RuntimeError('Closed recent bin physical and HTTP inputs differ')
        proof[spec['pv']] = {'begin': begin, 'end': end, 'source': source,
                             'reduced': [max(source, key=lambda row: (row['secs'], row['nanos']))]
                             if spec['interval'] else source}
    save(root, 'recent-bin-expectations.json', proof)
    return proof


def retention(specs, snapshot, records, chain, invocation, recent_bins=None):
    granularities = contract.chain_configuration(chain)['granularities']
    completed = {index: max([row for row in records if row['transition'] == index
                            and row['invocation_id'] == invocation],
                           key=lambda row: evaluate.epoch(row['endedAt'])) for index in (0, 1)}
    recent_output = {}
    for spec in specs:
        for marker in spec['input'][-2:]:
            tier = 0
            for index in (0, 1):
                seconds = contract.PARTITION_SECONDS[granularities[index]]
                processing = evaluate.epoch(completed[index]['processingTime'])
                cutoff = int((processing - 2 * seconds) // seconds) * seconds - 1
                if marker['secs'] > cutoff:
                    break
                tier += 1
            if marker is spec['input'][-1] and recent_bins is not None:
                bin_proof = recent_bins[spec['pv']]
                expected = bin_proof['reduced'] if tier == 2 else bin_proof['source']
                for store in range(3):
                    actual = events(snapshot, spec['pv'], store, bin_proof['begin'], bin_proof['end'])
                    if actual != (expected if store == tier else []):
                        raise RuntimeError('Closed recent bin differs from its captured source expectation')
                recent_output[spec['pv']] = dict(bin_proof, expected=expected)
                continue
            if tier == 2 and marker is spec['input'][-1] and spec['interval']:
                raise RuntimeError('Reduced recent retention requires a closed-bin source proof')
            counts = [sum(all(row[key] == marker[key] for key in FIELDS)
                          for row in events(snapshot, spec['pv'], store, marker['secs'], marker['secs'] + 1))
                      for store in range(3)]
            if counts != [int(store == tier) for store in range(3)]:
                raise RuntimeError('Recent/intermediate marker retention differs from processing time')
    return recent_output


def compare_recent_http(root, bins, label):
    hashes = {}
    for pv, proof in bins.items():
        output = request('data/getData.json', retrieval=True, pv=pv, **{
            'from': dt.datetime.fromtimestamp(proof['begin'], dt.timezone.utc).isoformat(),
            'to': dt.datetime.fromtimestamp(proof['end'], dt.timezone.utc).isoformat()})
        path = root / (label + '-recent-http-' + pv.replace(':', '_') + '.json')
        save(root, path.name, output)
        hashes[str(path)] = contract.digest(path)
        wanted = [{key: row[key] for key in FIELDS} for row in proof['expected']]
        if http_interval(output, pv, proof['begin'], proof['end']) != wanted:
            raise RuntimeError('Recent bin HTTP events differ from the captured source expectation')
    return hashes


def passes(root, invocation):
    text = observe.checked(['journalctl', '-u', collect.UNIT, '_SYSTEMD_INVOCATION_ID=' + invocation,
                            '--no-pager', '-o', 'json'])
    path = root / ('passes-' + invocation + '.jsonl')
    records = []
    for line in text.splitlines():
        row = json.loads(line)
        if evaluate.PASS.search(row.get('MESSAGE', '')):
            records.append(line)
    path.write_text(''.join(line + '\n' for line in records))
    return evaluate.pass_records(path)


def successful_pass(row):
    keys = ('jobsFailed', 'jobsAborted', 'jobsSkipped', 'streamsDeletedForSpace')
    if (row['overrun'] != 'false' or row['aborted'] != 'false' or int(row['pvCount']) != 903
            or int(row['jobsRun']) != 903 or any(int(row[key]) for key in keys)):
        raise RuntimeError('Automatic pass failed its execution contract')


def regular_passes(records, chain, invocation):
    config = contract.chain_configuration(chain)
    selected_rows = []
    for row in records:
        if row['invocation_id'] == invocation:
            successful_pass(row)
    for transition, (cadence, offset) in enumerate(zip(config['cadences'], config['offsets'])):
        rows = sorted([row for row in records if row['invocation_id'] == invocation
                       and row['transition'] == transition and row['cadence'] == cadence],
                      key=lambda row: evaluate.epoch(row['startedAt']))
        if len(rows) < 2:
            return None
        candidates = [row for row in rows[1:] if (int(evaluate.epoch(row['plannedAt'])) - offset) % cadence == 0]
        if not candidates:
            return None
        if any(count != 1 for count in collections.Counter(row['plannedAt'] for row in candidates).values()):
            raise RuntimeError('Duplicate regular pass identity')
        row = candidates[0]
        began, planned, ended = (evaluate.epoch(row[key]) for key in ('startedAt', 'plannedAt', 'endedAt'))
        blockers = [prior for prior in records if prior['transition'] < transition
                    and evaluate.epoch(prior['startedAt']) <= began and evaluate.epoch(prior['endedAt']) > planned]
        ready = max([planned, *[evaluate.epoch(prior['endedAt']) for prior in blockers]])
        if not 0 <= began - ready <= 5 or ended < began:
            raise RuntimeError('Regular pass timing or ordering failed')
        if abs(began - evaluate.epoch(row['processingTime']) - 60) > 0.000002:
            raise RuntimeError('Processing margin differs from sixty seconds')
        selected_rows.append(row)
    return selected_rows


def ready():
    for component, port in zip(COMPONENTS, range(17665, 17669)):
        try:
            with CLIENT.open('http://127.0.0.1:%d/%s/bpl/startupState' % (port, component), timeout=10) as response:
                if json.load(response).get('status') != 'STARTUP_COMPLETE':
                    return False
        except (urllib.error.URLError, TimeoutError) as error:
            print('Startup HTTP not ready: ' + str(error), flush=True)
            return False
    return True


def wait_until(description, predicate, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        print('Waiting for ' + description, flush=True)
        time.sleep(5)
    raise RuntimeError('Timeout waiting for ' + description)


def configure_debug(root):
    source = INSTALL / 'etl/webapps/etl/WEB-INF/classes/log4j2.xml'
    tree = ET.fromstring(source.read_text())
    loggers = tree.find('Loggers')
    if loggers is None or any(row.get('name') == LOGGER for row in loggers):
        raise RuntimeError('Unexpected existing pass logger configuration')
    ET.SubElement(loggers, 'Logger', name=LOGGER, level='debug')
    target = root / 'log4j2.xml'
    ET.ElementTree(tree).write(target, encoding='utf-8', xml_declaration=True)
    target.chmod(0o644)
    dropin = observe.UNITS / (collect.UNIT + '.d') / '30-etl-focused.conf'
    expected = '[Service]\nEnvironment="LOG4J_CONFIGURATION_FILE=' + str(target) + '"\n'
    reused = dropin.exists()
    if reused and dropin.read_text() != expected:
        raise RuntimeError('Focused logging configuration differs from the required path')
    dropin.parent.mkdir(parents=True, exist_ok=True)
    if not reused:
        dropin.write_text(expected)
    save(root, 'logging-configuration.json', {'reused': reused, 'dropin': str(dropin),
                                           'dropin_sha256': contract.digest(dropin),
                                           'configuration_sha256': contract.digest(target)})
    observe.checked(['systemctl', 'daemon-reload'])


def live_population(root, recorded, name):
    rows = request('getPVStatus', pv='AASOAK*')
    names = {row['pv'] for row in recorded['pvs']}
    if len(rows) != len(names) or {row['pvName'] for row in rows} != names:
        raise RuntimeError('Live fixture population differs from the registered 903 names')
    save(root, name, {'observed_at': now(), 'records': rows})
    return all(row.get('status') == 'Being archived' and row.get('connectionState') == 'true' for row in rows)


def check_preparation(root, result):
    binding_path = root / 'preparation-binding.json'
    if file_digest(binding_path) != result['preparation_binding_sha256']:
        raise RuntimeError('Preparation binding changed during verification')
    binding = json.loads(binding_path.read_text())
    if any(file_digest(Path(path)) != digest for path, digest in binding['files'].items()):
        raise RuntimeError('Immutable preparation evidence changed')
    verify_preserved_stores(root)
    if binding['source_pins'] != {'env': ENV_HEAD, 'maven': MAVEN_HEAD}:
        raise RuntimeError('Preparation source pins differ from the approved commits')


def run(root, chain):
    protect()
    root.mkdir(mode=0o755)
    root.chmod(0o755)
    result = {'result': 'Incomplete', 'started_at': now(), 'chain': chain}
    save(root, 'result.json', result)
    def stage(name):
        result['stage'] = name
        save(root, 'result.json', result)
    try:
        stage('registered-live-preparation')
        recorded = inventory(root, chain)
        if not live_population(root, recorded, 'live-before-stop.json'):
            raise RuntimeError('All 903 registered PVs must be connected and archiving before preparation')
        classpath = compile_helper(root)
        specs = specifications(recorded, int(time.time()) + 3)
        save(root, 'manifest.json', {'pvs': specs})
        before_stop = pb(root, classpath, 'snapshot', 'before-stop.json')
        baseline_check(specs, before_stop)
        shutdown_modes(specs)
        configure_debug(root)
        stage('normal-shutdown-preservation')
        observe.checked(['systemctl', 'stop', collect.UNIT])
        if collect.resources.jvm_pids():
            raise RuntimeError('JVMs remain after normal stop')
        # Recent fixture time is chosen after stop so the shipped writer remains monotonic.
        previous_windows = {spec['pv']: spec['snapshot_windows'] for spec in specs}
        specs = specifications(recorded, int(time.time()) + 1)
        for spec in specs:
            for window in previous_windows[spec['pv']]:
                if window not in spec['snapshot_windows']:
                    spec['snapshot_windows'].append(window)
        save(root, 'manifest.json', {'pvs': specs})
        preliminary = pb(root, classpath, 'snapshot', 'before-seed.json')
        baseline_check(specs, preliminary, require_live=False)
        save(root, 'shutdown-preservation.json', shutdown_preservation(specs, before_stop, preliminary))
        observe.checked(['systemctl', 'stop', collect.IOC_UNIT])
        offline()
        stage('offline-storage-preservation')
        database = database_snapshot(root, 'database-before-storage.sql')
        roots = [Path(mode['rootFolder']) for mode in selected(recorded)[0][0]['effective']['modes']]
        preserve_stores(root, roots)
        offline()
        empty = pb(root, classpath, 'snapshot', 'empty-tiers.json')
        empty_paths(specs, empty)
        stage('offline-seed-baseline')
        specs = specifications(recorded, int(time.time()) + 1)
        save(root, 'manifest.json', {'pvs': specs})
        baseline = pb(root, classpath, 'seed', 'baseline.json')
        account = pwd.getpwnam('mid-srv')
        for spec in specs:
            for path in baseline[spec['pv'] + '#createdPaths']:
                os.chown(path, account.pw_uid, account.pw_gid)
        baseline_check(specs, baseline, seeded=True)
        empty_paths(specs, baseline, seeded=True)
        if database_snapshot(root, 'database-after-seed.sql') != database:
            raise RuntimeError('Registration database changed during offline preparation')
        if artifacts() != recorded['artifacts'] or observe.tool_hashes() != recorded['tools']:
            raise RuntimeError('Installed artifacts or tools changed during preparation')
        offline()
        stage('live-ca-timestamp-gate')
        observe.checked(['systemctl', 'start', collect.IOC_UNIT])
        ca_attempt = 0
        def later():
            nonlocal ca_attempt
            ca_attempt += 1
            samples = pb(root, classpath, 'ca', 'ca-attempt-%03d.json' % ca_attempt)
            if later_ca_samples(specs, samples):
                save(root, 'ca-before-start.json', samples)
                return samples
            return None
        wait_until('actual CA timestamps later than the last seed', later, START_TIMEOUT)
        source_check = pb(root, classpath, 'snapshot', 'baseline-before-start.json')
        if any(source_check[spec['pv']] != baseline[spec['pv']] for spec in specs):
            raise RuntimeError('Seeded storage changed before normal startup')
        preserved = verify_preserved_stores(root)
        immutable = [root / name for name in
                     ('inventory.json', 'manifest.json', 'before-stop.json', 'before-seed.json',
                      'shutdown-preservation.json', 'storage-preservation.json', 'empty-tiers.json',
                      'baseline.json', 'baseline-before-start.json', 'ca-before-start.json',
                      'database-before-storage.sql', 'database-after-seed.sql', 'logging-configuration.json')]
        immutable.extend((root / 'helper-classes').rglob('*.class'))
        binding = {'observed_at': now(), 'chain': chain, 'source_pins': recorded['artifacts']['heads'],
                   'preparation_identity': recorded['identity'], 'tools': recorded['tools'],
                   'archive_sha256': preserved['archive_sha256'],
                   'files': {str(path): file_digest(path) for path in immutable}}
        save(root, 'preparation-binding.json', binding)
        result['preparation_binding_sha256'] = file_digest(root / 'preparation-binding.json')
        stage('normal-startup-and-automatic-transfer')
        observe.checked(['systemctl', 'start', collect.UNIT])
        wait_until('appliance startup', ready, START_TIMEOUT)
        running = identity()
        wait_until('all 903 live PVs after startup',
                   lambda: live_population(root, recorded, 'live-after-start.json'), START_TIMEOUT)
        finish_run(root, chain, recorded, classpath, specs, baseline, running, result)
    except BaseException as error:
        result['result'] = 'Incomplete'
        result['error'] = str(error)
        raise
    finally:
        result['finished_at'] = now()
        save(root, 'result.json', result)


def finish_run(root, chain, recorded, classpath, specs, baseline, running, result,
               resume_guard=None, expected_tools=None):
    if artifacts() != recorded['artifacts']:
        raise RuntimeError('Artifacts changed during focused startup')
    def startup():
        records = passes(root, running['invocation_id'])
        for row in records:
            successful_pass(row)
        return records if {row['transition'] for row in records} == {0, 1} else None
    wait_until('both automatic startup passes', startup, START_TIMEOUT)
    snapshot = pb(root, classpath, 'snapshot', 'startup.json')
    expected = compare_physical(specs, baseline, snapshot)
    retention(specs, snapshot, passes(root, running['invocation_id']), chain, running['invocation_id'])
    compare_http(root, expected, specs, 'startup')
    recent_bins = capture_recent_bins(root, classpath, specs)
    def repeated():
        if identity() != running:
            raise RuntimeError('Appliance restarted during focused repeats')
        return regular_passes(passes(root, running['invocation_id']), chain, running['invocation_id'])
    regular = wait_until('all regular transition repeats', repeated,
                         max(contract.chain_configuration(chain)['cadences']) + ORDER_MARGIN)
    snapshot = pb(root, classpath, 'snapshot', 'repeat.json')
    expected = compare_physical(specs, baseline, snapshot)
    recent_output = retention(specs, snapshot, passes(root, running['invocation_id']), chain, running['invocation_id'], recent_bins)
    compare_recent_http(root, recent_output, 'repeat')
    compare_http(root, expected, specs, 'repeat')
    pass_source = root / ('passes-' + running['invocation_id'] + '.jsonl')
    (root / 'focused-passes.jsonl').write_bytes(pass_source.read_bytes())
    final_root = root / 'final-inspection'
    final_root.mkdir()
    final = inventory(final_root, chain)
    if resume_guard is not None:
        check_resume_files(root, resume_guard, outputs_changed=True)
        if contract.digest(root / 'resume-guard.json') != result['resume_guard_sha256']:
            raise RuntimeError('Resume guard changed during execution')
        logging = json.loads((root / 'logging-configuration.json').read_text())
        if contract.digest(Path(logging['dropin'])) != logging['dropin_sha256']:
            raise RuntimeError('Original focused logging configuration changed')
    key_root = root / 'chunk-key-verification'
    key_root.mkdir()
    keys = expected_chunk_keys(key_root, recorded)
    check_chunk_paths(specs, [baseline, snapshot], keys)
    check_completion(recorded, final, running, identity(), expected_tools, keys)
    if 'preparation_binding_sha256' in result:
        check_preparation(root, result)
    result.update(result='Passed', identity=running, regular_passes=regular, artifacts=final['artifacts'],
                  pvs=final['pvs'], flags=final['flags'], tools=final['tools'],
                  source_manifest_sha256=contract.digest(root / 'manifest.json'),
                  baseline_sha256=contract.digest(root / 'baseline.json'),
                  evidence_sha256={str(path): contract.digest(path)
                      for path in [final_root / 'inventory.json',
                                   root / 'focused-passes.jsonl', root / 'startup.json', root / 'repeat.json',
                                   root / 'before-stop.json', root / 'before-seed.json',
                                   root / 'shutdown-preservation.json',
                                   root / 'logging-configuration.json',
                                   root / 'recent-bin-source.json', root / 'recent-bin-expectations.json',
                                   *root.glob('recent-source-http-*.json'),
                                   *root.glob('repeat-recent-http-*.json'),
                                   *root.glob('startup-http-*.json'), *root.glob('repeat-http-*.json')]},
                  helper_sha256={str(path): contract.digest(path) for path in (root / 'helper-classes').rglob('*.class')})
    result['evidence_sha256'].update({str(path): file_digest(path)
                                     for path in key_root.rglob('*') if path.is_file()})
    if 'preparation_binding_sha256' in result:
        result['evidence_sha256'].update({str(root / name): file_digest(root / name)
                                         for name in ('preparation-binding.json', 'live-before-stop.json',
                                                      'live-after-start.json')})


def check_completion(recorded, final, running, current, expected_tools=None, expected_keys=None):
    if expected_keys is not None:
        check_chunk_keys(recorded, final, expected_keys)
    if (any(final[key] != recorded[key] for key in ('flags', 'artifacts'))
            or expected_keys is None and final['pvs'] != recorded['pvs']):
        raise RuntimeError('Effective configuration changed during focused execution')
    if final['tools'] != (recorded['tools'] if expected_tools is None else expected_tools):
        raise RuntimeError('Focused tools changed during execution')
    if final['identity'] != running or current != running:
        raise RuntimeError('Appliance restarted before focused completion')


def check_chunk_keys(recorded, final, expected):
    before, after = recorded.get('pvs'), final.get('pvs')
    if (not isinstance(before, list) or not isinstance(after, list) or len(before) != 903
            or len(after) != 903 or len({row['pv'] for row in before}) != 903
            or {row['pv'] for row in before} != set(expected)):
        raise RuntimeError('Chunk key PV inventory differs from all 903 fixture PVs')
    for original, current in zip(before, after):
        old = original['typeinfo'].get('chunkKey')
        actual = current['typeinfo'].get('chunkKey')
        wanted = expected[original['pv']]
        if not isinstance(wanted, str) or not wanted or actual != (wanted if old is None else old):
            raise RuntimeError('Unexpected chunk key change: ' + original['pv'])
        if ({key: value for key, value in original.items() if key != 'typeinfo'} !=
                {key: value for key, value in current.items() if key != 'typeinfo'}
                or {key: value for key, value in original['typeinfo'].items() if key != 'chunkKey'} !=
                {key: value for key, value in current['typeinfo'].items() if key != 'chunkKey'}):
            raise RuntimeError('PV configuration changed beyond initial chunk key generation')


def expected_chunk_keys(root, recorded):
    candidates = [Path(name) for name, digest in recorded['artifacts']['files'].items()
                  if digest == recorded['artifacts']['properties_sha256']
                  and Path(name).name == 'archappl.properties']
    if len(candidates) != 1 or contract.digest(candidates[0]) != recorded['artifacts']['properties_sha256']:
        raise RuntimeError('Original deployed properties are required for chunk keys')
    properties = root / 'archappl.properties'
    shutil.copyfile(candidates[0], properties)
    save(root, 'key-input.json', {'pvs': [{'pv': row['pv']} for row in recorded['pvs']]})
    classes = root / 'key-classes'
    classes.mkdir()
    webinf = INSTALL / 'etl/webapps/etl/WEB-INF'
    classpath = str(webinf / 'classes') + ':' + str(webinf / 'lib/*')
    source = Path(__file__).parent / 'PBFixture.java'
    with (root / 'key-converter.log').open('x') as log:
        subprocess.run(['javac', '-proc:none', '-cp', classpath, '-d', str(classes), str(source)],
                       stdout=log, stderr=subprocess.STDOUT, check=True, timeout=120)
        subprocess.run(['java', '-Xmx256m', '-cp', str(classes) + ':' + classpath, 'PBFixture',
                        'keys', str(root / 'key-input.json'), str(root / 'expected-keys.json'), str(properties)],
                       stdout=log, stderr=subprocess.STDOUT, check=True, timeout=120)
    if contract.digest(properties) != recorded['artifacts']['properties_sha256']:
        raise RuntimeError('Chunk key properties changed during conversion')
    return json.loads((root / 'expected-keys.json').read_text())


def check_chunk_paths(specs, snapshots, expected):
    for spec in specs:
        key = expected[spec['pv']]
        if spec.get('chunkKey') is not None and spec['chunkKey'] != key:
            raise RuntimeError('Manifest key differs from deployed converter: ' + spec['pv'])
        count = 0
        for snapshot in snapshots:
            for url, files in zip(spec['stores'], snapshot[spec['pv']]):
                store = Path(urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)['rootFolder'][0])
                for row in files:
                    relative = str(Path(row['path']).relative_to(store))
                    if not re.fullmatch(re.escape(key) + r'\d{4}(?:_\d{2}){0,4}\.pb', relative):
                        raise RuntimeError('Physical PB path differs from deployed converter: ' + row['path'])
                    count += 1
        if not count:
            raise RuntimeError('Physical PB paths missing for selected PV: ' + spec['pv'])


def check_resume_files(root, guard, outputs_changed=False):
    for name, digest in guard['source_hashes'].items():
        live_output = name == 'result.json' or name == 'passes-' + guard['identity']['invocation_id'] + '.jsonl'
        if (contract.digest(root / 'resume-source' / name) != digest
                or (not (outputs_changed and live_output) and contract.digest(root / name) != digest)):
            raise RuntimeError('Original resume source changed: ' + name)


def check_resume_identity(guard, current):
    if current != guard['identity']:
        raise RuntimeError('Original appliance invocation or JVM identity changed')


def prepare_resume(root, chain):
    failure = json.loads((root / 'result.json').read_text())
    recorded = json.loads((root / 'inventory.json').read_text())
    running = identity()
    pass_files = list(root.glob('passes-*.jsonl'))
    expected = root / ('passes-' + running['invocation_id'] + '.jsonl')
    if (failure.get('result') != 'Incomplete' or failure.get('chain') != chain
            or not failure.get('error', '').startswith('Expecting value: line 1 column 1')
            or pass_files != [expected] or expected.read_text().strip() or (root / 'startup.json').exists()
            or running['boot_id'] != recorded['identity']['boot_id']):
        raise RuntimeError('Only the original empty-pass interruption can be resumed')
    boot_time = int(next(line.split()[1] for line in Path('/proc/stat').read_text().splitlines()
                         if line.startswith('btime ')))
    begin = dt.datetime.fromisoformat(failure['started_at']).timestamp()
    end = dt.datetime.fromisoformat(failure['finished_at']).timestamp()
    for process in running['jvms'].values():
        started = boot_time + int(process['start']) / os.sysconf('SC_CLK_TCK')
        if not begin - 1 <= started <= end + 1:
            raise RuntimeError('A JVM did not start in the original fixture invocation')
    specs = json.loads((root / 'manifest.json').read_text())['pvs']
    baseline_check(specs, json.loads((root / 'baseline.json').read_text()), seeded=True)
    preserved = shutdown_preservation(specs, json.loads((root / 'before-stop.json').read_text()),
                                     json.loads((root / 'before-seed.json').read_text()))
    if preserved != json.loads((root / 'shutdown-preservation.json').read_text()):
        raise RuntimeError('Original shutdown proof changed')
    source = root / 'resume-source'
    source.mkdir()
    names = ['result.json', 'inventory.json', 'manifest.json', 'baseline.json',
             'before-stop.json', 'before-seed.json', 'shutdown-preservation.json',
             'logging-configuration.json', 'log4j2.xml', expected.name]
    classes = list((root / 'helper-classes').rglob('*.class'))
    if not classes:
        raise RuntimeError('Original compiled PB helper is required')
    names.extend(str(path.relative_to(root)) for path in classes)
    hashes = {}
    for name in names:
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
        hashes[name] = contract.digest(root / name)
    guard = {'chain': chain, 'identity': running, 'prepared_at': now(), 'source_hashes': hashes}
    check_resume_files(root, guard)
    check_resume_identity(guard, identity())
    save(root, 'resume-guard.json', guard)


def resume(root, chain):
    guard = json.loads((root / 'resume-guard.json').read_text())
    if guard['chain'] != chain:
        raise RuntimeError('Resume chain differs from original fixture')
    check_resume_files(root, guard)
    check_resume_identity(guard, identity())
    recorded = json.loads((root / 'resume-source/inventory.json').read_text())
    inspection = root / 'resume-inspection'
    inspection.mkdir()
    current = inventory(inspection, chain)
    for key in ('artifacts', 'pvs', 'flags'):
        if current[key] != recorded[key]:
            raise RuntimeError('Original fixture configuration changed: ' + key)
    for name, digest in recorded['tools'].items():
        if name != 'focused.py' and current['tools'].get(name) != digest:
            raise RuntimeError('A helper other than the resumed driver changed: ' + name)
    logging = json.loads((root / 'logging-configuration.json').read_text())
    if (contract.digest(Path(logging['dropin'])) != logging['dropin_sha256']
            or contract.digest(root / 'log4j2.xml') != logging['configuration_sha256']):
        raise RuntimeError('Original focused logging configuration changed')
    check_resume_identity(guard, identity())
    specs = json.loads((root / 'manifest.json').read_text())['pvs']
    baseline = json.loads((root / 'baseline.json').read_text())
    classpath = str(root / 'helper-classes') + ':' + str(INSTALL / 'etl/webapps/etl/WEB-INF/classes') + ':' + str(INSTALL / 'etl/webapps/etl/WEB-INF/lib/*')
    result = {'result': 'Incomplete', 'chain': chain, 'started_at': now(),
              'original_started_at': json.loads((root / 'resume-source/result.json').read_text())['started_at'],
              'resume_guard_sha256': contract.digest(root / 'resume-guard.json')}
    save(root, 'result.json', result)
    try:
        finish_run(root, chain, recorded, classpath, specs, baseline, guard['identity'], result,
                   resume_guard=guard, expected_tools=current['tools'])
        result['evidence_sha256'].update({str(path): contract.digest(path)
                                         for path in (root / 'resume-source').rglob('*') if path.is_file()})
        result['evidence_sha256'][str(root / 'resume-guard.json')] = contract.digest(root / 'resume-guard.json')
        result['evidence_sha256'][str(inspection / 'inventory.json')] = contract.digest(inspection / 'inventory.json')
    except BaseException as error:
        result['result'] = 'Incomplete'
        result['error'] = str(error)
        raise
    finally:
        result['finished_at'] = now()
        save(root, 'result.json', result)


def verified_focused_result(root, chain):
    result = json.loads((root / 'result.json').read_text())
    if result.get('result') != 'Passed' or result['chain'] != chain:
        raise RuntimeError('A complete matching focused proof is required')
    if contract.digest(root / 'manifest.json') != result['source_manifest_sha256'] or contract.digest(root / 'baseline.json') != result['baseline_sha256']:
        raise RuntimeError('Focused source evidence changed')
    for group in ('evidence_sha256', 'helper_sha256'):
        if not result.get(group) or any(contract.digest(Path(path)) != digest for path, digest in result[group].items()):
            raise RuntimeError('Focused evidence or compiled helper changed')
    if 'preparation_binding_sha256' in result:
        check_preparation(root, result)
    return result


def compare_configuration(recorded, result):
    for key in ('artifacts', 'pvs', 'flags', 'tools'):
        if recorded[key] != result[key]:
            raise RuntimeError('Focused evidence differs from current ' + key)


def recheck(root, chain):
    failure = json.loads((root / 'result.json').read_text())
    if (failure.get('result') != 'Incomplete' or failure.get('chain') != chain
            or failure.get('error') != 'Effective configuration changed during focused execution'):
        raise RuntimeError('Only the retained final configuration comparison failure can be rechecked')
    destination = root / ('recheck-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
    destination.mkdir(mode=0o700)
    source_files = [path for path in root.rglob('*') if path.is_file() and destination not in path.parents
                    and not path.name.startswith('passes-')]
    source_hashes = {str(path): file_digest(path) for path in source_files}
    proof = {'result': 'Incomplete', 'chain': chain, 'started_at': now(),
             'scope': 'Retained automatic ETL execution records; no new ETL execution or soak',
             'original_result_sha256': source_hashes[str(root / 'result.json')]}
    try:
        recorded = json.loads((root / 'inventory.json').read_text())
        final = json.loads((root / 'final-inspection/inventory.json').read_text())
        running = final['identity']
        check_preparation(root, failure)
        keys = expected_chunk_keys(destination, recorded)
        check_completion(recorded, final, running, identity(), expected_keys=keys)
        current = inventory(destination, chain)
        check_completion(final, current, running, identity())
        specs = json.loads((root / 'manifest.json').read_text())['pvs']
        baseline = json.loads((root / 'baseline.json').read_text())
        baseline_check(specs, baseline, seeded=True)
        startup = json.loads((root / 'startup.json').read_text())
        repeat = json.loads((root / 'repeat.json').read_text())
        check_chunk_paths(specs, [baseline, startup, repeat], keys)
        records = evaluate.pass_records(root / 'focused-passes.jsonl')
        regular = regular_passes(records, chain, running['invocation_id'])
        if regular is None:
            raise RuntimeError('Both retained regular transition passes are required')
        startup_records = [min([row for row in records if row['transition'] == index],
                               key=lambda row: evaluate.epoch(row['endedAt'])) for index in (0, 1)]
        retention(specs, startup, startup_records, chain, running['invocation_id'])
        bins = json.loads((root / 'recent-bin-expectations.json').read_text())
        recent_source = json.loads((root / 'recent-bin-source.json').read_text())
        for spec in specs:
            pv = spec['pv']
            value = bins[pv]
            source = sorted(events(recent_source, pv, 0, value['begin'], value['end'])
                            + events(recent_source, pv, 1, value['begin'], value['end']),
                            key=lambda row: (row['secs'], row['nanos'], row['raw']))
            reduced = [max(source, key=lambda row: (row['secs'], row['nanos']))] if spec['interval'] else source
            if (not source or value['source'] != source or value['reduced'] != reduced
                    or events(recent_source, pv, 2, value['begin'], value['end'])
                    or len({(row['secs'], row['nanos']) for row in source}) != len(source)
                    or sum(all(row[key] == spec['input'][-1][key] for key in FIELDS) for row in source) != 1):
                raise RuntimeError('Retained recent expectations differ from actual PB input')
            response = json.loads((root / ('recent-source-http-' + pv.replace(':', '_') + '.json')).read_text())
            if http_interval(response, pv, value['begin'], value['end']) != [
                    {key: row[key] for key in FIELDS} for row in source]:
                raise RuntimeError('Retained recent source HTTP differs from physical input')
        for label, snapshot in (('startup', startup), ('repeat', repeat)):
            expected = compare_physical(specs, baseline, snapshot)
            for spec in specs:
                pv = spec['pv']
                response = json.loads((root / (label + '-http-' + pv.replace(':', '_') + '.json')).read_text())
                if http_interval(response, pv, spec['old'], spec['old'] + 300) != [
                        {key: row[key] for key in FIELDS} for row in expected[pv]]:
                    raise RuntimeError('Retained historical HTTP differs from physical expectation')
        recent = retention(specs, repeat, records, chain, running['invocation_id'], bins)
        for pv, value in recent.items():
            response = json.loads((root / ('repeat-recent-http-' + pv.replace(':', '_') + '.json')).read_text())
            if http_interval(response, pv, value['begin'], value['end']) != [
                    {key: row[key] for key in FIELDS} for row in value['expected']]:
                raise RuntimeError('Retained recent HTTP differs from independent reduction expectation')
        if not later_ca_samples(specs, json.loads((root / 'ca-before-start.json').read_text())):
            raise RuntimeError('Original live CA timestamp gate failed')
        check_preparation(root, failure)
        if identity() != running:
            raise RuntimeError('Appliance identity changed during retained record recheck')
        if any(file_digest(Path(path)) != digest for path, digest in source_hashes.items()):
            raise RuntimeError('Retained execution evidence changed during recheck')
        proof.update(result='Passed', identity=running, regular_passes=regular,
                     source_evidence_sha256=source_hashes, expected_keys_sha256=file_digest(destination / 'expected-keys.json'),
                     recheck_evidence_sha256={str(path): file_digest(path)
                                              for path in destination.rglob('*') if path.is_file()},
                     checker_sha256=file_digest(Path(__file__)), helper_source_sha256=file_digest(Path(__file__).parent / 'PBFixture.java'))
    except BaseException as error:
        proof['error'] = str(error)
        raise
    finally:
        proof['finished_at'] = now()
        save(destination, 'result.json', proof)
        print(str(destination / 'result.json'), flush=True)


RECHECK_ORIGINAL_ERROR = 'Effective configuration changed during focused execution'
RECHECK_ORIGINAL_FILES = ('result.json', 'inventory.json', 'manifest.json', 'baseline.json',
                          'final-inspection/inventory.json')
RECHECK_APPROVED = {
    'proofs': {
        'shortened': {
            'path': '/var/lib/etl-focused/shortened/recheck-20261009T233038265889/result.json',
            'sha256': 'eb5e0f73b134e34e4ad35603b0894ed24b597fd6916bdd765e485a8ee5041977'},
        'default': {
            'path': '/var/lib/etl-focused/default/recheck-20261009T233038375804/result.json',
            'sha256': '491bca76b849d53061b4d486ede58c6f877c776154f2dd079eca9e07673c8897'},
    },
    # Producing version of the retained-record recheck; the running focused.py differs by design.
    'checker': '4265dfac7f62cb99e0a03a5db981a3449a37dc51365f05c156a5a20d3e264fd3',
    'helper': 'df29f030028d9c920c30a2faf360045b4595b40258666ef5dff7ab4939e4fb7d',
}


def rebased(path, root, chain):
    try:
        relative = Path(path).relative_to(ROOT / chain)
    except ValueError:
        raise RuntimeError('Recorded evidence path lies outside the chain root: ' + str(path))
    return Path(root) / relative


def retained_digest(path):
    try:
        return file_digest(path)
    except OSError:
        raise RuntimeError('Retained recheck evidence is missing: ' + str(path))


def recheck_acceptance(root, chain, approved=None):
    """Accept a retained-record recheck proof for an Incomplete original result.

    Reads retained files only; the original result and the proof are never changed.
    """
    approved = RECHECK_APPROVED if approved is None else approved
    root = Path(root)
    entry = approved['proofs'].get(chain)
    if entry is None:
        raise RuntimeError('No approved recheck proof for this chain')
    proof_file = rebased(entry['path'], root, chain)
    if retained_digest(proof_file) != entry['sha256']:
        raise RuntimeError('Recheck proof differs from the approved proof')
    proof = json.loads(proof_file.read_text())
    if proof.get('result') != 'Passed' or proof.get('chain') != chain:
        raise RuntimeError('A Passed recheck proof for this chain is required')
    original = root / 'result.json'
    failure = json.loads(original.read_text())
    if (failure.get('result') != 'Incomplete' or failure.get('chain') != chain
            or failure.get('error') != RECHECK_ORIGINAL_ERROR):
        raise RuntimeError('Only the retained final configuration comparison failure can be accepted')
    if retained_digest(original) != proof.get('original_result_sha256'):
        raise RuntimeError('Original result differs from the recheck proof')
    for group in ('source_evidence_sha256', 'recheck_evidence_sha256'):
        entries = proof.get(group)
        if not isinstance(entries, dict) or not entries:
            raise RuntimeError('Recheck proof lacks ' + group)
        for path, digest in entries.items():
            if retained_digest(rebased(path, root, chain)) != digest:
                raise RuntimeError('Retained recheck evidence changed: ' + str(path))
    source = proof['source_evidence_sha256']
    for name in RECHECK_ORIGINAL_FILES:
        if str(ROOT / chain / name) not in source:
            raise RuntimeError('Recheck proof does not bind the original record: ' + name)
    if proof.get('checker_sha256') != approved['checker'] or proof.get('helper_source_sha256') != approved['helper']:
        raise RuntimeError('Recheck checker or helper differs from the approved producing version')
    directory = proof_file.parent
    for name in ('inventory.json', 'expected-keys.json', 'key-input.json', 'archappl.properties'):
        if str(Path(entry['path']).parent / name) not in proof['recheck_evidence_sha256']:
            raise RuntimeError('Recheck proof does not bind its own record: ' + name)
    recorded = json.loads((root / 'inventory.json').read_text())
    final = json.loads((root / 'final-inspection/inventory.json').read_text())
    current = json.loads((directory / 'inventory.json').read_text())
    names = {row['pv'] for row in recorded['pvs']}
    if len(recorded['pvs']) != 903 or len(names) != 903:
        raise RuntimeError('The original inventory must list exactly 903 distinct PVs')
    key_input = json.loads((directory / 'key-input.json').read_text())
    if len(key_input['pvs']) != 903 or {row['pv'] for row in key_input['pvs']} != names:
        raise RuntimeError('Chunk key input differs from the original inventory PVs')
    if retained_digest(directory / 'expected-keys.json') != proof.get('expected_keys_sha256'):
        raise RuntimeError('Expected chunk keys differ from the recheck proof')
    if retained_digest(directory / 'archappl.properties') != recorded['artifacts']['properties_sha256']:
        raise RuntimeError('Recheck properties differ from the original deployed properties')
    check_chunk_keys(recorded, current, json.loads((directory / 'expected-keys.json').read_text()))
    if proof.get('identity') != final['identity'] or current['identity'] != final['identity']:
        raise RuntimeError('Recheck proof identity differs from the original focused execution')
    return {'chain': chain, 'proof_path': str(proof_file), 'proof_sha256': entry['sha256'],
            'original_result_sha256': proof['original_result_sha256'], 'identity': proof['identity'],
            'inventory': current, 'inventory_sha256': retained_digest(directory / 'inventory.json')}


def check_recheck_configuration(acceptance, fresh):
    for key in ('artifacts', 'pvs', 'flags'):
        if fresh.get(key) != acceptance['inventory'][key]:
            raise RuntimeError('Current configuration differs from the recheck inventory: ' + key)


def check_recheck_tools(recorded_tools, bundle_root, approved=None):
    """Compare a verified bundle with the recheck-time tools, allowing the approved changes."""
    approved = RECHECK_APPROVED if approved is None else approved
    current = contract.verify_bundle(Path(bundle_root))
    if set(current) != set(recorded_tools):
        raise RuntimeError('Tool set differs from the recheck inventory')
    for name, digest in recorded_tools.items():
        if name == 'focused.py':
            continue
        expected = approved['helper'] if name == 'PBFixture.java' else digest
        if current[name] != expected:
            raise RuntimeError('A tool other than the approved replacements changed: ' + name)
    return current


def accepted_focused_result(root, chain, approved=None):
    failure = json.loads((Path(root) / 'result.json').read_text())
    if failure.get('result') == 'Passed':
        return {'result': verified_focused_result(Path(root), chain), 'recheck': None}
    return {'result': None, 'recheck': recheck_acceptance(root, chain, approved)}


def imported_modules():
    allowed = {str(Path(__file__).resolve().parent)}
    for entry in os.environ.get('PYTHONPATH', '').split(os.pathsep):
        if entry:
            allowed.add(str(Path(entry).resolve()))
    found = {}
    for name, module in sorted(sys.modules.items()):
        path = getattr(module, '__file__', None)
        if path and str(Path(path).resolve().parent) in allowed:
            found[name] = str(Path(path).resolve())
    return found


def check_recheck(chain, evidence_root, bundle_root, scratch, approved=None):
    """Accept the retained recheck proof against live appliance state and a frozen bundle copy."""
    root = Path(evidence_root) if evidence_root else ROOT / chain
    scratch = Path(scratch).resolve()
    if scratch == ROOT.resolve() or ROOT.resolve() in scratch.parents:
        raise RuntimeError('The scratch directory must lie outside the retained tree')
    scratch.mkdir(mode=0o700)
    acceptance = recheck_acceptance(root, chain, approved)
    fresh = inventory(scratch, chain, bundle_root=bundle_root)
    check_recheck_configuration(acceptance, fresh)
    check_recheck_tools(acceptance['inventory']['tools'], bundle_root, approved)
    result = {'result': 'Passed', 'observed_at': now(), 'chain': chain,
              'proof_sha256': acceptance['proof_sha256'],
              'original_result_sha256': acceptance['original_result_sha256'],
              'focused_sha256': file_digest(Path(__file__)), 'python': sys.version,
              'bundle_root': str(Path(bundle_root).resolve()), 'modules': imported_modules()}
    save(scratch, 'recheck-acceptance.json', result)
    return result


def continuity(root, chain):
    accepted = accepted_focused_result(root, chain)
    name = 'continuity-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    inventory_name = name + '-inventory.json'
    recorded = inventory(root, chain, inventory_name)
    if accepted['recheck'] is None:
        compare_configuration(recorded, accepted['result'])
    else:
        check_recheck_configuration(accepted['recheck'], recorded)
        check_recheck_tools(accepted['recheck']['inventory']['tools'], observe.TOOLS)
    specs = json.loads((root / 'manifest.json').read_text())['pvs']
    classpath = str(root / 'helper-classes') + ':' + str(INSTALL / 'etl/webapps/etl/WEB-INF/classes') + ':' + str(INSTALL / 'etl/webapps/etl/WEB-INF/lib/*')
    snapshot = pb(root, classpath, 'snapshot', name + '.json')
    expected = compare_physical(specs, json.loads((root / 'baseline.json').read_text()), snapshot)
    current_records = passes(root, recorded['identity']['invocation_id'])
    if {row['transition'] for row in current_records} != {0, 1}:
        raise RuntimeError('Current invocation lacks automatic startup pass evidence')
    for row in current_records:
        successful_pass(row)
    recent_output = retention(specs, snapshot, current_records, chain, recorded['identity']['invocation_id'],
                              json.loads((root / 'recent-bin-expectations.json').read_text()))
    http_hashes = compare_http(root, expected, specs, name)
    http_hashes.update(compare_recent_http(root, recent_output, name))
    if identity() != recorded['identity']:
        raise RuntimeError('Appliance restarted during continuity readback')
    proof = {'observed_at': now(), 'chain': chain, 'identity': recorded['identity'],
             'focused_result_sha256': contract.digest(root / 'result.json'),
             'inventory_sha256': contract.digest(root / inventory_name),
             'inventory_path': str(root / inventory_name),
             'physical_sha256': contract.digest(root / (name + '.json')), 'physical_path': str(root / (name + '.json')),
             'http_sha256': http_hashes,
             'pass_sha256': contract.digest(root / ('passes-' + recorded['identity']['invocation_id'] + '.jsonl')),
             'pass_path': str(root / ('passes-' + recorded['identity']['invocation_id'] + '.jsonl')),
             'tools': recorded['tools'], 'result': 'Passed'}
    if accepted['recheck'] is not None:
        proof['recheck_proof_sha256'] = accepted['recheck']['proof_sha256']
        proof['recheck_proof_path'] = accepted['recheck']['proof_path']
    save(observe.OUT, 'readiness-continuity.json', proof)
    return proof


def require_continuity(chain):
    proof = json.loads((observe.OUT / 'readiness-continuity.json').read_text())
    root = ROOT / chain
    age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(proof['observed_at'])).total_seconds()
    if (proof.get('result') != 'Passed' or proof['chain'] != chain or not 0 <= age <= 120
            or proof['identity'] != identity() or proof['tools'] != observe.tool_hashes()
            or proof['focused_result_sha256'] != contract.digest(root / 'result.json')
            or not proof.get('inventory_path')
            or Path(proof['inventory_path']).parent != root
            or Path(proof['inventory_path']).name == 'inventory.json'
            or proof['inventory_sha256'] != contract.digest(Path(proof['inventory_path']))
            or proof['physical_sha256'] != contract.digest(Path(proof['physical_path']))
            or proof['pass_sha256'] != contract.digest(Path(proof['pass_path']))
            or not proof.get('http_sha256')
            or any(contract.digest(Path(path)) != digest for path, digest in proof['http_sha256'].items())):
        raise RuntimeError('Current focused continuity evidence is required')
    accepted = accepted_focused_result(root, chain)
    if accepted['recheck'] is None:
        if 'recheck_proof_sha256' in proof:
            raise RuntimeError('Continuity names a recheck proof for a Passed original result')
    elif (proof.get('recheck_proof_sha256') != accepted['recheck']['proof_sha256']
            or proof['focused_result_sha256'] != accepted['recheck']['original_result_sha256']):
        raise RuntimeError('Continuity does not bind both the original result and the recheck proof')
    return proof


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('inventory', 'run', 'prepare-resume', 'resume', 'continuity', 'recheck',
                                           'check-recheck'))
    parser.add_argument('--chain', required=True, choices=contract.CHAINS)
    parser.add_argument('--evidence-root', help='check-recheck: chain evidence root, default the retained tree')
    parser.add_argument('--bundle-root', help='check-recheck: directory of the frozen bundle to compare')
    parser.add_argument('--scratch', help='check-recheck: new private directory outside the retained tree')
    args = parser.parse_args()
    if args.action == 'check-recheck':
        if not args.bundle_root or not args.scratch:
            parser.error('check-recheck requires --bundle-root and --scratch')
        print(json.dumps(check_recheck(args.chain, args.evidence_root, args.bundle_root, args.scratch),
                         indent=2, sort_keys=True))
        return
    protect()
    ROOT.mkdir(mode=0o755, exist_ok=True)
    ROOT.chmod(0o755)
    root = ROOT / ('inventory-' + args.chain if args.action == 'inventory' else args.chain)
    with collect.locked(ROOT / (args.chain + '.lock')):
        if args.action == 'run':
            run(root, args.chain)
        else:
            root.mkdir(mode=0o755, exist_ok=True)
            root.chmod(0o755)
            {'inventory': inventory, 'continuity': continuity, 'recheck': recheck,
             'prepare-resume': prepare_resume, 'resume': resume}[args.action](root, args.chain)


if __name__ == '__main__':
    main()
