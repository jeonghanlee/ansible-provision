# Archiver Soak Tools

## Scope

Preserve the tools, fixtures and measurement methods used for the archiver
functional/load soak and the parallel ETL scheduler observations. The source
baseline files preserve the executed tools. The ETL collector and observation
tools provide independent initial functional checks and versioned 7200/86400-second
observations for both chains. Journal recording, retention and collection acceptance
belong to [journal-validation](journal-validation/README.md). This directory is suitable
for Git tracking.

Out of scope: VM inventories, SSH settings, credentials, application
configuration backups, measured CSVs, logs, JFR recordings and live run status.
Those belong in private evidence directories. The canonical plan and observed
verification results are in [the work register](../../docs/milestone-38560eb.md).

## Contents

| Path | Purpose |
| --- | --- |
| `etl-pass/collect.py` | Collect actual application-file pass events, diagnostics, metrics, process resources, stores, service state and GC/latency measurements |
| `etl-pass/measure.py`, `heap.jfc` | Capture GC heap/collection/pause events, complete jstat fields, retrieval freshness and representative visibility bounds |
| `etl-pass/resource_helpers.py` | Host, process and JVM helpers imported by the collector; preserves the baseline sampler source |
| `etl-pass/install-fixture.py` | Install the loopback IOC and systemd collection units on an empty appliance, without registering PVs |
| `etl-pass/initialize-fresh.py` | Initialize GC/JFR and finite measurement units on a fresh deployment; prepare ETL measurement metadata without a journal-study proof |
| `etl-pass/register.py` | Register a CSV fixture through the real mgmt API and retain the registration response status |
| `etl-pass/observe.py` | Open a default 24-hour or explicit 7200-second observation; preserve final evidence and measure shutdown or early abort |
| `etl-pass/prepare-retest.py`, `apply-fixture.py` | Preserve completed evidence, install measurement tools and verify the accepted existing deadband override before observation |
| `etl-pass/health-event.py`, `verify-health.py` | Retain actual health invocation results and verify the installed exit-status contract through real collection |
| `etl-pass/verify-runtime.py`, `launch-retest.py` | Verify real negative freshness and abort paths, then refresh readiness at a UTC launch target |
| `etl-pass/evaluate.py`, `test_retest.py` | Evaluate schedule, metrics, health and measurement coverage; exercise shipped code with external transport boundaries |
| `etl-pass/test_evidence.py` | Replay retained completed runtime evidence through the actual evaluator and verify failed or missing input handling |
| `etl-pass/contract.py`, `bundle.json`, `verify-chain.py` | Bind duration, actual stores, measured capacity and the complete frozen bundle |
| `etl-pass/aggregate.py`, `evidence.py`, `rate-semantics.json` | Portable numerical aggregation, bounded GC overlap handling and pinned metric meanings |
| `etl-pass/pass_source.py` | Capture actual per-component Log4j File events with producer PID/invocation, immutable file-prefix receipts and native completed-pass fields |
| `journal-validation/` | Independent journal installation, producer schedules, direct queries, native collection and frozen replay |
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
Eight waveform PVs have a configured capacity of 1000 elements; retain actual lengths.
Configured source processing is 775 general PVs and 8 arrays at 1 Hz, 110 fast PVs
at 10 Hz and 10 slow PVs at 0.1 Hz. Registration periods and actual archived-event
counts are separate measurements; nominal frequency times duration is not an observed count. The databases contain additional
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

### Independent Execution Phases

| Phase | Allocation | Required evidence |
| --- | --- | --- |
| Initial functional processing | About 3 hours | Original native-writer inputs, actual startup passes, physical store movement/transformation/retention/deletion and HTTP equality on both chains |
| Long observation | At least 24 hours per chain, in parallel | Subsequent regular continuity, repeated scheduling, fixed-interval physical equality and complete required measurements |
| Overall result decision | About 2 hours across both independent issues | Reconcile original evidence, missing data and separate ETL/journal verdicts |

The separate basic journal check has an approximately one-hour allocation. Its
completion is not an ETL installation, start, continuation or acceptance prerequisite.
The three-hour functional allocation is not a minimum observation duration or a promise
that the default regular repeat will fit inside it. The default subsequent regular
pass can require 28800 plus 600 seconds. Record actual setup, check, wait and capture
times separately; initial functional success does not establish regular continuity.

### Independent Application Evidence

The focused configuration preserves the original Console appender and adds a native
Log4j File appender under each component's `logs/etl-validation.jsonl`. Actual events
retain application time in milliseconds, the real JVM PID, the systemd invocation,
message and throwable. Native pass messages retain their own full planned/start/end
fields. No synthetic pass message or manual scheduler tick is used.

`pass_source.py` captures an actual file prefix with device/inode, byte offsets, a
SHA256 receipt and trailing-line accounting. Later capture rejects changed previous
bytes, truncation or changed identity. ETL events use explicit `appliance-file` source
metadata; the file positions are not journald cursors. When this configuration is active,
periodic pass capture reads the four application files. A journald read error alone
cannot remove pass evidence supplied by that path. Missing required independent fields
or files remain unresolved evidence. Health and kernel diagnostics retain their own
actual capture requirements and do not depend on the journal-study package or verdict.
The legacy raw filename `journal.jsonl` also carries these normalized application-file
events; `_TRANSPORT` and source path/offset/hash identify their real origin.

After a successful whole-unit stop, terminal collection reads the same application
files using the retained four JVM PIDs and the verified pre-stop invocation. An actual
terminal marker, inactive successful unit and unchanged boot are required. Device,
inode and previous-prefix checks still apply; a different new invocation, wrong PID,
missing identity or incomplete final record prevents complete capture.

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
application-file JSON or mismatched producer identity is rejected. For an interrupted empty-pass poll after a verified seed,
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

For the initial functional stage, use the explicit initial-only path on each chain:

```bash
python3 -B focused.py run --chain=shortened --initial-only
python3 -B focused.py run --chain=default --initial-only
```

`functional-initial-result.json` records the initial physical/HTTP verdict and hashes
its copied original evidence under `functional-initial/`. The overall focused
`result.json` remains Incomplete while regular-pass continuity is Pending. An initial
result is written only after the real comparisons and unchanged preparation/runtime/tool
checks. It neither starts a full-day observation nor claims exact value verification of
all 903 types: four scalar-double representatives cover raw and lastSample_10/30/60;
configuration and pass population cover all 903 PVs.

After separate execution authorization, `focused.py continue-initial --chain=<chain>`
uses the same fixed inputs, compiled helper, unchanged running identity and frozen tools.
It preserves the original initial result, requires subsequent regular passes and runs
the existing repeat physical/HTTP and final configuration checks. It adds no historical
input, restarts no appliance and does not start an observation. The default `run` without
`--initial-only` still includes regular repeats before complete focused acceptance.

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
tools except `focused.py` (excluded by name), `PBFixture.java` (the approved helper
literal) and the exact approved replacements listed by name and digest. Retained
combined proofs use their own original frozen tools; the independent candidate does not
extend their old approval lists. The same tool rule applies when `continuity` compares a Passed
original result with the installed bundle; `artifacts`, `pvs` and `flags` stay strict.
`continuity` records the recheck proof hash beside the original result hash and
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
It retains the independent application-file appender, restarts the appliance and checks four real 256M JVMs, their active JFR
recordings and their GC log files. Run its `check` action after the PV population
has reconnected to reverify source/configuration identity, units and instruments.
These actions do not create an observation or start the sample timer.

From `/usr/local/share/etl-soak`:

```bash
python3 initialize-fresh.py instruments
python3 initialize-fresh.py check
```

Actual free space below the existing 2 GiB runtime reserve refuses preparation.
Capacity forecasts, projected growth, journal retention evidence and journal-study
modules are not preparation or start conditions. Deployment and GC/latency findings
are retained independently.

The `measure` action captures actual GC/JFR and retrieval measurements
without opening an observation. Use a new private directory. The `prepare` action
requires an explicit duration and chain. Both actions preserve original source data and record real
times. They remain later observation preparation, separate from initial functionality.

```bash
measurements=/var/lib/etl-soak-fresh-measurements
python3 initialize-fresh.py measure --measurements="$measurements" --duration-seconds=86400 --chain=shortened
python3 initialize-fresh.py prepare --duration-seconds=86400 --chain=shortened
```

Use `--chain=default` for the default deployment. Preparation creates schema-6 ETL
metadata and actual collection boundaries. Deployed-chain, health, full-sample and
runtime verification remain separate evidence before any authorized observation.

### Observation And Shutdown

`observe.py start` requires explicit duration/chain and refuses only two
conditions: an existing `observation.json` (evidence is never replaced) and free
space below the 2 GiB reserve. Every other readiness check (a successful full
sample under 120 seconds old, 903 archiving PVs, closed-pass records,
synchronized time, four JVMs with heap/pause events, six visibility probes,
health, runtime, chain, focused continuity and JFR coverage) is run and a failure is recorded in the manifest's
`start_findings`; it never refuses the start, and the evaluator judges the
evidence. It writes an immutable schema-6 `observation.json`, captures JVM
PID/start identities and starts five-minute sampling plus the finish timer. Select 86400 seconds for the full window;
`--duration-seconds 7200` selects the accepted retest. The readiness sample
checks, and the start records, that all 903 PVs contain actual archived
timestamps inside the preceding 30-second query window.
An HTTP 200 response containing empty or older data does not establish freshness.
The initial sampler result is retained separately in `initial-sample.json`.
Normal finish requires the complete interval in both clocks. A 86400-second
result must cross UTC midnight. Both durations require the approved variant.

For the retest, `prepare-retest.py` archives an existing terminal observation
and its tools, preserving stores and registration. It installs the collector,
health completion hook and abort unit without opening a window.
`verify-runtime.py empty` substitutes only the clock boundary while querying
the real retrieval service and verifies detection/reporting without opening an observation.
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
configuration and complete tool hashes. `launch-retest.py` reruns the chain
and health checks, checks focused continuity, and takes a final full sample;
each failure is recorded in `launch-started.json` under `findings` and none
stops the launch. An omitted `--start-at` starts immediately after readiness;
an explicit timezone-aware target must be within 120 seconds. Runtime proofs
and the abort probe are optional evidence: their age and
presence are recorded at start, not required. `initialize-fresh.py prepare`
records deployment findings in `preparation.json`. `initialize-fresh.py measure` captures actual GC/JFR
and retrieval; it records failed measurements and interval/tool
findings without requiring journal-study snapshots or a retention budget.
An absent or
unreadable readiness metrics baseline is missing metric coverage in the overall
verdict, not an unreadable evaluation.

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
full samples that each fail an abort-listed check request abort; less than
2 GiB free requests immediate abort. The abort-listed checks are
`contract.ABORT_CHECKS`, recorded in the manifest's `abort_policy`: the
appliance down, required pass evidence unavailable from every configured ETL source,
the sampler itself unable to record,
the ETL or engine JVM replaced or missing (`abort_policy.jvms`; a management
or retrieval JVM is recorded only), and the fixture population not archiving.
These are the conditions under which continuing cannot produce scheduler
evidence or the load premise is gone. Any other failed check, including the
management interface, the clock, the tools, the fixture and the appliance
health command, is recorded in the sample and the observation continues. A
single genuine health failure or full-sample error still prevents an overall
Passed.
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
The result also carries `scheduler_verdict`, `scheduler_failed_assertions` and
`scheduler_missing_coverage`, computed only from the observation contract
(duration, UTC midnight, boot, chain, schedule, bundle, abort), the pass
records and their fields, timing and ordering, the appliance stop, the
sampler's own coverage and the verdict-deciding sample checks
(`contract.SCHEDULER_CHECKS`, a superset of the abort-listed ones: the
appliance and its management interface, the fixture population, JVM identity
of any component, the sampler, the clock, the tools, the fixture and the
appliance health command); a failed final collection enters it by the
recorded final sample's errors, not by name.
Metric, GC, latency, journal and health-journal findings stay in the overall
verdict and never decide the scheduler verdict; of the aggregated numerical
items only `terminal_manifest_mismatch` enters it. A pass that ends inside a
metrics request window is accepted under either counter reading;
`metric_window_ambiguities` counts such snapshot and transition pairs.
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
| `raw/*/journal.jsonl`, `passes.jsonl`, `metrics.csv` | Actual source-labelled application events, completed ETL pass timing/counters and raw metric values |
| `raw/*/*-application.jsonl`, receipt files | Native per-component file prefixes with PID/invocation, device/inode/offset, prefix continuity and SHA256 |
| `gc-heap.csv` | Per-component heap occupancy before and after observed GC events |
| `gc-collections.csv`, `gc-pauses.csv` | Collection causes/durations and individual pause durations with PID, GC ID and timestamps |
| `jstat.csv`, `processes.csv` | Generation occupancy, young/full/concurrent collection counters and times, RSS, periodic heap and process identity |
| `raw/*/freshness.json` | All 903 PVs queried over the previous 30 seconds with two workers; response duration/status/size/hash and latest source timestamp |
| `raw/*/visibility.json` | Six representative source timestamps, retrieval attempts, matching archived timestamps and visibility bounds |
| `latency.csv`, `samples.csv`, `latest.json` | Per-sample measurement counts, failures and the latest collection state |
| `latest-full.json` | Latest full sample retained independently of journal-only collection |
| `health-invocations.csv`, `raw/*/health-journal.jsonl` | Health invocation completion evidence and cursor continuity |
| `health-verification.json`, `empty-data-verification.json`, `terminal-path-verification.json` | Executed preparation proofs bound to tool hashes |
| `jvm/`, `raw/*/*.jfr`, `final-gc/` | Rotating GC logs, JFR snapshots and final recordings |
| `shutdown.json`, final journal | Actual elapsed observation, whole-unit stop duration and service result |
| `abort.json`, `shutdown.json`, `fixture-adjustment.json` | Terminal result with embedded evaluation and retained assertion failures, and the accepted fixture variant |

JFR enables `GCHeapSummary`, `GarbageCollection`, `GCPhasePause` and `DataLoss`.
Each JVM's recording is bounded to 64 MiB and 26 hours, with a recording saved
on exit. GC logging uses a 16 MiB active file and three archives. Five-minute
collection takes ten-minute JFR snapshots limited to 8 MiB each and requires
at least 2 GiB free before a dump; retained snapshots are never pruned or
capped. A JFR
data-loss event is a collection failure.

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
Kernel collection reads the unfiltered current-boot journal and retains each
actual query in `kernel-checkpoint-journal.jsonl`. Its initial checkpoint is
the latest retained journal record at or before the collection boundary.
Adjacent reads require the exact prior checkpoint, remove only that overlap
and advance through every transport, including intervals without kernel messages.
Only records with `_TRANSPORT=kernel` enter `kernel-journal.jsonl` and kernel
memory-event checks. Query errors, missing boundaries, suppression
and actual kernel memory events remain visible. These are ETL process diagnostics;
all-stream sequence accounting, journal-file headers, rotation, retention budgets
and deliberate-loss acceptance belong to the independent journal package.

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
JFR configuration, independent application-file capture and rate meanings. Schema 6
has 23 dependencies; journal-study modules are not members.
Missing/unexpected
entries or changed bytes invalidate readiness. Installed relative paths
must remain intact. Changed tools need
a verified new freeze and new runtime proofs. A locally frozen candidate
qualifies for dedicated testing; it becomes a replacement bundle only after
the required live scenarios pass.

### Numerical Replay

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
preparation rejection. Set `ETL_SOAK_DU_RACE_EVIDENCE` to an actual JSON result (`returncode`, `stdout`,
`stderr`) of `du -sb` that exited 1 because files vanished while it walked a
directory; the store size measurement accepts exactly that case.
Only external HTTP, command, filesystem and clock boundaries are replaced.
Local parser/arithmetic coverage does not establish installed ETL integration or
complete current-schema preparation. Those require actual dedicated execution.
Historical combined evidence uses its own preserved tools and schema.

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
pair and aborted observation cases require completed current-schema evidence and are
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
