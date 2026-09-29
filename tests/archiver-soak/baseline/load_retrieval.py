#!/usr/bin/env python3
"""Concurrent retrieval load for the load test.

Runs CLIENTS threads until the deadline. Each client picks a random PV from
the list and reads a one-hour window, or a one-day window for a 1 Hz scalar,
ending now, pauses briefly, and repeats; every request is appended to
retrieval-load.csv. The response is streamed and counted in chunks, never
held whole: a one-day window of a 10 Hz PV or a waveform is hundreds of MB.
Usage: load_retrieval.py <pvs.csv> <out_dir> <hours> [clients]
"""

import csv
import datetime
import os
import random
import sys
import threading
import time
import urllib.parse
import urllib.request

RETRIEVAL = "http://localhost:17668/retrieval/data/getData.json"
PAUSE_S = 2.0
WINDOWS = {"1h": 3600, "1d": 86400}


def main():
    pvs_csv, out_dir, hours = sys.argv[1], sys.argv[2], float(sys.argv[3])
    clients = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    with open(pvs_csv, newline="") as f:
        rows = list(csv.DictReader(f))
    pvs = [r["pv"] for r in rows]
    # Only a 1 Hz scalar gets a one-day window; everything else stays at one hour.
    day_ok = {r["pv"] for r in rows if r["scan"] == "1 second" and "WF" not in r["pv"]}
    deadline = time.monotonic() + hours * 3600
    out = os.path.join(out_dir, "retrieval-load.csv")
    lock = threading.Lock()
    if not os.path.exists(out):
        with open(out, "w", newline="") as f:
            csv.writer(f).writerow(["ts", "client", "pv", "window", "http", "ms", "bytes", "samples"])

    def client(cid):
        rng = random.Random(cid)
        while time.monotonic() < deadline:
            pv = rng.choice(pvs)
            window = rng.choice(list(WINDOWS)) if pv in day_ok else "1h"
            now = datetime.datetime.now(datetime.timezone.utc)
            frm = now - datetime.timedelta(seconds=WINDOWS[window])
            url = (f"{RETRIEVAL}?pv={urllib.parse.quote(pv)}"
                   f"&from={frm.strftime('%Y-%m-%dT%H:%M:%S.000Z')}"
                   f"&to={now.strftime('%Y-%m-%dT%H:%M:%S.000Z')}")
            t0 = time.monotonic()
            code, size, samples = 0, 0, ""
            try:
                with urllib.request.urlopen(url, timeout=120) as r:
                    code, size, samples, tail = r.status, 0, 0, b""
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        size += len(chunk)
                        # Count across the chunk boundary once: occurrences wholly
                        # inside the carried tail were counted with the last chunk.
                        data = tail + chunk
                        samples += data.count(b'"secs"') - tail.count(b'"secs"')
                        tail = data[-8:]
            except urllib.error.HTTPError as e:
                code = e.code
            except Exception:
                code = 0
            ms = round((time.monotonic() - t0) * 1000)
            with lock, open(out, "a", newline="") as f:
                csv.writer(f).writerow([now.strftime("%Y-%m-%dT%H:%M:%SZ"), cid, pv, window,
                                        code, ms, size, samples])
            time.sleep(PAUSE_S)

    threads = [threading.Thread(target=client, args=(i,)) for i in range(clients)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
