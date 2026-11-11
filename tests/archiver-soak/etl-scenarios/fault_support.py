#!/usr/bin/env python3
"""Bind fault controller and replay claims to actual sources and terminal facts."""

import argparse
import base64
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('independence_support', ROOT / 'run-etl-independence-v3.py')
support = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(support)
require, digest, load, save = support.require, support.digest, support.load, support.save
members, execute, now = support.members, support.execute, support.now
VERSION = 'fault-candidate-v3'
TOOLS = Path('/usr/local/share/etl-soak')
OUT = Path('/var/lib/etl-soak')
FILES = ('fault_support.py', 'run-etl-fault-v3.py', 'replay-etl-fault-v2.py',
         'run-etl-independence-v3.py', 'replay-etl-independence-v2.py', 'run.py',
         'etl-native-preflight-v2.py', 'preflight-etl-fault-boundary.py',
         'etl-fault-sampler.py', 'wait-etl-startup-v1.py')


def configuration(value):
    require(isinstance(value, dict) and value.get('role') == 'etl', 'Configuration requires role=etl')
    require(value.get('chain') in ('shortened', 'default') and value.get('case') in ('E3', 'E4'),
            'Unsupported fault chain or case')
    budget = value.get('timeout_seconds')
    require(type(budget) in (int, float) and math.isfinite(budget) and budget > 0,
            'Finite positive controller timeout required')
    for name in ('native_preflight_script', 'boundary_preflight_script'):
        path = Path(value[name])
        require(path.is_absolute() and path.resolve() == path and path.is_file() and not path.is_symlink(),
                'Actual canonical preflight source required: ' + name)
        require(digest(path) == value[name + '_sha256'], 'Preflight source identity differs: ' + name)
    require(set(value.get('scenario_sha256', {})) == set(FILES), 'Complete candidate source identities required')
    require(all(digest(ROOT / name) == expected for name, expected in value['scenario_sha256'].items()),
            'Candidate source identity differs')
    wrapper = ROOT / 'etl-fault-sampler.py'
    require(value['wrapper_source_sha256'] == digest(wrapper) and
            base64.b64decode(value['wrapper_source_base64'], validate=True) == wrapper.read_bytes(),
            'Actual shipped namespace sampler required')
    return dict(value)


def controller(receipt, sources, configuration_sha256):
    require(receipt['returncode'] == 0 and not receipt.get('timed_out', False),
            'Actual fault controller exit 0 required')
    command = receipt['command']
    require(len(command) == 6 and command[1] == '-B' and
            Path(command[2]).name == 'run-etl-fault-v3.py' and command[3] == '--config' and
            command[5] == 'run', 'Actual fault run command required')
    require(receipt['source_sha256'] == sources['run-etl-fault-v3.py'] and
            receipt['configuration_sha256'] == configuration_sha256, 'Controller source/configuration identity differs')


def terminal(value, native_status):
    require(value.get('terminal_kind') == 'abort', 'Actual abort terminal required')
    require(value.get('verdict') == 'Incomplete' and native_status == 1,
            'Short native observation must remain Incomplete with exit 1')
    require(value.get('stop', {}).get('rc') == 0 and not value.get('errors') and value.get('boot_unchanged'),
            'Complete same-boot abort capture and actual successful stop required')


def source_path(original, original_root, selected):
    path = Path(original)
    require(path.is_absolute() and path.is_relative_to(original_root), 'Recorded path is outside the original input')
    relative = path.relative_to(original_root)
    require('..' not in relative.parts, 'Recorded input path contains traversal')
    target = selected / relative
    require(target.resolve().is_relative_to(selected.resolve()) and target.is_file() and not target.is_symlink(),
            'Recorded input member is missing or linked')
    return target


def freeze(roots, output):
    require(not output.exists(), 'Frozen manifest already exists')
    require(set(roots) == {'tools', 'input', 'case'}, 'All three frozen roots required')
    record = {name: members(path) for name, path in roots.items()}
    require(all(record.values()), 'Frozen input roots must be nonempty')
    require(all(not output.resolve().is_relative_to(path.resolve()) for path in roots.values()),
            'Manifest must be outside frozen inputs')
    require(record == {name: members(path) for name, path in roots.items()}, 'Inputs changed during freezing')
    save(output, {'version': VERSION, 'members': record})


def verified(roots, manifest, expected):
    require(digest(manifest) == expected, 'Frozen manifest identity differs')
    record = load(manifest)
    require(record['version'] == VERSION and set(record['members']) == set(roots) == {'tools', 'input', 'case'},
            'Complete frozen input manifest required')
    require(all(record['members'].values()) and record['members'] == {name: members(path) for name, path in roots.items()},
            'Frozen input membership or bytes differ')
    return record['members']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', action='store_true', required=True)
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    freeze({name: getattr(args, name).resolve() for name in ('tools', 'input', 'case')}, args.output)
    print(json.dumps({'result': 'Frozen', 'manifest_sha256': digest(args.output)}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(2)
