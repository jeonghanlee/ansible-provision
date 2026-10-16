"""Read actual deployed configurations, PB files and HTTP with shipped comparators."""

import argparse
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

sys.path.insert(0, '/usr/local/share/etl-soak')
import contract
import evaluate
import focused
import observe


class ConfirmedViolation(RuntimeError):
    """A completed comparison found a changed required value or identity."""


def compare(action):
    try:
        return action()
    except RuntimeError as error:
        raise ConfirmedViolation(str(error)) from error


def capture(chain, label, trigger=None):
    base = observe.OUT / 'physical-checks'
    base.mkdir(mode=0o700, exist_ok=True)
    root = base / label
    root.mkdir(mode=0o700)
    result = {'result': 'Incomplete', 'chain': chain, 'started_at': focused.now(),
              'scope': 'Read-only live configurations, shipped PB decoder and policy/HTTP comparators',
              'trigger_pass': trigger, 'executor_sha256': contract.digest(Path(__file__))}
    try:
        manifest_path = observe.OUT / 'observation.json'
        manifest_sha = contract.digest(manifest_path)
        observation = json.loads(manifest_path.read_text())
        before = focused.identity()
        invocation = dict(line.split('=', 1) for line in observation['unit_before_observation'].splitlines() if '=' in line)['InvocationID']
        if before['invocation_id'] != invocation or before['jvms'] != observation['jvm_identity'] or before['boot_id'] != observation['boot_id']:
            raise ConfirmedViolation('Physical checkpoint differs from the active observation identity')
        current_tools = observe.tool_hashes()
        if current_tools != observation['tool_hashes']:
            raise ConfirmedViolation('Physical checkpoint tools differ from the frozen observation')
        original = focused.ROOT / chain
        accepted = focused.verified_focused_result(original, chain)
        focused.check_recheck_tools(accepted['tools'], observe.TOOLS)
        if focused.artifacts() != accepted['artifacts']:
            raise ConfirmedViolation('Deployed artifacts differ from the original focused result')
        values = focused.environment()
        def configuration(row):
            observed = focused.request('getPVTypeInfo', pv=row['pv'])
            effective = focused.settings(chain, observed, values)
            typeinfo = {key: observed.get(key) for key in ('DBRType', 'chunkKey')}
            if effective != row['effective'] or typeinfo != row['typeinfo']:
                raise ConfirmedViolation('A deployed PV configuration differs from its original input')
            return {'pv': row['pv'], 'response': observed, 'effective': effective}
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            configurations = list(pool.map(configuration, accepted['pvs']))
        if len(configurations) != 903 or len({row['pv'] for row in configurations}) != 903:
            raise RuntimeError('Exactly 903 unchanged deployed configurations are required')
        focused.save(root, 'configurations.json', configurations)
        flags = focused.request('getAllNamedFlags')
        if flags != accepted['flags']:
            raise ConfirmedViolation('Deployed flags differ from the original focused result')
        focused.save(root, 'flags.json', flags)
        for name in ('manifest.json', 'baseline.json', 'recent-bin-expectations.json'):
            shutil.copy2(original / name, root / name)
        specs = json.loads((root / 'manifest.json').read_text())['pvs']
        baseline = json.loads((root / 'baseline.json').read_text())
        classpath = str(original / 'helper-classes') + ':' + str(focused.INSTALL / 'etl/webapps/etl/WEB-INF/classes') + ':' + str(focused.INSTALL / 'etl/webapps/etl/WEB-INF/lib/*')
        snapshot = focused.pb(root, classpath, 'snapshot', 'physical.json')
        expected = compare(lambda: focused.compare_physical(specs, baseline, snapshot))
        captured = (observe.OUT / 'passes.jsonl').read_bytes()
        end = captured.rfind(b'\n') + 1
        (root / 'native-passes.jsonl').write_bytes(captured[:end])
        result['pass_capture_trailing_bytes'] = len(captured) - end
        records = evaluate.pass_records(root / 'native-passes.jsonl')
        current_records = [row for row in records if row['invocation_id'] == invocation]
        if {row['transition'] for row in current_records} != {0, 1}:
            raise RuntimeError('Physical checkpoint lacks both real transition records')
        for row in current_records:
            focused.successful_pass(row)
        recent = compare(lambda: focused.retention(specs, snapshot, current_records, chain, invocation,
            json.loads((root / 'recent-bin-expectations.json').read_text())))
        http = compare(lambda: focused.compare_http(root, expected, specs, 'historical'))
        http.update(compare(lambda: focused.compare_recent_http(root, recent, 'recent')))
        if focused.identity() != before or contract.digest(manifest_path) != manifest_sha or observe.tool_hashes() != current_tools:
            raise ConfirmedViolation('Observation, runtime identity or tools changed during the physical checkpoint')
        result.update(result='Passed', configured_population=903, exact_pv_count=len(specs),
            original_focused_result_sha256=contract.digest(original / 'result.json'),
            source_manifest_sha256=contract.digest(root / 'manifest.json'), baseline_sha256=contract.digest(root / 'baseline.json'),
            physical_sha256=contract.digest(root / 'physical.json'), configurations_sha256=contract.digest(root / 'configurations.json'),
            http_sha256=http, observation_sha256=manifest_sha, identity=before, tool_hashes=current_tools)
    except ConfirmedViolation as error:
        result.update(result='Failed', error_type=type(error).__name__, error=str(error))
    except Exception as error:
        result.update(error_type=type(error).__name__, error=str(error))
    result['finished_at'] = focused.now()
    focused.save(root, 'result.json', result)
    return result


def watch(chain):
    (observe.OUT / 'physical-checks').mkdir(mode=0o700, exist_ok=True)
    manifest = json.loads((observe.OUT / 'observation.json').read_text())
    invocation = dict(line.split('=', 1) for line in manifest['unit_before_observation'].splitlines() if '=' in line)['InvocationID']
    start, end = map(evaluate.epoch, (manifest['started_at'], manifest['earliest_finish_at']))
    completed = {}
    while time.time() < end and len(completed) != 2:
        try:
            records = evaluate.pass_records(observe.OUT / 'passes.jsonl')
        except (OSError, ValueError):
            records = []
        for transition in (0, 1):
            candidates = [row for row in records if row['invocation_id'] == invocation
                          and row['transition'] == transition and start <= evaluate.epoch(row['plannedAt']) < end]
            if transition not in completed and candidates:
                trigger = min(candidates, key=lambda row: evaluate.epoch(row['endedAt']))
                completed[transition] = capture(chain, 'readonly-regular-transition-' + str(transition), trigger)
        if len(completed) != 2:
            time.sleep(30)
    summary = {'chain': chain, 'completed': {str(key): value['result'] for key, value in completed.items()},
               'result': 'Passed' if len(completed) == 2 and all(row['result'] == 'Passed' for row in completed.values()) else 'Incomplete',
               'finished_at': focused.now()}
    focused.save(observe.OUT / 'physical-checks', 'readonly-regular-summary.json', summary)
    return 0 if summary['result'] == 'Passed' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chain', required=True, choices=contract.CHAINS)
    parser.add_argument('--mode', required=True, choices=('watch', 'initial', 'final'))
    args = parser.parse_args()
    if args.mode == 'watch':
        raise SystemExit(watch(args.chain))
    result = capture(args.chain, 'readonly-' + args.mode)
    raise SystemExit(0 if args.mode == 'final' or result['result'] == 'Passed' else 1)
