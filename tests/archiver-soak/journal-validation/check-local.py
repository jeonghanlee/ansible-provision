#!/usr/bin/env python3
"""Check real package CLI operations without substituting any internal path."""

import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading

SOURCE = Path(__file__).resolve().parent
BASELINE = '649fee80561611f1494c1c3ce1f9546f6c619173'


def snapshot(root):
    return {str(path.relative_to(root)): (
        'link:' + os.readlink(path) if path.is_symlink() else
        hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'directory')
        for path in sorted(root.rglob('*'))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--appliance-source', type=Path, required=True)
    args = parser.parse_args()
    workspace = Path(tempfile.mkdtemp(prefix='journal-local-'))
    package = workspace / 'package'
    results = []
    receipts = []

    def run(script, *arguments, succeeds=True):
        command = [sys.executable, '-B', str(script), *map(str, arguments)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        receipts.append({'command': command, 'returncode': result.returncode,
                         'stdout': result.stdout, 'stderr': result.stderr})
        if (result.returncode == 0) != succeeds:
            raise AssertionError('Unexpected CLI outcome: ' + repr(command) + '\n' + result.stderr)
        return result

    try:
        run(SOURCE / 'prepare.py', 'build', '--repository', args.repository,
            '--appliance-source', args.appliance_source, '--destination', package)
        run(package / 'prepare.py', 'verify', package)
        source = json.loads((package / 'source.json').read_text())
        for name, metadata in source['files'].items():
            if metadata.get('commit') != BASELINE:
                continue
            original = subprocess.check_output(['git', '-C', str(args.repository),
                                                 'show', BASELINE + ':' + metadata['source']])
            assert (package / name).read_bytes() == original, name
        for path in package.glob('*.py'):
            compile(path.read_bytes(), str(path), 'exec')
        for name in ('prepare.py', 'basic.py', 'long.py'):
            run(package / name, '--help')
        results.append('Build, syntax, CLI entry points and exact immutable dependencies')

        config = workspace / 'config.json'
        configuration = json.loads((package / 'config.example.json').read_text())
        config.write_text(json.dumps(configuration))
        stage = workspace / 'stage'
        stage.mkdir()
        run(package / 'prepare.py', 'install', package, '--config', config, '--root', stage)
        installed = stage / 'opt/journal-validation'
        run(installed / 'prepare.py', 'verify', installed)
        assert (stage / 'var/lib/journal-validation').stat().st_mode & 0o777 == 0o700
        assert (stage / 'run/journal-validation').stat().st_mode & 0o777 == 0o700
        units = sorted((stage / 'etc/systemd/system').glob('*.service'))
        assert {path.name for path in units} == {'journal-validation-ioc.service',
                                                'journal-validation-health.service',
                                                'journal-validation-basic.service'}
        assert all('etl-pass' not in path.read_text() for path in units)
        original_stage = snapshot(stage)
        run(package / 'prepare.py', 'install', package, '--config', config, '--root', stage, succeeds=False)
        assert snapshot(stage) == original_stage
        results.append('Staged install, private state, independent units and existing-install refusal')

        for name in ('journal-validation-ioc.service', 'journal-validation-health.service',
                     'journal-validation-basic.service',
                     configuration['appliance_unit'] + '.d/journal-validation.conf'):
            root = workspace / ('conflict-' + str(len(results)))
            conflict = root / 'etc/systemd/system' / name
            conflict.parent.mkdir(parents=True)
            conflict.write_text('Existing owner content\n')
            before = snapshot(root)
            run(package / 'prepare.py', 'install', package, '--config', config, '--root', root, succeeds=False)
            assert snapshot(root) == before, name
            results.append('Pre-mutation conflict refusal: ' + name)

        for name in ('var/lib/journal-validation', 'run/journal-validation'):
            root = workspace / ('state-conflict-' + str(len(results)))
            conflict = root / name
            conflict.mkdir(parents=True)
            (conflict / 'evidence.json').write_text('{}\n')
            before = snapshot(root)
            run(package / 'prepare.py', 'install', package, '--config', config, '--root', root, succeeds=False)
            assert snapshot(root) == before, name
            results.append('Existing evidence/runtime refusal: ' + name)

        bad_package = workspace / 'tampered-package'
        shutil.copytree(package, bad_package)
        with (bad_package / 'journal_coverage.py').open('a') as stream:
            stream.write('\n# Changed collector content.\n')
        run(package / 'prepare.py', 'verify', bad_package, succeeds=False)
        root = workspace / 'tampered-stage'
        root.mkdir()
        run(package / 'prepare.py', 'install', bad_package, '--config', config, '--root', root, succeeds=False)
        assert snapshot(root) == {}
        results.append('Actual collector modification rejected before installation')

        for key, value in (('appliance_unit', '../escaped.service'), ('user', 'other/account'),
                           ('mgmt_url', 'http://example.com/mgmt/bpl'),
                           ('retrieval_url', 'http://user:password@localhost/retrieval')):
            bad = dict(configuration, **{key: value})
            bad_config = workspace / ('bad-config-' + str(len(results)) + '.json')
            bad_config.write_text(json.dumps(bad))
            root = workspace / ('bad-config-stage-' + str(len(results)))
            root.mkdir()
            run(package / 'prepare.py', 'install', package, '--config', bad_config, '--root', root, succeeds=False)
            assert snapshot(root) == {}
            results.append('Unsafe deployment configuration rejected: ' + key)

        root, external = workspace / 'symlink-stage', workspace / 'external'
        root.mkdir()
        external.mkdir()
        (root / 'opt').symlink_to(external, target_is_directory=True)
        before = snapshot(root)
        run(package / 'prepare.py', 'install', package, '--config', config, '--root', root, succeeds=False)
        assert snapshot(root) == before and snapshot(external) == {}
        results.append('Staged symlink escape rejected before writing external files')

        readiness = workspace / 'actual-host-readiness'
        result = run(installed / 'basic.py', 'preflight', '--config', installed / 'config.json',
                     '--evidence', readiness, succeeds=False)
        observed = json.loads(result.stdout)
        assert observed['ready'] is False
        assert observed['checks']['appliance_artifact'] is False
        results.append('Actual host preflight refuses an undeployed example configuration')

        class Boundary(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(500 if self.path == '/error' else 200)
                self.end_headers()
                self.wfile.write(b'HTTP boundary response\n')

            def log_message(self, *_):
                pass

        server = http.server.HTTPServer(('127.0.0.1', 0), Boundary)
        worker = threading.Thread(target=server.serve_forever)
        worker.start()
        try:
            code = ('import json,sys; from pathlib import Path; '
                    'sys.path.insert(0,sys.argv[1]); import basic; '
                    'print(json.dumps(basic.request(sys.argv[2],Path(sys.argv[3]))))')
            for suffix, status in (('/success', 200), ('/error', 500)):
                url = 'http://127.0.0.1:' + str(server.server_port) + suffix
                destination = workspace / ('http-' + str(status))
                response = run('-c', code, package, url, destination)
                outcome = json.loads(response.stdout)
                assert outcome['status'] == status and not outcome.get('error')
                assert destination.with_suffix('.body').read_bytes() == b'HTTP boundary response\n'
                assert json.loads(destination.with_suffix('.json').read_text()) == outcome
                results.append('Real shipped HTTP helper retains status/body/receipt: ' + str(status))
        finally:
            server.shutdown()
            server.server_close()
            worker.join()

        empty = workspace / 'empty-evidence'
        empty.mkdir()
        before = snapshot(empty)
        result = run(package / 'basic.py', 'replay', empty, succeeds=False)
        assert json.loads(result.stdout)['overall'] == 'Incomplete'
        assert snapshot(empty) == before
        results.append('Replay refuses absent evidence and performs no writes')
        report = {'result': 'Passed', 'scope': 'local package preparation only', 'checks': results,
                  'count': len(results), 'workspace': str(workspace),
                  'live_journal_basic': 'Not run', 'full_day': 'Not run',
                  'actual_host_readiness': observed}
    except Exception as error:
        report = {'result': 'Failed', 'error': str(error), 'checks': results,
                  'count': len(results), 'workspace': str(workspace)}
    (workspace / 'command-receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
    (workspace / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))
    return 0 if report['result'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
