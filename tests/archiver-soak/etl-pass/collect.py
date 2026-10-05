#!/usr/bin/env python3
"""Collect real appliance evidence, preserving failed samples and raw inputs."""

import argparse
import collections
import csv
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
import shlex
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

import resource_helpers as resources
import measure
import contract
import math
import journal_coverage
import journal_retention

UNIT = "epicsarchiverap-maven.service"
HEALTH_UNIT = "epicsarchiverap-maven-health.service"
IOC_UNIT = "etl-soak-ioc.service"
MGMT = "http://127.0.0.1:17665/mgmt/bpl"
STORE = Path("/arch")
INSTANCES = ("mgmt", "engine", "etl", "retrieval")
TIERS = ("sts", "mts", "lts")
JOURNAL_KEYS = ("__CURSOR", "__REALTIME_TIMESTAMP", "SYSLOG_IDENTIFIER",
                "PRIORITY", "MESSAGE", "_PID", "_SYSTEMD_INVOCATION_ID",
                "INVOCATION_ID", "EXIT_CODE", "EXIT_STATUS", "SERVICE_RESULT",
                "MESSAGE_ID", "UNIT", "_BOOT_ID")
HEALTH_PREFIX = "ETL_SOAK_HEALTH "
ABORT_UNIT = "etl-soak-abort.service"
HEALTH_COMMAND = Path('/opt/epicsarchiverap-maven/archappl.bash')
HEALTH_COMPLETION_MAX_AGE_SECONDS = 120


@contextlib.contextmanager
def locked(path):
    with path.open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def properties(text):
    return dict(line.split("=", 1) for line in text.splitlines() if "=" in line)


def accepted_statuses(health):
    return {"0", *health.get("SuccessExitStatus", "").split()}


def health_succeeded(health):
    return (health.get("Result") == "success" and
            health.get("ExecMainCode", "exited") in ("exited", "1") and
            health.get("ExecMainStatus") in accepted_statuses(health) and
            bool(health.get("ExecMainExitTimestamp")))


def health_completion(health_journal, now):
    completed = health_journal['completed']
    if not completed:
        raise RuntimeError('No completed health invocation is available')
    event = max(completed.values(), key=lambda row: row['observed_at'])
    finished = datetime.datetime.fromisoformat(event['observed_at'])
    if not 0 <= (now - finished).total_seconds() <= HEALTH_COMPLETION_MAX_AGE_SECONDS:
        raise RuntimeError('The last health completion is outside its freshness bound')
    if (event.get('result') != 'success' or event.get('exit_code') != 'exited' or
            event.get('exit_status') not in accepted_statuses(health_journal['properties'])):
        raise RuntimeError('The last completed health invocation failed')
    return event


def health_properties():
    health = properties(run(["systemctl", "show", HEALTH_UNIT, "-p", "Result",
                           "-p", "ExecMainCode", "-p", "ExecMainStatus",
                           "-p", "SuccessExitStatus", "-p", "ExecMainExitTimestamp",
                           '-p', 'ExecStart', '-p', 'User', '-p', 'Group',
                           '-p', 'TimeoutStartUSec', '-p', 'FragmentPath', '-p', 'DropInPaths']))
    if health.get('SuccessExitStatus') == '[unprintable]':
        address = shlex.split(run(['busctl', 'call', 'org.freedesktop.systemd1',
                                  '/org/freedesktop/systemd1', 'org.freedesktop.systemd1.Manager',
                                  'GetUnit', 's', HEALTH_UNIT]))
        if len(address) != 2 or address[0] != 'o':
            raise RuntimeError('Unexpected health unit D-Bus address')
        values = run(['busctl', 'get-property', 'org.freedesktop.systemd1', address[1],
                      'org.freedesktop.systemd1.Service', 'SuccessExitStatus']).split()
        if len(values) < 3 or values[0] != '(aiai)':
            raise RuntimeError('Unexpected health exit-status D-Bus value')
        count = int(values[1])
        signal_count = int(values[2 + count])
        if len(values) != 3 + count + signal_count:
            raise RuntimeError('Incomplete health exit-status D-Bus value')
        health['SuccessExitStatus'] = ' '.join(values[2:2 + count])
        health['SuccessSignals'] = ' '.join(values[3 + count:])
    if health.get('FragmentPath'):
        paths = [health['FragmentPath'], *shlex.split(health.get('DropInPaths', ''))]
        health['unit_files_sha256'] = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in paths}
        health['command_sha256'] = hashlib.sha256(HEALTH_COMMAND.read_bytes()).hexdigest()
    return health


def health_contract(health):
    return {key: health.get(key) for key in ('SuccessExitStatus', 'SuccessSignals',
            'User', 'Group', 'TimeoutStartUSec', 'unit_files_sha256', 'command_sha256')}


def collect_health(out, raw, previous, now):
    health = health_properties()
    command = ["journalctl", "-u", HEALTH_UNIT, "--no-pager", "--all", "-o", "json"]
    cursor = previous.get("health_journal_cursor")
    if cursor:
        command += ["--cursor", cursor]
    else:
        command += ["--since", previous.get("health_journal_since",
                    now.strftime("%Y-%m-%d 00:00:00 UTC"))]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError("Health journal collection failed: " + str(result.returncode))
    errors, events = [], []
    manifest_path = out / 'observation.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        verified = manifest.get('health_verification', {}).get('executions', [])
        if verified and health_contract(health) != health_contract(verified[-1]['health']):
            errors.append({'check': 'health_contract', 'message': 'Installed health command or unit contract changed'})
    lines = result.stdout.splitlines()
    if cursor:
        if not lines or json.loads(lines[0]).get('__CURSOR') != cursor:
            errors.append({"check": "health_coverage", "message": "Previous health journal cursor is unavailable"})
        else:
            lines = lines[1:]
    starts = previous.get('health_starts', 0)
    seen = dict(previous.get("health_seen", {}))
    completed = dict(previous.get("health_completed", {}))
    with (raw / "health-journal.jsonl").open("w") as archive:
        for line in lines:
            entry = json.loads(line)
            archive.write(json.dumps({key: entry[key] for key in JOURNAL_KEYS if key in entry}) + "\n")
            cursor = entry["__CURSOR"]
            message = str(entry.get("MESSAGE", ""))
            if entry.get('MESSAGE_ID') == '7d4958e842da4a758f6c1cdc7b36dcc5':
                starts += 1
            if "suppressed" in message.lower() or "missed" in message.lower():
                errors.append({"check": "health_coverage", "message": "Health journal records were suppressed or missed"})
            invocation = entry.get("_SYSTEMD_INVOCATION_ID", "")
            if invocation and str(entry.get("_PID", "")) != "1":
                seen.setdefault(invocation, entry.get("__REALTIME_TIMESTAMP", ""))
            if not message.startswith(HEALTH_PREFIX):
                continue
            event = json.loads(message[len(HEALTH_PREFIX):])
            invocation = event.get("invocation_id") or invocation
            if not invocation:
                errors.append({"check": "health_coverage", "message": "Health completion lacks invocation identity"})
                continue
            event["invocation_id"] = invocation
            if invocation in completed:
                errors.append({"check": "health_coverage", "message": "Duplicate health completion"})
                continue
            completed[invocation] = event
            events.append(event)
            if (event.get("result") != "success" or event.get("exit_code") != "exited" or
                    event.get("exit_status") not in accepted_statuses(health)):
                errors.append({"check": "health_invocation", "message": "Health invocation did not succeed"})
    if not completed:
        errors.append({"check": "health_coverage", "message": "No instrumented health completion recorded"})
    append(out / "health-invocations.csv", ["observed_at", "invocation_id", "result", "exit_code", "exit_status"], events)
    if starts - len(completed) > 1:
        errors.append({"check": "health_coverage", "message": "Health starts lack completion records"})
    return {"cursor": cursor, "seen": seen, "completed": completed, "starts": starts,
            "pending": sorted(set(seen) - set(completed)), "events": len(events),
            "completed_total": len(completed), "properties": health, "errors": errors}


def run(command, accepted=(0,), timeout=60):
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    if result.returncode not in accepted:
        raise RuntimeError("command failed: " + command[0] + ": " + str(result.returncode))
    return result.stdout.strip()


def tolerated_du(returncode, stdout, stderr):
    # The ETL moves and removes partitions while a store is measured. du then exits 1 after listing the files
    # that vanished, and the total it printed still stands; any other error is a failed measurement.
    problems = [line for line in stderr.splitlines() if line.strip()]
    if (returncode not in (0, 1) or not stdout.strip() or
            (returncode == 1 and (not problems or any(not line.endswith('No such file or directory') for line in problems)))):
        raise RuntimeError('command failed: du: ' + str(returncode))
    return int(stdout.split()[0])


def directory_bytes(root):
    result = subprocess.run(['du', '-sb', str(root)], capture_output=True, text=True, timeout=60)
    return tolerated_du(result.returncode, result.stdout, result.stderr)


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def append(path, fields, rows):
    new = not path.exists()
    with path.open("a", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        if new:
            writer.writeheader()
        writer.writerows(rows)


def request(endpoint, destination):
    started = time.monotonic()
    try:
        with urllib.request.urlopen(MGMT + "/" + endpoint, timeout=60) as response:
            status, body = response.status, response.read()
    except urllib.error.HTTPError as error:
        destination.write_bytes(error.read())
        raise RuntimeError("HTTP " + str(error.code) + ": " + endpoint) from error
    destination.write_bytes(body)
    if status != 200:
        raise RuntimeError("HTTP " + str(status) + ": " + endpoint)
    value = json.loads(body)
    if isinstance(value, dict) and value.get("status") == "error":
        raise RuntimeError("application error: " + endpoint)
    return value, round((time.monotonic() - started) * 1000, 3)


def collect_journal(out, raw, previous, now):
    command = ["journalctl", "-u", UNIT, "--no-pager", "--all", "-o", "json"]
    if previous.get("journal_cursor"):
        command += ["--cursor", previous["journal_cursor"]]
    else:
        command += ["--since", previous.get('journal_since', now.strftime("%Y-%m-%d 00:00:00 UTC"))]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError("journal collection failed: " + str(result.returncode))
    cursor = previous.get("journal_cursor")
    lines = result.stdout.splitlines()
    if cursor:
        if not lines or json.loads(lines[0]).get('__CURSOR') != cursor:
            raise RuntimeError('Previous appliance journal cursor is unavailable')
        lines = lines[1:]
    counts = collections.Counter()
    pass_count = 0
    with (raw / "journal.jsonl").open("w") as journal, (out / "passes.jsonl").open("a") as passes:
        for line in lines:
            entry = json.loads(line)
            selected = {key: entry[key] for key in JOURNAL_KEYS if key in entry}
            encoded = json.dumps(selected) + "\n"
            journal.write(encoded)
            cursor = entry["__CURSOR"]
            if any(term in str(entry.get('MESSAGE', '')).lower() for term in ('suppressed', 'missed')):
                raise RuntimeError('Appliance journal records were suppressed or missed')
            counts[entry.get("SYSLOG_IDENTIFIER", "unknown")] += 1
            if "ETL pass of transition " in str(entry.get("MESSAGE", "")):
                passes.write(encoded)
                pass_count += 1
    return cursor, dict(counts), pass_count


def collect_kernel(raw, previous, now):
    cursor = previous.get('kernel_journal_cursor')
    since = previous.get('kernel_journal_since', now.strftime('%Y-%m-%d 00:00:00 UTC'))
    command = ['journalctl', '-k', '-b', '--no-pager', '--all', '-o', 'json']
    command += ['--cursor', cursor] if cursor else ['--since', since]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError('Kernel journal collection failed')
    lines = result.stdout.splitlines()
    if cursor:
        if not lines or json.loads(lines[0]).get('__CURSOR') != cursor:
            raise RuntimeError('Previous kernel journal cursor is unavailable')
        lines = lines[1:]
    else:
        boot = run(['journalctl', '-b', '--no-pager', '-o', 'json', '--reverse', '--until', since, '--lines=1'])
        first_boot = json.loads(boot.splitlines()[0]) if boot else None
        if not first_boot or int(first_boot['__REALTIME_TIMESTAMP']) > datetime.datetime.fromisoformat(
                since.replace(' UTC', '+00:00')).timestamp() * 1000000:
            raise RuntimeError('Journal retention begins after the collection boundary')
        (raw / 'journal-retention-before.json').write_text(json.dumps(
            {key: first_boot[key] for key in JOURNAL_KEYS if key in first_boot}) + '\n')
        retained = run(['journalctl', '-k', '-b', '--no-pager', '-o', 'json', '--reverse', '--until', since, '--lines=1'])
        if retained:
            cursor = json.loads(retained.splitlines()[-1])['__CURSOR']
    events = 0
    with (raw / 'kernel-journal.jsonl').open('w') as archive:
        for line in lines:
            entry = json.loads(line)
            archive.write(json.dumps({key: entry[key] for key in JOURNAL_KEYS if key in entry}) + '\n')
            cursor = entry['__CURSOR']
            message = str(entry.get('MESSAGE', '')).lower()
            if any(term in message for term in ('suppressed', 'missed')):
                raise RuntimeError('Kernel journal records were suppressed or missed')
            events += any(term in message for term in ('out of memory', 'oom-kill', 'killed process'))
    return {'cursor': cursor, 'previous_cursor': previous.get('kernel_journal_cursor'),
            'since': since, 'coverage_complete': True, 'memory_events': events}


def event_rates(rows, observed_at):
    semantics = json.loads((Path(__file__).parent / 'rate-semantics.json').read_text())
    result = []
    for row in rows:
        if row.get('name') not in semantics['metrics'] or row.get('source', '').upper() != 'ENGINE':
            continue
        value = float(str(row['value']).replace(',', ''))
        if not math.isfinite(value) or value < 0:
            raise RuntimeError('Invalid engine rate metric')
        result.append({**row, 'numeric_value': value, 'observed_at': observed_at,
                       **semantics['metrics'][row['name']], 'source_commit': semantics['source_commit']})
    if {row['name'] for row in result} != set(semantics['metrics']):
        raise RuntimeError('Required engine event/data rate metrics are missing')
    return result


def fixture_parameters(out, tools=None):
    adjustment = json.loads((out / 'fixture-adjustment.json').read_text())
    tools = tools or Path('/usr/local/share/etl-soak')
    expected = {**adjustment['original_database_sha256'],
                adjustment['override_name']: adjustment['override_sha256']}
    if any(hashlib.sha256((tools / name).read_bytes()).hexdigest() != digest for name, digest in expected.items()):
        raise RuntimeError('Installed fixture source changed')
    environment = dict(os.environ, EPICS_CA_ADDR_LIST='127.0.0.1', EPICS_CA_AUTO_ADDR_LIST='NO')
    fields = [name + suffix for name in adjustment['records'] for suffix in ('.MDEL', '.ADEL')]
    result = subprocess.run([measure.CAGET, '-w', '5', '-t', *fields], env=environment,
                            capture_output=True, text=True, timeout=15)
    values = result.stdout.split()
    if result.returncode or len(values) != 20 or any(float(value) != -1 for value in values):
        raise RuntimeError('Actual retest fixture deadband fields do not match their approved values')
    return {'override_name': adjustment['override_name'], 'override_sha256': adjustment['override_sha256'],
            'verified_records': len(adjustment['records']), 'original_database_sha256': adjustment['original_database_sha256']}


def _sample(out, fixture, journal_only=False):
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%S.%fZ")
    ts = now.isoformat()
    raw = out / "raw" / stamp
    raw.mkdir(parents=True)
    state_path = out / "state.json"
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    state = dict(previous)
    summary = {"observed_at": ts, "errors": [], "raw_directory": str(raw),
               "sample_kind": "journal" if journal_only else "full"}

    def capture(name, action):
        try:
            value = action()
            summary[name] = value
            return value
        except Exception as error:
            summary["errors"].append({"check": name, "type": type(error).__name__, "message": str(error)})
            return None

    journal = capture("journal", lambda: collect_journal(out, raw, previous, now))
    if journal is not None:
        state["journal_cursor"] = journal[0]
    health_journal = capture("health_journal", lambda: collect_health(out, raw, previous, now))
    if health_journal is not None:
        state.update({"health_journal_cursor": health_journal["cursor"],
                      "health_seen": health_journal["seen"],
                      "health_starts": health_journal["starts"],
                      "health_completed": health_journal["completed"]})
        summary["errors"].extend(health_journal["errors"])
        summary["health_journal"] = {key: health_journal[key] for key in
                                    ("pending", "events", "completed_total")}
        boundary = previous.get('health_coverage_ended_at') if journal_only else None
        capture('health_completion', lambda: health_completion(health_journal,
            datetime.datetime.fromisoformat(boundary) if boundary else datetime.datetime.now(datetime.timezone.utc)))
        if journal_only and health_journal["pending"]:
            summary["errors"].append({"check": "health_coverage", "message": "Health invocations lack completion records"})
        if journal_only and health_journal['starts'] != health_journal['completed_total']:
            summary['errors'].append({'check': 'health_coverage', 'message': 'Health completion coverage is incomplete'})
    preparation_path = out / 'preparation.json'
    current_schema = (json.loads(preparation_path.read_text()).get('schema')
                      if preparation_path.exists() else None)
    manifest_path = out / 'observation.json'
    if manifest_path.exists():
        current_schema = json.loads(manifest_path.read_text()).get('measurement_schema')
    if current_schema == contract.SCHEMA:
        capture('journal_retention_budget', lambda: journal_retention.runtime(
            out, raw, Path(__file__).parent, previous,
            terminal=any((out / name).exists() for name in ('shutdown-started.json', 'abort-started.json'))))
        snapshot_path = raw / 'journal-retention-snapshot.json'
        budget_path = raw / 'journal-retention-budget.json'
        if snapshot_path.exists():
            state['journal_retention_snapshot'] = json.loads(snapshot_path.read_text())
        if budget_path.exists():
            bounds = json.loads(budget_path.read_text())['rates_bytes_per_second']
            state['journal_retention_bounds'] = {stream: max(value,
                previous.get('journal_retention_bounds', {}).get(stream, 0)) for stream, value in bounds.items()}
    kernel = capture('kernel_journal', lambda: journal_coverage.collect(raw, previous, now)
                     if current_schema == contract.SCHEMA else collect_kernel(raw, previous, now))
    if kernel is not None:
        state['kernel_journal_cursor'] = kernel['cursor']
        state['kernel_journal_since'] = kernel['since']
        if 'checkpoint' in kernel:
            state['system_journal_checkpoint'] = kernel['checkpoint']
        if kernel['memory_events']:
            summary['errors'].append({'check': 'kernel_memory', 'message': 'Kernel memory event observed'})
    if not journal_only:
        with fixture.open(newline="") as stream:
            pv_rows = list(csv.DictReader(stream))
        names = {row["pv"] for row in pv_rows}
        keys = {row["store_key"]: row["pv"] for row in pv_rows}
        summary["fixture_sha256"] = hashlib.sha256(fixture.read_bytes()).hexdigest()
        summary["expected_pvs"] = len(names)
        if (out / 'fixture-adjustment.json').exists():
            capture('fixture_adjustment', lambda: fixture_parameters(out))
        cpu = resources.cpu_totals()
        memory = resources.meminfo()
        state["cpu"] = cpu
        state["wall"] = now.timestamp()
        summary["memory_kb"] = memory
        summary["load"] = Path("/proc/loadavg").read_text().split()[:3]
        summary["disk"] = {"available_bytes": os.statvfs(STORE).f_bavail * os.statvfs(STORE).f_frsize}
        if previous.get("cpu") and cpu["total"] > previous["cpu"]["total"]:
            elapsed = cpu["total"] - previous["cpu"]["total"]
            summary["cpu_percent"] = {key: round(100 * (cpu[key] - previous["cpu"][key]) / elapsed, 3)
                                      for key in ("user", "sys", "idle", "iowait")}

        pids = resources.jvm_pids()
        fixture_pid = capture("ioc_pid", lambda: run(["systemctl", "show", "--value", "-p", "MainPID", IOC_UNIT]))
        if fixture_pid and fixture_pid != "0":
            pids["ioc"] = fixture_pid
        database_pid = capture("database_pid", lambda: run(["systemctl", "show", "--value", "-p", "MainPID", "mariadb.service"]))
        if database_pid and database_pid != "0":
            pids["mariadb"] = database_pid
        state["processes"] = {}
        process_rows = []
        for name, pid in sorted(pids.items()):
            detail = resources.proc_stat(pid)
            if detail is None:
                summary["errors"].append({"check": "process", "message": "unreadable: " + name})
                continue
            row = {"ts": ts, "name": name, "pid": pid, **detail, "cpu_percent": "",
                   "heap_used_kb": "", "heap_cap_kb": "", "ygc": "", "fgc": "", "gct": ""}
            old = previous.get("processes", {}).get(name)
            if old and old["pid"] == pid and old["start"] == detail["start"]:
                elapsed = now.timestamp() - previous["wall"]
                if elapsed > 0:
                    row["cpu_percent"] = round(100 * (detail["ticks"] - old["ticks"]) / os.sysconf("SC_CLK_TCK") / elapsed, 3)
            if name in INSTANCES:
                heap = resources.jstat(pid)
                if not heap:
                    summary["errors"].append({"check": "heap", "message": "jstat failed: " + name})
                row.update(heap)
            state["processes"][name] = {"pid": pid, **detail}
            process_rows.append(row)
        append(out / "processes.csv", ["ts", "name", "pid", "ticks", "start", "rss_kb", "threads", "cpu_percent",
                                      "heap_used_kb", "heap_cap_kb", "ygc", "fgc", "gct"], process_rows)
        summary["live_instances"] = [name for name in INSTANCES if name in pids]
        if len(summary["live_instances"]) != len(INSTANCES):
            summary["errors"].append({"check": "instances", "message": "expected four live JVMs"})
        summary["stores"] = {}
        for tier in TIERS:
            root = STORE / tier / "ArchiverStore"
            files = list(root.rglob("*.pb"))
            present = {keys[key] for path in files
                       for key in [str(path.relative_to(root)).rsplit(":", 1)[0]] if key in keys}
            size = capture(tier + "_bytes", lambda root=root: directory_bytes(root))
            summary["stores"][tier] = {"bytes": size, "files": len(files), "pvs": len(present)}
        for label, unit in (("unit", UNIT), ("health", HEALTH_UNIT)):
            capture(label, lambda unit=unit: run(["systemctl", "show", unit, "-p", "ActiveState", "-p", "Result",
                                                 "-p", "ExecMainStatus", "-p", "ExecMainExitTimestamp"]))
        capture("clock", lambda: run(["timedatectl", "show", "-p", "NTPSynchronized"]))
        if summary.get("clock") != "NTPSynchronized=yes":
            summary["errors"].append({"check": "clock", "message": "clock is not synchronized"})
        for label, unit in (("appliance", UNIT), ("ioc", IOC_UNIT), ("mariadb", "mariadb.service")):
            active = capture(label + "_active", lambda unit=unit: run(
                ["systemctl", "show", unit, "--value", "-p", "ActiveState"]))
            if active != "active":
                summary["errors"].append({"check": label, "message": "service is not active"})
        capture("database", lambda: run(["mysql", "--protocol=SOCKET", "-N", "-B", "archappl", "-e",
                                        "SELECT (SELECT COUNT(*) FROM PVTypeInfo), (SELECT COUNT(*) FROM ArchivePVRequests)"]))
        capture("mgmt", lambda: request("getApplianceInfo", raw / "appliance.json"))
        status = capture("pv_status_request", lambda: request("getPVStatus?pv=AASOAK*", raw / "pv-status.json"))
        if status is not None:
            records, milliseconds = status
            summary["pv_status_ms"] = milliseconds
            summary.pop("pv_status_request")
            observed = {item["pvName"]: item.get("status", "") for item in records}
            summary["archiving_pvs"] = sum(observed.get(name) == "Being archived" for name in names)
            summary["connected_pvs"] = sum(item.get("connectionState") == "true" for item in records
                                             if item["pvName"] in names)
            summary["missing_pvs"] = len(names - set(observed))
            summary["unexpected_pvs"] = len(set(observed) - names)
            if (summary["archiving_pvs"] != len(names) or summary["connected_pvs"] != len(names)
                    or summary["unexpected_pvs"]):
                summary["errors"].append({"check": "pv_status", "message": "fixture population is not fully archiving"})
        metrics = capture("metrics_request", lambda: request("getApplianceMetricsForAppliance?appliance=appliance0", raw / "metrics.json"))
        if metrics is not None:
            rows, milliseconds = metrics
            summary["metrics_ms"] = milliseconds
            summary['metrics_observed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            summary["metric_rows"] = len(rows)
            summary.pop("metrics_request")
            capture('event_rates', lambda: event_rates(rows, summary['metrics_observed_at']))
            append(out / "metrics.csv", ["ts", "source", "name", "value"],
                   [{"ts": ts, "source": row.get("source", ""), "name": row.get("name", "").replace("&raquo;", ">"),
                     "value": row.get("value", "")} for row in rows])
            if not rows:
                summary["errors"].append({"check": "metrics", "message": "empty metrics response"})
        capture("latency", lambda: measure.latency(out, raw, fixture, ts))
        capture("gc", lambda: measure.gc(out, raw, ts))
        manifest_path = out / "observation.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
            if manifest.get('measurement_schema') == contract.SCHEMA:
                capture('tool_bundle', lambda: contract.verify_bundle(Path(__file__).parent))
            for name, expected in manifest.get("jvm_identity", {}).items():
                current = state["processes"].get(name, {})
                if any(current.get(key) != expected[key] for key in ("pid", "start")):
                    summary["errors"].append({"check": "jvm_restart", "message": name})
    summary["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if not journal_only:
        state["consecutive_failures"] = previous.get("consecutive_failures", 0) + 1 if summary["errors"] else 0
    write_json(raw / "sample.json", summary)
    write_json(out / "latest.json", summary)
    if not journal_only:
        write_json(out / "latest-full.json", summary)
    write_json(state_path, state)
    abort_if_required(out, summary, state)
    append(out / "samples.csv", ["ts", "raw_directory", "error_count"],
           [{"ts": ts, "raw_directory": str(raw), "error_count": len(summary["errors"])}])
    print(json.dumps({"observed_at": ts, "error_count": len(summary["errors"]),
                      "archiving_pvs": summary.get("archiving_pvs"), "closed_passes": journal[2] if journal else None}))
    return bool(summary["errors"])


def abort_if_required(out, summary, state):
    manifest_path = out / "observation.json"
    if summary['sample_kind'] == 'full' and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        policy = manifest.get("abort_policy", {})
        low_space = summary.get("disk", {}).get("available_bytes", measure.MINIMUM_FREE_BYTES) < measure.MINIMUM_FREE_BYTES
        repeated = state["consecutive_failures"] >= policy.get("consecutive_failures", float("inf"))
        if policy and (low_space or repeated) and not any((out / name).exists() for name in
                                                        ("shutdown.json", "abort.json", "shutdown-started.json", "abort-started.json")):
            if not (out / 'abort-request.json').exists():
                write_json(out / "abort-request.json", {"requested_at": summary["completed_at"],
                           "reason": "disk_reserve" if low_space else "consecutive_sample_failures",
                       "trigger_sample": str(Path(summary['raw_directory']) / "sample.json")})
            try:
                run(["systemctl", "--no-block", "start", ABORT_UNIT])
            except Exception as error:
                summary['errors'].append({'check': 'abort_dispatch', 'type': type(error).__name__,
                                          'message': str(error)})
                write_json(Path(summary['raw_directory']) / 'sample.json', summary)
                write_json(out / 'latest-full.json', summary)
                write_json(out / 'latest.json', summary)


def sample(out, fixture, journal_only=False):
    with locked(out / ".sample.lock"):
        try:
            return _sample(out, fixture, journal_only)
        except Exception as error:
            now = datetime.datetime.now(datetime.timezone.utc)
            raw = out / 'raw' / (now.strftime('%Y%m%dT%H%M%S.%fZ') + '-failed')
            raw.mkdir(parents=True)
            state_path = out / 'state.json'
            state = json.loads(state_path.read_text()) if state_path.exists() else {}
            summary = {'observed_at': now.isoformat(), 'completed_at': now.isoformat(),
                       'raw_directory': str(raw), 'sample_kind': 'journal' if journal_only else 'full',
                       'errors': [{'check': 'collection', 'type': type(error).__name__, 'message': str(error)}]}
            if not journal_only:
                state['consecutive_failures'] = state.get('consecutive_failures', 0) + 1
                write_json(out / 'latest-full.json', summary)
            write_json(raw / 'sample.json', summary)
            write_json(out / 'latest.json', summary)
            write_json(state_path, state)
            abort_if_required(out, summary, state)
            append(out / 'samples.csv', ['ts', 'raw_directory', 'error_count'],
                   [{'ts': summary['observed_at'], 'raw_directory': str(raw), 'error_count': len(summary['errors'])}])
            print(json.dumps({'observed_at': summary['observed_at'], 'error_count': len(summary['errors'])}))
            return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--journal-only", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    args.out.mkdir(parents=True, exist_ok=True)
    return sample(args.out, args.fixture, args.journal_only)


if __name__ == "__main__":
    raise SystemExit(main())
