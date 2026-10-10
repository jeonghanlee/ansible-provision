#!/usr/bin/env python3
"""Start a bounded observation or preserve a measured whole-unit stop."""

import argparse
import datetime
import json
import os
from pathlib import Path
import hashlib
import re
import subprocess
import time

import collect
import measure
import evaluate
import contract
import journal_retention

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')
UNITS = Path('/etc/systemd/system')
SAMPLER = 'etl-soak-sample'
FINISH = 'etl-soak-finish'
DURATION = 24 * 60 * 60
RETEST_DURATION = 7200
SAMPLER_WAIT_SECONDS = 250
PASS_WAIT_SECONDS = 180
BOOT = Path('/proc/sys/kernel/random/boot_id')


def command(args, timeout=600):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return {'command': args, 'rc': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


def checked(args):
    result = command(args)
    if result['rc']:
        raise RuntimeError('Command failed: ' + ' '.join(args))
    return result['stdout'].strip()


def stop_loaded(units):
    # A finish timer exists only after an observation opens; an unloaded unit has nothing to cancel.
    states = {unit: checked(['systemctl', 'show', unit, '--value', '-p', 'LoadState']) for unit in units}
    loaded = [unit for unit in units if states[unit] == 'loaded']
    result = command(['systemctl', 'stop', *loaded]) if loaded else {'command': [], 'rc': 0, 'stdout': '', 'stderr': ''}
    return {**result, 'load_states': states}


def unit_state():
    return checked(['systemctl', 'show', collect.UNIT, '-p', 'ActiveState', '-p', 'SubState',
                    '-p', 'Result', '-p', 'ExecMainStatus', '-p', 'TimeoutStopUSec',
                    '-p', 'MainPID', '-p', 'InvocationID'])


def tool_hashes():
    return contract.verify_bundle(TOOLS)


def start(duration=DURATION, chain='shortened'):
    manifest = OUT / 'observation.json'
    if manifest.exists():
        raise RuntimeError('An observation is already recorded; refusing to replace it')
    prepared = contract.preparation(OUT, duration, chain)
    latest = json.loads((OUT / 'latest-full.json').read_text())
    now = datetime.datetime.now(datetime.timezone.utc)
    sampled = datetime.datetime.fromisoformat(latest['observed_at'])
    if (latest.get('sample_kind') != 'full' or latest['errors'] or
            not 0 <= (now - sampled).total_seconds() <= 120):
        raise RuntimeError('A recent successful full sample is required')
    if (latest.get('archiving_pvs') != 903 or latest.get('connected_pvs') != 903 or
            latest.get('fixture_sha256') != contract.FIXTURE_SHA or
            len(latest.get('live_instances', [])) != 4 or
            not (OUT / 'passes.jsonl').stat().st_size):
        raise RuntimeError('The full fixture and real pass evidence are required')
    if latest['clock'] != 'NTPSynchronized=yes':
        raise RuntimeError('The clock must be synchronized')
    for component in collect.INSTANCES:
        evidence = latest.get('gc', {}).get(component, {})
        if not evidence.get('heap_events') or not evidence.get('pause_events'):
            raise RuntimeError('Real heap and pause events are required: ' + component)
    latency = latest.get('latency', {})
    if (latency.get('queried_pvs') != 903 or latency.get('pvs_with_recent_samples') != 903 or
            latency.get('visible_probes') != len(measure.REPRESENTATIVES)):
        raise RuntimeError('Real retrieval and visibility evidence is required')
    if latest.get('fixture_adjustment', {}).get('verified_records') != 10:
        raise RuntimeError('The approved ten-record retest fixture adjustment must be verified')
    verification = json.loads((OUT / 'health-verification.json').read_text())
    if (not verification.get('cause') or not verification.get('corrective_action') or
            verification.get('tool_hashes') != tool_hashes() or
            verification.get('boot_id') != BOOT.read_text().strip() or
            verification.get('successful_invocations', 0) < 2):
        raise RuntimeError('Executed health-correction verification is required')
    negative = json.loads((OUT / 'empty-data-verification.json').read_text())
    terminal_check = json.loads((OUT / 'terminal-path-verification.json').read_text())
    verifier_hash = hashlib.sha256((TOOLS / 'verify-runtime.py').read_bytes()).hexdigest()
    for proof in (negative, terminal_check):
        if (proof.get('duration_seconds') != duration or proof.get('configuration') != prepared['configuration'] or
                proof.get('boot_id') != BOOT.read_text().strip() or not 0 <=
                (now - datetime.datetime.fromisoformat(proof['observed_at'])).total_seconds() <= 3600):
            raise RuntimeError('Runtime proofs are stale or belong to another prepared observation')
    if (negative.get('http_200_pvs_without_recent_samples') != 903 or
            not negative.get('collector_failed') or not negative.get('start_rejected') or
            negative.get('verifier_sha256') != verifier_hash or
            terminal_check.get('verifier_sha256') != verifier_hash or
            negative.get('tool_hashes') != tool_hashes() or terminal_check.get('tool_hashes') != tool_hashes() or
            not terminal_check.get('normal_finish_guard_rejected') or
            not terminal_check.get('repeated_finish_rejected') or terminal_check.get('stop_rc') != 0 or
            terminal_check.get('errors') or set(terminal_check.get('complete_gc_components', [])) != set(collect.INSTANCES)):
        raise RuntimeError('Executed negative-readiness and installed terminal verification are required')
    capacity = json.loads((OUT / 'capacity.json').read_text())
    measured_at = datetime.datetime.fromisoformat(capacity['observed_at'])
    filesystem = os.statvfs(collect.STORE)
    available = filesystem.f_bavail * filesystem.f_frsize
    if (not 0 <= (now - measured_at).total_seconds() <= 600 or
            capacity['duration_seconds'] != duration or capacity.get('configuration') != prepared['configuration'] or
            capacity['projected_growth_bytes'] < 512 * 1024 ** 2 or
            available - capacity['projected_growth_bytes'] < measure.MINIMUM_FREE_BYTES or
            100 * (filesystem.f_blocks * filesystem.f_frsize - available + capacity['projected_growth_bytes']) /
            (filesystem.f_blocks * filesystem.f_frsize) >= 85):
        raise RuntimeError('A current capacity projection leaving 2 GiB is required')
    checked(['systemctl', 'is-active', collect.UNIT, collect.IOC_UNIT, 'mariadb.service'])
    stores = json.loads((OUT / 'chain-verification.json').read_text())
    now = datetime.datetime.now(datetime.timezone.utc)
    if (stores.get('configuration') != prepared['configuration'] or stores.get('duration_seconds') != duration or
            stores.get('verified_pvs') != 903 or stores.get('fixture_sha256') != contract.FIXTURE_SHA or
            stores.get('source_sha256') != contract.digest(OUT / 'deployed-pv-stores.json') or
            stores.get('boot_id') != BOOT.read_text().strip() or stores.get('tool_hashes') != tool_hashes() or
            not 0 <= (now - datetime.datetime.fromisoformat(stores['observed_at'])).total_seconds() <= 600):
        raise RuntimeError('Current verified deployed store configuration is required')
    deployed = json.loads((OUT / 'deployed-pv-stores.json').read_text())
    if len(deployed) != 903 or len({row['pv'] for row in deployed}) != 903:
        raise RuntimeError('Exactly 903 deployed configurations are required')
    for row in deployed:
        if contract.deployed_configuration(chain, row['dataStores']) != prepared['configuration']:
            raise RuntimeError('Deployed store evidence differs from preparation')
    before = unit_state()
    import focused
    focused_proof = focused.require_continuity(chain)
    measurement = json.loads((OUT / 'measurement-config.json').read_text())
    uptime = float(Path('/proc/uptime').read_text().split()[0])
    maximum_age = max(uptime - int(jvm['start']) / os.sysconf('SC_CLK_TCK')
                      for jvm in focused_proof['identity']['jvms'].values())
    if measurement['jfr_duration_hours'] * 3600 - maximum_age < duration + 2700:
        raise RuntimeError('JFR duration cannot cover the observation and final capture')
    journal_proof = journal_retention.validate(OUT / 'journal-retention-proof.json', TOOLS)
    now = datetime.datetime.now(datetime.timezone.utc)
    monotonic_start = time.monotonic()
    end = now + datetime.timedelta(seconds=duration)
    record = {'started_at': now.isoformat(), 'earliest_finish_at': end.isoformat(),
              'focused_continuity': focused_proof,
              'initial_sample_record': 'initial-sample.json',
              'duration_seconds': duration, 'boot_id': BOOT.read_text().strip(),
              'monotonic_start': monotonic_start, 'fixture_sha256': latest['fixture_sha256'],
              'configuration': prepared['configuration'], 'chain_verification': stores,
              'readiness_sample': latest['raw_directory'], 'unit_before_observation': before,
              'deployment': json.loads((OUT / 'deployment-verification.json').read_text()),
              'measurement_configuration': json.loads((OUT / 'measurement-config.json').read_text()),
              'measurement_schema': contract.SCHEMA, 'existing_store_data_preserved': True,
              'tool_hashes': tool_hashes(), 'health_verification': verification,
              'journal_retention': journal_proof,
              'fixture_adjustment': latest.get('fixture_adjustment'),
              'capacity': capacity, 'abort_policy': {'consecutive_failures': 2},
              'expected_firings': expected_firings(now, end, prepared['configuration']),
              'counter_baseline': str(Path(latest['raw_directory']) / 'metrics.json'),
              'baseline_observed_at': latest['metrics_observed_at'],
              'jvm_identity': {name: {key: value[key] for key in ('pid', 'start')}
                               for name, value in json.loads((OUT / 'state.json').read_text())['processes'].items()
                               if name in collect.INSTANCES}}
    timer = '[Unit]\nDescription=Finish the ETL soak observation\n[Timer]\n'
    timer += 'OnCalendar=' + end.strftime('%Y-%m-%d %H:%M:%S UTC') + '\n'
    timer += 'AccuracySec=1s\nPersistent=true\n[Install]\nWantedBy=timers.target\n'
    (UNITS / (FINISH + '.timer')).write_text(timer)
    state = json.loads((OUT / 'state.json').read_text())
    state['journal_retention_snapshot'] = journal_proof['current']
    state['journal_retention_bounds'] = {stream: max(value,
        state.get('journal_retention_bounds', {}).get(stream, 0))
        for stream, value in journal_proof['current_budget']['rates_bytes_per_second'].items()}
    collect.write_json(OUT / 'state.json', state)
    collect.write_json(manifest, record)
    checked(['systemctl', 'daemon-reload'])
    checked(['systemctl', 'enable', '--now', SAMPLER + '.timer', FINISH + '.timer'])
    initial = command(['systemctl', 'start', SAMPLER + '.service'])
    collect.write_json(OUT / 'initial-sample.json', initial)
    if initial['rc']:
        raise RuntimeError('Initial collection failed; the immutable observation remains recorded')
    print(json.dumps(record))


def expected_firings(started, ended, configuration=None):
    return contract.expected_firings(started, ended, configuration or contract.chain_configuration('shortened'))


def wait_unit(unit, seconds):
    deadline = time.monotonic() + seconds
    while checked(['systemctl', 'show', unit, '--value', '-p', 'ActiveState']) in ('active', 'activating', 'deactivating'):
        if time.monotonic() >= deadline:
            raise RuntimeError('Unit did not become idle within its deadline: ' + unit)
        time.sleep(1)


def wait_sampler():
    return wait_unit(SAMPLER + '.service', SAMPLER_WAIT_SECONDS)


def timeout_seconds(value):
    units = {'us': 0.000001, 'ms': 0.001, 's': 1, 'min': 60, 'h': 3600}
    parts = re.findall(r'([0-9.]+)(us|ms|min|s|h)', value)
    if not parts or re.sub(r'([0-9.]+)(us|ms|min|s|h)|\s+', '', value):
        raise RuntimeError('Unsupported installed stop timeout: ' + value)
    return sum(float(amount) * units[unit] for amount, unit in parts)


def wait_passes(manifest):
    configuration = manifest['configuration']
    expected = {(row['transition'], row['cadence'], evaluate.epoch(row['planned_at']))
                for row in contract.expected_firings(datetime.datetime.fromisoformat(manifest['started_at']),
                    datetime.datetime.fromisoformat(manifest['earliest_finish_at']), configuration)}
    invocation = collect.properties(manifest['unit_before_observation']).get('InvocationID')
    began, deadline = time.monotonic(), time.monotonic() + PASS_WAIT_SECONDS
    while True:
        result = command(['/usr/bin/python3', str(TOOLS / 'collect.py'), str(OUT),
                          str(TOOLS / 'pvs-all.csv'), '--journal-only'])
        if result['rc']:
            raise RuntimeError('Required pass wait could not collect complete journals')
        records = evaluate.pass_records(OUT / 'passes.jsonl')
        completed = {(row['transition'], row['cadence'], evaluate.epoch(row['plannedAt']))
                     for row in records if row['invocation_id'] == invocation}
        if expected <= completed:
            return {'deadline_seconds': PASS_WAIT_SECONDS, 'elapsed_seconds': time.monotonic() - began,
                    'required': len(expected), 'completed': len(expected)}
        if time.monotonic() >= deadline:
            raise RuntimeError('Required in-window passes did not close before the bounded deadline')
        time.sleep(2)


def terminal(aborted=False, reason=None):
    manifest = json.loads((OUT / 'observation.json').read_text())
    if any((OUT / name).exists() for name in ('shutdown.json', 'abort.json', 'shutdown-started.json', 'abort-started.json')):
        raise RuntimeError('A terminal operation is already recorded; refusing a repeated stop')
    if not aborted and (OUT / 'abort-request.json').exists():
        raise RuntimeError('An abort was requested; normal finish is forbidden')
    if aborted and not reason:
        reason = json.loads((OUT / 'abort-request.json').read_text())['reason']
    end = datetime.datetime.fromisoformat(manifest['earliest_finish_at'])
    remaining = (end - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    if not aborted and remaining > 2:
        raise RuntimeError('The observation window has not elapsed')
    monotonic_remaining = manifest['duration_seconds'] - (time.monotonic() - manifest['monotonic_start'])
    boot_unchanged = BOOT.read_text().strip() == manifest['boot_id']
    if not aborted and (not boot_unchanged or monotonic_remaining > 2):
        raise RuntimeError('The monotonic observation duration has not elapsed in this boot')
    if not aborted:
        while remaining > 0 or monotonic_remaining > 0:
            time.sleep(max(remaining, monotonic_remaining))
            remaining = (end - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
            monotonic_remaining = manifest['duration_seconds'] - (time.monotonic() - manifest['monotonic_start'])
    result = {'observation': manifest, 'finish_started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'boot_unchanged': BOOT.read_text().strip() == manifest['boot_id'],
              'monotonic_elapsed_seconds': time.monotonic() - manifest['monotonic_start'],
              'terminal_kind': 'abort' if aborted else 'finish', 'reason': reason,
              'errors': []}
    if not aborted and (not result['boot_unchanged'] or
                       result['monotonic_elapsed_seconds'] < manifest['duration_seconds']):
        raise RuntimeError('The monotonic observation duration has not elapsed in this boot')
    marker = OUT / ('abort-started.json' if aborted else 'shutdown-started.json')
    collect.write_json(marker, result)

    def capture(name, action):
        try:
            result[name] = action()
            if isinstance(result[name], dict) and result[name].get('rc', 0) != 0:
                result['errors'].append(name)
        except Exception as error:
            result[name] = {'error': type(error).__name__, 'message': str(error)}
            result['errors'].append(name)
        collect.write_json(marker, result)

    capture('cancel_timers', lambda: stop_loaded([SAMPLER + '.timer', FINISH + '.timer']))
    capture('sampler_wait', wait_sampler)
    if not aborted and manifest.get('measurement_schema') == contract.SCHEMA:
        capture('required_pass_wait', lambda: wait_passes(manifest))
    filesystem = os.statvfs(collect.STORE)
    reserve = filesystem.f_bavail * filesystem.f_frsize >= measure.MINIMUM_FREE_BYTES
    if 'sampler_wait' not in result['errors'] and reserve:
        capture('final_sample', lambda: command(['/usr/bin/python3', str(TOOLS / 'collect.py'),
                                               str(OUT), str(TOOLS / 'pvs-all.csv')]))
        if (OUT / 'latest-full.json').exists():
            final = json.loads((OUT / 'latest-full.json').read_text())
            if final['observed_at'] >= result['finish_started_at']:
                result['final_full_sample'] = final['raw_directory']
            else:
                result['errors'].append('missing_final_full_sample')
    else:
        result['final_sample'] = {'skipped': 'disk_reserve' if not reserve else 'sampler_busy'}
        result['errors'].append('final_sample')
    final_gc = OUT / 'final-gc'
    final_gc.mkdir(exist_ok=False)
    filesystem = os.statvfs(collect.STORE)
    if (filesystem.f_bavail * filesystem.f_frsize >= measure.MINIMUM_FREE_BYTES and
            'sampler_wait' not in result['errors']):
        capture('complete_gc_recordings', lambda: measure.gc(OUT, final_gc,
                datetime.datetime.now(datetime.timezone.utc).isoformat(), complete=True))
    else:
        result['complete_gc_recordings'] = {'skipped': 'disk_reserve_or_sampler_busy'}
        result['errors'].append('complete_gc_recordings')
    capture('etl_state_before_stop', lambda: collect.request('getApplianceMetricsForAppliance?appliance=appliance0',
                                                           final_gc / 'metrics-before-stop.json')[0])
    capture('cancel_health_timer', lambda: command(['systemctl', 'stop',
                                                  collect.HEALTH_UNIT.replace('.service', '.timer')]))
    capture('health_wait', lambda: wait_unit(collect.HEALTH_UNIT, 120))
    result['health_coverage_ended_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    state_path = OUT / 'state.json'
    if state_path.exists():
        state = json.loads(state_path.read_text())
        state['health_coverage_ended_at'] = result['health_coverage_ended_at']
        collect.write_json(state_path, state)
    capture('before', unit_state)
    before = collect.properties(result.get('before', '') if isinstance(result.get('before'), str) else '')
    if before.get('ActiveState') != 'active':
        result['errors'].append('appliance_not_active_before_stop')
    capture('stop_timeout', lambda: checked(['systemctl', 'show', collect.UNIT,
                                           '--value', '-p', 'TimeoutStopUSec']))
    try:
        timeout = timeout_seconds(result['stop_timeout'])
    except (TypeError, RuntimeError):
        timeout = 600
        result['errors'].append('stop_timeout_unavailable')
    began = time.monotonic()
    try:
        result['stop'] = command(['systemctl', 'stop', collect.UNIT], timeout=timeout + 30)
    except subprocess.TimeoutExpired:
        result['stop'] = {'rc': None, 'error': 'systemctl stop exceeded its bounded deadline'}
    result['stop_elapsed_seconds'] = time.monotonic() - began
    capture('after', unit_state)
    after = collect.properties(result.get('after', '') if isinstance(result.get('after'), str) else '')
    if (result['stop'].get('rc') != 0 or result['stop_elapsed_seconds'] > timeout or
            after.get('ActiveState') != 'inactive' or after.get('Result') != 'success'):
        result['errors'].append('orderly_stop')
    capture('final_journal', lambda: command(['/usr/bin/python3', str(TOOLS / 'collect.py'), str(OUT),
                                            str(TOOLS / 'pvs-all.csv'), '--journal-only']))
    result['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result['verdict'] = 'Incomplete' if aborted else 'Failed' if result['errors'] else 'Incomplete'
    result['analysis_required'] = 'Evaluate every sample, scheduled pass, metrics and GC pair before Passed'
    capture('evaluation', lambda: evaluate.evaluate(OUT, result))
    if 'evaluation' not in result['errors']:
        result['verdict'] = result['evaluation']['verdict']
    collect.write_json(OUT / ('abort.json' if aborted else 'shutdown.json'), result)
    print(json.dumps({'finished_at': result['finished_at'], 'stop_elapsed_seconds': result['stop_elapsed_seconds'],
                      'stop_rc': result['stop']['rc'], 'verdict': result['verdict']}))
    return result['verdict'] != 'Passed'


def finish():
    return terminal()


def main():
    os.umask(0o077)
    os.environ['PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'finish', 'abort'])
    parser.add_argument('--duration-seconds', type=int, choices=contract.DURATIONS)
    parser.add_argument('--chain', choices=contract.CHAINS)
    parser.add_argument('--reason')
    args = parser.parse_args()
    if args.action == 'start' and (args.duration_seconds is None or args.chain is None):
        parser.error('start requires --duration-seconds and --chain')
    with collect.locked(OUT.parent / (OUT.name + '.lifecycle.lock')):
        if args.action == 'start':
            return start(args.duration_seconds, args.chain)
        return terminal(args.action == 'abort', args.reason)


if __name__ == '__main__':
    raise SystemExit(main())
