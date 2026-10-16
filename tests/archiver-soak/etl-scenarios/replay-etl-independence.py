#!/usr/bin/env python3
"""Replay real native evidence and assess the declared independence challenge."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(mode=0o700)
    sys.path.insert(0, str(TOOLS))
    import contract
    hashes = contract.verify_bundle(TOOLS)
    challenge = json.loads((args.case / 'challenge.json').read_text())
    runtime = json.loads((args.case / 'runtime.json').read_text())
    contract_record = json.loads((args.case / 'runtime-contract.json').read_text())
    proof = json.loads((args.case / 'runtime-before-abort.json').read_text())
    manifest = json.loads((OUT / 'observation.json').read_text())
    terminal = json.loads((OUT / 'abort.json').read_text())
    original_hash = digest(OUT / 'abort.json')
    assert challenge['case'] in ('E1', 'E2') and runtime['case'] == challenge['case']
    assert challenge['chain'] == runtime['chain'] == contract_record['chain']
    assert challenge['original_import_returncode'] == 0 and challenge['subject_outside_etl_bundle']
    assert (challenge['challenged_import_returncode'] != 0) == (challenge['case'] == 'E1')
    assert digest(args.case / 'journal-study-original.py') == challenge['original_source_sha256']
    assert digest(args.case / 'journal-study-challenged.py') == challenge['challenged_source_sha256']
    if challenge['case'] == 'E1':
        assert b'Intentional unrelated journal-study import failure' in (args.case / 'challenged-import.stderr').read_bytes()
    assert runtime['explicit_native_abort_complete'] and runtime['unrelated_journal_source_restored']
    assert challenge['etl_tool_hashes_unchanged'] and hashes == proof['unchanged_tool_hashes']
    assert manifest['tool_hashes'] == hashes and manifest['duration_seconds'] == 86400
    assert not manifest['start_findings'] and terminal['observation'] == manifest
    assert terminal['terminal_kind'] == 'abort' and terminal['verdict'] == 'Incomplete'
    assert terminal['stop']['rc'] == 0 and not terminal['errors']
    assert terminal['reason'] == contract_record['explicit_abort_reason']
    assert not (OUT / 'abort-request.json').exists()
    assert proof['automatic_abort_request_before_explicit_end'] is False
    samples = []
    for name, expected in proof['sample_files_sha256'].items():
        path = Path(name)
        assert path.is_relative_to(OUT / 'raw') and digest(path) == expected
        sample = json.loads(path.read_text())
        assert sample['sample_kind'] == 'full' and not sample['errors']
        assert manifest['started_at'] <= sample['observed_at'] < terminal['finish_started_at']
        samples.append(sample)
    assert len(samples) >= contract_record['minimum_consecutive_successful_full_samples'] == 2
    actual_full = set()
    for path in (OUT / 'raw').glob('*/sample.json'):
        sample = json.loads(path.read_text())
        if (sample.get('sample_kind') == 'full' and
                manifest['started_at'] <= sample['observed_at'] < terminal['finish_started_at']):
            actual_full.add(str(path))
    assert actual_full == set(proof['sample_files_sha256'])
    actual = subprocess.run([sys.executable, '-B', str(TOOLS / 'evaluate.py'), '--input', str(OUT)],
                            capture_output=True, timeout=600)
    (args.output / 'native-evaluate.stdout').write_bytes(actual.stdout)
    (args.output / 'native-evaluate.stderr').write_bytes(actual.stderr)
    evaluation = json.loads(actual.stdout)
    assert actual.returncode == 1 and evaluation['verdict'] == 'Incomplete'
    aggregate_file = args.output / 'aggregate.json'
    aggregate = subprocess.run([sys.executable, '-B', str(TOOLS / 'aggregate.py'),
                               '--input', str(OUT), '--output', str(aggregate_file)],
                              capture_output=True, timeout=600)
    (args.output / 'native-aggregate.stdout').write_bytes(aggregate.stdout)
    (args.output / 'native-aggregate.stderr').write_bytes(aggregate.stderr)
    numerical = json.loads(aggregate_file.read_text())
    assert aggregate.returncode == 1 and numerical['verdict'] == 'Incomplete'
    assert digest(OUT / 'abort.json') == original_hash
    result = {'case': challenge['case'], 'chain': challenge['chain'], 'expectation': 'Passed',
              'successful_full_samples': len(samples), 'native_short_observation': terminal['verdict'],
              'native_evaluation': evaluation, 'native_aggregate': numerical,
              'terminal_sha256': original_hash, 'original_terminal_unchanged': True}
    (args.output / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: result[key] for key in ('case', 'chain', 'expectation',
                      'successful_full_samples', 'native_short_observation', 'terminal_sha256')}))


if __name__ == '__main__':
    main()
