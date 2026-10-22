#!/usr/bin/env python3
"""Retain a real command's streams, timing, identity and native return code."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    temporary = path.with_suffix(".tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="New private receipt directory")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("A command is required")
    directory = args.directory.resolve()
    directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    receipt_path = directory / "receipt.json"
    receipt = {
        "schema": 1,
        "state": "starting",
        "argv": command,
        "cwd": os.getcwd(),
        "started_utc": utc_now(),
        "started_monotonic_ns": time.monotonic_ns(),
        "capture_tool_sha256": digest(Path(__file__).resolve()),
        "python": sys.version,
        "returncode": None,
        "signals": [],
    }
    write_json(receipt_path, receipt)
    process = None

    def forward_signal(number, _frame):
        receipt["signals"].append({"signal": number, "utc": utc_now()})
        if process is not None and process.poll() is None:
            try:
                os.killpg(process.pid, number)
            except ProcessLookupError:
                pass

    for number in (signal.SIGINT, signal.SIGTERM):
        signal.signal(number, forward_signal)
    try:
        with (directory / "stdout").open("xb") as stdout:
            with (directory / "stderr").open("xb") as stderr:
                process = subprocess.Popen(
                    command, stdout=stdout, stderr=stderr, start_new_session=True
                )
                receipt.update(state="running", pid=process.pid)
                write_json(receipt_path, receipt)
                receipt["returncode"] = process.wait()
        receipt["state"] = "completed"
    except OSError as error:
        receipt.update(state="incomplete", error=str(error))
    finally:
        receipt.update(
            finished_utc=utc_now(),
            finished_monotonic_ns=time.monotonic_ns(),
        )
        receipt["elapsed_ns"] = (
            receipt["finished_monotonic_ns"] - receipt["started_monotonic_ns"]
        )
        receipt["streams"] = {
            name: {"bytes": (directory / name).stat().st_size,
                   "sha256": digest(directory / name)}
            for name in ("stdout", "stderr") if (directory / name).is_file()
        }
        write_json(receipt_path, receipt)
    print(str(receipt_path))
    status = receipt["returncode"]
    if status is None:
        return 2
    return status if status >= 0 else 128 - status


if __name__ == "__main__":
    sys.exit(main())
