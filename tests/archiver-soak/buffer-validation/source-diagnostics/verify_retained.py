#!/usr/bin/env python3
"""Exercise the corrected comparator and pass validator with retained actual evidence."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time

ROOT = Path(os.environ['BUFFER_REPLAY_OUTPUT'])
ARCHIVE = Path(os.environ['BUFFER_REPLAY_ARCHIVE'])
MODULE = Path(os.environ['BUFFER_REPLAY_RUNNER'])


def main():
    ROOT.mkdir(mode=0o700)
    with tarfile.open(ARCHIVE) as archive:
        for entry in archive.getmembers():
            if entry.name.startswith('/') or '..' in Path(entry.name).parts or not (entry.isfile() or entry.isdir()):
                raise RuntimeError('Unexpected evidence archive entry')
        archive.extractall(ROOT)
    original = ROOT / 'preflight'
    specification = importlib.util.spec_from_file_location('buffer29_runner', MODULE)
    runner = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(runner)
    passes = json.loads((original / 'passes.json').read_text())
    runner.validate_pass(15, passes['15'], True)
    try:
        runner.validate_pass(16, passes['16'], False)
    except runner.Incomplete as error:
        rejected = str(error)
    else:
        raise RuntimeError('The actual missing-injection pass was accepted')
    ready = json.loads((original / 'readiness.json').read_text())
    verdict = json.loads((original / 'verdict.json').read_text())
    identity = json.loads((original / 'engine-identity.json').read_text())
    counters = json.loads((original / 'final-counters.json').read_text())
    # This diagnostic window is fixed before decoding and ends before the final normal writes.
    windows = [(ready['ready_mono_ns'], verdict['finished_mono_ns'] - 20 * runner.NS)]
    decoded = ROOT / 'decoded'
    decoded.mkdir()
    deadline = time.monotonic_ns() + 900 * runner.NS
    with (decoded / 'decode.raw.log').open('w') as log:
        for mode, source in [('inputs', original / ('trace-' + str(identity['pid']) + '.bin')),
                             ('physical', original / 'pb')]:
            runner.execute([runner.JAVA, '-Xmx512m', '-cp', runner.CP, 'PBDecode', mode, str(source),
                            str(decoded / (mode + '.tsv')), str(runner.TOOLS / 'fast.txt')], deadline, log)
    result = runner.compare_decoded(decoded, windows, counters, deadline)
    result.update(actual_missing_injection_rejected=rejected, actual_first_write_pass_accepted=True,
                  window=windows, acceptance_preflight=False)
    (ROOT / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
