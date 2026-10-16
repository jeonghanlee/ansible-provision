"""Prepare a fresh case using retained physical originals and actual new instruments."""

import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import time

TOOLS = Path('/usr/local/share/etl-soak')
STARTUP_WAITER = Path('/var/lib/etl-negative-orchestration/wait-etl-startup-v1.py')
STARTUP_WAITER_SHA256 = 'd6e2dfdaec47c1ad89859a9c6ce7a720c2cffde18cd33b2cd701df80e0758219'

CHAIN, CASE = PAYLOAD['chain'], PAYLOAD['case']
assert ROLE == 'etl' and CHAIN in ('shortened', 'default') and CASE in ('E1', 'E2', 'E3', 'E4')
ROOT = Path('/var/lib/etl-negative-preparation-' + CHAIN + '-' + CASE)
assert not ROOT.exists()
os.umask(0o077)
ROOT.mkdir(mode=0o700)
sys.path.insert(0, str(TOOLS))
import contract
import focused
import observe

assert not (observe.OUT / 'observation.json').exists()
state = {'chain': CHAIN, 'case': CASE, 'stage': 'Starting fresh preparation',
         'steps': [], 'observation_started': False}
hashes = contract.verify_bundle(TOOLS)


def save():
    state['observed_at'] = focused.now()
    (ROOT / 'state.json').write_text(json.dumps(state, indent=2))


def run(label, arguments, timeout):
    state['stage'] = label
    save()
    began = focused.now()
    with (ROOT / (label + '.stdout')).open('xb') as output, (ROOT / (label + '.stderr')).open('xb') as errors:
        actual = subprocess.run(['/usr/bin/python3', '-B', *map(str, arguments)],
                                stdout=output, stderr=errors, timeout=timeout)
    state['steps'].append({'name': label, 'started_at': began, 'finished_at': focused.now(),
                           'returncode': actual.returncode})
    save()
    assert actual.returncode == 0, 'Actual native case preparation failed: ' + label


def wait_population(label):
    state['stage'] = label
    save()
    with (TOOLS / 'pvs-all.csv').open(newline='') as stream:
        names = {row['pv'] for row in csv.DictReader(stream)}
    assert len(names) == 903
    deadline = time.monotonic() + 600
    attempt = 0
    while True:
        if focused.ready():
            attempt += 1
            population = focused.request('getPVStatus', pv='AASOAK*')
            captured = ROOT / (label + '-population-' + str(attempt).zfill(4) + '.json')
            captured.write_text(json.dumps(population, indent=2))
            if (isinstance(population, list) and len(population) == len(names)
                and {row.get('pvName') for row in population} == names
                and all(row.get('status') == 'Being archived'
                        and row.get('connectionState') == 'true' for row in population)):
                state[label] = {'actual_population': str(captured),
                                'sha256': contract.digest(captured), 'ready_pvs': len(population),
                                'observed_at': focused.now()}
                save()
                return
        assert time.monotonic() < deadline, 'The actual fixture population did not become ready: ' + label
        time.sleep(2)


try:
    assert contract.digest(STARTUP_WAITER) == STARTUP_WAITER_SHA256
    if CASE == 'E1':
        actual = subprocess.run(['systemctl', 'start', 'etl-soak-ioc.service',
            'epicsarchiverap-maven.service', 'epicsarchiverap-maven-health.timer'],
            capture_output=True, timeout=600)
        (ROOT / 'actual-baseline-start.stdout').write_bytes(actual.stdout)
        (ROOT / 'actual-baseline-start.stderr').write_bytes(actual.stderr)
        assert actual.returncode == 0
        focused.wait_until('actual baseline startup before fresh instruments', focused.ready, focused.START_TIMEOUT)
    wait_population('actual-pre-instrument-readiness')
    run('fresh-instruments', [TOOLS / 'initialize-fresh.py', 'instruments'], 600)
    wait_population('actual-post-instrument-readiness')
    run('healthy-instrument-check', [TOOLS / 'initialize-fresh.py', 'check'], 180)
    run('wait-actual-post-instrument-startup-passes', [STARTUP_WAITER, '--chain', CHAIN,
        '--output', ROOT / 'startup-after-instruments'], focused.START_TIMEOUT + 60)
    run('retained-original-physical-http-continuity', [TOOLS / 'focused.py', 'continuity', '--chain', CHAIN], 600)
    if CASE in ('E1', 'E2'):
        run('actual-journal-only-change', [PAYLOAD['challenge_script']], 60)
    else:
        case = Path('/var/lib/etl-negative-cases') / (CHAIN + '-' + CASE)
        case.mkdir(mode=0o700)
    measurement = ROOT / 'measurements'
    run('seven-real-measurement-rounds', [TOOLS / 'initialize-fresh.py', 'measure', '--measurements', measurement,
        '--duration-seconds', '86400', '--chain', CHAIN], 3000)
    assert not json.loads((measurement / 'measurements.json').read_text())['findings']
    run('native-fresh-prepare', [TOOLS / 'initialize-fresh.py', 'prepare', '--duration-seconds', '86400',
        '--chain', CHAIN], 180)
    assert not json.loads((observe.OUT / 'preparation.json').read_text())['findings']
    assert contract.verify_bundle(TOOLS) == hashes
    state.update(stage='Prepared for runtime verification', seven_measurement_rounds_complete=True,
                 native_retained_original_continuity_verified=True, tool_hashes=hashes)
except BaseException as error:
    state.update(stage='Incomplete', error_type=type(error).__name__, error=str(error))
    raise
finally:
    save()
