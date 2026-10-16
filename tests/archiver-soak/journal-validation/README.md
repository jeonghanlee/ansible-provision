# Independent Journal Checks

The deliberate-loss entry point is `loss.py run`. Before removing its one
closed file, it waits for every independently scheduled action due before the
observed file-closure boundary to have an actual producer outcome and complete
direct source confirmation. It retains byte-for-byte producer/query-ledger
snapshots, the exact required IDs in the enumerated file and a hashed real file
copy outside live search roots. Frozen replay derives the same declaration
from those original snapshots and retains every lost ID in the required set.
Native complete-coverage refusal and actual partial capture stay separate;
remaining required records must be present exactly once with unchanged content.

The failure lifecycle entry point is `failure.py run`. It uses the unchanged
four real source schedules and direct reader, with real interval CLI services.
After an ordinary 300-second collection, the next collector service receives
ReadOnlyPaths for its output parent only. Its real filesystem error is retained
outside that parent. The driver detects the failure, records an outcome for
every cancelled future action, restores ordinary collection and stops the
declared appliance once. The original positive observation remains Failed or
Incomplete; `failure.py replay` independently decides the negative expectation.
`failure.py finish <directory>` refuses any second terminal operation without
writing to the original evidence or dispatching another stop.

## Scope

This package prepares and exercises the approximately one-hour basic journal
check and the independent 24-hour positive observation: actual input, direct
live visibility, later live reads, and exact collector identity/content
comparison. ETL processing acceptance is independent.

The lifecycle entry point additionally runs the dedicated 1200-second
quiet-kernel scenario: kernel input for five minutes, ten explicitly quiet
minutes, then five minutes of resumed input. Other producers and native
collection continue. Baselines, direct queries, native archives and frozen
replay use the same real paths as the positive observation. Any actual kernel
event inside the quiet interval leaves that scenario Incomplete.

`rotation-outside` records for 900 seconds with the ordinary four source
periods. Between seconds 360 and 480, after a successful native interval,
it executes one real `journalctl --rotate`. It retains the command outputs,
file identities and actual daemon/collection times. Replay requires preserved
closed-file identities, a new journal file, no overlapping collector interval,
and complete required-record comparison before and after the rotation.

File preservation requires the identities of populated journal files. An empty
file has no stored records; its removal or replacement does not establish
record loss. Required source records still require exact live/archive equality.

`rotation-during` records for 1200 seconds and observes up to three native
collector query opportunities. Its first ordinary collector wait begins at
t0, retaining the original pre-baseline collection boundary so no baseline
record is skipped. It records the real journalctl child process,
its parent and start identity, nonterminal process state and output progress
before and after the actual rotation command. The process arguments must match
the retained successful native query. No query is substituted, paused or
extended. Missing overlap evidence is Incomplete even if retention succeeds.

Concurrent observations also bracket real file-header reads with live query
and rotation-process snapshots. The same query identity must remain active
from the original file map through the observed populated-file rename and
new file identity, with actual output progress. Child-task lists narrow
discovery only; an omitted child is never evidence of absence, and process
snapshots and actual command arguments remain required. The frozen replay
recomputes this physical overlap from the raw observations and their hashes.

`obsolete-anchor` records for 1200 seconds after a real native checkpoint,
pre-window rotation and directly confirmed new-window anchor. Before the next
native interval it removes only the exact hashed closed checkpoint file,
after preserving its real bytes outside live search roots and confirming
that required baselines belong to the later window. Actual file identities
must prove that rotation replaced the active file. The candidate must be
stable and offline or archived, with no journald descriptor or mapping,
both before copying and immediately before removal. The original native
checkpoint is passed unchanged into collection; it is never cleared after
removal. The journal-owned `window_coverage.py` collector also receives the
independently confirmed boundary before every required baseline. It can exclude
an older checkpoint only when its actual time and sequence precede that boundary.
It records both the original input and the actual old-anchor query, then proves
every sequence identity in the required interval through real journal-file
enumeration. Every persistent file whose stored range intersects the required
interval is included; each cursor retains its actual file stream. Different
user-file streams are not excluded from sequence accounting. The immutable
baseline collector remains in the package. Subsequent
intervals retain their actual preceding checkpoints. The frozen replay repeats
the accounting from original file-enumeration queries and checks the declared
window against every required producer record. The full replay verifies every current required record against direct
and final live reads and proves none belonged to the removed file. Native
collector refusal or missing archive coverage remains Incomplete; lifecycle
metadata alone does not establish complete archive acceptance.

`restart.py` runs two separate 300-second recording segments around a real
dedicated-VM reboot. The first segment completes actual native collection and
directly confirms known records immediately before the declared generation
pause. The original checkpoint is retained as the post-reboot collector input.
The second segment accepts only declared retained boot files and records its
own UTC and monotonic clocks. Final live queries read both boots; replay compares
every required identity and payload and never subtracts monotonic values across
boots. The parent contract owns both segment paths and their frozen inputs.
Internal restart policies cannot be launched through the ordinary lifecycle CLI.
`restart.py check-boundary` rechecks actual retained producer outcomes and direct
query rows through the same source-correlation API. Its result covers only those
saved inputs; it does not establish reboot, duration or archive acceptance.
A refused native boot transition remains Incomplete until independently verified
coverage exists; two live segments alone do not establish complete archiving.
The journal-owned `boot_coverage.py` establishes a directly confirmed current-boot
boundary before any required baseline. Initial collection is permitted only for
a fresh before segment. A post-reboot collection retains the exact old checkpoint
input and requires the completed old segment, unchanged pre-reboot native tail,
actual normal reboot request, independent external boot observations, unchanged
hardware identity and a successful later live query of that old checkpoint.
Actual file enumeration proves each current-boot interval; subsequent intervals
retain the preceding real checkpoint. Frozen replay repeats these checks and the
parent compares every required old/new record and payload with both live queries
and the combined archive. The declared generation pause is outside the collected
live-segment scope and is never claimed as continuously covered.

**Out of scope:** actions not supported by the package entry points,
ETL verification, and production deployment management. A basic result does
not establish full-day preservation. Normal-stop/post-stop capture and replay
on an independent recipient are separate verification scopes; this package's
positive full-day observation does not claim either of them.

## Reuse And Evidence Boundary

Reusable source, configuration examples and procedures live in this directory.
Build a fresh package for each deployment and retain its manifest with that
observation. The build includes the retained-record health regression CLI;
its input is operator-provided actual evidence, not a generated replacement.

Keep deployment-specific configuration, host/VM identities, raw journal rows,
producer ledgers, command receipts and evidence archives in private runtime
storage. They are not source fixtures and must not be copied into this
directory or committed. The repository's ignored `work/` directory may hold
local operational records; reusable commands must not depend on its contents.

Use `check-local.py` for actual package build/install checks, `basic.py` for
the one-hour logging check and `long.py` for a new positive full-day observation.
Use the saved observation's own frozen replay CLI to recheck completed records;
replay does not start another 24-hour observation or operate services. Preserve
the original package and unsuccessful result when explicitly testing corrected
tools against a separate evidence copy. A new package manifest must never be
presented as the original observation's manifest.

## Package And Data Flow

`prepare.py build` reads the collector, registration client and five fixtures
from commit `649fee80561611f1494c1c3ce1f9546f6c619173`, rather than the evolving
ETL checkout. The package records each original path, revision and SHA256.
The extracted collector remains byte-identical, including its legacy
checkpoint tag. The package has no runtime import from the ETL directory.

The DEBUG configuration derives from the actual console configuration at
appliance source commit `162269e7db97f527626ba0b387933a8c47e8bb57` and enables
`org.epics.archiverappliance.retrieval.DataRetrievalServlet`. Its root remains
at the original configured level. The build manifest hashes every shipped
member; `verify` checks the exact required member set and contents.

The independent producer freezes its complete schedule before executing it.
Separate workers perform system, kernel, retrieval and health actions. A
one-second direct-query worker records raw journal results, command receipts
and UTC/monotonic query times. Another worker calls the unchanged collector
every 300 seconds and once after the final live query. Collector output is
never the source of expected producer IDs or first visibility evidence.
Direct reads include the cursor position and deduplicate identical overlap;
a cursor excluded by the source filters must not discard the first matching
record. The collector receives its UTC boundary in the native journalctl 239
timestamp format. Health completion retains the actual unit invocation, main
process and start/exit properties during `ExecStopPost`, before an inactive
unit can release those properties.
The terminal message must match that invocation's actual main PID and service;
the process name alone does not establish or reject the recorded source.
Retrieval workers allow outstanding responses without serializing the
one-second input schedule. The contract records worker counts, timeouts and
actual action times; exhausted workers produce explicit missed actions.

| Path | Scheduled actual action | Required journal evidence |
| --- | --- | --- |
| System | `logger` every second, unique payload | Exact payload, syslog transport, root source and independent action ID. |
| Kernel | Write to `/dev/kmsg` every 10 seconds | Exact payload with actual kernel transport. |
| Appliance | Real retrieval GET every second | Both DEBUG `pvName` and `requestTimesOb` messages, matching a distinct PV/time tuple, PID/thread, service, stdout transport and priority. |
| Health | Actual health script through its own systemd unit every minute | The real script's terminal result and the invocation's actual systemd exit information, with the same invocation identity. |

The 903-PV CSV and databases are copied without alteration. Their configured
periods are 783 at one second, 110 at 0.1 second and 10 at 10 seconds;
registration is 880 MONITOR and 23 SCAN. The eight arrays have configured
capacity 1000. These settings are not measured event counts or observed array
occupancy. No expected journal total is derived from PV frequency.

## Build And Stage

Use Python 3.9 or later. Both repositories must contain the pinned objects.
Run the commands from this directory; destination directories must be new.

```bash
repo=/absolute/path/to/ansible-provision
app=/absolute/path/to/epicsarchiverap-maven
pkg=/tmp/journal-package
python3 -B prepare.py build --repository "$repo" --appliance-source "$app" --destination "$pkg"
python3 -B prepare.py verify "$pkg"
```

`check-local.py` runs the actual build/install/verify/preflight/replay CLIs
against those source objects and fresh temporary filesystem roots. It checks
conflict and changed-file refusals without substituting internal functions.
It does not assert live journal delivery or appliance acceptance.

```bash
python3 -B check-local.py --repository "$repo" --appliance-source "$app"
```

Copy `config.example.json` to a deployment-specific file and replace the
example executable, artifact, account and Tomcat paths with actual values.
Endpoints must refer to the dedicated local appliance. `deployment_role`
explicitly identifies the journal deployment; it is an operator declaration,
not automatic proof of host ownership. Retain the actual appliance build
revision and artifact identity with the deployment evidence.

An offline installation can be inspected under a new staging root:

```bash
stage=$(mktemp -d /tmp/journal-stage.XXXXXX)
python3 -B prepare.py install "$pkg" --config /tmp/journal-config.json --root "$stage"
```

The installer writes `/opt/journal-validation`, private evidence/runtime
directories, three `journal-validation-*` units, and the dedicated appliance's
logging drop-in under that root. It starts no service and replaces no existing
installation, independent state directory, unit or logging drop-in. Conflicts
are checked before installation. Verify the staged paths and effective unit
configuration before applying them to the dedicated deployment.

## Dedicated Deployment

Runtime requires root, Python 3.9 or later, actual systemd 239, persistent
journal files of the current boot only, no volatile journal files, writable
`/dev/kmsg`, and the dedicated running appliance. These are the unchanged
collector's supported runtime conditions. Other journald versions are not
claimed compatible by this package.

Keep the actual journald configuration and versions with the run. Configure
the positive test to retain its required records. Capacity is sufficient by
premise; no size forecast, calculated retention budget or inherited 1-GiB cap
is a readiness condition. This installer does not change journald policy.

Install only on that dedicated host. Reload systemd there, start the private
fixture IOC, and start or restart that host's appliance with the logging
configuration. Its engine must discover the loopback fixture. The retrieval
JVM must inherit `LOG4J_CONFIGURATION_FILE=/opt/journal-validation/log4j2.xml`;
an explicit assignment in `archappl.conf` must agree with it. Preflight checks
the actual retrieval JVM's environment and service cgroup, not just a drop-in
file. Required messages must still be observed through the real stdout path.

Register the immutable CSV through the shipped registration client, then
inspect its actual response and missing count:

```bash
python3 -B /opt/journal-validation/register.py /opt/journal-validation/pvs-all.csv /tmp/journal-registration
```

The client's default management endpoint is the example loopback endpoint.
Supply its fourth positional argument when the dedicated management URL
differs. Preserve registration evidence with the deployment. Preflight reads
the actual registered PV list; it does not assert ETL processing correctness.

## Basic Execution And Replay

Use a new evidence directory for each preflight. The command fails unless
runtime prerequisites are actually met; it is not a delivery test.

```bash
python3 -B /opt/journal-validation/basic.py preflight --evidence /var/lib/journal-validation/readiness-001
systemctl start --no-block journal-validation-basic.service
```

`run-basic` defaults to 3600 scheduled seconds. A direct invocation with
`--seconds` below 3600 is an explicitly shorter probe; its
`one_hour_basic_acceptance` stays Incomplete. The basic CLI always keeps
full-day acceptance Pending. Planned/actual action times and actual stage durations remain in
the evidence rather than being replaced with the estimate.

Every run uses a fresh private `basic-<UUID>` directory and a runtime lock.
Busy, expired or interrupted schedule slots remain visible. HTTP error
responses, response timeouts and actual unhealthy health results can be valid
logging inputs when the dispatched action and all required real source
messages are confirmed. An attempted request without its complete actual
source-message set remains Incomplete. The HTTP outcome stays recorded
separately; missing messages and ambiguous correlation cannot produce Passed.

Health completion markers must match the exact saved receipt JSON, stdout
transport and health unit. When journal invocation metadata is present, it
must match the receipt; its absence is accepted only for that exact marker.
The actual health output still requires its recorded main PID and journal
invocation identity. Conflicting identities, changed receipt contents and
multiple distinct matching markers remain unacceptable. Disk-backed replay
selects both invocation-bound records and the exact marker without invocation
metadata, preserving every original journal field unchanged.

`check-health-records.py` checks both shipped matchers with actual unresolved
health evidence selected by `--evidence` and `--result`, using the tools named
by `--package`. It preserves the positive records and separately checks
explicit negative derivatives for missing markers, conflicting identities,
changed bodies, wrong process IDs and distinct duplicate markers. It does not
create a live observation or establish full-day acceptance.

The evidence and result paths select a completed actual observation and its
preserved unresolved source-set result. The package path selects the exact
original or explicitly corrected frozen tools to test. None of these inputs
is modified. The regression CLI reports each real-record case separately
from its negative derivatives and does not replace full-day comparison.

```bash
pkg=/absolute/path/to/frozen-journal-package
run=/absolute/path/to/retained-observation
result=/absolute/path/to/preserved-incomplete-result.json
python3 -B "$pkg/check-health-records.py" --package "$pkg" --evidence "$run" --result "$result"
```

Finalization waits for action completion and journal visibility, performs a
separate final live query, and requests final collection. It records errors
without stopping or restarting an appliance or ETL observation. An
interruption cannot turn a partial schedule into a completed basic result.
This is not the separate terminal/failure-termination scenario's acceptance.

The evidence retains producer schedules/outcomes, raw direct reads and
receipts, collector intervals/proofs, source/configuration identities, frozen
tools and fixtures, and an artifact hash index. Queries are private raw
evidence; sanitize any export before sharing it.

Run the saved replay tool against the run directory. Replay reads saved
evidence without writing or operating services:

```bash
run=/var/lib/journal-validation/basic-REPLACE_WITH_RUN_ID
python3 -B "$run/package/basic.py" replay "$run"
```

Replay compares required identities and full journal content. Intentional
direct-query overlap is deduplicated only when content is equal. Adjacent
collector intervals may share only their identical declared checkpoint;
other repeated identities fail the archive check. Initial confirmation time
is an observed bound, not the exact time of durable storage. The later read
reports the elapsed age since initial confirmation.

`result.json` separates delivery, later live visibility, collection and the
basic overall result. A confirmed violation is Failed; unresolved evidence
is Incomplete. Saved evidence changes refuse replay acceptance. Full-day
acceptance always remains Pending here. The seven canonical scenarios and
the independent 24-hour observation retain their own requirements.

## Positive Full-Day Observation

`long.py` uses the same real producers, source matcher, direct reader and
unchanged native collector. It freezes one baseline action per path, executes
those actual inputs and directly confirms every required message before t0.
The observation then follows a separately frozen schedule with the same
one-second system/retrieval, ten-second kernel and one-minute health periods.
No reference count comes from the collector or nominal PV frequency.

```bash
python3 -B /opt/journal-validation/long.py run --seconds 120
python3 -B /opt/journal-validation/long.py run --seconds 86400
```

The 120-second command is a long-path probe. Its full-day acceptance remains
Pending even when every probe comparison passes. The full-day command requires
at least 86400 elapsed seconds in UTC and monotonic time after t0 within the
same boot, with every baseline already directly confirmed. The observation
does not stop or restart an appliance. All runs share the basic runtime lock,
so the shared health producer cannot be used by concurrent journal runs.

The full-day intermediate live queries occur at six, twelve and eighteen
hours; the probe queries occur at forty and eighty seconds. Every checkpoint
requires all baselines and every scheduled action older than the declared
sixty-second visibility allowance. Actual query start/end, raw output and
command status are retained. Final live reading must find every baseline
and in-window required record with unchanged identity/content. Baseline ages
must reach the selected duration in both clocks; younger in-window record ages
are reported individually and are not labelled 24-hour-old records.

The final native collection must archive every required record exactly once,
apart from the one declared adjacent-checkpoint overlap. Delivery, later live
reading, baseline retention, intermediate reads, collection and overall
results remain separate. An executed action without its complete source set
is unresolved; skipped or failed required actions cannot disappear from the
result. Missing or changed confirmed identities prevent successful acceptance.

`long-<UUID>/` retains original producer schedules/outcomes, baseline confirmations,
query receipts, native collector proofs and the complete frozen package. Replay
uses a new private SQLite index under `/tmp` and streams original journal rows;
it never replaces a logging or collector path with a substitute. The original
evidence remains unchanged. `comparisons.jsonl` retains per-event identities,
initial confirmation, final ages and required checkpoints. Its digest must
reproduce exactly on replay.

```bash
run=/var/lib/journal-validation/long-REPLACE_WITH_RUN_ID
python3 -B "$run/package/long.py" replay "$run"
```

Only a completed 86400-second positive observation can receive Passed full-day
acceptance. Deliberate loss, rotation, quiet intervals, obsolete anchors,
restart and terminal/failure scenarios retain their separate canonical checks.
