"""Exercise the real sampler and abort unit under a private filesystem fault."""

import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

TOOLS = Path('/usr/local/share/etl-soak')
CHAIN, CASE = PAYLOAD['chain'], PAYLOAD['case']
assert ROLE == 'etl' and CHAIN in ('shortened', 'default') and CASE in ('E3', 'E4')
ROOT = Path('/var/lib/etl-negative-cases') / (CHAIN + '-' + CASE)
FAULT = Path('/etc/systemd/system/etl-soak-sample.service.d/90-negative-fault.conf')
POLL_SECONDS = 1
FAULT_SAMPLE_TIMEOUT = 1500
TERMINAL_TIMEOUT = 3000
sys.path.insert(0, str(TOOLS))
import collect
import contract
import evaluate
import focused
import observe
import pass_source

os.umask(0o077)
assert ROOT.exists() and not (ROOT / 'runtime.json').exists()
assert not FAULT.exists() and not (observe.OUT / 'observation.json').exists()
hashes = contract.verify_bundle(TOOLS)
state = {'chain': CHAIN, 'case': CASE, 'stage': 'Actual native preflight',
         'expectation': 'Incomplete', 'steps': []}
snapshots = ROOT / 'actual-state-history'
snapshots.mkdir(mode=0o700)
seen_states = set()
abort_invocations = set()


def save():
    state['observed_at'] = focused.now()
    (ROOT / 'runtime.json').write_text(json.dumps(state, indent=2))


def run(label, arguments, timeout=600, accepted=(0,)):
    state['stage'] = label
    save()
    began = focused.now()
    actual = subprocess.run(arguments, capture_output=True, timeout=timeout)
    (ROOT / (label + '.stdout')).write_bytes(actual.stdout)
    (ROOT / (label + '.stderr')).write_bytes(actual.stderr)
    state['steps'].append({'name': label, 'started_at': began, 'finished_at': focused.now(),
                           'returncode': actual.returncode, 'actual_arguments': arguments})
    save()
    assert actual.returncode in accepted, 'An actual fault-case command failed: ' + label


def history():
    data = (observe.OUT / 'state.json').read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    actual = json.loads(data)
    if digest not in seen_states:
        seen_states.add(digest)
        (snapshots / (digest + '.json')).write_bytes(data)
        with (ROOT / 'actual-state-history.jsonl').open('a') as stream:
            stream.write(json.dumps({'sha256': digest, 'observed_at': focused.now(),
                'monotonic_ns': time.monotonic_ns(),
                'consecutive_abort_failures': actual.get('consecutive_abort_failures')}) + '\n')
    text = subprocess.check_output(['systemctl', 'show', collect.ABORT_UNIT, '-p', 'InvocationID',
        '-p', 'MainPID', '-p', 'ActiveState', '-p', 'ExecMainStartTimestampMonotonic'], text=True)
    values = collect.properties(text)
    invocation = values.get('InvocationID')
    if values.get('MainPID') not in ('0', None) and invocation:
        abort_invocations.add(invocation)
        (ROOT / ('actual-abort-invocation-' + invocation + '.txt')).write_text(text)
    return actual


def samples_after(boundary):
    rows = []
    for path in sorted((observe.OUT / 'raw').glob('*/sample.json')):
        sample = json.loads(path.read_text())
        if sample.get('sample_kind') == 'full' and sample['observed_at'] >= boundary:
            rows.append((path, sample))
    return rows


def restore_fault():
    if FAULT.exists():
        assert FAULT.read_bytes() == (ROOT / 'declared-fault-dropin.conf').read_bytes()
        FAULT.rename(ROOT / 'removed-fault-dropin.conf')
        subprocess.run(['systemctl', 'daemon-reload'], capture_output=True, check=True, timeout=60)
        restored = subprocess.check_output(['systemctl', 'cat', observe.SAMPLER + '.service'])
        (ROOT / 'actual-sampler-after-restoration.txt').write_bytes(restored)
        assert restored == (ROOT / 'actual-sampler-before-fault.txt').read_bytes()
        (ROOT / 'actual-restoration.json').write_text(json.dumps({'observed_at': focused.now(),
            'fault_dropin_absent': not FAULT.exists(),
            'restored_effective_unit_sha256': hashlib.sha256(restored).hexdigest(),
            'original_effective_unit_bytes_equal': True}, indent=2))


try:
    run('actual-native-preflight', ['/usr/bin/python3', '-B', PAYLOAD['native_preflight_script'],
        '--chain', CHAIN, '--case', CASE], 3000)
    run('actual-boundary-preflight', ['/usr/bin/python3', '-B', PAYLOAD['boundary_preflight_script']], 180)
    boundary = json.loads((ROOT / 'boundary-preflight.json').read_text())
    assert boundary['actual_boundary_preflight'] == 'Passed'
    fault = json.loads((ROOT / 'fault-sampler.json').read_text())
    assert fault['tool_hashes'] == hashes
    configuration = contract.chain_configuration(CHAIN)
    now = datetime.datetime.now(datetime.timezone.utc)
    upcoming = contract.expected_firings(now + datetime.timedelta(seconds=120),
        now + datetime.timedelta(seconds=configuration['cadences'][0] + 601), configuration)
    target = next(row for row in upcoming if row['transition'] == 0)
    planned = datetime.datetime.fromisoformat(target['planned_at'])
    text = ('[Service]\nExecStart=\nExecStart=/usr/bin/python3 -B ' + str(ROOT / 'fault-sampler.py') +
            ' ' + str(ROOT / 'fault-sampler.json') + '\nInaccessiblePaths=' +
            ' '.join(fault['inaccessible_paths']) + '\n')
    (ROOT / 'declared-fault-dropin.conf').write_text(text)
    declared = {'chain': CHAIN, 'case': CASE, 'configured_duration_seconds': 86400,
        'minimum_fault_full_samples': 2, 'target_native_sts_pass': target,
        'actual_fault_paths': fault['inaccessible_paths'], 'tool_hashes': hashes,
        'fault_dropin_sha256': contract.digest(ROOT / 'declared-fault-dropin.conf')}
    (ROOT / 'runtime-contract.json').write_text(json.dumps(declared, indent=2))
    run('actual-native-observation-start', ['/usr/bin/python3', '-B', str(TOOLS / 'launch-retest.py'),
        '--duration-seconds', '86400', '--chain', CHAIN], 600)
    manifest = json.loads((observe.OUT / 'observation.json').read_text())
    assert not manifest['start_findings']
    identity = focused.identity()
    assert not json.loads((observe.OUT / 'latest-full.json').read_text())['errors']
    assert history().get('consecutive_abort_failures', 0) == 0
    state['stage'] = 'Waiting for the declared actual scheduler time'
    save()
    while datetime.datetime.now(datetime.timezone.utc) < planned - datetime.timedelta(seconds=120):
        assert focused.identity() == identity and not (observe.OUT / 'abort-request.json').exists()
        history()
        time.sleep(POLL_SECONDS)
    observe.wait_sampler()
    assert datetime.datetime.now(datetime.timezone.utc) < planned
    for component in focused.COMPONENTS:
        assert pass_source.read(component, ROOT / ('outside-before-' + component + '.jsonl'))
    original_unit = subprocess.check_output(['systemctl', 'cat', observe.SAMPLER + '.service'])
    (ROOT / 'actual-sampler-before-fault.txt').write_bytes(original_unit)
    FAULT.parent.mkdir(mode=0o755, exist_ok=True)
    FAULT.write_text(text)
    FAULT.chmod(0o644)
    run('actual-sampler-daemon-reload', ['systemctl', 'daemon-reload'], 60)
    run('actual-sampler-unit-verification', ['systemd-analyze', 'verify',
        '/etc/systemd/system/etl-soak-sample.service'], 60)
    began = focused.now()
    (ROOT / 'actual-fault-begin.json').write_text(json.dumps({'observed_at': began,
        'identity': identity, 'state_sha256': contract.digest(observe.OUT / 'state.json')}, indent=2))
    deadline = time.monotonic() + FAULT_SAMPLE_TIMEOUT
    first = None
    while True:
        current = history()
        full = samples_after(began)
        if full and first is None:
            sampler_pid = subprocess.check_output(['systemctl', 'show', observe.SAMPLER + '.service',
                '-p', 'MainPID', '--value'], text=True).strip()
            if sampler_pid != '0':
                assert time.monotonic() < deadline
                time.sleep(POLL_SECONDS)
                continue
            current = history()
            first = str(full[0][0])
            assert not (observe.OUT / 'abort-request.json').exists()
            assert current['consecutive_abort_failures'] == (1 if CASE == 'E4' else 0)
            (ROOT / 'actual-first-fault-sample.json').write_text(json.dumps({'sample': first,
                'sample_sha256': contract.digest(full[0][0]), 'state_sha256': contract.digest(observe.OUT / 'state.json'),
                'automatic_abort_request_absent': True, 'observed_at': focused.now()}, indent=2))
        if len(full) >= 2:
            break
        assert time.monotonic() < deadline, 'Two actual fault full samples did not complete'
        assert focused.identity() == identity
        if CASE == 'E3':
            assert not (observe.OUT / 'abort-request.json').exists()
        time.sleep(POLL_SECONDS)
    for _, sample in full:
        checks = {row['check'] for row in sample['errors']}
        assert checks <= {'journal', 'health_journal', 'kernel_journal'}
        assert 'health_journal' in checks or 'kernel_journal' in checks
        assert ('journal' in checks) == (CASE == 'E4')
        assert collect.critical(sample, **collect.abort_policy(observe.OUT)) == (CASE == 'E4')
    fault_end = focused.now()
    if CASE == 'E3':
        assert not (observe.OUT / 'abort-request.json').exists() and not abort_invocations
        restore_fault()
        recovered_at = focused.now()
        deadline = time.monotonic() + FAULT_SAMPLE_TIMEOUT
        while True:
            history()
            recovered = samples_after(recovered_at)
            assert all(not row['errors'] for _, row in recovered)
            if len(recovered) >= 2:
                break
            assert time.monotonic() < deadline
            time.sleep(POLL_SECONDS)
        (ROOT / 'actual-recovery-samples.json').write_text(json.dumps({str(path): contract.digest(path)
            for path, _ in recovered}, indent=2))
        run('planned-native-abort', ['/usr/bin/python3', '-B', str(TOOLS / 'observe.py'), 'abort',
            '--reason', 'Planned journal-unavailable File-evidence case'], TERMINAL_TIMEOUT, accepted=(0, 1))
    else:
        deadline = time.monotonic() + TERMINAL_TIMEOUT
        while not (observe.OUT / 'abort.json').exists():
            history()
            assert time.monotonic() < deadline
            time.sleep(POLL_SECONDS)
        history()
        request = json.loads((observe.OUT / 'abort-request.json').read_text())
        assert request['reason'] == 'consecutive_sample_failures'
        assert request['trigger_sample'] == str(full[1][0])
        assert len(abort_invocations) == 1
        assert any(json.loads(path.read_text()).get('consecutive_abort_failures') == 2 for path in snapshots.glob('*.json'))
        observe.wait_unit(collect.ABORT_UNIT, 60)
        restore_fault()
    terminal = json.loads((observe.OUT / 'abort.json').read_text())
    assert terminal['terminal_kind'] == 'abort' and terminal['stop']['rc'] == 0
    assert not terminal['errors'], 'The real final terminal capture has unresolved errors'
    for component in ('mgmt', 'engine', 'retrieval'):
        assert pass_source.read(component, ROOT / ('outside-after-' + component + '.jsonl'),
            ROOT / ('outside-before-' + component + '.jsonl'))
    for label, unit in (('actual-sampler-journal', observe.SAMPLER + '.service'),
                        ('actual-abort-unit-journal', collect.ABORT_UNIT)):
        since = datetime.datetime.fromisoformat(manifest['started_at']).astimezone(
            datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        run(label, ['/usr/bin/journalctl', '-u', unit, '--since', since,
            '--no-pager', '--all', '-o', 'json'], 60)
        assert (ROOT / (label + '.stderr')).stat().st_size == 0
    outside = ROOT / 'outside-native-passes.jsonl'
    events = pass_source.read('etl', ROOT / 'outside-after-etl.jsonl', ROOT / 'outside-before-etl.jsonl')
    outside.write_text(''.join(json.dumps(row) + '\n' for row in events if evaluate.PASS.search(row['MESSAGE'])))
    witnesses = [row for row in evaluate.pass_records(outside) if row['transition'] == 0 and
        row['invocation_id'] == identity['invocation_id'] and row['plannedAt'] == target['planned_at']]
    assert len(witnesses) == 1
    witness = witnesses[0]
    focused.successful_pass(witness)
    assert evaluate.epoch(began) <= evaluate.epoch(witness['startedAt']) <= evaluate.epoch(witness['endedAt']) <= evaluate.epoch(fault_end)
    if CASE == 'E3':
        assert witness in evaluate.pass_records(observe.OUT / 'passes.jsonl')
    assert contract.verify_bundle(TOOLS) == hashes
    state.update(stage='Native case complete; preservation and frozen replay pending', expectation='Pending',
                 native_short_observation=terminal['verdict'], actual_fault_full_samples=len(full),
                 actual_fault_sample_hashes={str(path): contract.digest(path) for path, _ in full},
                 actual_abort_invocations=sorted(abort_invocations), actual_native_pass=witness,
                 fault_begin=began, fault_end=fault_end, fault_restored=True)
except BaseException as error:
    state.update(stage='Incomplete', error_type=type(error).__name__, error=str(error))
    restore_fault()
    if ((observe.OUT / 'observation.json').exists() and not any((observe.OUT / name).exists()
        for name in ('abort.json', 'shutdown.json', 'abort-started.json', 'shutdown-started.json', 'abort-request.json'))):
        run('failure-native-abort', ['/usr/bin/python3', '-B', str(TOOLS / 'observe.py'), 'abort',
            '--reason', 'Fault-case failure; preserve all original evidence'], TERMINAL_TIMEOUT, accepted=(0, 1))
    state['stage'] = 'Incomplete'
    raise
finally:
    save()
