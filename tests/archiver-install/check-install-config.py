#!/usr/bin/env python3
"""Exercise the shipped rendering function against real aa-env source trees."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import yaml


FUNCTION = "render_install_config"
RENDERED = (
    "site-template/systemd/override.conf",
    "site-template/systemd/epicsarchiverap-maven.service",
    "site-template/systemd/epicsarchiverap-maven-health.service",
    "site-template/systemd/epicsarchiverap-maven-health.timer",
    "site-template/.versions",
)
ENVIRONMENT_KEYS = ("MAKEFLAGS", "MFLAGS", "GNUMAKEFLAGS", "MAKEOVERRIDES", "BASH_ENV", "ENV")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--legacy", type=Path, action="append", required=True)
    parser.add_argument("--maven", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output = args.output.resolve()
    role = args.role.resolve()
    tasks = yaml.safe_load(role.read_text())
    raw = tasks[0]["ansible.builtin.raw"]
    matches = re.findall(r"(?ms)^function " + FUNCTION + r" \{\n.*?^\}\n", raw)
    if len(matches) != 1:
        parser.error("Exactly one shipped rendering function is required")
    args.output.mkdir(mode=0o700, parents=False, exist_ok=False)
    function_script = args.output / "render-function.bash"
    function_script.write_text("#!/bin/bash\nset -e\n" + matches[0] + "\n" + FUNCTION + "\n")
    capture = Path(__file__).with_name("capture-command.py").resolve()
    environment = os.environ.copy()
    for key in ENVIRONMENT_KEYS:
        environment.pop(key, None)
    environment["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    sequence = 0

    def run(command, cwd):
        nonlocal sequence
        sequence += 1
        directory = args.output / ("command-{:03d}".format(sequence))
        subprocess.run([sys.executable, str(capture), str(directory), "--"] + command,
                       cwd=str(cwd), env=environment, check=False,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        receipt = json.loads((directory / "receipt.json").read_text())
        return receipt["returncode"], directory

    report = {"scope": "Production-function unit checks; no complete role installation claim",
              "role_sha256": digest(role), "function_sha256": digest(function_script),
              "tool_sha256": digest(Path(__file__)), "cases": []}
    cases = [("legacy-{}".format(i), path, "legacy") for i, path in enumerate(args.legacy)]
    cases += [("current", args.current, "current"),
              ("query-error", args.current, "query-error"),
              ("render-error", args.current, "render-error")]
    try:
        for label, source, kind in cases:
            source = source.resolve()
            case = args.output / label
            case.mkdir(mode=0o700)
            status, identity = run(["git", "-C", str(source), "rev-parse", "HEAD"], case)
            if status != 0:
                raise ValueError("Source identity query failed: " + label)
            commit = (identity / "stdout").read_text().strip()
            status, archive = run(["git", "-C", str(source), "archive", commit], case)
            if status != 0:
                raise ValueError("Actual source export failed: " + label)
            status, _ = run(["tar", "-xf", str(archive / "stdout"), "-C", str(case)], case)
            if status != 0:
                raise ValueError("Actual source extraction failed: " + label)
            (case / "epicsarchiverap-maven-src").symlink_to(args.maven.resolve(), target_is_directory=True)
            changes = {}
            if kind == "query-error":
                changes["Makefile"] = "\ninclude missing-install-contract.mk\n"
            elif kind == "render-error":
                changes["configure/CONFIG_SYSTEMD"] = "\nSYSTEMD_OVERRIDE_FILENAME:=missing-render.conf\n"
            for name, suffix in changes.items():
                with (case / name).open("a", encoding="ascii") as stream:
                    stream.write(suffix)
            snapshot = []
            for path in sorted(case.rglob("*")):
                if path.is_symlink():
                    snapshot.append({"path": str(path.relative_to(case)), "link": os.readlink(path)})
                elif path.is_file():
                    snapshot.append({"path": str(path.relative_to(case)), "sha256": digest(path)})
            save(case / "input.json", {"source_commit": commit, "archive_sha256": digest(archive / "stdout"),
                                       "mutations": changes, "members": snapshot})
            status, command = run(["/bin/bash", str(function_script)], case)
            stderr = (command / "stderr").read_text()
            generated = {name: (case / name).is_file() for name in RENDERED}
            expected = 2 if kind in ("query-error", "render-error") else 0
            passed = status == expected
            if kind == "legacy":
                passed = passed and not any(generated.values())
            elif kind == "current":
                passed = passed and all(generated.values())
            elif kind == "query-error":
                passed = passed and "cannot query install prerequisites" in stderr
            else:
                passed = passed and "No rule to make target" in stderr and "cannot query install prerequisites" not in stderr
            report["cases"].append({"case": label, "source_commit": commit, "native_status": status,
                                    "expected_status": expected, "generated": generated,
                                    "command_receipt": str(command.relative_to(args.output)),
                                    "result": "Passed" if passed else "Failed"})
    except (OSError, ValueError, KeyError) as error:
        report["error"] = str(error)
    report["result"] = ("Incomplete" if "error" in report else
                        "Passed" if all(row["result"] == "Passed" for row in report["cases"]) else "Failed")
    save(args.output / "report.json", report)
    print(json.dumps(report, indent=2))
    return {"Passed": 0, "Failed": 1, "Incomplete": 2}[report["result"]]


if __name__ == "__main__":
    sys.exit(main())
