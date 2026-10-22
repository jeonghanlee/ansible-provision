# Archiver Installation Checks

## Scope

These checks exercise a real general-server SQLite installation on a dedicated
Rocky Linux 8.10 VM. The canonical test contract and observed results belong to
M51 in `docs/milestone-38560eb.md`.

Out of scope: physical-server deployment, source promotion, long observations,
performance comparisons and the aa-maven unit test suite.

## Prerequisites

Use Python 3.9 or newer for these tools. On Rocky 8.10, select the installed
`/usr/bin/python3.9` explicitly; the system `python3` may select Python 3.6.
The controller compatibility check also needs PyYAML, Bash, Git, GNU Make and
tar. The live collector needs the installed appliance, SQLite CLI, systemd and
one installed EPICS Base tree containing `softIoc` and `camonitor`.

Before live collection, complete the canonical installation preflight and full
Make assembly. Obtain the dedicated guest identity and private inventory from
its provider. Keep the fixed full source overrides and actual command receipts
under ignored `work/`; source defaults are not changed by this procedure.

## Execution And Evidence

`capture-command.py` executes the supplied command directly and retains its
complete stdout/stderr, native process return code, UTC bounds, monotonic elapsed
time and capture-tool hash in a new private directory. Arguments and output must
not contain credentials. Use a private extra-vars file for deployment settings.
The tool does not interpret a successful command as product acceptance.

```bash
python3 tests/archiver-install/capture-command.py work/install-contract -- make check-general-server-contract
```

The installation itself uses the shipped `archiver_server_sqlite.rocky8` Make
target with the actual runtime inventory, one-host limit and private fixed
source overrides. No task or internal function is substituted. The unchanged
110-record soak fixture supplies three selected archived PVs. Independent CA
events establish expected values and timestamps for retrieval comparison.

Preserve receipts on success, failure and interruption. A process killed before
final persistence leaves a visibly unfinished receipt; missing output is
Incomplete. Evaluate required functional claims only after final capture, and
freeze members/hashes before replaying saved-data comparisons on separate copies.
VM lifecycle is performed by its provider; send a finished notice when use ends.

## Target Check Interface

`target-check.py` provides `facts`, `health`, `fixture`, `register`, `ready`, `window`,
`requery`, `compare` and `stop` modes. Live modes require root and the configured dedicated
guest UUID; they retain command and HTTP evidence in a new output directory.
`compare` reads saved CA and retrieval inputs and reports Passed, Failed or
Incomplete. Configuration selects the PVs, fixture hash, sample count, timeouts
and timestamp tolerance. The canonical M51 results record which modes and data
comparisons actually ran; source checks alone establish no functional result.

Create a private JSON config using the actual provider UUID and installed SQLite
path. The values below implement the canonical three-PV contract. Replace the
UUID placeholder before live execution; it is checked against guest DMI before
any output directory or system change. The same unchanged config is required for
saved comparisons.

```json
{
  "expected_uuid": "<dedicated-guest-uuid>",
  "pvs": ["AASOAK:S1:CH01", "AASOAK:S1:CH02", "AASOAK:S1:CH03"],
  "fixture_sha256": "c0a70bbd3b4e9bf9b37df6ad3cb6fb5b78889c5dc1bac172ce738b5619d2e1b5",
  "sqlite_file": "/arch/config/archappl.sqlite",
  "minimum_updates": 60,
  "input_timeout_seconds": 120,
  "retrieval_timeout_seconds": 120,
  "timestamp_tolerance_ns": 1000
}
```

Copy `target-check.py`, `capture-command.py`, the private config and the unchanged
`tests/archiver-soak/fixtures/aasoak.db` to a root-owned private directory on the
assigned guest, here `/var/tmp/archiver-install`. Run the following commands in a
root Bash session on that guest. Create a new run directory; each mode requires a
new output directory with an existing parent.

```bash
py=/usr/bin/python3.9
tool=/var/tmp/archiver-install/target-check.py
capture=/var/tmp/archiver-install/capture-command.py
cfg=/var/tmp/archiver-install/config.json
db=/var/tmp/archiver-install/aasoak.db
run=$(mktemp -d /var/tmp/archiver-install/run.XXXXXXXX)
"$py" "$tool" facts --config "$cfg" --output "$run/facts-before"
"$py" "$tool" health --config "$cfg" --output "$run/health-before"
"$py" "$tool" fixture --config "$cfg" --fixture "$db" --output "$run/fixture"
"$py" "$tool" register --config "$cfg" --output "$run/register"
"$py" "$tool" ready --config "$cfg" --output "$run/ready-before"
"$py" "$tool" window --config "$cfg" --output "$run/window-before"
"$py" "$capture" "$run/compare-before" -- "$py" "$tool" compare --config "$cfg" --input "$run/window-before"
```

Live modes collect evidence; their status 0 alone does not accept the product.
Inspect `report.json`, native command receipts and HTTP bodies against every
canonical T3-T6 assertion. In particular, health must complete a new invocation,
SQLite access must succeed as the service account, and all four JVM identities
must be present. `compare` alone returns verdict statuses: Passed 0, Failed 1,
Incomplete 2. The examples use `capture-command.py` to retain its stdout/stderr
and native status separately from the finalized collection directory.

Run `ready` after registration and after restarting the appliance, before
starting an independent `window`. It requires retrieval data in at least three
distinct recent seconds for every selected PV within the input timeout. This
keeps initial sampling and reconnect time outside the comparison window. The
window's separate `compare` execution evaluates the finalized CA/HTTP inputs.
After restart, pass `ready --not-before-ns` a recorded guest UTC boundary after
startup; old samples cannot establish new collection. `requery --input` copies
the original independent CA reference unchanged and queries its exact original
interval again, then `compare` checks persistence against that reference.

For a normal restart, retain stop/start native results and capture the stopped
state before starting again. Record the guest UTC boundary after startup.

```bash
"$py" "$capture" "$run/app-stop" -- systemctl stop epicsarchiverap-maven.service
"$py" "$tool" facts --config "$cfg" --output "$run/facts-stopped"
"$py" "$capture" "$run/app-start" -- systemctl start epicsarchiverap-maven.service
"$py" -c 'import time; print(time.time_ns())' > "$run/restart-boundary-ns"
IFS= read -r boundary < "$run/restart-boundary-ns"
"$py" "$tool" facts --config "$cfg" --output "$run/facts-restarted"
"$py" "$tool" health --config "$cfg" --output "$run/health-restarted"
"$py" "$tool" requery --config "$cfg" --input "$run/window-before" --output "$run/old-window"
"$py" "$capture" "$run/compare-old" -- "$py" "$tool" compare --config "$cfg" --input "$run/old-window"
"$py" "$tool" ready --config "$cfg" --not-before-ns "$boundary" --output "$run/ready-after"
"$py" "$tool" window --config "$cfg" --output "$run/window-after"
"$py" "$capture" "$run/compare-after" -- "$py" "$tool" compare --config "$cfg" --input "$run/window-after"
```

Reapply the same controller Make target, inventory, limit and private inputs.
Take `facts` immediately before and after reapply. Check the actual launch result
for `ARCHIVER_BUILD_SKIPPED`, compare nonempty built WAR/deployed-file populations,
stamp and JVM/service lifetimes, then require new retrieval samples with `ready`
using a guest UTC boundary after reapply. Do not register the PVs again.

At completion, stop the fixture and inspect its actual unit state. Preserve the
whole run directory and the private config before sending the provider a finished
notice. On an unsuccessful step, retain partial evidence, stop the fixture if it
started, and finish the same retention/shutdown procedure; do not infer acceptance
from later successful commands.

```bash
"$py" "$tool" stop --config "$cfg" --output "$run/fixture-stop"
```

## Installation Compatibility Unit Check

`check-install-config.py` requires controller Python 3.9 or newer, PyYAML, Bash, Git, GNU
Make and tar. Supply `--role`, `--current`, repeated `--legacy`, `--maven` and
a new `--output` directory. The tool extracts the production role's rendering
function unchanged and calls it with actual Git-exported aa-env sources. The
actual Maven checkout supplies the source-version dependency. Source exports,
declared configuration mutations, the exact function, command streams and native
statuses are retained. Cases cover both old pins, current rendering, a missing
Make include and a missing render template. These are production-function unit
checks; the complete Ansible role is verified by the separate fresh VM trial.

## Saved Window Checks

`check-window-evidence.py` takes a retained actual `--input` window, its
`--config` and a new `--output` directory. It freezes the original membership,
copies the comparator and dependencies, and verifies fresh input copies before
and after every real CLI execution. Cases cover intact data, missing/partial CA
input, malformed retrieval, changed values/timestamps and a confirmed mismatch
alongside missing or malformed evidence for another PV. Fresh replay must agree
byte for byte, and the originals must remain unchanged.

Use `--old-tool` only with a retained earlier comparator. The mixed-case check
demonstrates its incorrect Incomplete verdict; the corrected comparator must
keep the confirmed Failed verdict. A Passed case in this driver means the
declared comparator outcome was observed. It is separate from appliance
acceptance and injects no fault into the live appliance.
