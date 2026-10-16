#!/usr/bin/env python3
"""Verify actual E4 fault and shutdown records through the frozen native readers."""

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case-root', type=Path, required=True)
parser.add_argument('--input', type=Path, default=Path('/var/lib/etl-soak'))
parser.add_argument('--tools', type=Path, default=Path('/usr/local/share/etl-soak'))
args = parser.parse_args()
ROOT = args.case_root.resolve()
OUT = args.input.resolve()
TOOLS = args.tools.resolve()
sys.path.insert(0, str(TOOLS))
import collect
import contract
import evaluate
import evidence
import focused
import observe

def load(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

originals = {str(path): digest(path) for path in
             (ROOT / "runtime.json", ROOT / "runtime-contract.json", OUT / "observation.json", OUT / "abort.json")}
hashes = contract.verify_bundle(TOOLS)
runtime = load(ROOT / "runtime.json")
declaration = load(ROOT / "runtime-contract.json")
manifest = load(OUT / "observation.json")
terminal = load(OUT / "abort.json")
assert runtime["case"] == declaration["case"] == "E4"
assert runtime["stage"] == runtime["expectation"] == "Incomplete"
assert hashes == declaration["tool_hashes"] == manifest["tool_hashes"]
assert manifest["duration_seconds"] == 86400 and not manifest["start_findings"]
assert terminal["observation"] == manifest and terminal["terminal_kind"] == "abort"
assert terminal["stop"]["rc"] == 0 and not terminal["errors"]
assert terminal["stop_elapsed_seconds"] <= observe.timeout_seconds(terminal["stop_timeout"])
assert (ROOT / "actual-sampler-before-fault.txt").read_bytes() == (ROOT / "actual-sampler-after-restoration.txt").read_bytes()
assert (ROOT / "declared-fault-dropin.conf").read_bytes() == (ROOT / "removed-fault-dropin.conf").read_bytes()
restoration = load(ROOT / "actual-restoration.json")
assert restoration["fault_dropin_absent"] and restoration["original_effective_unit_bytes_equal"]
assert not Path("/etc/systemd/system/etl-soak-sample.service.d/90-negative-fault.conf").exists()
assert digest(ROOT / "actual-sampler-after-restoration.txt") == restoration["restored_effective_unit_sha256"]
states = {}
for path in (ROOT / "actual-state-history").glob("*.json"):
    assert digest(path) == path.stem
    states[path.stem] = load(path)
first = load(ROOT / "actual-first-fault-sample.json")
assert first["automatic_abort_request_absent"]
assert digest(Path(first["sample"])) == first["sample_sha256"]
assert states[first["state_sha256"]]["consecutive_abort_failures"] == 1
request = load(OUT / "abort-request.json")
assert request["reason"] == "consecutive_sample_failures"
began = load(ROOT / "actual-fault-begin.json")
start_ns = evidence.timestamp_ns(began["observed_at"])
end_ns = evidence.timestamp_ns(request["requested_at"])
samples = []
for path in sorted((OUT / "raw").glob("*/sample.json")):
    sample = load(path)
    if sample.get("sample_kind") == "full" and start_ns <= evidence.timestamp_ns(sample["observed_at"]) < end_ns:
        samples.append((path, sample))
assert len(samples) == declaration["minimum_fault_full_samples"] == 2
probes = [load(path) for path in (ROOT / "namespace-probes").glob("*/receipt.json")]
probes = [row for row in probes if not row["probe_only"]]
assert len(probes) >= 2
for probe in probes:
    assert probe["native_collector_sha256"] == hashes["collect.py"]
    assert probe["journal_query"].get("returncode", -1) != 0
    assert all(not row["available"] for row in probe["files"].values())
events = [json.loads(line) for line in (ROOT / "actual-sampler-journal.stdout").read_text().splitlines()]
for index, (path, sample) in enumerate(samples, 1):
    checks = {row["check"] for row in sample["errors"]}
    assert checks == {"journal", "health_journal", "kernel_journal"}
    assert collect.critical(sample, **collect.abort_policy(OUT))
    matches = []
    for event in events:
        try:
            message = json.loads(event.get("MESSAGE", ""))
        except (TypeError, ValueError):
            continue
        if isinstance(message, dict) and message.get("observed_at") == sample["observed_at"]:
            matches.append(event)
    assert len(matches) == 1
    assert matches[0]["_SYSTEMD_UNIT"] == "etl-soak-sample.service"
    assert sum(str(probe["pid"]) == matches[0]["_PID"] for probe in probes) == 1
    wall = datetime.datetime.fromisoformat(sample["observed_at"]).timestamp()
    corresponding = [row for row in states.values() if row.get("wall") == wall]
    assert corresponding and all(row["consecutive_abort_failures"] == index for row in corresponding)
assert request["trigger_sample"] == str(samples[1][0])
recorded_invocations = set()
for path in ROOT.glob("actual-abort-invocation-*.txt"):
    properties = collect.properties(path.read_text())
    recorded_invocations.add(properties["InvocationID"])
abort_events = [json.loads(line) for line in (ROOT / "actual-abort-unit-journal.stdout").read_text().splitlines()]
actual_invocations = {row["_SYSTEMD_INVOCATION_ID"] for row in abort_events
                      if row.get("_SYSTEMD_UNIT") == "etl-soak-abort.service" and row.get("_SYSTEMD_INVOCATION_ID")}
assert actual_invocations == recorded_invocations and len(actual_invocations) == 1
target = declaration["target_native_sts_pass"]
outside = evaluate.pass_records(ROOT / "outside-native-passes.jsonl")
invocation = began["identity"]["invocation_id"]
literal = [row for row in outside if row["transition"] == target["transition"] and
           row["invocation_id"] == invocation and row["plannedAt"] == target["planned_at"]]
matching = [row for row in outside if row["transition"] == target["transition"] and
            row["invocation_id"] == invocation and
            evidence.timestamp_ns(row["plannedAt"]) == evidence.timestamp_ns(target["planned_at"])]
assert len(literal) == 0 and len(matching) == 1
witness = matching[0]
focused.successful_pass(witness)
assert start_ns <= evidence.timestamp_ns(witness["startedAt"]) <= evidence.timestamp_ns(witness["endedAt"]) <= end_ns
actual = subprocess.run(["/usr/bin/python3", "-B", str(TOOLS / "evaluate.py"), "--input", str(OUT)],
                        capture_output=True, timeout=180)
assert actual.returncode == 1 and not actual.stderr
native = json.loads(actual.stdout)
assert native["verdict"] == "Incomplete"
assert "observation_duration" in native["failed_assertions"]
appliance = collect.properties(subprocess.check_output(["systemctl", "show", "epicsarchiverap-maven.service",
    "-p", "MainPID", "-p", "ActiveState", "-p", "Result"], text=True))
assert appliance["MainPID"] == "0" and appliance["ActiveState"] == "inactive" and appliance["Result"] == "success"
assert all(digest(Path(path)) == value for path, value in originals.items())
assert contract.verify_bundle(TOOLS) == hashes
print(json.dumps({"observed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "case": "E4", "chain": "shortened", "expectation": "Passed",
    "acceptance_scope": "Two actual unavailable-source samples triggered one automatic abort and orderly appliance stop",
    "fault_full_samples": [{"observed_at": row["observed_at"], "sha256": digest(path)}
                           for path, row in samples],
    "counter_sequence": [1, 2], "automatic_abort_invocations": 1,
    "stop_rc": terminal["stop"]["rc"], "stop_elapsed_seconds": terminal["stop_elapsed_seconds"],
    "fault_restored": True, "appliance_stopped": True,
    "actual_etl_pass": {key: witness.get(key) for key in
                       ("transition", "plannedAt", "startedAt", "endedAt", "pvCount", "jobsRun",
                        "jobsFailed", "jobsAborted", "jobsSkipped", "aborted", "overrun")},
    "declared_planned_at": target["planned_at"], "literal_time_matches": len(literal),
    "native_timestamp_matches": len(matching),
    "original_runtime_verdict": runtime["expectation"], "native_observation_verdict": terminal["verdict"],
    "native_replay_verdict": native["verdict"], "original_hashes": originals,
    "originals_unchanged": True, "bundle_unchanged": True, "guest_modified": False}, sort_keys=True))
