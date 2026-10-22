#!/usr/bin/env python3
"""Collect dedicated-guest installation evidence and compare saved PV samples."""

import argparse
import calendar
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


APPLIANCE = Path("/opt/epicsarchiverap-maven")
ENV_SOURCE = Path("/opt/epicsarchiverap-env-src/epicsarchiverap-env")
FIXTURE_ROOT = Path("/var/lib/archiver-install")
UNIT = "epicsarchiverap-maven.service"
HEALTH = "epicsarchiverap-maven-health.service"
IOC_UNIT = "archiver-install-ioc.service"
COMPONENTS = ("mgmt", "engine", "etl", "retrieval")
READY_WINDOW_SECONDS = 30
READY_SAMPLE_COUNT = 3
NANOSECONDS_PER_SECOND = 1000000000
PROPERTIES = ("LoadState", "ActiveState", "SubState", "Result", "MainPID",
              "InvocationID", "ExecMainStatus", "ExecMainCode",
              "ExecMainStartTimestampMonotonic", "ExecMainExitTimestampMonotonic",
              "TimeoutStopUSec")
MONITOR_LINE = re.compile(
    r"^(\S+)\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})"
    r"\.(\d{1,9})\s+(\S+)(.*)$"
)


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def monitor_records(path, pvs):
    records = {pv: [] for pv in pvs}
    errors = []
    occurrences = Counter()
    seen = set()
    for line in Path(path).read_text(errors="strict").splitlines():
        match = MONITOR_LINE.match(line)
        if not match:
            if line.split() and line.split()[0] in pvs:
                errors.append(line)
            continue
        pv, date, clock, fraction, value, alarm = match.groups()
        if pv not in records:
            errors.append(line)
            continue
        try:
            numeric = Decimal(value)
            if not numeric.is_finite() or "INVALID" in alarm:
                raise ValueError("Unusable numeric reference")
            stamp = calendar.timegm(datetime.strptime(
                date + " " + clock, "%Y-%m-%d %H:%M:%S"
            ).timetuple()) * 1000000000 + int(fraction.ljust(9, "0"))
        except (ValueError, InvalidOperation):
            errors.append(line)
            continue
        key = (pv, stamp, numeric)
        occurrences[pv] += 1
        if key not in seen:
            records[pv].append({"timestamp_ns": stamp, "value": value,
                                "timestamp_text": date + " " + clock + "." + fraction,
                                "fraction_digits": len(fraction), "raw": line})
            seen.add(key)
    return records, dict(occurrences), errors


def retrieval_records(directory, pv, query):
    if not query or not query.get("body"):
        raise ValueError("No valid retrieval response")
    body = directory / query["body"]
    if body.parent.resolve() != directory.resolve():
        raise ValueError("Retrieval evidence must remain inside its directory")
    document = json.loads(body.read_text())
    if not isinstance(document, list) or len(document) != 1:
        raise ValueError("Expected one retrieval channel")
    if document[0].get("meta", {}).get("name") != pv:
        raise ValueError("Retrieval channel identity mismatch")
    samples = document[0]["data"]
    if not isinstance(samples, list):
        raise ValueError("Retrieval samples must be an array")
    indexed = {}
    for sample in samples:
        if "val" not in sample:
            continue
        if type(sample["secs"]) is not int or type(sample["nanos"]) is not int:
            raise ValueError("Retrieval timestamps require integer seconds/nanoseconds")
        if not 0 <= sample["nanos"] < 1000000000:
            raise ValueError("Retrieval nanoseconds are outside their range")
        value = Decimal(str(sample["val"]))
        if not value.is_finite():
            raise ValueError("Retrieval numeric value is not finite")
        stamp = sample["secs"] * 1000000000 + sample["nanos"]
        indexed.setdefault(stamp // 1000000000, []).append((stamp, value))
    return indexed, len(samples)


def compare(directory, config, metadata):
    directory = Path(directory)
    if metadata.get("config") != config:
        raise ValueError("Comparison configuration differs from the captured configuration")
    records, occurrences, errors = monitor_records(directory / "camonitor.stdout", config["pvs"])
    result = {"result": "Passed", "pvs": {}, "reference_errors": errors,
              "occurrences": occurrences, "missing_evidence": []}
    confirmed_failure = False
    for pv in config["pvs"]:
        rows = records[pv]
        changes = sum(Decimal(a["value"]) != Decimal(b["value"])
                      for a, b in zip(rows, rows[1:]))
        missing = []
        query = metadata.get("queries", {}).get(pv)
        if changes < config["minimum_updates"]:
            result["missing_evidence"].append(pv + ": insufficient independent updates")
        precision_valid = not any(10 ** (9 - row["fraction_digits"]) > config["timestamp_tolerance_ns"] for row in rows)
        clock_valid = not any(a["timestamp_ns"] > b["timestamp_ns"] for a, b in zip(rows, rows[1:]))
        if not precision_valid:
            result["missing_evidence"].append(pv + ": insufficient reference timestamp precision")
        if not clock_valid:
            result["missing_evidence"].append(pv + ": reference clock moved backwards")
        query_valid = True
        try:
            indexed, retrieved_count = retrieval_records(directory, pv, query)
        except (OSError, ValueError, KeyError, TypeError, AttributeError, InvalidOperation) as error:
            query_valid = False
            indexed, retrieved_count = {}, 0
            result["missing_evidence"].append(pv + ": " + str(error))
        for row in rows:
            stamp = row["timestamp_ns"]
            candidates = []
            for second in (stamp // 1000000000 - 1, stamp // 1000000000, stamp // 1000000000 + 1):
                candidates.extend(indexed.get(second, []))
            if not any(abs(actual - stamp) <= config["timestamp_tolerance_ns"]
                       and value == Decimal(row["value"]) for actual, value in candidates):
                missing.append(row)
        comparable = query_valid and precision_valid and clock_valid
        confirmed_failure = confirmed_failure or bool(missing and comparable)
        result["pvs"][pv] = {"reference_records": len(rows), "actual_updates": changes,
                              "retrieved_records": retrieved_count, "missing": missing,
                              "comparable": comparable,
                              "first": rows[0] if rows else None, "last": rows[-1] if rows else None}
    if confirmed_failure:
        result["result"] = "Failed"
    elif errors or result["missing_evidence"]:
        result["result"] = "Incomplete"
    return result


class Collector:
    def __init__(self, directory, config):
        self.directory = Path(directory)
        self.config = config
        self.sequence = 0
        self.fixture_started = False
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def run(self, argv, env=None):
        self.sequence += 1
        prefix = "command-{:04d}".format(self.sequence)
        started = utc()
        begin = time.monotonic_ns()
        with (self.directory / (prefix + ".stdout")).open("xb") as stdout:
            with (self.directory / (prefix + ".stderr")).open("xb") as stderr:
                native = subprocess.run(argv, stdout=stdout, stderr=stderr, env=env)
        receipt = {"argv": argv, "returncode": native.returncode, "started_utc": started,
                   "finished_utc": utc(), "elapsed_ns": time.monotonic_ns() - begin,
                   "stdout": prefix + ".stdout", "stderr": prefix + ".stderr"}
        save(self.directory / (prefix + ".json"), receipt)
        return receipt, (self.directory / receipt["stdout"]).read_text()

    def _request(self, path, parameters=None, data=None, retrieval=False):
        self.sequence += 1
        prefix = "http-{:04d}".format(self.sequence)
        base = "http://127.0.0.1:17668/retrieval/" if retrieval else "http://127.0.0.1:17665/mgmt/bpl/"
        url = base + path
        if parameters:
            url += "?" + urllib.parse.urlencode(parameters)
        payload = json.dumps(data).encode() if data is not None else None
        request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        receipt = {"url": url, "method": request.get_method(), "started_utc": utc(),
                   "request": data, "body": prefix + ".body"}
        begin = time.monotonic_ns()
        raw = b""
        try:
            try:
                with self.opener.open(request, timeout=20) as response:
                    receipt.update(status=response.status, headers=dict(response.headers))
                    raw = response.read()
            except urllib.error.HTTPError as error:
                receipt.update(status=error.code, headers=dict(error.headers))
                raw = error.read()
            if not 200 <= receipt["status"] < 300:
                raise ValueError("Unsuccessful HTTP response")
            document = json.loads(raw)
            if isinstance(document, dict) and document.get("status") == "error":
                raise ValueError("Application error response")
            receipt["valid_json"] = True
        except Exception as error:
            receipt.update(valid_json=False, error=str(error))
            document = None
        finally:
            (self.directory / receipt["body"]).write_bytes(raw)
            receipt.update(finished_utc=utc(), elapsed_ns=time.monotonic_ns() - begin)
            save(self.directory / (prefix + ".json"), receipt)
        return document, receipt

    def unit(self, name):
        receipt, output = self.run(["systemctl", "show", name, *["--property=" + p for p in PROPERTIES]])
        return {"receipt": receipt, "properties": dict(line.split("=", 1) for line in output.splitlines() if "=" in line)}

    def facts(self):
        result = {"service": self.unit(UNIT), "health": self.unit(HEALTH), "jvms": {}, "wars": {},
                  "build_wars": {}, "deployed_files": {},
                  "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}
        uid = pwd.getpwnam("mid-srv").pw_uid
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                arguments = (entry / "cmdline").read_bytes().split(b"\0")
                for component in COMPONENTS:
                    marker = ("-Dcatalina.base=" + str(APPLIANCE / component)).encode()
                    if marker in arguments:
                        fields = (entry / "stat").read_text().rsplit(") ", 1)[1].split()
                        result["jvms"].setdefault(component, []).append({
                            "pid": int(entry.name), "start_ticks": fields[19],
                            "uid": entry.stat().st_uid, "expected_uid": uid,
                            "cgroup": (entry / "cgroup").read_text(),
                            "argv": [x.decode() for x in arguments if x]})
            except (FileNotFoundError, ProcessLookupError):
                continue
        for path in sorted(APPLIANCE.rglob("*.war")):
            result["wars"][str(path.relative_to(APPLIANCE))] = sha(path)
        for path in sorted((ENV_SOURCE / "epicsarchiverap-maven-src" / "target").glob("*.war")):
            result["build_wars"][path.name] = sha(path)
        for component in COMPONENTS:
            for path in sorted((APPLIANCE / component / "webapps").rglob("*")):
                if path.is_file():
                    result["deployed_files"][str(path.relative_to(APPLIANCE))] = sha(path)
        stamp = Path("/var/tmp/archiver-build.config")
        result["install_stamp_sha256"] = sha(stamp) if stamp.is_file() else None
        for key, path in (("aa-env", ENV_SOURCE), ("aa-maven", ENV_SOURCE / "epicsarchiverap-maven-src")):
            receipt, output = self.run(["git", "-C", str(path), "rev-parse", "HEAD"])
            result[key] = {"receipt": receipt, "commit": output.strip()}
        receipt, output = self.run(["runuser", "-u", "mid-srv", "--", "sqlite3", self.config["sqlite_file"], ".tables"])
        result["sqlite"] = {"receipt": receipt, "tables": output.split()}
        receipt, _ = self.run(["runuser", "-u", "mid-srv", "--", "test", "-w", self.config["sqlite_file"]])
        result["sqlite_write_access"] = receipt
        result["readiness"], result["readiness_receipt"] = self._request("getApplianceInfo")
        return result

    def epics_bin(self):
        candidates = list(Path("/opt/epics").glob("*/rocky-8.10/*/base/bin/linux-x86_64/softIoc"))
        if len(candidates) != 1:
            raise ValueError("Expected one installed EPICS Base binary tree")
        return candidates[0].parent

    def fixture(self, source):
        if sha(source) != self.config["fixture_sha256"]:
            raise ValueError("Unexpected fixture hash")
        unit = Path("/etc/systemd/system") / IOC_UNIT
        if unit.exists():
            raise ValueError("Fixture unit already exists")
        FIXTURE_ROOT.mkdir(exist_ok=True, mode=0o755)
        target = FIXTURE_ROOT / "aasoak.db"
        with target.open("xb") as stream:
            stream.write(Path(source).read_bytes())
        target.chmod(0o644)
        unit.write_text("[Unit]\nDescription=Archiver installation IOC fixture\n[Service]\n"
                        "User=mid-srv\nGroup=mid\nType=simple\nRestart=no\n"
                        "ExecStart=" + str(self.epics_bin() / "softIoc") + " -S -d " + str(target) + "\n")
        self.run(["systemctl", "daemon-reload"])
        receipt, _ = self.run(["systemctl", "start", IOC_UNIT])
        if receipt["returncode"]:
            self.run(["systemctl", "stop", IOC_UNIT])
            raise RuntimeError("Fixture start failed")
        self.fixture_started = True
        return {"fixture_sha256": sha(target), "record_count": sum(line.startswith("record(") for line in target.read_text().splitlines()),
                "unit": self.unit(IOC_UNIT)}

    def register(self):
        body = [{"pv": pv, "samplingperiod": "1", "samplingmethod": "MONITOR"} for pv in self.config["pvs"]]
        document, receipt = self._request("archivePV", data=body)
        return {"response": document, "receipt": receipt}

    def queries(self, begin, end):
        result = {}
        for pv in self.config["pvs"]:
            document, receipt = self._request("data/getData.json", {"pv": pv, "from": begin, "to": end}, retrieval=True)
            result[pv] = {"body": receipt["body"] if receipt["valid_json"] else None, "receipt": receipt}
        return result

    def ready(self, not_before_ns=0):
        deadline = time.monotonic() + self.config["input_timeout_seconds"]
        attempt = 0
        while True:
            attempt += 1
            now = int(time.time())
            lower = now - READY_WINDOW_SECONDS
            lower_ns = max(lower * NANOSECONDS_PER_SECOND, not_before_ns)
            begin = datetime.fromtimestamp(lower, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            end = datetime.fromtimestamp(now + 1, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            queries = self.queries(begin, end)
            counts = {}
            errors = {}
            for pv in self.config["pvs"]:
                try:
                    indexed, _ = retrieval_records(self.directory, pv, queries[pv])
                    counts[pv] = sum(any(lower_ns <= stamp <= now * NANOSECONDS_PER_SECOND
                                         for stamp, _ in rows) for rows in indexed.values())
                except (OSError, ValueError, KeyError, TypeError, AttributeError, InvalidOperation) as error:
                    counts[pv] = 0
                    errors[pv] = str(error)
            observation = {"queries": queries, "query_from": begin, "query_to": end,
                           "not_before_ns": not_before_ns,
                           "recent_sample_seconds": counts, "errors": errors}
            save(self.directory / ("ready-{:04d}.json".format(attempt)), observation)
            if all(count >= READY_SAMPLE_COUNT for count in counts.values()):
                return {"ready": True, "observation": observation}
            if time.monotonic() >= deadline:
                raise ValueError("Required recent retrieval samples did not become available")
            time.sleep(2)

    def requery(self, source):
        metadata = json.loads((source / "window.json").read_text())
        if metadata["config"] != self.config:
            raise ValueError("Source-window configuration differs from the current configuration")
        for name in ("camonitor.stdout", "camonitor.stderr", "camonitor.json"):
            shutil.copy2(source / name, self.directory / name)
        metadata["queries"] = self.queries(metadata["query_from"], metadata["query_to"])
        save(self.directory / "window.json", metadata)
        return {"source_window": str(source), "comparison_input": "window.json",
                "capture_finalized": True}

    def window(self):
        environment = dict(os.environ, TZ="UTC", LC_ALL="C", EPICS_CA_ADDR_LIST="127.0.0.1", EPICS_CA_AUTO_ADDR_LIST="NO")
        command = [str(self.epics_bin() / "camonitor"), *self.config["pvs"]]
        started = utc()
        begin = time.monotonic_ns()
        with (self.directory / "camonitor.stdout").open("xb") as stdout:
            with (self.directory / "camonitor.stderr").open("xb") as stderr:
                process = subprocess.Popen(command, stdout=stdout, stderr=stderr, env=environment)
                try:
                    deadline = time.monotonic() + self.config["input_timeout_seconds"]
                    while process.poll() is None and time.monotonic() < deadline:
                        records, _, _ = monitor_records(self.directory / "camonitor.stdout", self.config["pvs"])
                        if all(sum(Decimal(a["value"]) != Decimal(b["value"]) for a, b in zip(rows, rows[1:])) >= self.config["minimum_updates"] for rows in records.values()):
                            break
                        time.sleep(1)
                finally:
                    if process.poll() is None:
                        process.terminate()
                    try:
                        native = process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        native = process.wait()
        monitor = {"argv": command, "returncode": native, "started_utc": started, "finished_utc": utc(),
                   "elapsed_ns": time.monotonic_ns() - begin}
        save(self.directory / "camonitor.json", monitor)
        records, _, _ = monitor_records(self.directory / "camonitor.stdout", self.config["pvs"])
        stamps = [row["timestamp_ns"] for rows in records.values() for row in rows]
        if not stamps:
            raise ValueError("Independent CA capture is empty")
        lower = min(stamps) // 1000000000 - 1
        upper = max(stamps) // 1000000000 + 2
        begin_text = datetime.fromtimestamp(lower, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_text = datetime.fromtimestamp(upper, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        deadline = time.monotonic() + self.config["retrieval_timeout_seconds"]
        attempt = 0
        while True:
            attempt += 1
            metadata = {"queries": self.queries(begin_text, end_text), "query_from": begin_text,
                        "query_to": end_text, "monitor": monitor, "config": self.config}
            save(self.directory / ("attempt-{:04d}.json".format(attempt)), metadata)
            compared = compare(self.directory, self.config, metadata)
            if compared["result"] == "Passed" or time.monotonic() >= deadline:
                break
            time.sleep(2)
        save(self.directory / "window.json", metadata)
        return {"capture_finalized": True, "comparison_input": "window.json"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("facts", "health", "fixture", "register", "ready", "window", "requery", "compare", "stop"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--not-before-ns", type=int, default=0)
    args = parser.parse_args()
    if args.mode in ("compare", "requery") and args.input is None:
        parser.error("A finalized input window is required")
    if args.not_before_ns < 0:
        parser.error("The readiness time boundary must be nonnegative")
    try:
        config = json.loads(args.config.read_text())
        pvs = config["pvs"]
        if not isinstance(pvs, list) or any(not isinstance(pv, str) or not pv for pv in pvs):
            raise ValueError("PV selection must be a list of nonempty names")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    if len(pvs) != len(set(pvs)) or not pvs:
        parser.error("A nonempty unique PV selection is required")
    if args.mode == "compare":
        try:
            metadata = json.loads((args.input / "window.json").read_text())
            result = compare(args.input, config, metadata)
        except (OSError, ValueError, KeyError, TypeError, InvalidOperation) as error:
            result = {"result": "Incomplete", "error": str(error)}
        print(json.dumps(result, indent=2))
        return {"Passed": 0, "Failed": 1, "Incomplete": 2}[result["result"]]
    if os.geteuid() != 0:
        parser.error("Dedicated guest identity and root execution are required")
    try:
        actual_uuid = Path("/sys/class/dmi/id/product_uuid").read_text().strip().lower()
        expected_uuid = config["expected_uuid"].lower()
    except (OSError, KeyError, AttributeError) as error:
        parser.error(str(error))
    if actual_uuid != expected_uuid:
        parser.error("Dedicated guest identity and root execution are required")
    if args.output is None:
        parser.error("A new output directory is required")
    args.output.mkdir(mode=0o700, parents=False, exist_ok=False)
    collector = Collector(args.output, config)
    report = {"mode": args.mode, "started_utc": utc(), "tool_sha256": sha(__file__), "config_sha256": sha(args.config)}
    code = 0
    try:
        if args.mode == "facts":
            report["facts"] = collector.facts()
        elif args.mode == "health":
            report["before"] = collector.unit(HEALTH)
            report["start"], _ = collector.run(["systemctl", "start", HEALTH])
            report["after"] = collector.unit(HEALTH)
        elif args.mode == "fixture":
            report["fixture"] = collector.fixture(args.fixture)
        elif args.mode == "register":
            report["registration"] = collector.register()
        elif args.mode == "ready":
            report["readiness"] = collector.ready(args.not_before_ns)
        elif args.mode == "requery":
            report["capture"] = collector.requery(args.input)
        elif args.mode == "window":
            report["capture"] = collector.window()
        else:
            report["stop"], _ = collector.run(["systemctl", "stop", IOC_UNIT])
            report["after"] = collector.unit(IOC_UNIT)
    except Exception as error:
        report["error"] = str(error)
        if args.mode == "fixture" and collector.fixture_started:
            report["fixture_failure_stop"], _ = collector.run(["systemctl", "stop", IOC_UNIT])
        code = 2
    finally:
        report["finished_utc"] = utc()
        save(args.output / "report.json", report)
    print(json.dumps(report, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
