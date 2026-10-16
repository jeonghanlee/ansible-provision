"""Run one unrelated-study independence case through real native observation and abort."""

import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

TOOLS = Path('/usr/local/share/etl-soak')
STARTUP_WAITER = Path('/var/lib/etl-negative-orchestration/wait-etl-startup-v1.py')
STARTUP_WAITER_SHA256 = 'd6e2dfdaec47c1ad89859a9c6ce7a720c2cffde18cd33b2cd701df80e0758219'

CHAIN, CASE = PAYLOAD['chain'], PAYLOAD['case']
assert ROLE == 'etl' and CHAIN in ('shortened', 'default') and CASE in ('E1', 'E2')
ROOT = Path('/var/lib/etl-negative-cases') / (CHAIN + '-' + CASE)
sys.path.insert(0, str(TOOLS))
import collect
import contract
import focused
import observe

os.umask(0o077)
challenge = json.loads((ROOT / 'challenge.json').read_text())
assert challenge['case'] == CASE and challenge['etl_tool_hashes_unchanged']
assert not (ROOT / 'runtime.json').exists()
state = {'chain': CHAIN, 'case': CASE, 'expectation': 'Incomplete', 'stage': 'Native preflight', 'steps': []}
study = Path('/var/lib/etl-negative-study/journal_coverage.py')
assert contract.digest(study) == challenge['challenged_source_sha256']
initial_tools = contract.verify_bundle(TOOLS)


def save():
    state['observed_at'] = focused.now()
    (ROOT / 'runtime.json').write_text(json.dumps(state, indent=2))


def run(label, arguments, timeout=360, accepted=(0,)):
    state['stage'] = label
    save()
    began = focused.now()
    with (ROOT / (label + '.stdout')).open('xb') as output, (ROOT / (label + '.stderr')).open('xb') as errors:
        actual = subprocess.run(['/usr/bin/python3', '-B', *map(str, arguments)], stdout=output, stderr=errors, timeout=timeout)
    state['steps'].append({'name': label, 'started_at': began, 'finished_at': focused.now(), 'returncode': actual.returncode})
    save()
    if actual.returncode not in accepted:
        raise RuntimeError('Actual native case step failed: ' + label)


def health(label):
    proof = observe.OUT / 'health-verification.json'
    if proof.exists():
        shutil.copy2(proof, ROOT / (label + '-previous-proof.json'))
    run(label, [TOOLS / 'verify-health.py', '--cause', 'Verify current native health before the independence challenge',
                '--corrective-action', 'Execute two actual health invocations with full collector capture'])


try:
    prepared = contract.preparation(observe.OUT, 86400, CHAIN)
    assert not prepared['findings'] and not (observe.OUT / 'observation.json').exists()
    (ROOT / 'runtime-contract.json').write_text(json.dumps({'case': CASE, 'chain': CHAIN,
        'configured_observation_seconds': 86400, 'minimum_consecutive_successful_full_samples': 2,
        'explicit_abort_reason': 'Planned unrelated-study independence case ' + CASE,
        'unexpected_case_failure': 'preserve and request one bounded native abort',
        'challenge_sha256': contract.digest(ROOT / 'challenge.json')}, indent=2))
    health('health-before-empty')
    run('negative-readiness', [TOOLS / 'verify-runtime.py', 'empty', '--duration-seconds', '86400', '--chain', CHAIN])
    health('health-before-terminal')
    run('installed-terminal-path', [TOOLS / 'verify-runtime.py', 'abort', '--duration-seconds', '86400', '--chain', CHAIN], 1200)
    deadline = time.monotonic() + 300
    while not focused.ready():
        if time.monotonic() >= deadline:
            raise RuntimeError('The actual appliance did not recover after native terminal preflight')
        time.sleep(2)
    health('health-after-terminal')
    assert contract.digest(STARTUP_WAITER) == STARTUP_WAITER_SHA256
    run('wait-actual-post-terminal-startup-passes', [STARTUP_WAITER, '--chain', CHAIN,
        '--output', ROOT / 'startup-after-terminal'], focused.START_TIMEOUT + 60)
    run('current-physical-http-continuity', [TOOLS / 'focused.py', 'continuity', '--chain', CHAIN], 600)
    run('current-chain', [TOOLS / 'verify-chain.py', '--duration-seconds', '86400', '--chain', CHAIN])
    health('health-final')
    readiness = observe.start(86400, CHAIN, readiness_only=True)
    (ROOT / 'native-readiness.json').write_text(json.dumps(readiness, indent=2))
    assert not readiness['start_findings']
    assert contract.digest(study) == challenge['challenged_source_sha256']
    run('native-observation-start', [TOOLS / 'launch-retest.py', '--duration-seconds', '86400', '--chain', CHAIN], 600)
    manifest = json.loads((observe.OUT / 'observation.json').read_text())
    assert manifest['duration_seconds'] == 86400 and not manifest['start_findings']
    actual_identity = focused.identity()
    started = datetime.datetime.fromisoformat(manifest['started_at'])
    deadline = time.monotonic() + 1500
    while True:
        assert not (observe.OUT / 'abort-request.json').exists()
        assert not (observe.OUT / 'abort-started.json').exists()
        assert focused.identity() == actual_identity and contract.verify_bundle(TOOLS) == initial_tools
        assert contract.digest(study) == challenge['challenged_source_sha256']
        full = []
        for path in sorted((observe.OUT / 'raw').glob('*/sample.json')):
            sample = json.loads(path.read_text())
            if sample.get('sample_kind') == 'full' and datetime.datetime.fromisoformat(sample['observed_at']) >= started:
                full.append((path, sample))
        if any(sample['errors'] for _, sample in full):
            raise RuntimeError('An actual full sample failed during the independence challenge')
        if len(full) >= 2:
            break
        if time.monotonic() >= deadline:
            raise RuntimeError('Two actual native full samples did not complete within the case deadline')
        state.update(stage='Waiting for two actual native full samples', completed_full_samples=len(full))
        save()
        time.sleep(5)
    proof = {'case': CASE, 'chain': CHAIN, 'actual_successful_full_samples': len(full),
             'sample_files_sha256': {str(path): contract.digest(path) for path, _ in full},
             'unchanged_runtime_identity': actual_identity, 'unchanged_tool_hashes': initial_tools,
             'automatic_abort_request_before_explicit_end': False,
             'challenged_journal_source_sha256': contract.digest(study)}
    (ROOT / 'runtime-before-abort.json').write_text(json.dumps(proof, indent=2))
    run('planned-native-abort', [TOOLS / 'observe.py', 'abort', '--reason',
        'Planned unrelated-study independence case ' + CASE], 3000, accepted=(0, 1))
    terminal = json.loads((observe.OUT / 'abort.json').read_text())
    assert terminal['terminal_kind'] == 'abort' and terminal['stop']['rc'] == 0 and not terminal['errors']
    assert terminal['verdict'] == 'Incomplete'
    original = (ROOT / 'journal-study-original.py').read_bytes()
    assert contract.digest(ROOT / 'journal-study-original.py') == challenge['original_source_sha256']
    study.write_bytes(original)
    assert contract.digest(study) == challenge['original_source_sha256']
    assert contract.verify_bundle(TOOLS) == initial_tools
    state.update(stage='Native case complete; preservation and frozen replay pending', expectation='Pending',
                 actual_successful_full_samples=len(full), native_short_observation='Incomplete',
                 unrelated_journal_source_restored=True, explicit_native_abort_complete=True)
except BaseException as error:
    state.update(stage='Incomplete', error_type=type(error).__name__, error=str(error))
    if ((observe.OUT / 'observation.json').exists() and not any((observe.OUT / name).exists()
            for name in ('abort.json', 'shutdown.json', 'abort-started.json', 'shutdown-started.json', 'abort-request.json'))):
        run('failure-native-abort', [TOOLS / 'observe.py', 'abort', '--reason',
            'Independence case failure; preserve original evidence'], 3000, accepted=(0, 1))
    state['stage'] = 'Incomplete'
    raise
finally:
    save()
