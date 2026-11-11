#!/usr/bin/env python3
"""Stage the complete declared source tree without contacting a test environment."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tarfile

sys.dont_write_bytecode = True
import fault_support as candidate

RUNTIME_CLAIMS = ('journal-interval-coverage', 'unrelated-study-independence',
                  'partial-source-availability', 'all-source-automatic-abort',
                  'post-stop-capture-and-refusal', 'collection-during-deletion',
                  'accumulation-restart-and-request-overlap')


def sources(root):
    manifest = root / 'SHA256SUMS'
    result = {'SHA256SUMS': candidate.digest(manifest)}
    for line in manifest.read_text().splitlines():
        expected, name = line.split('  ', 1)
        relative = Path(name)
        candidate.require(not relative.is_absolute() and '..' not in relative.parts and name not in result,
                          'Invalid or duplicate source manifest member')
        path = root / relative
        candidate.require(path.is_file() and not path.is_symlink() and candidate.digest(path) == expected,
                          'Source manifest mismatch: ' + name)
        result[name] = expected
    actual = {name: value for name, value in candidate.members(root).items()
              if '__pycache__' not in Path(name).parts}
    candidate.require(actual == result, 'Complete source membership differs from manifest')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, output = args.source_root.resolve(), args.output.resolve()
    candidate.require(not output.exists() and not output.is_relative_to(root) and not root.is_relative_to(output),
                      'Output exists or overlaps original sources')
    before = sources(root)
    candidate.require(candidate.digest(root / 'etl-scenarios/wait-etl-startup-v1.py') ==
                      'd6e2dfdaec47c1ad89859a9c6ce7a720c2cffde18cd33b2cd701df80e0758219',
                      'Required original startup helper differs')
    output.mkdir(parents=True, mode=0o700)
    shutil.copytree(root, output / 'archiver-soak', ignore=shutil.ignore_patterns('__pycache__'))
    candidate.require(sources(output / 'archiver-soak') == before == sources(root), 'Staged source identity differs')
    candidate.save(output / 'source-members.json', {'members': before})
    deployed = Path('/var/lib/etl-negative-orchestration')
    wrapper = root / 'etl-scenarios/etl-fault-sampler.py'
    config = {'role': 'etl', 'chain': 'shortened', 'case': 'E3', 'timeout_seconds': 21600,
              'scenario_sha256': {name: candidate.digest(root / 'etl-scenarios' / name) for name in candidate.FILES},
              'wrapper_source_sha256': candidate.digest(wrapper),
              'wrapper_source_base64': base64.b64encode(wrapper.read_bytes()).decode()}
    for name, source in (('native_preflight_script', 'etl-native-preflight-v2.py'),
                         ('boundary_preflight_script', 'preflight-etl-fault-boundary.py')):
        config[name] = str(deployed / source)
        config[name + '_sha256'] = candidate.digest(root / 'etl-scenarios' / source)
    candidate.save(output / 'fault-configuration-template.json', config)
    candidate.save(output / 'batch.json', {'scope': 'Source staging only', 'runtime_claims': RUNTIME_CLAIMS,
                   'source_members': len(before), 'source_manifest_sha256': candidate.digest(output / 'source-members.json'),
                   'vm_contacted': False, 'runtime_verified': False, 'recipient_verified': False,
                   'excluded_generated_directories': ['__pycache__'],
                   'prerequisites': ['Dedicated Rocky 8.10 / Python 3.9 / systemd 239 environment',
                                     'Pinned appliance, Java, EPICS, native shim/decoder and 903-PV fixture',
                                     'Measured resource budget and declared case durations',
                                     'Private installed-path configurations and independent recipient context',
                                     'Per-case source identity, fault exposure, restoration and stop conditions']})
    archive = output / 'archiver-soak.tar.gz'
    with tarfile.open(archive, 'x:gz') as stream:
        stream.add(output / 'archiver-soak', arcname='archiver-soak')
    with tarfile.open(archive) as stream:
        archived = {}
        for member in stream:
            if member.isdir():
                continue
            candidate.require(member.isfile(), 'Nonregular staged archive member')
            name = Path(member.name).relative_to('archiver-soak').as_posix()
            candidate.require(name not in archived, 'Duplicate staged archive member')
            archived[name] = hashlib.sha256(stream.extractfile(member).read()).hexdigest()
    candidate.require(archived == before, 'Archive membership or bytes differ')
    candidate.save(output / 'package.json', {'archive': archive.name, 'bytes': archive.stat().st_size,
                   'sha256': candidate.digest(archive), 'members': len(archived), 'scope': 'Verified source package only'})
    print(json.dumps({'result': 'Staged', 'source_members': len(before), 'runtime_claims': len(RUNTIME_CLAIMS),
                      'archive_sha256': candidate.digest(archive), 'runtime_verified': False}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(2)
