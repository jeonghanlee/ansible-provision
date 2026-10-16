"""Challenge the real unrelated journal-study file outside the frozen ETL bundle."""

import base64
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')
CASE_ROOT = Path('/var/lib/etl-negative-cases')
assert ROLE == PAYLOAD['role'] == 'etl'
chain, case = PAYLOAD['chain'], PAYLOAD['case']
assert chain in ('shortened', 'default') and case in ('E1', 'E2')
assert (OUT / 'fresh-initialization.json').exists() and not (OUT / 'observation.json').exists()
sys.path.insert(0, str(TOOLS))
import contract
original = base64.b64decode(PAYLOAD['original_base64'], validate=True)
assert hashlib.sha256(original).hexdigest() == PAYLOAD['original_sha256']
before_tools = contract.verify_bundle(TOOLS)
root = CASE_ROOT / (chain + '-' + case)
root.mkdir(parents=True, mode=0o700)
study = Path('/var/lib/etl-negative-study')
study.mkdir(mode=0o700, exist_ok=True)
target = study / 'journal_coverage.py'
if target.exists():
    assert target.read_bytes() == original
else:
    target.write_bytes(original)
assert not target.resolve().is_relative_to(TOOLS.resolve())
(root / 'journal-study-original.py').write_bytes(original)
import_code = ('import importlib.util,sys; '
               'spec=importlib.util.spec_from_file_location("unrelated_journal_study",sys.argv[1]); '
               'module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); '
               'print("Imported actual journal-study module")')


def imported(label):
    result = subprocess.run(['/usr/bin/python3', '-I', '-B', '-c', import_code, str(target)],
                            capture_output=True, timeout=30)
    for suffix, data in (('stdout', result.stdout), ('stderr', result.stderr)):
        (root / (label + '.' + suffix)).write_bytes(data)
    return result


baseline = imported('original-import')
assert baseline.returncode == 0
if case == 'E1':
    changed = original + b'\nraise RuntimeError("Intentional unrelated journal-study import failure")\n'
    expected_hash = PAYLOAD['broken_sha256']
else:
    assert original.count(b'QUERY_TIMEOUT = 60\n') == 1
    changed = original.replace(b'QUERY_TIMEOUT = 60\n', b'QUERY_TIMEOUT = 61\n')
    expected_hash = PAYLOAD['changed_sha256']
assert hashlib.sha256(changed).hexdigest() == expected_hash
(root / 'journal-study.diff').write_text(''.join(difflib.unified_diff(
    original.decode().splitlines(keepends=True), changed.decode().splitlines(keepends=True),
    fromfile='original-journal-study.py', tofile='challenged-journal-study.py')))
(root / 'declared-challenge.json').write_text(json.dumps({'case': case, 'chain': chain,
    'original_sha256': PAYLOAD['original_sha256'], 'challenged_sha256': expected_hash,
    'subject_outside_etl_bundle': True, 'expected_import_failure': case == 'E1'}, indent=2))
target.write_bytes(changed)
(root / 'journal-study-challenged.py').write_bytes(changed)
challenged = imported('challenged-import')
assert (challenged.returncode != 0) == (case == 'E1')
if case == 'E1':
    assert b'Intentional unrelated journal-study import failure' in challenged.stderr
assert contract.verify_bundle(TOOLS) == before_tools
record = {'case': case, 'chain': chain, 'stage': 'Challenge applied; runtime acceptance pending',
          'original_import_returncode': baseline.returncode, 'challenged_import_returncode': challenged.returncode,
          'original_source_sha256': PAYLOAD['original_sha256'], 'challenged_source_sha256': expected_hash,
          'etl_tool_hashes_unchanged': True, 'subject_outside_etl_bundle': True,
          'actual_full_samples_completed': 0, 'scenario_acceptance': 'Pending'}
(root / 'challenge.json').write_text(json.dumps(record, indent=2))
print(json.dumps(record, sort_keys=True))
