#!/usr/bin/env python3
"""Verify the real comparator on retained CA/HTTP evidence and changed copies."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


NANOSECONDS_PER_SECOND = 1000000000
VALUE_CHANGE = 1000000
TIME_CHANGE_MULTIPLIER = 100


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def members(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError("Evidence symlinks are not supported")
        if path.is_file():
            result[str(path.relative_to(directory))] = {
                "sha256": digest(path), "bytes": path.stat().st_size,
                "mode": path.stat().st_mode & 0o777,
            }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tool", type=Path, default=Path(__file__).with_name("target-check.py"))
    parser.add_argument("--old-tool", type=Path)
    args = parser.parse_args()
    original = args.input.resolve()
    output = args.output.resolve()
    original_members = members(original)
    if not original_members:
        parser.error("Retained actual window evidence is required")
    config = json.loads(args.config.read_text())
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    save(output / "original-members.json", original_members)
    tools = output / "tools"
    tools.mkdir(mode=0o700)
    shutil.copy2(args.tool, tools / "target-check.py")
    shutil.copy2(Path(__file__).with_name("capture-command.py"), tools / "capture-command.py")
    shutil.copy2(__file__, tools / "check-window-evidence.py")
    shutil.copy2(args.config, output / "config.json")
    if args.old_tool:
        shutil.copy2(args.old_tool, tools / "old-target-check.py")
    tool_members = members(tools)
    config_sha256 = digest(output / "config.json")
    save(output / "execution-source.json", {
        "tools": tool_members, "config_sha256": config_sha256,
        "python": sys.version, "python_executable": sys.executable,
        "python_sha256": digest(Path(sys.executable).resolve()),
    })
    report = {"cases": [], "result": "Incomplete"}

    def run(label, input_directory, expected, tool="target-check.py"):
        frozen = members(input_directory)
        save(output / (label + "-members.json"), frozen)
        if members(input_directory) != frozen or members(tools) != tool_members:
            raise ValueError("Pre-launch source or evidence changed")
        if digest(output / "config.json") != config_sha256:
            raise ValueError("Comparison configuration changed")
        directory = output / (label + "-command")
        command = [sys.executable, str(tools / "capture-command.py"), str(directory), "--",
                   sys.executable, "-B", str(tools / tool), "compare", "--config",
                   str(output / "config.json"), "--input", str(input_directory)]
        subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        receipt = json.loads((directory / "receipt.json").read_text())
        observed = json.loads((directory / "stdout").read_text())
        if members(input_directory) != frozen or members(tools) != tool_members:
            raise ValueError("Execution changed frozen evidence or tools")
        actual = observed["result"]
        native = receipt["returncode"]
        expected_status = {"Passed": 0, "Failed": 1, "Incomplete": 2}[expected]
        passed = receipt["state"] == "completed" and actual == expected and native == expected_status
        row = {"case": label, "expected": expected, "observed": actual,
               "native_status": native, "command_receipt": str(directory.relative_to(output)),
               "result": "Passed" if passed else "Failed"}
        report["cases"].append(row)
        return row, (directory / "stdout").read_bytes()

    def prepare(label, mutation):
        target = output / label
        shutil.copytree(original, target)
        if members(target) != original_members:
            raise ValueError("Fresh copy differs from original evidence")
        metadata = json.loads((target / "window.json").read_text())
        first, second = config["pvs"][:2]
        first_body = target / metadata["queries"][first]["body"]
        second_body = target / metadata["queries"][second]["body"]
        if first_body.parent.resolve() != target or second_body.parent.resolve() != target:
            raise ValueError("Mutation input must remain inside the copied evidence")
        if mutation == "missing-reference":
            (target / "camonitor.stdout").rename(target / "camonitor.omitted")
        elif mutation == "partial-reference":
            path = target / "camonitor.stdout"
            body = path.read_bytes()
            path.write_bytes(body[:len(body) // 2])
        elif mutation == "malformed-retrieval":
            body = first_body.read_bytes()
            first_body.write_bytes(body[:len(body) // 2])
        elif mutation in ("value-mismatch", "time-mismatch", "mismatch-and-missing", "mismatch-and-malformed"):
            document = json.loads(first_body.read_text())
            for sample in document[0]["data"]:
                if "val" not in sample:
                    continue
                if mutation == "time-mismatch":
                    stamp = sample["secs"] * NANOSECONDS_PER_SECOND + sample["nanos"]
                    stamp += config["timestamp_tolerance_ns"] * TIME_CHANGE_MULTIPLIER
                    sample["secs"], sample["nanos"] = divmod(stamp, NANOSECONDS_PER_SECOND)
                else:
                    sample["val"] += VALUE_CHANGE
            first_body.write_text(json.dumps(document) + "\n")
            if mutation == "mismatch-and-missing":
                second_body.rename(second_body.with_suffix(".omitted"))
            elif mutation == "mismatch-and-malformed":
                body = second_body.read_bytes()
                second_body.write_bytes(body[:len(body) // 2])
        return target

    try:
        intact, baseline = run("intact", prepare("intact-input", None), "Passed")
        if intact["result"] != "Passed":
            raise ValueError("Actual intact evidence did not establish the baseline")
        for label, expected in (
            ("missing-reference", "Incomplete"), ("partial-reference", "Incomplete"),
            ("malformed-retrieval", "Incomplete"), ("value-mismatch", "Failed"),
            ("time-mismatch", "Failed"), ("mismatch-and-missing", "Failed"),
            ("mismatch-and-malformed", "Failed"),
        ):
            run(label, prepare(label + "-input", label), expected)
        replay, replay_bytes = run("fresh-replay", prepare("fresh-replay-input", None), "Passed")
        report["replay_byte_equal"] = replay_bytes == baseline and replay["result"] == "Passed"
        if args.old_tool:
            old, _ = run("old-mixed-verdict", prepare("old-mixed-input", "mismatch-and-missing"),
                         "Incomplete", tool="old-target-check.py")
            report["old_defect_exposed"] = old["observed"] == "Incomplete" and old["native_status"] == 2
            old["scope"] = "Observed previous incorrect verdict; correctness requires Failed"
        report["originals_unchanged"] = members(original) == original_members
    except (OSError, ValueError, KeyError, TypeError) as error:
        report["error"] = str(error)
    if any(row["result"] == "Failed" for row in report["cases"]):
        report["result"] = "Failed"
    elif "error" in report:
        report["result"] = "Incomplete"
    else:
        report["result"] = ("Passed" if report.get("replay_byte_equal") and
                            report.get("originals_unchanged") and
                            (not args.old_tool or report.get("old_defect_exposed")) else "Failed")
    save(output / "report.json", report)
    print(json.dumps(report, indent=2))
    return {"Passed": 0, "Failed": 1, "Incomplete": 2}[report["result"]]


if __name__ == "__main__":
    sys.exit(main())
