# Archiver Soak Tools

## Scope

Preserve the tools, fixtures and measurement methods used for the archiver
functional/load soak and the parallel ETL scheduler observations. The source
files are copies of the executed tools; their fixed runtime paths and command
interfaces are preserved. This directory is suitable for Git tracking.

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
| `etl-pass/register.py` | Register a CSV fixture through the real mgmt API and retain the registration response status |
| `etl-pass/observe.py` | Open a 24-hour observation after readiness checks, or collect final evidence and measure whole-unit shutdown |
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
module name. Original working copies remain available for the active runs.

## Environment And Fixture

The ETL tools target Rocky Linux 8.10, systemd, Python 3.9 or later, OpenJDK 21,
and the EPICS 1.3.0 distribution with Base 7.0.10. The executed VM baseline is
2 vCPU, 4096 MiB allocated RAM and a 20 GiB disk, with MariaDB on the same VM.
The current collector uses the MariaDB Unix socket. Each of mgmt, engine, etl
and retrieval has a 256M minimum and maximum heap.

`common.yml` pins epicsarchiverap-env `d09dca7` and epicsarchiverap-maven
`3bdf378c`. Apply it with exactly one store configuration through the shipped
`archiver_dev` species, using a separately supplied private inventory.

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
backup, configures loopback CA discovery, installs the IOC and measurement
units, then restarts the appliance. It does not install JFR settings or register
PVs. Supply the three databases and `pvs-all.csv` under the installed tools
directory before calling it.

`register.py` accepts a fixture CSV, an evidence directory, an optional output
filename and an optional mgmt URL. It sends one `archivePV` JSON request.
Registration replies alone do not establish readiness: the collector must
observe all 903 expected PVs connected and archiving, no unexpected PVs,
synchronized time and healthy services.

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
collector or opening its observation.

### Observation And Shutdown

`observe.py start` requires a successful full sample less than 120 seconds old,
903 archiving PVs, real closed-pass records, synchronized time, all four JVMs
with actual heap/pause events, and six successful visibility probes. It writes
`observation.json`, captures JVM PID/start identities and starts five-minute
sampling plus the 24-hour finish timer.

`observe.py finish` runs after the manifest's full interval. It stops the sample
timer, collects a final full sample and bounded full JFR recordings, measures
the whole-unit stop and collects the remaining journal. `shutdown-started.json`
precedes the stop; `shutdown.json` records the outcome. The appliance timeout
is 300 seconds. The IOC, data, VM and inventories are retained.

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
| `jvm/`, `raw/*/*.jfr`, `final-gc/` | Rotating GC logs, JFR snapshots and final recordings |
| `shutdown.json`, final journal | Actual elapsed observation, whole-unit stop duration and service result |

JFR enables `GCHeapSummary`, `GarbageCollection`, `GCPhasePause` and `DataLoss`.
Each JVM's recording is bounded to 64 MiB and 26 hours, with a recording saved
on exit. GC logging uses a 16 MiB active file and three archives. Five-minute
collection takes ten-minute JFR snapshots limited to 8 MiB each, checks a
512 MiB snapshot archive limit and requires at least 2 GiB free before a dump.
A limit or JFR data-loss event is a collection failure.

Snapshots overlap. Before counting events or summing pause durations,
deduplicate by component, PID, event type, GC ID, event timestamp and `when`.
Filter by the observation manifest, check boundary coverage and retain
incomplete before/after pairs as incomplete. The maximum observed heap is a
maximum at recorded GC/sample times, not a continuous heap high-water mark.
No full GC is induced to obtain a measurement.

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

Keep raw run evidence private and separate for each VM. Exclude
`archappl.conf.before-fixture` from exported evidence; configuration backups can
contain credentials. Sanitize journal/API content before including it in a
report. SSH addresses, private inventories and active-run timestamps stay in
the private handoff document.

Preservation checks comprise byte comparison against the original tools,
Python/Bash/XML/YAML syntax, fixture regeneration with the real generators and
comparison against the shipped fixture, and a source/configuration credential
scan. These local checks establish archive fidelity. Runtime verification
requires the real appliance, IOC, database and systemd paths; mocks or a
reconstructed substitute do not establish integration success. A timer being
configured does not establish a completed 24-hour observation or a successful
shutdown.
