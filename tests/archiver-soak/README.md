# Archiver Soak Tools

## Scope

Preserve the tools, fixtures and measurement methods used for the archiver
functional/load soak and the parallel ETL scheduler observations. The source
baseline files preserve the executed tools. The ETL collector and observation
tools provide versioned 7200/86400-second workflows for both chains. This directory is
suitable for Git tracking.

Out of scope: VM inventories, SSH settings, credentials, application
configuration backups, measured CSVs, logs, JFR recordings and live run status.
Those belong in private evidence directories. The canonical plan and observed
verification results are in [the work register](../../docs/milestone-38560eb.md).

## Contents

| Path | Purpose |
| --- | --- |
| `etl-pass/collect.py` | Collect journal entries, closed ETL passes, raw metrics, process resources, stores, service state and the added GC/latency measurements |
| `etl-pass/measure.py`, `heap.jfc` | Capture GC heap/collection/pause events, complete jstat fields, retrieval freshness and representative visibility bounds |
| `etl-pass/resource_helpers.py` | Host, process and JVM helpers imported by the collector; preserves the baseline sampler source |
| `etl-pass/install-fixture.py` | Install the loopback IOC and systemd collection units on an empty appliance, without registering PVs |
| `etl-pass/initialize-fresh.py` | Initialize GC/JFR and finite measurement units on a fresh deployment; prepare from actual journal and capacity proofs |
| `etl-pass/register.py` | Register a CSV fixture through the real mgmt API and retain the registration response status |
| `etl-pass/observe.py` | Open a default 24-hour or explicit 7200-second observation; preserve final evidence and measure shutdown or early abort |
| `etl-pass/prepare-retest.py`, `apply-fixture.py` | Preserve completed evidence, install measurement tools and verify the accepted existing deadband override before observation |
| `etl-pass/health-event.py`, `verify-health.py` | Retain actual health invocation results and verify the installed exit-status contract through real collection |
| `etl-pass/verify-runtime.py`, `launch-retest.py` | Verify real negative freshness and abort paths, then refresh readiness at a UTC launch target |
| `etl-pass/evaluate.py`, `test_retest.py` | Evaluate schedule, metrics, health and measurement coverage; exercise shipped code with external transport boundaries |
| `etl-pass/test_evidence.py` | Replay retained completed runtime evidence through the actual evaluator and verify failed or missing input handling |
| `etl-pass/contract.py`, `bundle.json`, `verify-chain.py` | Bind duration, actual stores, measured capacity and the complete frozen bundle |
| `etl-pass/aggregate.py`, `evidence.py`, `rate-semantics.json` | Portable numerical aggregation, bounded GC overlap handling and pinned metric meanings |
| `etl-pass/journal_coverage.py`, `journal_retention.py`, `test_journal.py` | System-only checkpoints, bounded sequence coverage, measured retention budgets and local arithmetic/parser checks |
| `etl-pass/test_contract.py` | Contract, bundle, fixture-preservation and retained-export replay checks |
| `etl-pass/focused.py`, `PBFixture.java`, `test_focused.py` | Installed configuration inventory, real writer/decoder, automatic two-hop physical/HTTP checks and subsequent regular-pass evidence |
| `etl-pass/replace-bundle.py` | Replace an installed bundle by a frozen bundle while carrying every other file and keeping a preserved sibling and rollback; not a bundle member |
| `etl-pass/restart-observation.py` | Preserve a previous observation and restart its appliance with bounded GC/JFR settings and persistent ETL pass logging |
| `etl-pass/common.yml`, `shortened.yml`, `default.yml` | Fixed source pins, heap/database settings and the two store-chain configurations |
| `fixtures/` | Three IOC databases and four PV lists for the 100/500/903-PV populations |
| `baseline/gen_soak.py`, `gen_load.py` | Generate the original IOC databases and PV registration lists |
| `baseline/sampler.py`, `register.py`, `load_retrieval.py` | Original resource sampler, registration client and concurrent retrieval load client |
| `baseline/journald_facts.sh`, `step2.sh`, `store-test.yml` | Original journald inspection, second load-step launcher and shortened store configuration |
| `baseline/pilot/` | Earlier pilot IOC, sampler and installed policy source; independent of the 903-PV fixture |
| `SHA256SUMS` | File hashes for this preserved copy |

The current sources originate from `work/soak-etl-pass-3bdf378c/`; baseline
sources and fixtures originate from `work/soak-9eed006/`. The registration
client is shared by both workflows. `resource_helpers.py` and the baseline
sampler retain separate filenames because the current collector imports that
module name. Original working copies remain in private evidence directories.

## Environment And Fixture

The ETL tools target Rocky Linux 8.10, systemd 239, Python 3.9 or later, OpenJDK 21,
and the EPICS 1.3.0 distribution with Base 7.0.10. The executed VM baseline is
2 vCPU, 4096 MiB allocated RAM and a 20 GiB disk, with MariaDB on the same VM.
The current collector uses the MariaDB Unix socket. Each of mgmt, engine, etl
and retrieval has a 256M minimum and maximum heap.

`common.yml` pins epicsarchiverap-env `482cf2939ea997064e4a2df64e3cb420681f4566`,
the verified current head of `release-2.0.1`, and epicsarchiverap-maven
`162269e7db97f527626ba0b387933a8c47e8bb57`. Deployment variables require
unique keys and plain double-quoted scalar values; other YAML forms are rejected
by the source-pin guard. Apply it with exactly one store configuration through the shipped
`archiver_dev_uds` species (`archiver_dev` is a deprecated alias), using a separately supplied
private inventory.

| Configuration | STS | MTS | LTS |
| --- | --- | --- | --- |
| Shortened | 5-minute partitions, hold 2 | Hour partitions, hold 2 | Day partitions |
| Default | Hour partitions, hold 2 | Day partitions, hold 2 | Year partitions |

The original fixture contains 100 PVs. The first load adds 400; the second
adds 403, for 903 total. The combined list has 783 PVs at 1 second, 110 at
0.1 second and 10 at 10 seconds, with 880 MONITOR and 23 SCAN registrations.
Eight waveform PVs use 1000-element arrays. The databases contain additional
source records that are not registered as archived PVs. PV names and store
keys must remain unique.

The preserved `fixtures/pvs-all.csv` SHA256 is
`037a92691bc23a6dcac37ec3613ad19c9f80b93b689209ec8dc403b519eaf594`.
The same list, IOC databases, registration methods and rates serve both chains.

The accepted retest variant loads `fixtures/retest-deadband.db` after the
original three databases. It changes only MDEL and ADEL to -1 on the ten
deadband records, retaining their calculations, one-second scans, PV names and
registration settings. `apply-fixture.py` preserves the original IOC files and
verifies all twenty fields through actual CA reads. Every full sample checks
the file hashes and those fields. This variant has separate evidence from the
original fixture. The retained shortened/default disks are 40/48 GiB; each requires a measured capacity
projection that preserves at least 2 GiB free and stays below 85 percent usage.
The revised 24-hour plan applies this same variant to both chains.
`apply-fixture.py --verify-existing` preserves and verifies an existing
adjustment, including hashes, effective IOC command and twenty actual fields.
Conflicting inputs are rejected without replacement.

## Execution Contracts

The appliance unit is `epicsarchiverap-maven.service`; the installation is
`/opt/epicsarchiverap-maven`, with stores under `/arch/{sts,mts,lts}/ArchiverStore`.
The tools use local mgmt/retrieval APIs on ports 17665 and 17668, and the
fixture IOC is restricted to loopback. EPICS and Java binary paths are explicit
constants in the source and must match the installed environment.

The systemd services use tools and fixture files placed directly under
`/usr/local/share/etl-soak/`. Python modules must remain adjacent there.
Evidence is written under `/var/lib/etl-soak/` with private permissions.
Installation, registration, observation start, observation finish and restart
change appliance state; use them only in the intended isolated test environment.

### Fixture Installation And Registration

`install-fixture.py` requires an empty configuration database, the exact fixture
hash and no existing observation manifest. It preserves a private configuration
backup, configures loopback CA discovery and installs the IOC and measurement
units. Both appliance and IOC must be inactive. It starts neither service and
does not register PVs or install JFR settings. Supply the three databases and
`pvs-all.csv` under the installed tools directory before calling it. Start the
IOC and appliance explicitly afterward, apply the accepted override, then register.

`register.py` accepts a fixture CSV, an evidence directory, an optional output
filename and an optional mgmt URL. It sends one `archivePV` JSON request.
Registration replies alone do not establish readiness: the collector must
observe all 903 expected PVs connected and archiving, no unexpected PVs,
synchronized time and healthy services.

### Focused Automatic Transfer Before Soak

The focused workflow requires Python 3.9 or later and the installed JDK 21.
Verify the deployed interpreter version before running tools; a newer control-host
interpreter or a grammar-only check does not establish target runtime compatibility.
Use a fresh isolated appliance with all 903 fixture PVs connected and the accepted
deadband variant, before instrumentation or any observation manifest exists.

`focused.py run --chain=shortened` or `--chain=default` records all effective store
URLs, reductions, conditional flags, artifacts and process identities independently
of soak preparation. It installs persistent pass DEBUG, compiles `PBFixture.java`
against installed classes and normally stops the appliance. The helper seeds four
existing scalar-double policy PVs using the shipped PlainPB writer in an empty
staging store. Normal service startup and the real ticker perform ETL; the tools
never call ETL ticks or jobs themselves.
Completion permits an initially absent `chunkKey` only when it equals the exact
key independently generated for that PV by the installed converter class and
the unchanged deployed properties. All 903 PVs are checked. Existing keys must
remain identical; all other effective settings, flags, artifacts, tools and
process identities remain subject to exact comparison. The four selected PVs'
physical PB paths must also agree with the independently generated keys.

`focused.py recheck --chain=<chain>` accepts only a retained failure at the final
configuration comparison. It checks the original startup and repeat PB/HTTP
records, real source sample reduction expectations, regular pass records,
preparation hashes and unchanged running identity. It writes a separate
`recheck-<timestamp>/result.json`; the original records and `Incomplete` result
remain unchanged. This record-only proof does not satisfy the complete focused
proof required by continuity or authorize a soak. Run the checker from a separate
directory with its imports pointing to the original installed tools, preserving
the original tool inventory and compiled helper.
Before stopping, live STS events must be readable. With STS consolidation enabled,
normal shutdown can empty STS into unreduced MTS. The workflow compares each known
source timestamp's exact raw-event, value and alarm multiplicities across STS/MTS,
including matching events already in MTS. New timestamps received before shutdown
are allowed. Known source events in LTS and unsupported shutdown settings are rejected.
Both physical snapshots and the comparison proof are retained before any seed write.
The workflow then stops the IOC, requires both units inactive and every JVM absent,
and preserves the registration database and all three preparation storage trees.
A verified private archive contains every original file. Each complete active tree
is renamed to an absent `preparation-stores` destination outside all scanned roots
on the same filesystem; hashes and ownership are rechecked. Empty roots are created
at the original paths with their original ownership, modes and security attributes.
Original data and archives are retained. A collision, symlink, overlapping root,
cross-filesystem destination or partial move stops preparation without automatic
retry or deletion; the location of every completed move is recorded.

The real PB path inventory for every selected PV must be empty in STS/MTS/LTS
before seed, and MTS/LTS must remain empty afterward. Empty bounded event windows
do not satisfy this condition when files remain. Seed and exact writer readback run
while the appliance and IOC are stopped. The database, source pins and tools must
remain unchanged. The IOC then starts while the appliance remains stopped.
`PBFixture` reads real DBR_TIME_DOUBLE samples through the installed JCA library
using loopback discovery, preserving full seconds/nanoseconds, value and alarm.
Each selected PV must have a timestamp strictly later than its last seeded sample.
Every attempted CA read is retained; failure or timeout prevents appliance startup.
After rechecking the seeded files and preservation proof, the appliance starts
normally and all 903 names must again be connected and archiving. No stop, restart
or consolidation may occur between seed and completion of automatic transfer and
regular-repeat checks.

`common.yml`, the focused source guards and initializer SOURCE_PINS contain the
same approved full aa-env/Maven commits. Both inspectors reject different installed
commits or deployment-variable disagreement. The frozen bundle includes deployment
variables and the offline fixture installer. Final success verifies the immutable
preparation binding and preserved trees, separately from the new seed/run evidence.
PB snapshots decode the real files and retain only manifest intervals: the old fixture,
intermediate marker, recent bin and a completed 60-second pre-stop source interval.
All file paths and decoded-event counts are recorded. Each interval is at most 300
seconds, with at most eight intervals including the pre-stop intervals preserved
across seed-time selection. Overlapping intervals retain each event only once.
The shutdown comparison covers these captured source intervals, not every live sample.
The helper retains its 256 MiB heap. Logging setup reuses an existing focused drop-in
only when its entire content matches the required configuration path; other content
is rejected. The generated logging configuration and drop-in hashes are retained.
The optional `inventory` action writes to `/var/lib/etl-focused/inventory-<chain>/`,
separately from the execution directory, so inspection can precede `run`.
The latest installer deploys an exploded WAR. Inspection compares all installed
class/JAR bytes with the corresponding retained build WAR and records both hashes.

An empty completed-pass poll is valid and waits for real ticker results. Malformed
journal JSON is rejected. For an interrupted empty-pass poll after a verified seed,
`prepare-resume` preserves original files and compiled-helper hashes, the original
failure and logging configuration. It requires the same boot and service invocation,
with all four JVMs starting inside the original execution window. `resume` requires
these identities and all source hashes to remain unchanged, then independently
inspects all 903 effective settings, flags, artifacts and unchanged helper tools.
It performs the same physical/HTTP and regular-pass checks as `run`, without
stopping the appliance, adding seeds or manually invoking ETL. The preserved source,
resume guard and current inspection are included in the final proof hashes.
Before `Passed`, it compares the final inspection and current boot/invocation/JVM
identities with the original runtime, and checks the approved resume tools again.
All preserved original files, immutable live inputs, compiled helper and logging
hashes must still match the guard. Only live result and pass outputs may change;
final inspection uses a separate directory to preserve the original inventory.

The physical baseline contains eight old samples at reduction-bin boundaries and
two intermediate/recent markers for each selected PV. Raw policies require identical
timestamp/raw-event multiplicities; lastSample_10/30/60 policies require the independently
specified last timestamps, values, status and severity in each bin. Both old sources
must disappear. The intermediate marker remains exactly once in the tier selected by
actual processingTime. After the recent marker's bin closes, the workflow retains the
actual STS/MTS bin samples and requires matching HTTP input. Before LTS reduction it
expects those exact source events; in LTS a reduced policy expects the latest captured
timestamp, value, status and severity. Ongoing IOC samples can replace the recent marker
legitimately. Raw policies retain every captured event. Physical and HTTP comparisons
use the same fixed bin, and the original source proof remains bound by hashes.
HTTP retrieval also returns the expected fixed historical interval.

Every completed pass in the focused invocation must report 903 PVs/jobs, no failed,
aborted or skipped jobs, no space deletion and no overrun. Each transition must complete
a subsequent regular grid pass before physical/HTTP equality is checked again. The
default chain can require 28800 seconds plus 600 seconds for ticker/order completion.
Evidence remains under `/var/lib/etl-focused/<chain>/` and incomplete runs retain errors.

Only after focused success, start the 26-hour JFR recording and prepare the observation.
After the last readiness restart, `focused.py continuity --chain=<chain>` rechecks
artifacts, all PV settings/flags, current InvocationID and JVM PID/start identities, and
physical/HTTP data against the original proof. This is launch continuity evidence;
the original `inventory.json` remains immutable. Each inspection writes a separate
`continuity-<timestamp>-inventory.json`, whose path and hash are bound in
`readiness-continuity.json` and checked again before launch.
it does not establish restart-fault, commit-failure or deletion-failure safety.
`launch-retest.py` performs this readback followed by a real full sample. Observation
start rejects absent, changed or stale continuity evidence and insufficient JFR time.

### Recheck Proof Acceptance And Bundle Replacement

A focused execution that ended Incomplete at the final configuration comparison can be
accepted for continuity only through its separate retained-record recheck proof. The
approved proof of each chain is named by path and SHA256 in an approved list inside
`focused.py`; the original `result.json` stays Incomplete and is never changed. The
acceptance path (`recheck_acceptance`, used by `continuity` and `require_continuity`)
requires, from retained files:

- the original result to be the exact Incomplete configuration-comparison failure whose
  SHA256 the proof records, and the proof to be Passed for the same chain;
- every `source_evidence_sha256` and `recheck_evidence_sha256` entry to match its file;
- the proof's checker and helper hashes to equal the approved producing-version literals;
- the key-input PV names to equal the 903 PV names of the original `inventory.json`, the
  properties copy to equal the original deployed properties hash, the expected-keys hash
  to match, and only null-to-expected chunk key changes between original and recheck
  inventory;
- the proof identity to equal the final-inspection identity of the original execution.

Against a live appliance, `artifacts`, `pvs` and `flags` of a fresh inventory must equal
the recheck inventory strictly. The tools of a verified bundle must equal the recheck-time
tools except `focused.py` (excluded by name) and `PBFixture.java` (the approved helper
literal). `continuity` records the recheck proof hash beside the original result hash and
`require_continuity` rejects a proof that does not bind both.

`focused.py check-recheck --chain=<chain> --bundle-root=<frozen bundle directory>
--scratch=<new directory outside /var/lib/etl-focused>` performs the live comparison without
writing under the retained tree and records the path of every imported project module in
`recheck-acceptance.json`. It does not take the per-chain lock, whose file lives under the
retained tree, so it can run beside a `continuity` action. Run it from a private staging directory that holds only the
candidate `focused.py` and `PBFixture.java`; the installed modules are found through
`PYTHONPATH`, behind the script directory.

`etl-pass/replace-bundle.py` replaces an installed bundle and is not a member of the frozen
bundle. `replace --bundle=<directory or tar>` requires `bundle.json` to match the
`ACCEPTED_BUNDLE_SHA256` literal and every member to match it, refuses an existing staged
or preserved sibling and any active sampler or finish unit, copies the whole installed
directory with `cp -a` (ownership, mode, timestamps, security context), overwrites only the
members and `bundle.json`, verifies the staged copy, then renames the installed directory to
`<installed>.prev-<UTC>` and the staged copy into place. It refuses a symbolic link or a
non-regular file in the installed directory or the bundle, because an overwrite would write
through it. It prints both rollback commands and, for a failure between the two renames, the
single `mv` that restores the preserved sibling; it deletes nothing except the temporary
directory used to unpack an archive. `rollback --preserved=<directory>` renames the current
installation to `<installed>.rejected-<UTC>` and the preserved sibling back into place.

### GC And Latency Extension

`restart-observation.py` extends an existing observation. It consumes a JSON
object on stdin with exactly four source-file entries: `measure.py`, `heap.jfc`,
`collect.py` and `observe.py`; each value is the file's complete text. Its
preconditions include an active appliance, at least 10 GiB free, an existing
older observation, no completed shutdown and no measurement drop-in.

The script stops the old timers, collects final evidence, stops the appliance,
preserves the old evidence and tools in a separate private directory, and
installs the measurement bundle. It copies the installed log4j2 configuration,
enabling DEBUG only for ETLPassDriver, and starts the appliance. Existing stores
and PV registrations remain intact. It does not open the replacement window.
It refuses to replace a schema-2 observation.

The archived current collector requires these active JFR settings. Fixture
installation alone does not provide that prerequisite. These scripts preserve
the separate installation and existing-observation extension operations; a
fresh-host installation must establish instrumentation before using the current
collector or opening its observation. `initialize-fresh.py` supplies that path
without a previous observation or synthetic terminal record.
The four-file extension interface is preserved for its historical sources.
Schema-5 tools require their complete bundle and journal retention evidence
through `prepare-retest.py`.

### Fresh Deployment Initialization

After fixture installation, registration and the approved deadband adjustment,
run `initialize-fresh.py instruments` as root from the installed tools directory.
It requires the approved source pins, synchronized time, an active appliance,
IOC and MariaDB, all 903 expected PVs connected and archiving, and inactive
observation timers. Existing instrumentation, observation or terminal records
prevent replacement. The original configuration and units are preserved.

The initializer installs bounded GC/JFR settings, ETL pass logging, the health
completion hook and actual sample/finish/abort timeouts of 240/2700/2700 seconds.
It restarts the appliance and checks four real 256M JVMs, their active JFR
recordings and their GC log files. Run its `check` action after the PV population
has reconnected to reverify source/configuration identity, units and instruments.
These actions do not create an observation or start the sample timer.

From `/usr/local/share/etl-soak`:

```bash
python3 initialize-fresh.py instruments
python3 initialize-fresh.py check
```

Complete the qualified journal measurements below and separate historical/current
capacity-growth measurements. Both proofs must match the actual deployment,
unchanged policy, duration and chain. The `measure` action runs seven actual
load-bound snapshots 300-320 seconds apart, captures real GC/JFR and two-worker
retrieval evidence, and records two separate capacity-growth windows. It keeps
the appliance and IOC active without starting an observation. It requires a new
private measurement directory and refuses missing recordings, incomplete
retrieval, changed tools/policy, excessive intervals and failed growth/budgets.

```bash
measurements=/var/lib/etl-soak-fresh-measurements
measure_args=(--measurements="$measurements" --duration-seconds=86400 --chain=shortened)
python3 initialize-fresh.py measure "${measure_args[@]}"
```

After successful measurement, run the prepare action with both real inputs:

```bash
retention="$measurements/retention/proof.json"
capacity="$measurements/capacity/input.json"
fresh_args=(--journal-retention-evidence="$retention" --capacity-evidence="$capacity")
fresh_args+=(--duration-seconds=86400 --chain=shortened)
python3 initialize-fresh.py prepare "${fresh_args[@]}"
```

Use `--chain=default` for a default deployment. Preparation preserves the actual
proof/source bytes and store data, and refuses missing/stale evidence,
insufficient capacity, a changed initialization or an existing preparation.
It creates the schema-5 preparation and initial collection boundaries from the
observed current time. Deployed-chain, health, full-sample and runtime verification
remain required through the existing shipped tools before any observation.

### Observation And Shutdown

`observe.py start` requires explicit duration/chain and a successful full sample less than 120 seconds old,
903 archiving PVs, real closed-pass records, synchronized time, all four JVMs
with actual heap/pause events, and six successful visibility probes. It writes
an immutable schema-5 `observation.json`, captures JVM PID/start identities and starts five-minute
sampling plus the finish timer. Select 86400 seconds for the full window;
`--duration-seconds 7200` selects the accepted retest. All 903 PVs must contain
actual archived timestamps inside the preceding 30-second query window.
An HTTP 200 response containing empty or older data does not establish freshness.
The initial sampler result is retained separately in `initial-sample.json`.
Normal finish requires the complete interval in both clocks. A 86400-second
result must cross UTC midnight. Both durations require the approved variant.

For the retest, `prepare-retest.py` archives an existing terminal observation
and its tools, preserving stores and registration. It installs the collector,
health completion hook and abort unit without opening a window.
`verify-runtime.py empty` substitutes only the clock boundary while querying
the real retrieval service and verifies that negative collection prevents start.
`verify-runtime.py abort` uses a separate evidence directory to exercise early
finish rejection, actual abort collection and shutdown, and repeated finish
rejection; it restarts the appliance only after successful verification.
Before a launch no finish timer exists, so the terminal path stops only the
observation timers that are loaded and records each timer's load state.
`verify-health.py` requires two distinct successful real health invocations and
full samples. Readiness binds these proofs to the installed tool hashes.
Preparation, chain/runtime verification and launch require explicit
`--duration-seconds` (7200 or 86400) and `--chain` (shortened or default).
`verify-chain.py` queries every shipped PV's actual `dataStores`, verifies
granularities/hold-two sources and binds its proof to fixture, boot, duration,
configuration and complete tool hashes. `launch-retest.py` repeats the chain
and health checks and stamps the capacity record, but it does not measure
growth: it refuses a current capacity window that ended more than 600 seconds
earlier. An omitted `--start-at` starts immediately after readiness; an
explicit timezone-aware target must be within 120 seconds. Runtime proofs
expire after one hour; the full sample must be under 120 seconds old, and
store/capacity verification under 600 seconds old.

`observe.py finish` runs after the manifest's full interval. It stops the sample
timer, waits at most 180 seconds for in-window passes, collects a final full
sample and bounded full JFR recordings, captures current ETL metrics, measures
the whole-unit stop and collects the remaining journal. `shutdown-started.json`
precedes the stop; `shutdown.json` records the outcome. The appliance timeout
is read from the actual unit (300 seconds in the retained deployments).
Health scheduling stops and active health work drains before the intentional
appliance stop; this coverage boundary is recorded. Preparation preserves old
units and sets a separate 45-minute bound on finish/abort services to cover
collection and shutdown deadlines. The IOC, data, VM and inventories are retained.

`observe.py abort` records Incomplete and cancels both timers. Two consecutive
failed full samples request abort; less than 2 GiB free requests immediate
abort. A single genuine health failure or full-sample error prevents Passed.
Journal collection preserves invocation IDs, accepted exit statuses, cursors
and completion events; missing or suppressed coverage prevents success.
The collector requires the latest completed health invocation to be successful
and no more than 120 seconds old. An invocation still running does not replace
that completion. Explicit preparation verification still requires the current
invocation to finish successfully. Final journal-only collection also requires
every started health invocation to have its completion record.
Final collection errors and skipped JFR captures remain visible in the terminal
record. An aborted observation cannot later receive a normal finish.

`evaluate.py` derives the half-open schedule independently of the manifest's
list. A 24-hour shortened window normally has 288/24 firings; default has 24/3.
It reconciles
metrics against the initial counters, checks five-second timing and ordering,
and evaluates health, freshness, JVM identity and GC coverage. Missing required
coverage is Incomplete; a completed window with a failed assertion is Failed.
Passed requires all assertions and the actual normal terminal path to succeed.
An observation recorded under any other schema is Incomplete with
`unsupported_observation_schema`; earlier-schema sources are not shipped.
Schema-2 inputs
can be numerically aggregated but cannot qualify under the current contract.

The automatic services continue after SSH disconnects. Do not reinstall,
register again or restart an appliance during its active observation.

## Measurements And Interpretation

The IOC feeds the engine, which writes STS. ETL pass records describe transfers
to MTS/LTS. Retrieval probes query the actual service using source timestamps.
The collector retains each failure instead of treating absent data as success.

| Evidence | Meaning |
| --- | --- |
| `observation.json`, `measurement-config.json` | Window boundaries, source fixture, process identities, measurement settings and tool hashes |
| `raw/*/journal.jsonl`, `passes.jsonl`, `metrics.csv` | Journal cursor continuity, completed ETL pass timing/counters and raw metric values |
| `gc-heap.csv` | Per-component heap occupancy before and after observed GC events |
| `gc-collections.csv`, `gc-pauses.csv` | Collection causes/durations and individual pause durations with PID, GC ID and timestamps |
| `jstat.csv`, `processes.csv` | Generation occupancy, young/full/concurrent collection counters and times, RSS, periodic heap and process identity |
| `raw/*/freshness.json` | All 903 PVs queried over the previous 30 seconds with two workers; response duration/status/size/hash and latest source timestamp |
| `raw/*/visibility.json` | Six representative source timestamps, retrieval attempts, matching archived timestamps and visibility bounds |
| `latency.csv`, `samples.csv`, `latest.json` | Per-sample measurement counts, failures and the latest collection state |
| `latest-full.json` | Latest full sample retained independently of journal-only collection |
| `health-invocations.csv`, `raw/*/health-journal.jsonl` | Health invocation completion evidence and cursor continuity |
| `journal-retention-proof.json`, `journal-retention-sources/` | Hash-bound measurement intervals, logging policy and preparation budgets |
| `raw/*/journal-{sequence,coverage,marker}.*`, query receipts | Bounded all-stream sequence evidence with system-only anchor and terminal marker |
| `raw/*/journal-sequence-accounting.json` | Journal file headers and the stored-entry count for the retained sequence range at each collection |
| `raw/*/journal-retention-{snapshot,budget}.json` | Actual journal inventory, effective caps, measured rates, collection gap and retained budget verdict |
| `health-verification.json`, `empty-data-verification.json`, `terminal-path-verification.json` | Executed preparation proofs bound to tool hashes |
| `jvm/`, `raw/*/*.jfr`, `final-gc/` | Rotating GC logs, JFR snapshots and final recordings |
| `shutdown.json`, final journal | Actual elapsed observation, whole-unit stop duration and service result |
| `abort.json`, `shutdown.json`, `fixture-adjustment.json` | Terminal result with embedded evaluation and retained assertion failures, and the accepted fixture variant |

JFR enables `GCHeapSummary`, `GarbageCollection`, `GCPhasePause` and `DataLoss`.
Each JVM's recording is bounded to 64 MiB and 26 hours, with a recording saved
on exit. GC logging uses a 16 MiB active file and three archives. Five-minute
collection takes ten-minute JFR snapshots limited to 8 MiB each, checks a
512 MiB snapshot archive limit and requires at least 2 GiB free before a dump.
A limit or JFR data-loss event is a collection failure.

Snapshots overlap. Before counting events or summing pause durations,
deduplicate by component, JVM identity, event type, GC ID and heap marker or
pause phase. Matching payloads may differ by at most two microseconds per
cluster, compared with integer nanoseconds. Exact timestamp equality alone is
insufficient. Distinct pauses remain separate; conflicts or unsupported
timestamp variation prevent complete coverage.
Filter by the observation manifest, check boundary coverage and retain
incomplete before/after pairs as incomplete. The maximum observed heap is a
maximum at recorded GC/sample times, not a continuous heap high-water mark.
No full GC is induced to obtain a measurement.
Periodic collection retains incremental GC logs across rotations. JFR summary
bounds, byte/digest integrity, full-export counts and DataLoss are checked.
jstat includes actual request/response times; young/full counters reconcile
with collections, and concurrent counters with remark/cleanup pauses.
`G1Old` includes concurrent mark and undo events and differs from jstat `CGC`.
Schema-5 kernel collection archives all journal entries between system-only
checkpoints, then extracts the kernel rows. Quiet intervals advance a root-owned
terminal marker without depending on the last kernel entry. Each interval
must return its system anchor and terminal marker; per-file sequence
identities remain recorded separately. `journalctl` before systemd 248 does
not return an entry whose boot, timestamp and content equal the entry before
it (corrected upstream by systemd commit `b17f651a17cd`, not present in
239-82.el8_10.19), so identical lines written in one burst leave unreturned
numbers in the shared sequence although the entries are stored. Each interval
records those numbers as `sequence_holes` instead of failing. Each interval
then reads every journal file header directly, twice a few milliseconds
apart until both reads agree, and requires one stored entry per sequence
number from the oldest retained system file through the newest entry
(`journal-sequence-accounting.json`); an unreturned number outside that range
fails the interval. A file that begins before the range is enumerated for the
entries it returns inside it. The evaluator recomputes the unreturned numbers,
the accounting and the budgets from the archived source rows, query receipts,
file headers and snapshots. A missing anchor or marker, a stored-entry count
that differs from the range, changed boot/daemon identity, failed queries or
suppression leave incomplete coverage. An empty memory-error search cannot
establish coverage. Actual rotation, loss, reboot and terminal integration
require the dedicated journal scenarios in the canonical plan.

A failed in-window journal budget is a finding about the journal settings, not
about the observed ETL. The sample records it as `journal_budget_failed` and
keeps the budget record, but it is not a sample error: it does not count toward
the two-failure abort and the evaluator does not list it among the failed
assertions; it reports the number of such samples as
`journal_budget_failed_samples`. Record loss, coverage gaps, suppression and
the stored-entry count still decide the ETL verdict.

Visibility probes read six representative scalar, fast, slow and waveform CA
timestamps with one-microsecond precision, then query matching archived samples
with one-second polling and a 30-second probe deadline. Preserve every attempt,
including timeouts. First-request success has a zero lower bound; its upper
bound includes the source sample's age. Freshness, request duration and these
visibility bounds are distinct measurements; none is exact engine ingestion
latency. The collector records kernel memory events and JVM identity changes;
application journals remain evidence for OOM and service-failure analysis.

For ETL timing, compare actual start with `plannedAt`. Without a preceding
transition wait, require a start within one 5-second tick. A pass held by the
ordering rule retains its original planned time and starts on the first tick
after the preceding transition ends. Preserve both delays. Exclude startup
passes from grid checks and shutdown-aborted passes from normal-load overruns.
The default MTS-to-LTS cadence is 00:10, 08:10 and 16:10 UTC; its hold of two
day partitions means a fresh 24-hour run does not establish new data in LTS.

## Frozen Current Bundle And Numerical Interface

After local verification, `contract.py --freeze` writes `bundle.json` with
exactly `BUNDLE_FILES`: preparation, runtime/aggregation dependencies, helpers,
JFR configuration and rate meanings. Schema 5 has 20 dependencies.
Missing/unexpected
entries or changed bytes invalidate readiness. Installed relative paths
must remain intact. Changed tools need
a verified new freeze and new runtime proofs. A locally frozen candidate
qualifies for dedicated testing; it becomes a replacement bundle only after
the required live scenarios pass.

### Journal Retention Preparation

Run this procedure as root only on an authorized deployment. The complete
candidate, original fixture CSV and existing adjustment evidence must be
available. Verify the effective logging policy and finite sample/finish/abort
timeouts before measuring; preparation or a policy change that alters them
requires new measurements. Keep the evidence directory private, outside the
observation directory that preparation archives.

With the approved 903 PVs actually connected and archiving, record seven
snapshots named `snapshot-000.json` through `snapshot-006.json`. Start each
snapshot 300-320 seconds after the preceding one, using its monotonic time.
Each snapshot retains actual PV status, twenty verified deadband fields,
boot/daemon identity, effective configuration, physical write counters and
system/user file inventories. A capped or unchanged directory total cannot
supply a zero write rate. The synchronized daemon write counter bounds the
system stream; each stream is also bounded by its allocated-file growth.
An interval with no counted writes is refused when a file's size, allocation
or identity changed or a file appeared or disappeared; a changed modification
time alone is not growth, because the inventory and counters are read at
different instants.

From the installed directory, set `index=000` for the first snapshot. At each
following five-minute boundary set it to 001, 002, 003, 004, 005 and 006, then
repeat the snapshot command. The directory must already exist with root-only
access.

```bash
bundle=/usr/local/share/etl-soak
evidence=/var/lib/etl-soak-retention
cd "$bundle"
index=000
python3 journal_retention.py snapshot --output="$evidence/snapshot-$index.json"
```

After all seven measurements, create the proof and check it again. Success
returns zero; a failed budget retains its calculation and returns nonzero.
Supply each applicable historical higher-rate measurement proof with
`--history-evidence`; its original source files must remain below the same
evidence root with coherent relative paths and digests.

```bash
python3 journal_retention.py prepare --measurements="$evidence" --output="$evidence/proof.json"
python3 journal_retention.py check --output="$evidence/proof.json"
```

The budget uses the largest measured rate under the unchanged policy, plus
retained user-journal bytes and two file-size allowances per stream. The
daemon's one `write_bytes` counter covers both streams, so it bounds the
system stream only; the user stream is bounded by its own allocation growth.
An interval shorter than 300 seconds, whether between the last measurement
and a preparation or check snapshot or between two collections, is checked
for continuity but is not a rate bound. Its
factor-two horizon covers the sample-gap limit plus the effective collection
or terminal timeout. With 320/240/2700-second limits the horizon is 6040 seconds.
Actual byte, retention-time and file-count caps must all permit that budget;
no command raises a cap. A current check must be within 120 seconds of launch.
The 320-second full-sample limit remains independently required.

Measure while the load is active, then complete its authorized terminal path
and preserve the terminal record before calling `prepare-retest.py`. Supply
`--journal-retention-evidence="$evidence/proof.json"` alongside the existing
bundle, capacity, duration and chain arguments. Preparation validates and
copies the original proof/source bytes before archiving the old observation;
it leaves stores intact. Runtime verification, launch and observer start
recheck the current caps and proof identity. Policy, boot, daemon or bundle
changes require new evidence.

Each collection and final capture preserves its actual snapshot, gap and
budget. A higher rate observed over at least 300 seconds increases the
retained bound; a shorter gap is still checked against its gap limit. Missing/failing
input remains a sample error; one error prevents Passed, two consecutive
failed full samples request abort, and the 2-GiB reserve rule still applies.
Live preparation and the T22-T28 scenarios establish integration behavior;
local arithmetic/parser checks alone do not authorize a new observation.

Capacity inputs are private schema-1 JSON with `duration_seconds`, the normalized
`configuration` and `windows`. Each window has `role` (`historical` or `current`),
`source_path` and `source_sha256`. Both roles and separate measured intervals
are required. Each source has `start`/`end` objects with `observed_at`, matching
`boot_id` and a `bytes` map covering `data`, `application_logs`, `journal`, `jfr`
and `measurement`. Current growth must match this boot and end within 600
seconds. Unsupported resets/rotations prevent preparation. The projection
uses the greater measured rate for each category over the selected duration,
plus 512 MiB. Preparation takes `--capacity-evidence` and
`--projected-growth-bytes` at least that value, retains source inputs and checks
85-percent usage and the 2-GiB reserve again before start.

From the installed tool directory, take snapshots across an actual collection
interval; `after.json` must follow `before.json`. Build both role sources before
preparation. Repeat readiness after the abort probe before launch.

Launch more than ten minutes after the last capacity measurement needs a new
current window first: take two snapshots about 300 seconds apart with real full
samples between them, build the current source with `--capacity-window`, store
it with its digest under `capacity-sources/`, rewrite `capacity-input.json`
with the unchanged historical window, recompute the projection and rewrite
`capacity.json` (keep the previous files), then launch within 600 seconds and
within one hour of the runtime proofs. No shipped command writes those two
files, so a launch after a fresh preparation uses a private step for it.

```bash
python3 contract.py --capacity-snapshot=before.json
python3 contract.py --capacity-snapshot=after.json
python3 contract.py --capacity-window before.json after.json --output=current.json
python3 verify-chain.py --duration-seconds=86400 --chain=shortened
python3 verify-runtime.py empty --duration-seconds=86400 --chain=shortened
python3 verify-runtime.py abort --duration-seconds=86400 --chain=shortened
python3 launch-retest.py --duration-seconds=86400 --chain=shortened
```

`aggregate.py` reads coherent manifest/terminal, raw samples/metrics, pass and
GC CSVs/logs, jstat, RSS and retrieval files. Relative paths stay inside the
input directory; historical absolute `raw/` paths are rebased. Its deterministic
schema-1 JSON includes source/tool digests, integer timestamps, counts, units,
statistics at six decimal places and failure/coverage fields. It reports busy
time, planned/ordering-adjusted delays, movement, partial-day weekly usage,
heap/post-GC range and change, GC counts/times, RSS, rates and retrieval bounds.
Startup/final-capture passes remain separate. Raw source timestamps independently
determine freshness. No private absolute path is required in the result.

`rate-semantics.json` pins the engine definitions: per-PV cumulative averages
since initial/latest connection or reset are summed. Benchmark writing rows
are excluded. Sampled means are arithmetic; overlapping intervals do not yield
a time-weighted rate or IOC scan rate. GC-event and sampled maxima do not
establish a continuous maximum or prescribe heap sizes.

Missing/malformed required inputs return nonzero with Incomplete and retained
failures. `--compare` checks parsed values regardless of key order and returns
nonzero on mismatch. A matching historical Incomplete replay still returns
nonzero. These commands run beside the Python modules:

```bash
python3 evaluate.py --input=/private/run
python3 aggregate.py --input=/private/run --output=/private/result.json
python3 aggregate.py --input=/private/run --output=/private/replay.json --compare=/private/result.json
```

The complete local suite also needs `ETL_SOAK_ARCHIVE_ROOT`, containing retained
`analysis-24h-{shortened,default}.tar` and actual `retest-fixture-adjustment.json`,
and `ETL_SOAK_EXTRACTED_ROOT`, containing coherent extracted per-chain inputs
with actual GC logs. Together with `ETL_SOAK_EVIDENCE`, these enable historical
replay, real numerical CLI comparisons, fixture preservation and missing-proof
preparation rejection. Set `ETL_SOAK_JOURNAL_SEQUENCE` to an actual retained
JSON journal file for the cursor parser checks. A filtered application-only
file exercises checkpoint rejection and unreturned-number counting; it cannot
prove all-stream coverage.
Set `ETL_SOAK_SEQUENCE_HOLE_EVIDENCE` to an actual sample directory whose
`journal-sequence.jsonl` and `system-journal-tail.jsonl` span unreturned
sequence numbers, and `ETL_SOAK_SEQUENCE_ACCOUNTING_EVIDENCE` to a directory of
actual `journal-sequence-accounting.json` records, at least one from a rotated
journal. Set `ETL_SOAK_JOURNAL_HEADER_EVIDENCE` to a directory holding one
actual archived journal file and `header-239.txt`, the `journalctl --header`
listing systemd 239 printed for it.
Set `ETL_SOAK_RETENTION_EVIDENCE` to a directory of actual retention snapshots
(`snapshot-*.json`) and the `proof.json` whose `latest` snapshot follows them;
the shared write-counter and short-interval regressions replay those inputs.
Set `ETL_SOAK_RUNTIME_RETENTION_EVIDENCE` to a directory holding two actual
consecutive collection snapshots (`first.json`, `second.json`) taken less than
300 seconds apart and the first collection's budget (`first-budget.json`).
Set `ETL_SOAK_MTIME_RETENTION_EVIDENCE` to a directory holding two actual
snapshots (`first.json`, `second.json`) between which no writes were counted
and only a journal file's modification time changed.
Set `ETL_SOAK_ROTATION_RETENTION_EVIDENCE` to a directory holding two actual
consecutive snapshots (`first.json`, `second.json`) taken before and after the
first rotation of the system journal, and the first collection's budget
(`first-budget.json`).
Set `ETL_SOAK_BUDGET_ABORT_EVIDENCE` to a retained actual observation directory
that the abort policy ended after in-window budget failures (`abort.json` with
its raw samples).
Set `ETL_SOAK_DU_RACE_EVIDENCE` to an actual JSON result (`returncode`, `stdout`,
`stderr`) of `du -sb` that exited 1 because files vanished while it walked a
directory; the store size measurement accepts exactly that case.
Only external HTTP, command, filesystem and clock boundaries are replaced.
Budget arithmetic is unit coverage. Historical collector transport checks and
schema-5 negative cases do not establish new journal integration or successful
schema-5 preparation. Those require the dedicated live environment.

```bash
python3 -B -m unittest discover -s tests/archiver-soak/etl-pass -p 'test_*.py'
```

## Baseline Tools

The baseline generator writes alongside its own source file. To reproduce the
fixture, copy both generators to a temporary directory, run `gen_soak.py` then
`gen_load.py`, and compare all seven generated databases/CSVs with `fixtures/`.
Do not regenerate into a running observation's input directory.

The baseline sampler records five-minute host, process, log, first-arrival,
retrieval and appliance metric CSVs. It has periodic heap samples and total GC
counters, without per-GC heap or pause events. `load_retrieval.py` accepts a
fixture CSV, evidence directory, duration in hours and optional client count
(default four). It streams one-hour responses, or one-day responses for eligible
1 Hz scalars, recording request duration/status/size/sample count. This load
client is separate from the two-worker probes in the ETL measurement.

`step2.sh` retains the original `/usr/local/share/aasoak9` and
`/var/tmp/aasoak9` paths, starts an additional IOC, waits 20 seconds and registers
its load list. The pilot sampler uses its own eleven-PV list and 900-second
interval. These historical launchers retain their original environment and
privilege assumptions; they are not part of the current ETL timer workflow.

## Evidence Retention And Verification

Run the local retest checks from the repository root:

```bash
python3 -B -m unittest discover -s tests/archiver-soak/etl-pass -p test_retest.py -v
```

Local checks exercise the shipped code with substitutes only at external
command, HTTP, filesystem and clock boundaries. They do not establish a real
two-hour observation or successful normal shutdown; those require retained
runtime evidence from the real appliance.

To verify the evaluator, set `ETL_SOAK_EVIDENCE` to a private captured evidence
directory containing `shutdown.json`, `state.json`, `passes.jsonl`,
`gc-heap.csv`, the manifest's baseline metrics and `raw/*/{sample,metrics}.json`
with each sample's `journal.jsonl`. Use a real completed passing observation.
The tests copy those inputs into a temporary directory and adjust filesystem
paths. Each negative case relabels the manifest to the current schema and then
changes one external evidence input; no evaluator
helper is replaced. Original evidence remains intact.

```bash
export ETL_SOAK_EVIDENCE=/absolute/private/evidence-directory
python3 -B -m unittest discover -s tests/archiver-soak/etl-pass -p test_evidence.py -v
```

Without that environment variable the evidence tests are skipped; skips
do not establish Passed/Failed/Incomplete verification. The retained input
predates schema 5, so each case relabels its manifest to the current schema and
the evaluator must not return Passed. Single sample, freshness and health
failures must appear as failed assertions, and missing final coverage must
retain existing failures. A Passed replay and the missing scheduled pass, GC
pair and aborted observation cases require completed schema-5 evidence and are
not covered.

Apply accepted collector revisions only after the current terminal record is
written and the appliance, sampler, finish, abort and health services are idle.
Stop-state verification precedes replacement. Preserve the original collector
and the completed manifest, measurement configuration and terminal record.
Record the revision separately; new installed hashes require fresh preparation
proofs before another observation.

Keep raw run evidence private and separate for each VM. Exclude
`archappl.conf.before-fixture` from exported evidence; configuration backups can
contain credentials. Sanitize journal/API content before including it in a
report. SSH addresses, private inventories and active-run timestamps stay in
the private handoff document.

Archive preservation uses byte comparison for unchanged baseline tools.
Current-tool verification uses syntax checks,
the shipped regression suites, retained real evidence and frozen digests.
Fixture regeneration uses the real generators and compares their output
against the shipped fixture. Source/configuration scans check for credentials.
Runtime verification
requires the real appliance, IOC, database and systemd paths; mocks or a
reconstructed substitute do not establish integration success. A timer being
configured does not establish a completed 24-hour observation or a successful
shutdown.
