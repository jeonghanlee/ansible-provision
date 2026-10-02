#!/usr/bin/env python3
"""Verify real freshness rejection and terminal paths before opening a retest."""

import argparse
import datetime
import grp
import hashlib
import json
import os
from pathlib import Path
import pwd
import time
from unittest.mock import patch

import collect
import observe
import contract
import journal_retention

EMPTY_WINDOW_EPOCH = 946684800

def empty_data(duration, chain):
    contract.preparation(observe.OUT, duration, chain)
    journal_retention.validate(observe.OUT / 'journal-retention-proof.json', observe.TOOLS)
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('Runtime preflight requires no observation')
    with patch('time.time', return_value=EMPTY_WINDOW_EPOCH):
        failed = collect.sample(observe.OUT, observe.TOOLS / 'pvs-all.csv')
    latest = json.loads((observe.OUT / 'latest-full.json').read_text())
    rows = json.loads((Path(latest['raw_directory']) / 'freshness.json').read_text())
    missing = sum(row.get('http') == 200 and row['outcome'] == 'no_sample_in_window' for row in rows)
    if not failed or missing != 903:
        raise RuntimeError('The negative collection must fail before testing readiness')
    rejected = False
    try:
        observe.start(duration, chain)
    except RuntimeError as error:
        rejected = 'recent successful full sample' in str(error)
    if (observe.OUT / 'observation.json').exists():
        observe.terminal(aborted=True, reason='Unexpected start during negative readiness verification')
        raise RuntimeError('Negative readiness unexpectedly opened an observation; aborted')
    record = {'clock_boundary_substituted': True, 'real_appliance_and_fixture': True,
              'duration_seconds': duration, 'configuration': contract.chain_configuration(chain),
              'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'boot_id': observe.BOOT.read_text().strip(),
              'http_200_pvs_without_recent_samples': missing,
              'empty_response_pvs': sum(row.get('returned_samples') == 0 for row in rows),
              'collector_failed': failed, 'start_rejected': rejected,
              'tool_hashes': observe.tool_hashes(),
              'sample': latest['raw_directory'], 'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    collect.write_json(observe.OUT / 'empty-data-verification.json', record)
    if not rejected:
        raise RuntimeError('Negative readiness verification failed')
    print(json.dumps(record))


def abort_probe(duration, chain):
    prepared = contract.preparation(observe.OUT, duration, chain)
    main = observe.OUT
    if (main / 'observation.json').exists():
        raise RuntimeError('Terminal preflight requires no observation')
    now = datetime.datetime.now(datetime.timezone.utc)
    probe = main.with_name(main.name + '-terminal-probe-' + now.strftime('%Y%m%dT%H%M%S.%fZ'))
    probe.mkdir(mode=0o710)
    os.chown(probe, 0, grp.getgrnam('mid').gr_gid)
    probe.chmod(0o710)
    journal_retention.install_proof(main / 'journal-retention-proof.json', probe / 'journal-retention-proof.json')
    collect.write_json(probe / 'preparation.json', prepared)
    (probe / 'jvm').mkdir(mode=0o700)
    user = pwd.getpwnam('mid-srv')
    os.chown(probe / 'jvm', user.pw_uid, user.pw_gid)
    collect.write_json(probe / 'state.json', {
        'kernel_journal_since': now.strftime('%Y-%m-%d %H:%M:%S.%f UTC'),
        'journal_since': now.strftime('%Y-%m-%d %H:%M:%S.%f UTC'),
        'health_journal_since': now.strftime('%Y-%m-%d %H:%M:%S.%f UTC')})
    observe.checked(['systemctl', 'start', collect.HEALTH_UNIT])
    if collect.sample(probe, observe.TOOLS / 'pvs-all.csv'):
        raise RuntimeError('Probe full collection failed; retained the probe directory')
    latest = json.loads((probe / 'latest-full.json').read_text())
    journal_proof = journal_retention.validate(probe / 'journal-retention-proof.json', observe.TOOLS)
    state = json.loads((probe / 'state.json').read_text())
    state['journal_retention_snapshot'] = journal_proof['current']
    state['journal_retention_bounds'] = {stream: max(value,
        state.get('journal_retention_bounds', {}).get(stream, 0))
        for stream, value in journal_proof['current_budget']['rates_bytes_per_second'].items()}
    collect.write_json(probe / 'state.json', state)
    now = datetime.datetime.now(datetime.timezone.utc)
    end = now + datetime.timedelta(seconds=duration)
    manifest = {'started_at': now.isoformat(), 'earliest_finish_at': end.isoformat(),
                'duration_seconds': duration, 'boot_id': observe.BOOT.read_text().strip(),
                'measurement_schema': contract.SCHEMA, 'configuration': prepared['configuration'],
                'tool_hashes': observe.tool_hashes(),
                'journal_retention': journal_proof,
                'monotonic_start': time.monotonic(), 'unit_before_observation': observe.unit_state(),
                'health_verification': json.loads((main / 'health-verification.json').read_text()),
                'expected_firings': observe.expected_firings(now, end, prepared['configuration']),
                'counter_baseline': str(Path(latest['raw_directory']) / 'metrics.json'),
                'baseline_observed_at': latest['metrics_observed_at']}
    collect.write_json(probe / 'observation.json', manifest)
    observe.OUT = probe
    early_rejected, repeat_rejected = False, False
    try:
        try:
            observe.finish()
        except RuntimeError as error:
            early_rejected = 'window has not elapsed' in str(error)
        if not early_rejected:
            raise RuntimeError('The installed finish guard did not reject an early finish')
        observe.terminal(aborted=True, reason='Installed terminal-path preflight')
        terminal = json.loads((probe / 'abort.json').read_text())
        try:
            observe.finish()
        except RuntimeError as error:
            repeat_rejected = 'terminal operation' in str(error)
        record = {'normal_finish_guard_rejected': early_rejected, 'repeated_finish_rejected': repeat_rejected,
                  'duration_seconds': duration, 'configuration': prepared['configuration'],
                  'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'boot_id': observe.BOOT.read_text().strip(),
                  'verdict': terminal['verdict'], 'stop_rc': terminal['stop']['rc'],
                  'stop_seconds': terminal['stop_elapsed_seconds'], 'errors': terminal['errors'],
                  'complete_gc_components': sorted(terminal['complete_gc_recordings']),
                  'tool_hashes': observe.tool_hashes(),
                  'probe_directory': str(probe), 'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        collect.write_json(main / 'terminal-path-verification.json', record)
        if (terminal['stop']['rc'] != 0 or not repeat_rejected or terminal['verdict'] != 'Incomplete' or
                terminal['errors'] or set(terminal['complete_gc_recordings']) != set(collect.INSTANCES)):
            raise RuntimeError('Installed abort verification failed; retained all evidence')
        print(json.dumps(record))
    finally:
        observe.OUT = main
    observe.checked(['systemctl', 'start', collect.UNIT])
    observe.checked(['systemctl', 'start', collect.HEALTH_UNIT.replace('.service', '.timer')])


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('empty', 'abort'))
    parser.add_argument('--duration-seconds', required=True, type=int, choices=contract.DURATIONS)
    parser.add_argument('--chain', required=True, choices=contract.CHAINS)
    args = parser.parse_args()
    with collect.locked(observe.OUT.parent / (observe.OUT.name + '.lifecycle.lock')):
        {'empty': empty_data, 'abort': abort_probe}[args.action](args.duration_seconds, args.chain)


if __name__ == '__main__':
    main()
