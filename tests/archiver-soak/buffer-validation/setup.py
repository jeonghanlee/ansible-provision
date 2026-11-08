#!/usr/bin/env python3
"""Install observation tools and shipped fixtures on the separate empty appliance."""

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

SOURCE = Path(os.environ['BUFFER_SOURCE_DIR'])
TOOLS = Path('/usr/local/share/buffer29')
FIXTURE = Path('/usr/local/share/etl-soak')
ROOT = Path('/var/lib/buffer29')
APP = Path('/opt/epicsarchiverap-maven')
ENV = Path('/opt/epicsarchiverap-env-src/epicsarchiverap-env')
MAVEN = ENV / 'epicsarchiverap-maven-src'
CONF = APP / 'archappl.conf'
EXPECTED = '629533a37ef889ffe3203d97538038eaaec95283'
EXPECTED_ENV = '482cf2939ea997064e4a2df64e3cb420681f4566'
FLAGS = ('--add-exports=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED '
         '--add-exports=java.base/jdk.internal.org.objectweb.asm.commons=ALL-UNNAMED '
         '-javaagent:/usr/local/share/buffer29/observer.jar=/usr/local/share/buffer29 '
         '-Dbuffer29.output=/var/lib/buffer29/preflight')


def checked(args):
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    os.environ['PATH'] = '/usr/sbin:/usr/bin:/sbin:/bin'
    os.umask(0o022)
    if ROOT.exists():
        raise RuntimeError('Refusing replacement of an existing campaign')
    if checked(['git', '-C', str(MAVEN), 'rev-parse', 'HEAD']) != EXPECTED:
        raise RuntimeError('Unexpected appliance source identity')
    if checked(['git', '-C', str(ENV), 'rev-parse', 'HEAD']) != EXPECTED_ENV:
        raise RuntimeError('Unexpected environment source identity')
    checked(['git', '-C', str(MAVEN), 'merge-base', '--is-ancestor', '6c6b973a', 'HEAD'])
    core = ['org/epics/archiverappliance/engine/model/SampleBuffer.class',
            'org/epics/archiverappliance/engine/ArchiveEngine.class',
            'org/epics/archiverappliance/engine/writer/WriterRunnable.class',
            'org/epics/archiverappliance/engine/pv/EngineContext.class',
            'edu/stanford/slac/archiverappliance/PlainPB/AppendDataStateData.class',
            'edu/stanford/slac/archiverappliance/PB/data/PBScalarDouble.class']
    installed_core = []
    for name in core:
        installed = APP / 'engine/webapps/engine/WEB-INF/classes' / name
        if digest(installed) != digest(MAVEN / 'target/classes' / name):
            raise RuntimeError('Installed class differs from the verified build: ' + name)
        installed_core.append(installed)
    checked(['systemctl', 'stop', 'epicsarchiverap-maven.service'])
    ROOT.mkdir(mode=0o755)
    TOOLS.mkdir(mode=0o755)
    FIXTURE.mkdir(mode=0o755)
    for name in ('observer.jar', 'bootstrap.jar', 'Agent.java', 'Trace.java', 'shim.c', 'PBDecode.java',
                 'runner.py', 'fast.txt', 'fixture-sha256.json', 'campaign.py'):
        shutil.copy2(SOURCE / name, TOOLS / name)
    for name in ('aasoak.db', 'load1.db', 'load2.db', 'retest-deadband.db', 'pvs-all.csv', 'register.py', 'install-fixture.py'):
        shutil.copy2(SOURCE / name, FIXTURE / name)
    manifest = json.loads((TOOLS / 'fixture-sha256.json').read_text())
    for name in ('aasoak.db', 'load1.db', 'load2.db', 'pvs-all.csv'):
        expected = manifest.get(name)
        if isinstance(expected, dict):
            expected = expected.get('sha256')
        if expected is None:
            expected = next((v for k, v in manifest.items() if Path(k).name == name), None)
        if digest(FIXTURE / name) != expected:
            raise RuntimeError('Shipped fixture digest mismatch: ' + name)
    checked(['/usr/bin/python3', str(FIXTURE / 'install-fixture.py')])
    # The approved override is the shipped database; no record is reconstructed.
    ioc = Path('/etc/systemd/system/etl-soak-ioc.service')
    command = next(line for line in ioc.read_text().splitlines() if line.startswith('ExecStart='))
    dropin = Path('/etc/systemd/system/etl-soak-ioc.service.d')
    dropin.mkdir()
    (dropin / '50-retest-deadband.conf').write_text('[Service]\nExecStart=\n' + command
                                                 + ' -d ' + str(FIXTURE / 'retest-deadband.db') + '\n')
    java_home = Path(checked(['readlink', '-f', '/usr/bin/javac'])).parent.parent
    checked(['/usr/bin/gcc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fPIC', '-shared', '-pthread',
             '-I' + str(java_home / 'include'), '-I' + str(java_home / 'include/linux'),
             str(TOOLS / 'shim.c'), '-o', str(TOOLS / 'libbuffer29.so')])
    classes = TOOLS / 'classes'
    classes.mkdir()
    web = APP / 'engine/webapps/engine/WEB-INF'
    checked(['/usr/bin/javac', '-proc:none', '-cp', str(web / 'classes') + ':' + str(web / 'lib/*'),
             '-d', str(classes), str(TOOLS / 'PBDecode.java')])
    checked(['/usr/bin/python3', '-m', 'py_compile', str(TOOLS / 'runner.py'), str(TOOLS / 'campaign.py')])
    backup = ROOT / 'archappl.conf.before-agent'
    shutil.copy2(CONF, backup)
    backup.chmod(0o600)
    contents, count = re.subn(r'^JAVA_OPTS="([^"\n]*)"$', lambda m: 'JAVA_OPTS="' + m.group(1)
                             + ' ' + FLAGS + '"', CONF.read_text(), flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError('Unexpected JAVA_OPTS configuration')
    CONF.write_text(contents)
    preload = Path('/etc/systemd/system/epicsarchiverap-maven.service.d')
    preload.mkdir(exist_ok=True)
    (preload / '90-buffer29.conf').write_text('[Service]\nEnvironment=LD_PRELOAD=/usr/local/share/buffer29/libbuffer29.so\n')
    checked(['systemctl', 'daemon-reload'])
    checked(['systemd-analyze', 'verify', str(ioc), '/etc/systemd/system/epicsarchiverap-maven.service'])
    files = list(TOOLS.glob('*')) + installed_core + [CONF, APP / 'archappl.properties', APP / 'policies.py',
            APP / 'appliances.xml', ioc, dropin / '50-retest-deadband.conf', preload / '90-buffer29.conf']
    frozen = {'source': EXPECTED, 'environment_source': EXPECTED_ENV,
              'files': {str(p): digest(p) for p in files if p.is_file()},
              'fixtures': {p.name: digest(p) for p in FIXTURE.glob('*') if p.is_file()}}
    (ROOT / 'frozen-identities.json').write_text(json.dumps(frozen, indent=2, sort_keys=True) + '\n')
    (ROOT / 'frozen-identities.json').chmod(0o600)
    print(json.dumps({'offline_setup': 'completed', 'source': EXPECTED, 'native_compilation': 'completed',
                      'fixture_files': len(frozen['fixtures']), 'preflight_started': False}))


if __name__ == '__main__':
    main()
