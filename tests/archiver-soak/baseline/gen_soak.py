#!/usr/bin/env python3
"""Generate the soak IOC database and the PV registration list.

Writes aasoak.db (softIoc, base records only) and pvs.csv (one row per
archived PV: name, group, rate, method, period, policy, store key).
The store key is the path the appliance derives from the PV name, with
':', '_' and '-' each becoming a directory separator; the generator stops
when two PVs would share one key.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (group, count, name pattern, scan, kind, method, period, policy)
# kind: counter | walk | wave | enum | string
GROUPS = [
    ("basic", 10, "AASOAK:S1:CH{n:02d}", "1 second", "counter", "MONITOR", "1.0", ""),
    ("underscore", 10, "AASOAK:S1_UND:CH_{n:02d}", "1 second", "counter", "MONITOR", "1.0", ""),
    ("dash", 10, "AASOAK-DASH:S1-CH-{n:02d}", "1 second", "counter", "MONITOR", "1.0", ""),
    ("nested", 10, "AASOAK:N1:N2:N3:CH{n:02d}", "1 second", "counter", "SCAN", "1.0", ""),
    ("prefix", 10, "AASOAK:PFX_A:PFX_B:LEAF{n:02d}", "1 second", "counter", "MONITOR", "1.0", ""),
    ("long", 10, "AASOAK:LONG_SECTION_NAME:SUBSYSTEM_DEVICE_READBACK_VALUE_{n:02d}",
     "1 second", "counter", "MONITOR", "1.0", ""),
    ("fast", 10, "AASOAK:FAST:CH{n:02d}", ".1 second", "counter", "MONITOR", "0.1", "VeryFast"),
    ("slow", 10, "AASOAK:SLOW:CH{n:02d}", "10 second", "counter", "SCAN", "10.0", "Medium"),
    ("deadband", 10, "AASOAK:DB:CH{n:02d}", "1 second", "walk", "MONITOR", "1.0", "Fast"),
    ("wave", 5, "AASOAK:WF:CH{n:02d}", "1 second", "wave", "MONITOR", "1.0", ""),
    ("enum", 3, "AASOAK:ENUM:CH{n:02d}", "1 second", "enum", "SCAN", "1.0", ""),
    ("string", 2, "AASOAK:STR:CH{n:02d}", "1 second", "string", "MONITOR", "1.0", ""),
]

WAVE_NELM = 1000
DEADBAND = 2.0


def store_key(pv):
    return pv.replace(":", "/").replace("_", "/").replace("-", "/")


def counter(name, scan, n):
    # Sawtooth offset per channel so channels differ.
    return (
        f'record(calc, "{name}") {{\n'
        f'  field(SCAN, "{scan}")\n'
        f'  field(INPA, "{name}.VAL NPP")\n'
        f'  field(CALC, "(A+1)%3600")\n'
        f'  field(VAL, "{n * 100}")\n'
        f'  field(PREC, "1")\n'
        f"}}\n"
    )


def walk(name, scan):
    # Random walk; MDEL and ADEL make monitor updates sparse.
    return (
        f'record(calc, "{name}") {{\n'
        f'  field(SCAN, "{scan}")\n'
        f'  field(INPA, "{name}.VAL NPP")\n'
        f'  field(CALC, "A+RNDM-0.5")\n'
        f'  field(MDEL, "{DEADBAND}")\n'
        f'  field(ADEL, "{DEADBAND}")\n'
        f'  field(PREC, "3")\n'
        f"}}\n"
    )


def wave(name, scan):
    # A source calc feeds a circular-buffer compress record, so the whole
    # 1000-element array shifts by one element on every scan.
    src = f"{name}_SRC"
    return (
        f'record(calc, "{src}") {{\n'
        f'  field(SCAN, "{scan}")\n'
        f'  field(INPA, "{src}.VAL NPP")\n'
        f'  field(CALC, "A+1")\n'
        f'  field(FLNK, "{name}")\n'
        f"}}\n"
        f'record(compress, "{name}") {{\n'
        f'  field(INP, "{src}.VAL NPP")\n'
        f'  field(ALG, "Circular Buffer")\n'
        f'  field(NSAM, "{WAVE_NELM}")\n'
        f"}}\n"
    )


def enum(name, scan):
    src = f"{name}_SRC"
    return (
        f'record(calc, "{src}") {{\n'
        f'  field(SCAN, "{scan}")\n'
        f'  field(INPA, "{src}.VAL NPP")\n'
        f'  field(CALC, "(A+1)%4")\n'
        f'  field(FLNK, "{name}")\n'
        f"}}\n"
        f'record(mbbi, "{name}") {{\n'
        f'  field(DTYP, "Raw Soft Channel")\n'
        f'  field(INP, "{src}.VAL NPP")\n'
        f'  field(ZRVL, "0")\n  field(ZRST, "IDLE")\n'
        f'  field(ONVL, "1")\n  field(ONST, "RAMP")\n'
        f'  field(TWVL, "2")\n  field(TWST, "HOLD")\n'
        f'  field(THVL, "3")\n  field(THST, "FAULT")\n'
        f"}}\n"
    )


def string(name, scan):
    src = f"{name}_SRC"
    return (
        f'record(calc, "{src}") {{\n'
        f'  field(SCAN, "{scan}")\n'
        f'  field(INPA, "{src}.VAL NPP")\n'
        f'  field(CALC, "A+1")\n'
        f'  field(FLNK, "{name}")\n'
        f"}}\n"
        f'record(stringin, "{name}") {{\n'
        f'  field(INP, "{src}.VAL NPP")\n'
        f"}}\n"
    )


def main():
    rows = []
    db = []
    for group, count, pattern, scan, kind, method, period, policy in GROUPS:
        for n in range(1, count + 1):
            name = pattern.format(n=n)
            if kind == "counter":
                db.append(counter(name, scan, n))
            elif kind == "walk":
                db.append(walk(name, scan))
            elif kind == "wave":
                db.append(wave(name, scan))
            elif kind == "enum":
                db.append(enum(name, scan))
            else:
                db.append(string(name, scan))
            rows.append([name, group, scan, method, period, policy, store_key(name)])

    keys = [r[6] for r in rows]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    if dupes:
        sys.exit(f"store key collision: {dupes}")
    if len(rows) != 100:
        sys.exit(f"expected 100 PVs, got {len(rows)}")

    with open(os.path.join(HERE, "aasoak.db"), "w") as f:
        f.write("# Generated by gen_soak.py; do not edit.\n")
        f.write("\n".join(db))
    with open(os.path.join(HERE, "pvs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pv", "group", "scan", "method", "period", "policy", "store_key"])
        w.writerows(rows)
    print(f"{len(rows)} PVs, {len(db)} record blocks")


if __name__ == "__main__":
    main()
