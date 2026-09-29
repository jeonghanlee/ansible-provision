#!/usr/bin/env python3
"""Collect real appliance evidence, preserving failed samples and raw inputs."""

import argparse
import collections
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

import resource_helpers as resources
import measure

UNIT = "epicsarchiverap-maven.service"
HEALTH_UNIT = "epicsarchiverap-maven-health.service"
IOC_UNIT = "etl-soak-ioc.service"
MGMT = "http://127.0.0.1:17665/mgmt/bpl"
STORE = Path("/arch")
INSTANCES = ("mgmt", "engine", "etl", "retrieval")
TIERS = ("sts", "mts", "lts")
JOURNAL_KEYS = ("__CURSOR", "__REALTIME_TIMESTAMP", "SYSLOG_IDENTIFIER",
                "PRIORITY", "MESSAGE", "_PID", "_SYSTEMD_INVOCATION_ID")


def run(command, accepted=(0,), timeout=60):
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    if result.returncode not in accepted:
        raise RuntimeError("command failed: " + command[0] + ": " + str(result.returncode))
    return result.stdout.strip()


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
        command += ["--after-cursor", previous["journal_cursor"]]
    else:
        command += ["--since", now.strftime("%Y-%m-%d 00:00:00 UTC")]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError("journal collection failed: " + str(result.returncode))
    cursor = previous.get("journal_cursor")
    counts = collections.Counter()
    pass_count = 0
    with (raw / "journal.jsonl").open("w") as journal, (out / "passes.jsonl").open("a") as passes:
        for line in result.stdout.splitlines():
            entry = json.loads(line)
            selected = {key: entry[key] for key in JOURNAL_KEYS if key in entry}
            encoded = json.dumps(selected) + "\n"
            journal.write(encoded)
            cursor = entry["__CURSOR"]
            counts[entry.get("SYSLOG_IDENTIFIER", "unknown")] += 1
            if "ETL pass of transition " in str(entry.get("MESSAGE", "")):
                passes.write(encoded)
                pass_count += 1
    return cursor, dict(counts), pass_count


def sample(out, fixture, journal_only=False):
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%S.%fZ")
    ts = now.isoformat()
    raw = out / "raw" / stamp
    raw.mkdir(parents=True)
    state_path = out / "state.json"
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    state = dict(previous)
    summary = {"observed_at": ts, "errors": [], "raw_directory": str(raw)}

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
    if not journal_only:
        with fixture.open(newline="") as stream:
            pv_rows = list(csv.DictReader(stream))
        names = {row["pv"] for row in pv_rows}
        keys = {row["store_key"]: row["pv"] for row in pv_rows}
        summary["fixture_sha256"] = hashlib.sha256(fixture.read_bytes()).hexdigest()
        summary["expected_pvs"] = len(names)
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
            size = capture(tier + "_bytes", lambda root=root: int(run(["du", "-sb", str(root)]).split()[0]))
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
        health = dict(line.split("=", 1) for line in summary.get("health", "").splitlines() if "=" in line)
        if health.get("Result") != "success" or health.get("ExecMainStatus") != "0":
            summary["errors"].append({"check": "health", "message": "health service did not succeed"})
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
            summary["metric_rows"] = len(rows)
            summary.pop("metrics_request")
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
            for name, expected in manifest.get("jvm_identity", {}).items():
                current = state["processes"].get(name, {})
                if any(current.get(key) != expected[key] for key in ("pid", "start")):
                    summary["errors"].append({"check": "jvm_restart", "message": name})
        kernel = capture("kernel_memory_log", lambda: run(
            ["journalctl", "-k", "-b", "--since", now.strftime("%Y-%m-%d 00:00:00 UTC"),
             "--no-pager", "-o", "cat"]))
        if kernel is not None:
            memory_lines = [line for line in kernel.splitlines()
                            if any(term in line.lower() for term in ("out of memory", "oom-kill", "killed process"))]
            (raw / "kernel-memory.log").write_text("\n".join(memory_lines) + "\n")
            summary.pop("kernel_memory_log")
            summary["kernel_memory_events_today"] = len(memory_lines)
            if memory_lines:
                summary["errors"].append({"check": "kernel_memory", "message": "kernel memory event observed"})
    write_json(raw / "sample.json", summary)
    write_json(out / "latest.json", summary)
    write_json(state_path, state)
    append(out / "samples.csv", ["ts", "raw_directory", "error_count"],
           [{"ts": ts, "raw_directory": str(raw), "error_count": len(summary["errors"])}])
    print(json.dumps({"observed_at": ts, "error_count": len(summary["errors"]),
                      "archiving_pvs": summary.get("archiving_pvs"), "closed_passes": journal[2] if journal else None}))
    return bool(summary["errors"])


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
