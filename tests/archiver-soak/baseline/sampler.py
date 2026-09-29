#!/usr/bin/env python3
"""One soak sample: host, processes, logs, tiers, database, retrieval.

Run as root every 5 minutes. Appends to CSV files under OUT_DIR and keeps
the previous CPU counters in state.json so CPU use is a rate over the
interval. Stdlib only (the soak host has Python 3.9).
Usage: sampler.py <out_dir> <pvs.csv>
"""

import csv
import datetime
import glob
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

INSTALL = "/opt/epicsarchiverap-maven"
INSTANCES = ["mgmt", "engine", "etl", "retrieval"]
STORE = "/arch"
TIERS = ["sts", "mts", "lts"]
UNIT = "epicsarchiverap-maven.service"
HEALTH = "epicsarchiverap-maven-health.service"
IOC_UNITS = {"ioc": "aasoak9-ioc.service", "ioc_load1": "aasoak9-load1.service",
             "ioc_load2": "aasoak9-load2.service", "retrieval_load": "aasoak9-retrieval-load.service"}
MGMT = "http://localhost:17665/mgmt/bpl"
RETRIEVAL = "http://localhost:17668/retrieval/data/getData.json"
RETRIEVAL_PVS = ["AASOAK:S1:CH01", "AASOAK:FAST:CH01", "AASOAK:WF:CH01"]
DB_NAME = "archappl"
INTERVAL_S = 300

APP_LINE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (\w+)")
JULI_LINE = re.compile(r"^\d{2}-\w{3}-\d{4} \d{2}:\d{2}:\d{2}\.\d{3} (\w+)")
# In catalina.out JULI prints two lines per record; the level opens the second.
JULI_LEVEL_LINE = re.compile(r"^(SEVERE|WARNING|INFO):")
ACCESS_STATUS = re.compile(r'" (\d{3}) ')


def sh(cmd, timeout=60):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except subprocess.TimeoutExpired:
        return ""


def append(path, header, rows):
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(header)
        w.writerows(rows)


def http_get(url, timeout=30):
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            body = r.read()
            return r.status, (time.monotonic() - t0) * 1000, body
    except urllib.error.HTTPError as e:
        return e.code, (time.monotonic() - t0) * 1000, b""
    except Exception:
        return 0, (time.monotonic() - t0) * 1000, b""


def cpu_totals():
    with open("/proc/stat") as f:
        v = [int(x) for x in f.readline().split()[1:]]
    # user nice system idle iowait irq softirq steal
    return {"user": v[0] + v[1], "sys": v[2] + v[5] + v[6], "idle": v[3],
            "iowait": v[4], "total": sum(v[:8])}


def meminfo():
    m = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":", 1)
            m[k] = int(v.split()[0])
    return m


def proc_stat(pid):
    try:
        with open(f"/proc/{pid}/stat") as f:
            fields = f.read().rsplit(")", 1)[1].split()
        with open(f"/proc/{pid}/status") as f:
            st = dict(line.split(":", 1) for line in f if ":" in line)
        return {
            "ticks": int(fields[11]) + int(fields[12]),
            "start": int(fields[19]),
            "rss_kb": int(st["VmRSS"].split()[0]),
            "threads": int(st["Threads"]),
        }
    except (OSError, KeyError, IndexError, ValueError):
        return None


def jstat(pid):
    out = sh(f"jstat -gc {pid}").splitlines()
    if len(out) < 2:
        return {}
    d = dict(zip(out[0].split(), out[1].split()))
    try:
        used = sum(float(d[k]) for k in ("S0U", "S1U", "EU", "OU"))
        cap = sum(float(d[k]) for k in ("S0C", "S1C", "EC", "OC"))
        return {"heap_used_kb": round(used), "heap_cap_kb": round(cap),
                "ygc": d.get("YGC", ""), "fgc": d.get("FGC", ""), "gct": d.get("GCT", "")}
    except (KeyError, ValueError):
        return {}


def jvm_pids():
    # Scan /proc directly: a pgrep -f run through a shell would also match
    # the shell whose own command line carries the pattern.
    found = {}
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            with open(f"/proc/{d}/cmdline", "rb") as f:
                args = f.read().split(b"\0")
        except OSError:
            continue
        for inst in INSTANCES:
            if f"-Dcatalina.base={INSTALL}/{inst}".encode() in args:
                found.setdefault(inst, d)
    return found


def processes():
    jvms = jvm_pids()
    procs = {inst: jvms.get(inst, "") for inst in INSTANCES}
    procs["mariadb"] = sh("pgrep -x mariadbd | head -1") or sh("pgrep -x mysqld | head -1")
    for name, unit in IOC_UNITS.items():
        pid = sh(f"systemctl show -p MainPID --value {unit}")
        if pid and pid != "0":
            procs[name] = pid
        elif name == "ioc":
            procs[name] = ""
    return procs


def count_file(path, access):
    c = {"bytes": os.path.getsize(path), "lines": 0, "app_error": 0, "app_warn": 0,
         "app_info": 0, "app_other": 0, "juli_severe": 0, "juli_warning": 0,
         "juli_info": 0, "exceptions": 0, "access_5xx": 0}
    with open(path, errors="replace") as f:
        for line in f:
            c["lines"] += 1
            if access:
                m = ACCESS_STATUS.search(line)
                if m and m.group(1).startswith("5"):
                    c["access_5xx"] += 1
                continue
            if "Exception" in line:
                c["exceptions"] += 1
            m = APP_LINE.match(line)
            if m:
                lvl = m.group(1)
                key = {"ERROR": "app_error", "FATAL": "app_error", "WARN": "app_warn",
                       "INFO": "app_info"}.get(lvl, "app_other")
                c[key] += 1
                continue
            m = JULI_LINE.match(line) or JULI_LEVEL_LINE.match(line)
            if m:
                key = {"SEVERE": "juli_severe", "WARNING": "juli_warning",
                       "INFO": "juli_info"}.get(m.group(1))
                if key:
                    c[key] += 1
    return c


def du_bytes(path):
    out = sh(f"du -sb {path} 2>/dev/null | cut -f1")
    return int(out) if out.isdigit() else ""


def main():
    out_dir, pvs_csv = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    state_path = os.path.join(out_dir, "state.json")
    try:
        with open(state_path) as f:
            prev = json.load(f)
    except (OSError, ValueError):
        prev = {}
    state = {}

    # --- host CPU over the interval ---
    cpu = cpu_totals()
    state["cpu"] = cpu
    pc = prev.get("cpu")
    if pc and cpu["total"] > pc["total"]:
        dt = cpu["total"] - pc["total"]
        cpu_pct = {k: round(100.0 * (cpu[k] - pc[k]) / dt, 1) for k in ("user", "sys", "iowait", "idle")}
    else:
        cpu_pct = {k: "" for k in ("user", "sys", "iowait", "idle")}
    hz = os.sysconf("SC_CLK_TCK")

    # --- processes ---
    procs = processes()
    proc_rows = []
    state["proc"] = {}
    for name, pid in procs.items():
        p = proc_stat(pid) if pid else None
        if not p:
            proc_rows.append([ts, name, "", "", "", "", "", "", "", "", "", "", ""])
            continue
        state["proc"][name] = {"pid": pid, "ticks": p["ticks"]}
        pp = prev.get("proc", {}).get(name)
        pct = ""
        if pp and pp["pid"] == pid and "wall" in prev:
            wall = now.timestamp() - prev["wall"]
            if wall > 0:
                pct = round(100.0 * (p["ticks"] - pp["ticks"]) / hz / wall, 1)
        j = jstat(pid) if name in INSTANCES else {}
        proc_rows.append([ts, name, pid, p["start"], p["rss_kb"], p["threads"], p["ticks"], pct,
                          j.get("heap_used_kb", ""), j.get("heap_cap_kb", ""),
                          j.get("ygc", ""), j.get("fgc", ""), j.get("gct", "")])
    state["wall"] = now.timestamp()
    append(os.path.join(out_dir, "proc.csv"),
           ["ts", "name", "pid", "start_ticks", "rss_kb", "threads", "cpu_ticks", "cpu_pct",
            "heap_used_kb", "heap_cap_kb", "ygc", "fgc", "gct"], proc_rows)

    # --- logs per instance ---
    log_rows = []
    for inst in INSTANCES:
        logdir = f"{INSTALL}/{inst}/logs"
        for path in sorted(glob.glob(f"{logdir}/*")):
            if not os.path.isfile(path):
                continue
            c = count_file(path, os.path.basename(path).startswith("localhost_access_log"))
            log_rows.append([ts, inst, os.path.basename(path), c["bytes"], c["lines"],
                             c["app_error"], c["app_warn"], c["app_info"], c["app_other"],
                             c["juli_severe"], c["juli_warning"], c["juli_info"],
                             c["exceptions"], c["access_5xx"]])
        log_rows.append([ts, inst, "_logs_dir_", du_bytes(logdir), "", "", "", "", "", "", "",
                         "", "", ""])
    append(os.path.join(out_dir, "logs.csv"),
           ["ts", "instance", "file", "bytes", "lines", "app_error", "app_warn", "app_info",
            "app_other", "juli_severe", "juli_warning", "juli_info", "exceptions", "access_5xx"],
           log_rows)

    # --- tiers: files per tier and first arrival per PV ---
    with open(pvs_csv, newline="") as f:
        key_to_pv = {r["store_key"]: r["pv"] for r in csv.DictReader(f)}
    first_path = os.path.join(out_dir, "first_arrival.csv")
    seen = set()
    if os.path.exists(first_path):
        with open(first_path, newline="") as f:
            seen = {(r["pv"], r["tier"]) for r in csv.DictReader(f)}
    tier_stats = {}
    new_first = []
    for tier in TIERS:
        root = f"{STORE}/{tier}/ArchiverStore"
        files = [p for p in glob.glob(f"{root}/**/*.pb", recursive=True)]
        pvs_here = set()
        for p in files:
            key = os.path.relpath(p, root).rsplit(":", 1)[0]
            pv = key_to_pv.get(key)
            if pv:
                pvs_here.add(pv)
        tier_stats[tier] = (du_bytes(root), len(files), len(pvs_here))
        for pv in sorted(pvs_here):
            if (pv, tier) not in seen:
                new_first.append([pv, tier, ts])
    append(first_path, ["pv", "tier", "first_seen_utc"], new_first)

    # --- appliance state ---
    mgmt_code, mgmt_ms, _ = http_get(f"{MGMT}/getApplianceInfo")
    code, _, body = http_get(f"{MGMT}/getPVStatus?pv=AASOAK*", timeout=60)
    being, other = "", ""
    if code == 200:
        try:
            st = json.loads(body.decode())
            being = sum(1 for s in st if s.get("status") == "Being archived")
            other = len(st) - being
        except ValueError:
            pass
    q = "SELECT (SELECT COUNT(*) FROM PVTypeInfo), (SELECT COUNT(*) FROM ArchivePVRequests)"
    db = sh(f'mysql -N -B {DB_NAME} -e "{q}"').split()
    live = sum(1 for inst in INSTANCES if procs.get(inst))
    health = sh(f"systemctl show -p Result --value {HEALTH}")
    health_at = sh(f"systemctl show -p ExecMainExitTimestamp --value {HEALTH}")
    oom = sh("journalctl -k -b --no-pager -q | grep -c -i 'out of memory'") or "0"
    unit_lines = sh(f"journalctl -u {UNIT} -b --no-pager -q -o cat | wc -l")
    crash = sh(f"find {INSTALL} -maxdepth 3 \\( -name 'hs_err*' -o -name '*.hprof' \\) | wc -l")
    load = open("/proc/loadavg").read().split()
    m = meminfo()
    host_row = [ts, cpu_pct["user"], cpu_pct["sys"], cpu_pct["iowait"], cpu_pct["idle"],
                load[0], load[1], m.get("MemAvailable", ""),
                m.get("SwapTotal", 0) - m.get("SwapFree", 0), du_bytes(STORE)]
    for tier in TIERS:
        host_row += list(tier_stats[tier])
    host_row += [sh(f"systemctl is-active {UNIT}"), live, mgmt_code, round(mgmt_ms),
                 db[0] if len(db) > 0 else "", db[1] if len(db) > 1 else "", being, other,
                 health, health_at, oom, unit_lines, crash]
    append(os.path.join(out_dir, "host.csv"),
           ["ts", "cpu_user", "cpu_sys", "cpu_iowait", "cpu_idle", "load1", "load5",
            "memavail_kb", "swap_used_kb", "arch_bytes",
            "sts_bytes", "sts_files", "sts_pvs", "mts_bytes", "mts_files", "mts_pvs",
            "lts_bytes", "lts_files", "lts_pvs",
            "unit_state", "instances_live", "mgmt_code", "mgmt_ms",
            "pvtypeinfo_rows", "archivepvrequests_rows", "pvs_being_archived", "pvs_other",
            "health_result", "health_exit_at", "kernel_oom", "unit_journal_lines", "crash_files"],
           [host_row])

    # --- retrieval over the last interval ---
    frm = (now - datetime.timedelta(seconds=INTERVAL_S)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    to = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    ret_rows = []
    for pv in RETRIEVAL_PVS:
        url = f"{RETRIEVAL}?pv={urllib.parse.quote(pv)}&from={frm}&to={to}"
        code, ms, body = http_get(url, timeout=60)
        n = ""
        if code == 200:
            try:
                n = sum(len(x.get("data", [])) for x in json.loads(body.decode()))
            except ValueError:
                pass
        ret_rows.append([ts, pv, code, round(ms), n])
    append(os.path.join(out_dir, "retrieval.csv"), ["ts", "pv", "http", "ms", "samples"], ret_rows)

    # --- appliance metrics (engine, ETL, retrieval, mgmt), one row per metric ---
    code, _, body = http_get(f"{MGMT}/getApplianceMetricsForAppliance?appliance=appliance0", timeout=60)
    met_rows = []
    if code == 200:
        try:
            for m in json.loads(body.decode()):
                met_rows.append([ts, m.get("source", ""), m.get("name", "").replace("&raquo;", ">"),
                                 m.get("value", "")])
        except ValueError:
            pass
    append(os.path.join(out_dir, "metrics.csv"), ["ts", "source", "name", "value"], met_rows)

    with open(state_path, "w") as f:
        json.dump(state, f)


if __name__ == "__main__":
    main()
