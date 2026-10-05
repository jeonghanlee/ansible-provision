#!/usr/bin/env python3
"""Preserve a stopped observation and install instruments for a separate retest."""

import argparse
import datetime
import grp
import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil

import collect
import measure
import observe
import contract
import journal_retention

FILES = (*contract.BUNDLE_FILES, 'bundle.json')
CAPTURE_RESERVE = contract.CAPTURE_RESERVE
HEALTH_USE_LIMIT = 85
ENV_SOURCE = Path('/opt/epicsarchiverap-env-src/epicsarchiverap-env')
SOURCE_PINS = {'env_head': 'd09dca7a604840bc3f8dcd9edd7a7434fdf6992e',
               'maven_head': 'aa953a44bd2e6fb2a299224b97d365e7753a2fd8'}
STAMP_PATH = Path('/var/tmp/archiver-build.config')
CONFIG_PATH = Path('/opt/epicsarchiverap-maven/archappl.conf')


def prepare(bundle, projected_growth, capacity_evidence, duration, chain, retention_evidence=None):
    contract.validate_duration(duration)
    configuration = contract.chain_configuration(chain)
    contract.verify_bundle(bundle)
    if retention_evidence is None:
        raise RuntimeError('Measured journal retention preparation evidence is required')
    journal_retention.validate(retention_evidence, bundle)
    retention_payload = journal_retention.preservation_payload(retention_evidence)
    if projected_growth < CAPTURE_RESERVE or not capacity_evidence.is_file():
        raise RuntimeError('A measured growth projection with a 512 MiB capture allowance is required')
    required_growth = contract.capacity_projection(capacity_evidence, duration, configuration)
    if projected_growth < required_growth:
        raise RuntimeError('Projection is smaller than the measured growth and capture allowance')
    previous = json.loads((observe.OUT / 'observation.json').read_text())
    deployment = json.loads((observe.OUT / 'deployment-verification.json').read_text())
    pins = {name: observe.checked(['git', '-C', str(path), 'rev-parse', 'HEAD'])
            for name, path in (('env_head', ENV_SOURCE),
                               ('maven_head', ENV_SOURCE / 'epicsarchiverap-maven-src'))}
    if pins != SOURCE_PINS or STAMP_PATH.read_text() != deployment['stamp']:
        raise RuntimeError('Source pins or installed configuration differ from the approved deployment')
    terminal = [observe.OUT / name for name in ('shutdown.json', 'abort.json')
                if (observe.OUT / name).exists()]
    if len(terminal) != 1 or not json.loads(terminal[0].read_text()).get('finished_at'):
        raise RuntimeError('A completed terminal record is required')
    if collect.properties(observe.unit_state()).get('ActiveState') != 'inactive':
        raise RuntimeError('The appliance must already be stopped')
    filesystem = os.statvfs(collect.STORE)
    total, free = filesystem.f_blocks * filesystem.f_frsize, filesystem.f_bavail * filesystem.f_frsize
    if (free - projected_growth < measure.MINIMUM_FREE_BYTES or
            100 * (total - free + projected_growth) / total >= HEALTH_USE_LIMIT):
        raise RuntimeError('Projected growth violates the free-space reserve or health storage threshold')
    sources = {}
    dropin_dir = observe.UNITS / (collect.HEALTH_UNIT + '.d')
    dropin = dropin_dir / '50-soak-outcome.conf'
    abort_unit = observe.UNITS / collect.ABORT_UNIT
    dropin_text = '[Service]\nExecStopPost=/usr/bin/python3 ' + str(observe.TOOLS / 'health-event.py') + '\n'
    abort_text = ('[Unit]\nDescription=Preserve and abort the ETL soak\n[Service]\n'
                  'Type=oneshot\nTimeoutStartSec=45min\nUMask=0077\n'
                  'ExecStart=/usr/bin/python3 ' + str(observe.TOOLS / 'observe.py') + ' abort\n')
    if ((dropin.exists() and dropin.read_text() != dropin_text) or
            (abort_unit.exists() and abort_unit.read_text() not in
             (abort_text, abort_text.replace('45min', '20min')))):
        raise RuntimeError('Existing retest units differ; refusing replacement')
    for name in FILES:
        source = bundle / name
        if not source.is_file():
            raise RuntimeError('Missing instrument: ' + name)
        sources[name] = source.read_bytes()
        if name.endswith('.py'):
            compile(sources[name], name, 'exec')
    evidence_contents = capacity_evidence.read_bytes()
    capacity_input = json.loads(evidence_contents)
    capacity_source_contents = [(capacity_evidence.parent / window['source_path']).read_bytes()
                                for window in capacity_input['windows']]
    finish_unit = observe.UNITS / (observe.FINISH + '.service')
    finish_text = finish_unit.read_text()
    expected_finish = 'ExecStart=/usr/bin/python3 ' + str(observe.TOOLS / 'observe.py') + ' finish'
    if expected_finish not in finish_text.splitlines() or not any(line in finish_text.splitlines() for line in
                                                                ('TimeoutStartSec=15min', 'TimeoutStartSec=45min')):
        raise RuntimeError('Unexpected finish unit; refusing an unverified replacement')
    now = datetime.datetime.now(datetime.timezone.utc)
    archive = observe.OUT.with_name(observe.OUT.name + '-completed-' + now.strftime('%Y%m%dT%H%M%S.%fZ'))
    if archive.exists() or (observe.OUT / 'measurement-tools-before-retest').exists():
        raise RuntimeError('Preservation destination already exists')
    observe.checked(['systemctl', 'stop', observe.SAMPLER + '.timer', observe.FINISH + '.timer',
                     collect.HEALTH_UNIT.replace('.service', '.timer'), collect.HEALTH_UNIT])
    observe.wait_sampler()
    shutil.copytree(observe.TOOLS, observe.OUT / 'measurement-tools-before-retest')
    preserved_units = observe.OUT / 'measurement-units-before-retest'
    preserved_units.mkdir()
    for unit in (finish_unit, abort_unit):
        if unit.exists():
            shutil.copy2(unit, preserved_units / unit.name)
    record = {'schema': contract.SCHEMA, 'duration_seconds': duration, 'configuration': configuration,
              'prepared_at': now.isoformat(), 'previous_observation': previous,
              'archive_directory': str(archive), 'existing_store_data_preserved': True,
              'source_pins': pins,
              'configuration_sha256': hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest(),
              'tool_hashes': contract.bundle_hashes(bundle)}
    collect.write_json(observe.OUT / 'retest-preservation.json', record)
    observe.OUT.rename(archive)
    archive.chmod(0o700)
    account = pwd.getpwnam('mid-srv')
    observe.OUT.mkdir(mode=0o710)
    os.chown(observe.OUT, 0, grp.getgrnam('mid').gr_gid)
    observe.OUT.chmod(0o710)
    (observe.OUT / 'jvm').mkdir(mode=0o700)
    os.chown(observe.OUT / 'jvm', account.pw_uid, account.pw_gid)
    collect.write_json(observe.OUT / 'preparation.json', record)
    journal_retention.install_payload(retention_payload, observe.OUT / 'journal-retention-proof.json')
    capacity_sources = observe.OUT / 'capacity-sources'
    capacity_sources.mkdir()
    for index, window in enumerate(capacity_input['windows']):
        data = capacity_source_contents[index]
        name = str(index) + '.json'
        (capacity_sources / name).write_bytes(data)
        window['source_path'] = 'capacity-sources/' + name
    collect.write_json(observe.OUT / 'capacity-input.json', capacity_input)
    collect.write_json(observe.OUT / 'capacity.json', {
        'observed_at': now.isoformat(), 'duration_seconds': duration, 'configuration': configuration,
        'projected_growth_bytes': projected_growth, 'available_bytes': free,
        'measured_required_growth_bytes': required_growth,
        'input_sha256': contract.digest(observe.OUT / 'capacity-input.json')})
    for name in ('measurement-config.json', 'deployment-verification.json', 'fixture-adjustment.json'):
        if (archive / name).is_file():
            shutil.copy2(archive / name, observe.OUT / name)
    collect.write_json(observe.OUT / 'state.json', {
        'kernel_journal_since': now.strftime('%Y-%m-%d %H:%M:%S.%f UTC'),
        'health_journal_since': now.strftime('%Y-%m-%d %H:%M:%S UTC'),
        'journal_since': now.strftime('%Y-%m-%d %H:%M:%S UTC')})
    for name, contents in sources.items():
        destination = observe.TOOLS / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(contents)
        destination.chmod(0o644)
    config_path = observe.OUT / 'measurement-config.json'
    if config_path.exists():
        config = json.loads(config_path.read_text())
        config['files_sha256'] = record['tool_hashes']
        collect.write_json(config_path, config)
    dropin_dir.mkdir(mode=0o755, exist_ok=True)
    dropin.write_text(dropin_text)
    dropin.chmod(0o644)
    abort_unit.write_text(abort_text)
    abort_unit.chmod(0o644)
    finish_unit.write_text(finish_text.replace('TimeoutStartSec=15min', 'TimeoutStartSec=45min'))
    observe.checked(['systemctl', 'daemon-reload'])
    observe.checked(['systemd-analyze', 'verify', str(abort_unit),
                     str(observe.UNITS / (observe.SAMPLER + '.service')),
                     str(observe.UNITS / (observe.FINISH + '.service'))])
    state = json.loads((observe.OUT / 'state.json').read_text())
    state['health_journal_since'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f UTC')
    collect.write_json(observe.OUT / 'state.json', state)
    observe.checked(['systemctl', 'start', collect.UNIT])
    observe.checked(['systemctl', 'start', collect.HEALTH_UNIT.replace('.service', '.timer')])
    print(json.dumps({'archive_directory': str(archive), 'observation_started': False}))


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('--projected-growth-bytes', required=True, type=int)
    parser.add_argument('--capacity-evidence', required=True, type=Path)
    parser.add_argument('--journal-retention-evidence', required=True, type=Path)
    parser.add_argument('--duration-seconds', required=True, type=int, choices=contract.DURATIONS)
    parser.add_argument('--chain', required=True, choices=contract.CHAINS)
    args = parser.parse_args()
    with collect.locked(observe.OUT.parent / (observe.OUT.name + '.lifecycle.lock')):
        prepare(args.bundle, args.projected_growth_bytes, args.capacity_evidence,
                args.duration_seconds, args.chain, args.journal_retention_evidence)


if __name__ == '__main__':
    main()
