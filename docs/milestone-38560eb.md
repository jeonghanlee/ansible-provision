# Work Register

## Scope

This document is the canonical work register for the `master` release line of
`ansible-provision` after the reset carried by prior state commit `38560eb`.
It records unfinished deliverables, external gates, accepted plans, and
verification needed to continue the current generation.

**Out of scope:** completed work remains reachable in the prior state commit;
detailed operating procedures remain in the linked runbooks; EtherCAT execution
remains in the owner's separate tracker.

The prior generation's Version 1.0 release convention — the joint
`iocrunner-gate-1.0.0` tag on `cloud-provision` (`2b77a97`) and
`ansible-provision` (`69158cc`), naming the gate environment that bakes and
runs the `epics-ioc-runner` consumer gate — was executed under the prior
generation and, together with its completed milestones, is retained at commit
`38560eb`.

The 1.3.0 EPICS-env gate ran its source-build OS matrix. Ubuntu 26 was
initially outside that matrix, but the C17 bridge shipped under 1.3.0
(`jeonghanlee/EPICS-env#29`) and its firing on the Ubuntu 26 source-build path
was confirmed (`jeonghanlee/EPICS-env#63`), so Ubuntu 26 now passes as well
(see `M2` and `D4`).

- Release line: master
- Milestone index: 38560eb
- Canonical path: `docs/milestone-38560eb.md`
- Canonical branch or ref: `master`
- Git upstream: `origin/master`
- Remote tracker: `jeonghanlee/ansible-provision`, GitHub milestone `Backlog`

Next session entry point: M37 shared-checker integration and preservation passed locally under #56/D34/D35 (T4). The duplicate local scripts are removed and privately preserved; historical T1-T3 results remain unchanged. Prepare its scoped source commit and checksum-only issue update when requested; obtain actual landing evidence before marking M37 Complete. M50 is active only for this component. All other tool work in #53-#56 remains Deferred and requires its own scoped start. M22/#30, M25/#31 and M24/#52 remain Complete/closed; M14 is Blocked on G2 and M26 on G5. No Milestone row is Ready.

Both original shortened/default 24-hour ETL processing observations completed on 2026-10-15 UTC and are accepted under D29. They ran for 86416.387 and 86415.088 monotonic seconds before normal finish across UTC midnight. The unchanged native scheduler evaluator Passed with all 312 and 27 required passes present exactly once. Read-only initial, both-transition and final physical/HTTP comparisons Passed on each chain. Whole-unit normal stops returned 0 in 12.516 and 13.770 seconds, below the installed 300-second timeout. Each observation retained 290 in-window full samples and its original frozen bundle.

Original terminal/aggregate verdicts remain Incomplete due to kernel cursor diagnostic refusal, JFR comparison including prior JVMs and evaluation before terminal persistence. Actual read-only native reevaluation and matching-PID reconciliation identified these defects without rewriting original records or tools. Historical kernel coverage remains unresolved because failed-query bytes were not retained. D30 confirms completed ETL functional verification; all additional tool cases, measurement/report and independent-recipient work belong to independent Deferred M29/M30 Backlogs. They do not gate ETL acceptance or require a repeat full-day run solely for tool correction.

Private evidence is work/etl-full-day-analysis-20261015/shortened-inspection-001.json and default-inspection-001.json, with exact native invocation and original/bundle hashes. Preserve the original stopped deployments and all evidence.

Separate control-host rechecks completed at 2026-10-14 06:01:37 UTC using copies of
the completed 2026-09-29/30 shortened/default records and their separately retained
GC logs. Actual retained-export checks, JFR/GC-log reconciliation, the retained
deletion-race result parser, the bundle dependency guard and repeated historical
aggregation checks Passed within their recorded scope. The historical aggregate
verdicts remain Incomplete, retaining their original health/retrieval findings and
missing current-contract evidence; the schema-2 inputs were not rewritten as current
observations. No running deployment was contacted or modified by this offline work.
Private `work/etl-offline-completed-20261013/latest.json` identifies the verified
report and exact copied inputs. This does not complete T1, T3, T8 or either current
24-hour observation; continue their remaining real-path checks separately.

M25's one-hour basic check, full-day recording/preservation/collection and eight additional lifecycle/negative expectations are accepted within their recorded scopes. Interrupted and unsuccessful originals remain unchanged. The original approximately one-hour journal, three-hour ETL, parallel independent 24-hour observations and approximately two-hour result-decision allocation remain documented; actual journal reconciliation exceeded that estimate. M27/M28 hold the two unexecuted tool checks independently. Journal acceptance does not start, stop or decide M22.

<details>
<summary>Historical entry notes before the independent plans</summary>

These notes retain their original observations and instructions for historical evidence.
They do not authorize a current run or override the current M22/M25 plans.

Previous entry point: Preserve the retained pair of cold guests, which was shut down
normally with its disks and files kept and nothing deleted, together with their original
failed-run evidence and all earlier M22 evidence. On 2026-10-10 the owner restarted the
preparation on two fresh guests, one per store chain; a retained guest is restarted only on
the owner's separate authorization.
On the retained pair the 2026-10-09 automatic executions ended Incomplete at an overly
strict initial chunk-key comparison. The correction, the separate recheck proofs, the
consumer acceptance path, the frozen bundle and the replacement step were accepted, and their
guest checks (T29 to T32) passed on that pair on 2026-10-10. On the fresh guests the species
deployment, the tool bundle and fixture installation, the registration of 903 connected PVs
and the ETL focused execution completed on both chains with Passed results, and an
independent decode of the real PB files confirmed the seeded transfers; both guests keep
running with the appliance and IOC active. The same decode found an engine sample-buffer
loss on 0.1-second PVs (a few samples per guest in about ten hours), outside ETL scope and
filed as epicsarchiverap-maven issue #29. On 2026-10-11 the owner authorized the
instrumentation, measured preparation and `prepare` steps on both fresh guests, chain by
chain with the shortened chain first. The first measured preparation on the shortened
guest was refused by a defect of the journal configuration check, corrected in a newly
frozen bundle (M25 T6) that the accepted replacement step delivered to both fresh guests
the same day; after it the instrumentation, measured preparation and `prepare` completed
on both chains (shortened at 08:01 UTC, default at 08:33 UTC), so both guests hold a
schema-5 preparation for the 86400-second window with the replaced tools. Later that day
the owner authorized the pre-launch checks (health, chain, empty and abort runtime
probes), the private capacity-window renewal and the launch of both 86400-second
observations, chain by chain with the shortened chain first. On the shortened guest every
pre-launch check passed and the launch was refused at the continuity's strict tool
comparison against the replaced bundle; the owner extended the approved-replacement rule
to that comparison in a newly frozen bundle, whose delivery invalidated the retention
proofs bound to the earlier tools, so both guests were measured and prepared again under
it. After the repeated pre-launch checks both 86400-second observations opened (shortened
2026-10-11T17:35:15 UTC, default 18:14:06 UTC) and both aborted themselves on 2026-10-12
(12:35:04 and 15:45:04 UTC) at a fixed JFR snapshot archive bound of the sampler, with
every pass planned before the abort recorded and no scheduler defect. The owner then ruled
that instrument failures must neither end an observation nor decide the scheduler
verification; the tool change (abort allowlist, scheduler verdict, bound removed, metrics
window tolerance, checkpoint retry; decision of 2026-10-12) was delivered as bundle
`eb93dfe4…`; its first relaunch stopped before launch when the shortened capacity
projection refused a store decrease, and the owner narrowed the abort list to the
evidence-stopping checks and accepted a store decrease as zero growth (decision of
2026-10-12, later the same day), refrozen as bundle `abd6c7b7…`. Its relaunch stopped at
the journal retention budget inside the abort probe; the owner ruled that no pre-start
check refuses the start except free space below 2 GiB (decision of 2026-10-13), and under
bundle `2ba4eaf4…` both 86400-second observations are open: shortened since
2026-10-13T00:10:06 UTC and default since 00:10:08 UTC, earliest finish 2026-10-14 at
00:10:06 and 00:10:08 UTC. Next: let both finish through their finish timers, then
evaluate each with the `2ba4eaf4…` evaluator (the installed copy or the delivery archive;
another evaluator reports `tool_bundle_changed`) through `evaluate.py --input` (overall and
scheduler verdicts) and record the results. Do not restart, reseed or re-register a guest during an active observation.
Earlier amendment and preparation evidence follows.
Local code implementation and verification were authorized on 2026-10-01.
Dedicated VM acquisition and deployment were subsequently authorized on
2026-10-01, with the owner selecting a 48-GiB disk. The actual Rocky 8.10
baseline was verified at 2026-10-02 04:31:25 UTC; archiver-dev installation
completed on the separate test VM. Actual source pins, four 256-MiB JVM
heaps and the 39-dependency candidate bundle are verified. Both current
journal tools now use systemctl --version. The corrected bundle was installed
only on the dedicated VM at 2026-10-02 05:01:14 UTC, preserving its previous
three files. Actual journal collection succeeds. At 2026-10-02 05:10:44 UTC,
journald was restarted on the dedicated VM and configuration application was
verified. Original fixture installation, registration and the approved override
succeeded; all 903 expected PVs were connected and archiving at 05:15:17 UTC.
The actual retention snapshot returned zero at 05:17:03 UTC. This is one raw
measurement, not a retention proof: the abort unit is absent and GC/JFR
instrumentation is not configured. The existing instrumentation/preparation
entry points require a prior observation. Fresh-VM initialization was subsequently
authorized on 2026-10-02. The actual initialize-fresh.py instruments command
succeeded at 07:28:37 UTC with four running JFR recordings, nonempty GC logs
and loaded 240/2700/2700-second sample/finish/abort services. All 40 candidate
dependencies verify; 59 local checks passed at 07:26:16 UTC with no skips.
Seven actual approved-load snapshots and GC/retrieval captures completed
between 07:35:39 and 08:05:40 UTC. The retention-budget calculation failed at
08:05:44 UTC, so measurements.json and preparation.json were not produced.
At 08:25:26 UTC the measurement service is failed with exit status 1; the
dependent preparation/chain/health checks did not execute. The six qualified
five-minute intervals require 1,291,544,426 bytes against a 1-GiB cap. The
additional 4.376-second final interval raises the required budget to
34,248,546,484 bytes. The 2026-10-02 diagnosis found that the one daemon
write counter was counted for both streams and that the short final interval
was taken as a rate bound; the owner chose to correct the accounting, leaving
the cap, logging policy and VM size unchanged. A launcher
wait timed out while the real oneshot service continued executing; this is
preserved separately and is not a failed observation. No observation exists.
On 2026-10-02 the earlier-schema sources were removed from the shipped tools.
The accounting-corrected 20-dependency candidate, bundle SHA256
e11d3ebc820f14d961bbefbf1dc1e514c2b304733fdf21ce1d8aa1f30871f98c, passed 58
local checks with no skips at 2026-10-03 06:12:06 UTC and replaces the
standalone candidate 567d629b. A second dedicated Rocky 8.10 VM, created by
cloud-provision on 2026-10-03 on the control host, carries this candidate: its
measured preparation passed at 07:33:25 UTC with 964,562,529 required bytes
against the 1-GiB cap, and fresh preparation succeeded at 07:35:14 UTC. The
first dedicated VM was last verified with the 40-dependency candidate
(5cd0f390) on 2026-10-02 and has not been contacted from the control host.
The second VM's first readiness health check failed on 2026-10-04 at 04:31
UTC because `runtime()` still took a 9.4-second gap between two collections
as a rate bound. The in-window correction, bundle SHA256
7c551c4b75382acf0ab94f091fb1710b3755563dfe11368387ff4da3d35a7158, passed 60
local checks with no skips; it needs a new measured preparation, which the
second VM cannot take because its preparation already exists. A third
dedicated VM with that bundle passed measured preparation (940,299,280
bytes), preparation, both health checks with a 5.2-second gap, the chain
check and the empty-data check on 2026-10-04, then failed the abort check
because the terminal path stopped a finish timer that exists only after a
launch. With that correction (bundle `bbbf5d90`) a fourth dedicated VM, for
the shortened chain, passed everything through the empty-data check, then
failed the abort check on a 0.293-second interval with no counted writes in
which only a journal file's modification time changed. That correction,
bundle SHA256
ad70a93adcf916e28c3b6641f6e5f5ae9850f6ed79714c8d4acca84018f2d5c6, passed 64
local checks with no skips. Moving the Maven pin to `254a6542` then gave
bundle SHA256
cc2024251224d89946a84f8936ab3b8dab8aadb20d5cc53e21fca3cd76378f4a, which
passed the same 64 checks. A fifth VM for the default chain was stopped
during measurement because its bundle was superseded.
Two new dedicated VMs with bundle `cc202425` then failed readiness on two
independent Rocky 8.10 defects. The shortened chain passed measured
preparation (777,867,682 bytes), preparation, health and chain checks, then
failed `kernel_journal` after the first closed pass on the journald loss
recorded in the results. The default chain left 95 of 903 PVs unconnected
because two engine CA contexts share one search port; that defect is
tracked in jeonghanlee/epicsarchiverap-maven#26.
The journald "loss" is a systemd 239 `journalctl` defect that hides stored
entries (results row "Rocky 8 journald cause"). Bundle SHA256
9c38425c77468ee0a9283c206ba5580bab5c410f98f9d558705fe5952608a43f records
unreturned sequence numbers instead of failing and accounts for them from the
journal file headers at every collection; it passed 69 local checks.
The Maven pin then moved to `aa953a44`, which carries the engine's CA
search-port correction; bundle SHA256
68d527a0a6e4173a1d7c02e7e9abef1659fb698466ba90cc7595ae53e729567b passed the
same 69 checks.
Two fresh VMs, one per chain, passed every readiness check with bundle
`68d527a0` and both 24-hour observations started on 2026-10-05 at 05:20Z
(results rows "Tenth and eleventh dedicated environments" and "Launch of both
24-hour observations"). Both aborted by the abort policy, shortened at 14:00Z
and default at 07:20Z, at the first rotation of the system journal, because
`rates()` took the renamed journal file as new growth (results row "First
24-hour observations, aborted at the first journal rotation"). The correction,
bundle `cb9b8106` (results row "T13 rotation accounting correction"), matches
files by device and inode and passed 71 local checks.
The default observation of the new pair started on 2026-10-05 at 17:18:34Z
with bundle `cb9b8106` (results row "Twelfth and thirteenth dedicated
environments"); its shortened observation was aborted after 14 minutes by a
store size check, which the bundle `3e9815b0` corrects (results row "T13 store
size measurement correction").
The journal checks formerly T22-T28 are the separate work unit `M25` since
2026-10-05; its first step is a compressed rehearsal (`M25` / T8) of the full
collection path, which this row's observations do not wait for. The two
observations running on 2026-10-05 were left as they are.
The replacement shortened observation started on 2026-10-05 at 18:24:54Z with
bundle `3e9815b0` (results row "Replacement shortened observation"). On
2026-10-06 that pair ended: the shortened observation was aborted by its
bundle at 04:15:29Z when the journal budget failed twice, and the default
observation was stopped on owner request at 05:28:57Z with 5 MB of budget
left (results row "Terminations of the earlier pair"); both evidence sets
are on the control host and both VMs are removed. The current pair runs
bundle `11ee9c8e`, which records a failed budget without aborting (`D23`):
shortened since 2026-10-06 01:36:33Z and default since 02:12:51Z, each for
24 hours across UTC midnight (results row "Fourteenth and fifteenth
dedicated environments"). The `M25` / T8 rehearsal with that bundle
finished on 2026-10-06 at 03:26:22Z; its evidence is on the control host
and its VM is no longer needed.
Next: let both finish. Each finish timer runs `observe.py finish` (README
section Observation And Shutdown); then read the verdict from `shutdown.json`,
collect the private evidence and record the results; T6/T20 comparison, T21
remain pending. The aborted VMs may be removed once the owner agrees. Launching
a further observation after a fresh preparation needs a new capacity growth
window first (README section Journal Retention Preparation), done with the
private steps `refresh-runtime-proofs.bash`, `fresh-capacity-refresh.py` and
`launch-after-capacity.bash`, or `run-and-launch.bash` for the whole
sequence, in `work/soak-etl-pass-3bdf378c/`. For `M25`, run its T8
rehearsal first; no upstream report is planned. Each VM's inventory,
known-hosts file and step logs are in its private
`work/soak-etl-pass-3bdf378c/journal-test-<label>/` directory;
the commands are in `tests/archiver-soak/README.md`: section Observation And
Shutdown for `verify-health.py` (two health completions and full samples) and
section Journal Retention Preparation for `verify-chain.py`,
`verify-runtime.py empty|abort` and `launch-retest.py`.
Live scenario results remain pending before actual
T22-T28 preparation/checks.
The two schema-4 trials that started on 2026-10-01 at 07:19:39 UTC have both
aborted with Incomplete verdicts: shortened ended at 18:25:26.991110 UTC and
default at 21:35:37.251269 UTC. The collector kept a pre-trial kernel cursor
during a quiet kernel interval; that cursor became unavailable while the
earliest retained system journal record still preceded the trial start.
Both trial VMs were later removed from the LAB host (reported 2026-10-04);
their manifests, raw samples and abort records went with them.
The scenario revision is accepted; candidate tools are installed on the
dedicated VM. Required live scenarios and replacement trials remain pending.
Before a new manifest, the revised checks must run through the shipped paths,
any tool change must produce a newly verified bundle, and both deployments
must repeat actual preparation and readiness. T6/T20 comparison and T21's
sanitized reproducible package remain required after successful full windows.
Previous schema-4 preparation passed on both VMs with the approved service-specific
journal interval 1us and burst 10000; prior 2010/11215/3741-message suppression
failures remain preserved. The deployed schema-4 bundle passed 46 local
checks and real runtime checks on both deployments. Shortened has a 40-GiB disk;
default's approved expansion to 48 GiB was verified before the new trial.
Keep the fixture, event-rate, existing-store-age and different disk conditions
explicit in comparisons. Original 24-hour observations remain Incomplete;
shortened's passing two-hour observation remains partial verification.
Preserved measurement/soak tools, fixtures and measurement methods are in
`tests/archiver-soak/`. Private inputs, collected evidence and the retained-run
continuation procedure are in `work/soak-etl-pass-3bdf378c/`.
The raw evidence remains on each VM under
`/var/lib/etl-soak/`; preserve it and the separate inventories. G4 is Complete.
M14 stays Blocked on G2 and M3 Deferred.
M20 closed on 2026-09-28 (`268a060`): the test-user
handoff document follows the operator model. M18 closed on 2026-09-28 (`0a3d4e4`, #28 closed):
the `archiver-dev-sqlite` species keeps the appliance configuration in SQLite.
M21 closed on 2026-09-28 (`8a5c355`): archiver hosts reach
MariaDB over its Unix socket. M17 closed on 2026-09-28 with the pins at epicsarchiverap-env
`d09dca7` and epicsarchiverap-maven `2fc12f01` (`940b63a`). Background follows. The schema load is fixed:
epicsarchiverap-env's `sql.fill` fix (G3, jeonghanlee/epicsarchiverap-env#47) is on `modernize` at `1fc20a8`, and M14/T17 passed on a Rocky 8.10 and a Debian 13
host rebuilt through this operator at that ref on 2026-09-23: the operator's
table check let the build continue and `make sql.show` lists `PVTypeInfo`,
`PVAliases`, `ArchivePVRequests` and `ExternalDataServers`. Both hosts were
removed afterwards. The pin is now at `9eed006`, which renders the store
granularity and hold of each tier from Make variables
(jeonghanlee/epicsarchiverap-env#50). M14/T20, the one-day functional soak, passed
on the soak host - a Rocky 8.10 archiver-dev VM provisioned for it and applied
through the full species at operator `dca2255` with the README test store values
on 2026-09-24, where T17 also passed at `9eed006`: all 100 PVs reached STS, MTS,
LTS and a second LTS day partition, and PV configuration survived an appliance
restart. M14/T21, the load test on the same host, passed on 2026-09-26: no
instance or mgmt outage up to 903 PVs and a 6 h retrieval load (42417 requests,
median 31 ms, all served), and no limit was reached before the run was ended
with the disk 91% full; each STS-to-MTS ETL pass took 0.4 s at 500 PVs and
0.7-1.0 s at 903 PVs (the steadily rising "last job" metric read at first as a
slowdown is a running sum); the two
end events showed a quiet IOC restart and a 5 MB, 10836-line etl burst for 10 min of an unwritable
MTS. All IOCs and the sampler are stopped; the appliance is left running with no
PVs connected. The soak writes
its 5-minute CSVs (host, per-process, per-log-stream, per-tier first arrival,
retrieval, appliance metrics) and the load clients write `retrieval-load.csv`,
all to
`/var/tmp/aasoak9/` on the soak host from tools installed under
`/usr/local/share/aasoak9/`; the tool sources are preserved under
`tests/archiver-soak/baseline/`. The run has ended: the IOCs, the sampler and the step timers
are stopped, and the day-1 and load-test CSVs and logs are copied to the local
working directory. The pilot host - the Rocky 8.10 archiver-dev host kept from T17's
original three at `6a026d4` - was removed on 2026-09-25 after its records were
kept. Separately, M15 (lab-VM clocks from the KVM PTP clock in `common`) is
Complete, delivered in `57d9d3f` and `eb9ba56`. M16 (the MariaDB application
password generated on the host, replacing the `raw_stdin` transport) is Complete,
delivered in `3e89e33`; M17 (the epicsarchiverap-env pin moved to the journald and
log4j2 service model) and M18 (SQLite through its own operator) follow it in that
order (D19), each with a draft plan. The rest of the M14 scope is untouched:
the distribution-based `archiver` species, for which
cloud-provision's `create_vm.bash` carries no selector - it has only the
archiver-dev pair; the Phoebus pair, a `phoebus`
operator consuming the published distribution and a `phoebus_build` source-build
alternative, with their species; and the `middleware` combination. Each also needs
the generator addition that the Generator gap note below tracks. Committed and
verified so far: the MariaDB loopback-TCP mode and the `[archiver_dev]` group_vars
(`5b5ee44`, `08dbb93`), the `archiver_build` operator with its playbook and the
`archiver_dev` species (`575b3f4`), and their proxy, sizing and health hardening
(`a9a24cd`). Later work on the branch is not enumerated here; `git log` on
`m14-middleware-reconcile` carries it.
Java installation, default commands, login `JAVA_HOME`, and re-apply
passed on Rocky 8.10 and Debian 13 VMs (M14/T3-T4). The existing EPICS distribution
operator now defaults to 1.3.0 and passed installation, example IOC build/runtime,
CA communication, binary dependency checks, and re-apply on both (M14/T5-T7).
Tomcat 9.0.121 is installed as shared `CATALINA_HOME`; temporary-instance
HTTP/startup/shutdown, re-apply, and integrity rejection passed on both
(M14/T8-T10). Path-overlap, permission, and file-list rejection preserve the
installed tree. The standalone MariaDB operator now supplies the UDS service,
`archappl` database and application account; client access, re-apply, password
rotation, service restart and preservation checks passed on both OS families
(M14/T11-T13). Anonymous accounts, remote root accounts and default test
database access are removed, with preservation and re-apply verified on both
(M14/T14). The account hash travels through SSH stdin; unsupported existing
authentication conditions fail before account changes (M14/T15-T16).
Application instances, schema and JDBC/client UDS configuration
remain epicsarchiverap-env responsibilities.
The full `archiver-dev` path follows epicsarchiverap-env and epicsarchiverap-maven readiness; M14 remains
Blocked on G2 for completion.

Milestone summary: `M16` (the MariaDB application password generated on the
host, replacing the `raw_stdin` transport; #26) is Complete, delivered in `3e89e33`; `M17` (the epicsarchiverap-env pin moved to the journald and log4j2 service model) and
`M18` (SQLite through its own operator) follow it in that order per `D19`, also
Not started with draft plans. `M15` (lab-VM clocks from the KVM PTP clock in the `common`
operator) is Complete: verified on fresh Rocky 8.10 and Debian 13 guests
2026-09-25 - PHC0 selected and synchronized, unchanged on re-apply and reboot,
the pools kept where the device is absent, and the Debian first `apt update`
retrying only on a signature-date failure; delivered in `57d9d3f` and `eb9ba56`
(jeonghanlee/cloud-provision#44). `M13` (RedHat python provisioning
for EPICS source builds) is Complete: rocky8 and rocky10 clean operator runs,
pyDevSup builds on both, full public gz matrix 6/6 (issue #25). `M14` (middleware
server provisioning) is Blocked on `G2` (cloud-provision ships the middleware
package baseline and the middleware VM). Every other milestone is Complete
except `M3` (Deferred per `D3`) and `M17`, `M18`
(Not started); the one open external gate is `G2`. `M12` (keep
`/run/cloud-init` at 0755 after the in-build cloud-init upgrade)
is Complete: verified on a rocky10 epics-dev guest 2026-09-09 - the `/etc`
tmpfiles override holds the directory at 0755 immediately and after a repeated
`systemd-tmpfiles --create`, restoring an unprivileged `cloud-init status`;
delivered in `75cc487` (issue #24). `M7` (harden the epics_build source build) is
Complete: verified on rocky8 2026-09-01 (T1) — the detached systemd unit survives
a dropped connection, a retry attaches without a second build, and a real source
build completes and is idempotent. `M6` (four
non-golden vacua) is Complete: both acquisition paths convergence-verified (distribution
on rocky10/ubuntu24, source build on all four); debian12/ubuntu26 distribution stays
blocked upstream (jeonghanlee/EPICS-env-distribution#4). `M4` (operator/species
provisioning model) is Complete: `M4/T1` (species syntax-check and enumeration)
and `M4/T3` (P_proxy apply and re-apply idempotency) were verified earlier, and
`M4/T2` (iocserver on the production IOC server) passed 2026-09-03 once the
internal git host became reachable over the site proxy's CONNECT tunnel (`G1`
Complete). `M3` (base_os/app role hardening) is Deferred per
`D3`: the old model is retired, so its Debian 13 re-verification is not pursued.
`M1` (4-OS source-build) and `M2` (Ubuntu 26 source-build) are both Complete;
the C17 bridge (`jeonghanlee/EPICS-env#29`) fires on Ubuntu 26 and its
source-build path was confirmed (`jeonghanlee/EPICS-env#63`). `M8` (restore the
chrony poll/key/leap directives dropped by the operator rewrite) is Complete:
verified on the production IOC server 2026-09-03, `/etc/chrony.conf` renders the five site
pools with `minpoll 4`/`maxpoll 4`, `keyfile`, and `leapsectz`. `M9` (share the
EPICS install root safely across group deployers) is Complete: verified on the
production IOC server 2026-09-03 — the root-owned shared root carries a default
ACL and a system-wide git `safe.directory`, and a group member's clone completes
with group-writable content. `M10` (route EPICS firewall ports to per-service
zones on a multi-homed IOC server) is Complete: verified on the production IOC
server 2026-09-03 — with the two zones set in the site override the second
apply is idempotent (`failed=0`), the CA zone carries exactly 5064 TCP+UDP and
5065 UDP, and the PVA zone carries 5075 TCP+UDP and 5076 UDP. `M11` (install
the requested version in the app and EPICS roles) is Complete: the install-once
guard is removed so a re-apply installs the requested version and
`epics_clone_mode` picks a minimal single-OS or a full multi-OS checkout;
verified on the production IOC server 2026-09-04 (con 1.1.0 replaced by 1.2.0,
full mode carries every OS tree, second apply `failed=0`). Delivered in
`fd4ff1c` and `13bc8e6`.

</details>

Status tally: 24 Complete, 0 In progress, 0 Not started, 0 Deferred, 2 Blocked. 5 external gates (3 Complete, 2 Open). Backlog excluded: 22 Deferred and 2 In progress carry-forward items; only the M37 checksum component is authorized.

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env 4-OS source-build environment | Carry-forward | Complete | No | | Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass both source-build layers and checks; [detail](#m1---epics-env-4-os-source-build-environment) |
| Core | M2 | Ubuntu 26 source-build | Carry-forward | Complete | No | D4 | Ubuntu 26 passes the complete source-build path (both layers, `gz` flavor, repeated-run checks) with the C17 bridge active; [detail](#m2---ubuntu-26-source-build) |
| Core | M3 | base_os/app role hardening from production deployment | Carry-forward | Complete | No | D3, D24 | Retired on 2026-10-06 (D24): the old roles it hardened are superseded by the operator model (D3) and its one open check is waived; [detail](#m3---base_osapp-role-hardening-from-production-deployment) |
| Core | M4 | Operator/species provisioning model | Milestone | Complete | No | G1 | Vacua, single-role operators, and species assemblies replace the staged model, iocserver registered; P_proxy verified (apply and full-species re-apply idempotency); `species/iocserver.yml` applies cleanly on the production IOC server (2026-09-03); [detail](#m4---operatorspecies-provisioning-model) |
| Core | M5 | Restore the EPICS OS package set into the operator model | Milestone | Complete | No | D5 | `epics_os_packages` installed by `roles/epics` and `roles/epics_build`, `pkg_automation.bash` retired; verified on the golden pair (rocky8, debian13) across both acquisition paths; four non-golden vacua moved to `M6`; [detail](#m5---restore-the-epics-os-package-set-into-the-operator-model) |
| Core | M6 | Convergence-verify EPICS OS build dependencies on the four non-golden vacua | Milestone | Complete | No | D6 | rocky10, debian12, ubuntu24, ubuntu26 convergence-verified by Live-mode apply on both paths — distribution (`iocrunner`, where the tree exists) and source build (`epics_dev`); the role-assurance step before golden promotion; [detail](#m6---convergence-verify-epics-os-build-dependencies-on-the-four-non-golden-vacua) |
| Core | M7 | Harden the epics_build source build against a dropped connection | Milestone | Complete | No | D7 | The `epics_build` raw build survives or cleanly resumes an SSH drop without leaving a half-built tree; [detail](#m7---harden-the-epics_build-source-build-against-a-dropped-connection) |
| Core | M8 | Restore chrony poll/key/leap directives dropped by the operator rewrite | Milestone | Complete | No | D8 | `roles/common` renders per-server `minpoll`/`maxpoll` and `keyfile`/`leapsectz` when set and omits them when empty; production render verified on the production IOC server 2026-09-03; [detail](#m8---restore-chrony-pollkeyleap-directives-dropped-by-the-operator-rewrite) |
| Core | M9 | Share the EPICS install root safely across group deployers | Milestone | Complete | No | D9 | `roles/epics` prepares a group-shared install root (`root:<group>` `2775`, default ACL, system-wide git `safe.directory`) so any group member can clone and write; verified on the production IOC server 2026-09-03; [detail](#m9---share-the-epics-install-root-safely-across-group-deployers) |
| Core | M10 | Route EPICS firewall ports to per-service zones on a multi-homed IOC server | Milestone | Complete | No | D10 | `roles/epics` opens the CA and PVA port sets each in a site-configurable firewalld zone (empty keeps the default zone), validates the zone exists, and carries the protocol-correct port set; verified on the production IOC server 2026-09-03 (second apply `failed=0`, PVA zone carries UDP 5075); [detail](#m10---route-epics-firewall-ports-to-per-service-zones-on-a-multi-homed-ioc-server) |
| Core | M11 | Install the requested version in the app and EPICS roles | Milestone | Complete | No | D11 | The con/procServ/conserver and EPICS roles drop the install-once guard and install the requested version on every apply (EPICS re-checks out the tag; `epics_clone_mode` picks minimal single-OS or full multi-OS); verified on the production IOC server 2026-09-04 (con 1.1.0 replaced by 1.2.0, full mode carries every OS tree, second apply `failed=0`); delivered in `fd4ff1c`/`13bc8e6`; [detail](#m11---install-the-requested-version-in-the-app-and-epics-roles) |
| Core | M12 | Keep /run/cloud-init world-readable after the in-build cloud-init upgrade | Milestone | Complete | No | D12 | After `roles/epics_build` runs on a rocky epics-dev guest, `/run/cloud-init` is 0755 and an unprivileged `cloud-init status --long` prints, both immediately and after a later `systemd-tmpfiles --create`; debian/ubuntu unaffected; [detail](#m12---keep-runcloud-init-world-readable-after-the-in-build-cloud-init-upgrade) |
| Core | M13 | Fix RedHat python provisioning for EPICS source builds | Milestone | Complete | No | D13, D14 | The RedHat python operator installs Python dev headers and makes `python3` resolve to the intended version, so `Python.h` is present and pyDevSup compiles on rocky8/rocky10; debian unaffected; [detail](#m13---fix-redhat-python-provisioning-for-epics-source-builds) |
| Core | M14 | Middleware server provisioning (Archiver Appliance, Phoebus) | Milestone | Blocked | No | G2, G3 | A middleware species provisions the EPICS Archiver Appliance and Phoebus, each independently selectable, on a middleware host layered on the common+epics base - system Java (distribution OpenJDK 21 with `JAVA_HOME`), Tomcat 9.0.121, MariaDB, the applications from their binary distribution repositories (species `archiver`, `phoebus`) or from source (`archiver-dev`, `phoebus-dev`), combinable as `middleware`, group `mid` / user `mid-srv` - with internal specifics supplied through the site override layer; blocked until the cloud-provision operator/species structure, package baseline, and middleware VM land (G2); [detail](#m14---middleware-server-provisioning-archiver-appliance-phoebus) |
| Core | M15 | Discipline lab-VM clocks from the KVM PTP clock in the common operator | Milestone | Complete | No | D17 | On a KVM guest the `common` operator loads `ptp_kvm`, links `/dev/ptp_kvm` through a udev rule gated on the KVM clock name, and adds a PHC refclock to the chrony configuration it writes, so `timedatectl` reports the clock synchronized with PHC0 selected; where no KVM PTP clock exists the configuration carries no refclock and the site pools serve as before; the first `apt update` on the Debian path retries on a signature-date failure; delivered in `57d9d3f` and `eb9ba56`; [detail](#m15---discipline-lab-vm-clocks-from-the-kvm-ptp-clock-in-the-common-operator) |
| Core | M16 | Generate the MariaDB application password on the host | Milestone | Complete | No | D18 | The `mariadb` operator creates the application password on the target host, keeps it in a root-only file, and sets the account from that file; `archiver_build` reads the same file for epicsarchiverap-env; no credential travels from the control host, `raw_stdin` and its tests are removed, and the operator works over SSH and over a local connection alike; delivered in `3e89e33`; [detail](#m16---generate-the-mariadb-application-password-on-the-host) |
| Core | M17 | Move the epicsarchiverap-env pin to the journald and log4j2 service model | Milestone | Complete | No | M16, D19 | `archiver_env_ref` and `archiver_maven_src_tag` move past epicsarchiverap-env `bbe0968` and epicsarchiverap-maven `67be91d7`, where the appliance runs its four Tomcats in the foreground under one journald service with a WAR log4j2 layout; the operator's install check, repair, stamp and documentation fit that unit, the host keeps a persistent, bounded journal, and a fresh `archiver_dev` build serves and persists PV configuration; delivered in `940b63a`; [detail](#m17---move-the-epicsarchiverap-env-pin-to-the-journald-and-log4j2-service-model) |
| Core | M18 | Select SQLite as the archiver configuration database through its own operator | Milestone | Complete | No | M17, D19 | A `sqlite` operator installs the SQLite CLI, an `archiver-dev-sqlite` species puts it in place of `mariadb`, and `archiver_build` passes `DB_BACKEND=sqlite` and checks the schema with `make sql.show`; fresh Rocky 8.10 and Debian 13 `archiver_dev_sqlite` hosts build with no MariaDB server and persist PV configuration across a restart; delivered in `0a3d4e4`; [detail](#m18---select-sqlite-as-the-archiver-configuration-database-through-its-own-operator) |
| Core | M19 | Add an ioc-group operator fixture account with linger | Milestone | Complete | No | | The `testusers` operator also creates `opc`, a member of the `ioc` group with systemd linger enabled, while `opa`, `opb`, `obs`, `usera` and `userb` keep their current membership and linger; a fresh iocrunner host applied through this repository shows that state and re-applies cleanly; delivered in `32ea95f`; [detail](#m19---add-an-ioc-group-operator-fixture-account-with-linger) |
| Core | M21 | Reach the archiver MariaDB over its Unix socket | Milestone | Complete | No | M17 | `archiver_build` writes `DB_SOCKET` for the `mariadb` backend and the `archiver_dev` group returns to `skip-networking`; fresh Rocky 8.10 and Debian 13 `archiver_dev` hosts build with TCP closed, serve mgmt and persist PV configuration, and an installed TCP host moves over in one forced run; delivered in `8a5c355`; [detail](#m21---reach-the-archiver-mariadb-over-its-unix-socket) |
| Core | M20 | Align the test-user handoff document with the operator model | Milestone | Complete | No | | `docs/test_users_handoff.md` names `roles/testusers`, `playbooks/operators/testusers.yml`, the `iocrunner` species order and the bake's species step instead of the retired `app_ioc_runner`, `roles/test_users`, `playbooks/07_test_users.yml`, `CONFIG_SITE` list and `site.yml`; delivered in `268a060`; [detail](#m20---align-the-test-user-handoff-document-with-the-operator-model) |
| Core | M22 | Verify the ETL pass scheduler on two parallel store chains | Milestone | Complete | No | M17, M21, G4, D27, D29, D30 | Actual ETL functionality and both full-day observations Passed; six criteria satisfied; #30 closed completed on 2026-10-15. M29/M30 tool work remains independent; [detail](#m22---verify-the-etl-pass-scheduler-on-two-parallel-store-chains) |
| Core | M23 | Add the Perl modules for the EPICS-env installed-tree utility to the EPICS OS package set | Milestone | Complete | No | D20 | `epics_os_packages` carries `perl-Digest-SHA`, `perl-JSON-PP`, `perl-Pod-Checker` and `perl-Test-Simple` on rocky8 and rocky10 and `perl` on debian12, debian13, ubuntu24 and ubuntu26; after the `epics` operator applies on each vacuum, the four modules load and `podchecker` runs; delivered in `4dfb290`, verified on all six vacua (`300ccc7`); [detail](#m23---add-the-perl-modules-for-the-epics-env-installed-tree-utility-to-the-epics-os-package-set) |
| Core | M24 | Split the archiver MariaDB operator into socket and TCP operators and rename the archiver-dev species | Milestone | Complete | No | D21 | Operators `mariadb_uds` and `mariadb_tcp` and species `archiver-dev-uds`, `archiver-dev-tcp` and `archiver-dev-sqlite` exist with the group variables `archiver_dev_uds.yml`, `archiver_dev_tcp.yml` and `archiver_dev_sqlite.yml`; each species deploys on a fresh guest with its database reachable exactly as the cloud-provision definition states; the old `archiver-dev` name still resolves for a limited period; delivered in `3b697e1`, with recorded T1/T2 Passed; #52 closed completed at 2026-10-16T06:42:05Z; [detail](#m24---split-the-archiver-mariadb-operator-into-socket-and-tcp-operators-and-rename-the-archiver-dev-species) |
| Core | M25 | Verify independent journal recording, retention and collection | Milestone | Complete | No | D27, D28 | Accepted 24-hour recording, live retention and exact archive comparison Passed with zero violations/unresolved records; #31 closed completed on 2026-10-15. Two unexecuted tool checks are independent M27/M28 Backlog work; [detail](#m25---verify-independent-journal-recording-retention-and-collection) |
| Core | M26 | Provision the SQLite Archiver Appliance on an existing general Rocky Linux 8.10 server | Milestone | Blocked | No | M18, G5, D26 | The `archiver_server_sqlite` assembly applies on the existing server without a proxy readiness gate, installs the appliance on the SQLite backend at the pinned sources, and passes the install checks on that server; the optional `proxy_check` role and its suite exist but are not part of the assembly; [detail](#m26---provision-the-sqlite-archiver-appliance-on-an-existing-general-rocky-linux-810-server) |
| Gate | G1 | the production IOC server reaches the internal git host | External gate | Complete | No | | Reachability achieved through the site HTTP proxy's CONNECT tunnel (an ssh `ProxyCommand` over the proxy), not a firewall whitelist: the owner's key authenticates and `git ls-remote` returns the refs; confirmed 2026-09-03 by the successful iocserver clone (M4/T2) |
| Gate | G2 | cloud-provision ships the middleware package baseline and the middleware VM | External gate | Open | No | | The middleware operator/species structure and OS package baseline (system OpenJDK 21, Tomcat 9.0.121, MariaDB; no Maven package) originate in cloud-provision (`docs/milestone-e260630.md` M11) as the normative source and a middleware VM is provisionable there, before ansible-provision mirrors the set and layers its roles; owned by the cloud-provision session |
| Gate | G3 | epicsarchiverap-env ships a `sql.fill` that loads the configuration schema when the database and application account are provisioned externally | External gate | Complete | No | | Complete when the jeonghanlee/epicsarchiverap-env#47 fix commit is on `modernize` and epicsarchiverap-env records #47's acceptance as met: with only the application account, `make sql.fill` loads the schema, `make sql.show` lists `PVTypeInfo`, `PVAliases`, `ArchivePVRequests` and `ExternalDataServers`, and an absent database exits non-zero. Observing it on an archiver-dev host is M14/T17, not this gate; owned by the epicsarchiverap-env session; met 2026-09-23: the fix is `1fc20a8` on `modernize`, and #47 closed with epicsarchiverap-env's acceptance recorded |
| Gate | G4 | Prepare two independent ETL soak environments | External gate | Complete | No | | Two fresh archiver-dev VM inventories are available; the owner selected the same existing 903-PV fixture for both chains, and initial disk and host capacity were assessed on 2026-09-28; [detail](#g4---prepare-two-independent-etl-soak-environments) |
| Gate | G5 | The server owner prepares the proxy settings and approves the installation on the existing server | External gate | Open | No | | The server owner has set the proxy configuration directly (environment, DNF, and the Maven settings file) and has approved the installation; [detail](#g5---the-server-owner-prepares-the-proxy-settings-and-approves-the-installation-on-the-existing-server) |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D1 | Local `T` labels identify verification inside their owning work detail and are not independent work IDs. | Prior canonical register, prior state commit `38560eb` |
| D2 | Ubuntu 26 is excluded from the current source-build matrix and deferred to EPICS-env 1.3.1 or a later version. The 1.3.0 gate matrix does not include Ubuntu 26, and the `iocStats` GCC 15 fix is owned by EPICS-env. | Owner decision, 2026-08-17 |
| D3 | The staged old model (`01_base`/`02_apps`/`03_epics`) and its retained roles `base_os` and `app_epics` are retired; the operator/species model supersedes them. Removing the old roles and playbooks is separate follow-up work. | Owner decision, 2026-08-29 |
| D4 | Ubuntu 26 source-build is no longer deferred. The C17 bridge shipped under milestone 1.3.0 (`jeonghanlee/EPICS-env#29`), and `jeonghanlee/EPICS-env#63` (closed 2026-08-24) confirmed it fires for `iocStats` on the Ubuntu 26 source-build path; the complete `gz` path passed on 2026-08-27. Supersedes `D2`. | Owner decision, 2026-08-30 |
| D5 | The EPICS OS package regression (`M5`) is fixed across all six vacua, `pkg_automation` is removed from `roles/epics_build` in the same change, ansible-provision drafts the cloud `docs/IMAGE_WORKFLOW.md` change for cloud-provision to land, and the milestone and GitHub issue are recorded before implementation begins. | Owner decision, 2026-08-31 |
| D6 | `M5` closes on the golden pair (rocky8, debian13), verified on both acquisition paths. The four non-golden vacua (rocky10, debian12, ubuntu24, ubuntu26) have no iocrunner golden pipeline; they carry the same package lists (names dry-run-verified) and move to `M6` for Live-mode verification. The cloud-side golden bake-matrix expansion stays a separate cloud-provision item. | Owner decision, 2026-08-31 |
| D7 | The `epics_build` source-build fragility surfaced during `M5` verification (cloud-provision Finding B) is hardened as `M7`, not accepted. `M5`'s fix removed the known trigger (the NetworkManager restart); `M7` addresses the underlying structure so a dropped connection cannot leave a half-built tree. | Owner decision, 2026-08-31 |
| D8 | The chrony per-server `minpoll`/`maxpoll` and `keyfile`/`leapsectz` directives dropped by the operator rewrite (`0012e2d`) are restored into `roles/common`, mirroring the `M5` EPICS-package regression from the same rewrite. Empty defaults keep the baseline render unchanged; site overrides (the production IOC server) render the production directives. | Owner decision, 2026-09-02 |
| D9 | With `epics_install_group` set, the EPICS install root stays `root:<group>` `2775` (setgid) and gains a default ACL on local disk plus a system-wide git `safe.directory` on the deploy server, so any group member can run git on the single shared repository and write into it. Owner-owned roots (one deployer only), per-user `safe.directory` (per-member setup), a per-member subdirectory layout (the ioc-runner per-engineer model, unsuited to a single distribution tree), and a dedicated deploy account were rejected for the one-server-deploys/many-hosts-read topology. Site prerequisites (consistent group GID, `root_squash` pinning deploy to the filesystem server, NFSv4 idmapping) stay in the site provisioning record. | Owner decision, 2026-09-02 |
| D11 | The con, procServ, and conserver roles and the EPICS role drop the install-once guard so a re-apply installs the requested version, replacing the installed one; whether the installed version matches the requested one is verified by the separate site verification tool, not by these roles. `con_version` is a git tag on the con repository, while `procserv_version` and `conserver_version` select a wrapper-repo ref whose upstream daemon version is pinned inside the wrapper (`configure/RELEASE` `SRC_TAG`), so the role controls the wrapper ref only. The EPICS distribution checkout adds `epics_clone_mode`: `minimal` (default) is a shallow, blob-filtered, single-OS sparse checkout for a Docker or single-OS host; `full` is a plain clone of every OS tree for a production NFS server. Both modes re-check out the requested tag in place, full disables sparse so a mode switch expands correctly, and an unknown mode value fails loudly. The roles keep `changed_when: false`. | Owner decision, 2026-09-04 |
| D10 | EPICS firewall ports are opened per service in site-configurable firewalld zones (`epics_ca_zone`, `epics_pva_zone`; empty keeps the default zone for single-homed hosts) because a multi-homed IOC server binds CA and PVA to different interfaces and zones, where the default zone carries no interface. The role validates that a named zone exists and fails loudly rather than silently skipping; it does not create zones (site infrastructure). The port sets follow the protocol constants — CA 5064 TCP+UDP and 5065 UDP, PVA 5075 TCP+UDP and 5076 UDP — dropping the previously opened 5065/TCP, which is not an EPICS port. | Owner decision, 2026-09-03 |
| D12 | The rocky-family in-place cloud-init upgrade run by `roles/epics_build`'s `dnf update` fires rpm's tmpfiles trigger, which resets `/run/cloud-init` to 0700 until the next boot and breaks an unprivileged `cloud-init status`. The fix lands in the role that causes it, not cloud-provision's cloud-init templates: cloud-provision recorded a Closed Door (2026-09-08, commit `47c1bb5`) because a template runcmd would move the proxy apply out of last position (proxy ADR D018). The role writes an `/etc/tmpfiles.d/cloud-init.conf` override (`d /run/cloud-init 0755 root root - -`) that shadows the vendor rule and applies it immediately with `systemd-tmpfiles --create`, chosen over a one-shot `chmod` because the override also survives a later `systemd-tmpfiles --create`. Rocky family only; debian ships no such rule. Mirrors the 2026-08-17 vmadmin-home 0700 precedent, fixed in ansible-provision. | Owner decision, 2026-09-09 |
| D13 | The RedHat-family python provisioning gap - no Python dev headers, so a pyDevSup C extension fails with `Python.h` missing on Rocky - is fixed in `roles/python` by mirroring the Debian `python3-dev`: add `python3-devel` to the default `pkg_python_redhat` (reaching rocky10 and any generic RedHat vacuum) and `python39-devel` to the rocky8 override (matching its 3.9 module). The milestone and GitHub issue (#25) are recorded before the code change; implementation status and live rocky verification (T2) are tracked in the M13 detail. | Owner decision, 2026-09-10 |
| D14 | The rocky8 python operator set only the unversioned `python` alternative, leaving `python3` at the system 3.6, so pyDevSup built against absent 3.6 headers. The operator now sets a `runtime_python_alts` list of name -> path pairs, applying each only when its alternatives group exists and failing loudly when a present group cannot be set (replacing the silent `\|\| true`). rocky8 sets `python3 -> /usr/bin/python3.9` (the versioned target pyDevSup reads) and `python -> /usr/bin/python3` (which then follows python3 to 3.9); setting `python -> python3.9` directly is avoided because the unversioned `python` group does not reliably register `python3.9`. The system python 3.6 is kept, not removed: RHEL8 platform-python depends on it, so the supported switch is alternatives. | Owner decision, 2026-09-11 |
| D15 | Middleware server provisioning (a middleware server, the middleware counterpart of the IOC dev host) is built in ansible-provision the same way the IOC species are: a new `java` operator role pins a non-system OpenJDK/Maven (dnf module stream + `alternatives`, with override keys `maven_module_version`/`pkg_java`/`java_alternatives_path` and a Maven settings template) and a middleware species layers it on `common`+`epics`, with Phoebus as the middleware application and a middleware group analogous to `ioc`. The internal lineage origin these repos derive from is a substance reference only (OpenJDK 21 + Maven 3.8, Phoebus); internal endpoints stay out of this public repository and are supplied through the site override layer. The cloud-provision package baseline and the middleware VM are the normative source and land first (G2). Sub-decisions left pending: increment scope (Java/Maven runtime first vs with Phoebus), the middleware group name and GID policy, the pinned Java default version, and the species name and target vacuum. | Owner decision, 2026-09-11 |
| D16 | Middleware server provisioning follows the cloud-provision middleware plan (`docs/milestone-e260630.md` M11, D2, D3): system Java (the distribution OpenJDK 21 with `JAVA_HOME` at the distribution path), no non-system pin and no Maven package (epicsarchiverap-maven supplies Maven 3.9.9 through its Maven Wrapper on the source-build path only), Tomcat 9.0.121 as the shared `CATALINA_HOME` and MariaDB (SQLite later) as the Archiver Appliance baseline, the Archiver Appliance and Phoebus installed from their binary distribution repositories (aa-distribution, phoebus-distribution) with source-build alternatives, and service group `mid` / user `mid-srv` parallel to `ioc` / `ioc-srv`. Supersedes the pinned non-system OpenJDK/Maven and Phoebus-build substance of `D15`; the ansible-provision-way build and the site override layer from `D15` stand. | Owner decision, 2026-09-12 |
| D17 | The lab-VM time-sync fix handed off by cloud-provision (jeonghanlee/cloud-provision#44: lab VMs never reach NTP sync because the public pools are unreachable behind the site proxy, and one Debian apply failed its first `apt update` on a signature date) is implemented in ansible-provision's `common` operator, the single writer of `chrony.conf`, not in cloud-init. | Owner decision, 2026-09-25 |
| D18 | The MariaDB application password is generated on the target host by the `mariadb` operator and kept in a root-only file there, read by `archiver_build` for epicsarchiverap-env, replacing the control-host `mariadb_password_hash` carried to the target through the `raw_stdin` action. Carrying the credential was the source of the plugin, its SSH-only constraint and its dedicated tests; a site that wants its own password places the file before the first apply. | Owner decision, 2026-09-25 |
| D19 | An archiver host gets exactly one configuration-database operator, `mariadb` (as today) or a new `sqlite`, chosen by species (`archiver-dev` or `archiver-dev-sqlite`, later `archiver` or `archiver-sqlite`) with the underscore group carrying `archiver_db_backend`; no new VM selector. Agreed with cloud-provision on 2026-09-25 (its `OPERATOR_MODEL.md` and generator follow this repository's role). The work runs in the order M16, M17, M18, because M16 and M18 both change the database handling in `archiver_build` and M18 needs an epicsarchiverap-env ref at or past `bbe0968`, which M17 brings. Owner decisions 2026-09-28 (M21 and M18 details): M21, the MariaDB socket, ran between M17 and M18, and for M18 cloud-provision landed its generator and definition first (`8c9b6ba`). | Owner decision, 2026-09-26 |
| D20 | The Perl modules EPICS-env's installed-tree utility uses (`JSON::PP`, `Digest::SHA`, `Test::More`, `Pod::Checker`) are added to `epics_os_packages`: `perl-Digest-SHA`, `perl-JSON-PP`, `perl-Pod-Checker` and `perl-Test-Simple` on rocky8 and rocky10, and `perl` on debian12, debian13, ubuntu24 and ubuntu26, whose `perl-base` alone does not carry them. Each Rocky module package is named even where another package already pulls it in, because the utility uses the modules directly. | Owner decision, 2026-10-02 |
| D21 | The archiver configuration database follows the cloud-provision definition (`docs/OPERATOR_MODEL.md` at `796682c`, its D8): three separate operators, `mariadb-uds` (the socket-only contract `mariadb` has today), `mariadb-tcp` (IPv4 loopback `127.0.0.1:3306` only, `skip-name-resolve`, the application account at `127.0.0.1`) and `sqlite`, and every archiver species carries exactly one: `archiver-dev-uds`, `archiver-dev-tcp` and `archiver-dev-sqlite`. `archiver-dev` and the group `archiver_dev` are renamed to the `-uds` names and stay as a deprecated alias for a limited period, removed after epicsarchiverap-env confirms it moved. Implementation starts after the two observations of M22 finish, because the soak tools and the next preparation resolve their deploy path through the current names. | Owner decision, 2026-10-05 |
| D22 | The journal checks of the ETL soak, T22-T28 of `M22`, are a separate work unit `M25` with its own completion criteria, tests and results, so that a journal check cannot decide the ETL scheduler verdict of `M22` and the reverse. `M22` keeps T1-T21 and opens an observation after T27's preparation portion passes; T22-T28 become `M25` T1-T7 and a compressed rehearsal of the full collection path is added as T8. The observations that were running on 2026-10-05 are left as they are. | Owner decision, 2026-10-05 |
| D23 | A check belongs to the work unit whose purpose it serves: a check whose failure makes the ETL conclusion of `M22` unreliable (record loss, coverage gaps, suppression, the stored-entry count, the kernel journal) stays in `M22`; a check of the journal settings or of the collection method (the retention budget) belongs to `M25`. A failed in-window journal budget is therefore recorded in the sample and reported by the evaluator as `journal_budget_failed_samples`, and it no longer counts toward the abort or the ETL verdict. | Owner decision, 2026-10-06 |
| D24 | `M3` is retired. The old roles `base_os` and `app_epics` it hardened were superseded by the operator/species model (`D3`), the surface it covered was re-verified through the operator roles, and its Debian 13 re-verification is waived because it targets roles that are no longer used. | Owner decision, 2026-10-06 |
| D25 | Proxy readiness of a general Rocky 8.10 server is verified read-only by the cloud-provision schema-3 checker, pinned by commit `05cf57398d09882f628d7356316f31576ca840c6` and source SHA-256 `dcf63cb79ecaf6a8dc9c955e5c1cec01cb69e3c92db21b9d0a3fa51f3ea36cff`, through a `proxy_check` role that precedes the group assembly and, for the general-server scope, `archiver_build`. The server owner prepares the six proxy files and the private input; `op.proxy` and the schema-2 runtime lock no longer gate this assembly. Superseded for the assembly wiring by `D26`. | Owner decision, 2026-10-10 |
| D26 | A general Rocky 8.10 server is provisioned without a proxy readiness gate: its owner sets the proxy configuration directly (environment, DNF, and the Maven settings file `/etc/maven-proxy-settings.xml`), the assembly neither writes nor checks it, and `archiver_build` keeps its precondition that a proxied host carries that file. The `proxy_check` role and its suite stay available and are wired in only when a site needs a gate. | Owner decision, 2026-10-11 |
| D27 | M22 and M25 have independent packages, preparation, execution, evidence and completion. M22 alone changes the existing ETL integration; M25 extracts its standalone journal workflow from the same immutable baseline. Neither requires the other's merge or result. Journal acceptance measures actual delivery, live retention and collection equality on sufficient disk, without an inherited cap or calculated retention horizon. All required in-window records receive final live reads, and actual retrieval messages must be correlated to requests. Supersedes the coupling and budget prerequisites of D22/D23 and the earlier plans; historical results retain their original meaning. | 2026-10-13 |
| D28 | Accept completed 24-hour journal recording, live retention and exact collection. Transfer unexecuted normal-stop/post-stop collector verification to M27 and independent-recipient full-day replay to M28 as separate Deferred Backlog work. Neither gates journal acceptance or requires a new full-day producer run. Preserve reusable procedures/source in Git-managed paths, keep operational evidence private, and record the reason/evidence in #31 before closure. | 2026-10-15 |
| D29 | Accept both completed shortened/default full-day ETL processing observations from retained actual scheduling, physical/HTTP and orderly-stop evidence. Preserve original Incomplete tool verdicts. Transfer kernel collector/ETL terminal isolation to M29 and JFR scope/terminal ordering correction to M30 as independent Deferred Backlog work. Neither gates the accepted ETL results or requires a repeat full-day run solely for tool correction. Other independence, fault/abort, measurement/report and recipient expectations remain unaccepted. | 2026-10-15 |
| D30 | ETL test completion concerns actual movement, transformation, policy retention/deletion, HTTP retrieval and full-day repeated processing only. Those declared functional expectations Passed on both chains. Transfer all remaining package/source-fault/collection/measurement/report/independent-recipient tool checks to existing M29/#34 and M30/#35 after ETL acceptance; they do not gate it. Conclude the already executed E4 case from unchanged retained evidence and preserve original unsuccessful tool statuses. | 2026-10-15 |
| D31 | Separate independent tool defects and unfinished verification/reporting into individually scoped Backlog work. M29/#34 and M30/#35 coordinate their respective child work; neither is one combined implementation. Preserve accepted ETL/journal results, actual shortened-case scope and original unsuccessful records. Corrected preparation failures and normal metrics overlap are not reopened as product defects. New corrective execution remains separately authorized. | 2026-10-15 |
| D32 | Organize tool follow-ups under four representative Journal, ETL, Buffer and Shared issues. Preserve all existing #32-#51 scopes, criteria, evidence and states; give each one primary group without removing cross-group references. Add the reviewed buffer replay/progress and Maven coverage findings to Buffer, and installation/source-preservation work to Shared. Accepted ETL/journal/buffer results remain independent. Future repairs, source import and runtime tests remain Deferred; this decision authorizes grouping preparation only. | 2026-10-16 |
| D33 | Consolidate GitHub tool tracking into four Journal, ETL, Buffer and Shared issues. Copy every original scope, acceptance criterion, verification method and evidence statement from #32-#51 before retiring those twenty issues with reason not planned and replacement links. Preserve unmet criteria directly in the replacements; source issue closure is not tool completion. Canonical component identities and unfinished verification remain independent and Deferred. Supersedes D32's plan to retain twenty open source issues. Actual GitHub mutation requires separate Issue delegation. | 2026-10-16 |
| D34 | Reactivate M37 checksum maintenance only within Shared #56. Refresh the existing parent source manifest for all current Git-managed sources, retain prior lists in Git, and add read-only membership/native checksum verification with real-copy negative checks. Exclude only the parent manifest itself from its digest list; retain both child manifests and frozen observation inputs unchanged. M50 reflects this active component only; all other components remain deferred and unauthorized. This tool work stays outside the release tally and does not reopen accepted product results. | 2026-10-16 |
| D35 | Remove the uncommitted archiver-specific checksum checker and regression suite in favor of the committed common test-framework checker with explicit project source and all three manifest declarations. Preserve their source and historical test receipts privately; update only current-source hashes, execution documentation and these component records. This accepts and authorizes the scoped deduplication, without other tool repairs, long observations or product-result changes. | 2026-10-18 |

### Assignment History

| Work Identity | From Canonical | To Canonical | Target Commit | Authority Moved At |
| --- | --- | --- | --- | --- |
| 38560eb / M20 | master, `docs/milestone-38560eb.md` `## Backlog` | master, `docs/milestone-38560eb.md` `## Milestone` | `268a060` | `268a060` |

### Milestone Details

#### M1 - EPICS-env 4-OS Source-Build Environment

- Origin: 38560eb / M1
- Identity History: new reset-generation identity; prior scope and evidence are reachable from commit `38560eb`. Ubuntu 26 was split out to `M2` (Deferred) by owner decision `D2` on 2026-08-17, narrowing this row to the four passing OSes.
- GitHub Issue: #7, https://github.com/jeonghanlee/ansible-provision/issues/7
- Status: Complete

##### Summary

Dedicated build hosts compile EPICS-env and EPICS-env-support from source,
install vendor libraries into the release tree, and validate the installed
runtime without changing `site.yml`.

##### Scope

Run the source-build layers on Rocky 8, Debian 13, Rocky 10, and Ubuntu 24,
including the `gz` flavor and repeated-run checks.

Out of scope: Ubuntu 26 (deferred to `M2`); binary-distribution deployment and
golden-image baking for these source-build hosts.

##### Completion Criteria

- Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass both source-build layers and checks.
- Vendor libraries have no retained absolute-path dependency findings.

##### Dependencies And Decisions

- No M or G dependencies.
- `D1` applies. `D2` splits Ubuntu 26 into `M2`.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: accepted plan preserved from prior state commit `38560eb`
- Implementation Authorization: prior owner-authorized implementation plan and verification evidence
- Superseded Plan Artifacts: none

1. Build the base and support layers on the supported source-build matrix.
2. Keep vendor libraries inside the release tree and run dependency checks.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Build and re-run the current EPICS-env path | Rocky 8 | Base and support layers pass; rerun is idempotent. |
| T2 | Integration | Build and re-run the current EPICS-env path | Debian 13 | Layered tree and dependency checks pass. |
| T3 | Integration | Build vendor libraries inside the release tree | Debian 13 | No absolute-path dependency findings remain. |
| T4 | Integration | Build the EPICS-env-support layer | Debian 13 | Support layer and checks pass. |
| T5 | Matrix | Build configured source-build hosts | Rocky 10 and Ubuntu 24 | Rocky 10 and Ubuntu 24 pass. |
| T6 | Integration | Build the `gz` flavor through both source-build roles | Rocky 10 and Ubuntu 24 | Installed flags and dependency checks pass. |
| T7 | Idempotency | Re-run the support role | Rocky 8 | Installed-tree skip is observed with `changed=0` and `failed=0`. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-28 | Rocky 8 | Passed | Fresh layers, `changed=0`, and `check_deps.bash` passed |
| T2 | 2026-07-28 | Debian 13 | Passed | Commits `fc030f8` and `829369e` |
| T3 | 2026-07-28 | Debian 13 | Passed | Commit `fc030f8`, absolute paths reduced from 9 to 0 |
| T4 | 2026-07-28 | Debian 13 | Passed | Commit `829369e` |
| T5 | 2026-07-28 | Rocky 10, Ubuntu 24 | Passed | Rocky 10 and Ubuntu 24 passed |
| T6 | 2026-07-28 | Rocky 10 and Ubuntu 24 | Passed | `-g0 -gz=zlib` and `check_deps.bash` passed |
| T7 | 2026-07-28 | Rocky 8 | Passed | `EPICS_ENV_SUPPORT_BUILD_SKIPPED`, `changed=0`, `failed=0` |

##### Closure Evidence

- The four in-scope OSes pass both source-build layers and their checks (observed 2026-07-28). Ubuntu 26 is split out to `M2` (Deferred) per `D2`; this row no longer depends on it.

##### GitHub Projection

- Title: `EPICS-env source-build verification matrix`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-16; GitHub updated 2026-08-16T08:33:22Z

#### M2 - Ubuntu 26 Source-Build

- Origin: 38560eb / M2
- Identity History: split from `M1` on 2026-08-17 by owner decision `D2`; carries the former Ubuntu 26 gate scope (prior generation `G2`). Returned to active and completed by owner decision `D4` on 2026-08-30.
- GitHub Issue: none dedicated. The Ubuntu 26 scope was originally carried in `#7`, which was reconciled to `M1`'s four-OS scope and closed. Upstream: `jeonghanlee/EPICS-env#29` (C17 bridge), `jeonghanlee/EPICS-env#63` (bridge firing confirmed on the Ubuntu 26 source-build path).
- Status: Complete

##### Summary

Ubuntu 26 source-build passes. GCC 15 defaults to C23, which broke the
`iocStats` `devIocStatsAnalog.c` `DEVSUPFUN`/`DSET` initializers; the EPICS-env
C17 bridge writes `USR_CFLAGS += -std=gnu17` into the module and restores the
build.

##### Scope

Build the complete Ubuntu 26 source-build path (both layers, `gz` flavor,
repeated-run checks) with the C17 bridge active.

Out of scope: the `iocStats` GCC 15 fix itself, which EPICS-env owns.

##### Completion Criteria

- The complete Ubuntu 26 source-build path (both layers, `gz` flavor,
  repeated-run checks) passes with the C17 bridge active.

##### Dependencies And Decisions

- `D2` deferred this row (2026-08-17); `D4` (2026-08-30) supersedes it and
  records completion. Ubuntu 26 did not require EPICS-env 1.3.1: the C17 bridge
  shipped under 1.3.0.
- Resolution mechanism owned by EPICS-env: the C17 bridge in
  `jeonghanlee/EPICS-env#29` (closed). `configure/RULES_MODS_CONFIG` adds
  `$(SRC_PATH_IOCSTATS)` to `MODS_C17_SRC_PATHS`, so `conf.modules.c17` writes
  `USR_CFLAGS += -std=gnu17` into the module's `CONFIG_SITE.local`; both the
  internal (`conf.modules`) and public (`conf.gz.modules`) paths depend on it.
  `jeonghanlee/EPICS-env#63` (closed 2026-08-24) confirmed the bridge fires for
  `iocStats` on the Ubuntu 26 source-build path.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: completed under owner decision `D4`
- Implementation Authorization: owner decision `D4`, 2026-08-30
- Superseded Plan Artifacts: none

1. Build the complete Ubuntu 26 source-build path with the C17 bridge active and
   confirm `iocStats/configure/CONFIG_SITE.local` carries `-std=gnu17`.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Matrix | Build the complete source-build path with the C17 bridge | Ubuntu 26 | Both layers, the `gz` flavor, and dependency/idempotency checks pass. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-27 | Ubuntu 26 | Passed | C17 bridge fires (`jeonghanlee/EPICS-env#63`, closed 2026-08-24, verified on the real build path); `iocStats/configure/CONFIG_SITE.local` carries `-std=gnu17`, `devIocStatsAnalog.c` compiles, and iocStats 4.0.1 installs under both `make build` and `make build.gz`. |

##### Closure Evidence

- Completed by owner decision `D4` (2026-08-30). Ubuntu 26 passes the complete
  source-build path with the C17 bridge active; the bridge shipped under 1.3.0
  (`jeonghanlee/EPICS-env#29`) and its firing was confirmed by
  `jeonghanlee/EPICS-env#63` (closed 2026-08-24). Ubuntu 26 did not require
  EPICS-env 1.3.1.

#### M3 - base_os/app role hardening from production deployment

Deferred 2026-08-29 per D3: the old model is retired, so the pending Debian 13
re-verification of the old roles is not pursued. The base and app surface is
re-verified under the operator model (M4) through the `common`, `con`,
`conserver`, and `procserv` operator roles. The completed Rocky 8 evidence on
the production IOC server (T1) remains valid as historical record.

##### Scope

Role fixes and enhancements surfaced while provisioning a real IOC server
(the production IOC server) rather than the testbed. Delivered on `master`:

- `base_os` OS-family detection reads `/etc/os-release` and branches on exit
  code, not raw stdout, which arrived empty on the first become task over a
  local connection (`c900b5e`).
- chrony.conf directives became site-overridable variables; a `trim_blocks`
  newline drop that joined the pool lines and broke `chronyd` restart was fixed
  with a `+%}` control (`dc1bfea`, `0b8ec0a`).
- Rocky `python` default set to 3.9 via an `alternatives --install` of the
  unversioned-python master link before `--set` (`6ba1278`, Rocky-only).
- con/procServ/conserver gained branch/tag/commit version pinning (`0996270`).
- `app_epics` clones the distribution as the IOC owner, sparse and tag-pinned,
  into a group-writable install root, so a host with no root ssh key can pull
  from an internal remote (`7c55229`).

**Out of scope:** the production IOC server deployment record and its site-specific
overrides live in the `server-configuration` repository, not here.

##### Verification Results

| Check | Result | OS | Evidence |
| --- | --- | --- | --- |
| T1 | Verified | Rocky 8 | the production IOC server: `01_base`/`02_apps` completed, chrony synced (`^*`, Reach 377), `python --version` 3.9.25 from a clean 3.6.8 state, con/procServ/console/conserver installed. |
| T2 | Not run | Debian 13 | os-detect, chrony render, version pinning, and epics owner-clone touch the shared/Debian path but were exercised only through `--syntax-check`; a Debian 13 run is pending. |

##### Closure Evidence

- Retired by `D24` on 2026-10-06. Complete here means retirement, not delivery
  of the pending check: T2 (Debian 13 re-verification of the old roles) is
  waived. T1 (Rocky 8 on the production IOC server) remains the verified
  record, and the base and app surface is covered by the operator roles
  re-verified under `M4` and later.
- The two old role directories `roles/app_epics` and `roles/base_os` were
  removed from the repository by the operator rewrite; on 2026-10-06 neither
  `origin/master` nor the working branch carried a tracked file under them
  and the hosting service returned no content for either path. Only an empty
  `templates` directory under each remained in one working copy, and it was
  removed with this retirement.

#### M4 - Operator/species provisioning model

Origin: 38560eb / M4

##### Scope

The staged 01_base/02_apps/03_epics model is replaced by the operator/species
model whose normative definition is cloud-provision `docs/OPERATOR_MODEL.md`
(origin/master `de8e03f`). ansible-provision implements it:

- Vacua: six OS baselines (debian12, debian13, rocky8, rocky10, ubuntu24,
  ubuntu26) as inventory groups under the `vacua` parent.
- Single-role operators under `playbooks/operators/` (common, provenance,
  python, epics, epics_build, epics_support, con, conserver, procserv,
  iocrunner, testusers, rt, nfs_sim, ethercat), each importing one role.
- Species assemblies under `playbooks/species/` (bare, iocrunner, iocrunner_nfs,
  iocserver, epics_dev, nfs_sim, rtbase, ethercat) that import operators in
  operator-model product order, enumerated in `configure/RELEASE` and
  `inventory/lab.ini`.
- iocserver: iocrunner without P_testusers, for an existing production IOC
  server (the production IOC server) that already owns its accounts; added and registered in
  `6fbbf71`, `79fba36`, and `5b0ac04`, matched char-for-char to the SOT
  iocserver product at `bb64ad2`.

Implemented and verified:

- P_proxy: an optional precondition operator that applies the site proxy
  contract to an existing server by streaming cloud-provision
  `bin/proxy_contract.bash` in apply mode, so the logic is not duplicated.
  Design converged with the cloud-provision owner (ADR-20260820); `roles/proxy`
  and `playbooks/operators/proxy.yml` are implemented (stage the shipped script
  plus a schema-1 input, then run apply as root). Apply was verified on 2026-08-31
  through proxied Debian 13 and Rocky 8 golden-image bakes, and a second full-species
  apply on the same VMs confirmed idempotency (`changed=0`, installed tree identical).

**Out of scope:** the operator-model definition itself (owned by
cloud-provision); the production IOC server site record and overrides (the
`server-configuration` repository); EtherCAT live execution (owner's separate
tracker).

##### Completion Criteria

Every named species assembly resolves and applies in operator-model order,
iocserver applies cleanly on the production IOC server, and P_proxy is either built and applied
or explicitly deferred by owner decision.

##### Dependencies And Decisions

- `G1` (internal-git reachability) is Complete: the site HTTP proxy's CONNECT
  tunnel carries ssh to the internal git host, so the live iocserver run (`T2`)
  ran and passed.
- P_proxy depends on cloud-provision shipping `bin/proxy_contract.bash` as the
  single authority; the SOT P_proxy precondition lands together with the
  `roles/proxy` implementation.

Plan Status: accepted
Plan Acceptance: owner decision `D3` (2026-08-29) established the operator/species model
Implementation Authorization: owner-directed; T1–T3 implemented and verified
Superseded Plan Artifacts: none

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Structure | Syntax-check every species playbook and confirm each is listed in `configure/RELEASE` and `inventory/lab.ini` | control host | Each species assembly resolves its operator imports; RELEASE and the inventory groups enumerate every species. |
| T2 | Integration | Apply `species/iocserver.yml` on the production IOC server | Rocky 8 (the production IOC server) | The iocrunner operator set installs on the existing server with no test-user creation. |
| T3 | Integration | Build `roles/proxy` and apply `operators/proxy.yml` on a proxied host | Debian / Rocky | The shipped `proxy_contract.bash` applies the proxy artifacts and a re-run is idempotent. |

##### Verification Results

| Check | Result | OS | Evidence |
| --- | --- | --- | --- |
| T1 | Passed | control host; debian12 (epics_dev) | All eight species playbooks (`bare`, `epics_dev`, `ethercat`, `iocrunner`, `iocrunner_nfs`, `iocserver`, `nfs_sim`, `rtbase`) pass `ansible-playbook --syntax-check`, and every species is enumerated in `configure/RELEASE` `SPECIES_PLAYBOOKS` with its `inventory/lab.ini` group present for every non-bare species (bare is vacuum-only by design); no stray non-vacuum groups. Registration landed in `6fbbf71`, `79fba36`, `5b0ac04`. Live evidence: after `c3b4612`, `epics_dev` applied on a real debian12 host (PLAY RECAP `ok=15 changed=4 failed=0`) installing EPICS-env 1.3.0 / base 7.0.10 layers 1+2 at `/opt/epics/1.3.0/debian-12/7.0.10`, and the `gz` flavor of the same path also passed (`make build.gz`, `ok=15 changed=4 failed=0`), both observed by the cloud-provision session. |
| T2 | Passed | Rocky 8 (the production IOC server) | 2026-09-03: `species/iocserver.yml` applied with `ok=25 failed=0` — the EPICS distribution cloned from the internal git host as the IOC owner (sparse, tag-pinned 1.2.2) over the proxy CONNECT tunnel, and the iocrunner operator set installed with no test-user creation. |
| T3 | Passed | Debian 13, Rocky 8 | Apply verified 2026-08-31 via proxied iocrunner golden-image bakes: `proxy_contract.bash` applied with proxy seal `clean=true`, and the proxied `pip` installed `epicscorelibs`, `softioc`, and `cothread` (added to `P_python` in `2fc1065`), closing #16. Full-species re-apply idempotency verified the same day: a second `species/iocrunner.yml` apply on the same VM ran `failed=0 changed=0` on both OSes, pip reported "Requirement already satisfied", the proxy artifacts were byte-identical with seal `clean=true`, and the installed-tree fingerprint (pip freeze, dpkg/rpm sets, ioc accounts, EPICS path) was identical between runs. The SOT P_proxy definition landed one-to-one at cloud-provision `8654990`. |

##### Closure Evidence

- Complete 2026-09-03. Every species assembly resolves and applies in
  operator-model order (T1), P_proxy applies and re-applies idempotently (T3),
  and `species/iocserver.yml` applies cleanly on the production IOC server (T2)
  once the internal git host became reachable over the site proxy's CONNECT
  tunnel (`G1` Complete). The same apply verified `M8` and `M9`.

#### M5 - Restore the EPICS OS package set into the operator model

- Origin: 38560eb / M5
- GitHub Issue: #18, https://github.com/jeonghanlee/ansible-provision/issues/18
- Status: Complete

##### Summary

The operator rewrite (`0012e2d`) retired `base_os` and dropped its `pkg_standard`
OS package list, so the iocrunner distribution path (`roles/epics`) installs none
of the EPICS OS build/link dependencies. A fresh Rocky 8 IOC runner image cannot
link an IOC against Net-SNMP (`-lnetsnmp` unresolved). Restore the full EPICS OS
package set into the operator model as ansible-managed per-OS lists, and retire
the `pkg_automation.bash` call from `roles/epics_build`.

##### Scope

Declare a per-OS EPICS package list for all six vacua (rocky8, rocky10, debian12,
debian13, ubuntu24, ubuntu26), reconciled from the retired `pkg_standard` and the
pkg_automation `pkg-<os>/{common,epics,extra}` lists. Install it in `roles/epics`
(distribution path) and `roles/epics_build` (source path), removing the
`pkg_automation.bash` invocation. The normative operator definition in
cloud-provision `docs/IMAGE_WORKFLOW.md` states the requirement first (that
repository is its single writer).

Out of scope: EPICS-env's own internal invocation of pkg_automation (EPICS-env
repo); the source-build tag pins (`M1`/`M2`).

##### Completion Criteria

- The golden pair (rocky8, debian13) installs `epics_os_packages` via ansible on
  both the distribution (`roles/epics`) and source-build (`roles/epics_build`)
  paths; `net-snmp-devel` and `libnetsnmp.so` present.
- `ServiceTestIOC` links successfully against the installed EPICS environment on
  the golden pair.
- `roles/epics_build` no longer calls `pkg_automation.bash`; its OS deps come
  from the ansible list.
- The four non-golden vacua carry the same lists (names dry-run-verified); their
  live verification is `M6`.

##### Dependencies And Decisions

- Owner decisions `D5` (2026-08-31): all six vacua; remove pkg_automation in the
  same change; ansible-provision drafts the cloud `docs/IMAGE_WORKFLOW.md` change
  for cloud-provision; record the milestone and issue before starting.
- Cloud-first ordering: the normative operator definition (cloud-provision
  `docs/IMAGE_WORKFLOW.md`, cloud-provision single-writer) lands before the ansible
  implementation.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner decisions 2026-08-31 (`D5`)
- Implementation Authorization: owner, 2026-08-31
- Superseded Plan Artifacts: none

1. Reconcile the per-OS EPICS package list (`work/plan-epics-os-packages.md`, Phase 0).
2. Draft the cloud `docs/IMAGE_WORKFLOW.md` change; cloud-provision lands it.
3. Install the list in `roles/epics`; remove `pkg_automation.bash` from `roles/epics_build`.
4. Re-bake per OS via cloud-provision; verify.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Fresh proxied bake, inspect installed packages | each of the six vacua | The EPICS OS package set is present; `net-snmp-devel` installed; the `pkg_automation.bash` call is gone. |
| T2 | Integration | Build `ServiceTestIOC` against the installed EPICS env | Rocky 8 | The link stage resolves `-lnetsnmp` and completes. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-31 | rocky8, debian13 | Passed | Distribution: iocrunner golden bakes install the set (`net-snmp-devel` + `libnetsnmp.so` on the fresh VM). Source: `epics_dev` builds and installs EPICS-env clean with `pkg_automation` removed (rocky8 `b553562`, debian13 `d2bb866`, recap `failed=0`). |
| T2 | 2026-08-31 | rocky8, debian13 | Passed | `ServiceTestIOC` built with the snmp module links: `-lnetsnmp` resolves against the installed `libnetsnmp.so`; no "cannot find -lnetsnmp" on either OS. |

##### Closure Evidence

- Complete 2026-08-31. Golden pair verified on both acquisition paths; `pkg_automation` retired from `roles/epics_build`. Along the way the rocky8 list gained `cmake`, `re2c`, `patch` and the debian lines `cmake`/`re2c` (source-build tools the old `pkg_standard` seed lacked), and the `epics_build` OS update excludes `kernel*` and `NetworkManager*` to keep the SSH session alive during a source build. The four non-golden vacua carry the same lists and move to `M6`.

#### M6 - Convergence-verify EPICS OS build dependencies on the four non-golden vacua

- Origin: 38560eb / M6
- Status: Complete

##### Summary

The EPICS OS build dependencies (`M5`) are declared for all six vacua and installed by
`roles/epics` (distribution, `P_epics`) and `roles/epics_build` (source build,
`P_epics-build`). rocky8 and debian13 are golden-verified end to end. The four
non-golden vacua (rocky10, debian12, ubuntu24, ubuntu26) have no iocrunner golden
pipeline yet; convergence-verify them by Live-mode species apply per vacuum across both
acquisition paths. This is convergence verification, not image verification: Live keeps
the running host and the proxy, with no manifest, proxy seal, published image, or
consumer boot.

##### Scope

Both paths, because `M5` changed both — the distribution role installs the set, and the
source-build role installs it AND is where `pkg_automation` was retired:

- Distribution path (`iocrunner` species, `P_epics`): apply Live to a fresh proxied VM,
  confirm the EPICS OS build dependencies install (net-snmp dev package + `libnetsnmp.so`)
  and a sample IOC (`ServiceTestIOC` with the snmp module) links. Needs the published
  EPICS-env-distribution tree for the OS.
- Source-build path (`epics_dev` species, `P_epics-build`): apply Live to a fresh proxied
  VM, confirm EPICS-env builds and installs from source with `pkg_automation` gone and
  `epics_os_packages` providing the deps. Needs no distribution tree.

Per OS: rocky10 and ubuntu24 have distribution trees at 1.2.2 (`rocky-10.2`,
`ubuntu-24.04`), so both paths apply. debian12 and ubuntu26 have no distribution tree at
1.2.2 (`debian-12`, `ubuntu-26.04` absent), so their distribution path stays blocked
upstream (EPICS-env-distribution) and they are convergence-verified by the source-build
path only.

Long-term goal: these four ship as golden images too. Golden promotion — the cloud bake
matrix, consumer-boot paths, and validation — is a separate cloud-provision milestone
that reuses these roles and species as-is. This `M6` convergence check de-risks it.

Out of scope: the golden bake-matrix expansion itself (cloud-provision); the
EPICS-env-distribution publishing of the `debian-12` / `ubuntu-26.04` trees (upstream).

##### Completion Criteria

- Distribution path convergence-verified on rocky10 and ubuntu24 (the two with published
  trees): `epics_os_packages` install and a sample IOC links.
- Source-build path convergence-verified on all four (rocky10, debian12, ubuntu24,
  ubuntu26): EPICS-env builds and installs from source with `pkg_automation` gone.
- Recorded as convergence-verified, not image-verified. The debian12/ubuntu26
  distribution path and golden shipping stay separate upstream/cloud items.

##### Dependencies And Decisions

- Origin decision `D6` (2026-08-31): split from `M5` at its close.
- `epics_os_dir` was missing for rocky10/ubuntu24/ubuntu26 and added in `8350954`, so
  `P_epics` can resolve the distribution sparse path.
- The EPICS-env-distribution 1.2.2 tag has no `debian-12` or `ubuntu-26.04` tree, so the
  distribution path for debian12/ubuntu26 is blocked upstream (tracked at
  jeonghanlee/EPICS-env-distribution#4); the source-build path is their verification
  route until the distribution ships those trees.
- Package names dry-run-verified by cloud-provision on 2026-08-31 (rocky10 needs `P_common`'s
  EPEL+CRB, which the species order provides).

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Distribution path: cloud-provision Live-applies the `iocrunner` species per OS with a
   published tree (rocky10, ubuntu24), checks net-snmp + IOC link, discards the VM.
2. Source-build path: cloud-provision Live-applies the `epics_dev` species per OS (all four),
   confirms the source build completes with `pkg_automation` gone, discards the VM.
3. Record per-vacuum, per-path verification here.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Live `iocrunner` species (distribution, `P_epics`) | rocky10, ubuntu24 | `epics_os_packages` install; a sample IOC links against the installed distribution. |
| T2 | Integration | Live `epics_dev` species (source build, `P_epics-build`) | rocky10, debian12, ubuntu24, ubuntu26 | EPICS-env builds and installs from source with `pkg_automation` gone; `epics_os_packages` provide the deps. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-31 | rocky10, ubuntu24 | Passed | Live `iocrunner` on fresh VMs (`8350954`): rocky10 recap `ok=30 changed=5 failed=0`, ubuntu24 all operators `failed=0`; net-snmp dev package + `libnetsnmp.so` present, `setEpicsEnv.bash` at `/opt/epics/1.2.2/<os>/7.0.10`, ServiceTestIOC links. debian12/ubuntu26 have no distribution tree at 1.2.2 — blocked upstream, jeonghanlee/EPICS-env-distribution#4. |
| T2 | 2026-08-31 | rocky10, debian12, ubuntu24, ubuntu26 | Passed | Live `epics_dev` source build on fresh VMs (`bff06f7`), each `failed=0`: EPICS-env builds and installs from source with `pkg_automation` gone and `epics_os_packages` providing the deps; `setEpicsEnv.bash` present, softIocPVX runs, AreaDetector modules built. ubuntu26 needed `python3-dev` for the pyioc pip C-extension build. |

##### Closure Evidence

- Complete 2026-09-01. Both acquisition paths convergence-verified: distribution (`iocrunner`) on rocky10 and ubuntu24 (the two OSes with a published distribution tree), source build (`epics_dev`) on all four. `pkg_automation` retired; `epics_os_packages` provide the deps. M6 surfaced and fixed two role gaps along the way: the missing `epics_os_dir` for rocky10/ubuntu24/ubuntu26 (`8350954`) and `python3-dev` for the pyioc pip C-extension build (`bff06f7`). debian12/ubuntu26 distribution stays blocked upstream (jeonghanlee/EPICS-env-distribution#4) and golden shipping stays the separate cloud milestone.

#### M7 - Harden the epics_build source build against a dropped connection

- Origin: 38560eb / M7
- GitHub Issue: #19, https://github.com/jeonghanlee/ansible-provision/issues/19
- Status: Complete

##### Summary

`roles/epics_build` runs the whole EPICS-env source build as one long
`ansible.builtin.raw` task over SSH. During `M5` verification (cloud-provision Finding
B), a dropped SSH connection left the remote shell still running on the VM — the
build kept progressing while ansible reported the task failed — so a failed run
can leave a half-built tree, and a same-VM retry can race the surviving shell or
see partial state. `M5`'s fix (`4b272a8`, excluding `kernel*`/`NetworkManager*`
from the update) removed the known trigger, but the underlying structure remains
fragile.

##### Scope

Restructure the `epics_build` source build so a dropped connection cannot leave
an inconsistent tree: e.g. run it as a detached, resumable unit that ansible
polls, or make partial state clean-on-retry with no surviving-shell race.

Out of scope: the dnf-update SSH-drop trigger (fixed under `M5`); the
distribution path (`roles/epics`), which has no long build.

##### Completion Criteria

- A connection drop during the source build does not leave a half-built tree
  that a retry mistakes for progress, and does not race a surviving shell.
- The build completes (or cleanly resumes) and the result is verified on a real
  source-build run.

##### Dependencies And Decisions

- Origin decision `D7` (2026-08-31): harden rather than accept (cloud-provision Finding
  B). `M5`'s `4b272a8` removed the known trigger; this row addresses the
  structure.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-01 (owner accepted the detached/resumable structure)
- Implementation Authorization: 2026-09-01
- Superseded Plan Artifacts: none

Structure: run the source build as a detached `systemd` transient unit that
ansible polls, so a dropped SSH connection cannot leave a half-built tree or let
a retry race a surviving shell. Chosen over the inline clean-on-retry guard
because the detached unit removes the surviving-shell race at the root, matching
`D7`'s intent; cloud-provision validated the direction by manually detaching the build
to survive kills during `M5` verification. All six vacua are systemd-based.

1. Move the inline build body (`roles/epics_build/tasks/main.yml`, the
   `ansible.builtin.raw` build block) into a remote build script at
   `/usr/local/sbin/epics-env-build.sh` (0755) that records a success sentinel
   only after `make check.env` passes.
2. Launch it idempotently: skip when an install tree already exists; leave a
   running unit alone (no second build); otherwise clean partial state and start
   it with `systemd-run --unit=epics-env-build --collect`.
3. Poll to completion with a short `raw` task under ansible `until` — a running
   unit (active or activating) retries, a success sentinel or an existing
   install tree means done, and a stopped unit with neither is a failure that
   surfaces `journalctl` and stops.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Source build with a mid-build connection drop, then retry | rocky8 or debian13 | No half-built tree survives; the build completes or cleanly resumes with no surviving-shell race. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-01 | rocky8 (a fresh lab VM) | Passed | Real path on a fresh rocky8 VM at master 72fa9a9: after the build unit went active, killing the local ansible process left the detached unit still building (single unit, no orphan); a retry reported `EPICS_ENV_BUILD_RUNNING` (changed=false, no second build); a genuine dnf failure was reported `FAILED rc=2` without hanging; a full `epics_dev` run completed (`ok=18 changed=6 failed=0`, Wait `DONE`, install tree `/opt/epics/1.3.0/rocky-8.10/7.0.10/setEpicsEnv.bash`, success sentinel present); a re-apply was idempotent (`ok=4 changed=0`). |

##### Closure Evidence

- T1 passed 2026-09-01 on a fresh rocky8 VM (provisioned by cloud-provision) against ansible-provision master 72fa9a9 (role commit 91a9470):
  the detached systemd unit survives an ansible/SSH kill, a retry attaches to the
  running unit without starting a second build, a real failure is reported without
  hanging, a full source build completes with the install tree and success
  sentinel present, and a re-apply is idempotent (changed=0).
- GitHub issue #19: closed via the completion commit (Closes #19).

#### M8 - Restore chrony poll/key/leap directives dropped by the operator rewrite

- Origin: 38560eb / M8
- GitHub Issue: #20, https://github.com/jeonghanlee/ansible-provision/issues/20
- Status: Complete

##### Summary

The operator rewrite (`0012e2d`) re-authored the `base_os` chrony configuration
into `roles/common` and, in the move, dropped the per-server `minpoll`/`maxpoll`
selectors and the `keyfile`/`leapsectz` directives together with their four
site-overridable variables. A production IOC server whose site `chrony.conf`
depends on those directives (the production IOC server) silently loses them under the operator
model. This is the same class of collateral regression as `M5` (the EPICS OS
package set dropped by the same rewrite).

##### Scope

Restore the four conditionals into the `roles/common` chrony deploy task and
add their empty-string defaults. The restored block is byte-identical to the
pre-rewrite original (`0012e2d^`); empty defaults keep the baseline render
unchanged.

Out of scope: any other chrony directive; the production IOC server site override values
(the `server-configuration` repository); the broader `iocserver` species run.

##### Completion Criteria

- `roles/common` renders `minpoll`/`maxpoll` and `keyfile`/`leapsectz` when set
  and omits each when its variable is empty.
- The baseline render (no site override) is unchanged from before the restore.
- On a real render, a host carrying the production IOC server override produces the
  production `chrony.conf` directives and `chronyd` syncs.

##### Dependencies And Decisions

- Owner decision `D8` (2026-09-02): restore rather than accept the regression.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-02
- Implementation Authorization: 2026-09-02
- Superseded Plan Artifacts: none

1. Restore the four conditionals into `roles/common/tasks/main.yml`'s chrony
   block, byte-identical to `0012e2d^`.
2. Add `chrony_minpoll`/`maxpoll`/`keyfile`/`leapsectz` empty-string defaults to
   `roles/common/defaults/main.yml`.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Regression | Diff the restored block against the shipped `0012e2d^` original; confirm baseline defaults omit the directives | control host | Block byte-identical; empty defaults render no `minpoll`/`maxpoll`/`keyfile`/`leapsectz`. |
| T2 | Integration | Apply the `common` operator with the production IOC server override and inspect `/etc/chrony.conf` | rocky8 (the production IOC server) | `chrony.conf` carries `pool ... minpoll 4 maxpoll 4`, `keyfile`, `leapsectz`; `chronyd` restarts and syncs. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-02 | control host | Passed | Restored `pool`/conditional and `keyfile`/`leapsectz` lines diff-clean against `0012e2d^:roles/base_os/tasks/main.yml`; baseline defaults empty, so the four directives are omitted and the pre-restore render is unchanged. |
| T2 | 2026-09-03 | rocky8 (the production IOC server) | Passed | Live `species/iocserver.yml` apply on the production IOC server: `/etc/chrony.conf` renders all five site pools with `minpoll 4 maxpoll 4`, plus `keyfile /etc/chrony.keys` and `leapsectz right/UTC`. Re-check: `grep -E 'minpoll\|maxpoll\|keyfile\|leapsectz' /etc/chrony.conf`. |

##### Closure Evidence

- Complete 2026-09-03. `roles/common` restores the four conditionals
  byte-identical to the pre-rewrite original (`0012e2d^`); empty defaults leave
  the baseline render unchanged, and the production IOC server override renders the
  production directives. Verified on the production IOC server: `/etc/chrony.conf` carries all
  five site pools with `minpoll 4 maxpoll 4`, `keyfile /etc/chrony.keys`, and
  `leapsectz right/UTC`. GitHub issue #20 closed at verification.

#### M9 - Share the EPICS install root safely across group deployers

- Origin: 38560eb / M9
- GitHub Issue: #21, https://github.com/jeonghanlee/ansible-provision/issues/21
- Status: Complete

##### Summary

With `epics_install_group` set, `roles/epics` prepared the install root as
`root:<group>` `2775` and then cloned the distribution as the IOC owner into
that root-owned directory. Git refuses to operate on a repository whose top
directory is owned by another user ("dubious ownership"), so the owner's clone
failed on a production IOC server, and a second group member could not have
written into the tree either. The role now prepares a group-shared root that
any group member can deploy into: a default ACL grants the group write on newly
cloned content, and a system-wide git `safe.directory` lets any member run git
on the single shared repository. The model is recorded in
`docs/ARCHITECTURE.md` "Shared Install-Root Ownership" (`e8f100b`).

##### Scope

`roles/epics` "Prepare the EPICS install root", group path only: keep
`root:<group>` `2775`, add `setfacl -d` group `rwx` and other `rx` defaults,
and register `path_epics_local` as a system-wide `safe.directory` idempotently.
Delivered in `810eacf`.

Out of scope: the non-group path (owner-owned root, unchanged); creating the
group, firewalld zones, or the NFS export; the site values (group GID,
`root_squash`, idmapping), which live in the site provisioning record.

##### Completion Criteria

- A group member's clone into the root-owned shared root completes without
  git's owner check failing.
- Newly cloned content carries effective group write (`rw` on files, `rwx` on
  directories) regardless of the deployer's umask.
- The root is `root:<group>` `2775` with the default ACL and is listed in the
  system-wide git `safe.directory`.

##### Dependencies And Decisions

- Owner decision `D9` (2026-09-02): the group-shared model and the rejected
  alternatives.
- Reference model: epics-ioc-runner `docs/INSTALL.md` "Shared Deployment
  Directory Setup" (`root:group` `2775` plus default ACLs on local disk).
- Surfaced by the first `species/iocserver.yml` apply on the production IOC
  server once `M4`'s internal-git reachability was resolved.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-02
- Implementation Authorization: 2026-09-02
- Superseded Plan Artifacts: none

1. In the group branch of "Prepare the EPICS install root", add the default
   ACLs and the idempotent system-wide `safe.directory` registration, assign
   the templated values to shell variables once, and end with a `test -d`
   postcondition.
2. Record the ownership model in `docs/ARCHITECTURE.md`.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | Real `git clone` into a directory carrying the default ACL; inspect a cloned file with `getfacl` | control host | The file's effective group permission is `rw` (mask `rw-`), so the ACL grants group write regardless of umask. |
| T2 | Integration | Live `species/iocserver.yml` apply, then `stat`, `getfacl`, `git config --system --get-all safe.directory`, and `getfacl` on a cloned file | rocky8 (the production IOC server) | Clone completes; root is `root:<group> 2775` with the default ACL; the root is a `safe.directory`; the cloned file carries effective group `rw`. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-02 | control host | Passed | Real clone into an ACL-bearing directory: `mask::rw-`, `group:<group>:rwx #effective:rw-`, file mode `-rw-rw-r--+`. |
| T2 | 2026-09-03 | rocky8 (the production IOC server) | Passed | Apply `ok=25 failed=0` (the clone no longer fails on dubious ownership); `stat` → `root:<group> 2775`; `getfacl` → `default:group:<group>:rwx`, `default:other::r-x`; `safe.directory` lists the root; cloned `setEpicsEnv.bash` → `group:<group>:rwx #effective:rw-`, `mask::rw-`. Re-check: `stat -c '%U:%G %a' <root>`, `getfacl -p <root>`, `git config --system --get-all safe.directory`. |

##### Closure Evidence

- Complete 2026-09-03. `roles/epics` (`810eacf`) prepares the group-shared
  root with the default ACL and the system-wide `safe.directory`; verified on
  the production IOC server (T2) after the mechanism was proven on a real
  clone (T1). The model is documented in `docs/ARCHITECTURE.md` "Shared
  Install-Root Ownership" (`e8f100b`).

#### M10 - Route EPICS firewall ports to per-service zones on a multi-homed IOC server

- Origin: 38560eb / M10
- GitHub Issue: #22, https://github.com/jeonghanlee/ansible-provision/issues/22
- Status: Complete

##### Summary

`roles/epics` opened every EPICS port in firewalld's default zone. On a
multi-homed IOC server, CA and PVA sit on different interfaces bound to
different zones, and the default zone carries no interface, so the opening was
ineffective there: the CA zone was already complete but the PVA zone lacked UDP
5075 (name search). The role also opened 5065/TCP, which is not an EPICS port.
The role now opens the CA and PVA port sets each in a site-configurable zone,
validates the zone exists, and carries the protocol-correct port set.

##### Scope

`roles/epics` firewalld task and defaults: add `epics_ca_zone` and
`epics_pva_zone` (empty keeps the default zone), open the CA set in the CA
zone and the PVA set in the PVA zone, validate each named zone against the
permanent zone list and fail loudly if absent, and correct the port lists to
the protocol. Delivered in `0df0c08`.

Out of scope: creating firewalld zones or binding interfaces (site
infrastructure, recorded in the site provisioning record); the Debian family,
which the task does not configure; the `ntp` service, which stays in the
default zone as an outbound client.

##### Completion Criteria

- With both zone values empty, the ports open in the default zone as before.
- With the zones set, the CA set opens in the CA zone and the PVA set in the
  PVA zone, and a missing zone fails the task with a clear error.
- On the production IOC server, a second apply is idempotent (`failed=0`) and
  the PVA zone carries UDP 5075.

##### Dependencies And Decisions

- Owner decision `D10` (2026-09-03).
- Port constants verified against the EPICS base source
  (`configure/CONFIG_ENV`: `EPICS_CA_SERVER_PORT=5064`,
  `EPICS_CA_REPEATER_PORT=5065`; pva2pva: `EPICS_PVA_SERVER_PORT=5075`,
  `EPICS_PVA_BROADCAST_PORT=5076`).
- Surfaced by the post-apply firewall check on the production IOC server
  (`M4/T2`).

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-03
- Implementation Authorization: 2026-09-03
- Superseded Plan Artifacts: none

1. Add the two zone variables and correct the port lists in
   `roles/epics/defaults/main.yml`.
2. Split the firewalld task into a CA loop and a PVA loop, each with its
   optional `--zone`; validate named zones against
   `firewall-cmd --permanent --get-zones`; drop the `|| true` on the port adds
   so a failure aborts the task.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | Syntax-check; POSIX `sh -e` simulation of the task body with empty zones, valid zones, and a misspelled zone | control host | Empty zones yield no `--zone`; valid zones yield `--zone=<zone>` per service; a misspelled zone prints a clear error and aborts. |
| T2 | Integration | Set the two zones in the site override and re-apply `species/iocserver.yml` twice; inspect both zones | rocky8 (the production IOC server) | Second run `failed=0`; the CA zone carries 5064 TCP+UDP and 5065 UDP; the PVA zone carries 5075 TCP+UDP and 5076 UDP. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-03 | control host | Passed | `ansible-playbook --syntax-check` passes; `sh -e` simulation: empty zones → `ca_opt=[] pva_opt=[]`, valid zones → `--zone=` per service, misspelled zone → `error: firewalld zone does not exist: <zone>` and abort. |
| T2 | 2026-09-03 | rocky8 (the production IOC server) | Passed | Site override with the two zones, `git pull` to `0df0c08`, two applies; second recap `ok=25 changed=0 failed=0`. `--zone=<ca-zone> --list-ports`: `5064/tcp 5064/udp 5065/udp` (exactly the CA set). `--zone=<pva-zone> --list-ports`: `5075/tcp 5075/udp 5076/udp` present, alongside site-opened CA ports and `5076/tcp` that the role did not add. |

##### Closure Evidence

- Complete 2026-09-03. `T2` passed on the production IOC server: with the two
  zones set in the site override, the second apply reported `failed=0` with no
  changes, the CA zone carries exactly 5064 TCP+UDP and 5065 UDP, and the PVA
  zone carries 5075 TCP+UDP and 5076 UDP. The PVA zone also lists CA ports and
  5076/TCP opened by the site before this change; the role does not add or
  remove them, so they stay a site matter. Delivered in `0df0c08`.

#### M11 - Install the requested version in the app and EPICS roles

- Origin: 38560eb / M11
- GitHub Issue: #23, https://github.com/jeonghanlee/ansible-provision/issues/23
- Status: Complete

##### Summary

The build roles guarded the whole clone/checkout/build/install block on the
binary already existing, so a changed version selector was silently ignored:
con stayed at its installed version when `con_version` was bumped, and the same
held for procServ, conserver, and the EPICS distribution. The roles now drop the
guard and install the requested version on every apply, replacing the installed
one. The EPICS role additionally re-checks out the requested tag and gains a
clone mode.

##### Scope

`roles/con`, `roles/procserv`, `roles/conserver`, and `roles/epics` task files,
plus `roles/epics/defaults` and the `docs/ARCHITECTURE.md` site-override table.
The three build roles remove the `if [ ! -f <bin> ]` guard, assign the templated
values to shell variables, check out the requested ref, build, and install to
replace, ending with the binary assertion. The EPICS role selects the checkout
by `epics_clone_mode` (minimal: shallow, blob-filtered, single-OS sparse; full:
plain clone of every OS tree), re-checks out the requested tag on an existing
clone, disables sparse when full so a mode switch expands correctly, and fails
loudly on an unknown mode.

Out of scope: comparing the installed version against the configured one, which
the separate site verification tool owns; the wrapper repositories' internal
upstream pin (`SRC_TAG`), which the role does not manage; converting a
minimal-origin clone's shallow history to full.

##### Completion Criteria

- A changed version selector is honored: a re-apply installs the requested
  version, replacing the installed one, on the build roles and the EPICS tree.
- `epics_clone_mode` selects minimal or full, both re-check out the requested
  tag in place, and an unknown value fails the task with a clear error.
- A live apply on a target confirms the version replacement and full mode's
  multi-OS tree.

##### Dependencies And Decisions

- Owner decision `D11` (2026-09-04).
- Surfaced by a report that a `con_version` bump to 1.2.0 left con at 1.1.0.
- Version-model facts confirmed against the repositories: con carries git tags
  (1.0.0/1.1.0/1.2.0); the procServ and conserver wrapper repositories carry no
  tags and pin the upstream daemon version inside `configure/RELEASE`
  (`SRC_TAG`); the EPICS distribution's `epics_env_version` is a git tag whose
  tree holds `<env>/<os>/<base>`.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-04
- Implementation Authorization: 2026-09-04
- Superseded Plan Artifacts: none

1. Remove the install-once guard in the three build roles; check out the
   requested ref, build, install to replace, assert the binary.
2. Rewrite the EPICS checkout around `epics_clone_mode`; re-check out the tag on
   an existing clone; disable sparse in full mode; validate the mode value.
3. Add `epics_clone_mode` to the EPICS defaults and to the ARCHITECTURE
   site-override table.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | ansible `--syntax-check`; RAW_STYLE audit; execute the git sequences (con checkout against the real con repository; EPICS minimal/full/re-checkout/mode-switch against a tag-and-tree-identical fixture); simulate the mode guard | control host | Syntax passes; RAW_STYLE holds; con checks out a requested tag and re-checks out another; minimal yields a single-OS tree, full yields every OS tree, a version change re-checks out in place, a minimal-to-full switch expands to every OS; an unknown mode value aborts with a clear error |
| T2 | Integration | Bump a version selector and re-apply on a target; on a production NFS server set `epics_clone_mode: full` | a target host | The binary or tree is replaced at the requested version; full mode carries every OS tree |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-04 | control host | Passed | `--syntax-check` passes; RAW_STYLE audit (set -e, trailing assertion, shell-variable assignment, even single-quote count) holds; con checked out 1.2.0 and re-checked out 1.1.0 against the real con repository; on a tag-and-tree-identical fixture, minimal produced a single-OS tree, full produced every OS tree, a 1.2.0-to-1.2.2 re-checkout switched in place, and a minimal-to-full switch expanded to every OS after `sparse-checkout disable`; the mode guard accepted `minimal`/`full` and aborted on other values. First-, second-, and third-person reviews converged. |
| T2 | 2026-09-04 | the production IOC server (rocky8) | Passed | `con_version` bumped to 1.2.0 and re-applied: `con -V` went 1.1.0 to 1.2.0 (site verify tool PASS). `epics_clone_mode: full` re-applied: `/opt/epics` is a plain full clone carrying every OS tree (1.2.2/debian-13, 1.2.2/rocky-8.10, plus other env trees and repo files), not a single-OS sparse checkout. Second apply idempotent: PLAY RECAP `ok=25 changed=0 failed=0`. Site verify tool: 23 pass / 0 fail / 1 skip (conserver wrapper ref, not compared by design) |

##### Closure Evidence

- Complete 2026-09-04. `T2` passed on the production IOC server: `con_version`
  1.2.0 re-applied and `con -V` went 1.1.0 to 1.2.0 (the install-once bug is
  gone); `epics_clone_mode: full` produced a plain full clone of every OS tree;
  the second apply reported `ok=25 changed=0 failed=0`. The site verify tool
  scored 23 pass / 0 fail / 1 skip (the conserver wrapper ref, not compared by
  design). Delivered in `fd4ff1c` (roles) and `13bc8e6` (ARCHITECTURE).

#### M12 - Keep /run/cloud-init world-readable after the in-build cloud-init upgrade

- Origin: 38560eb / M12
- GitHub Issue: #24, https://github.com/jeonghanlee/ansible-provision/issues/24
- Status: Complete

##### Summary

On the rocky family the rebuilt cloud-init ships
`/usr/lib/tmpfiles.d/cloud-init.conf` as `d /run/cloud-init 0700 root root`. A
booted guest is 0755 because cloud-init recreates the directory at that mode
every boot, but an in-place package upgrade fires rpm's tmpfiles trigger
(`systemd-tmpfiles --create`), which applies 0700, and no cloud-init stage runs
again until the next reboot. In that window an unprivileged `cloud-init status`
and any unprivileged read of `/run/cloud-init/*` fail with a permission error.
In this stack the only in-place cloud-init upgrade is the rocky branch of
`roles/epics_build`'s detached build (`dnf update`), so the guest-config fix
belongs in that role.

##### Scope

`roles/epics_build/tasks/main.yml`, the rocky/rhel/centos branch of the detached
build script, after the `dnf update`. The role writes
`/etc/tmpfiles.d/cloud-init.conf` containing `d /run/cloud-init 0755 root root - -`
(a same-named file in `/etc` shadows the `/usr/lib` vendor rule) and runs
`systemd-tmpfiles --create /etc/tmpfiles.d/cloud-init.conf` so the running system
is 0755 immediately, not only after the next reboot.

Out of scope: the debian/ubuntu branch (no such tmpfiles rule; the directory is
already 0755); cloud-provision's cloud-init templates (Closed Door on that side,
proxy ADR D018); the operator-path mitigation cloud-provision already shipped
(reading status under sudo).

##### Completion Criteria

- After the role runs on a rocky epics-dev guest, `stat -c %a /run/cloud-init`
  is 755.
- An unprivileged `cloud-init status --long` prints a status, both immediately
  and after a subsequent `systemd-tmpfiles --create`.
- The debian/ubuntu path is unaffected.

##### Dependencies And Decisions

- Owner decision `D12` (2026-09-09).
- Delegated by the cloud-provision session; root cause verified here - the
  trigger is the rocky-branch `dnf update`, and cloud-provision recorded a
  Closed Door (2026-09-08, commit `47c1bb5`) declining a template change.
- Mirrors the 2026-08-17 vmadmin-home 0700 precedent, fixed in
  ansible-provision, not cloud-provision.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-09
- Implementation Authorization: 2026-09-09
- Superseded Plan Artifacts: none

1. After the rocky `dnf update`, write the `/etc` tmpfiles override that shadows
   the vendor rule and apply it with `systemd-tmpfiles --create`.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | ansible `--syntax-check`; RAW_STYLE audit (even single-quote count) | control host | Syntax passes; RAW_STYLE holds |
| T2 | Integration | On a rocky epics-dev guest, trigger the in-place cloud-init upgrade, then check the directory mode and an unprivileged `cloud-init status`, before and after a repeated `systemd-tmpfiles --create` | a rocky epics-dev guest | `/run/cloud-init` is 0755 and unprivileged `cloud-init status --long` prints, both immediately and after the repeated `systemd-tmpfiles --create` |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-09 | control host | Passed | ansible `--syntax-check` on the epics_build operator playbook passes; the RAW_STYLE even single-quote count holds (build block 34) |
| T2 | 2026-09-09 | a rocky10 epics-dev guest | Passed | Pre-state already showed the post-upgrade bug: `/run/cloud-init` at 0700, the vendor rule 0700, no `/etc` override, and an unprivileged `cloud-init status --long` aborting with a permission traceback. Running the role's verbatim override step as root (write `/etc/tmpfiles.d/cloud-init.conf` as `d /run/cloud-init 0755 root root - -`; `systemd-tmpfiles --create /etc/tmpfiles.d/cloud-init.conf`) took the directory to 0755 and `cloud-init status --long` then printed `status: done`. A subsequent full `systemd-tmpfiles --create` - the rpm tmpfiles trigger - left it at 0755 with status still printing; the `/etc` override shadows the `/usr/lib` vendor rule. `dnf update` was not re-run because the guest already carried the post-upgrade 0700 state. |

#### M13 - Fix RedHat python provisioning for EPICS source builds

- Origin: 38560eb / M13
- GitHub Issue: #25, https://github.com/jeonghanlee/ansible-provision/issues/25
- Status: Complete

##### Summary

The `python` operator leaves the RedHat family unable to build EPICS Python
components, in two ways. First, it installs Python dev headers (`Python.h`) on
Debian (`pkg_python_debian` carries `python3-dev`) but not on RedHat:
`roles/python/tasks/main.yml` installs `pkg_python_redhat + pkg_python_system`,
and neither list carried a `*-devel` package. Second, on rocky8 the operator set
only the unversioned `python` alternative, not `python3`, so `python3` stayed the
system 3.6 and pyDevSup's makehelper compiled against the absent 3.6 headers.
Both surfaced by re-adding pyDevSup on a rocky8 epics-dev guest (EPICS-env
release-1.4.0, `make build.gz`, Layer 1): `fatal error: Python.h: No such file
or directory`.

##### Scope

Dev headers: `roles/python/defaults/main.yml` (default `pkg_python_redhat`, add
`python3-devel` for rocky10 and any generic RedHat vacuum) and
`inventory/group_vars/rocky8.yml` (rocky8 override, add `python39-devel` for its
3.9 module).

Alternatives: `roles/python/tasks/main.yml` sets the python command alternatives
from a `runtime_python_alts` list of name -> path pairs, applying each only when
its alternatives group exists and failing loudly when a present group cannot be
set. The default sets `python -> /usr/bin/python3`; rocky8 adds
`python3 -> /usr/bin/python3.9` and keeps `python -> /usr/bin/python3`, which
then follows python3 to 3.9.

Out of scope: the debian family (already carries `python3-dev` and
`python-is-python3`); removing the system python 3.6 on rocky8 (RHEL8
platform-python depends on it, so the switch is via alternatives, not removal);
the target python version per OS beyond the current selections.

##### Completion Criteria

- After the `python` operator runs on a rocky8 guest, `python3` resolves to 3.9
  and `Python.h` is present under that version's include dir.
- On rocky10 (and generic RedHat), `python3-devel` provides `Python.h` for the
  system python3.
- pyDevSup compiles on the Rocky `gz` build path.
- The debian path is unaffected.

##### Dependencies And Decisions

- Owner decisions `D13` (dev headers, 2026-09-10) and `D14` (python
  alternatives, 2026-09-11).
- Delegated by the EPICS-env session (jeonghanlee/EPICS-env#71); both defects
  verified here against `roles/python` and the rocky group_vars, the
  alternatives defect confirmed by that session on a rocky8 guest.
- The code for both fixes is implemented; T2 live rocky verification follows on
  VM availability (needs a rocky8 and a rocky10 epics-dev guest).

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-11
- Implementation Authorization: 2026-09-11
- Superseded Plan Artifacts: none

1. Add `python3-devel` to the default `pkg_python_redhat` in
   `roles/python/defaults/main.yml`.
2. Add `python39-devel` to the `pkg_python_redhat` override in
   `inventory/group_vars/rocky8.yml`.
3. Replace the single `alternatives --set` with a `runtime_python_alts`
   name -> path list looped in `roles/python/tasks/main.yml`: set each only if
   its group exists, fail loudly otherwise; rocky8 adds `python3 -> 3.9`.
4. Verify on a live rocky8/rocky10 guest that `python3` resolves correctly,
   `Python.h` is present, and pyDevSup builds.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | ansible `--syntax-check` on the python operator; all edited files parse as valid YAML; the `runtime_python_alts` loop renders the expected `name:path` tokens; RAW_STYLE single-quote parity holds | control host | Syntax passes; files well-formed; rocky8 renders `python:/usr/bin/python3 python3:/usr/bin/python3.9` |
| T2 | Integration | Run the `python` operator on rocky8 and rocky10 epics-dev guests, then check that `python3` resolves to the intended version, `Python.h` is present, and pyDevSup builds `gz` | rocky8 and rocky10 epics-dev guests | rocky8 `python3` -> 3.9 with `Python.h`; rocky10 system python3 with `python3-devel`; pyDevSup compiles; debian unaffected |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-11 | control host | Passed | `--syntax-check` exits 0; all edited files valid YAML; the `runtime_python_alts` loop renders `python:/usr/bin/python3 python3:/usr/bin/python3.9` on rocky8; RAW_STYLE single-quote parity holds (raw block 8, even) |
| T2 | 2026-09-11 | rocky8 and rocky10 epics-dev guests (EPICS-env session) | Passed | Both clean PASS, no manual override. rocky8: the operator set `python3` -> 3.9 and pyDevSup built against 3.9. rocky10: python3 is native 3.12, the absent `python` alternatives group skips cleanly (op.python rc 0), and pyDevSup built against 3.12. Both: MCoreUtils `libmcoreutils.so` has 0 `.debug_info`, `check_deps` exit 0; full public gz matrix 6/6 |

##### Closure Evidence

- Delivered in af239dd (dev headers), 37829b5 (python3 alternatives), and 54b32c6 (absent-group if-guard).
- T2 Passed 2026-09-11 (EPICS-env session): rocky8 and rocky10 clean operator runs with no manual override, pyDevSup built on both; full public gz matrix 6/6.

#### M14 - Middleware server provisioning (Archiver Appliance, Phoebus)

- Origin: 38560eb / M14
- Status: Blocked (on G2)

##### Summary

A middleware server (the middleware counterpart of the IOC dev host) hosts the
EPICS Archiver Appliance and Phoebus, each independently selectable, on the
`common` + `epics` base, provisioned the same way the IOC species are. It runs
the system Java (the distribution OpenJDK 21 with `JAVA_HOME` exported), Tomcat
9.0.121 as the shared `CATALINA_HOME`, and MariaDB as the Archiver Appliance
configuration database; the applications install from their binary distribution
repositories, each with a source-build alternative. ansible-provision mirrors
the operator/species structure and the middleware OS package baseline that
originate in cloud-provision (`G2`) as the normative source and land first.

##### Scope

- A `java` operator: install the distribution OpenJDK 21 JDK (the development
  package, not the headless runtime) from the mirrored package set and export
  `JAVA_HOME` at the distribution JDK path (family-specific, exposed as an
  override key with the distribution default). No non-system pin and no Maven
  package: the source-build path obtains Maven 3.9.9 through the epicsarchiverap-maven
  Maven Wrapper (`./mvnw`).
- A `tomcat` operator: Tomcat 9.0.121 (Apache tarball) as the shared
  `CATALINA_HOME` only; the Archiver Appliance instance skeleton, `server.xml`
  / `context.xml`, and schema stay with epicsarchiverap-env.
- A `mariadb` operator: the MariaDB server with the `archappl` database and
  user, kept a separable module because epicsarchiverap-env replaces it with SQLite later.
- Application operators `archiver` and `phoebus`: install the aa-distribution
  WARs and the phoebus-distribution binary, each paired with a source-build
  operator (`archiver-build` builds epicsarchiverap-maven at its freeze tag with `./mvnw`
  and needs `JAVA_HOME`, git with an origin ref, openssh-client, outbound HTTPS,
  and `-Dsphinx.skip=true`; `phoebus-build` builds Phoebus from source).
- Species `archiver` and `archiver-dev` (distribution install / source build),
  `phoebus` and `phoebus-dev`, and `middleware` (the selectable combination)
  layer those operators on `common` + `epics`, with the service group `mid` and
  user `mid-srv` parallel to `ioc` / `ioc-srv`, run as `make <species>.<vacuum>`.
- Version values (Tomcat, distribution refs) are override keys with neutral
  public defaults; internal endpoints (proxy, internal git remote, NTP) are
  supplied through the site override layer, not committed here.

Out of scope: the cloud-provision operator/species structure, middleware
package baseline, and middleware VM (`G2`, owned by the cloud-provision
session); creating and populating the aa-distribution and phoebus-distribution
repositories (epicsarchiverap-env and phoebus-env); the Archiver Appliance instance layout
and schema (epicsarchiverap-env); the site override values (the `server-configuration`
repository); Maven as an installed package.

##### Completion Criteria

- The middleware species provisions the distribution OpenJDK 21 JDK with
  `JAVA_HOME` at its path, Tomcat 9.0.121 at the shared `CATALINA_HOME`,
  MariaDB with the `archappl` database, and the selected applications
  (Archiver Appliance WARs, Phoebus binary) on a middleware host, layered on
  `common` + `epics`, under group `mid` / user `mid-srv`.
- The `archiver-dev` and `phoebus-dev` species provision the same applications
  through their source-build operators; no non-system Java pin and no Maven
  package are installed, and the Archiver Appliance build runs through `./mvnw`.
- Version values are override keys with neutral public defaults; no internal
  endpoint is committed to this repository.
- The species runs as `make <species>.<vacuum>` and a re-apply is idempotent.

##### Dependencies And Decisions

- `G2` (Open): cloud-provision ships the middleware operator/species structure,
  the middleware OS package baseline (system OpenJDK 21, Tomcat 9.0.121,
  MariaDB), and the middleware VM as the normative source (cloud-provision
  `docs/milestone-e260630.md` M11, D2, D3). `M14`'s row stays Blocked while `G2`
  is Open, but implementation proceeds on the branch (develop-before-merge, see
  Implementation Plan); the row completes when M11 merges (`G2`) and M14/T2 passes.
- `G3` (added 2026-09-23, Complete 2026-09-23): epicsarchiverap-env's `sql.fill` loaded no
  schema when the database and application account are provisioned externally,
  as this operator provisions them, and exited 0 anyway
  (jeonghanlee/epicsarchiverap-env#47, owned by the epicsarchiverap-env session). Fixed in
  `1fc20a8` on `modernize`; #47 closed with epicsarchiverap-env's acceptance recorded. The
  operator's post-`sql.fill` table check stays as a guard. `M14` stays Blocked
  while `G2` is Open and resumes as In progress when it is Complete.
- `D15` (owner, 2026-09-11): build it the ansible-provision way; internal
  specifics via the site override layer. Its pinned non-system Java/Maven and
  Phoebus-build substance is superseded by `D16`.
- `D16` (owner, 2026-09-12): system Java with `JAVA_HOME`, no Maven package
  (epicsarchiverap-maven wrapper on the source-build path), Tomcat 9.0.121 and MariaDB as
  the Archiver Appliance baseline, Archiver Appliance and Phoebus from their
  binary distribution repositories with source-build alternatives, group `mid`
  / user `mid-srv`.
- Sub-decisions resolved (owner, 2026-09-14): increment scope - the
  source-build path first, first increment `archiver-dev` (`java` + `tomcat` +
  `mariadb` + `archiver-build` + the `archiver-dev` species), matching the
  cloud-provision M11/T2 live gate; target vacuum - rocky8 first
  (cloud-provision's proposal), debian13 to follow; the `mid` group GID follows
  the `ioc`/`ioc-srv` precedent (a site-set GID via an override key); Maven proxy
  - ansible-provision supplies a `settings.xml` through the site override layer
  (Maven does not read the proxy env vars the `proxy` role exports), pending
  confirmation with epicsarchiverap-maven on ownership.
- Increment order (2026-09-15): add the standalone `java` operator first and
  reuse `proxy`, `common`, `provenance`, `python`, and `epics` unchanged.
  Tomcat, MariaDB, and the full `archiver-dev` assembly follow; epicsarchiverap-env and
  epicsarchiverap-maven are required for the application path.
- EPICS distribution selector (2026-09-15): use 1.3.0 as the `epics` role
  default, with Base 7.0.10. Existing operator behavior remains unchanged.
- `archiver_build` realization (owner, 2026-09-18): the operator drives epicsarchiverap-env's
  make sequence (epicsarchiverap-env clones and builds epicsarchiverap-maven from source internally); it
  does not build epicsarchiverap-maven separately. Runs as root like the other build
  operators - no build-user split, since epicsarchiverap-env's internal sudo no-ops when
  already root and `make install` chowns the instances to `mid-srv:mid`
  regardless. Pinned epicsarchiverap-env `fb43522` and epicsarchiverap-maven `SRC_TAG=3c96141d`; the epicsarchiverap-env
  pin moved to `e06c554` on 2026-09-21, to `6a026d4` on 2026-09-22 and to
  `1fc20a8` on 2026-09-23 (see the increment status). Variable
  placement: `configure/RELEASE.local` (SRC_TAG) and `../CONFIG_SITE.local` -
  one directory above the checkout, which survives the OS-conf rewrite -
  (AA_USERID/AA_GROUPID, DB name/user/pass, DB_HOST_NAME=127.0.0.1,
  DB_HOST_PORT, JAVA_HOME/TOMCAT_HOME). Pre-create `mid`/`mid-srv` with a
  site-set GID (ioc/ioc-srv precedent); default `als` overlay; skip epicsarchiverap-env
  `db.secure`/`db.addAdmin`/`db.create` (the `mariadb` operator makes the DB and
  account) and `install_os_packages.bash` (the operators supply the packages).
  Checkout at `/opt/epicsarchiverap-env-src`. Boundary: epicsarchiverap-env owns each make
  target's internals (WAR build, instance layout, systemd unit, schema, overlay);
  this operator owns orchestration, refs, config, and the service account.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-15 (Java-first increment, followed by standalone Tomcat and MariaDB)
- Implementation Authorization: 2026-09-15 (standalone `java`, `tomcat`, and `mariadb` additions; develop on branch
  `m14-middleware-reconcile` against the cloud-provision M11 branch definition
  `m11-middleware-operators` d52827c; merge to master after M14 and M11/T2)
- Security setup authorization: 2026-09-16 (remove anonymous accounts, remote
  root accounts, the test database and its default database grants)
- Review correction authorization: 2026-09-16 (remove the credential hash from
  command arguments and reject unsupported existing authentication conditions
  without clearing their security policy)
- MariaDB loopback-TCP authorization: 2026-09-18 (add a TCP-loopback +
  `skip-name-resolve` mode gated on `mariadb_skip_networking: false`, the
  `archappl@'127.0.0.1'` application account, and secure-step hardening to keep
  only `root@'localhost'`; committed `5b5ee44`. Wire it for the archiver species
  through the `[archiver_dev]` group and `group_vars/archiver_dev.yml`; committed
  `08dbb93`.)
- archiver_build authorization: 2026-09-18 (drive epicsarchiverap-env's make sequence as root
  in order: `init` -> `db.conf` -> `conf.archapplproperties` -> `build.mvn` ->
  `sql.fill` -> `conf.storage` -> `install` -> `sd_start`; never `make build`
  wholesale, which bundles the root `conf.storage`. Realization per the
  2026-09-18 sub-decision above.)
- Superseded Plan Artifacts: none

Developed before `G2` rather than after: `G2` completes when cloud-provision M11
merges to master, which follows M11/T2, which needs these M14 roles - so the
non-deadlocking path is to develop on the branch against the M11 branch
definition now (owner and cloud-provision, 2026-09-14).

1. Add the standalone `java` role and operator playbook, register `op.java`,
   and document its distribution JDK defaults and site override keys. Reuse
   the existing EPICS operators. Verify syntax and target resolution locally;
   verify installation, alternatives, login environment, and re-apply on rocky8.
2. Continue toward `archiver-dev`, rocky8: mirror the middleware OS package
   baseline (system OpenJDK 21, Tomcat 9.0.121, MariaDB) from the cloud-provision
   M11 branch; reuse `java` and add the `tomcat`
   (9.0.121 shared `CATALINA_HOME`), and `mariadb` operators; add the
   `archiver-build` operator, the `mid` group and `mid-srv` user, and the
   `archiver-dev` species.
   The Tomcat increment installs the SHA-512-verified Apache 9.0.121 archive
   under a versioned root-owned directory, exposes `/opt/tomcat9` as shared
   `CATALINA_HOME`, and registers `op.tomcat`. Version, checksum, URL, and
   paths are site override keys. The operator creates no service or application
   instance; a temporary instance verifies Java 21 startup and HTTP on both
   target VMs. Re-apply and invalid-checksum tests verify preservation.
   Destinations cannot contain one another. Re-apply checks the archive file
   list and hashes, root ownership, readable files, searchable directories,
   and executable startup scripts before publishing the home link or profile.
   The MariaDB increment installs the distribution server, enables its service,
   and supplies a runtime Unix domain socket: `/run/mariadb/mariadb.sock` on
   RedHat and `/run/mysqld/mysqld.sock` on Debian. TCP is disabled by default;
   a boolean override permits localhost TCP. Root management uses socket
   authentication; the application uses a private site-supplied password hash
   and receives only the `archappl` database privileges, without grant authority.
   Database creation uses epicsarchiverap-env's `utf8mb4` default. Schema, the separate admin
   workflow, and JDBC/client transport configuration remain with epicsarchiverap-env.
   Verify actual client login, data operations, denied access, re-apply,
   password rotation, and service restart on both OS families.
   Security setup removes anonymous accounts and root accounts outside the
   distribution localhost/loopback scope through DROP USER, drops the test
   database, removes its default database-level grants including orphan rows,
   and reloads privileges. Other databases and application accounts remain.
   The account hash is sent through SSH stdin by a controller-side raw action,
   with no target Python or credential file. A visible preflight rejects
   existing TLS requirements, explicit password expiration and account locks
   before account mutation; package and service configuration precede it.
3. Extend to debian13; add the distribution path (`archiver` operator and
   `archiver` species).
4. Add `phoebus` / `phoebus-build` and the `phoebus` / `phoebus-dev` /
   `middleware` species.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Structure | Syntax-check the middleware species and confirm they are enumerated in `configure/RELEASE` and `inventory/lab.ini` | control host | The species resolve their operator imports and are registered. |
| T2 | Integration | Apply the middleware species on a middleware host and inspect `JAVA_HOME`, `$JAVA_HOME/bin/java -version`, the Tomcat `CATALINA_HOME`, the MariaDB service, the `mid` group and `mid-srv` user, and the installed application artifacts | middleware host | `JAVA_HOME` points to the distribution JDK path and its `java -version` reports the distribution OpenJDK 21, no Maven package is installed, Tomcat 9.0.121 and MariaDB are present, the selected applications are installed under `mid` / `mid-srv`; a re-apply is idempotent. |
| T3 | Integration | Apply the real `common` and `java` operators on fresh VMs; inspect the installed JDK and default commands; remove only the installed JDK development package and repeat `op.java` to verify installation change reporting | Rocky 8.10 and Debian 13 | OpenJDK and javac 21 are installed; default commands resolve under `JAVA_HOME`; actual package installation reports `changed=1`, `failed=0` |
| T4 | Integration | Re-apply `op.java`; run the installed commands in a new login shell; compare the Java profile hash, inode, mtime, ownership and mode before and after | Rocky 8.10 and Debian 13 | Re-apply reports `changed=0`, `failed=0`; login exports the distribution `JAVA_HOME`; the profile remains identical and root:root 0644 |
| T5 | Integration | Apply `op.provenance`, `op.python`, and `op.epics` after `common`; use the default EPICS version without extra-vars; compare checkout identity with the remote tag and inspect the OS tree and login environment | Rocky 8.10 and Debian 13 archiver-dev VMs | EPICS-env 1.3.0 / Base 7.0.10 installs, the checkout matches the remote tag, 70 module entries have live links, and sampled modules provide headers and DBD files |
| T6 | Integration | Generate and build the shipped Base example with `makeBaseApp.pl`; run its generated startup script; read, write, and monitor its records through CA; run the unmodified EPICS-env 1.3.0 `tools/check_deps.bash` against the installed tree | Same two VMs | Example IOC builds and exits cleanly; CA read/write/readback and monitor updates pass; dependency checker exits 0 |
| T7 | Integration | Re-apply `op.epics`; compare installed package lists, checkout state, profile content hashes, and login environment; verify Python EPICS imports and the existing Java runtime/compiler | Same two VMs | Re-apply exits 0 with no package, checkout, or environment-content drift; Python imports succeed and Java/Javac remain 21 |
| T8 | Integration | Apply the real `op.tomcat` after Java; inspect the verified archive installation and login CATALINA_HOME; start and stop a temporary instance using the installed scripts and stock ROOT application | Rocky 8.10 and Debian 13 archiver-dev VMs | Tomcat 9.0.121 runs with Java 21 and serves HTTP; the shared home remains root-owned and no persistent instance or service is created |
| T9 | Integration | Re-apply `op.tomcat`; compare install files and profile metadata; use isolated paths to test an invalid checksum, valid overrides, and a modified installed JAR through the real operator | Same two VMs | Re-apply reports unchanged and preserves installed content; checksum rejection exits nonzero before publishing a home or profile; modified files are rejected without overwrite |
| T10 | Integration | Use the real operator with isolated paths to reject overlapping destinations before and after installation, a non-searchable parent, JAR mode 0600, directory mode 0700, startup-script modes 0644 and 0700, an added executable `bin/setenv.sh`, a symlink, and changed or missing JARs; compare content and metadata before and after each rejection; repeat the default re-apply and temporary-instance HTTP/startup/shutdown checks | Same two VMs | Every invalid case exits nonzero without changing the installed tree, home link, or profile; restoring valid state permits unchanged re-apply; the default installation remains usable with Java 21 |
| T11 | Integration | Apply the real `op.mariadb` after common; inspect the installed server, systemd service, socket and root authentication; use the distribution client as an ordinary user to create, read, update and remove a temporary application table, including a four-byte UTF-8 value; attempt invalid credentials and access to mysql.user | Rocky 8.10 and Debian 13 archiver-dev VMs | Distribution MariaDB runs through UDS, root requires Unix socket authentication, the application has only archappl database privileges, and unauthorized access fails |
| T12 | Integration | Re-apply through Make and compare configuration hashes and metadata, service PID, account definitions and existing profiles; rotate and restore the application password; enable localhost TCP and restore UDS-only mode; restart the service; restrict runtime/socket permissions and re-apply | Same two VMs | Unchanged runs report changed=0; credential and configuration changes report changed; data survives; old credentials and root TCP access fail; restart and permission repair restore ordinary-user UDS access |
| T13 | Integration | Use the real operator to reject missing credentials, reserved or malformed names, trailing newlines and a non-boolean transport value; test a separate existing latin1 database, an account with global privileges and a symlink configuration file; create a separate database named select with a separate application account | Same two VMs | Invalid inputs fail before provisioning; conflicting database/account definitions and symlink targets remain intact; quoted database identifiers install and re-apply correctly; fixture cleanup leaves the default database empty and the service on UDS only |
| T14 | Integration | Apply the real op.mariadb on both VMs, then seed anonymous accounts, remote root accounts including quoted/backslash host names, a populated test database, default test-prefix grants and an orphan grant row; retain a separate account and data in unrelated, test-prefix and application databases; apply under NO_BACKSLASH_ESCAPES and re-apply | Rocky 8.10 and Debian 13 | Target accounts, test database and default test grants are absent; test-prefix access is denied; other accounts, data, SQL mode, service PID and configuration are preserved; repeated apply reports changed=0 |
| T15 | Integration | Run tests/check-raw-stdin.yml normally and with --check through real SSH/sudo, using only public multiline markers; render the role and confirm its hash appears only in stdin; create a separate account through Make op.mariadb and rerun the password-rotation, UDS/TCP and security-cleanup checks | Rocky 8.10 and Debian 13 | Exact stdin arrives without a TTY and is absent from the receiving shell arguments; command failures and no_log enforcement are preserved; check mode skips execution; account creation, credential rotation, data preservation and unchanged reapply pass |
| T16 | Integration | Create a separate database/account through the real operator; add REQUIRE X509, SSL, CIPHER, ISSUER and SUBJECT separately on both servers; test PASSWORD EXPIRE and ACCOUNT LOCK on MariaDB 11.8; apply after each condition and compare SHOW CREATE USER and SHOW GRANTS, then restore the fixture condition | Same two VMs | Each unsupported condition produces a visible failure before account changes and preserves definitions; restoring the condition permits ordinary-user data access and changed=0 reapply; remove only the temporary fixture database and account |
| T17 | Integration | Apply the `archiver_build` build steps (`init`, `db.conf`, `conf.archapplproperties`, `build.mvn`) as root with the pinned epicsarchiverap-env ref (`fb43522` when this ran) + epicsarchiverap-maven `SRC_TAG=3c96141d`; inspect the produced WARs and the als overlay in `WEB-INF/classes`, and the schema load by the configuration database's tables (`make sql.show`), never by `sql.fill`'s exit status | Rocky 8.10 and Debian 13 archiver-dev VMs, and a freshly provisioned host | The four `aa-*-{mgmt,engine,etl,retrieval}.war` build with the als `appliances.xml`/`archappl.properties`/`policies.py` packed; `sql.fill` loads the schema over TCP as `archappl@'127.0.0.1'`, and the database holds `PVTypeInfo`, `PVAliases`, `ArchivePVRequests` and `ExternalDataServers` |
| T18 | Integration | Run the root install steps (`conf.storage`, `install`, `sd_start`); inspect `/arch` ownership, the four instances under `/opt/epicsarchiverap-maven`, the `epicsarchiverap-maven.service` unit and state, mgmt HTTP, and one archived PV | Same hosts as T17 | `/arch` and the instances are `mid-srv:mid`; the unit is enabled and active; mgmt returns HTTP 200; one PV archives and reads back |
| T19 | Integration | Re-apply the full `archiver_build` operator; compare the installed tree, unit, and service PID before and after | Same two VMs | Re-apply reports `changed=0`, `failed=0`; the installed tree, unit, and running service are unchanged |
| T20 | Soak | Apply the `archiver_dev` species through this operator at the pin to the soak host with the README test store values (a fresh host, or an installed one with `archiver_force_reinstall=true`); archive 100 PVs of varied name shapes, rates (0.1, 1 and 10 Hz), deadband, 1000-element waveforms, enum and string, mixing MONITOR and SCAN and the default policy with the VeryFast, Medium and Fast overrides; sample host, per-process, per-log-stream, per-tier and database state every 5 minutes for 24 h across one UTC midnight; restart the appliance once after that midnight | The soak host (Rocky 8.10) | The installed `policies.py` carries the test values and T17 passes on this host; every PV reaches STS, MTS and LTS, and a second LTS day partition appears within about three hours after midnight; after the restart `PVTypeInfo` still holds 100 rows and every PV is Being archived again; no kernel OOM and no instance lost; per-stream log growth and per-process memory and CPU are recorded |
| T21 | Soak | After T20, load the same appliance for 24 h: step up the PV count and rates and add concurrent retrieval, in a profile the owner sets from the per-PV disk, heap and CPU figures T20 measured; at the end restart the day-1 soak IOC (the one serving the T20 PVs) once, and remove the owner write bit across the whole MTS tree for at least one STS-to-MTS pass, about 10 minutes and until the etl log shows the write error, then restore it (ETL writes as `mid-srv`, and the top directory alone leaves existing subdirectories and files writable) | Same host | Each step's resource use, ETL pass time, retrieval latency and error rate are recorded; the first step at which an instance is lost or mgmt stops answering, if any, is recorded as the limit; the log lines and dominant messages around the two end events are recorded |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | pending | control host | Not run | |
| T2 | pending | middleware host | Not run | |
| T3 | 2026-09-15T07:43:13Z | Fresh Rocky 8.10 and Debian 13 archiver-dev VMs | Passed | Real Make `op.common` and `op.java` runs installed OpenJDK and javac 21.0.12.1 on both. After removal of only `java-21-openjdk-devel` or `openjdk-21-jdk-headless`, the corrected role reinstalled the package and reported `ok=1 changed=1 failed=0` on each host. Initial live execution exposed merged package output masking the change sentinel; the role now reads its final stdout line. |
| T4 | 2026-09-15T07:43:13Z | Same Rocky 8.10 and Debian 13 VMs | Passed | The real `op.java` re-apply reported `ok=1 changed=0 failed=0` on both. Fresh `bash -l` sessions verified runtime/compiler 21.0.12.1 and command resolution under `/usr/lib/jvm/java-21-openjdk` (Rocky) or `/usr/lib/jvm/java-21-openjdk-amd64` (Debian). The profile SHA-256, inode, mtime and root:root 0644 ownership/mode matched before and after. |
| T5 | 2026-09-15T17:12:59Z | Rocky 8.10 and Debian 13 archiver-dev VMs with common and Java installed | Passed | Real Make targets installed the prerequisites and distribution. Default 1.3.0 resolved to remote tag commit `d18e1cd0da2b62580d7d48d6e496bcb7e5757c38`; each clean sparse checkout selected its own OS tree. Login `EPICS_BASE`, profile mode/ownership, 70 module entries, live links, and calc/asyn/busy/sscan/std headers and DBD files passed. |
| T6 | 2026-09-15T17:12:59Z | Same two VMs | Passed | Each installed Base generated and built its own example IOC using the shipped templates. Its startup script, CA read/write/readback, monitor updates, and clean exit passed. The unmodified 1.3.0 dependency checker exited 0 on both: 150 executables and 78 shared libraries, with zero RPATH, non-system ABSPATH, or lost-ORIGIN violations. Sourced ldd checks resolved softIoc/caget/caput/camonitor dependencies. |
| T7 | 2026-09-15T17:12:59Z | Same two VMs | Passed | Real `op.epics` re-apply reported Rocky `ok=6 failed=0` and Debian `ok=5 failed=0 skipped=1`. Before/after package lists, clean checkout identity, sparse selection, profile content hashes, Python versions/imports, and login environment matched. Java and javac remained 21.0.12.1 with correct command resolution and profile ownership/mode. The existing role suppresses change reporting; `changed=0` alone is not the evidence. |
| T8 | 2026-09-15T18:49:43Z | Rocky 8.10 and Debian 13 archiver-dev VMs | Passed | Real `op.tomcat` first runs reported `ok=1 changed=1 failed=0` on both. The official archive SHA-512 and installed version matched 9.0.121. Login CATALINA_HOME resolved through `/opt/tomcat9`; root ownership and permissions passed. Stock configuration and the shipped ROOT application in temporary CATALINA_BASE directories ran with Java 21, returned HTTP 200, and stopped cleanly via the installed shutdown script. Shared install content/metadata stayed unchanged. Neither host has an installed Tomcat service. |
| T9 | 2026-09-15T18:49:43Z | Same two VMs | Passed | Default and alternate-path re-applies reported `ok=1 changed=0 failed=0`. File hashes, ownership, permissions, inode, mtime, home symlink, and Tomcat/Java/EPICS profiles matched before and after default re-apply. The real operator rejected an incorrect SHA-512 before publishing any destination, installed with valid path overrides, and rejected a modified JAR without overwriting it. Temporary failure-test installs were removed; default installations remained unchanged and Java 21 verification passed. |
| T10 | 2026-09-16T05:29:38Z | Rocky 8.10 and Debian 13 archiver-dev VMs | Passed | All listed invalid states were rejected by the real `op.tomcat`; content hashes, modes, ownership, inode, mtime, and home/profile state matched before and after rejection. Incorrect archive checksums still failed before publishing a destination. Fresh alternate-path installs passed, and valid or restored installs reported `changed=0`. Default re-apply also reported `changed=0` on both, preserving the shared tree and Tomcat/Java/EPICS profiles. Installed scripts with the stock ROOT application returned HTTP 200 and stopped cleanly under Java 21. |
| T11 | 2026-09-16T06:48:18Z | Rocky 8.10 and Debian 13 archiver-dev VMs | Passed | The real package task installed MariaDB 10.3.39 and 11.8.6 respectively. The real service/account tasks configured root Unix socket authentication, utf8mb4 archappl and its localhost account. Final-code client tests as vmadmin created/read/updated/deleted/dropped a temporary table and round-tripped a four-byte UTF-8 value. Wrong/empty passwords, root access as an ordinary OS user and mysql.user reads failed. No MariaDB TCP listener remained in default mode. |
| T12 | 2026-09-16T06:48:18Z | Same two VMs | Passed | Final-code re-applies reported ok=3 changed=0 failed=0 on each. Config content, ownership/mode, inode/mtime, service PID, root/application definitions and Java/EPICS/Tomcat profiles matched. Password rotation rejected the old password and preserved data; rotation re-apply was unchanged. Localhost TCP served the application while rejecting root TCP; restoring UDS disabled TCP. Service restart preserved data. Restricting runtime mode to 0750 and socket mode to 0770 was repaired by the real operator to mysql:mysql 0755 and 0777, with ordinary-user login restored and subsequent re-apply unchanged. |
| T13 | 2026-09-16T06:48:18Z | Same two VMs | Passed | All listed invalid-input runs failed and preserved the default configuration, service PID and account definitions. The real operator rejected a separate latin1 database and an account with global SELECT without changing their definitions. A symlink at the managed config path was rejected without overwriting its target or restarting MariaDB. A fresh database named select and its separate account installed successfully and reapplied unchanged. Only test-created fixtures were removed; the default archappl database is empty and final re-apply reported changed=0 on both. |
| T14 | 2026-09-16T15:05:57Z | Rocky 8.10 / MariaDB 10.3.39 and Debian 13 / MariaDB 11.8.6 | Passed | Actual existing-state cleanup and seeded-fixture runs succeeded through Make op.mariadb. Seeded cleanup reported changed=1 on each. SQL queries verified zero anonymous/remote-root accounts, zero test schemas and zero matching mysql.db rows. The retained account lost test-prefix access while keeping its own database access and authentication definition. Data in test_keep, securekeep and archappl survived; the global SQL mode, service PID, config metadata and existing profiles matched. Quote/backslash account host names were deleted under NO_BACKSLASH_ESCAPES. After fixture cleanup, the final run reported ok=4 changed=0 failed=0 on each, with root UDS authentication and no TCP listener verified. |
| T15 | 2026-09-16T15:57:43Z | Rocky 8.10 / MariaDB 10.3.39 and Debian 13 / MariaDB 11.8.6 | Passed | The shipped raw_stdin action received public multiline input through SSH/sudo; the receiving root shell had no TTY and no marker in its command arguments. Exit 23 propagated, missing no_log failed, and check mode skipped both valid commands. The role rendered with the credential value only in stdin. Real Make runs created separate accounts and passed the 21-check lifecycle and 8-check security regressions; final operator reapply reported ok=5 changed=0 failed=0 on both. No remote credential-visibility experiment was used. |
| T16 | 2026-09-16T15:56:03Z | Same two VMs | Passed | X509, SSL, CIPHER, ISSUER and SUBJECT conditions failed visibly on both servers before the account task. Explicit expiration and account lock tests ran on MariaDB 11.8 and failed as expected; MariaDB 10.3 rejected the PASSWORD EXPIRE fixture setup syntax. Account/grant definitions were unchanged after rejection. Restoring each fixture condition restored data access; the final custom-account reapply reported changed=0 on both, and fixture accounts/databases were removed. |
| T17 | 2026-09-23T09:05:24Z | The current three archiver-dev hosts (Rocky 8.10 x2, Debian 13): T17's original third host, and two hosts rebuilt through this operator on 2026-09-21 after the original run; all three installed at epicsarchiverap-env `6a026d4` since 2026-09-22 | Failed | The build half holds, observed 2026-09-21T06:23:08Z: our `archiver_build` operator ran `init`, `db.conf`, `conf.archapplproperties` and `build.mvn` as root on the original three hosts, and the als classpathfiles are packed as required: `appliances.xml`, `archappl.properties` and `policies.py` are each present in `WEB-INF/classes` of all four deployed webapps, generated into `site-template/siteid/classpathfiles` by `copy.sitespecific` within `build.mvn`. The two proxy defects in the increment status below - the detached unit carrying no proxy, and Maven not reading one from the environment - blocked that run first and had to be fixed. The schema half fails: `sql.fill` loaded nothing on any host. The 2026-09-21 result counted the load as executed because `sql.fill` exited 0 under `set -e`, but the exit status does not show the load. Inspected on the current three hosts: the configuration database exists and holds zero tables (`information_schema.tables` count 0); mgmt on every host logs `Table 'archappl.PVTypeInfo' doesn't exist` at each start, when it loads PV configuration from the database (`Loading PVTypeInfo from persistence`), and on the host where PVs were registered it logs the same error, and the same for `PVAliases`, on each registration. Cause, read from epicsarchiverap-env's scripts: `query_from_sql_file` first checks the database through `isDb`, which logs in as the admin account (`DB_ADMIN`, default `admin`) that this mode never creates, so the check reports the database absent; the not-found path prints `There is no >> archappl << in the dababase` beside the MariaDB `Access denied for user 'admin'` error - both lines stand in every build log - and then ends in a bare `exit`, which returns 0. The operator now counts the tables right after `sql.fill` and stops when there are none or the count cannot be read (fifth defect in the increment status below). |
| T17 | 2026-09-23T22:10:06Z | A Rocky 8.10 and a Debian 13 archiver-dev host rebuilt through this operator (`a3f9949`) at epicsarchiverap-env `1fc20a8` with `archiver_force_reinstall=true`; both hosts were removed afterwards | Passed | Observed between 22:07:52Z and 22:10:06Z on both hosts: the install stamp carries `envref=1fc20a8`; `CONFIG_SITE.local` carries `MAVEN_FLAGS:=-gs /etc/maven-proxy-settings.xml`, and the build log shows its use and `BUILD SUCCESS`; the four WARs carry the als classpathfiles; `sql.fill` loaded the schema and the operator's table check let the build continue, its first run inside a build; `make sql.show` lists `ArchivePVRequests`, `ExternalDataServers`, `PVAliases` and `PVTypeInfo`; mgmt answers 200, epicsarchiverap-env's health service and timer are installed, and mgmt logs no persistence error. The host then carrying the soak, now the pilot host, stayed at `6a026d4` with an empty configuration database; T17 there was the remaining check (owner decision 2026-09-23). |
| T17 | 2026-09-24T09:15:13Z | The soak host: a fresh Rocky 8.10 archiver-dev VM, the full species applied from `dca2255` at epicsarchiverap-env `9eed006` with the README test store values | Passed | The apply ran 08:49:29Z-09:08:21Z with `failed=0`. The install stamp carries `envref=9eed006` and the store values; `CONFIG_SITE.local` carries `MAVEN_FLAGS` and the five store lines; the installed `policies.py` and the copy packed into the mgmt webapp carry `PARTITION_5MIN` hold 2, `PARTITION_HOUR` hold 2 and `PARTITION_DAY`; the build log shows the settings file and `BUILD SUCCESS`; the database holds the four tables; all four JVMs run `-Xms256M -Xmx256M`; the health service and timer are installed; mgmt answered 200 at 09:09:03Z once initialised and logs no missing-table error. After 100 PVs were registered, `PVTypeInfo` held 100 rows at 09:15:13Z. This settles the remaining check the 2026-09-23 row named, on a new host instead of the old one (owner decision 2026-09-24). |
| T20 | 2026-09-25T09:27:24Z | The soak host (Rocky 8.10, 2 vCPU, 3.6 GiB) at operator `dca2255`, epicsarchiverap-env `9eed006` and the README test store values; 100 PVs registered at 2026-09-24T09:09:52Z | Passed | Over 23.9 h of 5-minute samples: the installed `policies.py` carries the test values and T17 passed on this host (row above); STS held all 100 PVs at 09:15Z, MTS at 09:30Z and LTS at 12:15Z, and the second LTS day partition existed for all 100 by 03:15Z on 2026-09-25, about 3 h 15 min after midnight; the unit stayed active with four instances, mgmt 200 and health success in every sample, one PID per JVM all day and kernel OOM 0; retrieval returned the full sample count in every window after the first. The appliance was restarted at 09:25:03Z on 2026-09-25, about 9 h 25 min after midnight: four new JVMs, mgmt 200 at 09:26:01Z, `PVTypeInfo` still 100 rows and all 100 PVs Being archived again, no missing-table error; archiving paused 55 s for the 1 Hz, 10 Hz and waveform PVs and 60 s for a 0.1 Hz PV. Resources: CPU idle mean 96%, MemAvailable 1.23-1.50 GB, no swap; JVM RSS 374-500 MiB each, heap used at most 241 MiB of 256M (etl), full GC 0; `/arch` 3.60 GB, of which LTS 3.11 GB (a 1000-element waveform about 0.69 GB per day, a 1 Hz scalar about 1.9 MB). Logs: the four logs directories together about 480 KB/h; mgmt `catalina.out` 151 KB/h, engine `catalina.out` 133 KB/h plus its dated JULI file 126 KB/h (CA client beacon and duplicate-response records), retrieval 52 KB/h, etl none after startup; ERROR 3, all during mgmt initialisation, and Exception 0. |
| T21 | 2026-09-26T19:25:06Z | The soak host after T20, heap 256M, 100 day-1 PVs plus 400 1 Hz scalars from 09:46Z on 2026-09-25 (step 1) and 300 1 Hz scalars, 100 10 Hz VeryFast scalars and three waveforms from 15:46Z (step 2, 903 PVs); four retrieval clients 21:46Z-21:56Z (client lost to the kernel OOM killer, its own fault: whole responses buffered) and again 08:30Z-14:30Z on 2026-09-26 with a streaming client; load held to 18:55Z; end events 18:57Z and 19:00-19:10Z | Passed | No step lost an instance or mgmt: 404 samples with four instances, mgmt 200 (max 12 ms) and health success; the only kernel OOM kill was the first retrieval client. Every PV of both steps reached STS, MTS and LTS (step 2 in LTS by 18:55Z). No limit was reached; the run was ended with the root disk 91% full (`/arch` 3.7 to 12.9 GB, about 0.3 GB/h at 903 PVs). The "Approximate time taken by last job in ETL(0>1)" figure rose about 9 s per hour to 277 s at 18:50Z, but it is a running sum of per-PV durations that resets only after 15 minutes without an update, which a 5-minute partition never gives; "Average time spent in ETL(0>1) (s/run)" is that sum over the run count (401 runs, 0.69 s at 18:50Z), a lifetime average. The sum's growth per run gives the time of each pass: 0.43 s in step 1 (500 PVs), 0.68 s and then 1.03 s in step 2 (903 PVs, 15:45Z-18:50Z and 18:50Z-21:45Z sample times), 0.73 s overnight, 0.78 s under the 6 h retrieval load and 0.69 s in the final hold; estimated weekly usage 0.18%. Read at first as ETL nearing the 300 s partition period, it is not a slowdown (correction 2026-09-27). Resources: CPU idle 90-95%; MemAvailable 1231 down to 1003 MiB over the run (JVM RSS 403 to 492 MiB mgmt, 374 to 449 engine, 375 to 431 etl, 377 to 422 retrieval); heap used peaked at 251 MiB of 256M on etl (10 full GCs, none on the others) and 227 on engine. Retrieval load: 42417 requests in 6 h, all 200, median 31 ms, p99 98 ms, max 479 ms, 156 GB served; the 10-minute first attempt got 1163 of 1167 answered (median 29 ms) until the client died; the four failures were one-day waveform requests that ended after about 6 s without a response, cause not isolated. Log growth: mgmt `catalina.out` about 140 KB/h and 800 lines/h at every step; engine 131 KB/h in step 1, 57 in step 2, 25 held, but 2.9 MB/h (21000 lines/h) under retrieval load; retrieval 54 KB/h idle and 12.8 MB/h (58000 lines/h, about 8 lines per request) under retrieval load; etl 2 KB/h. End events: the day-1 IOC restart (18:57:06Z) added about 30 engine application lines and 23 JULI lines with no ERROR; the MTS tree made unwritable for 10 min (19:00:11-19:10:11Z) made etl log 2709 "Exception processing" records with stack traces, 10836 lines and 5 MB, peaking at 1616 lines in one minute, STS files rose 3602 to 5410, and after the restore ETL cleared the backlog to 898 files within 15 min. |
| T18 | 2026-09-21T15:33:55Z | Same three hosts | Passed | The root install steps ran and the appliance serves. On all three hosts: the four instances are installed under `/opt/epicsarchiverap-maven` and listen on 17665 mgmt, 17666 engine, 17667 etl and 17668 retrieval, `epicsarchiverap-maven.service` is enabled and active, `/arch` (0755), the install root and all four instance directories are owned `mid-srv:mid`, the appliance processes run as the `mid-srv` service account and not as root (so the build-as-root, run-as-service-account split is now observed rather than derived), and mgmt `/mgmt/bpl/getApplianceInfo` returns HTTP 200 with identity `appliance0` and version 2025-6. A PV archives and reads back (verified on the freshly provisioned host): a 1 Hz calc record submitted through `mgmt/bpl/archivePV` moved `Initial sampling` to `Appliance assigned` to `Being archived`; `retrieval/data/getData.json` then returned 68 points carrying the record `EGU`, the leading samples one second apart and incrementing; and the short-term store held the PV under `/arch/sts/ArchiverStore/` as `<segment before the colon>/<remainder>:<YYYY_MM_DD_HH>.pb`, the hour bucket in UTC because the appliance stores in UTC - the 15:33Z run produced the `_15` bucket and the first sample carried epoch 1790004766, which is 15:32:46Z. The test IOC and the PV were removed afterwards. Timing note for any future probe: mgmt answers 500 for roughly 20-30 s after a start, so a single-shot check misreads as failure. |
| T19 | 2026-09-21T08:07:09Z | Rocky 8.10 and Debian 13 archiver-dev VMs | Passed | Re-apply reports `changed=0 failed=0` on both, with the launch step reporting all four instances live, and the installed state is unchanged across it: the install-tree fingerprint (file list and sizes, excluding `logs`, `temp` and `work`), all four per-instance JVM PIDs, and the unit `ActiveEnterTimestamp` were captured before and after and are identical on both hosts. The result is only trustworthy because of a defect found while producing it: an earlier re-apply reported `changed=0` while one host had a dead mgmt instance, because the check trusted `systemctl is-active` on a unit that stays active when one of its four Tomcat instances dies. The check now judges the four instances themselves and repairs with `restart`; verified by killing an instance and observing `changed=1` naming the missing instance, against a healthy control host reporting `changed=0`. |

MariaDB loopback-TCP verification (2026-09-18, Rocky 8.10 / MariaDB 10.3.39 and
Debian 13 / MariaDB 11.8.6 archiver-dev VMs): the `mariadb` operator applied with
`mariadb_skip_networking: false` on both. `@@skip_name_resolve=1`; a
`--protocol=tcp` login to 127.0.0.1 authenticates as `archappl@'127.0.0.1'`; the
listener is `127.0.0.1:3306` only (no `::1`); `root@'127.0.0.1'` and `root@'::1'`
are dropped, so root over TCP returns Access denied; the application grant is
`archappl.*` only. Re-apply reported `changed=0`. Verified role committed
`5b5ee44`; reviewed third- and second-person to convergence. The `[archiver_dev]`
group_vars resolution (`mariadb_skip_networking=False` for an `[archiver_dev]`
host, unset elsewhere) verified via `ansible-inventory --host`; committed
`08dbb93`.

archiver_build increment status (2026-09-20, Rocky 8.10 and Debian 13 archiver-dev
VMs and a third, freshly provisioned Rocky 8.10 host): the operator, its playbook
and the `archiver_dev` species are written, registered and have now run every step
of the make sequence (`575b3f4`). The per-step
privilege split and the ordered make sequence are no longer derived from epicsarchiverap-env's
Makefiles - both were executed and observed (T17, T18). Four defects surfaced in
that first end-to-end run and are resolved in the role, a fifth was found
later on the current hosts, two of them rebuilt after that run, and a sixth came
with the fix for the fifth:

- A detached `systemd-run` unit inherits no `/etc/profile.d`, so the build carried
  no proxy and could not fetch Maven. The build script now sources the proxy
  contract profile itself. The systemd-level equivalent is open on cloud-provision's
  side, so this stays until that is settled.
- Maven takes a proxy only from a settings file. Measured against the pinned
  epicsarchiverap-maven source with Maven 3.9.16: the shell proxy variables, `mvn
  -Dhttps.proxyHost`, and `MAVEN_OPTS` carried as JVM startup arguments each leave
  Maven Central unreachable, while a settings file selected with `-gs` resolves.
  That file belongs to the cloud-provision proxy contract (`0099673`); this
  operator consumes it and generates none, and a proxied host without it is
  refused before the build starts rather than failing inside mvn.
- Four appliance instances at epicsarchiverap-env's default 1G heap each oversubscribe a 4 GB
  vacuum, and the OOM killer takes one down: under 1G the Rocky host lost an
  instance about 2 h 50 min after install and the Debian host about 4 h.
  `archiver_java_heapsize` (default 256M) overrides `AA_JAVA_HEAPSIZE`. Available
  memory rose from about 0.5 GB to about 1.6 GB, and under 256M the two hosts had
  run 3 h 59 min and 4 h 30 min with zero kernel OOM events and all four instances
  alive as of 2026-09-21 01:07 PDT - each past the interval at which it previously
  failed. The freshly provisioned host stood at 1 h 45 min, also clean. Recheck by
  comparing the unit `ActiveEnterTimestamp` against the clock and counting kernel
  OOM with
  `journalctl -k`: a plain journal grep also matches this role's own comment text
  as echoed by sudo, which reads as phantom OOM events.
- The installed-and-active check trusted the systemd unit, which stays active when
  one of its four Tomcat instances dies, so a degraded appliance reported no
  change. It now judges the four instances and repairs with `restart` (T19).
- The schema load did not happen on any of the three hosts, and the operator
  took `sql.fill`'s exit status as proof that it had (found 2026-09-23; T17 then
  Failed at `6a026d4`). epicsarchiverap-env's `sql.fill` checked the database through the admin account
  before loading, and in this mode no admin account exists: the separate admin
  workflow is left to epicsarchiverap-env (MariaDB design above), while epicsarchiverap-env's own install
  guide runs only `sql.fill` against an externally provisioned database. The
  check printed the access error and a not-found message, both present in every
  build log, but exited 0; the operator read only the exit status, so every
  appliance ran on an empty configuration database. Every appliance served its
  management endpoint, and on the host where PVs were registered it archived,
  moved data through ETL and served retrieval, which is why every other check
  passed; PV configuration was never written. mgmt reads PV configuration from
  the database at every start, and on all three hosts that read failed on the
  missing table, so PVs registered since the last start would not have been
  reloaded by the next one (the restart itself not observed). The operator now counts
  the database's tables right after `sql.fill` and stops before install when
  the count is 0 or cannot be read. The query was run against the live empty
  database (0, stop) and a populated one (31, pass); inside a build the check
  first ran in the T17 re-run at `1fc20a8`, where the schema loaded and the
  check passed. epicsarchiverap-env fixed `sql.fill` in `1fc20a8`
  (jeonghanlee/epicsarchiverap-env#47).
- From `31b4424` to `a3f9949` the role did not load at all. An apostrophe
  inside a word in the build script, in one message (from `31b4424`) and one
  comment (from `29fb7e0`), left an unbalanced quote, and Ansible splits `raw` arguments on quotes, so every play
  using the operator failed before running a task (found 2026-09-23 when the
  T17 re-run started; fixed in `a3f9949`). Verified by a quote-splitting scan
  over every `raw` task and `--syntax-check`, both failing on the unfixed
  commit and passing on the fix.

A changed knob does not reach an already-installed appliance, so the operator
records a config stamp at install time, reports drift against it, and rebuilds
only under `archiver_force_reinstall`. Contract-file delivery and consumption are
both verified on the freshly provisioned host: the file arrives at first boot, the
build logs its use of it, no local file is generated, and Maven resolved from
central with no unreachable errors. Install, service account, serving endpoint,
unchanged re-apply and an archived PV read back were observed at earlier refs,
and the schema load is observed at `1fc20a8` on two rebuilt hosts (T17 re-run)
and at `9eed006` on the soak host, where PV configuration is written to the
database and survives an appliance restart (T20). The pilot host ran on an empty
configuration database at `6a026d4` until it was removed on 2026-09-25; its
first MTS to LTS move under the MTS `PARTITION_DAY` hold 2 and LTS
`PARTITION_YEAR` policy came between 06:45Z and 09:15Z that day, and the
restart that would have shown its PV configuration lost was not run.

Pinned epicsarchiverap-env ref moved to `e06c554` (2026-09-21). `fb43522` is its ancestor, and
nothing under `site-template/`, `scripts/`, `configure/CONFIG_SITE` or
`configure/CONFIG_SRC` differs between the two, so every override this operator
writes carries across unchanged; what did change is the build recipe, which now
passes `-DskipTests` (only the flag is observable here; epicsarchiverap-env reports the tests
moved to epicsarchiverap-maven CI), and `debian13.pkgs`,
which drops the four python packages. Verified by execution on the freshly
provisioned host: a plain re-apply was refused with the drift report naming
`envref` as the single differing field, leaving the appliance running untouched,
and a forced reinstall then rebuilt at `e06c554` in about a minute with
`failed=0`, leaving four instances, the unit active, heap `Xmx256M`, the als
classpathfiles in the webapp and mgmt answering 200 on the first probe. This was
the first exercise of drift detection against a real knob change rather than a
synthetic one. The two older hosts stayed installed at `fb43522` and could not be
moved in place, until they were recreated through cloud-provision later on
2026-09-21: a forced rebuild on them is refused before anything is torn down,
because the contract Maven settings file arrives only at provisioning and they
predate it. Recreating the VM is the route, through cloud-provision's `bin/create_vm.bash`,
and a host created now carries that file. Verified by running exactly that forced rebuild on both: it reported
`failed=1 changed=0`, the refusal naming the missing settings file, and left both
appliances serving at the old ref with four instances each.

Pinned epicsarchiverap-env ref moved to `6a026d4` (2026-09-22, `247f350`). It is seven commits
ahead of `e06c554`, and its one policy change sets the MTS store to
`PARTITION_DAY` (from `PARTITION_MONTH`, `hold=2` unchanged). All three current
archiver-dev hosts were force-reinstalled at `6a026d4` around 2026-09-22T00:29Z,
as their install stamps and JVM start times show; every observation after that,
including the T17 schema inspection, comes from that ref.

Pinned epicsarchiverap-env ref moved to `1fc20a8` (2026-09-23). It is twelve commits ahead of
`6a026d4` and carries the `sql.fill` fix (G3), a 256M heap default, a systemd
health timer for missing instances and the removal of the jsvc path. It also
renames epicsarchiverap-env's Maven flag hook from `MAVEN_OPTS` to `MAVEN_FLAGS` (`84b38e5`),
so the operator now writes `MAVEN_FLAGS` and needs `84b38e5` or later. Two hosts
were rebuilt at `1fc20a8` with `archiver_force_reinstall=true` on 2026-09-23 for
the T17 re-run and then removed; the pilot host stayed installed at `6a026d4`
until it was removed on 2026-09-25.

Pinned epicsarchiverap-env ref moved to `9eed006` (2026-09-24). It is nine commits ahead of
`1fc20a8` and renders the store granularity and hold of each tier from Make
variables (`ARCHAPPL_STS_GRANULARITY`, `ARCHAPPL_STS_HOLD`,
`ARCHAPPL_MTS_GRANULARITY`, `ARCHAPPL_MTS_HOLD`, `ARCHAPPL_LTS_GRANULARITY`;
jeonghanlee/epicsarchiverap-env#50). Their defaults are the previous values, so
an install that sets none keeps STS `PARTITION_HOUR` hold 2, MTS `PARTITION_DAY`
hold 2 and LTS `PARTITION_YEAR`. epicsarchiverap-env checks each name and hold in
`conf.policies` but leaves the order across tiers to the caller. The operator
exposes the five as `archiver_store_*`, writes only those that are set, and
refuses a partial, unknown, out-of-order or non-positive set before a build
starts. The rest of the range makes the database backup, listing and restore
exit non-zero on failure, paths this operator does not call. The config stamp
now carries the store values, so every installed host reports drift on its next
plain re-apply and moves only with `archiver_force_reinstall=true`. Verified
before any host run: the rendered launch step accepts the empty, full and
hold-only sets and refuses eight malformed ones before stopping anything; fed
the `CONFIG_SITE.local` lines the rendered build step writes, epicsarchiverap-env `9eed006`'s
own `make conf.policies` renders the test values into both the classpath copy
packed into the WARs and the copy `make install` installs. The soak host was
installed at `9eed006` on 2026-09-24 (T17, T20).

Generator gap closed (2026-09-18, cloud-provision `m11-middleware-operators`
`06ea800`): `generate_ansible_inventory.bash` now emits `[archiver_dev]` and
`[archiver]` for the archiver species pair (tests 197/197), so a real provision
attaches the `archiver_dev` group_vars with no change on our side; re-sync the
local cloud-provision checkout before provisioning. The generator still lacks
`phoebus`, `phoebus-dev`, `middleware`, and `iocserver` - the same one-line
addition when those are provisioned.

Java increment observation (2026-09-15, control host): the standalone role,
operator playbook, and `op.java` target are implemented in the working tree.
The real operator passes Ansible `--syntax-check`; its default-rendered raw
body passes `sh -n`, `bash -n`, and `shellcheck -s sh`. The raw single-quote
count is even. `make -n op.java.rocky8` resolves the operator playbook and
Rocky 8 limit. Ansible `--check` with a local inventory exits 0 and skips the
raw task; this is not installation or idempotency evidence. `git diff --check`
passes. The complete M14/T1 and M14/T2 remain unrun.

M14/T3-T4 installation evidence: `roles/java/tasks/main.yml` SHA-256
`f7d20ca2606e136f16c1a7c0ba65387e93e66c4d2c8288aa9f6b8853337ce9b5`.
Recheck with `make op.java` using the two VM host entries as runtime inventory,
then inspect `java -version`, `javac -version`, `JAVA_HOME`, and
`/etc/profile.d/java.sh` in a new login shell. This verifies the Java increment;
the full `archiver-dev` assembly and EPICS application path were not run here.

Review correction verification (2026-09-15T15:11:36Z): the role now identifies
the missing or non-executable `java` or `javac` path under `JAVA_HOME`.
On both existing test VMs, the real `op.java` run with
`java_home=/nonexistent/review-jdk` returned rc 1 and named
`/nonexistent/review-jdk/bin/java` in its error. A subsequent default run
reported `ok=1 changed=0 failed=0` on each. Ansible syntax, raw quote parity,
shell syntax, and ShellCheck passed. The verified role SHA-256 is
`a5a331b8700c713421949ed9ad051402a567e70153632f6ee5aa600e7c6d677d`.
The architecture tree matches the 16 existing roles and omits the absent
legacy directories; the corrected directory description passed the maintainer
reader check. Both accepted review findings are resolved.

M14/T5-T7 verification basis: ansible-provision `b8cc658` with the EPICS
default changed to 1.3.0. The verified `roles/epics/defaults/main.yml` SHA-256
is `8e5af33f1ca769b714df61565335965531d88509d27a94c5f62101610b8e27cd`;
the unchanged task file SHA-256 is
`40cf24fdaccc673a8822f00a8f28ac683fb3824b88bed21562062f44f3fb9a36`.
Recheck using the T5-T7 methods above on the same OS pair. This covers the
EPICS distribution operator and a shipped example consumer; full middleware
assembly checks T1-T2 remain unrun.

M14/T8-T9 verification basis: ansible-provision `dae8aef` with the initial
standalone Tomcat addition. The verified task SHA-256 is
`51706a8e53562c54ce30cbe67e256bd98f73460178b84dcccc6182ad9e73dfea`;
the defaults SHA-256 is
`f37485d6cd00990667a991f8a25d0d5b90a454f30e732696b7bae6e0519049f5`.
Ansible syntax, raw quote parity, rendered `sh -n` / `bash -n`, ShellCheck,
Make target resolution, and the 17-role/operator inventory check passed.
Static safety, privileged path/ownership checks, and observed failure/preservation
behavior were inspected separately. Recheck with T8-T9 on the same OS pair;
the full Archiver Appliance assembly remains outside this increment.

M14/T10 verification basis: ansible-provision `dae8aef` with the corrected
Tomcat task SHA-256
`bcadb2b0d32239cc4d9e86b6aa7fd8516eaab6131cef7503202f52e50722d708`;
defaults remain at the T8-T9 SHA-256 above. The default-rendered raw task passed
`sh -n`, `bash -n`, and `shellcheck -s sh`; Ansible syntax-check passed.
Recheck with T10 on the same OS pair using separate root-owned installation
parents with mode `0755`; run the installed scripts as an ordinary user with
explicit `CATALINA_HOME` and `CATALINA_BASE` for each test installation.

M14/T11-T13 verification basis: ansible-provision `6c81884` with the standalone
MariaDB addition. The final task SHA-256 is
`3baaac945cea28907d4786b5151d8fa08696cbcb7b12e760d63dd24c3cbeacc9`;
the defaults SHA-256 is
`516d8af8a57286d95b24c1921cf37ced16af1d800d152aeb289be84aaacf4019`.
Ansible syntax, rendered `sh -n` / `bash -n`, ShellCheck, raw quote parity,
Make target resolution, and the 18-role/operator inventory check passed.
Recheck T11-T13 with private test credentials using the real `op.mariadb`
target and the distribution SQL client on both OS families. The server and
local client path are verified; the AA JDBC path, schema and full
`archiver-dev` assembly remain unverified until epicsarchiverap-env and epicsarchiverap-maven integration.

M14/T14 verification basis: the security task extends the T11-T13 operator;
its verified task-file SHA-256 is
`3c134d0e2a331388ddb2a88fbd226d69d725b4be2038c99e0216e48aa8433709`.
The distribution secure-installation scripts on both OS families supplied the
account and default test-grant scope. Account deletion uses DROP USER across
MariaDB versions instead of writing mysql.user/mysql.global_priv directly.
Ansible syntax, shell syntax, ShellCheck and quote parity passed for all five
raw tasks. Recheck using T14 with disposable test accounts and databases on
both OS families; this procedure intentionally deletes the test database.


M14/T15-T16 verification basis: the accepted review corrections extend the
T14 operator. The task-file SHA-256 is
`e7a8cf60550d5abac8dbbd1c9a48b2082ffbe9e97dc5e780c2cfba7641234fd9`;
`action_plugins/raw_stdin.py` is
`b517b5fb2a95e57afd5c22544cb512db1ad93c73f5e6a7f34416bab7e4891ebd`.
All six role shell blocks passed sh/bash syntax and ShellCheck; YAML, Python,
Ansible syntax and raw quote-parity checks passed. Recheck the transport with
`tests/check-raw-stdin.yml` as described in RAW_STYLE.md, and the account policy
through T16 using private test credentials and separate disposable accounts.
The transport test uses public data, not a scan exposing database credentials.
The AA JDBC path, schema and full archiver-dev assembly remain outside these
operator checks.


#### M15 - Discipline lab-VM clocks from the KVM PTP clock in the common operator

- Origin: 38560eb / M15
- Status: Complete

##### Summary

Lab VMs never reach NTP synchronization: the `common` operator points chrony at
the site pools (`ntp_servers`), which are public pools the lab network cannot
reach behind the site proxy (no UDP 123 egress). kvm-clock keeps the guest clock
close, so builds work, but `timedatectl` reports the clock unsynchronized, and
one Debian apply through the `epics_dev` species failed its first task that
reaches the network, `common : Update apt cache` (`apt update` rc 100, a
security suite signature "created after the --not-after date"), then passed on
a re-run. A KVM guest exposes the host clock as a PTP hardware clock
(`ptp_kvm`), which chrony can use as a reference clock without any network.

##### Scope

`roles/common`: load `ptp_kvm` and persist it in `/etc/modules-load.d`; a udev
rule that links `/dev/ptp_kvm` only for the device whose `clock_name` is
`KVM virtual PTP`; in the chrony configuration the operator writes, a
`refclock PHC /dev/ptp_kvm poll 2` line when that device exists at apply time,
beside the existing pools and directives; chrony restarted through the existing
handler when the configuration changes. On the Debian path, the first
`apt update` retries a bounded number of times when its output shows a
signature-date failure. A switch, default on, turns the PTP refclock off for a
site that does not want it.

Out of scope: cloud-init and image changes (cloud-provision reverted its
templates); replacing the site pools or their `minpoll`/`maxpoll`, keyfile and
leapsectz directives; disabling the signature date check; hosts that are not
KVM guests beyond confirming they are unaffected.

##### Completion Criteria

- On fresh Rocky 8.10 and Debian 13 KVM guests, after the `common` operator:
  `/dev/ptp_kvm` exists, `chronyc sources` shows PHC0 selected, and
  `timedatectl` reports the clock synchronized.
- The written chrony configuration still carries the site pools and the other
  directives unchanged; a re-apply reports no change.
- Where `/dev/ptp_kvm` does not exist, the configuration carries no refclock
  line and chrony starts and serves from the pools.
- The Debian `apt update` retry fires only on a signature-date failure; any
  other failure fails at once.

##### Dependencies And Decisions

- `D17` (owner, 2026-09-25). Recipe verified by cloud-provision on a fresh
  Rocky 8 VM (PHC0 selected, stratum 1, `timedatectl` synchronized); the failing
  stage reported by the EPICS-env session and relayed by cloud-provision.
- Verification needs fresh Rocky 8.10 and Debian 13 VMs from cloud-provision.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-25
- Implementation Authorization: 2026-09-25
- Superseded Plan Artifacts: none

1. `roles/common/tasks/main.yml`, before the chrony configuration task: write
   `/etc/modules-load.d/ptp_kvm.conf` and
   `/etc/udev/rules.d/99-ptp-kvm.rules`
   (`SUBSYSTEM=="ptp", ATTR{clock_name}=="KVM virtual PTP", SYMLINK+="ptp_kvm"`),
   load the module (`modprobe ptp_kvm`, tolerated where it does not exist),
   and trigger udev so the link exists before chrony is configured. Guarded by
   a new `chrony_ptp_kvm` default `true`.
2. The chrony configuration task appends the refclock line only when
   `/dev/ptp_kvm` exists, so a host without the device keeps the current file
   and chrony never meets a missing device.
3. `roles/common/tasks/debian.yml`: `Update apt cache` retries up to 3 times,
   20 s apart, only when the output shows a signature-date failure ("not valid
   yet", "created after", or the sqv wording "Not live until"); other failures
   fail at once.
4. Restart chrony with the new configuration before waiting (flush the restart
   handler, or restart in that step, since a handler otherwise runs only at the
   end of the play), then wait for synchronization with `chronyc waitsync`
   under a bound of about 60 s and report, without failing, when it does not
   converge.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | `--syntax-check` on the species using `common`; the Ansible splitter over every `raw` task; render the chrony task with the device present and absent | control host | Syntax passes; no split failure; the refclock line appears only when the device exists |
| T2 | Integration | Apply `op.common` on fresh KVM guests; inspect `/dev/ptp_kvm`, `chronyc sources`, `chronyc tracking`, `timedatectl`, and the written chrony configuration | Fresh Rocky 8.10 and Debian 13 VMs | PHC0 selected, synchronized; pools and directives unchanged |
| T3 | Integration | Re-apply `op.common`; compare the chrony configuration, module and udev files; reboot and inspect `/dev/ptp_kvm`, `chronyc sources` and `timedatectl` again (the chrony unit carries no ordering after udev); then block the module with a temporary modprobe rule, unload it, remove the link and apply again, and finally lift the block and apply once more (a removed link alone comes back, since every apply loads the module and replays udev) | Same VMs | Re-apply reports no change; after the reboot the link exists, PHC0 is selected and the clock is synchronized; without the device no refclock line is written and chrony serves from the pools |
| T4 | Integration | Run the Debian `Update apt cache` task three ways: with time synchronization stopped and the clock set behind the suite signature time; with the clock correct; and with an unrelated repository error (a source naming a suite the Debian mirror does not carry, which apt reports as an error; an unresolvable host yields only a warning and exit 0) | Debian 13 VM | Clock behind: three retries, then a failure naming the signature date; clock correct: passes on the first attempt; unrelated error: fails at once with no retry |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-25T17:13Z | control host | Passed | `--syntax-check` passes for the `common` operator and the `epics_dev`, `iocserver` and `archiver_dev` species; the Ansible splitter accepts all 76 `raw` tasks. Rendered with the defaults, every new task passes `bash -n`; the chrony task carries the refclock step with `chrony_ptp_kvm` true and not with it false. Whether the device exists is decided on the host, so that branch is left to T2 and T3. The rendered `Update apt cache` script, run with only `apt` and `sleep` replaced: a "not valid yet" and a "created after" failure each run 4 attempts (3 logged retries) and exit 100; an unrelated fetch failure exits 100 after 1 attempt; success exits 0 after 1 attempt. The first run exposed an exit-status capture that turned every failure into 0; fixed before this result. After review added a task that reports a clock that did not converge (the wait prints only under `-v`), rechecked at 17:58Z: splitter 76/76 and syntax pass; the report task, run with each registered wait outcome, shows the message only for "did not report synchronization" and skips on synchronized, no device and a skipped (check mode) wait; a re-apply on the Rocky VM reported `changed=0` with the report skipped. |
| T2 | 2026-09-25T17:38:52Z | Fresh bare Rocky 8.10 and Debian 13 KVM guests from cloud-provision | Passed | `make op.common.rocky8` 17:25:49Z and `op.common.debian13` 17:36:37Z, both `failed=0`; the restart handler ran before the wait task. On both: `/dev/ptp_kvm -> ptp0`, `clock_name` "KVM virtual PTP", the module and udev files as planned; `chronyc sources` selects PHC0 (`#*`, reach 377, offset within 5 ns), `chronyc tracking` reference PHC0 at stratum 1, `timedatectl` "System clock synchronized: yes"; the written configuration keeps the pool, driftfile, makestep, rtcsync and logdir lines and adds `refclock PHC /dev/ptp_kvm poll 2`. The pool servers stay unreachable (`^?`). On Debian chrony replaced systemd-timesyncd (inactive) and answers as `chronyd` and `chrony`. |
| T3 | 2026-09-25T17:43Z | Same two VMs | Passed | Re-apply (`op.common` again) reported `changed=0` on both, and the chrony configuration, module and udev files kept their sha256 and mtime. After a reboot (17:40Z) both came up with `/dev/ptp_kvm` linked, chrony 4.5 (Rocky) and 4.6.1 (Debian) logged "Selected source PHC0" with no refclock error, PHC0 selected and the clock synchronized. With the module blocked by a temporary modprobe rule, unloaded and the link removed, an apply rewrote the chrony configuration without the refclock line and restarted chrony, which stayed active on the pools alone (unreachable in the lab, so unsynchronized, as expected there). With the block lifted, the next apply restored the link, the refclock line, PHC0 and synchronization. |
| T4 | 2026-09-25T17:47:28Z | The Debian 13 VM | Passed | Each case through `make op.common.debian13` with `-v`. Clock behind: with chrony stopped, `/var/lib/apt/lists` emptied and the clock set two days back, `apt update` failed on every suite with the sqv message "Not live until"; the task ran 4 attempts with 3 logged retries and failed with rc 100. Clock correct: the task passed on its first attempt (twice, before and after the clock case). Unrelated error: a source naming a suite the mirror does not carry gave a 404 and "does not have a Release file"; the task failed with rc 100 after one attempt, no retry. Two facts found on the way: with index files already present, a clock two days behind makes apt warn, keep the previous index and exit 0, so the reported rc 100 needs an empty list directory as on a fresh VM; and the sqv wording "Not live until" was missing from the retry pattern, added before this result. |

##### Closure Evidence

- Delivered in `57d9d3f` (the KVM PTP refclock, the sync wait and its report)
  and `eb9ba56` (the Debian first `apt update` retry); the work and its
  verification were recorded in `ea436ca`.
- Landed: after a fetch at 2026-09-25T18:56:23Z, `origin/m14-middleware-reconcile`
  stood at `ea436ca`, which contains both commits; the branch is not yet merged
  to `master`.
- T1-T4 Passed on 2026-09-25 against every completion criterion.


#### M16 - Generate the MariaDB application password on the host

- Origin: 38560eb / M16
- GitHub Issue: #26, https://github.com/jeonghanlee/ansible-provision/issues/26
- Status: Complete

##### Summary

The `mariadb` operator takes the application account credential as a
`mysql_native_password` hash in private variables on the control host and
carries it to the target through `action_plugins/raw_stdin.py`, so that no
target Python is needed and the hash never appears in a command line. That
design brought the plugin, its SSH-only guard, the `no_log` rules and the T15
and T16 checks, and it fails on a host that provisions itself over
`ansible_connection=local`. epicsarchiverap-env, by contrast, holds one plaintext
`DB_USER_PASS` and needs only that value at build time. Generating the
password on the host and keeping it there removes the transfer and everything
built around it.

##### Scope

`roles/mariadb`: a root-only credential file (path from `mariadb_password_file`,
default `/etc/ansible-provision/mariadb-<user>.pass`, mode 0600, root owned)
created with a random password when absent and left alone when present; the
application account at `localhost` and, under loopback TCP, `127.0.0.1` set
from that file, with the SQL fed to the client from the running script rather
than from command arguments, and a change reported only when the stored
authentication differs. `roles/archiver_build`: read the file and write
`DB_USER_PASS` to `CONFIG_SITE.local`, and use it for the post-`sql.fill` table
check. Removal of `action_plugins/raw_stdin.py`, `tests/check-raw-stdin.yml`,
`mariadb_password_hash`, `archiver_db_password` and their documentation in
README, RAW_STYLE and ARCHITECTURE; documentation of the file, a site-supplied
password (place the file first) and rotation (remove the file, re-apply the
operator, force-reinstall the appliance).

Out of scope: the MariaDB root account (socket-authenticated, unchanged); the
account host-spec and grants (unchanged); epicsarchiverap-env's own `db.*` targets, which
the operator does not run; encrypting the file at rest (the installed
`context.xml` already carries the plaintext).

##### Completion Criteria

- On fresh Rocky 8.10 and Debian 13 hosts, `op.mariadb` without any private
  variables creates the file (root, 0600) and the account, and a TCP login as
  the application account with the file's password succeeds; a re-apply reports
  no change; a file placed before the first apply is used as is; removing the
  file and re-applying sets a new password.
- The full `archiver_dev` species applied without private variables installs an
  appliance whose `sql.fill` loads the schema and whose mgmt persists PV
  configuration.
- `op.mariadb` passes over `ansible_connection=local` with password sudo kept
  warm, the case that failed before.
- `raw_stdin` and its test are gone; no remaining document names them or the
  hash variable.

##### Dependencies And Decisions

- `D18` (owner, 2026-09-25). Raised by the server-configuration session, which
  provisions a middleware host over a local connection and met the SSH-only
  guard in the account task; the epicsarchiverap-env contract needs only `DB_USER_PASS`.
- Supersedes the credential-transport checks recorded as M14/T15 and T16; those
  rows stay as history of the replaced design.
- Verification needs fresh Rocky 8.10 and Debian 13 VMs.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-26
- Implementation Authorization: 2026-09-26
- Superseded Plan Artifacts: none
- Plan revision (owner, 2026-09-27, from the second-person review of the
  documentation): step 2 also refuses to replace the password of an existing
  account when the file is missing, unless `mariadb_password_rotate` is set,
  so a host set up before the file existed is not cut off from its running
  appliance.

1. `roles/mariadb/defaults/main.yml`: add `mariadb_password_file` and
   `mariadb_password_rotate` (default false); drop `mariadb_password_hash`.
2. `roles/mariadb/tasks/main.yml`: replace the `raw_stdin` account task with a
   `raw` task that creates the directory when absent (root, 0700) and the
   file when absent (random password from `/dev/urandom`, root, 0600) unless
   the account already exists and `mariadb_password_rotate` is not set, in
   which case it stops with instructions; it then reads the file, and applies `CREATE USER ... IDENTIFIED BY`
   / `ALTER USER` for each host through the client's stdin from within the
   script, comparing `PASSWORD()` of the file against `mysql.user` first so a
   re-apply reports no change; keep the existing validation of names and the
   rejection of unsupported existing authentication conditions.
3. `roles/archiver_build`: a default `archiver_db_password_file` taken from
   `mariadb_password_file` the way `archiver_db_name` follows
   `mariadb_database`, so both roles name one path; read that file in the build
   script, write `DB_USER_PASS` unconditionally, use it in the table check;
   remove `archiver_db_password`; the stamp is unchanged.
4. Remove `action_plugins/raw_stdin.py` and `tests/check-raw-stdin.yml`; update
   README (mariadb and archiver sections), `docs/RAW_STYLE.md`,
   `docs/ARCHITECTURE.md` and `inventory/group_vars/archiver_dev.yml` comments.
5. Verify per the Test Plan; tell the server-configuration and epicsarchiverap-env sessions
   the landed shape.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | `--syntax-check` on the species using `mariadb`; the Ansible splitter over every `raw` task; grep for `raw_stdin` and `mariadb_password_hash` across the repository; render the account task | control host | Syntax passes; no split failure; no remaining reference; the rendered script carries no password literal |
| T2 | Integration | Apply `op.mariadb` without private variables on fresh hosts; inspect the file, `mysql.user`, a TCP login as the application account with the file's password; re-apply; place a file before a first apply on a third clean state; remove the file and re-apply without and then with `mariadb_password_rotate=true` | Fresh Rocky 8.10 and Debian 13 VMs | File root 0600 and account at both hosts; login succeeds; re-apply `changed=0`; a pre-placed password is used unchanged; a removed file beside an existing account is refused without rotation and yields a new password with it, the account following |
| T3 | Integration | Apply the full `archiver_dev` species without private variables on a fresh host; check `sql.fill`, the four tables, PV registration persisting to `PVTypeInfo` and mgmt logging no persistence error | Fresh Rocky 8.10 VM | The appliance builds, the schema loads, and a registered PV persists |
| T4 | Integration | On a VM, install `git`, clone the repository, run `make setup` for `ansible-core`, and apply `op.mariadb` to itself with `ansible_connection=local`, become through sudo with the credential kept warm and no become password given | Rocky 8.10 VM | The account task passes and T2's checks hold |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-26T00:48Z | control host | Passed | `--syntax-check` passes for the `mariadb` and `archiver_build` operators and the `archiver_dev` species; the Ansible splitter accepts all 77 `raw` tasks, including the account task that is now plain `raw` (its first draft used the shell length form `${#password}`, whose `{#` opens a Jinja comment and broke parsing; replaced by `wc -c`). No file outside this register names `raw_stdin`, `check-raw-stdin`, `mariadb_password_hash` or `archiver_db_password`. Rendered with the role defaults, the account task, the build script and the launch step pass `bash -n`, carry no password literal, and name the same file, `/etc/ansible-provision/mariadb-archappl.pass`. |
| T2 | 2026-09-27T03:31Z | Fresh bare Rocky 8.10 and Debian 13 VMs from cloud-provision | Passed | `make op.mariadb.<vacuum>` with no private variables. Rocky, socket-only first: `/etc/ansible-provision` root 0700, `mariadb-archappl.pass` root 0600 holding a generated 32-character password, account at `localhost`; re-apply `changed=0`. With `mariadb_skip_networking: false` from a vars file: the account gained `127.0.0.1` and a TCP login as `archappl` with the file's password returned `archappl@127.0.0.1`; re-apply `changed=0`. Rotation: removing the file and re-applying changed only the account task, the new 32-character password differs from the old, the new one logs in over TCP and the old one gets "Access denied". Debian: a site password (`Site-Pass.2026x`) written beforehand with mode 0644 was used as given and the file set to 0600; the socket-only and TCP applies and their re-applies behaved as on Rocky (TCP login `archappl@127.0.0.1`, re-apply `changed=0`). The validation task still refuses a non-boolean `mariadb_skip_networking` before any change (seen when the first run passed it as a string). After the plan revision, rechecked on the Rocky VM: with the file removed beside the existing account, an apply failed at the account task with the instruction message and changed nothing, and the old password still logged in; `-e mariadb_password_rotate=true` (a string on the command line, accepted through `| bool`; a first draft that demanded a true boolean refused it and was changed) regenerated the file, the stored hash changed, the old password got "Access denied" and the new one logged in; the next plain re-apply reported `changed=0`. |
| T3 | 2026-09-27T03:40Z | A fresh Rocky 8.10 archiver-dev VM from cloud-provision | Passed | `make archiver_dev.rocky8` with no private variables, 03:31:17Z-03:37:10Z, `failed=0`. The password file is root 0600; the generated `CONFIG_SITE.local` is 0600 and its one `DB_USER_PASS` line equals the file; the build log shows `BUILD SUCCESS` and no table-check refusal; the database holds `ArchivePVRequests`, `ExternalDataServers`, `PVAliases` and `PVTypeInfo`; mgmt answers 200. A PV registered through `archivePV` was stored in `ArchivePVRequests`, and once a one-record IOC served it, `PVTypeInfo` held its row within 100 s; mgmt logged no missing-table or access-denied line. |
| T4 | 2026-09-27T03:32Z | The fresh bare Rocky 8.10 VM | Passed | The uncommitted working tree was copied to the VM (a clone of origin would have carried the old code), `make` and ansible-core 2.16.3 installed, and `make op.mariadb.rocky8` run on the VM against `localhost ansible_connection=local` with become through sudo and no become password given. With the password file removed first, the apply changed only the account task, recreated the file root 0600, and a TCP login with it returned `archappl@127.0.0.1`; the re-apply reported `changed=0`. Sudo is passwordless on this lab VM, unlike the production host with password sudo kept warm; the account task no longer takes any secret from the control host, so the sudo mode does not change its path. |

##### Closure Evidence

- Delivered in `3e89e33` (the password file and account in `mariadb`, the
  consumer in `archiver_build`, `raw_stdin` and its test removed, the
  documentation); results recorded in `1864a1e`. The `Closes #26` footer
  remains valid for later integration into `master`; #26 is already closed.
- Decision Date: 2026-09-30. The linked issue #26 remains Open until the
  verified implementation commit `3e89e33` reaches `master`, where its
  `Closes #26` footer will close the issue automatically. This is the explicit
  issue-closure exception while the feature branch remains unmerged; the code
  and T1-T4 verification are Complete.
- Decision Date: 2026-09-30. Manual issue closure supersedes the Open-state
  exception above. Issue #26 was closed as completed at
  2026-10-01T06:21:00Z after its body was reconciled and a completion comment
  citing `3e89e33` and `1864a1e` was posted. Default-branch integration remains
  separate. Recheck with `gh issue view 26 --repo jeonghanlee/ansible-provision
  --json state,closedAt,updatedAt`.
- Landed: after a fetch at 2026-09-27T05:59:01Z,
  `origin/m14-middleware-reconcile` stood at `1864a1e`, which contains
  `3e89e33`; the branch is not yet merged to `master`.
- T1-T4 Passed on 2026-09-26/27 against every completion criterion, T2 again
  after the plan revision that guards an existing account.

##### GitHub Projection

- Issue: #26, https://github.com/jeonghanlee/ansible-provision/issues/26
- Observed State: Closed; observed after manual closure at 2026-10-01T06:21:00Z.
- Labels: `enhancement`
- Milestone: `Backlog`
- Assignee: `jeonghanlee`
- GitHub Updated At: 2026-10-01T06:21:00Z
- Body: reconciled with the guarded rotation behavior, implemented change,
  acceptance results, verification summary, and separate default-branch
  integration on 2026-09-30.


#### M17 - Move the epicsarchiverap-env pin to the journald and log4j2 service model

- Origin: 38560eb / M17
- Status: Complete

##### Summary

The operator pins epicsarchiverap-env `9eed006` and epicsarchiverap-maven `3c96141d`. Since then epicsarchiverap-env
runs the four Tomcats in the foreground under one service (`Type=simple`,
`KillMode=mixed`, `Restart=no`, each instance through `systemd-cat` as
`archappl-<instance>`), writes no `catalina.out` or dated JULI file, routes
Tomcat and java.util.logging through log4j2, takes the application layout from
the WAR, adds `ARCHAPPL_ROOT_LOGGER_LEVEL` and a launcher `loglevel` command,
drops macOS, and selects the database backend (`bbe0968`). An epicsarchiverap-env ref past
`a707cf5` stops `make install` unless the epicsarchiverap-maven build ships the Tomcat log4j
jars (from `9bbd69bf`), and one past `1400ae7` needs epicsarchiverap-maven `67be91d7` or later.
Logs then go only to the journal, which on these hosts is volatile and unbounded
by any site setting.

##### Scope

`roles/archiver_build`: move `archiver_env_ref` to the epicsarchiverap-env head chosen at
plan time (at or past `bbe0968`) and `archiver_maven_src_tag` to an epicsarchiverap-maven ref
at or past `67be91d7`; revisit the launch step's instance check and repair and
their comments against the foreground unit (a dead JVM now ends the unit as
failed); decide whether `ARCHAPPL_ROOT_LOGGER_LEVEL` becomes an operator knob.
The host journal: persistent storage, `MaxRetentionSec=8week` and a
`SystemMaxUse` cap sized from the T20/T21 log figures, and a per-unit rate
limit, as the logging model assigned to this repository; where that lives is
an owner decision in the plan. README and the ref history in this register.

Out of scope: the SQLite backend (M18); the MariaDB password change (M16);
epicsarchiverap-env's own internals.

##### Completion Criteria

- A fresh `archiver_dev` host built at the new refs serves mgmt, persists PV
  configuration across a restart, and writes each instance's log to the journal
  under `archappl-<instance>` with priorities.
- A plain re-apply leaves it unchanged; a killed instance is reported and
  repaired by the operator as documented.
- The journal is persistent and bounded as specified, and survives a reboot.

##### Dependencies And Decisions

- `D19` (owner, 2026-09-26): runs after M16.
- The logging model agreed by epicsarchiverap-env and epicsarchiverap-maven (2026-09-24/25) assigns the
  host journal settings to this repository.
- Owner decisions (2026-09-27): the journal settings go into a journald drop-in
  written by `archiver_build`, so they reach archiver hosts only and leave the
  IOC hosts' journals as they are; `ARCHAPPL_ROOT_LOGGER_LEVEL` becomes the
  operator knob `archiver_root_logger_level`, empty by default so the epicsarchiverap-env
  default (INFO) stands, since the load test showed retrieval logging about
  eight INFO lines per request.
- epicsarchiverap-maven `d9250d23` (on `modernize`, after `67be91d7`) moves three of those
  retrieval lines to DEBUG: `DataRetrievalServlet` "Mime is", `RetrievalState`
  "Update metrics for" and the per-store `PlainPBStoragePlugin` line. Still at
  INFO are `DataRetrievalServlet` "For the complete request",
  `MergeDedupConsumer` "Found a total of" and `PBOverHTTPStoragePlugin` "URL to
  fetch data is" on every request, and `RetrievalState` "Found a data source"
  on 79% of the T21 requests, about 3.8 lines per request on the T21 load
  (checked against the T21 retrieval log and `modernize` on 2026-09-27).
  Whether to move those as well is open on the epicsarchiverap-maven side
  (jeonghanlee/epicsarchiverap-maven#13); the knob's empty default is
  reconsidered when that is decided.
- Range (plan step 1, 2026-09-28): epicsarchiverap-env `9eed006` to `d09dca7` (`modernize`
  head; last code change `90e4a04`) and epicsarchiverap-maven `3c96141d` to `2fc12f01`
  (`modernize` head, which epicsarchiverap-env's own `SRC_TAG` follows; it contains
  `9bbd69bf`, `67be91d7` and `d9250d23`). Operator-facing changes: the unit
  is `Type=simple` with `KillMode=mixed`, `TimeoutStopSec=300` and
  `Requires=@DB_SYSTEMD_UNIT@`; `ARCHAPPL_LOG4J*` are gone (the operator sets
  none); `ARCHAPPL_ROOT_LOGGER_LEVEL`, `DB_BACKEND`, `DB_SOCKET` and
  `ARCHAPPL_STORAGE_ALARM_PERCENT` (health FAIL at or above 85% store
  filesystem use) are new; `conf.storage` warns when the store shares the root
  filesystem and still succeeds; Rocky 8 needs `java-21-openjdk-devel`, which
  the `java` operator already installs.
- Owner decisions (2026-09-28): the MariaDB socket transport (`DB_SOCKET`,
  with `skip-networking` back on archiver hosts) is separate work after M17
  (M21); `ARCHAPPL_STORAGE_ALARM_PERCENT` stays at the epicsarchiverap-env default with no
  operator knob.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-27
- Implementation Authorization: 2026-09-27
- Superseded Plan Artifacts: none

1. Derive the range from `9eed006` to the chosen epicsarchiverap-env head and from
   `3c96141d` to the chosen epicsarchiverap-maven ref: interface changes, operator statements
   whose truth changes, and the ref history to record.
2. Move both refs; adapt the launch step's instance check, repair and comments
   to the foreground unit; add `archiver_root_logger_level` (written to
   `../CONFIG_SITE.local` only when set, and recorded in the install stamp).
3. Write the journal settings as a journald drop-in from `archiver_build`
   (persistent storage, `MaxRetentionSec=8week`, a `SystemMaxUse` cap sized from
   the T20/T21 figures, a per-unit rate limit), and restart journald only when
   the drop-in changes.
4. Verify on a fresh VM; update README and the ref history.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | `--syntax-check`, the splitter over every `raw` task, and a render of the changed tasks | control host | All pass |
| T2 | Integration | Apply `archiver_dev` at the new refs on a fresh host; register PVs; restart the appliance; read `journalctl -u epicsarchiverap-maven.service -t archappl-<instance>` | Fresh Rocky 8.10 VM | Build succeeds, PV configuration persists across the restart, each instance logs to the journal with priorities |
| T3 | Integration | Re-apply; kill one instance and re-apply; reboot | Same VM | Re-apply unchanged; the dead instance is reported and repaired; the journal is persistent and within its cap after the reboot |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-28T04:33Z | control host, working tree on `00cf104` | Passed | `--syntax-check` passes for the `archiver_build` operator and the `archiver_dev` species; the Ansible splitter accepts all 79 `raw` tasks; rendered with Ansible's templar from the role defaults, and again with `archiver_root_logger_level=WARN`, the build script, the new journal task and the launch step pass `bash -n`; the WARN render writes `ARCHAPPL_ROOT_LOGGER_LEVEL:=WARN` and `loglevel=WARN` in the stamp, the default render `loglevel=-` and no level line; the journal drop-in renders `Storage=persistent`, `MaxRetentionSec=8week`, `SystemMaxUse=1G`, `RateLimitIntervalSec=30s`, `RateLimitBurst=10000` |
| T2 | 2026-09-28T04:55:20Z | A fresh Rocky 8.10 archiver-dev vacuum (2 vCPU, 4 GiB) from cloud-provision, working tree on `00cf104`, epicsarchiverap-env `d09dca7`, epicsarchiverap-maven `2fc12f01` | Passed | `make archiver_dev.rocky8` 04:45:37Z-04:51:50Z `failed=0`; stamp `loglevel=-` with `envref=d09dca7 srctag=2fc12f01` and no level line in `CONFIG_SITE.local`; the unit is `Type=simple`, `KillMode=mixed`, `TimeoutStopUSec=5min`, `Requires=mariadb.service`; four instances live, mgmt 200, four tables, no `catalina.out`; `journalctl -u epicsarchiverap-maven.service -t archappl-<instance>` holds every instance with priorities (mgmt 2 at 4 and 144 at 6, the others at 6 only); a 1 Hz test PV reached `Being archived` with one `PVTypeInfo` row, and after `systemctl restart` (10 s) mgmt answered 200 within 25 s, the row was still there and the PV was `Being archived` again |
| T3 | 2026-09-28T04:58:45Z | Same VM | Passed | Re-apply of the species `changed=0 failed=0`; with the etl JVM killed the launcher stopped the other three and the unit ended `failed` (status 1), and a re-apply of the operator reported `ARCHIVER_BUILD_REPAIRED` (`changed=1`) and `ARCHIVER_JOURNAL_UNCHANGED`, with the four instances back; the drop-in carries the five settings and `/var/log/journal` exists; after a reboot (04:57:55Z) the unit was active and mgmt 200 on its own, `journalctl --list-boots` listed both boots with each instance's entries of the previous boot still readable, the journal took 24 MB, and the test PV's row remained |

##### Closure Evidence

- Delivered in `940b63a` (the pins at epicsarchiverap-env `d09dca7` and
  epicsarchiverap-maven `2fc12f01`, `archiver_root_logger_level`, the journald
  drop-in, the instance-check comments, README and the results above); the
  repository names were spelled out afterwards in `6ca7a38`. No dedicated
  GitHub issue.
- Landed: after a fetch at 2026-09-28T07:40:39Z,
  `origin/m14-middleware-reconcile` stood at `6ca7a38`, which contains
  `940b63a`; the branch is not yet merged to `master`.
- T1-T3 Passed on 2026-09-28 against every completion criterion on Rocky 8.10.

#### M18 - Select SQLite as the archiver configuration database through its own operator

- Origin: 38560eb / M18
- GitHub Issue: #28, https://github.com/jeonghanlee/ansible-provision/issues/28
- Status: Complete

##### Summary

epicsarchiverap-env `bbe0968` (jeonghanlee/epicsarchiverap-env#43) lets the appliance keep its
configuration in SQLite instead of MariaDB: `DB_BACKEND:=sqlite` in
`../CONFIG_SITE.local`, the file `$(ARCHAPPL_STORAGE_TOP)/config/archappl.sqlite`
owned by the service account, root-run `make sql.fill` creating it with
`/usr/bin/sqlite3` as that account, `make sql.show` to check the tables, and no
MariaDB server or `mariadb.service` dependency. Per D19 a host selects the
backend by species, with a new `sqlite` operator in place of `mariadb`.

##### Scope

A `sqlite` role and `playbooks/operators/sqlite.yml` installing `sqlite`
(Rocky 8) or `sqlite3` (Debian 13); `playbooks/species/archiver_dev_sqlite.yml`
with the `archiver_dev` operator list and `sqlite` in place of `mariadb`;
`inventory/group_vars/archiver_dev_sqlite.yml` carrying `archiver_db_backend:
sqlite`; the registration points: `configure/RELEASE` (`SPECIES_PLAYBOOKS`,
`OPERATOR_PLAYBOOKS`), the `[archiver_dev_sqlite]` group in
`inventory/lab.ini`, the README species and operator tables and
`docs/ARCHITECTURE.md`; `archiver_build`: `archiver_db_backend` (default
`mariadb`) written as `DB_BACKEND`, its MariaDB-only steps (the password-file
precondition, the `DB_USER_PASS` line, the `archiver_db_socket` check and
`DB_SOCKET` line, the `mysql` table check) run only for `mariadb`, the SQLite
table check through `make sql.show` (never opening the file as root, which can
leave WAL files the appliance cannot write), the backend recorded in its
stamp, and its task header naming `sqlite` beside `mariadb` as the database
prerequisite; README, including the Archiver ordering sentence (`archiver_build`
after `java`, `tomcat` and `mariadb` or `sqlite`).

Out of scope: the distribution-based `archiver-sqlite` species (with the
`archiver` species).

##### Completion Criteria

- Fresh Rocky 8.10 and Debian 13 `archiver_dev_sqlite` hosts, made through the
  cloud-provision generator's `archiver-dev-sqlite` species, have no MariaDB
  server, build, hold the four tables in the SQLite file, persist PV
  configuration across an appliance restart, and re-apply unchanged.
- `archiver_dev` hosts are unaffected.

##### Dependencies And Decisions

- `D19` (owner, 2026-09-26): runs after M17, which brings an
  epicsarchiverap-env ref at or past `bbe0968`; the pin is now `d09dca7`.
- Contract confirmed by epicsarchiverap-env on 2026-09-26 after landing
  `bbe0968`; rechecked at `02737b0` on 2026-09-28: with `DB_BACKEND:=sqlite`,
  `conf.context` renders `context-sqlite.xml`, `sql.fill` and `sql.show` run
  `sqlite3` as the service account through `runuser`, and the unit carries no
  `mariadb.service` dependency; `db.conf` only writes an unused
  `mariadb.conf`.
- Plan review (2026-09-28), confirmed: the `archiver_build` password-file
  precondition, `DB_USER_PASS` read, `archiver_db_socket` check and `mysql`
  table check would each stop a SQLite build; the species needs its
  `configure/RELEASE`, `lab.ini` and README entries; epicsarchiverap-maven's
  SQLite checks wait on this provisioning (its `17fe35fa`).
- Owner decisions (2026-09-28): cloud-provision adds the `archiver-dev-sqlite`
  species to its generator and operator definition before this verification,
  reversing the order D19 first gave (requested the same day); T2 covers
  Rocky 8.10 and Debian 13, whose package names differ.
- cloud-provision `8c9b6ba` (branch `m11-middleware-operators`, observed on
  `origin` 2026-09-28): the generator accepts `--species archiver-dev-sqlite`
  and emits the vacuum group plus `archiver_dev_sqlite`; its operator
  definition gains `P_sqlite` and the species row, with `P_mariadb` and
  `P_sqlite` as alternatives for `P_archiver-build`. Test hosts are made with the
  existing `<os>-archiver-dev` selector and inventoried with the new species.
- epicsarchiverap-maven answered on 2026-09-28: `2fc12f01` declares
  `org.xerial:sqlite-jdbc` 3.53.4.0 at runtime scope, so every WAR carries it in
  `WEB-INF/lib` with the native library for x86_64 Linux; nothing outside the
  WAR is needed. Its SQLite and MariaDB backend checks (its M13 T4 and T5) take
  their evidence from this work, on one epicsarchiverap-env commit for both
  backends, reported with UTC times, the exact commands and the log lines.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-28
- Implementation Authorization: 2026-09-28
- Superseded Plan Artifacts: none

1. Add the `sqlite` role and operator playbook.
2. Add the `archiver_dev_sqlite` species playbook, group_vars, the
   `configure/RELEASE` entries and the `lab.ini` group.
3. Extend `archiver_build`: `archiver_db_backend`, the `DB_BACKEND` line, the
   MariaDB-only steps gated on `mariadb`, the `make sql.show` check for SQLite,
   the stamp field (for SQLite the `db=` entry names the SQLite file, not a
   socket or TCP address).
4. README and `docs/ARCHITECTURE.md`.
5. Verify on fresh VMs from the cloud-provision generator; report to
   cloud-provision, and to epicsarchiverap-maven in the form of its T4 (T2
   here) and T5 (T3 here).

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | `--syntax-check` on both species, the splitter, and a render of the changed tasks for each backend | control host | All pass; the SQLite render carries no MariaDB step |
| T2 | Integration | Apply `archiver_dev_sqlite` on a fresh host; record the deployed epicsarchiverap-env and epicsarchiverap-maven commits; confirm no MariaDB server (`rpm -q mariadb-server` or `dpkg -s mariadb-server` absent, no `mariadb.service` unit); `make sql.show` and `sqlite3 .tables` on the file as the service account; read the mgmt log's RDB Engine, SQL Dialect and driver-source lines; `archivePV`, `getPVStatus` and `getData.json` for one PV served by softIocPVX; read the `PVTypeInfo` row back with `sqlite3`; restart through the unit and repeat `getPVStatus` and `getData.json`; scan every instance log for errors and `SQLITE_BUSY`; re-apply | Fresh Rocky 8.10 and Debian 13 VMs from `--species archiver-dev-sqlite` | No MariaDB server; four tables; SQL Dialect SQLite with the driver from `WEB-INF/lib`; the PV archives, persists across the restart and serves data; no `SQLITE_BUSY` or unexpected error; re-apply unchanged |
| T3 | Regression | The same checks as T2 with the default backend, on the epicsarchiverap-env commit of T2: apply `archiver_dev` on a fresh host, read the dialect and driver lines, run the PV sequence with the `PVTypeInfo` row read back over the socket, restart, scan the logs, re-apply | A fresh Rocky 8.10 archiver-dev VM | Socket transport and four tables as before; the MariaDB dialect and driver; the PV persists across the restart; no unexpected error; re-apply `changed=0` |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-28T16:15Z | control host, working tree on `02da53a` | Passed | `--syntax-check` passes for the `sqlite` and `archiver_build` operators and the `archiver_dev_sqlite` and `archiver_dev` species; the Ansible splitter accepts all 80 `raw` tasks; `make -n` resolves `archiver_dev_sqlite.rocky8` and `op.sqlite.rocky8`; the runtime-inventory contract test passes 3/3; rendered with Ansible's templar, the `archiver_build` tasks for `archiver_db_backend` `mariadb` and `sqlite` and the `sqlite` role pass `bash -n`, the stamps read `db=archappl@socket:auto/archappl` and `db=sqlite:/arch/config/archappl.sqlite`, and every MariaDB step of the rendered build and launch scripts sits behind a `db_backend` test that the SQLite render leaves false; that branch taken at run time is T2's |
| T2 | 2026-09-28T16:33:20Z | Fresh Rocky 8.10 and Debian 13 vacua from cloud-provision (`<os>-archiver-dev` selector, inventoried with `--species archiver-dev-sqlite` by `8c9b6ba`), working tree on `02da53a` | Passed | `make archiver_dev_sqlite.rocky8` and `.debian13` `failed=0` (16:20:32Z-16:28:46Z); deployed epicsarchiverap-env `d09dca7` and epicsarchiverap-maven `2fc12f01`; stamp `db=sqlite:/arch/config/archappl.sqlite`; `CONFIG_SITE.local` carries `DB_BACKEND:=sqlite` and no password or socket line; `mariadb-server` not installed, no `mariadb.service` unit, the appliance unit requires only `sysinit.target system.slice`; `/arch/config/archappl.sqlite` `mid-srv:mid 644`; `make sql.show` and `runuser -u mid-srv -- sqlite3 ... .tables` list ArchivePVRequests, PVAliases, ExternalDataServers, PVTypeInfo; mgmt logs `RDB Engine is 'SQLite' '3.53.4'` and `SQL Dialect SQLite`, with `sqlite-jdbc-3.53.4.0.jar` in `mgmt/WEB-INF/lib`; a 1 Hz PV served by softIocPVX reached `Being archived` (16:31:15Z), `getData.json` returned its samples, `sqlite3` read its `PVTypeInfo` row back, and after `systemctl restart` (10 s, 16:31:46Z) it was `Being archived` again (16:32:33Z) with new samples; the unit journal holds no `SQLITE_BUSY` and four ERROR lines, all the mgmt start-up notice that actions wait until every component has started; a re-apply of the species reported `changed=0` on both |
| T3 | 2026-09-28T16:33:20Z | A fresh Rocky 8.10 archiver-dev vacuum from cloud-provision, same commits as T2 | Passed | `make archiver_dev.rocky8` `failed=0` (16:20:32Z-16:26:18Z); stamp `db=archappl@socket:auto/archappl`; `CONFIG_SITE.local` carries `DB_BACKEND:=mariadb`, the password and `DB_SOCKET:=/run/mariadb/mariadb.sock`; the unit requires `mariadb.service`; four tables; mgmt logs `RDB Engine is 'MariaDB' '10.3.39-MariaDB'` and `SQL Dialect MySQL`; the same PV sequence passed, with the `PVTypeInfo` row read over the socket and the PV `Being archived` again after the restart; no `SQLITE_BUSY`, the same four start-up ERROR lines; re-apply `changed=0` |

##### Closure Evidence

- Delivered in `0a3d4e4` (the `sqlite` operator, the `archiver_dev_sqlite`
  species and its registration, the `archiver_build` backend knob and SQLite
  table check, README and `docs/ARCHITECTURE.md`, the results above).
- Landed: after a fetch at 2026-09-28T16:56:42Z,
  `origin/m14-middleware-reconcile` stood at `0a3d4e4`; the branch is not yet
  merged to `master`.
- T1-T3 Passed on 2026-09-28 against every completion criterion; the evidence
  was reported to epicsarchiverap-maven in the form of its SQLite and MariaDB
  backend checks, and cloud-provision confirmed its `8c9b6ba` definition matches
  the role.
- #28 was closed manually on this verification (observed closed, reason
  completed, at 2026-09-28T17:19:55Z, with its body synced to the result); the
  commit's `Closes #28` footer has no further effect when the branch reaches
  `master`.

#### M19 - Add an ioc-group operator fixture account with linger

- Origin: 38560eb / M19
- GitHub Issue: #27, https://github.com/jeonghanlee/ansible-provision/issues/27
- Status: Complete

##### Summary

The `testusers` fixture serves the epics-ioc-runner multi-user scenarios.
`opa` and `opb` belong to `ioc` without linger, and `usera` and `userb` have
linger outside `ioc`. epics-ioc-runner 1.4.2 adds a scenario in which one
account runs an IOC in local mode (`systemctl --user`, which needs linger) and
then the same IOC as a system service (which needs `ioc` membership for the
sudoers gate), so no current account fits. A new account keeps the existing
accounts' meaning in the consumer's `gate/RUNBOOK.md`.

##### Scope

`roles/testusers`: a `test_users_operators_linger` list (default `[opc]`) and
one task that creates each account, adds it to `test_users_ioc_group` and
enables linger; an `opc` row in the Accounts table of
`docs/test_users_handoff.md` and a separate verification line dated from
M19/T2 (the existing Verification list records the 2026-07-05 accepted state
and stays as it is).

Out of scope: any change to `opa`, `opb`, `obs`, `usera` or `userb`; the
consumer's RUNBOOK fixture table and fixture check
(jeonghanlee/epics-ioc-runner); the golden bake itself, which cloud-provision
runs; the retired paths elsewhere in `docs/test_users_handoff.md` (M20).

##### Completion Criteria

- On a fresh Rocky 8.10 and a fresh Debian 13 iocrunner host applied through
  this repository, `opc` exists, belongs to `ioc`, and has linger enabled; the
  other five accounts are unchanged.
- A re-apply of the operator succeeds and leaves the same state.

##### Dependencies And Decisions

- Requested by epics-ioc-runner on 2026-09-27 as an external gate of its 1.4.2
  release; the owner chose a new account over enabling linger on an existing
  one.
- The consumer's release gate runs on a fresh bake, so the golden carries
  `opc` from the next iocrunner bake after this lands; a running host gets it
  by applying `playbooks/operators/testusers.yml`, which is not evidence for
  the golden. The consumer's gate also requires its two running test consumers
  to carry `opc`; this repository provides the operator, and the consumer side
  applies it to them.
- Owner decision (2026-09-27): `opc` gets its own list and task rather than
  joining `test_users_operators` with a separate linger list, so the existing
  account lists and tasks stay unchanged.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-27
- Implementation Authorization: 2026-09-27
- Superseded Plan Artifacts: none

1. Add `test_users_operators_linger` to `roles/testusers/defaults/main.yml`.
2. Add the create, `ioc` join and linger task to `roles/testusers/tasks/main.yml`.
3. Add the `opc` row to the Accounts table of `docs/test_users_handoff.md`.
4. Run T1 and T2 on fresh VMs, add the dated verification line to
   `docs/test_users_handoff.md`, and report the commit to epics-ioc-runner and
   cloud-provision, naming `make op.testusers.<vacuum>` as the way to give the
   two running test consumers `opc`.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | `--syntax-check` on `playbooks/operators/testusers.yml` and `playbooks/species/iocrunner.yml` | control host | Both pass |
| T2 | Integration | `make iocrunner.<vacuum> RUNTIME_INVENTORY=<host inventory>`; check `id -nG <account>` and `test -e /var/lib/systemd/linger/<account>` for all six accounts (the form of the consumer's fixture check); re-apply with `make op.testusers.<vacuum> RUNTIME_INVENTORY=<host inventory>` | Fresh Rocky 8.10 and Debian 13 VMs | `opc` lists `ioc` and has a linger file; the other five as before; re-apply succeeds with the same state |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-28T03:23:24Z | control host, working tree on `aaa026d` | Passed | `ansible-playbook --syntax-check` exits 0 for `playbooks/operators/testusers.yml` and `playbooks/species/iocrunner.yml`; `--list-tasks` shows the new task last in the operator |
| T2 | 2026-09-28T03:51:39Z | A fresh Rocky 8.10 and a fresh Debian 13 bare vacuum (2 vCPU, 4 GiB) from cloud-provision, working tree on `aaa026d` | Passed | `make iocrunner.rocky8` and `make iocrunner.debian13` `failed=0` (finished 03:51:11Z), the new task last in the operator on both; on both hosts `id -nG` and the linger file give `opa` and `opb` in `ioc` without linger, `obs` in neither, `usera` and `userb` with linger outside `ioc`, and `opc` in `ioc` with linger (home `/home/opc`, shell `/bin/bash`); `make op.testusers.<vacuum>` re-apply `ok=5 changed=0 failed=0` on both with the same state |

##### Closure Evidence

- Delivered in `32ea95f` (the `opc` list and task in `testusers`, the handoff
  document's `opc` row and dated check, the results above). #27 was closed
  manually on its verification (observed closed, reason completed, at
  2026-09-28T04:15:51Z); the commit's `Closes #27` footer has no further
  effect when the branch reaches `master`.
- Landed: after a fetch at 2026-09-28T03:59:23Z,
  `origin/m14-middleware-reconcile` stood at `32ea95f`; the branch is not yet
  merged to `master`.
- T1-T2 Passed on 2026-09-28 against every completion criterion. The consumer
  applied the operator to its two running test consumers the same day; the
  next iocrunner bake at or past `32ea95f` carries `opc`, which the consumer
  tracks as its own gate with cloud-provision.


#### M21 - Reach the archiver MariaDB over its Unix socket

- Origin: 38560eb / M21
- GitHub Issue: none
- Status: Complete

##### Summary

The `archiver_dev` group sets `mariadb_skip_networking: false` because epicsarchiverap-env
reached MariaDB only over TCP at `127.0.0.1:3306`. epicsarchiverap-env `90e4a04` adds
`DB_SOCKET`: with a socket path in `../CONFIG_SITE.local`, the appliance's JDBC
URL (`localSocket=`) and epicsarchiverap-env's own clients, `sql.fill` and `sql.show`
included, use that socket, and the server may run with `skip-networking`. The
account must be `<user>@'localhost'`, which the `mariadb` operator already
creates, and the socket and its directory must be reachable by the service
account.

##### Scope

`roles/archiver_build`: a knob `archiver_db_socket`, defaulting to the socket
the `mariadb` operator manages (`/run/mariadb/mariadb.sock` on Rocky,
`/run/mysqld/mysqld.sock` on Debian; epicsarchiverap-env's Rocky example
`/var/lib/mysql/mysql.sock` is not that path), written as `DB_SOCKET` and
recorded in the install stamp, with the post-`sql.fill` table check over the
same socket; an empty value keeps today's TCP path through `archiver_db_host`
and `archiver_db_port`; `roles/mariadb`: drop the application account's `127.0.0.1`
host when `skip-networking` is on; `inventory/group_vars/archiver_dev.yml`:
return to the operator default `skip-networking`; README, including the move of
an installed TCP host; every other statement that assumes loopback TCP for the
archiver (`docs/ARCHITECTURE.md`, the `archiver_build` task header and
`archiver_db_host` comment, the `mariadb` account-host comments).

Out of scope: the SQLite backend (M18); remote database hosts.

##### Completion Criteria

- Fresh Rocky 8.10 and Debian 13 `archiver_dev` hosts have no MariaDB TCP
  listener and no `127.0.0.1` application account, build, hold the four
  tables, serve mgmt, and persist PV configuration across a restart; a
  re-apply leaves them unchanged.
- A host installed over TCP by the previous operator moves to the socket in one
  run with `archiver_force_reinstall=true`, as README states, and then persists
  PV configuration.

##### Dependencies And Decisions

- Owner decision (2026-09-28): kept out of M17, which moves the
  epicsarchiverap-env pin past `90e4a04` and so makes `DB_SOCKET` available.
- Plan review (2026-09-28), confirmed: the post-`sql.fill` table check logs in
  over TCP (`127.0.0.1:3306`) and would stop every build once TCP is closed;
  and on an installed host the species runs `mariadb` first, which closes TCP
  under the running appliance's TCP JDBC connection, after which
  `archiver_build` reports drift and stops, leaving the appliance without its
  database until a forced reinstall.
- Owner decisions (2026-09-28): an installed TCP host moves in one run with
  `archiver_force_reinstall=true`, documented in README and exercised as T3,
  with no cross-role guard; the `mariadb` operator removes the `127.0.0.1`
  application account under `skip-networking`; T2 covers Rocky 8.10 and
  Debian 13, whose socket paths differ.
- The socket directory is `mysql:mysql 755` and the socket `777` under the
  `mariadb` operator, so the service account reaches it; epicsarchiverap-maven
  `2fc12f01` carries the jna libraries the socket path needs (`85f0f179`).
- Owner decision (2026-09-28): the socket path is the knob
  `archiver_db_socket` with a per-OS default; empty keeps the TCP path, so the
  host and port knobs stay meaningful and the change stays reversible.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-28
- Implementation Authorization: 2026-09-28
- Superseded Plan Artifacts: none

1. `roles/archiver_build`: add `archiver_db_socket` (per-OS default), write
   `DB_SOCKET` when it is set, run the table check over the socket then and
   over TCP otherwise, and record the transport in the stamp.
2. `roles/mariadb`: remove the `127.0.0.1` application account when
   `skip-networking` is on, and report the change.
3. `inventory/group_vars/archiver_dev.yml`: drop `mariadb_skip_networking:
   false`; README: the socket transport, `archiver_db_socket` (an empty value
   needs `mariadb_skip_networking: false` beside it, since the default closes
   TCP and drops the `127.0.0.1` account), and the one-run move of an
   installed TCP host; correct the other loopback-TCP statements named in the
   scope.
4. Run T1-T3; record the results.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | `--syntax-check`, the splitter over every `raw` task, and a render of the changed tasks | control host | All pass |
| T2 | Integration | Apply `archiver_dev` on a fresh host; check for a MariaDB TCP listener and the application accounts; register a PV; restart the appliance; re-apply | Fresh Rocky 8.10 and Debian 13 VMs | No TCP listener; only the `localhost` application account; four tables; PV configuration persists; re-apply unchanged |
| T3 | Integration | Build a host with the operator at `901563c` (loopback TCP), run from a `git worktree` checkout of that commit with `make archiver_dev.rocky8`; register a PV; apply the new operator with `archiver_force_reinstall=true` | Fresh Rocky 8.10 VM | One run succeeds; TCP closed, `127.0.0.1` account gone; the PV's configuration is still in the database and it archives again |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-28T08:16Z | control host, working tree on `901563c` | Passed | `--syntax-check` passes for the `archiver_build` and `mariadb` operators and the `archiver_dev` species; the Ansible splitter accepts all 79 `raw` tasks; rendered with Ansible's templar, the `archiver_build` tasks with `archiver_db_socket` `auto` and empty, and the `mariadb` tasks with `mariadb_skip_networking` true and false, all pass `bash -n`; the stamp reads `db=archappl@socket:auto/archappl` and `db=archappl@127.0.0.1:3306/archappl` respectively, and the account cleanup renders `tcp=0` and `tcp=1` |
| T2 | 2026-09-28T08:50Z | Fresh Rocky 8.10 and Debian 13 archiver-dev vacua (2 vCPU, 4 GiB) from cloud-provision, working tree on `901563c` | Passed | `make archiver_dev.rocky8` and `make archiver_dev.debian13` `failed=0` (finished by 08:45:11Z); on both the stamp reads `db=archappl@socket:auto/archappl`, `CONFIG_SITE.local` carries `DB_SOCKET:=/run/mariadb/mariadb.sock` (Rocky) or `/run/mysqld/mysqld.sock` (Debian), the rendered JDBC URL is `jdbc:mariadb://localhost/archappl?localSocket=<that socket>`, no listener on 3306, `@@skip_networking` 1, the only application account is `archappl@localhost`, four tables, mgmt 200, and all eight appliance connections come from `archappl@localhost`; a 1 Hz test PV reached `Being archived` with one `PVTypeInfo` row, stayed after `systemctl restart` (10 s) and archived again; a re-apply of the species reported `changed=0` on both |
| T3 | 2026-09-28T08:51:18Z | A fresh Rocky 8.10 archiver-dev vacuum from cloud-provision | Passed | Built with the operator at `901563c` from a `git worktree` checkout: stamp `db=archappl@127.0.0.1:3306/archappl`, JDBC `jdbc:mariadb://127.0.0.1:3306/archappl`, one listener on 3306, accounts `archappl@127.0.0.1` and `archappl@localhost`, eight connections from `127.0.0.1`; a test PV registered, restarted and archiving. One run of the new operator with `-e archiver_force_reinstall=true` (08:49:13Z-08:50:47Z, `failed=0`, changed: the MariaDB configuration, the account cleanup and the build launch) left the socket stamp and JDBC URL, no listener on 3306, only `archappl@localhost`, eight connections from `archappl@localhost`, the test PV's `PVTypeInfo` row still present and the PV `Being archived` again |

##### Closure Evidence

- Delivered in `8a5c355` (`archiver_db_socket` and the socket table check in
  `archiver_build`, the `127.0.0.1` account cleanup in `mariadb`, the
  socket-only `archiver_dev` group, README and `docs/ARCHITECTURE.md`, the
  results above). No dedicated GitHub issue.
- Landed: after a fetch at 2026-09-28T08:56:08Z,
  `origin/m14-middleware-reconcile` stood at `8a5c355`; the branch is not yet
  merged to `master`.
- T1-T3 Passed on 2026-09-28 against every completion criterion; the move of an
  installed TCP host was exercised on Rocky 8.10 only.


#### M20 - Align the test-user handoff document with the operator model

- Origin: 38560eb / M20
- GitHub Issue: none
- Status: Complete

##### Summary

`docs/test_users_handoff.md` still describes the staged model: it names
`test_users`, `app_ioc_runner`, `site.yml`, `roles/test_users`,
`playbooks/07_test_users.yml`, a `SERVER_ONLY_PLAYBOOKS` entry in
`configure/CONFIG_SITE`, `04_nfs_sim.yml`
and `nfs_sim_nodes`, and says the cloud-provision bake runs `07_test_users.yml`
as its Step 6/9. The fixture now lives in `roles/testusers`, runs through
`playbooks/operators/testusers.yml` as the last operator of
`playbooks/species/iocrunner.yml`, and the bake
(`bin/bake_iocrunner_image.bash` in cloud-provision) applies that species
assembly as its Step 4/8. The product `ioc-srv` account and `ioc` group come from
`roles/iocrunner`, which runs the runner's `setup-system-infra.bash --full`.

##### Scope

Every mention of a retired name in `docs/test_users_handoff.md`, by section:
Scope (`test_users`, `app_ioc_runner`), Purpose (`site.yml`), the Integration
table, the paragraph under Accounts (`app_ioc_runner`), and Ordering and Data
Flow, with these replacements:

- `test_users` / `roles/test_users` -> `testusers` / `roles/testusers`.
- `playbooks/07_test_users.yml` targeting `nfs_sim_nodes` ->
  `playbooks/operators/testusers.yml` (`hosts: vacua`, run as
  `make op.testusers.<vacuum>`), the last operator of
  `playbooks/species/iocrunner.yml`.
- The `SERVER_ONLY_PLAYBOOKS` entry in `configure/CONFIG_SITE` -> the
  `OPERATOR_PLAYBOOKS` entry in `configure/RELEASE`.
- `site.yml` excluding the fixture -> the `iocserver` species, the iocrunner
  product without `testusers`, for a production IOC server.
- `app_ioc_runner` -> `roles/iocrunner`, which runs the runner's
  `setup-system-infra.bash --full`.
- `04_nfs_sim.yml` creating the NFS simulation boundary before the fixture ->
  the `nfs_sim` operator, applied only by the `iocrunner_nfs` species (the
  bake's `iocrunner-nfs` flavor) and after the whole iocrunner species, so after
  `testusers`.
- The bake running `07_test_users.yml` as Step 6/9 -> the bake applying the
  iocrunner species assembly as Step 4/8, and Ordering step 4 -> its Steps 5-8
  (finalize provenance, validate it and extract the sidecar, seal the proxy
  artifact contract, shut down and publish the validated pair).

Out of scope: the Accounts table and Verification content, which M19 and the
accepted 2026-07-05 state own; the cloud-provision bake script.

##### Completion Criteria

- Every path in this repository that the document names exists, and the
  order it states matches `playbooks/species/iocrunner.yml` and
  `playbooks/species/iocrunner_nfs.yml`.
- Every reference to another repository matches that repository's current
  files (the cloud-provision bake script, the epics-ioc-runner RUNBOOK).

##### Dependencies And Decisions

- Owner decision (2026-09-27): kept out of M19 so that the fixture account for
  the consumer's release gate stays a small change.
- Assigned from the Backlog on 2026-09-28 (Assignment History).
- Owner decision (2026-09-28): the file keeps its name
  `docs/test_users_handoff.md`, which `docs/README.md`, `docs/SEAM.md` and
  `roles/testusers/defaults/main.yml` link to; only its content changes.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-09-28
- Implementation Authorization: 2026-09-28
- Superseded Plan Artifacts: none

1. Rewrite the retired mentions in the listed sections with the replacements
   above, checking each against the current operator, species and
   cloud-provision bake files.
2. Run T1; record the result.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | `grep` the document for the retired names; `test -e` every path of this repository it names; compare the stated order with `playbooks/species/iocrunner.yml` and `playbooks/species/iocrunner_nfs.yml` and the whole Ordering list with Steps 1-8 of cloud-provision `bin/bake_iocrunner_image.bash` | control host | No retired name; all paths exist; the operator order and every bake step match |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-28T18:08:29Z | control host, working tree on `71fa108`; cloud-provision and epics-ioc-runner at their fetched `origin` | Passed | A grep of the rewritten `docs/test_users_handoff.md` finds none of `test_users`, `app_ioc_runner`, `site.yml`, `roles/test_users`, `07_test_users`, `SERVER_ONLY`, `CONFIG_SITE`, `04_nfs_sim`, `nfs_sim_nodes` or `Step 6/9`; all eight repository paths it names exist; `playbooks/species/iocrunner.yml` ends with `testusers` and `iocrunner_nfs.yml` imports `iocrunner.yml` then `nfs_sim`, as its Ordering states; `iocserver.yml` has no `testusers`; the bake's Steps 1-8 and its `iocrunner`/`iocrunner-nfs` assemblies match the Ordering and Integration rows; `gate/RUNBOOK.md` exists in epics-ioc-runner |

##### Closure Evidence

- Delivered in `268a060` (the rewritten `docs/test_users_handoff.md` and the
  assignment of this item from the Backlog). No dedicated GitHub issue.
- Landed: after a fetch at 2026-09-28T18:28:48Z,
  `origin/m14-middleware-reconcile` stood at `268a060`; the branch is not yet
  merged to `master`.
- T1 Passed on 2026-09-28 against both completion criteria.


#### M22 - Verify the ETL pass scheduler on two parallel store chains

- Origin: 38560eb / M22
- Identity History: none
- GitHub Issue: #30, https://github.com/jeonghanlee/ansible-provision/issues/30; external request jeonghanlee/epicsarchiverap-maven#12
- Status: Complete

##### Summary

Verify that the deployed ETL actually moves eligible data between stores, applies the configured transformations, retains or deletes source data correctly, and returns the expected values and timestamps through HTTP retrieval. Then verify repeated scheduler operation on the shortened and default chains for a full 24 hours each, followed by evidence reconciliation and a separate ETL completion decision.

The ETL verification owns its workload, preparation, tools, evidence and verdict. Journal recording and retention are a separate test. A failed or incomplete journal test does not imply an ETL failure, and an ETL result does not establish journal correctness.

##### Scope

The actual deployed ETL behavior, the agreed 903-PV workload and store cadences, eligible historical inputs, physical and HTTP comparisons, all required scheduled passes and normal whole-appliance shutdown. Exact event/value comparisons cover four scalar-double policy representatives; configuration and population checks cover all 903 PVs. This does not claim exact value-level comparison of every PV or every data type.

##### Out Of Scope

#34 owns collector correction, package/journal-module independence, default variants, source-unavailability and automatic-abort tools, terminal capture/repeated requests and collection during runtime races. Completed additional tool cases retain their observed results there; unexecuted variants are not marked Passed.

#35 owns evaluator/JFR/process/time comparison corrections, remaining measurement reconciliation, supplemental workload/time reports and independent-recipient reproduction. These follow-ups occur after ETL functional acceptance and neither blocks its completion. Reuse the retained observations; no new full-day run is required solely for tool correction, analysis or replay.

Journal delivery/retention acceptance, production scheduler/store-policy changes, new storage-failure tests, host sizing and engine sample-buffer fixes tracked in jeonghanlee/epicsarchiverap-maven#29 are outside this issue. Sufficient full-day disk capacity is established; no journal size cap or predicted retention budget is an acceptance condition.

##### Root Cause

Earlier collector/evaluator coupling and diagnostic defects belong to M29/#34 and M30/#35. D30 limits this work's completion decision to actual ETL functionality and repeated processing. Original tool outcomes remain unchanged.

##### Test Signals And Store Cadences

Use the shipped 903-PV fixture and the accepted ten-record deadband override throughout functional checks and long observations.

| Signal group | PV count | Configured source frequency |
| --- | --- | --- |
| General scalar, string and state | 775 | 1 Hz |
| Arrays, configured capacity 1000 elements | 8 | 1 Hz |
| Fast | 110 | 10 Hz |
| Slow | 10 | 0.1 Hz |

The fixture has 880 MONITOR and 23 SCAN registrations. Source processing, registration and actual archived events are different measurements. Preserve independently obtained input values, timestamps and order; nominal frequency multiplied by elapsed time is not an observed reference count. Record actual array lengths instead of assuming every array always contains 1000 elements.

| Chain | STS / `hold` / `gather` | MTS / `hold` / `gather` | LTS | STS to MTS cadence | MTS to LTS cadence |
| --- | --- | --- | --- | --- | --- |
| Shortened | `PARTITION_5MIN` / 2 / 1 | `PARTITION_HOUR` / 2 / 1 | `PARTITION_DAY` | 5 minutes | 1 hour |
| Default | `PARTITION_HOUR` / 2 / 1 | `PARTITION_DAY` / 2 / 1 | `PARTITION_YEAR` | 1 hour | 8 hours |

Record actual per-PV stores, `hold`, `gather`, policy, artifact/source identities and unit timeouts. Both chains require `hold=2` and `gather=1` on STS and MTS; verify those values in all 903 effective per-PV store configurations. Scheduled ticks do not prove data eligibility. Write independently specified historical inputs with the real native writer so both transitions have eligible data, then let normal startup and the actual scheduler process them. Continue live PV generation throughout. Fresh default-chain data alone cannot prove transfer through the daily source into LTS during a 24-hour observation.

Check configuration and pass population for all 903 PVs. The existing exact physical and HTTP comparisons cover four scalar-double representatives, one per `raw`, `lastSample_10`, `lastSample_30` and `lastSample_60` policy. State that scope explicitly; it is not exact value-level verification of all 903 PVs or all data types. ETL records must come from actual passes at the configured cadences; synthetic pass messages cannot establish execution.

##### Execution Order And Time Allocation

Keep the functional test, long observation and final decision as separate parts of the execution plan.

| Order | Planned time | ETL work and required result |
| --- | --- | --- |
| Actual ETL processing checks | About 3 hours | On both chains, preserve fixed historical inputs and capture physical contents after initial processing; compare movement, transformation, policy-controlled retention/deletion, HTTP retrieval and actual ETL execution records. Record each result before the long observation. |
| Long observation | At least 24 hours per chain, in parallel | Keep the full live fixture running; verify repeated ETL scheduling, the same fixed intervals after later regular passes and required measurements. Journal retention is observed independently by the journal work. |
| Result decision | About 2 hours in the overall test schedule | Reconcile original inputs, physical outputs, actual pass records, metrics, retrieval and resource evidence; record missing evidence and an independent ETL verdict. |

The separate journal work retains its approximately one-hour basic recording/query/collection check. Its schedule can precede the ETL functional check, but its success is not an ETL start or completion prerequisite. The approximately two-hour result-decision period belongs to the overall schedule; it is not an additional two-hour allocation for every issue. Each issue produces its own verdict.

The three-hour allocation remains in the plan. It is a planning allowance, not proof that both functional checks will finish in three hours. The existing default focused workflow can wait up to 28800 plus 600 seconds for a subsequent regular pass. Record that scheduling constraint and actual preparation, functional-check, waiting, observation and final-check times. Report a conflict with the allocation before execution; do not silently remove the functional stage, shorten a required observation, or count waiting as evidence of successful processing.

The functional stage captures original historical inputs, independent policy expectations and physical contents after initial processing. Preserve the focused workflow's existing comparison after subsequent regular passes before granting focused continuity. During each long observation, compare the same fixed historical intervals again after a later regular pass of each transition and at final capture. Bind each snapshot to the actual pass and capture time. Add no new historical input to those intervals; all 903 live PVs continue generating outside them. Record the phase and actual time of every comparison without changing the time allocations or continuity requirements.

##### Evidence And Independent Verdict

Use original fixed historical inputs and independently specified policy outputs, actual native store contents and decoded event occurrences, HTTP values/timestamps/status/severity/order/counts and actual ETL pass records. Scheduled ticks, HTTP 200 or nominal rates alone do not establish correct processing.

Compare the same fixed intervals after initial processing, later regular passes of both transitions and final capture. All 903 live PVs continue outside those intervals. Preserve required source copies until deletion is due, verify expected destination multiplicities and compare unreduced serialized event bytes where applicable.

Journal recording and retention are independent. The actual application ETL records supplied every required pass in both completed observations. Kernel diagnostic collection and verifier failures remain recorded separately; they are not evidence of an ETL processing failure.

##### Completion Criteria

- [x] Both deployed chains preserve the agreed fixture, source/artifact identities and effective configuration for all 903 PVs, including STS/MTS `hold=2` and `gather=1`; eligible historical inputs exercise both transitions.
- [x] Real movement, transformation, policy-controlled retention/deletion and HTTP retrieval match original inputs and independent expectations, including values, timestamps, status, severity, order, policy-specific counts and unreduced event bytes in the four scalar-double exact scope.
- [x] Initial, later regular-pass checkpoints for both transitions and final physical/HTTP comparisons match the expected fixed-interval multiplicities with no additional historical seed, missing events or physical duplicates.
- [x] Each observation exceeds 86400 seconds in UTC and monotonic time across UTC midnight. Required passes are unique, ordered, complete and successful within the native timing/metric checks: 312/312 shortened and 27/27 default, with zero missing, duplicate or unexpected passes and native scheduler verdict `Passed`.
- [x] Both complete observations reach normal whole-appliance shutdown without forced termination: return code 0 in 12.516 and 13.770 seconds, below the installed 300-second timeout.
- [x] The ETL conclusion is supported by actual retained processing evidence and preserves original unsuccessful records. Separate collection/evaluation/program-reproduction work in #34 and #35 is excluded from this functional completion decision.

##### Dependencies And Decisions

- M17, M21 and G4 remain completed deployment prerequisites; D27 owns independent package separation. No M25 preparation, proof, service or result is an ETL execution or completion dependency.
- 2026-10-13: the owner restated the original one-hour journal check, three-hour ETL functional check, 24-hour parallel observations and two-hour overall decision allocation. The journal hour belongs to M25; ETL owns its functional stage, observations and verdict.
- 2026-10-13: journal-test failure does not decide ETL. Required ETL functionality and scheduling may be established using complete independent ETL evidence; unsupported claims remain Incomplete.
- 2026-10-13: require policy-specific physical event multiplicities across initial processing and later regular passes on fixed historical intervals, with status/severity/count and unreduced event-byte comparisons; require source `hold=2` and `gather=1` in all 903 effective per-PV configurations on both chains. These are document corrections; implementation remains paused.
- Decision Date: 2026-10-13. After confirming that journal completion is not an ETL prerequisite and reaffirming the agreed three-hour functional allocation, the owner requested separate ETL environments and proceeding. This resumes independent package preparation, acquisition and installation of two fresh shortened/default deployments, verification of the required independent evidence paths and the initial functional checks under Ordered Work 1 to 5. Keep the existing signals, store cadences and later regular-pass continuity requirements. No retained guest change or full-day start is authorized by this instruction.
- Decision Date: 2026-10-13. After the separate completed basic/initial results and the remaining regular-repeat, independent full-day and lifecycle checks were summarized, the owner directed proceeding. Continue the accepted remaining verification on these dedicated deployments. Preserve the initial results and fixed inputs; establish actual measurement and source readiness before each full-day start. Neither issue waits for the other's verdict.
- Decision Date: 2026-10-13. The owner authorized rechecking copies of already completed test records while leaving all three current 24-hour observations unaffected. Use only completed control-host evidence for this work, preserve originals and their unsuccessful outcomes, and distinguish retained-record checker conclusions from fresh runtime or full-window acceptance.
- D30; Decision Date: 2026-10-15. The completed ETL functionality is the purpose of this test. Remaining package/fault/measurement/report/recipient checks verify the tools and move to M29/M30 after ETL acceptance. They do not keep ETL functionality incomplete. The existing shortened E4 run is separately concluded from its retained actual evidence.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-10-15; D30 clarifies the existing accepted ETL functional purpose and independent tool follow-ups.
- Implementation Authorization: actual ETL processing/observation and retained-original reconciliation were authorized; the present request authorizes issue/document scope correction, not new runtime tests or deferred tool implementation.
- Superseded Plan Artifacts: former ETL completion prerequisites that required collection/evaluation tool robustness, supplemental reports or independent-recipient reproduction; those remain explicit M29/M30 Backlog work.

1. Verify the agreed fixture/configuration and independently specified eligible historical inputs.
2. Compare actual movement, transformation, retention/deletion and HTTP retrieval with original expectations.
3. Verify both actual full-day scheduled processing windows, repeated physical comparisons and whole-unit normal stops.
4. Record the supported ETL functional verdict while retaining original unsuccessful tool records; transfer tool follow-ups to M29/M30.

##### Test Plan

| Label | Check | Real path and evidence | Required result |
| --- | --- | --- | --- |
| T1 | Package independence tools | Transferred to M29/#34 under D30 | Independent Backlog; not an ETL functional completion criterion. |
| T2 | Start/terminal/fault tools | Transferred to M29/#34 under D30; existing E4 behavior concluded separately | Independent Backlog; not an ETL functional completion criterion. |
| T3 | Measurement regressions | Collection paths in M29/#34 and evaluation paths in M30/#35 | Independent Backlog; not an ETL functional completion criterion. |
| T4 | Functional processing | Original input expectations, actual scheduler, native physical decode and HTTP | Passed within four-PV exact and all-903 configuration/population scope. |
| T5 | Full-window scheduling | Actual native pass/timing/metric checks and repeated/final physical comparisons | Passed; 312/312 shortened and 27/27 default, no missing/duplicate/unexpected passes. |
| T6 | Supplemental measurements | Transferred to M30/#35 under D30 | Independent Backlog; not an ETL functional completion criterion. |
| T7 | Whole-unit normal stop | Actual completed windows and retained whole-appliance stop evidence | Passed on both chains within the installed 300-second timeout. |
| T8 | Report and recipient reproduction | Transferred to M30/#35 under D30 | Independent Backlog; not an ETL functional completion criterion. |

##### Verification Results

ETL functionality verification is complete within the declared scope. There is no remaining ETL functional acceptance check in this issue.

| Observation | Monotonic seconds before normal finish | Required/observed passes | Final physical/HTTP | Normal stop |
| --- | --- | --- | --- | --- |
| Shortened | 86416.387 | 312/312; no missing, duplicate or unexpected pass | Passed | 12.516 seconds; return code 0 |
| Default | 86415.088 | 27/27; no missing, duplicate or unexpected pass | Passed | 13.770 seconds; return code 0 |

Both observations span UTC midnight on the same boot and retain 290 in-window full samples. Each chain passed read-only initial, later regular-pass checkpoints for both transitions and final physical/HTTP comparisons. All original manifests, terminal records, tool identities and unsuccessful attempts remain unchanged.

The original terminal/aggregate verdicts remain `Incomplete`. The retained evidence identifies kernel cursor diagnostic refusal propagating into final collection/pass waiting, JFR comparisons including earlier JVMs and aggregate evaluation preceding final terminal persistence. Actual native reevaluation and recording-PID reconciliation established those tool defects without rewriting inputs. Historical failed kernel-query contents were not retained, so complete historical kernel coverage is not claimed. These tool findings are recorded in #34 and #35 and do not reverse the supported ETL processing result.

###### Detailed Verification Evidence

Dated earlier rows preserve their actual results and original scopes; D30 controls current completion criteria.


Earlier dated rows retain their original scope and outcomes. The completed full-day reconciliation is recorded above and in the following rows.

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T2 existing shortened E4 | 2026-10-15T17:39:50.066490+00:00 | Actual stopped additional-test deployment and frozen native readers; original files read only | Passed for observed automatic-abort behavior; original controller/native short observation Incomplete | Two full fault samples at 15:55:00.707457 and 16:00:00.364564 UTC could read neither journal nor four application files; actual native counters 1 then 2 triggered one automatic abort. The appliance stopped with rc 0 in 11.878069368991419 seconds, final capture had no errors and the sampler configuration was exactly restored. One successful 903-job pass existed during the fault. Literal plannedAt comparison found zero matches; native nanosecond comparison found exactly one. Evidence: private E4-owner-verification-20261015-001.stdout SHA256 3101a45cda7378620eda34768980766c85da828a1156df3c439261e41a9240b7. All original hashes and bundle unchanged; no guest mutation. |
| T1/T2/T8 shortened E3 journal-unavailable File-evidence case | 2026-10-15T15:28:33.259827+00:00 | Control host; preserved additional-test originals in two isolated read-only recipient namespaces; no current guest changes | Passed for the shortened source-availability expectation; original runtime/native terminal Incomplete and parent tests incomplete | Two actual full fault samples at 2026-10-15T10:00:00.148271+00:00 and 10:05:00.222108+00:00 proved failed journal access with all four original application files readable; native collector identity matched sampler journal events. The real 10:00 UTC scheduled pass processed all 903 jobs with no failure, abort, skip or overrun; independent source and collected pass records matched. No automatic abort request/invocation occurred and all observed abort-failure counters were zero. Exact sampler restoration, two error-free recovery samples and planned stop rc 0 with no terminal-capture errors were verified. All 1176 preserved originals and the 23-file native bundle remained unchanged; no input status, time, process identity, record or terminal result was rewritten. The shipped source reader, pass parser, abort classifier, evaluator and aggregator ran. Both complete recipient analysis results were identical; native evaluate/aggregate stayed Incomplete for deliberate early termination and declared journal faults. The observer had rejected its ISO journal-query timestamp; equal planned UTC instants were subsequently compared with the shipped nanosecond parser instead of unequal Z/+00:00 strings. This is recipient retained-evidence acceptance, not a completed exact guest/recipient scenario replay claim, default acceptance or full-day result. Archive SHA256 ee7d91dfa13cf6aaf0a55368282c4e7aa2c968b1fdb9260eb7f83df41138ed26; original runtime SHA256 a664ba6f1719ef0c07b6665de52a1feb897cb6aa2fa807b247f19c1389bc2d07; original terminal SHA256 e7531e29fc50d6ef27af7c3a6efa94f38eb8b5cbd437ec672c9be3912cf96123; analysis source SHA256 31b82b48980fcc287331b2610a4832bf5053451ca35e16b4bf90ef8d8866fb8a; result SHA256 25bec017d16f48dc55bf51155009863ae46ba1fcbec7b06bc42776d0c3097adc; frozen schema-6 bundle SHA256 4ec0987e3a788a44dbd6173ffdb3e41ef47074b87e9f33ffbfbc351612053f9d, carried by code commit 3ff784e. |
| T1/T2/T8 shortened E2 changed-module runtime | 2026-10-14T23:51:07.617946+00:00 | Separate additional-test deployment and independent recipient; actual frozen native tools and unchanged original inputs | Passed for shortened importable journal-study change; parent tests remain incomplete | The actual journal-only QUERY_TIMEOUT change from 60 to 61 remained importable. Real preparation/start/capture yielded two error-free full samples at 2026-10-14T23:47:36.104750+00:00 and 23:50:00.713053+00:00 before explicit abort, without an automatic abort request. All 23 frozen ETL dependencies remained unchanged; the unrelated source was restored. Guest and independent recipient executed the same frozen evaluator, numerical aggregator and scenario checker at original absolute paths and returned identical complete results without normalization. Original short native observation remains Incomplete after deliberate early termination; neither default E2, a full-day observation nor normal full-window finish is accepted by this case. Original terminal SHA256 de43cebfcd339cc9d5a939e528a944fc06d0403c350f01432c75a9efeaf56cd2 remains unchanged. Archive SHA256 8e91244ba5dc61f3b01656d0d628f3561ffe50e9fe80dd0842124d9e57822e63; matched guest/recipient result SHA256 379ccb1873e2984d03a139b93608bfdf4d4c00c138c6fb84ccb627b255fb43a0; private verification receipt SHA256 cade282a3f3f5377651cce549925817388826a69f9415f1b6fedfd66e8738898. Frozen schema-6 bundle SHA256 4ec0987e3a788a44dbd6173ffdb3e41ef47074b87e9f33ffbfbc351612053f9d, carried by code commit 3ff784e. |
| T1/T2/T8 shortened E1 failing-module runtime | 2026-10-14T23:06:53.942882+00:00 | Separate additional-test deployment and independent recipient; real installed ETL tools and unchanged original evidence | Passed for the shortened failing-module scenario; full T1/T2/T8 remain incomplete | The actual unrelated journal-study module imported successfully before the declared change and failed on import afterward. Native preparation, start and collection completed with unchanged ETL tools and runtime identity; two consecutive actual five-minute full samples had no errors and no automatic abort request. The planned explicit native abort completed successfully. Guest and independent recipient ran the same frozen evaluator, numerical aggregator and scenario checker against original absolute evidence paths and produced exactly equal complete results without normalization. The native short observation remains Incomplete because the configured 86400-second window was deliberately ended early; this scenario does not accept a full-day observation, normal full-window finish, the default failing-module case or other journal-change/fault cases. The original terminal remained unchanged. Archive SHA256 is 75626ead8368bce2733af77bd6493945c1642a9c45e0a4f1a227563ced7b9e25; terminal SHA256 is e590a955123fcbc93f3cbeed06f944419b5bba257ecad4dd469e42efc2f5f3c8. All 23 members match frozen schema-6 bundle SHA256 4ec0987e3a788a44dbd6173ffdb3e41ef47074b87e9f33ffbfbc351612053f9d, carried by code commit 3ff784e. |
| T5/T6 original full-day progress | 2026-10-14T20:01:21Z | Original shortened/default deployments; read-only service, source-identity and actual saved-sample inspection | Running; full-window acceptance Pending | Both sampler/finish timers remained active, all 903 PVs remained connected and archiving, original boot/invocation/JVM identities and frozen tools were unchanged, and no abort was requested. Both chains had actual Passed fixed-interval physical/HTTP comparisons for transitions 0 and 1. Both latest full samples still contained the existing kernel-journal diagnostic error. These observations neither remove that error nor establish full-window timing, resource, final-capture or stop acceptance. |
| T1/T2 separate E1 preflight and fresh retry | 2026-10-14T20:38:53Z | Separate additional-test deployment; actual native tools and fixed original inputs | Original preflight Incomplete before observation; fresh preparation Running | Actual health, empty-data and terminal preflights ran, but continuity stopped at 19:51:11 UTC before startup passes completed at 19:51:41/47 UTC. Original runtime SHA256 is 5f08f7473839ab32d0b1d38b8a88f4f6f79574781e52955e344a96b9250f878b. All 9532 declared original files matched the unchanged preservation archive SHA256 671061e0d12730f33170387c47f24bbe826659f8fff9aede1bb5f377e811f8a2. A distinct fresh initialization then completed actual instrument checks, waited for both real startup transitions and passed retained-original physical/HTTP continuity. The unrelated journal module actually imported before the challenge and failed afterward. One of seven real measurement snapshots existed; no additional runtime case was accepted. All 23 frozen members still matched the unchanged native bundle. |
| T4 separate shortened functional continuation | 2026-10-14T19:51:04.787508+00:00 | Separate dedicated Rocky 8.10 deployment; unchanged 903-PV fixture and actual native scheduler | Initial processing and subsequent regular-pass physical/HTTP continuity Passed; independence/fault cases Pending | The exact four scalar-double policy scope and all-903 configuration/population scope remain distinct. Actual transition cadences are 300/3600 seconds; STS/MTS hold 2 and gather 1 remain verified. Completed original result SHA256 `75f10a71134bdd33bc6d545384becaa9ac3c6097d678370960277b6fcdeb0c90`. The subsequent native instrumentation check passed with all 903 PVs connected and archiving, while preserving the first immediate-check HTTP 500 preparation failure as a separate Incomplete original. Neither this result nor current preparation completes journal-independence, fault/abort or full-window acceptance. |
| T1 local candidate checks only | 2026-10-13 18:10:38 UTC | Current control-host candidate; actual unit-test CLI | 67 local checks Passed; 48 evidence-dependent checks skipped | The 115-test suite completed with no failures. This is local parser/contract coverage, not live integration acceptance. The deployed candidate contains 23 frozen dependencies and no journal-study modules. |
| T1/T4 deployment and source preparation | 2026-10-13 18:12:17/18:12:20 UTC | Two fresh Rocky 8.10 deployments; Python 3.9.25; actual appliance and loopback fixture | Deployment/source preparation Passed; complete T1 and T4 Pending | Both frozen baseline Ansible deployments exited 0. Actual source pins are environment `482cf2939ea997064e4a2df64e3cb420681f4566` and appliance `162269e7db97f527626ba0b387933a8c47e8bb57`. All 903 PVs were connected and archiving; all effective configurations matched the selected chain with STS/MTS hold 2 and gather 1. Actual Log4j File events from all four JVMs retained PID/invocation identity; completed ETL pass records supplied both transitions, cadence, planned/start/end times, outcome and population outside journald. Five shortened and three default current-invocation source pass records were checked before functional start. Bundle SHA256 `dc1aeed5eb75b6485aa14f0afad498f1024fff181e03e013da7e3ac88cf36926`; private receipts retain native records, full configuration and preserved original preparation failures/tools. |
| T1/T4 preparation corrections | 2026-10-13 18:05:20/18:05:22 UTC | Actual dedicated guests and retained preparation results | Original preparations Incomplete; source conditions confirmed | The empty appliance produced real application events but no completed ETL passes, matching the installed native driver's empty-PV arming condition. After registration, all 903 PVs became ready and normal restarts exited 0, but the preparation checker let a Python 3.9 `socket.timeout` escape its `TimeoutError` handling. Actual target inspection confirmed these are different classes and all startup endpoints subsequently responded. The original results remain Incomplete. Only the focused driver and frozen manifest were replaced before functional execution, after preserving the complete original tools. No historical seed or observation had started. |
| T4 initial functional checks | 2026-10-13 18:16:15/18:16:17 UTC | Actual fresh shortened/default deployments, real native PB writer and scheduler | Initial functional processing Passed on both chains; regular continuity Pending | Actual starts were 18:12:17.440901 and 18:12:20.526017 UTC; initial completion was 18:16:15.640934 and 18:16:17.220844 UTC, giving 238.200033 and 236.694827 UTC seconds. These are measured initial-check durations, not three-hour or full-day observations. The actual writer/readback, normal automatic passes, physical movement/transformation/source retention/deletion and HTTP comparisons passed for the four scalar-double policy representatives. All 903 configuration/population checks preceded execution and all 903 live PVs reconnected afterward. Initial result SHA256 is shortened `d41b9c00498febeee47b2d76945f76068ff0ffc0b6aa7abbb82dca473197eb56`, default `fa08ee4fc32081498b389118402133d3fded1e6985ae777aec8656bd345f80a4`. The `--initial-only` jobs exited 0. Their overall focused results remain Incomplete while subsequent regular-repeat continuity is Pending. No manual tick, synthetic pass record, journal-study dependency or full-day start was used. Original preparation failures and their tools remain preserved. |
| T4 retrieved original evidence | 2026-10-13 18:24:07/18:24:10 UTC | Original per-chain archives and their frozen tools | Guest/local hashes and retained-record checks Passed | Shortened archive: 91822080 bytes, SHA256 `98bf0e6e87c8b128d80c6bc28bda9e2b56991359112c7283074964bb18c14ab2`; default: 90828800 bytes, SHA256 `b70eb9a02989b5d731c6b067aae31a728e595ac5f7b515e46556e1fdf6ea1e36`. Each original baseline had eight old events per representative. Actual LTS output and HTTP had eight raw events or four independently expected events for each lastSample_10/30/60 policy, matching values, timestamps, status, severity, order and raw event bytes; retained source-window contents were empty. Frozen baseline/retention/event/HTTP parsers checked the actual retained inputs. Local checks make no live-filesystem absence or full-observation claim. Original tools, preparation files, compiled helper, native pass records, snapshots and HTTP responses are private under each chain's `initial-evidence.tar`; `initial-local-check.json` records the comparison. Full independent observation replay and regular continuity remain Pending. |
| T4 preserved runtime | 2026-10-13 18:27:37/18:27:41 UTC | Actual running shortened/default appliances and fixture IOCs | Initial runtime/tools/population retained | Actual boot/invocation and all four JVM PID/start identities still matched each initial phase; the 23 frozen tool hashes were unchanged and all 903 expected PVs were connected and archiving. No observation manifest or active observation timers existed. Private `final-runtime-check.*` receipts retain the checks. This preserves the entry point for later authorized regular continuity; it does not establish that continuity or a full-day result. |
| T4 regular-repeat continuation | 2026-10-13 21:26:31 UTC | Original shortened invocation, tools, fixed historical inputs and real automatic scheduler | Shortened regular continuity Passed; full-day Pending | `focused.py continue-initial --chain=shortened` began at 21:26:00.412898 UTC and completed at 21:26:31.680391 UTC. Real subsequent passes, repeated physical/HTTP checks, final effective configurations and original evidence/tool identities passed without an added seed or manual tick. Original result SHA256 `05585843648e98316093d261f55774d5e93221b5b95458c5875ddcf3ff608326`. Default continuation began at 21:26:02.378201 UTC and was still present at 21:56:57 UTC, waiting for its next regular transition; its original runtime and bundle are unchanged. |
| T3 continuity consumer correction | 2026-10-13 22:07:29 to 22:13:10 UTC | Actual shortened continuity CLI, original Passed result, real physical data and HTTP | Original consumer refusal reproduced; candidate continuity Passed | The original consumer rejected its own unchanged current dependencies against a historical replacement list. The candidate first accepts an exactly unchanged dependency and otherwise retains explicit approved replacement hashes. Actual pre-correction continuity exited 1; the candidate CLI exited 0, preserving original result SHA256 `05585843648e98316093d261f55774d5e93221b5b95458c5875ddcf3ff608326`. Continuity proof SHA256 `98d785e025f68fccc42e81f11f2fe383769b5b3d0d653b39f7e3b7d3b3380d3c`. Complete original focused evidence was preserved before tool replacement, archive SHA256 `c4ca29147e9315a6b8a3d51e4bb4156ab7b61b4bffc10369ec265a63efaa0079`. |
| T1/T3 measurement preparation, shortened | 2026-10-13 22:16:30 to 22:20:39 UTC | Actual shortened deployment; replacement frozen bundle; four real instrumented JVMs | Instrument installation/readiness Passed; measurement Running; full-day Pending | Bundle SHA256 `66ca20a8c14355922a03ebb305c0160477c737565af789132bcd5fb010bdf35b` preserves the independent File appender during measurement installation and removes capacity forecasting from preparation/start/launch. Source frequencies, 903-PV fixture and fixed historical input remain unchanged. Four real JFR recordings, GC logs and configured independent application-file paths were verified after the shortened-only restart. The initial post-restart population checks were retained; readiness completed at 22:17:16.726771 UTC. The first real measurement round was written by 22:20:39 UTC; remaining rounds and preparation have not completed. Initialization SHA256 `d70d8fe076652b3135bbc6cc08c54dfe3540e48265976503aa0b690632b36ace`. The default continuation was not restarted or modified. Local source checks ran 115 tests, with 67 Passed and 48 evidence-dependent skips; they do not establish live measurement or full-window acceptance. |
| T4 default regular-repeat continuation | 2026-10-14 00:10:34 UTC | Original default invocation, tools, fixed historical inputs and real automatic scheduler | Default regular continuity Passed; full-day Pending | The continuation completed at 00:10:34.226631 UTC after waiting for the actual regular grid. Subsequent passes and physical/HTTP comparisons passed without another seed or manual tick. Original result SHA256 `21af5f99d867305890fb4ed36f3600f50010b9fa8ebe0fbc0a8cc2da47dd5b83`. The default tools and original focused evidence were preserved before measurement installation; archive SHA256 `6d166f8f826f9cb7247f7a8c105a3bba9282293fa735e37c8568a284de1b5626`. This actual waiting interval is separate from the approximately three-hour functional allocation. |
| T3 measured preparation | 2026-10-13 22:17:16 to 22:47:23 UTC; 2026-10-14 01:40:22 to 02:10:29 UTC | Actual shortened/default deployments and four instrumented JVMs per chain | Seven measurement rounds and preparation completed on both chains; full-window measurement acceptance Pending | Shortened measure ran 22:17:16.727880 to 22:47:22.587775 UTC, followed by preparation at 22:47:23.383219 UTC. Default measure ran 01:40:22.837383 to 02:10:28.440308 UTC, followed by preparation at 02:10:29.181250 UTC. Both used real five-minute rounds. Actual heap/pause events existed for all four JVMs, no JFR data-loss events were reported, all 903 PVs had recent samples and six probes were visible with no retrieval errors. Default initialization SHA256 `bd08f62da8f6f9c688a0923f72ccf2c85a58bdbacde6e77a02b0de35a7d65d33`. Preparation and later full-window clocks remain distinct. |
| T2 original terminal probe | 2026-10-14 01:44:58 to 01:45:25 UTC | Actual shortened appliance; original installed terminal/collector CLIs | Terminal verification Failed; retained abort result Incomplete | The real whole-unit stop exited 0 in 11.460486258998571 seconds. The early-finish/repeated-terminal guards and four GC components were present, but final File capture refused the stopped JVMs and the terminal verifier exited 1 with `final_journal`. No full-day observation had started. Original failed probe, abort result, source tools and captured records remain unchanged. |
| T1/T2 post-stop capture regression | 2026-10-14 01:57:17 UTC; default installation at 02:13:25 UTC | Actual stopped shortened appliance, retained real terminal inputs and shipped collector CLI | Original refusal reproduced; corrected capture and missing-identity refusal verified | The preserved old CLI exited 1 against the original retained stopped-state inputs. The corrected CLI exited 0 and captured real remaining File records from mgmt 23, engine 917, ETL 5 and retrieval 7; no additional ETL pass was inferred. A separate filesystem-boundary copy lacking one required process identity was refused. No internal substitute or reconstructed journal fixture was used. Bundle SHA256 `3a9d21cc03c2c10d89e52b9bc710fb715ed86aed2393256fe19a6e460e597a72`; only the collector and its explicit continuity replacement hash changed from the measured bundle. Measurement dependencies and original seven-round inputs stayed unchanged. Before-update evidence archives: shortened `1493f3e5aa9c7e188a84ff7e1e297591f166549d018334839eac9ef29309f3bf`, default `75df64ce455b0f712030c3c1b5ae62639fd9043e9ba4e6fc86cc70a4b7083b24`. Local CLI checks ran 115 tests, 67 Passed and 48 evidence-dependent skips; these do not establish full-window acceptance. |
| T1-T3 full-day preflight | 2026-10-14 02:07:07 to 02:10:22 UTC; 02:13:26 to 02:16:33 UTC | Actual installed shortened/default runtime, terminal and continuity CLIs | Required start checks completed; readiness findings empty | Health, real empty-data detection, terminal handling, post-terminal health, chain and final health exited 0 on both chains. Corrected terminal probes completed at 02:08:02.886738 and 02:14:14.621187 UTC after real stop/restart. Early continuity attempts remained refused while genuine startup pass evidence was absent; later actual attempts Passed at 02:10:10.262106 and 02:16:21.884905 UTC. No synthetic pass or added historical input was used. The 903-PV readiness and independent File capture were verified before each observation. Private per-chain `full-day-launch-monitor-*002*.stdout` retains every actual step and unsuccessful attempt. |
| T5/T6 full-day starts | 2026-10-14 02:10:54/02:17:02 UTC | Independent shortened/default deployments; frozen 23-file ETL bundle | Both Running; full-window acceptance Pending | Shortened t0 is 02:10:54.145355 UTC, earliest normal finish 2026-10-15 02:10:54.145355 UTC; manifest SHA256 `52f1e97cdf9de3e1459758f02b07a671677f016ea89e2dc9e0c20abb63b9fc60`. Default t0 is 02:17:02.827005 UTC, earliest finish 2026-10-15 02:17:02.827005 UTC; manifest SHA256 `47e079c6db560829e15ec147e52a226c76103961af9d1b230f0872cb1da0a098`. Each freezes 86400 seconds, actual UTC/monotonic clocks, boot/invocation/JVM identities, effective configuration and bundle `3a9d21cc03c2c10d89e52b9bc710fb715ed86aed2393256fe19a6e460e597a72`; start findings were empty and initial full samples had no errors with 903 connected/archiving PVs. |
| T5 in-window physical checkpoint, original | 2026-10-14 02:20:30 UTC | Actual running shortened observation; preparation-only continuity command | Incomplete; preserved unchanged | The real command refused with `An existing observation cannot be changed` before the PB/HTTP comparisons. No physical mismatch or ETL failure is inferred from this guard. Original `physical-checks/regular-transition-0/result.json` remains retained. Neither observation was restarted or changed. |
| T4/T5 read-only physical checkpoints | 2026-10-14 02:38:51 to 02:46:07 UTC | Actual running deployments, original fixed inputs and unchanged shipped PB decoder/policy/HTTP comparators | Initial checkpoints Passed on both chains; shortened regular transition 0 Passed; remaining regular/final checks Pending | Executor SHA256 `cd104bb48182aae75fd32d6d69d16ae03191e15c2ad74641761a37789cffa7d1` reads all 903 real effective configurations and exact physical/HTTP contents for the four policy representatives. Shortened initial result SHA256 `0f050300e782a3bb663e8c997bed7743edef55b05d3d04ace7eb85b9dbc430e4`; default `125a4a8184623f29e0a987254b1231dc3e89983101d49c0f59b48306b1769260`. Shortened's regular transition 0 comparison completed at 02:39:06.044781 UTC and retained its actual native trigger pass. Each capture preserves actual configurations, PB snapshot, HTTP responses, original expectation files, complete native pass prefix, times and hashes. It does not run or bypass the preparation command. Separate read-only services await each remaining transition; final read-only commands are loaded on both finish services. The executor is outside the frozen native bundle. T5 requires these regular/final results in addition to the native scheduler verdict. |
| T5/T6 current runtime | 2026-10-14 02:47:05 UTC | Both actual running full-day observations | Runtime and frozen package retained; full-day Pending | Boot/invocation and all four JVM identities matched each observation manifest. All 23 frozen dependencies were unchanged; sample/finish timers were active, read-only comparison processes were present and final commands were loaded. Both latest 02:45 samples retained 903 connected/archiving PVs with no errors. No abort request existed. Private per-chain `active-observation-003.*` receipts retain the recheck. |
| T1/T3 completed-record inputs and preservation | 2026-10-14 06:01:37 UTC | Control host only; copies of completed 2026-09-29/30 shortened/default records, separate actual GC logs and retained deletion-race command result | Input identity and original preservation Passed; current observations unaffected by this work | The two original 86400-second observations ended on 2026-09-30 at 01:06:43.213206 and 01:06:46.048027 UTC. Original archive SHA256 values are shortened `9c416567299e2b6ca6143bc0ada972998890f43bbfcce7e0e861db231eaef5f9` and default `001430f3d2421a6ade2cfe1d2738c8c94049271b28d5d5db01a2175a1b7d4714`; separate GC-log archives are `f8c60e1dd8a9502aab52e6ea4c2960876f05573bb441914d5dea7900da8eb535` and `27b7b988b85c3de070ce4b4af87bf52cee4f6ebdcb74bff956bc743dbc8a41bb`. Every extracted file matched its real archive member. Source archives, retained du input, base copies and shipped tools remained unchanged after execution. No current VM connection, service operation, runtime file change or active-observation input was used. Evidence is private `work/etl-offline-completed-20261013/run-20261014T060056.559753Z/`; report SHA256 `05337f1a8bc8e26e58e926f78125803173cd2c0bbe5efac473a0f5312136ba97`. |
| T3 retained export, GC and deletion-race checks | 2026-10-14 06:01:37 UTC | Current shipped code copied from frozen bundle `3a9d21cc03c2c10d89e52b9bc710fb715ed86aed2393256fe19a6e460e597a72`; original completed inputs | Four retained-export tests, both GC-log reconciliations and actual du-result parsing Passed; full T3 Pending | The real `test_contract.RetainedExportsTests` ran four checks with no skips: actual two-chain schedules, overlapping GC exports and pause totals, conflicting real-record derivative rejection, and actual cumulative rate semantics. Shipped aggregation reconciled every retained JFR GC ID with actual complete GC logs for all four JVMs on both chains. The shipped `collect.tolerated_du` consumed the unchanged actual deletion-race result, SHA256 `3f2aeedbe309b17cf4d9812366cae27527e4a038c9cd36e68dfc9752da24d8d0`, preserving its measured 376600 bytes despite its observed return code 1. No internal function was substituted. These are retained-input checks; they do not recreate a live deletion race, establish current JFR accumulation behavior or complete the metrics/pass-overlap and other remaining runtime cases. |
| T1/T8 retained-record dependency and replay checks | 2026-10-14 06:01:37 UTC | Actual shipped bundle verifier and aggregate CLI; isolated tool copies and unchanged completed schema-2 inputs | Dependency guard and exact replay comparisons Passed within historical-input scope; overall historical aggregates Incomplete; full T1/T8 Pending | With unrelated journal-study modules absent, failing on import, or changed, the real bundle verifier exited 0 and each chain's actual aggregate CLI reproduced exactly the same JSON and exit status. Changing the copied ETL collector without changing its frozen manifest was refused with exit 1. Each historical input had 289 actual full samples; actual parsed pass counts were shortened 288/24 and default 24/3. Historical aggregate verdicts stayed Incomplete: shortened retained `health` and `retrieval_outcomes`, default retained `retrieval_outcomes`; both lack the current observation schema, historical coverage contract and actual jstat request bounds. No missing fields, process history or successful result were invented. Exact output equality on these historical inputs does not establish the complete current deployed independence path or current full-day acceptance. All commands, actual outputs, per-file hashes and both the first and GC-complete recheck reports remain private under `work/etl-offline-completed-20261013/`. |
| T5/T7 full-day shortened | 2026-10-15 | Stopped original deployment; actual frozen native evaluator and pass parser | Passed for ETL processing; original aggregate Incomplete preserved | 86416.38661314899 monotonic seconds across UTC midnight; 312/312 passes with no missing/duplicate/unexpected entries; native scheduler Passed. Four read-only initial/transition/final physical/HTTP results Passed. Normal stop rc 0 in 12.516135794998263 seconds below 300-second timeout. Original records, manifest and installed tools unchanged. Private read-only report SHA256 5f230f2e84af096f4ba2d3fd05db4e9a0e308ec548d5fe9da6d1d081dfcb635e. |
| T5/T7 full-day default | 2026-10-15 | Stopped original deployment; actual frozen native evaluator and pass parser | Passed for ETL processing; original aggregate Incomplete preserved | 86415.088157011 monotonic seconds across UTC midnight; 27/27 passes with no missing/duplicate/unexpected entries; native scheduler Passed. Four read-only initial/both-transition/final physical/HTTP results Passed. Normal stop rc 0 in 13.769559552994906 seconds below 300-second timeout. Original records, manifest and installed tools unchanged. Private read-only report SHA256 7f557adb77ea464e42f5284f75da08abd9351d6ecd33512cfce67b3877c9c35c. |
| T3/T6/T8 full-day tool diagnosis | 2026-10-15 | Both stopped original deployments, actual frozen evaluator and native CSV deduplicator | JFR integrity/matching-PID reconciliation Passed; evaluator and collector defects diagnosed | All twelve heap/collection/pause counts per chain match the final recording PID; JFR full-window coverage, hashes/bytes and zero recorded data loss confirmed. Native reevaluation after terminal persistence removes coherent_manifest_and_terminal. Kernel cursor refusals in 240/237 full samples propagated into required_pass_wait/final_sample/final_journal despite complete application ETL evidence. Failed query bytes were not retained; historical kernel coverage remains unresolved. No candidate code or original status was rewritten. D29 assigns corrections to independent M29/M30 Backlogs. |
| T1-T3/T6/T8 tool follow-ups transferred | 2026-10-15 | Completed observations and existing tool records | Transferred to M29/M30; not an ETL completion condition | D30 moves every remaining package/source-fault/measurement/report/recipient expectation to independent Backlogs #34/#35. The actual shortened E4 fault/abort behavior Passed retained-original verification; original controller/native short-observation Incomplete records remain unchanged. No further ETL functional acceptance check is outstanding. |

##### Closure Evidence

- Complete on 2026-10-15 within the D30 actual ETL functionality scope. All six criteria are supported by the retained real input, physical/HTTP, scheduler and whole-appliance stop evidence.
- Both original full-day observations Passed: all 312 shortened and 27 default required passes present exactly once, repeated/final physical comparisons successful and orderly stops within the actual installed timeout.
- GitHub #30 observed closed with reason completed at 2026-10-15T18:09:12Z; read back at 2026-10-15T18:09:48.234Z. Published body SHA256 a1bca7810231262b68cb09a1b4feea3194d9e7927bbcd85fc6d9881b71e63134 remained unchanged with six completed and zero incomplete criteria.
- Closure comment: https://github.com/jeonghanlee/ansible-provision/issues/30#issuecomment-6198957585; exact approved content verified before closing, SHA256 51a91a901d6a9e9bb1cb96e59dfa38f9811e03c8fefb2531e2265df919c99ff2.
- The deployed product and frozen observation tools were unchanged during retained-original reconciliation. D30 requires observed ETL behavior rather than future tool implementation; M29/#34 and M30/#35 remain independent Deferred Backlogs.
- Original Incomplete collector/evaluator/controller records and all unsuccessful attempts remain unchanged. Documentation/source-preservation changes remain uncommitted; no commit, push or production-code change is claimed by this closure.

##### GitHub Projection

- Issue: #30, https://github.com/jeonghanlee/ansible-provision/issues/30
- Title: `Verify ETL processing independently of journal validation`
- Observed State: closed (completed)
- Labels: `enhancement`
- Milestone: `Backlog`
- Assignee: `jeonghanlee`
- GitHub Updated At: 2026-10-15T18:09:12Z
- Last Compared: 2026-10-15T18:09:48.234Z; closed/completed state and unchanged six-criterion body verified; independent Backlogs #34/#35 remain open.
- Body: actual ETL functionality complete; tool follow-ups in #34/#35. Published body SHA256 a1bca7810231262b68cb09a1b4feea3194d9e7927bbcd85fc6d9881b71e63134.
- Prepared Body: purpose/Backlog scope correction applied and read back; SHA256 a1bca7810231262b68cb09a1b4feea3194d9e7927bbcd85fc6d9881b71e63134.
- Applied Update: 2026-10-14T19:55:12.022571+00:00; 8 main tests retained with 1 completed main tests. Checked subitems and satisfied acceptance clauses total 20; unchecked parents remain incomplete. The issue remains open.
- Applied Update: 2026-10-14T23:34:45.218297+00:00; shortened E1 completed subitem added after actual failing-module runtime and exact guest/independent-recipient frozen replay. All 8 main tests were retained with 1 completed main test; checked subitems and satisfied acceptance clauses now total 21. Default E1 and incomplete parent tests remain unchecked; the issue remains open.
- Applied Update: 2026-10-15T08:55:28.023180+00:00; shortened E2 completed subitem added after actual changed-module runtime and exact guest/independent-recipient frozen replay. All eight main tests retain their prior states with one completed main test. Checked subitems/acceptance clauses total 22; default E2 and all incomplete parents remain unchecked. Issue #30 remains open.
- Applied Update: 2026-10-15T15:51:52.911065+00:00; shortened E3 retained-original source-availability completion added after actual fault/recovery/stop evidence and two exactly matching read-only recipient analyses. All eight main-test states remain unchanged with one completed main test; checked subitems/acceptance clauses total 23. Original E3 runtime/native terminal remain Incomplete, and no exact completed guest/recipient scenario replay or full-day acceptance is claimed. Default cases, the all-sources-unavailable automatic-abort case and incomplete parents remain unchecked. Issue #30 remains open.
- Applied Update: 2026-10-15T17:13:42.007Z; both original full-day ETL processing observations accepted from unchanged actual evidence. Created independent M29/#34 and M30/#35 as Deferred Backlogs, with no corrective implementation authorized. Body exactly matched SHA256 `9d92a5a7ef29b8ae2d43cc42c902c21340adb64fb3484a5ea1ba72934fbf299e`; issue #30 remains open with 34 checked items.

- Applied Purpose Update: 2026-10-15T17:52:30.345Z; body SHA256 a1bca7810231262b68cb09a1b4feea3194d9e7927bbcd85fc6d9881b71e63134; exact readback and unchanged metadata verified.

- Functional Completion: Passed; all six criteria satisfied; issue #30 closed completed at 2026-10-15T18:09:12Z.
- Closed At: 2026-10-15T18:09:12Z
- Closure Comment: https://github.com/jeonghanlee/ansible-provision/issues/30#issuecomment-6198957585

<details>
<summary>Historical combined ETL plans and verification</summary>

The following text is retained unchanged as historical evidence. Its authorizations,
test labels, capacity calculations and journal dependencies do not override D27 or
the current independent plan. Use each original frozen bundle for historical replay.

##### Retained-Record Recheck Proof Consumer Amendment (2026-10-09)

Plan Status: accepted
Plan Acceptance: 2026-10-10, the owner accepted this plan after independent review reached no finding above the floor at `eaf1376`
Implementation Authorization: 2026-10-10, the owner authorized implementation of Ordered Work 2 and 3, the consumer path and its local rehearsal on the control host, and then directed Ordered Work 4, the bundle freeze, the replacement step's literal and the request for independent review; each guest operation (T29 and T30 on a guest, the delivery, T31, T32) still requires its own separately recorded execution authority

Decision Date: 2026-10-09. The owner authorized amending the plan so the focused-proof
consumer can accept the retained-record recheck proof while the original focused result
stays Incomplete. This authorizes the plan text only. Review, acceptance and
implementation authorization are recorded separately above after they occur.

Decision Date: 2026-10-09. After review of the draft, the owner selected binding the proof
identity to the original focused execution instead of the current identity, and naming the
tool files that the delivered bundle changes in the approved list instead of requiring
every tool hash to equal the recheck-time inventory.

Decision Date: 2026-10-09. After the independent review of the draft, the owner accepted
all findings: the approved list pins only `PBFixture.java`, `focused.py` is excluded by
name and bound through `verify_bundle`, the accepted `bundle.json` SHA256 is enforced in
the replacement step instead of the consumer, the key-input comparison uses the original
inventory, the negative cases map every condition, and the replacement step fixes its
sibling names and rollback.

Decision Date: 2026-10-09. After the third independent review, the owner selected running
T29 and T30 on the guests with a private copy of the frozen bundle as the explicit bundle
root, after the freeze and its review and before the delivery, instead of letting the
tools comparison of T29 accept two `PBFixture.java` values. The candidate consumer runs
from a private staging directory; the claim that the retained-record recheck ran the
same way is withdrawn because its invocation was not retained.

Decision Date: 2026-10-10. The owner accepted the implementation of Ordered Work 2 to 4 as
frozen at `169ca96` after the independent review returned no finding above the floor.
This accepts the consumer path, the replacement step and the frozen bundle only; Ordered
Work 5 to 7, every guest operation, still requires its own recorded execution authority.

Decision Date: 2026-10-10. The owner authorized the guest execution of Ordered Work 5 to 7
on both retained cold guests: T29 and T30 on target Python 3.9, the delivery with T31, and
the continuity run T32. The authority covers only these operations on the frozen bundle
accepted above. It does not cover a restart, reseed, registration, a manual tick, a new
focused run, instrumentation, measured preparation, capacity renewal or any observation;
a failure of a check stops the sequence for the owner.

Decision Date: 2026-10-10. The owner accepted the guest results of T29 to T32 recorded in
the Verification Results, after the independent review closed them without a finding above
the floor. The acceptance covers the focused proof gate through the recheck proof and the
installed frozen bundle on both guests; instrumentation, measured preparation, negative
and abort checks, final-restart continuity, capacity and readiness gates and both
observations stay pending and need their own plan steps and recorded authority.

Decision Date: 2026-10-11. The owner approved the first tool replacement after the recheck
inventory: `journal_retention.py` at SHA256
`d9210972cbc2511c57357de6bc4c0e4063ba53664cc8d1cf837a5d3353ab1d74`, which corrects the
journal configuration check (M25 T6). `RECHECK_APPROVED` gains a `replacements` map by
name and digest, and `check_recheck_tools` accepts exactly those digests beside the
excluded `focused.py` and the approved helper; any other tool change still refuses. The
newly frozen bundle is
`43970448a8c23f48cb43c40966e98732a652409a5fdfe3d4dfcc5e65cbfe8c17` (changed members
`focused.py` `a9f74a5798873c029070ec0e0f19bc9ba4ea34bf9d70e906e8048190255f9217` and
`journal_retention.py` above); the replacement step literal follows it, and the retained
pair's recheck proofs stay consumable under it. The regression
`test_tools_comparison_allows_only_the_approved_replacements` now also refuses a second,
unapproved `journal_retention.py`.

Decision Date: 2026-10-11. The first launch attempt on the shortened guest was refused at
the launch continuity: for a Passed original result `continuity` compared the focused
result's run-time tool hashes with the installed bundle strictly, so the approved
replacement above did not apply there. The owner extended the rule: `continuity` now
compares `artifacts`, `pvs` and `flags` strictly and the tools through the same
`check_recheck_tools` as the recheck branch (`compare_focused_configuration`), and the
branch selection between a Passed original and a recheck proof is one function,
`check_focused_continuity`, that `continuity` calls. The regressions run on the retained
Passed focused records of both fresh guests (their `result.json` and final-inspection
inventory, kept privately in `work/m22-clean-20261010/focused-passed/` and selected by
`FOCUSED_PASSED_EVIDENCE`) and on the retained recheck records: the strict comparison
refuses the delivered bundle, the new comparison and the selector accept it on both
branches, and an unapproved tool change or a changed flag is refused on both. The
newly frozen bundle is
`d72cfc575cf1603d5303e448940756608d9c4b7c75fc314f441faceb61f31178` (changed member
`focused.py` `814152eba1d235109f793e8d847ea8ace2647885cf93ec2671db63a46daad62d`); the
replacement step literal follows it.

Premise: the original `result.json` receives `artifacts`, `pvs`, `flags`, `tools`,
`source_manifest_sha256`, `baseline_sha256`, `evidence_sha256` and `helper_sha256` only
after the final comparison passes, so an Incomplete original carries none of them.
`verified_focused_result`, `continuity` and `require_continuity` each bind to that file.
The recheck proof is a separate, hash-bound record of the same execution. The consumer
therefore needs its own acceptance path, not a relaxed Passed check.

Consumer acceptance conditions:

1. The original `result.json` stays Incomplete with the exact error
   `Effective configuration changed during focused execution`, and its SHA256 equals the
   proof's `original_result_sha256`. It is never edited or replaced.
2. Each chain's recheck proof is named by an explicit path and SHA256 literal in a reviewed
   approved list inside the shipped consumer (`focused.py`), never by glob, newest entry or
   a path read from the evidence tree it vets. The proof result is Passed and its chain
   matches. The approved entries are:
   `/var/lib/etl-focused/shortened/recheck-20261009T233038265889/result.json`
   `eb5e0f73b134e34e4ad35603b0894ed24b597fd6916bdd765e485a8ee5041977` and
   `/var/lib/etl-focused/default/recheck-20261009T233038375804/result.json`
   `491bca76b849d53061b4d486ede58c6f877c776154f2dd079eca9e07673c8897`.
3. At consume time every `source_evidence_sha256` and `recheck_evidence_sha256` entry is
   re-verified. Live `passes-*` files stay excluded as in the recheck. Files that
   continuity creates later lie outside the recorded sets.
4. `checker_sha256` and `helper_source_sha256` equal approved literals of the producing
   version, not the hash of the running file: `focused.py`
   `4265dfac7f62cb99e0a03a5db981a3449a37dc51365f05c156a5a20d3e264fd3` and `PBFixture.java`
   `df29f030028d9c920c30a2faf360045b4595b40258666ef5dff7ab4939e4fb7d`. The consumer change
   alters `focused.py` and `bundle.json`; the approved list must still name the producer.
5. `expected_keys_sha256` matches, the key-input PV names equal the 903 PV names of the
   original `inventory.json` (the manifest lists only the four selected PVs), the
   original deployed properties hash equals the original inventory value, and the
   converter helper is bound by `helper_source_sha256`. No key is regenerated at consume
   time.
6. Configuration and identity at consume time:
   - `artifacts`, `pvs` and `flags` of a fresh inventory equal strictly those of the
     recheck directory's `inventory.json`, which is hash-bound in
     `recheck_evidence_sha256` and already holds the generated keys. The
     null-to-generated allowance is not carried into the consumer. Under T29 the fresh
     inventory is written to the private staging directory, never under the retained
     tree; continuity (T32) writes it beside the retained records by design, outside
     the recorded sets of condition 3.
   - `tools`: every tool file equals its recheck-time entry, except two. `PBFixture.java`
     must equal its approved literal (the `df29f030…` value of condition 4). `focused.py`
     is excluded by name, as the resume path already does, because a file cannot carry
     its own hash. The installed bundle as a whole, `focused.py` included, is bound by
     `verify_bundle` against the frozen `bundle.json`. The accepted `bundle.json` SHA256
     is a literal in the bundle replacement step of Ordered Work 6, which lies outside the
     frozen bundle, and is enforced at delivery (T31); the consumer cannot pin it,
     because `bundle.json` contains the `focused.py` hash. Against the retained recheck
     inventories exactly `focused.py` and `PBFixture.java` differ on both chains.
   - The proof `identity` equals the identity recorded by the original focused execution
     (final-inspection `inventory.json`, bound in `source_evidence_sha256`). The pre-run
     `inventory.json` identity differs by design: it was taken before the run's own
     normal stop, seed and start. The proof identity is not compared with the current
     `identity()`, which changes at planned restarts; the existing check that identity
     stays unchanged during a continuity readback is kept. Consequently the proof is no
     longer tied to the running appliance; the remaining ties are the per-invocation
     startup pass check and that readback stability check.
7. `continuity` and `require_continuity` bind both the original result hash and the
   recheck proof hash.
8. Any missing or mismatched item fails as today. Instrumentation, measured preparation,
   negative/abort checks, final-restart continuity, readiness/capacity gates and the
   86400-second observation requirements are unchanged.

###### Ordered Work

1. **Review and accept this plan.** Independent review, owner acceptance and a separate
   implementation authorization precede every later item. That authorization covers
   local implementation and verification on the control host only; every guest
   operation (T29 and T30 on a guest, the delivery, T31 and T32) requires its own
   separately recorded execution authority. Closed by the recorded Plan Status, Plan
   Acceptance and Implementation Authorization above.
2. **Implement the consumer path.** Planned paths are
   `tests/archiver-soak/etl-pass/{focused.py,test_focused.py,bundle.json}` and
   `tests/archiver-soak/{README.md,SHA256SUMS}`, plus the bundle replacement step of
   item 6: it is not a member of the frozen bundle, its path is fixed at implementation,
   and its SHA256 is recorded in the review record after the accepted `bundle.json`
   SHA256 literal is filled in at the freeze of item 4. The acceptance path is a separate
   function; the Passed requirement of `verified_focused_result` for a new focused run
   stays unchanged. The callers `launch-retest.py` (`continuity`) and `observe.py`
   (`require_continuity`) are bundle members and are not changed: the tools comparison
   of condition 6 would reject either change, so a needed change to them requires a
   plan revision. Closed by the local rehearsal of item 3 for the conditions it covers,
   by T29 and T30 of item 5 for the guest-only conditions, and by T31 for the
   replacement step.
3. **Rehearse locally on the control host.** Run the real shipped consumer against local
   extracted copies of the retained final and recheck evidence, with the copy root and
   a private copy of the candidate bundle directory of the working tree as explicit
   arguments, because the control host has no installed bundle. Negative cases mutate
   copies of that real evidence; no internal span is replaced by a stub or a
   hand-built fixture. Host Python is 3.13 and is not target compatibility evidence.
   The acceptance path reads live appliance state that the control host does not
   have: `inventory()` calls the management API, `identity()` reads systemd and JVM
   state and `artifacts()` reads the installed source and class tree. The rehearsal
   therefore covers conditions 1 to 5, the proof-identity binding of condition 6 and
   its tools comparison from the retained files. The fresh-inventory comparison of
   condition 6 (`artifacts`, `pvs`, `flags`), the identity stability during a
   continuity readback and condition 7 are guest-only: T29 and T30 of item 5 close
   the fresh-inventory comparison, and T32 of item 7 closes the identity stability and
   condition 7, both of which live in `continuity` and `require_continuity`. No fresh
   inventory is built by hand for them. Closed by the recorded local results with the
   interpreter version and the `focused.py` SHA256 each run used.
4. **Freeze the new bundle and request independent review of the consumer and of the
   bundle replacement step** as a new charter. Record the frozen bundle SHA256, fill it
   into the replacement step as its literal, then record the step's SHA256. Closed by
   the frozen bundle SHA256, the step's SHA256 and the review result.
5. **Verify on the guests on target Python 3.9** under recorded execution authority:
   T29 and T30 with a private copy of the frozen bundle directory as the explicit
   bundle root, so that they exercise the bundle that item 6 delivers. The candidate
   consumer is not installed on a guest at this point; it runs from a private staging
   directory outside `/usr/local/share/etl-soak` that holds only the candidate
   `focused.py` and `PBFixture.java`, is first on `sys.path`, and finds the installed
   modules through `PYTHONPATH` behind it. A script's own directory precedes
   `PYTHONPATH`, so the run records the file path of every module it imported. It
   writes nothing under the retained tree; the retained evidence is only read in
   place. Name the frozen bundle SHA256 and the `focused.py` SHA256 in the results;
   rerun both checks if either hash changes after review. Closed by the T29 and T30
   results recorded with the target interpreter version.
6. **Deliver without touching retained state.** No existing procedure replaces an
   installed bundle: the first installation extracted an archive into an absent
   directory and refused an existing one. This item adds a reviewed replacement step,
   kept outside the frozen bundle. It takes the frozen bundle, a directory or an
   archive, as an explicit argument, carries the accepted `bundle.json` SHA256 as a
   literal and refuses a bundle that differs. Its copy of the installed directory
   preserves ownership, mode, timestamps and the SELinux security context, so the
   service accounts that read the fixture files keep their access. The staged sibling is
   `/usr/local/share/etl-soak.new-<first 8 hex of that SHA256>` and the preserved
   sibling is `/usr/local/share/etl-soak.prev-<UTC timestamp>`; the step refuses when
   either already exists. It requires `etl-soak-sample.service`,
   `etl-soak-sample.timer` and `etl-soak-finish.service` to be inactive, and it never
   stops or starts a unit: a unit found active is a refusal left to the owner. It
   never restarts `etl-soak-ioc.service` or `epicsarchiverap-maven.service`, which
   stay active. It copies the whole installed directory into the staged sibling, then
   overwrites only the frozen bundle members and `bundle.json` there (`bundle.json` is
   not a member of `BUNDLE_FILES`, yet `verify_bundle` reads it). Every other file,
   such as `pvs-all.csv`, the fixture database files the IOC unit references and
   `register.py`, is carried over unchanged. It requires `verify_bundle` to pass
   in the staged sibling, then renames the installed directory to the preserved
   sibling and the staged directory into place. The two renames leave a short window
   with no installed directory, which is acceptable only because the units above are
   inactive and the running IOC and appliance have already loaded their files.
   Rollback has two renames, because a rename onto the existing installed directory
   would nest the preserved sibling inside it: first rename the current
   `/usr/local/share/etl-soak` to `/usr/local/share/etl-soak.rejected-<UTC timestamp>`,
   then rename the preserved sibling to `/usr/local/share/etl-soak`. The step prints
   both exact commands before its first rename. Delete nothing. Write nothing under
   `/var/lib/etl-focused/<chain>/`, recompile no helper (`helper-classes` stays the
   original compiled helper), and touch no retained evidence archive. Do not rerun `run`, `prepare-resume`, `resume`, the
   orchestration scripts, registration, seed or installation against the existing
   fixture. This is a guest operation under its own recorded execution authority. Closed by T31.
7. **Run continuity through the accepted consumer** on both chains, then proceed through
   the existing observation gates under separately established execution authority.
   Closed by T32.

###### Consumer Test Plan

| Check | Planned Real Path And Required Outcome | Execution State |
| --- | --- | --- |
| T29 consumer acceptance on retained evidence | On each guest on actual Python 3.9, the shipped consumer code runs from the private staging directory of Ordered Work 5 with a private copy of the frozen bundle directory as the explicit bundle root; only the evidence is read in place, under `/var/lib/etl-focused/<chain>/`: its retained original, final and recheck records. Accept both chains and return the configuration from the recheck inventory. Read-only on the retained tree; no restart, reseed or manual tick. | Pending |
| T30 consumer rejection of altered evidence | On each guest on actual Python 3.9, with the same staging directory and frozen bundle copy as T29: copies of the real evidence placed under a unique private directory outside the retained tree. The consumer receives the copy root explicitly and rebases the recorded absolute paths onto it; an unrebased path must fail. The bundle is likewise a private copy of the frozen bundle directory passed as an explicit bundle root. The approved list is an explicit consumer argument whose default is the shipped literals. A case that changes the proof itself supplies the changed proof's own SHA256, so that only the intended condition fails; the default literals are exercised by T29 and by the condition 2 cases. One change per copy, each failing with its own error: condition 1, altered error string and original result changed to Passed; condition 2, wrong proof hash, a proof path not in the approved list and the other chain's proof; condition 3, altered source file and altered recheck file; condition 4, wrong checker hash and wrong helper hash in the proof; condition 5, a changed key-input PV name, a properties hash mismatch and a wrong expected-keys hash; condition 6, `artifacts`, `pvs` and `flags` each differing from the recheck inventory, a changed identity in the proof, a changed `PBFixture.java` in a re-frozen bundle copy, and an unapproved changed tool file in a re-frozen bundle copy; an unfrozen change to a bundle file fails earlier at `verify_bundle` with its own error; condition 8, a missing recorded file. | Pending |
| T31 delivery preserves retained state | The replacement step first runs its real copy, rename and rollback path against a private parent directory holding a copy of the installed directory, then on each guest. Every non-bundle file of the installed directory is byte-for-byte unchanged after the swap, `inventory()` still reads `pvs-all.csv`, and the `ls -Z` security context of every file and of the directory itself is the same before and after. Before and after delivery, every `source_evidence_sha256` and `recheck_evidence_sha256` entry of both proofs re-verifies, the file list under `/var/lib/etl-focused/<chain>/` is unchanged, the installed bundle passes `verify_bundle`, its `bundle.json` SHA256 equals the literal in the replacement step, the previous installed directory is preserved byte-for-byte as a sibling, and the tool files that differ from the recheck-time inventory are exactly `focused.py` and `PBFixture.java`. | Pending |
| T32 continuity binding | Real `continuity` and `require_continuity` on the guests: both the original result hash and the recheck proof hash are bound; a proof from the other chain or a stale proof is rejected; identity is stable during the readback. No reseed or manual tick. | Pending |

##### Separate-Environment Preparation Amendment (2026-10-08)

Plan Status: accepted
Plan Acceptance: 2026-10-08, owner instructed proceeding with the reviewed revision; Maven review2 accepted SHA256 15c61e1b3d7451abc58b0f980c21c33fd3a994550312ac26fbef704ac9d6253b with no must-fix/minor findings
Implementation Authorization: 2026-10-08, owner instruction to proceed with preparation-tool implementation and verification under this revision; deployments remain ordered after tooling verification and implementation review

Decision Date: 2026-10-08. Prepare this revised plan and request Maven review.
The initial instruction authorized the plan document only. The subsequent owner
instruction authorizes implementation and verification under the reviewed plan.
The proposed execution scope preserves every existing guest, service, store and
failed-run record and uses two additional independent environments. Prior execution
authority does not authorize this revised preparation sequence.

Decision Date: 2026-10-10. The focused proof gate is met for both retained guests through
the recheck proof (Retained-Record Recheck Proof Consumer Amendment, accepted results of
T29 to T32). The owner authorized the guest execution of the fresh preparation on both
guests, each with its own `--chain`: `initialize-fresh.py instruments` and `check`,
`measure`, and `prepare`, as the shipped README describes them. The authority includes the
appliance restart that `instruments` performs and the roughly 45-minute measurement
under the 903-PV load, and excludes the runtime verification of item 8, the abort checks,
`launch-retest.py` and any observation; those need their own recorded authority. A failed
check stops the sequence for the owner, and preserved evidence is never replaced.

Prerequisite check against this record, 2026-10-10: since `D22` (2026-10-05) the journal
checks formerly T22 to T26 and T28 are `M25` T1 to T5 and T7, and `D22` and the superseded
artifacts of the Retention Accounting Correction state that `M22` opens an observation after
T27's preparation portion passes, not after those checks. `M25` stays In progress (T1, T2
and T5 not run; T3, T4, T7 and T8 partial; T6 preparation passed and its in-window path
corrected afterwards). The sequence authorized above produces T27's preparation portion
for these guests and claims none of `M25`'s checks. The local tool checks (T13) passed on
the frozen bundle. Read on both guests on 2026-10-10 (T14 inputs): the management API
lists all 903 PVs, each being archived and connected; the four appliance JVMs run with
`-Xmx256M` and no JFR or GC option; `/var/lib/etl-soak` holds fixture and continuity
records only, with no observation or preparation record, and the sampler and finish
units are inactive. Each guest also holds one idle `java` process (about 56 MB resident,
no listening socket) started on 2026-10-09 by the chunk-key check from its
`m22-chunk-key-check-r1` classes; it was not touched and counts against the 3.6 GiB of
memory.

Decision Date: 2026-10-10. The owner decided to restart the preparation on two fresh
guests instead of continuing on the retained pair, which was shut down normally with
its disks and files kept and nothing deleted; a retained guest is restarted only on
the owner's separate authorization, for example to recheck a failure on the new pair.
The authority recorded above applies to the retained pair and does not carry over. For
the two fresh guests, one per chain, the owner authorized: the species deployment at
the approved source pins with its installed validation, the installation of the frozen
tool bundle and the soak fixture, the registration of the 903 PVs through the real
path with the read of their connected state, and the ETL focused execution on each
guest through its own detached unit. Instrumentation, measured preparation,
`prepare`, the runtime checks, `launch-retest.py` and any observation need their own
recorded authority. A failed check stops the sequence for the owner.

Decision Date: 2026-10-11. After both focused executions passed, the owner authorized
the next preparation sequence on the two fresh guests, chain by chain with the shortened
chain first and in this order: `initialize-fresh.py instruments` (which restarts the
appliance with its instrumentation), `check`, `measure` for the 86400-second window, and
`prepare` for that window. A failed step stops the sequence for the owner. The runtime
checks, `launch-retest.py` and any observation still need their own recorded authority.

Decision Date: 2026-10-11. The measured preparation on the shortened guest was refused by
a defect of the journal configuration check (results below and M25 T6). The owner chose to
correct the check rather than restart journald on the running guest: the corrected
`journal_retention.py` enters a newly frozen bundle listed as an approved replacement in
the recheck consumer, its delivery to both fresh guests runs through the accepted
replacement step, and the measured preparation then reruns into a new run-numbered
directory, `/var/lib/etl-soak-fresh-measurements-r2`, whose `retention/proof.json` and
`capacity/input.json` feed `prepare`, and the sequence continues as authorized above (the
README names the first-run directory, which this guest's partial run makes unusable). The partial measurement
directory and the failed transient unit of the refused run stay in place until the owner
decides their disposition.

Decision Date: 2026-10-11. With the preparation complete on both fresh guests, the owner
authorized the pre-launch checks and the launch, chain by chain with the shortened chain
first and stopping on any failure: `verify-health.py`, `verify-chain.py` and
`verify-runtime.py empty` and `abort` for the 86400-second window (the abort probe stops
the appliance and restarts it after a successful verification, followed by a repeated
readiness proof), a private step that renews the current capacity window from two
`contract.py` snapshots about 300 seconds apart and rewrites `capacity-input.json` and
`capacity.json` while keeping the previous files, and `launch-retest.py` opening one
86400-second observation per chain within the README's freshness limits. The observations
then run to their automatic finish; no reinstall, re-registration or appliance restart
during an active observation.

Decision Date: 2026-10-11. The second launch attempt on the shortened guest stopped at the
first health verification: the full sample's journal retention budget check refused the
retention proof as belonging to another bundle, because `journal_retention.validate`
binds a proof to the exact installed bundle and the measured preparation and `prepare`
had run under the bundle before the continuity correction. This is the README rule that
changed tools need new runtime proofs. The owner chose to repeat the measured preparation
under the final bundle rather than loosen the binding: on both fresh guests the superseded
preparation records (`preparation.json`, `state.json`, `capacity.json`,
`capacity-input.json`, `journal-retention-proof.json`, `capacity-sources/`) and the
verification files of the refused launch attempts move into a dated `superseded-<UTC>`
directory under `/var/lib/etl-soak` with nothing deleted, `measure` reruns into a new
run-numbered directory on both guests concurrently, `prepare` follows on each, and the
pre-launch checks and launch run again chain by chain as authorized above. The
instrumentation records stay in place.

Decision Date: 2026-10-11. The third attempt on the shortened guest passed every check up
to the abort probe and then failed the repeated health verification: the retention proof
validation rates the journald writes since the proof's last snapshot, and the appliance
restart of the abort probe put a startup burst into that short window (84.0 kB/s on the
first sample at 98 percent of the cap, 94.2 kB/s on the second, against a measured 43.0
kB/s). The first passing sample also fixed 84.0 kB/s as the in-window bound in
`state.json`. The owner chose to redo the shortened preparation once more so that no such
bound is recorded: the preparation records move aside again, `measure` and `prepare` rerun,
and the procedure waits 1800 s after the abort probe's restart before the repeated health
verification, the capacity renewal and the launch, all inside the one-hour validity of
the runtime proofs. The default guest keeps its preparation and runs the same procedure
with the same wait.

Decision Date: 2026-10-12. Both first full-window observations ended by the sampler's own
abort request at the fixed JFR snapshot archive bound (results row "T16 first full-window
attempt, both guests, self-aborted"), the seventh 24-hour attempt since 2026-09-29
(pairs counted once) to end on an instrument gate and none on a scheduler defect. The owner ruled
that an instrument failure must neither end an observation nor decide the scheduler
verification, and after a debate with one independent reviewer (two rounds; the review
record is private to the session) accepted the following tool change, frozen as bundle
`eb93dfe4f16a4c92952bd1c418f766ef078194b528a37e99a15e7f577bae3eeb`. (1) The abort policy
is an allowlist, `contract.ABORT_CHECKS`, recorded in the manifest's `abort_policy.checks`:
only a check that invalidates the scheduler evidence (the appliance and its management
interface, the fixture population, JVM identity, the sampler itself, the clock, the tool
bundle, the pass journal, the fixture and the appliance health command) counts toward the
two consecutive failures that request an abort, counted per sample; every other check is
recorded and the observation continues; the 2 GiB reserve abort is unchanged. (2) The
evaluator adds `scheduler_verdict`, `scheduler_failed_assertions` and
`scheduler_missing_coverage`, read from the observation contract (duration, UTC midnight,
boot, chain, schedule, bundle, abort), the pass records and their fields, timing and
ordering, the appliance stop, the sampler's own coverage and the allowlisted checks, with a
failed final collection entering by its recorded errors; the overall verdict keeps its
meaning and each observation records both, the overall one first. (3) The fixed 512 MiB
snapshot archive bound is removed; the 2 GiB free-space check before each dump, the
capacity projection's measured `jfr` rate and its 512 MiB capture reserve remain. (4) A
pass that ends inside a metrics request window is accepted under either counter reading
and the snapshot is counted in `metric_window_ambiguities`. (5) The kernel-journal
checkpoint tail query is repeated up to ten times, 0.5 s apart, each after a flush, and
`journal-coverage.json` records `checkpoint_attempts`; this is an `M25` instrument change
and claims no `M25` result. Rejected during the debate: replacing the capture reserve by a
JFR rate, because the reserve covers the terminal captures that no rate contains. The
relaunch sequence, both chains in parallel: delivery through the accepted replacement
step, start of the appliance and health timer that the abort stopped, the aborted records
moved into `superseded-<UTC>/` with nothing deleted, `check`, `measure`, `prepare` (the
delivery invalidates the retention proof), then the existing run-to-launch procedure;
`instruments` does not rerun, so each guest's `measurement-config.json` keeps the
superseded `jfr_snapshot_archive_limit_mib` field, which no shipped check reads.

Decision Date: 2026-10-12, later the same day. The first relaunch under bundle `eb93dfe4…`
stopped before either observation opened: on the shortened guest `measure` was refused at
its capacity projection because the store shrank by 120 MB inside a fifteen-minute window
that contained the hourly MTS-to-LTS pass (reduction and source deletion), which the
projection treated as a reset or rotation; the default guest passed the same step and its
launch procedure was stopped by the owner's choice before launch, so that both chains run
one bundle. The owner then reviewed the abort list item by item against one criterion, that a
stop is justified only when continuing could not produce scheduler evidence or the load
premise is gone, and ruled: the abort list is `appliance`, `journal`, `collection`,
`jvm_restart` and `instances` for the ETL and engine JVMs only, and `pv_status`; the
management interface, the clock, the tools, the fixture, the appliance health command and
the other JVMs are recorded only. The verdict-deciding sample checks of the evaluator stay
as accepted (`contract.SCHEDULER_CHECKS`, a superset of the abort list). The capacity
projection counts a decrease of the store category as zero growth and keeps refusing a
decrease of the journal, log, JFR or measurement categories. The bundle is refrozen as
`abd6c7b76be6125acaa8c5fc1fb7c5c8dc67d13fc196b412d5e904eebd284dd0`; the interrupted
preparation records move aside and both chains are prepared and launched again under it.

Decision Date: 2026-10-13. The second relaunch under `abd6c7b7…` passed `measure`, `prepare`,
the health, chain and empty-data checks on the shortened guest and stopped in the abort
probe at the journal retention budget (a 81 kB/s burst against a 70 kB/s measured bound);
the default guest was stopped before its abort probe so that both chains keep one bundle.
The owner ruled that no check run before the start may refuse it except free space below the
2 GiB reserve, because the journal budget, the capacity projection, the health verification,
the runtime proofs, the continuity tool comparison and the other readiness conditions are
the tools' own calculations and not conditions of the scheduler test. An existing
observation is still never replaced. `observe.py start`, `launch-retest.py` and
`initialize-fresh.py prepare` now run every check and record a failure in
`start_findings`, `launch-started.json` `findings` or `preparation.json` `findings`;
`initialize-fresh.py measure` records a late interval, a changed bundle, a failed
projection and a failed budget, and still stops when a snapshot, a GC or latency capture,
the deployment check or a capacity size cannot be taken; `journal_retention.validate` and `prepare` gained a non-refusing mode
that returns the failed budget; the evaluator requires only that the initial sample ran
(its errors are judged from the sample), reads the health contract from the manifest when the
verification is absent and counts a failed start budget as a budget finding. The abort probe,
the empty-data check and the capacity renewal become optional evidence. Bundle
`2ba4eaf4b95cd3a45dce7a1fb4cc769412141a70c2c5687c1b1e8065b4999429` was delivered to both
prepared guests and both observations opened from it (results rows of 2026-10-13).

Decision Date: 2026-10-13, after the start. The review of the record-only start found that
neither window is bound to the focused-proven deployment (the launch ran before the new
invocation's startup passes) and that `measure` still stopped on its snapshot and capture
steps. The owner ruled both: (1) the shipped `focused.continuity` readback runs once during
each window, under its chain lock and after a five-minute pass, with its proof saved under
the focused chain root as `in-window-readiness-continuity.json`; the shipped command refuses
during an observation so that the observation directory never changes, and the runner keeps
that directory unchanged (its listing is compared before and after); (2) the next bundle
makes every `measure` step record-only (refusing only free space below 2 GiB, an existing
observation and an existing measurement directory) and, from the review, lets the evaluator
treat an absent readiness metrics baseline as missing metric coverage instead of an
unreadable evaluation. That bundle is frozen as
`96bb8f987aa4c3b70082523383676ca6180dc2b04ef9526f25ce82e5ffa1af2d` and is not delivered to
the running guests; their windows are evaluated with the `2ba4eaf4…` evaluator.

The prerequisite is chronological append input. An empty historical source filename
does not establish an empty destination: the failed continuations had newer MTS data
before seed. Preserve the accepted old-eight-sample boundary fixture, middle/recent
markers, four policies, both chains and physical/HTTP acceptance criteria. Do not
replace them with natural aging of a new cohort or change production holds.

Proposed environments: one shortened and one default Rocky 8.10 deployment through
`archiver_dev_uds`, each with 2 vCPU, 4096 MiB RAM, a 48-GiB disk, MariaDB over its
Unix socket and four 256-MiB appliance JVM heaps. Request resources only after
implementation authorization; retain them through focused verification and any
separately gated 24-hour observation, approximately two days, and preserve their
evidence until the owner decides their disposition. Verify actual capacity and
resource availability before acquisition. Record the latest owner-selected aa-env
and Maven branches and full remote commits before freezing deployment inputs; the
2026-10-07 pins remain the evidence baseline, not proof of the latest remote state.
A change to effective stores, reduction or the input contract requires plan review.

###### Ordered Preparation And Verification

1. **Implement and verify explicit preparation stages.** Planned paths are
   `tests/archiver-soak/etl-pass/{install-fixture.py,focused.py,PBFixture.java,test_focused.py}`
   and `tests/archiver-soak/{README.md,SHA256SUMS}` plus
   `tests/archiver-soak/etl-pass/{common.yml,contract.py,initialize-fresh.py,test_contract.py,bundle.json}`.
   Before deployment, record the two owner-approved full commits and apply that
   same pair to `common.yml` deployment variables, `focused.py` ENV_HEAD/MAVEN_HEAD
   and `initialize-fresh.py` SOURCE_PINS. Keep exact installed-source comparisons;
   do not update only the recorded inventory or bypass either source guard.
   Verify both inspectors reject either installed commit differing from the
   approved pair and reject disagreement between deployment variables and either
   inspector's expected pair. Regenerate the complete bundle and SHA256SUMS for
   these synchronized sources. Deployment, focused proof and initializer proof
   must all name that pair and the same frozen tools before observation can start.
   Separate fixture installation,
   registration/live readiness, normal shutdown preservation, offline store
   preparation, seed and verified normal startup. Preserve the current collision
   and same-invocation resume guards. A preparation stage cannot implicitly restart
   the appliance or start IOC input. Verify shipped checker paths on actual target
   Python 3.9 before freezing the complete bundle; host Python results alone do not
   establish compatibility. Real PB writer/decoder checks use deployed Maven classes.
2. **Register through the real path in each additional environment.** Install the
   reviewed artifacts, original three IOC databases, 903-name registration fixture
   and accepted ten-record deadband override. Start the IOC and appliance normally;
   call the normal `archivePV` endpoint and verify all 903 names connected and
   archiving. Record installed WAR/class/JAR hashes, effective typeinfo, chunk keys,
   store URLs, policies, flags, unit settings and real process identities. Select
   one registered scalar-double PV for each unreduced/VeryFast/Fast/Medium policy.
   Do not fabricate metadata, insert database rows or use experimental typeinfo
   creation as a substitute for normal registration.
3. **Preserve preparation input and normal shutdown separately.** Capture the
   required real pre-stop PB intervals, then stop the appliance normally and verify
   every JVM is absent. Check the existing exact known-sample shutdown-preservation
   contract across STS/MTS, including pre-existing occurrences, before stopping the
   IOC. Preserve this result as preparation evidence. No historical seed exists
   yet, so this shutdown cannot count as automatic seed transfer.
4. **Prepare empty active storage offline in the additional environment only.**
   With appliance and IOC inactive, preserve all preparation STS/MTS/LTS trees in
   a separate private archive outside every active storage root. Record original
   and preserved paths, relative file lists, sizes and SHA256 hashes; verify the
   preserved bytes first. In the new unique evidence directory, reserve an absent
   `preparation-stores` directory outside all active roots, on the same filesystem
   as the store trees. Reject overlap, existing destinations or cross-filesystem
   placement. Move each complete active tree to its recorded
   `preparation-stores/{sts,mts,lts}` destination by rename; record each completed
   move and verify its file list and hashes against the archived original.
   After all moves verify, create empty directories at the original active paths
   and restore their recorded ownership, permissions and required security labels.
   This plan authorizes no deletion of originals or archives. On a partial move,
   mismatched bytes, collision or failed directory creation, preserve every tree
   at its recorded location, leave both services stopped and record Incomplete;
   do not retry automatically, overwrite a destination or restore by deletion.
   Keep database contents, registration, typeinfo, store URLs, policies and holds
   unchanged. Verify resolved absolute roots, non-overlap, ownership, permissions
   and absence of active writers. Enumerate actual PB paths for every selected PV
   in all three configured tiers, with the shipped path rules, extensions and
   compression modes: every selected tier must have zero PB files before seed.
   A bounded snapshot's `events=[]` is insufficient; reject any surviving path,
   changed metadata/configuration or unresolved root instead of deleting it.
5. **Seed and bind the physical baseline while offline.** Use the real shipped
   PlainPB writer and the existing independent ten-sample specification per selected
   PV: eight old boundary/nanosecond samples, the middle marker and recent marker,
   all initially in STS. Preserve staging files and exact raw/timestamp/value/alarm
   multiplicities. Verify MTS/LTS remain physically empty after seed and all source
   partitions contain the exact expected records once. Bind preparation archive
   hashes, empty-path proof, unchanged metadata/configuration, source/helper/tool
   hashes, manifest and baseline to a new unique evidence directory. A collision
   or partial stage prevents continuation; do not reuse a seeded directory.
6. **Start live input and the normal appliance without moving seed during stop.**
   Start the original IOC with its accepted override while the appliance remains
   stopped. Read actual CA timestamps for every selected PV and require each to
   be strictly later, including nanoseconds, than that PV's last seeded timestamp.
   Wall-clock waiting alone is not proof; retain the real CA timestamp/value/alarm
   readback. On timeout or backward timestamps retain Incomplete and do not start
   the appliance. Recheck seed/configuration proofs, then start the normal service.
   Bind its boot, InvocationID and four JVM PID/start identities to the offline
   proofs; verify normal component readiness and all 903 names connected/archiving
   again. No stop, restart, consolidation request, manual tick/job or store mutation
   is allowed between seed and completion of focused checks.
7. **Verify actual automatic movement and repetitions.** Run the existing real
   service/ticker path on shortened 5MIN-to-HOUR-to-DAY and default
   HOUR-to-DAY-to-YEAR, retaining hold=2/gather=1 and effective reductions. Require
   completed ordered automatic pass records and exact physical seed transfer,
   corresponding source deletion, recent-source retention, independently expected
   reduced timestamp/value/status/severity/multiplicities and matching HTTP output.
   Capture the actual recent closed-bin source before reduction; continued IOC
   input can legitimately replace the original marker. Require a later completed
   regular grid pass for each hop with 903 jobs and no failures, skips, space
   deletion or overrun, and fixed-interval PB/HTTP comparisons showing no extras.
   Use actual processingTime to select the recent bin's expected tier. Final
   artifact/configuration/tool and boot/invocation/JVM identities must match this
   run's baseline. Counters alone, checker replays and preparation shutdown cannot
   establish automatic physical transfer.
8. **Keep the existing observation gates.** Only after focused checks pass may
   the prior amendment's JFR, measured preparation, negative/abort, final-restart
   continuity, fresh capacity/readiness and 86400-second observation sequence
   proceed under separately established execution authority. Do not start an
   observation from an Incomplete focused result. Neither normal movement nor
   preparation shutdown proves injected commit/deletion/space/restart fault safety.

###### Test Plan And Evidence Binding

| Check | Planned Real Path And Required Outcome | Execution State |
| --- | --- | --- |
| T13 preparation guards and target compatibility | Shipped staged tools on target Python 3.9; actual PB path enumeration and writer/decoder. Require common.yml, focused source guards and initializer SOURCE_PINS to contain the same approved full commits; reject either installed commit mismatch or inspector/deployment disagreement. Reject a newer existing destination even when bounded event windows are empty; incomplete archives, root overlap, changed metadata, partial stages, seed collisions and live timestamps not strictly newer must prevent startup. Preserve real failed-run inputs for checker regressions; no internal ETL substitutes. | Pending |
| T14 separate environment and preparation provenance | Full species deployment and real IOC/archivePV registration; exactly 903 connected/archiving before normal shutdown and after startup. Verify original preparation file hashes, exact shutdown sample preservation, empty active selected-tier paths, unchanged DB/typeinfo/store URLs and installed artifacts. Existing guests remain untouched. | Pending |
| T3 automatic transfer and repeated passes | Real PlainPB seed, normal startup/ticker, physical source/destination records, independent four-policy expectations and live HTTP; exact original boundary fixture passes both chains and later scheduled repeats without duplicates or loss. Bind all records to the new invocation and complete bundle. | Pending |
| T15 launch continuity | Existing post-final-restart continuity and freshness/capacity gates using the new accepted focused proof; no old or partial proof can qualify. | Pending |
| T16-T21 observations and comparison | Existing two full 86400-second observations and final comparison; focused preparation is not soak acceptance. | Pending |

The stored preparation PB archive and shutdown proof remain immutable. Empty-path
and seed proofs describe the active roots after preparation; they must not be
presented as continuity of the archived preparation stores. Existing `run()` live
pre-seed and shutdown assumptions must be replaced by these explicit stages, not
silently bypassed. The tool README will describe the system procedure after
implementation is authorized; this revision changes only the canonical plan.
The complete execution outcomes above remain Pending; partial prerequisite results
are recorded below. Maven review2 accepted this revision;
owner acceptance and implementation authorization are recorded separately above.

###### Preparation Prerequisite Verification Results

| Check | Observed At | Actual Method And Result | Evidence And Limits |
| --- | --- | --- | --- |
| T14 environment acquisition | 2026-10-09 | Cloud created two additional Rocky 8.10 guests, each 2 vCPU, 4096 MiB and 48 GiB. Requester SSH confirmed OS, sudo and approximately 48.26 GB available root storage on both. Existing guests and evidence remain unchanged. | Private Cloud handoff and requester inventory in `work/m22-cold-preparation-20261008/`. Appliance installation and registration Pending. |
| T13 target compatibility | 2026-10-09, before 07:21 UTC | Shipped Python operator completed on both guests, exit 0. Each actual Python 3.9.25 execution passed all 24 focused checker tests and the source-pin agreement test, skip 0. Real retained shutdown, physical/HTTP and resume inputs were replayed. | `python-install-r1.log`, `python39-c-r1.log`, `python39-d-r1.log`. Checker execution is not new ETL, CA or HTTP acceptance. |
| T13 deployment-variable interpretation | 2026-10-09 | Actual control-host Ansible DataLoader selected the differing last value for six duplicate pin cases and interpreted a no-separator document as a string. Corrected shipped guard rejected all cases; both source-pin tests passed on host Python 3.13.5. | `contractdf89d6c7` and `test_contractaac5c3a3`. Real installed-commit mismatch checks and full cold continuity remain Pending. |
| T13 synchronized freeze | 2026-10-09, before 07:21 UTC | Remote branches reconfirmed aa-env `release-2.0.1` at `482cf2939ea997064e4a2df64e3cb420681f4566` and Maven `modernize` at `162269e7db97f527626ba0b387933a8c47e8bb57`. Complete 24-file bundle verification and all SHA256SUMS entries passed. Both store-specific species syntax checks passed. | Bundle SHA256 `4197b891071f5e605f6e77da5fc125fc637ad128e46e796e486cc71d1afe4c75`. Source review and real deployed classes remain required before focused execution. |
| T14 installed cold deployments and fixture | 2026-10-09 | Both new store-chain installations completed with 33 tasks successful, zero failures/unreachable hosts; actual installed revisions matched the latest approved pins and 3234 WAR/class/JAR files matched per deployment. Normal registration reached exactly 903 archived and connected fixture PVs per deployment. Actual installed PB writer/operator and CA checks completed before focused startup. | `deploy-shortened-r1.log`, `deploy-default-r1.log` and installed-validation records under the private cold evidence directory. This supersedes the acquisition row's installation/registration Pending note. |
| T3 retained cold execution and bounded recheck | 2026-10-09, rechecked after 23:30 UTC | Both automatic executions reached startup/repeat physical and HTTP comparisons and both regular transitions. Final comparison stopped because all 903 initially absent chunk keys became generated keys. The owner selected a bounded checker correction and retained-record recheck. Installed converter classes with unchanged deployed properties independently generated all 903 exact expected keys per chain. Two regression tests passed on each actual Python 3.9 interpreter, with no skips. Both record rechecks returned Passed: startup/repeat historical samples, recent-bin source and independent reduction, matching HTTP, source deletion/retention, regular passes, preparation binding, current configuration and original running identity were checked. | `final-evidence-{c,d}-r1.tar.gz`, `chunk-key-{c,d}-r2.log`, `recheck-{c,d}-r1.log`, `recheck-evidence-{c,d}-r1.tar.gz` in `work/m22-cold-preparation-20261008/`. Independent local archive comparison verified 1870 shortened and 967 default original file hashes with zero differences, including unchanged original Incomplete results. Separate recheck proofs do not satisfy the complete focused-proof consumer gate; continuity, instrumentation, measured preparation and 24-hour observations remain Pending. No restart, reseed or soak occurred during recheck. |
| T13 chunk-key correction source and independent review | 2026-10-09 | Completion allows only null-to-exact-independently-generated key for each PV, retains nonnull key equality and all other exact comparisons, and checks selected PB paths. Recheck writes separate hash-bound evidence and preserves original records. All 54 SHA256SUMS entries and diff whitespace checks passed. Independent review 2 accepted source and both completed record rechecks with no must-fix/minor findings. The reviewer directly checked all 1870/967 original source hashes, each 903-key expectation, all six new evidence hashes per chain, unchanged final/current settings and identity, and both regular transition records. | `focused.py` SHA256 `4265dfac7f62cb99e0a03a5db981a3449a37dc51365f05c156a5a20d3e264fd3`; bundle SHA256 `190c9d8fcc87e33c3e0d0f832092a2665d31731765a32fa9e36d525ac9e56809`. Reviewer read both two-test OK logs and inspected archives; no test rerun or VM action. Acceptance is limited to the correction and retained-record recheck. Continuity and soak remain Pending. |
| T14 fresh deployments, fixture and registration | 2026-10-10, 18:18 to 18:32 UTC | Both fresh Rocky 8.10 guests (2 vCPU, 4096 MiB, 48 GiB) received the `archiver_dev_uds` species with 33 successful tasks and zero failures each; the installed aa-env and Maven revisions matched the approved pins. Each guest's detached sequence unit then installed the tool archive (39 files from the current tree) and the soak fixture, passed the installed validation, and registered exactly 903 archived and connected PVs through the real path. | Syntax, host and deployment logs in the private `work/m22-clean-20261010/`; installation, validation and registration results in `/var/lib/m22-clean-sequence-r1/result.json` on each guest. The retained pair stayed shut down; nothing was deleted. |
| T3 fresh focused executions | 2026-10-10 18:33 UTC to 2026-10-11 00:11 UTC | Shortened chain: `focused.py run` started 18:38:07 UTC and returned Passed at 19:10:36 UTC at stage focused-complete. Its nine automatic pass records of the new invocation show startup moving 8 STS and 4 MTS partitions of the four seeded PVs, the 18:55 pass moving the 4 recent-marker partitions, the three 5-minute passes from 19:00 moving 903 partitions each, and the two selected regular passes (18:45 transition 0, 19:10 transition 1) running 903 jobs with zero failed, aborted, skipped or late. Default chain: started 18:33:13 UTC and returned Passed at 00:10:31 UTC on 2026-10-11 at stage focused-complete. Both detached units ended Succeeded with the appliance and IOC active and no failed unit. | `/var/lib/etl-focused/<chain>/result.json` and `passes-<invocation>.jsonl` on each guest; preparation binding SHA256 `af37365146664a7525b114947e9aad950cd1f2eb5de1ebe0fcfbbee302da0842` (shortened) and `902c45f99a90a5d79cb41490d88700252feebd0fd4f6274d59051dbe688b9d67` (default). The selected regular-pass records show zero partitions moved by selection; they prove timing and the job contract, while transfer is proven by the physical comparison and the full pass list. The default full pass list was not read separately. Focused automatic transfer only; no soak or launch continuity. |
| T3 independent physical movement and continuity check | 2026-10-10 20:23 UTC to 2026-10-11 04:16 UTC | Independently of the checker, the real PB files on both guests were decoded over SSH, read-only and at low priority. (1) The seeded source files of each selected PV are absent from STS and the old MTS partition is absent; the eight old samples sit in LTS exactly as the lastSample_10/30/60 reduction computed from the writer-staging seed bytes (4 events) or unreduced (8 events for the unreduced policy), and the middle and recent markers sit once each at the head of their MTS partition, byte for byte; no timestamp is stored twice across STS, MTS and LTS. (2) All 903 PVs: the 880 counter PVs step by exactly one across STS and MTS (LTS excluded where reduced), and every PV is time-ordered and current. (3) `getPVDetails` for all 903 PVs on both guests: the lost-event counters for connection loss, wrong timestamp and type change are zero. | Check scripts are private to the session and not in the repository; recheck by decoding `/arch/{sts,mts,lts}` PB files against `/var/lib/etl-focused/<chain>/writer-staging/` and the fixture calc expressions, and by reading `getPVDetails` for every PV. A duplicate timestamp seen once on one waveform PV (300 events) was a read during a running ETL pass and was absent on reread; read physical files between passes. Physical files keep changing while the appliance runs, so the checker's in-run records remain the acceptance evidence and these reads confirm them at their observation time. |
| T3 engine sample-buffer loss on 0.1-second PVs, outside ETL scope | 2026-10-11, 01:45 to 04:16 UTC | The counter check found samples missing only on 0.1-second MONITOR PVs, one per PV, several PVs at one instant: default 10 PVs at 00:27:41 UTC on 2026-10-11; shortened 5 before 01:45 UTC and 11 more at 02:54:53 UTC during a one-hour read-only observation (01:57 to 02:57 UTC). The engine counter for events lost because the sample buffer is full matched the decoded gaps one to one (default 10 of about 64.3 million events, shortened 16 of about 63.7 million); no 1-second or 10-second PV lost a sample. These instants are the IOC timestamps of the missing samples; by the code the overflow itself happened about 10.1 s later, when the next write pass was late. In the shortened overflow window (02:55:03 to 02:55:04 UTC) the 1-second observation shows a CPU burst of 58 jiffies at 02:55:02 (hourly median 6) with the ETL 5-minute pass planned at 02:55:00, zero iowait and steal, and one 54 ms young GC of the engine JVM in the 02:55:03 to 02:55:04 sample; the default overflow window had no observer running, no journal entry and no ETL pass scheduled near it. At the pinned Maven commit, `ArchiveEngine.addChannel` sizes the buffer as round(secondsToBuffer / period x sampleBufferCapacityAdjustment) + 1 (deployed 10 and 1.0: 101 slots at 0.1 s, 11 at 1 s), `SampleBuffer.add` drops the oldest sample when full, the writer swaps lists under the lock and appends outside it, and one scheduler thread runs the write pass at a fixed 10-second rate (measured 0.04 to 0.05 s per pass); the only overflow condition is a swap interval above capacity x period, so a write-pass delay above 0.1 s loses one sample on the fast PVs whose buffers are full. The trigger of that delay is not identified. | One-hour observation files (jstat and `/proc/stat` at 1 s on both guests, start and end counters) are private to the session. Not an ETL defect and outside M22 acceptance; reported to the Maven repository session on 2026-10-11 with the code references and filed the same day as epicsarchiverap-maven issue #29 (bug); no fix is decided and the pinned commit is untouched, and any fix must not move it. Later on 2026-10-11 the Maven session committed a fix on its branch `issue-29-sample-buffer-margin` (`6c6b973a`), unmerged: the margin becomes a time quantity through `sampleBufferMarginSeconds` (default 1.0, a 0.1 s PV then holds 110 samples), and its reproduction with a delay injected at the storage writer lost one sample on part of the fast PVs at 130 ms and on all of them at 200 ms, matching the guest pattern; adoption and the multi-hour zero-loss run on the real population stay with this record's plan review after the verification. Whether lost-sample counts enter the observation criteria is a separate decision. Deployed settings were not changed. |
| T14 fresh initialization sequence, shortened guest | 2026-10-11, 05:27 to 05:31 UTC | `initialize-fresh.py instruments` ran as root in a transient unit and succeeded in 17.6 s at 05:27:44 UTC: the appliance restarted with four JVMs, each with a GC log file and a JFR check recorded, schema 5, observation not started. After the 903 PVs reconnected (within 10 s), `check` succeeded in 1.1 s at 05:28:28 UTC. `measure` for the 86400-second window was refused at 05:28:53 UTC before its first snapshot: "Journal configuration application to the running daemon is unverified". Cause verified on the guest: the check derived the journald start from the whole-second `btime` (…805.910) while the drop-in's mtime was …806.347, and systemd's microsecond start was …806.375, 28 ms after the write; the role writes the drop-in and restarts journald within one second. A defect of the check, not of the deployment; the sequence stopped and the default guest was not touched. | Transient units `m22-fresh-instruments-shortened` and `m22-fresh-check-shortened` (collected) and `m22-fresh-measure-shortened` (left failed); `fresh-initialization.json`, `fresh-check-20261011T052827…/`, `jvm/` and `measurement-config.json` under `/var/lib/etl-soak`; a partial `/var/lib/etl-soak-fresh-measurements` (pv-status.json, four JFR checks, empty `capacity/` and `retention/`) that a rerun must not reuse. The correction is recorded under M25 T6 and the consumer amendment; the engine JVMs restarted, so their in-memory loss counters start again from zero. |
| T14 bundle replacement on both fresh guests | 2026-10-11, 07:29 to 07:31 UTC | The accepted replacement step delivered the refrozen bundle (SHA256 `43970448a8c23f48cb43c40966e98732a652409a5fdfe3d4dfcc5e65cbfe8c17`) from a private staging directory on each guest, running as root: the installed directory was copied, only `bundle.json`, `focused.py` and `journal_retention.py` changed (41 files on the shortened guest, 40 on the default guest), the preserved sibling `etl-soak.prev-<UTC>` equals the pre-delivery hash listing, the installed bundle verifies 24 members, directory ownership and security context are unchanged, and the appliance and IOC stayed active with the sampler and finish timers inactive. | Delivery records and before/after hash listings in each guest's private staging directory; nothing deleted. The shortened initialization record keeps the pre-replacement tool hashes while its preparation and later observation records carry the replaced ones; no shipped check compares the two (read in `initialize-fresh.py` and `observe.py`), so the difference is an evidence note, not a gate. The default guest was initialized after the delivery, so its records agree. |
| T14 measured preparation and prepare, shortened guest | 2026-10-11, 07:29 to 08:01 UTC | After the delivery, `check` passed in 1.2 s; `measure` into the run-numbered directory ran seven retention snapshots and three capacity points and ended Succeeded at 07:59:56 UTC; `prepare` for the 86400-second window succeeded at 08:00:41 UTC in 0.8 s. The journal retention budget passed (system 507,429,921 and user 276,828,160 bytes under the 1 GiB effective cap), the capacity projection is 12,553,757,630 bytes against 40,211,886,080 available, and the preparation record is schema 5 with the 24 replaced tool hashes. | `/var/lib/etl-soak-fresh-measurements-r2/{retention,capacity}` and `/var/lib/etl-soak/{preparation.json,capacity.json,capacity-input.json,journal-retention-proof.json,state.json}` on the guest; transient units `m22-fresh-check2-shortened`, `m22-fresh-measure2-shortened` and `m22-fresh-prepare-shortened` (collected). The runtime checks, launch and observation remain pending under their own authority. |
| T14 initialization, measured preparation and prepare, default guest | 2026-10-11, 08:01 to 08:33 UTC | With the refrozen bundle already delivered, `instruments` succeeded in 19.4 s at 08:01:24 UTC (appliance restarted; four JVMs, each with a GC log file and a JFR check recorded; schema 5; observation not started), the 903 PVs reconnected within about 50 s, `check` succeeded in 0.9 s at 08:02:14 UTC, `measure` into the first-run directory ran seven retention snapshots and three capacity points and ended Succeeded at 08:32:19 UTC, and `prepare` for the 86400-second window succeeded at 08:33:22 UTC in 0.7 s. The journal retention budget passed (system 526,855,726 and user 276,910,586 bytes under the 1 GiB effective cap), the capacity projection is 10,195,449,564 bytes against 39,179,419,648 available, and the initialization and preparation records carry the same replaced tool hashes. | `/var/lib/etl-soak-fresh-measurements/{retention,capacity}` and the preparation records under `/var/lib/etl-soak` on the guest; transient units `m22-fresh-instruments-default`, `m22-fresh-check-default`, `m22-fresh-measure-default` and `m22-fresh-prepare-default`, all ended Succeeded and collected. The authorized preparation sequence is complete on both fresh guests; the runtime checks, launch and observation remain pending under their own authority. |
| T15 first launch attempt, shortened guest | 2026-10-11, 08:46 to 08:58 UTC | Through the private run-to-launch procedure as root: `verify-health.py` passed twice (two distinct health invocations, full samples with 903 archiving PVs and no errors; closed passes 10 then 0), `verify-chain.py` passed, a closed ETL pass was already recorded (9,760 bytes), `verify-runtime.py empty` passed, `verify-runtime.py abort` passed (early and repeated finish rejected, verdict Incomplete, whole-unit stop rc 0 in 11.5 s, no errors, four complete GC recordings) and restarted the appliance, all 903 PVs were archiving and connected after five polls, `verify-health.py` passed again after 240 s, and the private capacity refresh took two real samples 300 s apart and rewrote the capacity files (required growth 12,706,788,547 bytes against 39,872,937,984 available, previous files preserved). `launch-retest.py` with a target 75 s ahead then failed at `focused.continuity`: "Focused evidence differs from current tools", because the Passed focused result carries the run-time tool hashes of the previous bundle and the continuity compared them strictly with the replaced bundle. No observation opened; the appliance and IOC stayed active with both observation timers inactive. | `health-verification.json`, `chain-verification.json`, `empty-data-verification.json`, `terminal-path-verification.json`, `launch-started.json` and `launch-failed.json` under `/var/lib/etl-soak`, the terminal probe directory beside it, and the local log `launch-shortened.log` in the private `work/m22-clean-20261010/`. The runtime proofs expire one hour after 08:47 UTC, so the checks rerun before the next launch. The continuity rule is corrected in the consumer amendment above. |
| T15 second launch attempt and superseded preparation, both guests | 2026-10-11, 09:20 to 09:25 UTC | The bundle with the corrected continuity (SHA256 `d72cfc575cf1603d5303e448940756608d9c4b7c75fc314f441faceb61f31178`) was delivered to both guests through the accepted replacement step at 09:20:50 UTC: only `bundle.json` and `focused.py` changed, the new preserved sibling equals the pre-delivery listing, 24 members verify, the appliance and IOC stayed active. The repeated procedure on the shortened guest then stopped at its first `verify-health.py`: the full sample's `journal_retention_budget` check refused the retention proof as belonging to another bundle, because the proof installed by `prepare` at 08:00 UTC binds the exact bundle of that time. Per the decision above, the superseded preparation records and the refused launch's verification files moved into `superseded-20261011T092424Z` (shortened) and `superseded-20261011T092450Z` (default) under `/var/lib/etl-soak`, nothing deleted, and `measure` restarted at 09:24 UTC into `/var/lib/etl-soak-fresh-measurements-r3` (shortened) and `-r2` (default) with the instrumentation records untouched. | Delivery records in each guest's private staging directory; the local log `launch-shortened-2.log`; the superseded directories list exactly the moved files. The re-measured preparation, `prepare` and the launch are recorded when they end. |
| T15 third launch attempt, shortened guest | 2026-10-11, 09:24 to 10:01 UTC | `measure` into the run-numbered directory ended Succeeded at 09:54:30 UTC and `prepare` at 09:54:56 UTC with the final bundle's tool hashes. The procedure then passed both health verifications, the chain check, the empty-data check and the abort probe (restart at about 09:56 UTC, 903 PVs reconnected after six polls), and failed the repeated health verification after 240 s: the first full sample passed with the proof-to-sample write rate at 83,958 bytes/s (required 1,052,374,616 of 1,073,741,824 bytes) and the second, 9 s later, failed at 94,249 bytes/s (required 1,114,526,616), both measured from the proof's last snapshot at 09:54:30 UTC across the restart burst (32,677,888 then 37,515,264 bytes written). The default guest's `measure` ended Succeeded at 09:54:56 UTC and its `prepare` at 09:55:56 UTC. | `/var/lib/etl-soak-fresh-measurements-r3` (shortened) and `-r2` (default); the raw sample directories of 10:00:59 and 10:01:08 UTC with their retention snapshots; the local log `launch-shortened-3.log`. The decision above records the chosen remedy. |
| T15 fourth attempt and observation start, shortened guest | 2026-10-11, 16:24 to 17:35 UTC | The preparation records moved into `superseded-20261011T162441Z`; `measure` into `/var/lib/etl-soak-fresh-measurements-r4` ended Succeeded at 16:54:47 UTC (measured bounds 47,683 bytes/s system and 27,949 bytes/s user, the user bound from an 8 MiB allocation step of the user journal; required 1,010,474,516 of 1,073,741,824 bytes, passed) and `prepare` at 16:55:34 UTC. The procedure from 16:56:06 UTC passed both health verifications, the chain check (a closed pass of 23,376 bytes already recorded), the empty-data check and the abort probe (restart at 16:56:52 UTC, 903 PVs after five polls), waited 1800 s, passed the repeated health verification at 17:27:35 and 17:27:44 UTC with no errors, and renewed the capacity window with two real samples (required growth 16,544,106,643 bytes against 37,029,502,976 available). The first launch command was refused by systemd because the transient unit name of the morning's failed attempt still existed; `launch-retest.py` ran at 17:34:00 UTC under a unique unit name: chain and health checks, the capacity check, the continuity of the Passed focused result under the replaced bundle and the readiness sample passed, and the observation opened at 17:35:15 UTC with 312 expected firings and the sample and finish timers active. | `observation.json`, `launch-started.json`, `initial-sample.json` and `readiness-continuity.json` under `/var/lib/etl-soak`; the local log `launch-shortened-4.log`; the earliest finish is 2026-10-12T17:35:15 UTC. The morning's failed transient units stay loaded as failed on the guest; the procedure now names launch units by time. |
| T15 launch and observation start, default guest | 2026-10-11, 17:35 to 18:14 UTC | With the preparation of 09:55 UTC kept (measured and prepared under the final bundle), the procedure passed both health verifications (903 archiving PVs, no errors), the chain check (a closed pass of 8,781 bytes already recorded), the empty-data check and the abort probe (early and repeated finish rejected, verdict Incomplete, whole-unit stop rc 0 in 13.1 s, no errors, four complete GC recordings; 903 PVs archiving and connected after six polls), waited 1800 s, passed the repeated health verification at 18:07:24 and 18:07:33 UTC with no errors, and renewed the capacity window with two real samples 300 s apart (required growth 11,366,051,777 bytes against 35,334,057,984 available, previous files preserved). `launch-retest.py` ran at 18:12:51 UTC under a time-named unit with a target 75 s ahead: chain and health checks, the capacity check, the continuity of the Passed focused result under the replaced bundle and the readiness sample passed, and the observation opened at 18:14:06 UTC with 27 expected firings (24 hourly and 3 eight-hourly) and the sample and finish timers active. | `observation.json`, `launch-started.json`, `initial-sample.json` and `readiness-continuity.json` under `/var/lib/etl-soak`; the continuity records of 18:13 UTC under `/var/lib/etl-focused/default`; the local log `launch-default.log`; the earliest finish is 2026-10-12T18:14:06 UTC. Both 86400-second observations are open and finish through their finish timers. |
| T16 first full-window attempt, both guests, self-aborted | 2026-10-12, 12:35 and 15:45 UTC | Both observations ended by the sampler's own abort request after two consecutive full samples failed the `gc` check with "JFR snapshot archive limit reached": shortened at 12:35:04 UTC after 68,389 s, default at 15:45:04 UTC after 77,458 s. Each `abort.json` records verdict Incomplete, the appliance stopped with rc 0 in 11.4 s and 13.1 s, boot unchanged, and four complete GC recordings (134 and 150 MiB). The cause is the fixed bound of 440 MiB (512 MiB less a 72 MiB reserve) that `measure.dump_jfr` applied to every snapshot under `raw/`: ten-minute snapshots average 0.36 MiB per JVM, about 1.45 MiB per sample and about 420 MiB per 288 samples, and the pre-launch measurement and verification snapshots in the same directory (shortened 109.6 MiB, default 69.0 MiB) consumed the margin; the totals stood at 440.2 and 440.1 MiB with the disks at 41 and 50 percent. Every pass planned before the abort fired (shortened 247 of 312, default 23 of 27; missing, duplicate and unexpected 0; incomplete GC pairs 0; budget-failed samples 0). The shortened record also holds one `kernel_journal` sample failure at 01:45:00 UTC (the checkpoint marker reached the journal after its tail query) and three metric assertions (`metric_snapshot_counter`, `metric_last_pass`, `metric_busy_time`) from the 08:35:00 UTC snapshot, whose 49 ms metrics request contained a pass end (counter 188 against 189 closed passes). | `abort.json`, `abort-request.json`, every sample, `passes.jsonl` and `final-gc/` under `/var/lib/etl-soak` on each guest; the evaluation embedded in `abort.json`; the earlier observation archives hold no per-sample JFR, so this was the first full window under the per-sample snapshot bound. The tool change and the relaunch are in the decision of 2026-10-12. |
| T13 abort allowlist, scheduler verdict and snapshot bound removal | 2026-10-12, 21:16 to 22:20 UTC | Shipped changes: `contract.ABORT_CHECKS` and the per-sample counters `consecutive_abort_failures` in `collect.py`; `abort_policy.checks` in the launch manifest; `scheduler_verdict`, `metric_variants` and the final-collection mapping in `evaluate.py`; `terminal_checkpoint` with a bounded retry in `journal_coverage.py`; the archive bound removed from `measure.py` and its field from `initialize-fresh.py`; eight approved replacements in `focused.py`; README. Local checks on the control host: 139 tests passed, 40 skipped (15 new: allowlist, per-sample reset, disk reserve, contract default, snapshot dump without a bound, checkpoint retry and bound, metric window variants, scheduler verdict membership, final-collection mapping, and two replays of the early-return scheduler mapping on retained runtime evidence). The new evaluator on read-only copies of both aborted records (JFR snapshots excluded): overall Incomplete; scheduler verdict Incomplete with exactly `aborted_observation`, `full_sample_coverage`, `required_pass_wait`, `scheduled_pass_coverage` and `observation_duration` (plus `tool_bundle_changed` against the host bundle); `gc` and `final_sample` outside it; the shortened record's three metric assertions cleared with two counted ambiguities; the one `kernel_journal` failure stays in the overall verdict. Bundle frozen as `eb93dfe4…`, 24 members, SHA256SUMS regenerated (55 entries), the replacement step's accepted hash updated, delivery archive verified against `bundle.json`. | Working tree at this record; the private review record under `work/review_sessions/`; the evaluator outputs on the copied records in the session scratch directory. Delivery, re-preparation and relaunch follow under the decision of 2026-10-12. |
| T15 first relaunch, both guests, stopped before launch | 2026-10-12, 22:08 to 22:45 UTC | Bundle `eb93dfe4…` delivered to both guests through the accepted replacement step (24 members verified), the appliance and health timer started, 903 PVs archiving and connected after five polls, the aborted records moved into `superseded-20261012T220800Z` (34 entries each), `check` passed on both. `measure` into the next run-numbered directory ended Succeeded on the default guest at 22:39 UTC and `prepare` followed; on the shortened guest it was refused at 22:39 UTC by the capacity projection ("Capacity growth was interrupted by a reset or rotation") because the store fell from 12,351,207,506 to 12,231,094,059 bytes between 22:08:53 and 22:23:53 UTC across the 22:10 hourly pass and rose again by 22:38:53 UTC; none of the other four categories decreased. The default launch procedure had passed its health and chain checks and was stopped by the owner's choice while waiting for a closed pass; no observation opened. | Measurement directories `-r5` (shortened, refused) and `-r3` (default, passed) on the guests; local logs `relaunch-shortened.log` and `relaunch-default.log`. The remedy is the decision of 2026-10-12, later the same day. |
| T13 abort list narrowed and store shrink accepted | 2026-10-12, 23:05 to 23:40 UTC | Shipped changes: `contract.ABORT_CHECKS` reduced to the six evidence-stopping checks with `ABORT_JVMS` (`engine`, `etl`) qualifying the JVM checks, `contract.SCHEDULER_CHECKS` carrying the verdict-deciding list, the `instances` error naming the missing JVMs, the manifest's `abort_policy.jvms`, the evaluator reading `SCHEDULER_CHECKS` and reporting `scheduler_checks`, and the capacity projection treating a store decrease as zero growth. Local checks: 142 tests passed, 40 skipped (three new or rewritten: the verdict-deciding but not abort-listed checks never request an abort; JVM identity errors count for the ETL and engine JVMs only; a shrinking store projects zero growth while the other categories still reset). The evaluator replays on both aborted copies are unchanged. Bundle refrozen as `abd6c7b7…`, SHA256SUMS regenerated, the replacement step's accepted hash and the delivery archive updated. | Working tree at this record; the relaunch under this bundle is recorded when it ends. |
| T15 second relaunch, both guests, stopped at the abort probe | 2026-10-12, 23:16 to 23:53 UTC | Bundle `abd6c7b7…` delivered (24 members verified), the interrupted preparation records moved into `superseded-20261012T231624Z`, `check`, `measure` (ended Succeeded at 23:46 UTC on both) and `prepare` passed on both guests. On the shortened guest both health verifications, the chain check, a closed pass and the empty-data check passed; the abort probe stopped at 23:52:22 UTC before touching the appliance with "Current journal retention budget failed": the probe sample measured 81,389 bytes/s against the proof's 69,928 bytes/s bound (required 1,070,422,183 of 1,073,741,824 bytes). The default guest was stopped by choice while waiting for a closed pass. No observation opened. | The probe directory `etl-soak-terminal-probe-20261012T235217…` beside `/var/lib/etl-soak` on the shortened guest; local logs `relaunch2-shortened.log` and `relaunch2-default.log`. The remedy is the decision of 2026-10-13. |
| T13 record-only start checks | 2026-10-12 23:55 to 2026-10-13 00:06 UTC | Shipped changes: `observe.start` refuses only an existing observation and free space below 2 GiB and records every other readiness, proof, capacity, continuity, JFR and journal check in `start_findings`, with the live health contract in the manifest; `launch-retest.py` records each refresh failure in `launch-started.json` and no longer stops the launch; `initialize-fresh.py prepare` records proof, projection and deployment-check failures and `measure` records interval, bundle, projection and budget failures (its snapshot and capture steps still stop it); `journal_retention.validate` and `prepare` accept `strict=False`; the evaluator accepts an initial sample that ran with errors, falls back to the manifest's health contract and counts a failed start budget as a budget finding; `launch-retest.py` joins the approved replacements. Local checks: 145 tests passed, 40 skipped (three new: missing proofs recorded and the observation opened, free space below the reserve refusing with nothing written, an existing observation never replaced). Evaluator replays on both aborted copies unchanged. Bundle `2ba4eaf4…` frozen, SHA256SUMS regenerated, accepted hash and delivery archive updated. | Working tree at this record. |
| T16 observation start under the record-only start, both guests | 2026-10-13, 00:07 to 00:10 UTC | On each prepared guest bundle `2ba4eaf4…` was delivered through the accepted replacement step, the appliance restarted so that the 26-hour JFR recordings cover the window (903 PVs archiving and connected after six polls) and `launch-retest.py` ran under a time-named unit. Shortened opened at 00:10:06 UTC (earliest finish 2026-10-14T00:10:06 UTC, 312 expected firings), default at 00:10:08 UTC (earliest finish 2026-10-14T00:10:08 UTC, 27 expected firings); sample and finish timers active; the manifests record the six-check abort policy. Recorded and not refusing: start findings for the readiness sample (its only error was the retention proof bound to the previous bundle), health verification, the absent abort probe (and on default the absent empty-data check), focused continuity (no readback after the restart), the retention proof and budget; launch findings for the retention proof, the health verification command, the stale capacity window, focused continuity ("Current invocation lacks automatic startup pass evidence" right after the restart) and the readiness sample. The first periodic samples show 903 archiving PVs with only the retention-budget error, which is not abort-listed and does not decide the scheduler verdict. Consequences for these windows: both manifests carry no retention proof (`journal_retention` empty, bound to the previous bundle), so the shipped evaluator leaves the in-window retention budget and the journal interval, sequence and kernel proofs unevaluated and the overall verdict is Incomplete by construction; both manifests carry an empty `focused_continuity` and no `readiness-continuity.json` exists, because the launch ran about three minutes after the appliance restart before the new invocation's startup passes, so the window was not bound to the focused-proven deployment at its start (artifacts, PV set, flags, tools and the physical and HTTP readback); the in-window readback of 00:46 UTC binds it (row "T16 focused continuity inside both windows"). | `observation.json`, `launch-started.json`, `initial-sample.json` and the samples under `/var/lib/etl-soak` on each guest; local logs `launch-direct-shortened.log` and `launch-direct-default.log`. |
| T13 record-only measurement and baseline guard (next bundle) | 2026-10-13, 00:30 to 00:40 UTC | Shipped changes for the next start, not delivered to the running guests: `initialize-fresh.py measure` refuses only free space below 2 GiB, an existing observation or terminal record and an existing measurement directory, and records a failed deployment check, journal snapshot, GC or latency capture, capacity size, capacity window, projection or retention budget, a late interval or a changed bundle in `measurements.json` `findings`; the evaluator treats an absent or unreadable readiness metrics baseline as `metric_counter_coverage` missing. The review of this change found that the loop spaced journal snapshots from the start of each pass, so the preamble time of one pass could shorten an interval below the five-minute minimum of the retention proof and the proof would fail; the loop now spaces each snapshot from the previous snapshot's own clock reading. Local checks: 148 tests passed, 40 skipped (three new: a measurement on a host without the appliance records every failed step and writes its record; every spacing is at least five minutes while the preamble time varies, which fails against the earlier loop with spacings of 299.91 to 300.09 seconds; free space below the reserve refuses). The evaluator on a copy of the shortened aborted record with the baseline removed now completes (312 expected passes, `metric_counter_coverage` missing) instead of returning an unreadable evaluation; the replays of both unedited copies are unchanged. Bundle `96bb8f98…` frozen, SHA256SUMS regenerated, accepted hash and delivery archive updated. | Working tree at this record; the evaluator outputs on the copies in the session scratch directory. |
| T16 focused continuity inside both windows | 2026-10-13, 00:41 to 00:47 UTC | A private runner ran the installed `focused.continuity` of bundle `2ba4eaf4…` on each guest under the chain lock, after the 00:45 pass, with the observation guard handled by the runner and the proof saved under the focused chain root. The first run at 00:41 UTC stopped inside the installed `inventory()` at its own observation guard before writing anything; the second at 00:46 UTC passed on both chains (shortened 00:46:16, default 00:46:33 UTC): inventory, tool comparison with the approved replacements, physical PB readback against the focused baseline, startup passes of both transitions of the running invocation, recent-bin retention and eight HTTP comparisons. Each proof's invocation, JVM PIDs and tool hashes equal the observation manifest's; the only write the continuity path makes into the observation directory is its proof file, which the runner redirects, and the directory listing was identical before and after; afterwards both observations showed 903 archiving PVs, no abort request and active sample and finish timers. This binds both windows to the focused-proven deployment. | `/var/lib/etl-focused/<chain>/in-window-readiness-continuity.json` with its continuity inventory, physical, HTTP and pass files on each guest; the private runner `continuity-in-window.py`. The evaluator does not read this proof; the record carries the binding. |

##### Focused Deployment Amendment (2026-10-07)

Plan Status: accepted
Plan Acceptance: 2026-10-07, owner accepted the bounded deployment proposal with the four peer-review conditions, selected the latest aa-env branch/version, and selected actual closed-bin source expectations for all four policies
Implementation Authorization: 2026-10-07, owner instruction to proceed with tooling, separate new deployments, focused checks and the gated two-chain observations; latest aa-env selection explicitly authorized after the compatibility failure

This amendment governs new work and supersedes earlier source pins and launch ordering without changing earlier evidence. Pin Maven at `120d53fe43133c7699e4c9624dc948cc96b0ece2` and aa-env at `6599fbb1dd9a939db89a3fef6eebb08df5eb123d`, the remote head of `release-2.0.1` verified on 2026-10-07. This aa-env pin removes the obsolete site build.xml rejected by the selected Maven. Leave existing observations and their guests unchanged. Use two new Rocky 8.10 deployments through `archiver_dev_uds`, with the unchanged 903-PV fixture and accepted deadband variant.

1. Implement and test deployed effective-configuration inspection, PB fixture preparation/readback, automatic two-hop checks, independent reduction expectations and regular-pass repeats. Record tests under T13; freeze the complete tool bundle only after these checks pass.
2. Deploy both chains, record installed artifacts and all registered PV settings independently of soak preparation, and establish persistent pass DEBUG before fixture startup. Record deployment/configuration under T2/T14. Reject prior observations and conflicting fixture paths before changing files or services.
3. Select one scalar-double PV per unreduced/VeryFast/Fast/Medium policy from the existing 903 names. With the service stopped, use the shipped writer in an empty staging store and copy only absent historical partitions. Verify the complete physical baseline before normal startup. Record automatic movement, source deletion/retention, raw multiplicities, independently specified lastSample_10/30/60 output and HTTP results under T3. Do not alter policies or manually invoke ticks/jobs.
4. Capture actual source events and matching HTTP data after each recent marker's bin closes, before its reduction. Preserve this independent source proof. In the focused invocation, require a subsequent completed regular grid pass for each transition with pvCount/jobsRun=903, zero failures/aborts/skips/space deletion and no overrun, then compare the fixed historical interval and recent bin physically and over HTTP. Allow the default 28800-second cadence plus tick/order margin. Derive the recent bin's location from actual processingTime. Expect all captured raw events before reduction; reduced LTS policies expect the latest captured timestamp/value/status/severity. Continued IOC input can legitimately replace the original recent marker.
5. Start the 26-hour JFR instrumentation only after focused repeats finish. Run existing measured preparation and negative/abort checks. After the last restart, recheck running artifacts, all 903 effective settings/flags, and selected PV physical/HTTP data against the original focused proof. Bind this continuity readback to the current unit InvocationID and JVM PID/start identities; it is not restart-fault coverage and does not require another eight-hour repeat.
6. Refresh actual growth with the private fresh-capacity-refresh operation after the final restart when needed, preserving every previous source/projection. At launch require growth age <=600 seconds, runtime proofs <=3600 seconds and a successful full sample <=120 seconds. Existing full chain/readiness checks remain required. Reject missing, mismatched or incomplete focused/continuity proofs. Record this launch gate under T15.
7. Only after all gates pass, launch each new 903-PV observation for 86400 seconds across UTC midnight. Record soak, metrics, final capture, whole-unit stop and comparison under T16-T21. Preserve historical Failed/Incomplete results and explicitly retain unverified commit/deletion/space/restart fault limits. Git/GitHub publication remains separately authorized.

Required implementation paths: tests/archiver-soak/etl-pass/{common.yml,initialize-fresh.py,contract.py,verify-chain.py,focused.py,PBFixture.java,test_focused.py,test_contract.py,observe.py,launch-retest.py,bundle.json}, tests/archiver-soak/{README.md,SHA256SUMS}, and the private capacity-renewal operation. All new deployed checks and observations are Pending until their real paths execute.

Amendment Verification Results, observed 2026-10-07:

| Check | Result | Observed Method And Evidence |
| --- | --- | --- |
| T13 local tooling | Partial | Host Python 3.13.5: 79 tests, 68 passed and 11 skipped with retained actual observation inputs; `work/etl-focused-20261007/retained-tests.log`. New Rocky 8.10 Python 3.9.25: 79 tests, 50 passed and 29 skipped without those inputs; `python39-tests.log`. Real PlainPB writer/decoder readback verified 80 exact fixture inputs over both chains and rejected existing partition reuse; `validate-pb-r3.log`. This does not establish ETL movement or HTTP correctness. Bundle and checksum checks passed; independent implementation review remains pending. |
| T14 new deployments | Passed | Both initial installations failed at the site overlay with aa-env `d09dca7`; `deploy-shortened.log` and `deploy-default.log` preserve those failures. After the owner selected the latest aa-env and Maven, both actual `archiver_dev_uds` retries exited 0 with failed=0; `deploy-shortened-latest.log` and `deploy-default-latest.log`. Installed source reads confirm aa-env `6599fbb1dd9a939db89a3fef6eebb08df5eb123d` and Maven `120d53fe43133c7699e4c9624dc948cc96b0ece2` in both guests; `installed-source-{b,d}.log`. Both run Python 3.9.25 and return STARTUP_COMPLETE from all four real component endpoints; `installed-{b,d}.log`. No manual site-file deletion was used. Fixture readiness is recorded separately below. |
| T14 fixture readiness | Passed | Both original IOC fixtures installed and all 20 approved deadband fields verified. Each actual archivePV request returned 903 replies with none missing; subsequent real getPVStatus checks confirmed exactly 903 archiving and 903 connected PVs with no missing or unexpected names. Both resumed preparation processes exited 0; `fixture-{b,d}-resume.log`. A private preparation import-path failure occurred before registration and remains in `fixture-{b,d}.log`; no fixture reinstall or input replacement was used. |
| T2 effective configuration | Passed for inspected version | Actual installed inspection passed in both guests, covering all 903 effective stores/reductions, named flags, source pins, configuration hashes and process identities. Installed exploded class/JAR bytes matched their retained build WARs; `inventory-{b,d}-r2.json/log`. The preceding inspection correctly failed at an assumed installed WAR-file path; `inventory-{b,d}.log`. The corrected inspector version is preserved with the installed bundle. Repeat inspection is required after further tool or runtime changes. |
| T13 implementation review corrections | Passed for tooling; deployment execution Pending | First implementation review requested changes F1-F5: encoded root replacement, recent-file ownership, valid reduced recent-bin expectations, missing negative checker coverage, and inventory/run directory collision. Corrected real writer/decoder checks passed 160 inputs over both chains with encoded/plain roots under umask 077, including all new source paths in the ownership list; `validate-pb-r4.log`. Host Python 3.13.5 ran 86 tests: 57 passed, 29 skipped without the older observation inputs; `local-tests-r3.log`. Target Python 3.9.25 ran 85 tests: 56 passed, 29 skipped, then all nine focused checker tests passed after the final source-file-presence check; `python39-r3.log`, `python39-focused-r5.log`. Target writer/decoder checks also passed both chains with encoded/plain roots using the latest installed Maven classes, and the shipped lastSample_10/30/60 operators selected the later source event in all 12 neighbour cases; `python39-r3.log`. The three errors in `python39-focused-r4.log` came from an older module earlier in the temporary import path, not from the selected tool version. These checker inputs are retained actual M28 physical/HTTP data and actual new deployment inventory. They reject loss/duplicates/nanos/alarm/raw changes, HTTP failure, changed source/helper hashes, artifacts/settings/flags/tools, and missing/incomplete/stale proofs. These checker replays do not rerun ETL. New recent-bin capture and automatic deployment execution remain Pending. Second implementation review confirmed F1-F5 corrections but requested a fix for negative waiting time when bins were already closed. The original timer failure is retained in `closed-bin-before.log`. Closed bins now bypass waiting; open bins wait until their settlement time. All 11 focused checker tests passed on actual target Python 3.9.25; `python39-closed-bin-r2.log`. Third independent implementation review and reader pass accepted the frozen focused5e0a8783/PBaf5893db/bundlec92c5f6b implementation with no must-fix or minor findings. Peer references etl-r3-result and etl-r3-limits confirm 11 focused checker passes, actual PB decode and rejection of an incorrect HTTP interval response. The reviewer read target Python 3.9 results; its HTTP replay is not live ETL or retrieval. Automatic transfer, repeated passes, continuity, capacity renewal and both 24-hour observations remain Pending. |
| T3 automatic transfer | Incomplete | Both real focused runs started on 2026-10-08 with the accepted final tool bundle. Normal service stop consolidated STS events into MTS under effective consolidateOnShutdown=true. The post-stop nonempty-STS guard rejected both runs before seed; runner exit 1. Original physical snapshots, manifests, inventory and logs are preserved in work/etl-focused-20261007/failed-focused-{b,d}-r1.tar.gz. Both appliance services were normally started again. This is a checker/procedure mismatch, not evidence of product data loss or successful transfer. Sample integrity across shutdown has not yet been checked. |
| T13 shutdown guard correction | Passed for checker and independent review | Owner authorized correction and rerun on 2026-10-08. Keep effective STS consolidateOnShutdown=true and unreduced MTS with consolidation disabled. Require readable live pre-stop STS, no remaining JVM, and real historical-path collision checks. Preserve both physical snapshots. Compare exact known pre-stop STS timestamp/raw/value/alarm multiplicities across STS/MTS, including pre-existing MTS occurrences; allow genuinely new timestamps and reject known records in LTS. Host and actual target Python 3.9.25 each passed all 14 focused checker tests; target evidence python39-shutdown-r2.log replays both retained stopped deployments plus existing real PB/HTTP records. These are checker tests, not a new ETL execution. Fifth independent implementation and reader review accepted focused8dcf6a65 and bundle9cc94630 with no must-fix/minor findings; references shutdown-r2-accept and shutdown-r2-limits. Reviewer executed all 14 host checkers and additional cross-tier duplicate/changed-alarm mutations using actual source records. Both authorized automatic reruns started with prior Incomplete run directories retained separately. Fresh seed/startup/repeat acceptance remains Pending. |
| T3 automatic rerun | Incomplete | Both accepted guard-correction reruns started on 2026-10-08 and stopped before seed. Shortened rejected its existing focused logging drop-in; Default real PB snapshot failed with java.lang.OutOfMemoryError in PBFixture.describe under the helper 256 MiB heap. Default appliance service remained active. Neither result proves a product ETL failure. Prior first-attempt archives and directories remain intact. Logging retry handling and helper snapshot memory correction require verification before another rerun. |
| T13 bounded PB capture and logging reuse | Passed for checker, actual decoder, writer and independent review | Owner selected bounded required sample intervals on 2026-10-08. Snapshots decode real PB files but retain only old fixture, intermediate marker, recent-bin and completed 60-second source intervals; each interval <=300 seconds and at most eight intervals. Preserve the pre-stop windows when choosing seed time. This establishes integrity only for captured intervals, not every live sample. Exact existing focused drop-in content can be reused; different content is rejected. Actual target Python 3.9.25 passed all 15 focused checkers. On the actual Default PB files, the changed helper under its unchanged 256 MiB heap decoded 680258 events and retained 726, exactly matching prior actual raw/timestamp/value/alarm multiplicities in the selected interval. Overlapping windows did not duplicate records. Empty, nonpositive, oversized and excessive windows were rejected by actual helper executions; python39-bounded-r1.log. Actual target writer/decoder checks passed both chains with encoded/plain roots and all 12 real lastSample neighbour cases; python39-bounded-writer-r1.log. Complete actual decoder/writer manifests, readbacks, helper classes and logs are retained in actual-bounded-validation-r1.tar.gz. The four invalid-window logs show the expected IllegalArgumentException messages from snapshotWindows. Sixth independent implementation/reader review accepted unchanged source focused6fa3d849/PBf683130f/bundle75a852e6 with no must-fix/minor findings; reference bounded-review6-accept. Reviewer executed all 15 host checkers, inspected full run binding and reader procedure, and verified 22 bundle hashes and diff check. Its acceptance applies to captured intervals and tooling, not fresh automatic ETL. No new automatic ETL acceptance or soak start. |
| T3 bounded-tool automatic rerun | Incomplete; same-invocation continuation authorized | Both finite background runs started on 2026-10-08 with accepted focused6fa3d849/PBf683130f/bundle75a852e6. Source hashes matched the reviewed freeze before installation. First and second Incomplete directories and their original archives remain intact. Both real shutdown-preservation checks and seeded physical baselines completed before normal startup. The early empty-pass poll wrote a blank line and the checker rejected it as JSON, preserving result=Incomplete; actual archives failed-focused-{b,d}-r3.tar.gz retain the original source bundle and proofs. Owner selected the same service/fixture continuation on 2026-10-08. No new seed or restart is authorized by this continuation. Corrected real journal reads confirm both startup transitions completed 903 jobs with zero failures/skips/space deletion in both original invocations; startup-pass-probe-{b,d}-r1.json. These counters alone do not establish physical or HTTP integrity. |
| T13 original-fixture continuation | Passed for original guard/checker; actual continuation Incomplete | Empty completed-pass polls produce an empty file and wait; malformed JSON still fails. The common finish_run executes real startup, physical/HTTP and scheduled-repeat checks for both fresh and resumed runs. Actual prepare-resume passed in both original guests, requiring the same boot/invocation and four JVMs created within the original run window. All source file hashes match original R3 archives; prepared-resume-{b,d}-r1.tar.gz. Actual target Python 3.9.25 passed 18 checker tests, including original/preserved file mutations and boot/invocation/PID/start changes; python39-resume-r1.log. Resume must independently recheck all 903 configurations, flags, artifacts and unchanged helper tools before physical/HTTP work. Actual resume outcomes are recorded in the continuation execution row. |
| T13 continuation completion checks | Passed for target checker and implementation review; reader correction recorded | Seventh independent review requested changes F1/F2: the final runtime and original-source/helper/tool hashes were not compared with the accepted original invocation and freeze before Passed. Corrected focused0d7d57f6/bundle988bdfd5 stores final inspection separately, verifies final and current boot/invocation/four JVM identities, compares approved resume tools, all preserved originals and immutable live inputs including compiled helper and logging, and rejects a changed guard. Only live result and pass files may change. The code restores Incomplete after a post-finish evidence error; that exception path has not been executed. Actual target Python 3.9.25 passed all 20 checker tests with no skips; python39-resume-r2.log. The checker permitted changes to the live result and pass outputs, and rejected mutations of every preserved/immutable input and final configuration/tools/runtime. This did not execute a post-finish evidence exception. These checker executions do not establish resumed ETL or HTTP acceptance. Eighth independent implementation review accepted F1/F2 for focused0d7d57f6/bundle988bdfd5; references etl-focused-resume-r2 and resume-review8-error-evidence. The reviewer independently passed all 20 shipped checkers without skips, verified all 22 bundle hashes and both sets of 11 original files against R3. Its reader finding required the explicit unexecuted exception limit recorded here. Actual continuation was subsequently executed and remained Incomplete, as recorded below. Actual guard refresh at 2026-10-08 19:07 UTC confirmed both original boot/invocation/four JVM identities and every original/preserved file unchanged; guard-refresh-{b,d}-r2.log. The delivered review request initially awaited peer processing; the eighth review subsequently completed. The approved same-fixture resume was subsequently launched; its actual outcome is recorded below. |
| T3 same-fixture continuation execution | Incomplete; fixture ordering precondition violated | Both approved focused0d7d57f6/bundle988bdfd5 resumes started at 2026-10-08 20:42:30-31 UTC after verifying the original runtime, unchanged original inputs and installed freeze. Both completed their configuration inspection and real PB snapshot, then exited 1 at 20:42:45 UTC with Physical LTS events differ. All four policies in both chains had eight original old STS samples and zero observed old samples in every tier afterward. Original startup hop0 reported eight streams/partitions moved, 936 bytes and zero jobs failed. The actual original startup journals contain eight bulk append rejection records per chain, one for each old and middle source partition; startup-append-rejections-{b,d}-r2.jsonl. Before seed, every selected MTS already held captured timestamps later than both seeded old/middle intervals. The deployed append timestamp guard rejects input not newer than the destination's last timestamp; this historical backfill fixture violates that precondition. These runs do not establish valid chronological transfer or a product regression. Full original/resume inputs, physical snapshots and results remain in failed-resume-{b,d}-r2.tar.gz. HTTP, recent-bin capture, final identity/provenance checks and complete regular-repeat verification were not reached. No appliance restart, reseed, policy or original IOC fixture changes occurred during resume/diagnosis. Actual post-failure guard checks at 2026-10-08 22:21 UTC verified both original appliance invocations and all immutable original/preserved files; post-failure-guard-{b,d}-r2.log. The independent archive/source review confirmed all eight chain/PV old8-to-zero cases, the deployed/current source equivalence for the relevant append and job classes, and each of the eight actual rejection records per chain. It did not classify this as a normal chronological-input product regression. The next decision is a plan for natural movement of a newly captured source cohort under unchanged holds, or a separate clean-destination fixture; neither is authorized for execution by the current same-fixture continuation. |
| T29/T30 consumer local rehearsal (Ordered Work 3) | Partial; control host only | 2026-10-10T10:41Z, control host Python 3.13.5, `focused.py` SHA256 `c8952f75baab7512…`. The shipped consumer accepted both chains from the retained final and recheck archives (1870 and 967 bound source files) and rejected each change in its own condition: altered error string, result or chain, wrong proof hash, absent entry and other chain's proof, altered source and recheck file, missing file, wrong checker and helper hash, changed key-input name, properties hash, expected-keys hash and expected key value, changed proof identity, and PBFixture.java or another tool changed in a re-frozen bundle copy; an unfrozen change fails at `verify_bundle`. Weakening one condition at a time in scratch copies made exactly the matching case fail. Evidence: `test_focused.RecheckProofConsumerTests`, 7 tests OK with `FOCUSED_RECHECK_ARCHIVES`; 58 tests OK, 27 skipped in `test_focused` and `test_contract`. Host Python is not target compatibility evidence. The fresh-inventory comparison, identity stability during a readback and condition 7 are guest-only and remain Pending (T29/T30 on a guest, T32); the working tree is not frozen and `bundle.json` still describes the previous `focused.py`. |
| T31 replacement step local rehearsal (Ordered Work 3) | Partial; real filesystem on the control host | 2026-10-10T10:41Z, `replace-bundle.py` SHA256 `d72ed3de4bffaa4e…`, `ACCEPTED_BUNDLE_SHA256` still unset. On a private directory tree holding bundle members, `pvs-all.csv`, database files, a nested directory and a mode 0750 file, the step swapped in the candidate bundle, carried every other file with digest, mode, timestamp and owner unchanged, preserved the previous tree byte-for-byte, and rolled back through two renames. It refused a wrong or unfilled hash, a member changed after the freeze, an active sampler timer or activating finish unit, and an existing staged sibling, each leaving the installed tree and siblings unchanged; an archive bundle was unpacked and an unsafe member rejected. Evidence: `test_focused.BundleReplacementTests`, 4 tests OK; only `systemctl` was replaced. The SELinux security context and ownership change as root were not exercised; the guest delivery check (T31) compares them. Restoring the copy of members only, not the whole directory, made 3 of the 4 tests fail. |
| Bundle freeze and replacement step literal (Ordered Work 4) | Frozen locally; independent review accepted at `169ca96` and implementation accepted by the owner on 2026-10-10 | 2026-10-10T10:50Z. `contract.py --freeze` rewrote `bundle.json` with exactly one changed member, `focused.py` `4265dfac…` to `c8952f75baab751281de87b5cfa571c6fa43c519bb4376252c765c16a8ef86b9`; `verify_bundle` passes on the 24 members. Frozen `bundle.json` SHA256 `5168ca0e495ea8720704bada64f3297b8c12d48ae2037acfb4762f9cb237cd15`, filled into `ACCEPTED_BUNDLE_SHA256` of `replace-bundle.py`, whose SHA256 was then `eb66af7961cdef8e68718c04bf9bb50ca6a6a60117aada9332c53ed1dd1593ba`. After the independent review of 2728000 the step refuses a symbolic link or non-regular file in the installed directory or the bundle and prints the single recovery `mv`; its SHA256 is now `7ef22236e7fb66712b2a5e6760ce267f6d00fa1b85983cc6413465dd0009bae3`, and `bundle.json` and `focused.py` are unchanged. A proof-chain and proof-result case was added to the consumer tests; 59 tests OK, 27 skipped. The shipped command line replaced a scratch copy of the previous bundle and rolled it back: installed files equal the frozen files, the extra file survived, and the previous `focused.py` returned. Evidence: 58 tests OK, 27 skipped; 55 `SHA256SUMS` entries match. The scratch run used the host `systemctl`, which reported the three units inactive, and no guest. The T29/T30 local results above ran with the same `focused.py` SHA256. |
| T29/T30 on the guests (Ordered Work 5) | Passed on both chains | 2026-10-10T17:16Z, target Python 3.9.25, candidate consumer run from a private staging directory with a private copy of the frozen bundle (`5168ca0e…`) as the explicit bundle root and the installed modules found through `PYTHONPATH`; `focused.py` SHA256 `c8952f75…`. T29 (`check-recheck`): against the live appliance the fresh `artifacts`, `pvs` and `flags` equalled the recheck inventory strictly and the tools comparison passed on both chains; the imported-module map names `focused.py` from the staging directory and every other project module from the installed path; the proofs `eb5e0f73…` and `491bca76…` matched their pins. T30: `RecheckProofConsumerTests`, 7 tests OK on each guest on the archived copies of the retained final and recheck evidence, with `test_focused.py` SHA256 `cbdd92a2a6cbbd87…`, the version that holds the proof-chain cases. Evidence: `recheck-acceptance.json` in a private scratch directory per guest. Limits: T30 used the retained archives copied to each guest, not a copy of the in-place tree; nothing was written under the retained tree. |
| T31 delivery of the frozen bundle (Ordered Work 6) | Passed on both chains | 2026-10-10T17:17Z. On each guest the step first replaced and rolled back a private copy of the installed directory and restored it byte for byte; the delivery then changed exactly `PBFixture.java`, `bundle.json` and `focused.py`, added and removed no file, and left ownership, mode and SELinux security context (`usr_t`, enforcing) of every file and of the directory unchanged. The previous directory is preserved as a sibling equal to the pre-delivery listing; the file list under `/var/lib/etl-focused/<chain>/` is unchanged (1878 and 975 files); `verify_bundle` passes on the 24 members; installed `bundle.json` `5168ca0e…` equals the step's literal. The sampler and finish units stayed inactive and the IOC and appliance units stayed active and were not restarted. How the checks ran: on the default guest one corrected script ran the whole sequence; on the shortened guest the first script completed the rehearsal, both listings and the file-change, attribute and retained-list comparisons, then stopped at its own parsing of the step output, and the preserved-sibling comparison, `verify_bundle` and the unit states were run by hand afterwards, their outputs kept with the listings; the literal comparison there rests on the step's own refusal of a different hash and the installed hash. Plan items: `inventory()` reading `pvs-all.csv` after the swap is shown by T32 on both chains, and the re-verification of every `source_evidence_sha256` and `recheck_evidence_sha256` entry is T29 before and `require_continuity` after. Evidence: before and after listings and the step output in a private directory per guest, preserved sibling `etl-soak.prev-<UTC>` on each. Limits: no rollback was run on the installed directory; the rehearsal rollback ran on the private copy. |
| T32 continuity binding (Ordered Work 7) | Passed on both chains | 2026-10-10T17:17:44Z (shortened) and 17:18:09Z (default): the installed `focused.py continuity` accepted the recheck proof, the identity stayed unchanged during the readback and equals the original execution's (`0f2126526…`, `481adce7c…`), and the current invocation's automatic startup passes were present; `require_continuity` then returned Passed, binding the original result SHA256 (`25a677e4…`, `90e0eeba…`) and the recheck proof SHA256 (`eb5e0f73…`, `491bca76…`). Negative cases, read-only on private copies of the proof with the live file unchanged: a proof older than 120 seconds (150 s on the shortened guest, 125 s on the default guest) was rejected with `Current focused continuity evidence is required`; a copy naming the other chain with a fresh timestamp was rejected with the same message; a copy without the recheck proof hash was rejected with `Continuity does not bind both the original result and the recheck proof`; an unchanged copy with a fresh timestamp was accepted, so the rejections follow from age, chain and binding. Evidence: `continuity-20261010T171744913115*` and `continuity-20261010T171809793959*` beside the retained records and `readiness-continuity.json` under `/var/lib/etl-soak`. Limits: this is not the launch continuity after the final restart; instrumentation, measured preparation, negative and abort checks, capacity renewal and both observations remain Pending. |
| T15 launch continuity | Pending | No launch-continuity execution or new observation start. |
| T16-T21 new observations and final comparison | Pending | Neither new observation was launched; prior observations and their results remain unchanged. |

##### Summary

Observe the deployed ETL pass scheduler on the earlier shortened store chain
and the epicsarchiverap-env default chain, using independent VMs in parallel.
The scheduler design at epicsarchiverap-maven `3bdf378c`, including Testing
item 10, defines the timing, metric meanings and comparison with M14/T21.

##### Scope

Two independent Rocky 8.10 `archiver_dev` deployments made through the full
species, with MariaDB over its Unix socket and a 256M heap per instance.
The accepted plan reuses those deployments and preserves existing archived
data. Shortened has a 40-GiB disk and default has a 48-GiB disk; verify current
resources and space for the complete observation window. Runtime variables pin epicsarchiverap-env
`d09dca7` and epicsarchiverap-maven `3bdf378c` without changing role defaults.

| Run | STS | MTS | LTS | PV fixture |
| --- | --- | --- | --- | --- |
| Shortened | PARTITION_5MIN, hold 2 | PARTITION_HOUR, hold 2 | PARTITION_DAY | Original 903-PV registration list and three IOC databases; accepted plan uses the ten-record `retest-deadband.db` override |
| Default | PARTITION_HOUR, hold 2 | PARTITION_DAY, hold 2 | PARTITION_YEAR | Separate copies of the same registration list, databases and accepted override |

Out of scope: scheduler code changes, repository-wide pin changes, host-sizing
experiments, SQLite coverage, repeated retrieval stress, deliberate archive-store
failures, disposal or reuse of the previous soak VM, and an exhaustive audit
of every source sample. The existing all-PV freshness and representative
visibility probes do not establish lossless archival.

##### Completion Criteria

- Both deployments identify the exact source commits, rendered store settings,
  effective properties, PV population and unit stop timeout.
- Both new observations run for at least 86400 seconds after readiness in
  UTC and monotonic time, cross UTC midnight, and retain complete pass logs
  and hourly ETL metrics. A short-trial verdict cannot satisfy this criterion.
- Both observations retain per-component GC before/after heap, collection
  causes and pauses, complete jstat counters, RSS, retrieval freshness and
  representative visibility bounds. Report collection gaps, restart and OOM
  evidence, and distinguish observed heap maxima from continuous maxima.
- Journal collection integrity and retention, formerly T22-T28, belong to
  `M25` from 2026-10-05 and are verified there. An observation opens only
  after T27's preparation portion (`M25` / T6) passes in the shipped tools.
  Under `D23`, since bundle `11ee9c8e` a failed in-window journal budget is
  recorded as a journal finding and does not count toward the abort or the
  verdict, while record loss, coverage gaps, suppression and the stored-entry
  count still do.
- After the startup pass, each pass retains the design's planned grid time.
  Under normal soak load, a pass with no preceding-transition wait starts
  within one 5-second tick of that time. A pass held by the ordering rule
  starts at the first tick after the preceding transition ends, retaining its
  original `plannedAt`. Verify both elapsed time from `plannedAt` and, when
  waiting occurred, elapsed time from the preceding pass's `endedAt`.
  Ordering, completed-pass counters and metric values agree with the pass
  records, with no overrun.
- A measured stop of the whole unit on each VM completes successfully within
  that unit's actual `TimeoutStopSec`, without forced termination.
- A comparison records last-pass and average busy time and weekly usage against
  the matching earlier load. The retired running-sum last-job value has no
  counterpart. Record actual event rate, retrieval concurrency, fixture,
  store age and resource differences; equal PV count alone does not establish
  equal load. Where earlier event-rate evidence is absent, label the numerical
  comparison as descriptive and make no performance-improvement claim.
- A recipient can identify the exact canonical plan/results version and
  independently check sanitized pass timing, metric values, GC statistics,
  fixture and tool hashes, window boundaries and evaluator output. Private
  inventories, credentials and unsanitized logs remain local.

##### Dependencies And Decisions

- Decision Date: 2026-09-28. The owner selected epicsarchiverap-maven `3bdf378c`
  and epicsarchiverap-env `d09dca7`, two VMs in parallel, and the same 903-PV
  fixture for both chains, then authorized execution of this plan.
- Decision Date: 2026-09-28. Correct the start-time criterion to include the
  pinned scheduler design's ordering rule: a held pass starts at the first
  tick after the preceding transition ends. Apply this criterion to the
  ongoing observations; retain the original planned timestamps and measured
  delays as evidence.
- Decision Date: 2026-09-28. Add per-GC heap and pause evidence and collection
  latency probes before restarting both appliance observations. Preserve the
  earlier evidence and existing stores. Start a new 24-hour window only after
  the additional instruments record real data and all 903 PVs are archiving.
- Decision Date: 2026-09-28. Preserve the measurement methods, current ETL tools,
  baseline soak tools and original fixtures under `tests/archiver-soak/`.
  Keep run evidence and private inventory/configuration data outside that tree.
- Decision Date: 2026-09-29. Expand the default VM's disk from 20 to 40 GiB
  online, retaining the existing observation window and data. Record the
  capacity change in the test conditions; the shortened VM remains at 20 GiB.
- Decision Date: 2026-10-01. Expand default from 40 to 48 GiB while preserving
  its stores and prior evidence. Actual projected usage on 40 GiB was 85.4005
  percent, above the accepted health threshold. Shortened remains at 40 GiB.
- Decision Date: 2026-10-01. Apply service-specific journal interval 1us and
  burst 10000 to both VMs after the initial 0/0 settings still allowed an
  observed 3741-message suppression on default. Preserve all previous failed
  preparation evidence and repeat real capacity, shutdown journal and T15
  checks before starting either full-window observation. The global journald
  configuration remains unchanged.
- M17 and M21 are completed deployment prerequisites. G4 completed on
  2026-09-28 with both VM inventories, the selected fixture and the initial
  capacity assessment. Post-installation space remains a T2 check.
- Both runs use `work/soak-9eed006/pvs-all.csv`, SHA256
  `037a92691bc23a6dcac37ec3613ad19c9f80b93b689209ec8dc403b519eaf594`.
  The fixture rates are one second for 783 PVs, 0.1 second for 110 PVs and
  10 seconds for 10 PVs; the registration methods are 880
  MONITOR and 23 SCAN. Both copies preserve the original policies and rates.
- G2 remains specific to M14's remaining middleware work; it does not prevent
  the existing archiver-dev deploy path from running this soak.
- The default chain's MTS-to-LTS cadence is capped at 8 hours, so its planned
  firings are 00:10, 08:10 and 16:10 UTC. Its hold of two day partitions means
  that a fresh 24-hour run does not verify new data reaching LTS. Scheduled
  passes with no eligible partition must still be observed and reported.
- `ETLPassStopWaitSeconds` defaults to 60 seconds and can be applied twice,
  followed by consolidation; it is not a 60-second bound on the whole unit.
- Decision Date: 2026-10-01. Apply all five findings from the first
  third-person review of the journal-scenario amendment. Split T27's
  preparation and in-window requirements; verify existing adjustments on
  both VMs; define numerical retention criteria and failure handling;
  add dedicated test-environment preparation; separate historical defects
  from current findings. This direction authorizes plan edits only.
- Decision Date: 2026-10-01. Accept the journal-scenario revision with all
  five review corrections reflected. Implementation authorization remains
  separate; dedicated test-environment selection/acquisition and all new
  scenario executions remain pending.
- Decision Date: 2026-10-01. Authorize collector correction, retention-budget
  implementation and local verification under the accepted journal-scenario
  revision. Preserve the original frozen tools and both terminal observations.
  Dedicated environment selection and live execution remain pending.
- Decision Date: 2026-10-01. Proceed with the accepted dedicated-VM plan,
  preserving both retained soak deployments. Select disk option 2, 48 GiB,
  with 2 vCPU and 4096 MiB RAM on the existing image-storage filesystem.
  Record acquisition, inventory, execution authority and baseline evidence
  in private `journal-test-environment.json`; scenario prerequisites remain
  mandatory before any replacement observation.
- Decision Date: 2026-10-01. Select option 1: replace the version command
  with systemctl --version in both current journal tools, verify a new frozen
  bundle, and apply it to the dedicated VM. Preserve original tools and both
  retained soak deployments.
- Decision Date: 2026-10-02. Proceed with a separate fresh-VM initializer and
  the remaining accepted preparation sequence. Initialize GC/JFR and real
  finite measurement units without manufacturing prior observation/terminal
  records. Require actual source, fixture, unit, recording, retention and
  capacity evidence; verify the new bundle on the dedicated VM before the
  required live scenarios or replacement deployment.
- Decision Date: 2026-10-02. Make the schema-5 tools standalone: remove the
  schema-3 evaluator and the nineteen schema-4 files from the shipped tree and
  bundle, and report an observation under any other schema as unsupported.
  Keep the removed sources in the private evidence directory as
  `legacy-sources-removed-from-tree-20261002/`. Add retained-evidence
  checks for the Passed replay, missing scheduled pass, missing GC pair and
  aborted observation cases after a schema-5 observation completes.
- Decision Date: 2026-10-02. Correct the retention accounting in the shipped
  tools rather than raise the journal cap, change the archiver logging policy
  or resize the VM. The single daemon `write_bytes` counter is counted once,
  as the system-stream bound; the user-stream bound is the user journal's own
  allocation growth. A preparation or validation interval shorter than 300
  seconds is no longer a rate bound; its identity and accounting continuity
  are still checked. Installation on the dedicated VM and a new measured
  preparation remain separately authorized steps.
- Decision Date: 2026-10-03. Apply the same 300-second rule between two
  in-window collections, in `runtime()` and in the evaluator, after
  back-to-back readiness samples on the second dedicated VM failed the
  budget. Repeat the measured and fresh preparation on a third dedicated VM;
  keep the second VM and its evidence unchanged.
- Decision Date: 2026-10-03. Make the terminal path stop only the observation
  timers that are loaded, after the third dedicated VM's abort check failed
  on the finish timer that exists only after a launch. Repeat the preparation
  sequence on a fourth dedicated VM; keep the third VM and its evidence.
- Reported 2026-10-04 UTC by the LAB session: at the owner's direction, for
  disk space, the LAB host removed both retained schema-4 trial VMs and the
  first dedicated VM, with their disks and address reservations. Their on-VM
  manifests, terminal records, raw samples, stores and installed tools are
  gone. Private copies under `work/soak-etl-pass-3bdf378c/` keep the trials'
  launch and journal records but no `observation.json`, `abort.json` or raw
  samples; the first dedicated VM's retention inputs remain in
  `journal-retention-diagnosis-20261002/`. Plan text that targets the
  retained deployments has no target until the owner re-plans the two
  chains.
- Decision Date: 2026-10-03. Rebuild both chains on fresh dedicated VMs on
  the control host: the fourth dedicated VM becomes the shortened chain and
  a fifth dedicated VM the default chain, each prepared through the same
  fresh-VM sequence with bundle `bbbf5d90` before its 24-hour observation.
- Decision Date: 2026-10-03. Treat a zero-write interval in which only a
  journal file's modification time changed as no growth, after the fourth
  dedicated VM's abort check failed on such a 0.293-second interval. A
  changed size, allocation, identity or file set with no counted writes is
  still refused. Prepare both chains again on two new dedicated VMs with
  the corrected bundle; keep the fourth and fifth VMs and their evidence.
- Decision Date: 2026-10-04. Move the epicsarchiverap-maven pin from
  `3bdf378c` to the current `modernize` head `254a6542`, keeping
  epicsarchiverap-env at `d09dca7`. The new head carries `d80eef3a`, which
  moved five of the seven per-request retrieval INFO lines to DEBUG, so each
  probe request writes three INFO lines instead of seven. Between the two
  commits the ETL pass scheduler, its design document and the engine rate
  metric definitions (`EngineMetrics.java`) are unchanged; `0fbd5592` only
  corrects a per-PV ETLDetails value that the evaluator does not read. The
  remaining per-request logging is studied in
  jeonghanlee/epicsarchiverap-maven#24.
- Decision Date: 2026-10-05. Move the epicsarchiverap-maven pin from
  `254a6542` to `aa953a44`, which carries the CA search-port correction
  `7adc7d5a` (jeonghanlee/epicsarchiverap-maven#26) that the maven owner
  declared final; its Maven workflow passed on `aa953a44`. Between the two
  commits the packaged sources differ only in the engine's `EngineContext`
  and `JCACommandThread`; the ETL scheduler, `EngineMetrics.java` and the
  logging configuration are unchanged. Both chains are prepared at this pin.
- Decision Date: 2026-10-05. Open the 24-hour observation on both prepared
  chains, and let the assistant run `launch-retest.py` and the preceding
  refresh steps on the two VMs.
- Decision Date: 2026-10-05. After both observations aborted at the first
  rotation of the system journal, correct the retention accounting so a
  renamed journal file is not counted as growth, prepare two fresh VMs with
  the new bundle under new names, and open both 24-hour observations again,
  including the launch steps. The aborted VMs stay until the new observations
  have started; their evidence is preserved privately.
- Decision Date: 2026-10-05. Let the store size measurement accept the total
  that `du` prints when it exits 1 only because files vanished during its
  walk, after the shortened-chain observation of the new pair aborted on that
  exit status. Prepare one more VM for the shortened chain with the resulting
  bundle; the default-chain observation that had just started on the earlier
  bundle continues.
- Reported 2026-10-04 by the epicsarchiverap-env session, on its owner's
  decision of that date: the two Rocky 8.10 defects seen in this soak are
  split by owner. This repository owns the journald loss; the CAJ shared
  search port belongs to epicsarchiverap-maven (#26). Each owner first
  proves the exact cause and fixes it on its own side; any patch or
  mitigation stays local, and no report goes to Rocky/RHEL or systemd until
  that owner revisits it. Each session requests its own VMs from
  cloud-provision. For the journald loss, the agreed first stage is a
  reproduction without the appliance: concurrent `systemd-cat` writers on
  fresh Rocky 8.10 and Debian 13 guests, comparing emitted and read-back
  lines, sequence holes and `journalctl --verify`, varying writer count and
  rate to find the loss threshold, and excluding rate limiting. Whether a
  hole fails the soak or is recorded within a measured limit is decided
  after that threshold is known. The epicsarchiverap-env side, measuring how
  both defects reach its VM acceptance checks, is tracked in
  jeonghanlee/epicsarchiverap-env#58; stage-1 results reference it.
- Decision Date: 2026-10-04. Take the journald reproduction stage: request
  one fresh Rocky 8.10 and one Debian 13 guest from cloud-provision and run
  the concurrent-writer reproduction there. On both guests a journald
  drop-in sets `RateLimitIntervalSec=0` before the runs, so suppression
  cannot account for a loss; each run still reports any Suppressed record.
- Decision Date: 2026-10-04. An unreturned sequence number no longer fails a
  journal interval, after the reproduction showed that systemd 239's
  `journalctl` hides stored entries and loses none. An interval still fails
  without its system anchor or terminal marker, on suppression, or on a
  changed boot or daemon; it records the unreturned numbers. At every
  collection the journal file headers must show one stored entry per
  sequence number across the range whose files are all retained, and an
  unreturned number outside that range fails the interval, so T25's
  required-record loss still cannot yield complete coverage. A first
  version that accounted only once at the terminal boundary was replaced
  the same day because retention could remove a lost file from the range
  before the end. No report goes upstream.
- The dedicated journal test environment is a required preparation input for
  live T22-T26/T28 checks. G4 supplies only the two retained soak deployments.
  The subsequent owner direction authorized a separate VM; its baseline,
  inventory and authority are now retained in the private environment record.
  Archiver-dev installation is verified there; its measurement prerequisites
  remain incomplete. A second dedicated VM, created on the control host on
  2026-10-03 and recorded in private
  `journal-test-20261003/environment.json`, has completed archiver-dev
  installation, fixture, instrumentation, measured preparation and fresh
  preparation; its runtime verification and the live scenarios remain.
  Neither reuse nor changes to the retained VMs follow from either
  dedicated-environment preparation.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-10-01; the owner accepted the journal-scenario revision with all five third-person review corrections reflected
- Implementation Authorization: 2026-10-01; collector correction, retention-budget implementation and local verification; subsequent owner direction authorizes the accepted dedicated-VM plan and selects a 48-GiB disk. Replacement observations remain gated by the required live checks and fresh preparation
- Revision Date: 2026-10-01
- Scope: two independent, parallel observations of at least 24 hours each,
  followed by measured shutdown, T6 comparison and independently checkable
  result delivery. The accepted scope includes applying the same ten-record
  deadband variant to both VMs while retaining the all-903-PV 30-second
  freshness requirement. The earlier acceptance of the shortened two-hour
  variant does not authorize this revised execution.
- Previous accepted plans and their observations remain below. Their
  authorizations do not authorize the current revision. Plan acceptance does
  not start a new trial.

###### Retention Accounting Correction

- Plan Status: accepted
- Plan Acceptance: 2026-10-02; the owner accepted correcting the accounting instead of the cap, logging policy or VM size. 2026-10-03 revision: the owner accepted applying the 300-second rule to in-window collections and the evaluator, and a third dedicated VM for the changed bundle
- Implementation Authorization: 2026-10-02; code correction, bundle regeneration and local verification. 2026-10-03; step 4 (candidate installation and measured preparation) on a second dedicated VM, together with its species deployment and fixture before it and the fresh preparation after it, and its readiness checks. 2026-10-03 revision: the in-window correction, its local verification and the same preparation sequence on a third dedicated VM
- Superseded Plan Artifacts: step 1's earlier statement that `runtime()` and the evaluator keep their interval handling; bundles `e11d3ebc`, `7c551c4b` and `bbbf5d90`; every statement of this Implementation Plan that requires completed T22-T26/T28 before an observation opens (moved to `M25` on 2026-10-05, `D22`)

1. `tests/archiver-soak/etl-pass/journal_retention.py`: `rates()` returns
   `max(write delta, system allocation growth) / duration` for the system
   stream and `user allocation growth / duration` for the user stream.
   `prepare()` and `validate()` still run `elapsed()` and `rates()` on the
   interval from the last measured snapshot to the current one, but take it
   as a rate bound only when it lasts at least 300 seconds. The 2026-10-03
   revision applies the same rule between two in-window collections:
   `runtime()` computes its budget through `interval_budget()`, which keeps
   the gap limit, and the evaluator's peak uses `bounded_interval()`.
2. `tests/archiver-soak/etl-pass/test_journal.py`: a real-input regression
   replays the seven actual dedicated-VM snapshots and the failed proof's
   actual final snapshot through the shipped functions. It must fail on the
   tools at `55ae31a` and pass on the corrected tools. Arithmetic tests cover
   the shared counter and the short-interval rule.
3. Regenerate `bundle.json` and `SHA256SUMS`, then run the shipped local
   suite with and without the private evidence paths.
4. Installing the corrected bundle on the dedicated VM and a new measured
   preparation in a new evidence directory need separate authorization.

Steps 1-3 are implemented and locally verified; step 4 ran on a second
dedicated VM on 2026-10-03 (results below). Its readiness health check then
exposed the in-window interval defect; the revised steps 1-3 are locally
verified, and step 4 repeats on a third dedicated VM because the shipped
prepare action refuses to replace an existing preparation. The third VM's
abort check exposed the unloaded-finish-timer defect in `observe.py`; that
correction is locally verified and step 4 repeated on a fourth dedicated VM.
That VM's abort check exposed the modification-time-only race in `rates()`;
that correction is locally verified and step 4 repeats on two new dedicated
VMs, one per chain.

The preceding two-chain revision was accepted on 2026-09-30. Its steps 1-2
were authorized for implementation and local verification on that date;
steps 3-7 were authorized on 2026-10-01 for preservation, frozen-bundle
deployment, actual preparation and the two observations. Those observations
are now terminal and remain Incomplete. This amendment adds required journal
scenarios; it does not select a collector algorithm or a larger journald cap.

###### Basis And Checks Still Required

| Class | Finding | Evidence / Next Check |
| --- | --- | --- |
| Confirmed finding | The passing shortened trial covers two hours; both successful 24-hour windows and T6 remain required | T11/T12, original T4/T8 reassessment and Completion Criteria |
| Confirmed finding | The corrected collector was applied after the passing trial | Post-terminal VM application evidence below; repeat hash-bound runtime preparation on both VMs |
| Confirmed finding | Freshness is sampled latest-data availability; changed deadbands can change load | `measure.py`, `fixtures/retest-deadband.db`, original T8; report actual event-rate observations and avoid sample-preservation claims |
| Confirmed finding | Both current VM fixtures already have the accepted adjustment | Actual read-only inspection at 2026-10-01 23:53:41 UTC: both adjustment records, overrides and IOC drop-ins exist; each real CA query returns twenty values of -1; preserve and verify both existing adjustments |
| Confirmed finding | The frozen collector retains the last kernel cursor when no new kernel record exists; both trials aborted after that pre-trial cursor disappeared | `collect.py::collect_kernel`, both actual `abort.json` records and failed full samples at 18:20/18:25 UTC on shortened and 21:30/21:35 UTC on default; T22-T28 must distinguish obsolete anchors from required-record loss |
| Confirmed finding | Earliest retained system records still preceded both trial starts during the post-abort inspection; a user journal can retain older records independently | Actual system-only journal inspection on 2026-10-01; shortened earliest system record 2026-09-30 07:55:01.063035 UTC and default 2026-10-01 06:49:49.287537 UTC; this observation alone does not prove all required records were retained |
| Hypothesis | Replacement-tool coverage, retention headroom and comparison evidence will satisfy the full-window criteria | Resolve through T22-T28 and new T14-T20 executions; previous successful preparations do not prove the replacement tools or an entire 24-hour window |
| Confirmed finding | Existing retest entry points require previous observation records; a separate initializer is required for the fresh dedicated VM | Actual preflight at 2026-10-02 05:17:03 UTC found no instrumentation or abort unit. Authorized initialize-fresh.py instrumentation succeeded at 07:28:37 UTC and preserves genuine configuration/JFR/GC evidence. On the second dedicated VM on 2026-10-03, initialize-fresh.py measured retention/capacity preparation passed at 07:33:25 UTC and its prepare action succeeded at 07:35:14 UTC; full-sample readiness remains pending. No synthetic observation or terminal record is permitted |

###### Historical Findings And Implemented Corrections

These findings describe the inputs to the 2026-09-30 implementation. They are
not current missing features. Their dated verification remains below; full
window acceptance and the newly identified stale-kernel-anchor defect remain
separate requirements.

| Historical finding | Current implemented behavior | Evidence / Remaining Check |
| --- | --- | --- |
| Preparation selected 7200 seconds and used only the shortened schedule | Schema-4 preparation and launch bind explicit 7200/86400-second duration and shortened/default configuration | T13 local checks and the actual two 86400-second manifests; replacement readiness and full windows still required |
| Normal finish allowed a two-second tolerance and evaluation lacked independent duration/midnight checks | Current observer waits for both complete durations; evaluator checks duration and UTC midnight independently | T13/T19 local results; both new aborted runs correctly retain missing duration, with normal full-window completion still unverified |
| Kernel queries restarted at the UTC-day boundary; result delivery depended on private uncommitted inputs | Current collector carries a persistent boundary/cursor; the T21 portable package contract is specified | Persistent cursor handling has the current stale-anchor defect; package execution and transferable evidence remain pending |
| Fixture reapplication rejected an existing adjustment without a verification entry point | apply-fixture.py has --verify-existing; preparation preserves adjustment evidence | T14 local and actual VM results; both current deployments now use verification, with conflicting/partial adjustments still rejected |
| Readiness hashes omitted helpers and JFR configuration | Current complete bundle covers eighteen dependencies, including resource_helpers.py and heap.jfc | Actual contract.verify_bundle execution during the first review confirms all eighteen entries; a replacement bundle and proofs remain required |
| Exact timestamps inflated counts in overlapping JFR exports | Current aggregate.py uses matching payload and bounded integer-nanosecond clusters | Historical T18 replay and overlap regressions are recorded; new full-window GC coverage remains required |

###### Accepted Review Corrections

Decision Date: 2026-10-01. All five findings from the first third-person review
were accepted for plan correction. The following changes are reflected in the
accepted plan; they are not evidence that the new checks have executed.

| Finding / Charter Item | Plan Correction | Execution State |
| --- | --- | --- |
| 1 / C3 preparation order | T15 requires only T27 preparation; T27 in-window checks run at T16 and close at T19 | Both T27 portions Pending |
| 2 / C4 actual fixture state | Step 3 and T14 verify existing adjustments on both VMs; missing/conflicting inputs stop preparation | Actual twenty-field checks on both VMs observed at 23:53:41 UTC; replacement preparation Pending |
| 3 / C2 numerical verdict | T27 defines gap limits, factor-two allowance, stream-byte budgets, freshness and retained-error/abort behavior | Schema-5 implementation and local arithmetic/parser checks verified; actual measurements, successful preparation and in-window integration Pending |
| 4 / C1 execution environment | Dedicated environment input, acquisition authority, deployment, readiness and terminal preservation are specified | Selection/acquisition Pending; no VM changes authorized by this edit |
| 5 / C4 current versus historical findings | Implemented duration/grid, finish, fixture/hash and overlap corrections move to the historical table; active defects remain in the current table | Existing dated evidence preserved; new full-window acceptance Pending |

Private `work/soak-etl-pass-3bdf378c/journal-scenario-review-observations-20261001.json`
retains the actual first-review CA queries, installed collector hashes and
terminal/unit observations. Both units and observation timers were inactive;
both original terminal verdicts remain Incomplete.

###### Ordered Work

1. **Generalize and verify observation control.** Update
   `tests/archiver-soak/etl-pass/{prepare-retest,launch-retest,observe,verify-runtime,evaluate}.py`.
   Carry explicit duration and chain identity through preparation, capacity,
   verification, launch and the immutable manifest. Retain 7200-second support;
   select 86400 seconds for these runs. Version the expanded manifest/evaluator
   contract; replay historical observations with their original requirements
   and tools without counting them as the new full-window verification.
   Derive cadences from the verified deployed store configuration and reject
   a chain/configuration mismatch.
   Check the schedule against the pinned scheduler design, independently of
   the manifest's expected list: shortened uses 300/3600-second cadences;
   default uses 3600/28800 seconds; offsets are 300/600 seconds. Normally a
   24-hour half-open interval contains 288/24 and 24/3 scheduled firings.
   Compute identities from the manifest's half-open interval rather than
   forcing those counts; reconcile additional final-capture passes separately.
   Capture UTC and monotonic starts together after readiness checks; normal
   finish must wait for both complete durations without subtracting tolerance.
   Preserve boot identity, lifecycle locks, collision protection, abort
   distinction and refusal of repeated shutdown. The evaluator must separately
   validate duration, UTC midnight and each chain's schedule, so a wrong
   manifest or early finish cannot report Passed. Verify T13 using shipped
   code, the pinned design and retained real pass records.
   Define one complete bundle hash contract shared by preparation, verification,
   launch, the manifest and evaluation. Include every installed executable
   dependency and measurement configuration, including `prepare-retest.py`,
   `resource_helpers.py` and `heap.jfc`, as well as all currently hashed tools.
   Reject missing or unexpected bundle entries. Check the installed bundle
   against its frozen digests before accepting proofs or opening a manifest.
   Verify that changing either the real helper or JFR configuration invalidates
   old proofs, even when the nine currently hashed scripts are unchanged.
2. **Prepare measurement and report coverage.** Extend `collect.py`, `measure.py`
   and `evaluate.py` only where required for the missing evidence. Implement
   T27 preparation/proof validation through `contract.py`, `prepare-retest.py`,
   `verify-runtime.py` and `launch-retest.py`, and in-window/final enforcement
   through `collect.py`, `observe.py` and `evaluate.py`. Missing, stale,
   wrong-boot, wrong-policy or wrong-bundle proofs must refuse start;
   missing/failing runtime budgets must remain errors. These are planned
   additions for live deployment; the schema-5 local candidate implements the
   proof contract, while currently installed readiness proofs do not implement T27. Implement
   the existing-adjustment verification path in `apply-fixture.py` and verify
   repeated preparation/verification and conflicting-input rejection locally
   with the shipped tools and fixture before deploying either VM.
   Implement `tests/archiver-soak/etl-pass/aggregate.py` with the input/output
   contract below. Verify the numerical aggregation and overlap handling on
   retained real observations before freezing the tool bundle. Preserve raw
   event-rate metric names, component/source, values, units, observation times
   and the pinned implementation's averaging interval; distinguish engine
   arrival/write rate from IOC scan rate. Existing responses contain event-rate
   rows, but their semantics must be checked before comparison. Capture actual
   appliance/engine rates; exclude benchmark-writing rows from load statistics.
   Report sampled-rate means and coverage; use time-weighted means only for
   known nonoverlapping intervals and label any gaps. Capture per-component
   heap before/after GC, GC counts/causes/pauses, full jstat,
   sampled heap and RSS, plus complete application, health and kernel journal
   coverage from the manifest start through final capture. Empty kernel
   searches do not prove coverage. Detect cursor loss, suppressed records,
   missing periodic samples, JFR DataLoss and recording/rotation limits.
   Reconcile required metrics and GC evidence in the evaluator; required
   missing evidence prevents Passed. Add meaningful regressions to
   `test_retest.py`/`test_evidence.py`, run the actual shipped paths with only
   external boundaries substituted locally, and replay preserved real inputs.
   Keep original failures visible. Finish all tool implementation and required
   local verification, including `apply-fixture.py` and `aggregate.py`, before
   updating the tool README and SHA256SUMS and freezing the complete bundle
   digests. Include the aggregation tool and its executable dependencies in
   that contract. The following VM preparation, runtime checks and observations
   use these exact frozen sources. A later tool change requires a new verified
   bundle and fresh preparation proofs before an observation can start.
   For the journal amendment, first resolve the dedicated environment input
   and complete its preparation described below. Run local checks, freeze a
   candidate bundle and install that candidate only on the authorized test
   environment. Complete T22-T26 and T28's local/live checks against its exact
   digests before marking it the final replacement bundle. Any subsequent
   executable change invalidates those checks and requires a new candidate
   and re-execution. Preserve the currently deployed defective
   bundle and run the same T22 regression against it: a regression that never
   fails on its stale-kernel-anchor behavior cannot establish correction.
3. **Preserve and prepare both stopped deployments.** Check actual terminal
   completion and idle services/timers before archiving each prior observation
   and its tools in separate private directories. Preserve original fixture
   databases, registration CSV, previous failures and existing stores. Install
   the same frozen, verified measurement bundle on both VMs. Use the completed
   `apply-fixture.py --verify-existing` path on both shortened and default.
   Retain each existing override, drop-in and adjustment evidence; verify
   their digests and effective IOC command against the original three
   databases and approved override, then read all twenty actual MDEL/ADEL
   fields on each VM. Both adjustments were already observed on 2026-10-01.
   If either expected adjustment is absent, partial or conflicting, stop
   preparation and preserve that evidence. Do not select initial application
   or overwrite an existing adjustment as a fallback.
   Both paths require MDEL/ADEL = -1 on exactly the ten approved records.
   A missing, partial or conflicting existing adjustment prevents preparation;
   retain its evidence without replacing it. Keep PV names, policies, sampling
   settings and eight 1000-element waveforms unchanged. Require the local
   repeated-preparation and conflicting-input checks from step 2 before this
   VM operation. Preserve the original refusal of an unrequested replacement.
   Record env/Maven full commits, tool/fixture hashes, JVM/GC options, four
   256M heaps, actual vCPU/RAM/disk, same-VM MariaDB, CA source isolation,
   effective stores, initial store sizes/partition ages and stop timeout.
   Derive 24-hour data, application-log, journal, JFR and measurement growth
   from retained evidence plus current measured growth. Include capture
   allowance and recording limits; require projected usage below the actual
   85-percent health threshold and at least 2 GiB free. Shortened's 40-GiB and
   default's approved 48-GiB disks still
   require this check. Insufficient or unsupported projection prevents start;
   no data deletion or new capacity change is implied by this plan.
   T27's preparation portion additionally checks journal retention
   headroom independently of free disk space. Rate-limit prevention and
   retained-record coverage are separate
   checks; the approved 1us/10000 service settings do not prove retention.
4. **Execute fresh real runtime preparation on each VM.** Require T13/T14,
   completed T22-T26/T28 in their stated environments and a passing T27
   preparation result for each actual VM,
   then repeat hash-bound health, empty-data, early-finish and abort checks
   through the installed tools, real appliance, IOC, MariaDB and systemd.
   Preserve probe evidence separately from the trial. The empty-data check
   uses the real retrieval path with its clock boundary changed; label that
   boundary explicitly. Exercise the corrected collector during a genuine
   activating health invocation with a recent completed success; retain every
   actual completion and ensure a later success cannot erase a failure.
   Record each VM's actual health contract and cause/correction separately;
   do not copy the shortened VM's historical storage failure onto default.
   After the abort probe, restart and require two distinct accepted health
   completions and two successful full samples, four JVMs with real heap/pause
   events, synchronized clocks, all 903 PVs connected/archiving/recent, six
   visible probes and all twenty verified deadband fields. Old proofs with
   different hashes under the complete bundle contract cannot qualify.
   Recheck readiness age, current capacity
   and hashes immediately before opening each manifest. This verifies the
   current collector without another preliminary two-hour soak.
5. **Observe both chains in parallel.** Open separate manifests only after T15.
   Record independent starts, both clock deadlines, UTC-midnight crossing,
   chain-specific schedules, startup-pass records and metric baselines.
   Collect full samples every five minutes, explicit initial/final samples,
   every closed pass and complete journals. Preserve all-PV outcomes and six
   bounded visibility probes with two retrieval workers; record actual request
   counts/rates and concurrency, without adding the historical four-client
   stress workload. Confirm each planned pass once, five-second start timing
   including preceding-transition waits, ordering, zero normal-load overrun
   and job errors, and metric/counter agreement including startup passes.
   Track actual event rate, disk growth, OOM signatures, JVM/boot identities
   and per-component resources throughout. Preserve midnight samples and
   daily ETL/metric behavior, and
   execute T27's in-window portion at each five-minute collection and final
   capture; it is not a pre-launch dependency. Retain every budget or coverage
   failure even if a later sample succeeds.
   Record partitions/bytes moved; default hold-two
   day partitions can produce legitimate empty MTS-to-LTS passes. Existing
   eligible data must be identified by age; no fresh-data LTS coverage is
   inferred from pass counts.
6. **Finish once and evaluate the complete windows.** Only after both clocks
   reach 86400 seconds on a VM and UTC midnight has crossed, stop its timers,
   wait for active collection, retain the final full sample and four complete
   JFR recordings, then measure one whole-unit stop against actual
   `TimeoutStopSec`. Before stop, wait with a recorded bounded deadline for
   required in-window passes to close; a missing completion prevents Passed.
   Keep shutdown-aborted final-capture passes separate from normal-load checks.
   Capture current ETL work/pass state immediately before stop and remaining
   application/health/kernel journals after it. Report
   whether shutdown occurred idle or with work in progress; an idle stop does
   not establish behavior under a forced busy load. Retain orderly/forced
   signals, service result, actual elapsed time and final consolidation.
   Preserve the existing abort policy: two consecutive failed full samples or
   free space below 2 GiB request early abort; a single genuine health,
   collection or freshness failure already prevents Passed. Abort/missing
   required coverage is Incomplete with failures retained; completed windows
   with failed assertions are Failed. Successful stop alone cannot pass a run.
7. **Produce the comparison and transferable evidence.** Run the frozen
   `tests/archiver-soak/etl-pass/aggregate.py` on each completed observation.
   Its planned CLI accepts `--input` for a coherent evidence directory,
   `--output` for a JSON aggregate, and optional `--compare` for a reference
   JSON aggregate. It reads the manifest, terminal record, raw samples/metrics,
   pass records, heap/collection/pause CSVs, GC logs, jstat, RSS, retrieval and
   coverage evidence through paths relative to that input directory. It writes
   a deterministic, versioned JSON result with source/tool digests, units, event/sample counts,
   numerical statistics, failed assertions and missing/ambiguous coverage.
   Missing or malformed required inputs and comparison mismatches return
   nonzero; no private absolute path is an input requirement. Implement and
   locally verify this contract in step 2; step 7 executes the frozen tool.
   Filter all aggregates by the immutable manifest; deduplicate overlapping JFR data before counts
   and pause totals, preserving GC IDs, paired heap and incomplete records.
   Define event identity using component, JVM identity, event kind and GC ID,
   retaining the before/after marker for heap events and phase identity for
   pause events. For overlapping exports of the same event, require matching
   payload and a maximum timestamp span of two microseconds per duplicate
   cluster, measured with integer nanoseconds. Retain original timestamps and
   report the deduplication counts. Do not merge distinct pause events sharing
   a GC ID; conflicting heap-pair payloads, ambiguous event identity or
   unsupported timestamp variation prevent the corresponding aggregate from
   qualifying as complete. The step-2 regression uses retained real
   shortened/default JFR exports, reconciles GC counts with GC logs/jstat,
   and verifies that overlap leaves event counts and pause totals unchanged.
   Exact timestamp equality alone must fail that regression. Apply the same
   counter and coverage checks to the new completed observations.
   Report per transition last/mean/min/max busy time, planned and
   ordering-adjusted delays, overruns, pass/job counts, partitions/bytes moved
   and weekly usage with the pinned design's partial-day denominator. For
   each JVM report observed GC-event and sampled heap maxima, post-GC heap
   range/trend, young/full/concurrent counts and times, pause totals/maxima
   and sampled RSS maxima; retain units and event/sample counts. Report
   event-rate range/mean and averaging semantics, request latency/visibility
   bounds and all-PV freshness separately. Compare with original 24-hour,
   shortened two-hour and M14/T21 evidence using explicit fixture, event-rate,
   store-age, resource and retrieval-load differences. The old 0.69-second
   value is a lifetime average; compare matching metric meanings and periods,
   exclude the retired 277-second running sum and do not infer improvement
   from unmatched load. Missing prior event rates remain marked unmeasured.
   Update canonical T13-T21 results from actual executions and prepare
   sanitized machine-readable aggregates, pass/metric evidence, GC statistics,
   manifest/terminal/evaluator output, tool sources and checksums. Include the
   exact canonical document snapshot/checksum and carrying commit when one
   exists; explicitly identify uncommitted content. Preserve originals and
   record both original and sanitized package checksums. Use coherent portable
   evidence paths and retain all numerical values and failure/coverage fields.
   Package adjacent Python tools under `tools/`, coherent sanitized evidence
   under `runs/shortened/` and `runs/default/`, and reference JSON aggregates
   under `aggregates/shortened.json` and `aggregates/default.json`. Generate
   those reference aggregates from the sanitized inputs, retaining the original
   private aggregates and original/sanitized digest mapping separately. The
   package README names required runtimes, evaluator invocation and both
   aggregation commands. From the package root, create `regenerated/` and run
   the planned aggregation interface:

   ```bash
   python3 tools/aggregate.py --input=runs/shortened --output=regenerated/shortened.json --compare=aggregates/shortened.json
   python3 tools/aggregate.py --input=runs/default --output=regenerated/default.json --compare=aggregates/default.json
   ```

   T21 must replay the shipped evaluator and both aggregation commands using
   only this package. Compare parsed JSON values independently of object-key
   order: counts, integer timestamps, digests, failure/coverage fields and
   statistics at their declared output precision must match exactly. A
   nonzero command or any mismatch prevents T21 from passing. The recipient
   must also locate every cited test row without access to this host's private
   work directory. Commit/push and external
   delivery require their own authorization. Overall M22 acceptance requires
   both full-window results and T6; retain all earlier results separately.

###### Previous Accepted Observation Plans

- Plan Status: accepted
- Plan Acceptance: 2026-09-28; the owner selected the existing 903-PV fixture for both chains and directed execution, then accepted the correction for passes waiting on the preceding transition.
- Implementation Authorization: 2026-09-28; deploy both selected inventories, verify readiness, run both observation windows and measure whole-unit shutdown; apply the accepted timing correction to the ongoing observations.
- Measurement extension accepted and authorized: 2026-09-28. Record JFR
  `GCHeapSummary`, `GarbageCollection`, and `GCPhasePause` events for all four
  JVMs, retain GC logs and complete jstat counters, and add timed retrieval
  probes. Preserve the superseded observation before the appliance restart.
  Preserve the existing PV rates, heaps, source pins and stores; the restarted
  run therefore begins with existing archived data. Per-GC maxima are observed
  event maxima, not continuous heap high-water marks. All-PV freshness and
  representative first-visibility bounds must remain distinct from exact
  engine ingestion latency. Do not induce full GC to create a measurement.
- Superseded Plan Artifacts: none

1. Keep each inventory separate and use the fixed 903-PV fixture on both VMs.
   Record the complete runtime configuration and check actual storage headroom
   again after deployment. G4 records the initial capacity assessment.
2. Apply `make archiver_dev.rocky8` separately to each inventory, passing
   `work/soak-etl-pass-3bdf378c/common.yml` plus `shortened.yml` or `default.yml`.
   Keep a separate deployment log for each VM. Verify the installed source
   commits, stamp, four running instances, database, health and clock sync.
   Identify whether the deployed `archappl.properties` comes from the source
   default site or the epicsarchiverap-env template, and record effective ETL
   properties without exposing database credentials.
3. Adapt the existing sampler for journald and a configurable PV fixture. Keep
   raw pass logs and raw metrics responses. Enable DEBUG only for
   `org.epics.archiverappliance.etl.common.ETLPassDriver` through the mgmt
   `setLogLevel` BPL. Report missing samples as collection failures.
4. Start the real fixture IOCs and register the exact lists. Scope each
   appliance's Channel Access discovery to its intended fixture IOC and check
   the connection endpoints, so duplicate PV names on the parallel VM cannot
   select the wrong source. Verify a real completed-pass log and matching
   metrics on each appliance. Define each observation start only after every
   expected PV is archiving, clocks are synchronized, and collection works.
   Collect host and per-process resources, service state and store state every
   five minutes, and ETL metrics at least hourly. Retain every pass record
   throughout the two parallel windows.
5. After each window, capture final metrics and time one whole-unit stop. Save
   the service result and journal, including consolidation and any signals.
   Keep the shutdown-aborted pass separate from normal-load overrun checks.
6. Record T1-T6 from actual executions. Prepare the scheduler comparison and
   whole-unit stop measurements for the two upstream projects. Any external
   message or issue update follows its own authorization.
7. Before restarting, stage and verify the additional measurement tools on
   the real appliances. Record GC before/after heap, GC cause and pause
   durations, and preserve raw JFR and GC logs. Extend jstat evidence with
   generation occupancy and separate young/full/concurrent collection times.
8. Record retrieval duration and newest archived source timestamp for all 903
   PVs every five minutes. On representative scalar, fast, slow and waveform
   PVs, record bounded polling of a real source timestamp until it becomes
   retrievable. Preserve polling bounds, timestamp precision and timeouts;
   do not label sample age or a polling upper bound as exact ingestion delay.
9. Stop the old observation timers, preserve its evidence under a separate
   private directory, and restart the appliance with the added JVM settings.
   Verify real GC events, latency results, four JVMs and 903 connected,
   archiving PVs before opening the replacement 24-hour observation. Schedule
   the measured whole-unit stop against that replacement manifest.
   Preserve DEBUG pass records across restart through a copy of the installed
   log4j2 configuration with only the ETLPassDriver logger changed. Bound GC
   log files to 16 MiB with three archives per JVM, and JFR to 64 MiB per JVM
   for 26 hours. Keep ten-minute JFR snapshots at five-minute collection
   intervals with an 8 MiB dump limit, a 512 MiB snapshot archive limit and a
   2 GiB free-space check; collection-limit failures remain visible.

###### Focused Two-Hour Retest

- Plan Status: accepted
- Plan Acceptance: 2026-09-29; the owner approved the two-hour shortened-chain
  retest with all accepted review findings reflected below.
- Implementation Authorization: 2026-09-29; implement and verify the approved
  preparation, measurement, two-hour observation and terminal paths. The
  observation remains conditional on the documented start prerequisites.
- Fixture Amendment Acceptance And Authorization: 2026-09-29; retain the
  all-903-PV 30-second freshness criterion and change the ten deadband records'
  MDEL and ADEL to -1 through a separate `retest-deadband.db` override. Preserve
  the original databases and registration CSV, PV names, calculation inputs,
  one-second scans, methods, periods and policies. Verify the actual twenty
  fields before readiness and during full samples. This variant is separate
  from the original 24-hour fixture and its evidence.
- Start-Time Amendment Acceptance And Authorization: 2026-09-30; start
  immediately after actual readiness instead of waiting for HH:54:30 UTC.
  Cancel the previous launch timer, retain the 7200-second duration and
  calculate expected firings and finish from the actual manifest boundaries.
- Scope: verify health reporting, measurement collection, ETL ordering and
  final collection followed by whole-unit shutdown on the shortened VM.
  Retain env `d09dca7`, Maven `3bdf378c`, all 903 PVs and their original
  rates, 256 MiB heaps, local MariaDB and existing archived data. Apply only the
  accepted ten-record deadband override in the focused retest.
- Existing T4-T8 evidence and the original 24-hour completion criteria remain
  applicable. A two-hour result does not establish absence of a late health
  failure, full-window GC coverage or default-chain behavior.

1. Inspect the shortened VM's actual health unit, command, accepted exit
   statuses and bounded journal around the failed samples. Distinguish a
   genuine command failure from a collector interpretation error. The check
   in `tests/archiver-soak/etl-pass/collect.py` currently requires exit 0;
   verify the installed unit's contract before proposing a change. Count
   failed sample observations separately from failed health invocations.
   Document the cause of the prior genuine health failures, the corrective
   action and its verification through the actual health command and
   collector. An explanation or a single successful readiness sample does
   not close this prerequisite. Do not open the retest while the cause,
   corrective action or executed verification remains unresolved. Preserve
   the verification inputs, tool identity, invocation results and timestamps.
   Extend collection to preserve the health unit's journal for the entire
   retest, with a separate cursor and invocation identities, exit statuses,
   results and timestamps. Include the interval between the last full sample
   and appliance shutdown. Detect journal gaps or suppressed records and
   report incomplete health coverage. Validate every retained invocation
   against the installed command and accepted exit-status contract; checking
   the unit state once every five minutes is insufficient.
2. Prepare the necessary changes to `measure.py`, `collect.py` and `observe.py` under
   `tests/archiver-soak/etl-pass/`. Support an explicit 7200-second window
   while retaining the 24-hour default and manifest replacement safeguards.
   Preserve a distinct reference to the final full sample when the later
   journal-only sample updates `latest.json`. Retain real nonzero failures.
   Verify the installed finish path, including full JFR checkpoints and
   shutdown evidence. Add an explicit early-abort path to `observe.py` that
   can terminate a retest before its scheduled finish without weakening the
   normal finish guard. Verify both finish and abort through the actual tools,
   including failure evidence and collision safeguards. Review the concrete
   changes before deployment.
   Treat `no_sample_in_window` as a failed freshness check and retain it
   separately from HTTP request errors. Require all 903 fixture PVs to have
   recent archived samples in each 30-second query window. Verify the real
   freshness, collector and readiness paths with the shipped fixture,
   including an HTTP 200 response containing no data. A function-level check
   with only the HTTP transport substituted is local validation; VM acceptance
   still requires the actual appliance, IOC, database and systemd paths.
3. Preserve the completed observation and its tools privately before opening
   a separate retest. `restart-observation.py` refuses schema-2 or finished
   observations and is not a rerun entry point. Prepare a start procedure for
   the completed appliance state with collision checks and preserved stores.
   Check current access, service state, source pins, instruments and disk
   capacity. Require projected data and measurement growth for two hours to
   leave at least 2 GiB free; resolve insufficient capacity before starting.
4. Open the 7200-second manifest only after a successful full readiness sample
   with four JVMs, synchronized time and all 903 PVs connected and archiving.
   Require the completed health-correction verification from step 1, zero
   full-sample errors, 903 PVs with recent archived data and six successful
   visibility probes before opening the manifest.
   Apply the accepted immediate-start amendment after readiness. The original
   HH:54:30 UTC target is superseded. Record the actual start and finish;
   normal completion requires
   the manifest duration to elapse. Compute the expected planned firings in
   the half-open interval [manifest start, manifest finish): transition 0 has
   cadence 300 seconds and offset 300 seconds; transition 1 has cadence 3600
   seconds and offset 600 seconds, relative to the epoch. A normal two-hour
   window contains 24 STS-to-MTS and two MTS-to-LTS scheduled firings. Match
   every expected (transition, cadence, plannedAt) to one completed pass after
   journal-cursor deduplication. Report missing, duplicate and unexpected
   firings and reconcile counters against the pre-window baseline, including
   startup passes where the counters include them. Exclude startup passes
   from grid checks and require both scheduled MTS-to-LTS passes to complete.
5. Collect every five minutes, including explicit initial and final full
   samples, and preserve every closed pass and metrics response. Record
   per-component GC heap, causes, pauses, jstat counters and RSS, all-PV
   freshness and six representative visibility probes. Deduplicate JFR events.
   Require `pvs_with_recent_samples=903` in every full sample, including the
   readiness and final samples. Preserve the per-PV outcomes privately and
   report missing-data counts separately from HTTP error counts. Zero HTTP
   errors and six visible representatives do not establish all-PV freshness.
   Report incomplete GC pairs; induce no GC. Compare pass counts and metric
   values, verify five-second timing and ordering, and report OOM, PID changes,
   collection failures and disk headroom. Request early abort after two
   consecutive failed full samples or immediately when available space falls
   below 2 GiB. Record the triggering sample, reason and actual elapsed time.
   Stop both sample and finish timers, wait for an active sampler with a
   bounded deadline, and record any timeout. Preserve available final
   evidence; attempt JFR checkpoints only while the reserve check succeeds,
   recording any skipped or failed capture. Measure and record the appliance
   stop and collect the remaining appliance and health journals. Write a
   distinct terminal abort record and classify the shortened observation as
   Incomplete while retaining each failed assertion. Prevent a later normal
   finish from repeating shutdown or reporting that aborted run as Passed.
   Any genuine health invocation failure or full-sample collection/freshness
   error, even once and even if explained or later recovered, prevents Passed.
   Evaluate health success against the installed accepted exit-status contract;
   an accepted nonzero status is not itself a failure. Two consecutive failed
   full samples control early abort only; that threshold does not permit one
   failure in a passing observation.
6. Preserve final full-sample and complete JFR results, measure whole-unit
   shutdown against the actual timeout, then collect the remaining journal.
   Require an active appliance before the stop, successful collection and
   shutdown, and no forced termination. Record this retest separately from
   the original T4-T8 results and continue analyzing the preserved 24-hour
   observations before an overall verdict.
   A completed observation with any failed assertion is Failed. An aborted
   observation or missing required coverage is Incomplete, with failed
   assertions retained. Passed requires every planned assertion, including
   zero full-sample errors, all-PV freshness and complete health coverage, to
   succeed throughout the manifest window and the required final collection.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Configuration | Use `ansible-inventory` to load each pair of runtime YAML files and run `ansible-playbook --syntax-check` on the shipped `archiver_dev` species with those files | Control host, static inventory only | Exact approved extra variables; socket MariaDB and 256M heap; shortened store values on one run and empty store overrides on the other; playbook syntax valid. Host-specific resolution remains T2 |
| T2 | Deployment | Apply the shipped species, then inspect the installed commits, stamp, policies, effective properties, four instances, database, health and clock; verify fixture connection endpoints after registration | Both VMs | Configurations match their recorded inputs, each appliance connects to its intended IOC sources, and both are ready |
| T3 | Collection | Run the sampler against each real appliance and compare its outputs with a completed-pass journal record and the live metrics response | Both VMs | Real pass evidence, metric fields, resource samples and UTC timestamps are preserved; failures remain visible |
| T4 | Soak | Observe each real PV population for at least 24 hours across UTC midnight; evaluate every retained pass and hourly metric snapshot. Check start delay from `plannedAt`; when the preceding transition held a pass, also check its start against that transition's `endedAt` and the next tick | Both VMs | Normal passes with no preceding-transition wait start within one 5-second tick of their planned time; held passes start at the first tick after the preceding transition ends and retain their original `plannedAt`. Passes do not overrun, and counters and metrics agree with the records; outages or data gaps are reported |
| T5 | Shutdown | Capture final metrics and time one whole-unit stop on each VM, preserving the unit result and journal | Both VMs after T4 | Successful orderly stops inside the actual timeout, without forced termination; elapsed times and effective wait settings recorded |
| T6 | Comparison | Compare new busy time and weekly usage with the shipped M14/T21 evidence, accounting for population and load differences | Control host | A reproducible comparison with the retired running-sum metric excluded and the default-chain LTS limitation stated |
| T7 | GC evidence | Read actual per-component JFR events and GC logs, correlate GC IDs and compare collected counters with the real JVM | Both VMs | Before/after heap and individual pauses are recorded for every observed GC; causes, PID, timestamps and incomplete records remain visible; no forced GC |
| T8 | Latency evidence | Query all fixture PVs through the real retrieval service and poll representative real CA timestamps until visible | Both VMs | All-PV freshness, request duration and representative visibility bounds are recorded separately, with errors and polling resolution preserved |
| T9 | Retest preparation | Resolve and verify the prior health failures through the actual command and collector; verify complete health-journal collection, empty-data rejection, normal finish and early-abort paths, evidence preservation and capacity | Control host and shortened VM | Cause, correction and executed verification recorded before retest; empty HTTP 200 data cannot satisfy freshness/readiness; both terminal paths preserve errors and prevent repeated shutdown; completed observations protected; projected free space at least 2 GiB |
| T10 | Retest readiness | Require T9 and successful full readiness samples before opening a separate manifest; the accepted immediate-start amendment supersedes HH:54:30 UTC | Shortened VM, accepted ten-record deadband variant of the original 903-PV fixture | Verified health correction, four JVMs, synchronized clock, 903 connected and archiving PVs with recent data, six visible probes, real GC evidence and zero sample errors; exact 7200-second boundary, expected schedule and counter baseline recorded |
| T11 | Focused soak | Observe the real fixture for 7200 seconds with five-minute collection, complete appliance and health journals, and pass-to-schedule and metrics comparisons | Shortened VM | Every expected firing has exactly one completed pass, normally 24 STS-to-MTS and two MTS-to-LTS; correct ordering and timing; counters and metrics agree; all 903 PVs have recent data in every full sample; zero genuine health failures or sample errors, no coverage gaps, OOM, JVM restart or normal-load overrun; any failure prevents Passed |
| T12 | Retest finish | Preserve the final full sample and complete JFR checkpoint, measure the whole-unit stop and collect both final journals; use the distinct abort path if a stop condition occurs early | Shortened VM after T11 or an early-abort trigger | Normal finish requires successful final collection and an active appliance stopping inside its timeout without forced termination; early abort preserves its cause, capture failures and stop result, records Incomplete, and cancels the scheduled finish |
| T13 | Observation control | Run shipped preparation/launcher/observer/evaluator paths with external clock/filesystem/command boundaries; check both grids against the pinned design and retained real pass records; reject shortened/default mismatch, early UTC/monotonic finish, absent midnight, stale hash proofs and repeated stop; change the actual helper/JFR configuration separately and require old-proof rejection | Control host; retained real observations and original tools | Explicit 86400-second duration is consistent throughout; shortened and default schedules are independently correct; complete bundle hashes include executable dependencies and JFR configuration, with missing/unexpected entries rejected; invalid duration/grid/coverage or a changed dependency cannot yield Passed; legacy two-hour verdicts remain separately reproducible |
| T14 | Preparation and load | First complete local shipped-tool/fixture repeated-preparation and conflicting-input checks, then freeze and install the bundle; preserve completed observations; verify existing adjustments on both VMs through --verify-existing; verify source pins, equal fixture/override, CA isolation, 256M heaps, MariaDB, real resources/store ages and measured 24-hour capacity projection | Both stopped/restarted VMs; local checks before bundle freeze and deployment | Implementation and local checks precede hash freeze; installed tools match the frozen bundle; both existing adjustments and original databases remain intact; absent/mismatched/partial adjustments are rejected without initial-application fallback; all 903 names/settings and twenty actual deadband fields match; actual disks are 40 GiB on shortened and 48 GiB on default; data and measurement growth leave at least 2 GiB and usage below the installed health limit; original data and evidence preserved |
| T15 | Current-tool runtime readiness | Require T27 preparation evidence (`M25` / T6) for the replacement bundle; install identical complete bundle hashes, including preparation, executable helpers and JFR configuration; execute real health, empty-data rejection, early-finish rejection and abort probe; exercise collector during a real activating health invocation; restart and obtain two successful health completions and two full samples | Both real appliances, IOC fixtures, MariaDB and systemd | Current proofs bind to the complete installed bundle and frozen digests; no failed/missing/stale health completion hidden; four real GC components, synchronized clock, all 903 PVs connected/archiving/recent, six visible probes and zero full-sample errors; no manifest before readiness or while pre-launch journal checks remain unverified; T27 in-window completion is deferred to T16/T19 |
| T16 | Full-window soak | Run both actual store chains in parallel for at least 86400 seconds in both clocks across UTC midnight; collect every five minutes plus initial/final samples and complete journals | Both VMs after T15 | Each VM independently meets duration/midnight, freshness, identity and coverage criteria; zero genuine health/sample failures, OOM or JVM restart; abort is Incomplete with failures retained |
| T17 | Scheduler and load metrics | Evaluate every expected pass and raw metric snapshot against the verified chain grid and pinned metric definitions; aggregate actual event rates and retrieval workload | Both completed observations | Exactly one completion per expected identity, no normal overrun/job errors; start within five seconds of planned/ordering-ready time; counters, busy time and weekly usage reconcile; numerical results, rate semantics, intervals and units available |
| T18 | Memory and GC | Parse real JFR recordings, heap/collection/pause CSVs, GC logs, jstat and RSS; use the specified event identity, matching payload and bounded two-microsecond timestamp clusters; exercise aggregation on retained real overlapping exports, preserve distinct pauses and reject conflicts/ambiguity; check recording/rotation coverage and counter agreement | All eight actual JVMs; retained real shortened/default exports for aggregation regression | Overlap does not inflate counts or pause totals, and exact-timestamp-only deduplication fails the regression; original timestamps and duplicate counts remain available; complete window evidence without DataLoss, missing pairs or unresolved conflicts; per-component observed heap/post-GC heap, GC counts/times, pause totals/maxima and RSS reported with counts/units; no continuous-max or heap-sizing claim |
| T19 | Normal terminal path | After both duration checks and in-window completion, capture final full sample/four complete JFRs; record ETL work state, time one unit stop, capture remaining journals and replay evaluator | Each VM after T16, or separate abort path | Successful final collection and orderly stop inside actual timeout; idle/in-progress state and elapsed time retained; no repeated stop; stop success cannot hide failed assertions or missing coverage |
| T20 | Earlier-result comparison | Complete T6 using M14/T21, original 24-hour, focused two-hour and new full-window inputs; reconcile last/average busy time and weekly usage meanings and intervals | Control host; preserved real evidence | Reproducible numerical comparison with fixture/event-rate, store-age, resource and retrieval-load differences stated; old unmeasured event rates identified; retired running sum excluded; no unsupported improvement claim |
| T21 | Recipient evidence | Build the specified sanitized package with tools, per-chain replay inputs, reference aggregates, canonical snapshot and checksums; replay the shipped evaluator and both documented aggregate.py commands solely from that package; compare regenerated JSON values and check every cited row | Control host; recipient-equivalent package paths | Both commands return zero and regenerated counts, timestamps, digests, numerical values at declared precision and failure/coverage fields match their reference aggregates exactly; per-chain verdicts and numerical evidence are reproducible without private host access; checksums resolve exact plan/results/tool versions; uncommitted content identified; no secrets or private endpoint identifiers; sending remains separately authorized |

The journal checks T22-T28 moved to `M25` on 2026-10-05 (`D22`) as its T1-T7
and are no longer checks of this row; M22 keeps T1-T21. The procedure
sections below are the accepted history of those checks and are owned by
`M25`.

###### Journal Scenario Procedure And Start Gate

T22-T28 are planned checks, not executed verification. Their results remain
pending until the named shipped paths run and their artifacts are inspected.
The scenarios specify required behavior without selecting between a collector
correction, retention-capacity adjustment or both. Any implementation choice
or capacity change remains a separate owner decision.

###### Dedicated Journal Test Environment

Resolve the environment before live scenario execution. Record the selected
inventory, environment owner and explicit execution authority in private
`work/soak-etl-pass-3bdf378c/journal-test-environment.json`; none is supplied
by G4 or created by this plan edit. If any input is missing, keep live
T22-T26/T28 Pending and do not proceed to deployment or observation launch.

Prepare the selected environment through the shipped archiver_dev species on
Rocky 8.10/systemd 239 with the same full source commits, local MariaDB,
four 256M heaps, original 903-PV fixture and approved deadband override.
Record actual CPU/RAM/disk, isolated CA endpoints and a measured space budget
for the declared scenario duration, raw journal reference copies, GC/JFR and
final capture. Require projected usage below 85 percent and at least 2 GiB
free. Any acquisition or resource-size choice remains an owner decision.

Install the candidate bundle and record its complete digests. Require actual
source/configuration checks, twenty deadband values of -1, 903 connected and
archiving PVs, two accepted health completions and two successful full samples
before destructive probes. Each probe uses a separate evidence directory and
records its boot, boundaries and expected negative outcome. Keep the retained
soak inventories and stores separate. After live scenarios, stop test timers
and the test appliance through the shipped terminal path and preserve the
probe evidence; VM deletion and data removal are not part of this amendment.

###### Journal Scenario Procedure

1. Preserve the two terminal observations, their original bundle, manifests,
   collection state, raw journals, errors and abort records before any new
   preparation. Run destructive rotation/retention scenarios only on a
   dedicated test deployment or disposable copies of its genuine journal
   files. Do not vacuum either retained soak VM's journal, remove its evidence,
   change its clock or force an OOM. No new VM is provisioned by this document
   update. Record the environment, systemd/Python versions and exact tool
   digests for every execution.
2. Produce inputs through the actual journald and kernel logging paths.
   Record independently emitted marker identities, their actual journal
   cursors/timestamps and the journal-file inventory before and after each
   operation. Use actual rotation and verify that the intended old cursor
   is absent and required interval records are retained or deliberately lost.
   File removal occurs only in the disposable test data; preserve a complete
   reference copy for independent comparison. A scenario whose intended
   retention state was not observed is inconclusive, not passed.
3. Exercise `collect.py::sample` and its shipped kernel/application/health
   collection and state persistence, followed by the shipped observer and
   evaluator where required. Local replay may substitute only the external
   journal transport, filesystem or clock to select actual captured inputs.
   It must not replace an internal collector function, synthesize journal
   JSON, hand-build sample/terminal evidence or reconstruct the fixture.
   T24 and T28 additionally require the live paths; local replay alone cannot
   satisfy their integration portions. The frozen defective collector must
   fail the same obsolete-anchor regression used for the candidate.
4. Inspect system-journal coverage separately from user journals and separately
   for application, health and kernel streams. Retain collection boundaries,
   boot identity, continuity evidence, raw query exit status, returned cursor
   identities and durable archive/checkpoint evidence. An empty kernel query,
   successful journalctl exit, arbitrary replacement cursor or one old
   unfiltered record is insufficient proof. Required records already archived
   do not need indefinite source retention; every not-yet-collected interval
   must still have independently checkable coverage.
5. T24 verifies benign kernel-event delivery, not OOM detection. Replay actual
   retained OOM evidence through the shipped detection path before making an
   OOM-detection claim; if suitable real records are unavailable, report that
   portion as unverified. Preserve real suppression and missing-record inputs
   as negative cases; neither a changed cursor nor a later success may erase
   them. Unresolved coverage remains Incomplete with failures retained.
6. Retention planning must record its measured growth rate, interval, effective
   byte/time caps, archived-file granularity and allowance for query/capture
   delay. Account for system and user journals sharing the cap. Prove that the
   oldest still-required source boundary survives the declared maximum gap;
   do not infer this from the 24-hour disk-growth calculation or the nominal
   MaxRetentionSec alone. Actual in-window continuity remains required even
   after the preparation estimate passes.
7. Require T27 preparation (`M25` / T6) and existing T13-T15 before opening
   another manifest; the live scenarios formerly named T22-T26/T28 belong to
   `M25` and no longer gate an observation. T27 in-window checks run during T16 and must complete
   through T19 before final acceptance. Keep
   negative scenario failures in separate probe evidence; an expected rejection
   passes its negative check, but never makes a failed probe an accepted soak.
   Any executable change requires local regression, updated frozen bundle
   hashes and newly generated runtime proofs on each actual VM. Then obtain
   two distinct accepted health completions and two zero-error full samples
   per VM and recheck source/fixture identity and capacity immediately before
   launch. Retain the original two-independent-window requirement: at least
   86400 seconds in UTC and monotonic time, UTC midnight, measured shutdown
   and T6/T20/T21. These short scenarios cannot replace either 24-hour trial.

###### Journal Retention Calculation And Failure Handling (T27)

Measure at least six consecutive five-minute intervals under the approved
903-PV load and current logging policy. For system and user journals, retain
separate physical byte-write/allocation bounds, file inventories and rotation
or vacuum evidence. A flat disk-usage total at a cap is not a zero write rate.
Intervals with unaccounted removed files, reset counters or missing accounting
cannot supply a bound. Use the highest measured rate per stream, also taking
the maximum with any applicable retained higher rate under the same policy.
Record the source intervals, units, file digests and accounting method.

Use these definitions and inequalities, rounding byte quantities upward:

```text
P = evaluator sample-gap limit in seconds
A = effective sample-service TimeoutStartSec in seconds
T = max(effective finish-service TimeoutStartSec,
        effective abort-service TimeoutStartSec) in seconds
G_periodic = P + A
G_terminal = P + T
G_required = max(G_periodic, G_terminal)
S = 2
H = S * G_required
R_system = peak measured system-journal physical bytes per second
R_user = peak measured user-journal physical bytes per second
F_system = max(effective system journal file-size limit,
               largest observed system journal file) in bytes
F_user = max(effective user journal file-size limit,
             largest observed user journal file) in bytes
U = current retained user-journal bytes
B_system = ceil(R_system * H) + 2 * F_system
B_user = U + ceil(R_user * H) + 2 * F_user
B_required = B_system + B_user
B_required <= C_effective
H <= effective finite retention time limit, when applicable
```

`C_effective` is the usable combined journal byte cap after resolving the
actual SystemMaxUse and filesystem free-space restrictions, including
SystemKeepFree and other journal consumers. Unresolved effective defaults,
limits or accounting refuse preparation; do not assume a larger cap.
Current source values specify P=320 seconds, A=240 seconds and T=2700 seconds,
so G_periodic=560, G_terminal=3020 and H=6040 seconds. These are conservative
budget bounds, not permission to miss a 320-second full-sample requirement.
Read installed limits before each calculation; unbounded timeouts refuse
preparation. A changed limit or tool invalidates the previous proof.

Before launch, require successful byte/time inequalities, unchanged measured
policy, current caps and a result checked within 120 seconds. Keep the
existing capacity-input freshness and 24-hour disk-growth checks in T14.
Preserve raw inputs and the result privately under
`work/soak-etl-pass-3bdf378c/journal-retention/` and bind the proof to the actual
boot, bundle, logging policy and measurement interval. T15 requires only this
preparation portion; a future in-window result cannot authorize launch.

During T16 and final capture, record the actual elapsed collection gap,
oldest uncollected boundary, caps, stream rates and archive continuity.
Use at least the preparation rate bounds; a higher observed rate raises the
budget immediately. Missing input, an inequality failure or a gap beyond the
declared bound produces a retained `journal_retention_budget` sample error;
actual missing records are additionally reported as a coverage gap. A single
error prevents Passed, two consecutive failed full samples invoke the existing
abort policy, and the 2-GiB reserve rule remains unchanged. Final capture
retains the budget result or its failure even after an orderly stop. Complete
the in-window portion only when every required check and terminal coverage
has been evaluated; do not relabel either aborted historical run as Passed.

##### Verification Results

Rows labelled T22-T28, and rows named for T27, T13 or T15 that concern the
journal, were recorded in this row before the split of 2026-10-05; they remain
here as the record of that period. In `M25` the labels read T22 = T1,
T23 = T2, T24 = T3, T25 = T4, T26 = T5, T27 = T6 and T28 = T7.

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-09-28 19:19:10 UTC | Control host, working tree on `3060a7f` | Passed | The real `ansible-inventory --host localhost` loaded `common.yml` with each store file and returned the approved ten extra-variable values; the real `ansible-playbook --syntax-check` accepted `playbooks/species/archiver_dev.yml` with both file pairs. Only the static inventory was used; no target host was contacted. The existing PV lists contain 100, 400 and 403 entries, with 903 in `pvs-all.csv`, and all three IOC database files exist |
| T2 | 2026-09-28 21:34:54 UTC | Both Rocky 8.10 VMs; full archiver-dev species from `b8823c1` with recorded runtime variables | Passed | Each actual deployment returned rc=0, with 33 successful tasks and no failed or unreachable host. Installed commits are env `d09dca7a604840bc3f8dcd9edd7a7434fdf6992e` and Maven `3bdf378cb0a5eba42ad73648ec9e2c76b898bc1e`; stamps and rendered policies match the two approved chains. Four JVMs each use 256M minimum and maximum heaps. Socket MariaDB, health checks and KVM PTP synchronization succeed; `TimeoutStopSec` is 300 seconds. Post-installation free space was 13.69 GiB on each VM; at readiness 13.63/13.62 GiB remained. All 903 PVs are connected and archiving with the original sampling methods and periods, all 903 have STS files, and registration queues are empty. Both IOC listeners and all engine CA connections use loopback. The generated properties match the env site template copied into the Maven ALS site, SHA256 `5b91d9fca81adc7f25f82e75c6bd02e823de7b1acf496a33c215e1ab868f8bba`; no ETL worker or wait override is present, so the deployed source uses one worker per transition and a 60-second wait at each shutdown wait stage |
| T3 | 2026-09-28 21:36:09 UTC | Both real appliances and the original 903-PV fixture | Passed | The real collector returned rc=0 on both VMs at 21:34:53/54 UTC, preserving journal cursors, raw pass records, raw metrics, process resources, services, database counts, stores and UTC timestamps. Each startup transition processed 903 PVs with zero failed, aborted or skipped jobs and no overrun. Actual record-to-metric assertions matched completed-pass counts, PV counts, job and movement counters, last busy time and average busy time at the metrics' display precision: shortened 76/4 ms and default 41/13 ms for transitions 0/1. These startup passes moved no partitions. Pre-readiness samples that ran while PVs were still being assigned returned failure and were retained. The actual systemd unit validation returned rc=0; the 24-hour shutdown path is configured and remains unverified until T5 |
| T4 | 2026-09-29 01:07:59 UTC | Both VMs, unchanged source pins and 903-PV fixture; existing stores preserved | In progress | Replacement shortened start: 2026-09-29 01:06:22.691862 UTC; default start: 01:06:25.999358 UTC. Both schema-2 manifests retain readiness, fixture hash, boot ID, monotonic start and all four JVM PID/start identities. Both timers are active. The first automatic samples at 01:06:22.859989/26.185274 UTC completed with no collection errors, all 903 PVs connected and archiving, real GC events and six successful visibility probes; each run has three new closed-pass records. Free space is 12.37/12.36 GiB. Neither new 24-hour window has elapsed |
| T5 | Scheduled for 2026-09-30 01:06:22.691862/25.999358 UTC | Both VMs | Pending | Each finish timer invokes final collection, preserves a full bounded JFR recording, measures one stop of the whole appliance unit and records the service result plus the remaining journal. The actual timeout is 300 seconds. The previous finish schedule was replaced. A scheduled timer does not establish shutdown success |
| T6 | Not run | Control host | Pending | Requires new measurement evidence |
| T7 | 2026-09-29 01:07:59 UTC | Both real appliances; all eight JVMs | Passed | The actual collector preserved JFR, GC logs, complete jstat fields and per-process RSS. Unique before/after GC pairs for mgmt/engine/etl/retrieval are 26/48/26/56 on shortened and 26/48/25/51 on default; none is unpaired, and every captured heap-event GC ID occurs in that JVM's GC log. Stored jstat fields equal the actual raw jstat output. Each component has real pause and collection events, unchanged 256M heaps and a PID matching its new manifest; full-GC counters are zero. No forced GC was requested. Evidence: local `measurement-start-shortened.json` and `measurement-start-default.json` under the work directory, plus the raw JFR and logs on each VM. This verifies initial collection; deduplicated full-window coverage remains T4 |
| T8 | 2026-09-29 01:07:59 UTC | Both real retrieval services and original CA fixture | Passed | The first automatic samples queried all 903 PVs with two concurrent workers: 903 recent samples and zero request errors on each VM. Maximum request durations were 54.104/49.466 ms. All six representative CA timestamps were retrieved on each VM; source timestamp precision, poll attempts and visibility bounds are retained separately. In these samples all probes were visible on the first request, so lower bounds are zero and upper bounds include source sample age. These are not exact engine ingestion delays. Evidence: each sample's `freshness.json`, `visibility.json`, and `latency.csv`; full-window coverage remains T4 |

Interim verification on 2026-09-29 supplements the initial rows above:

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T2 | 2026-09-29 08:29:56-08:30:29 UTC | Default VM; online disk, partition and XFS expansion | Passed | `virsh blockresize` increased the attached disk from 21474836480 to 42949672960 bytes. A `growpart -N` check preceded `growpart /dev/vda 5`; partition 5 retained start sector 2265088 and grew from 39677919 to 81620959 sectors. Partitions 1-4 were unchanged. `xfs_growfs /` increased data blocks from 4959739 to 10202619. The 08:29:56 UTC check matched the boot ID and all four JVM PID/start identities to the observation manifest; the live API reported 903 connected and archiving PVs. The automatic 08:30:00.176110 UTC sample had no collection or retrieval errors, six visible probes, all four GC components and 28.537 GiB free. The original finish timer remains 2026-09-30 01:06:25.999358 UTC. This verifies the capacity intervention, not a repeat deployment or final soak acceptance |
| T4 | 2026-09-29 08:21:36-08:33:41 UTC | Both observations; default disk expanded during the window | In progress | At 08:21 UTC each VM had 88 full samples with zero collection failures and a maximum sample gap of 300 seconds; boot and all four JVM identities matched the manifests. The bounded appliance and kernel journal error searches at 08:22 UTC returned no OOM, killed-process or failed-unit matches. At 08:33 UTC, journal-cursor deduplication and parsing of `passes.jsonl` found 96 closed in-window passes on shortened (88 STS-to-MTS, 8 MTS-to-LTS) and 8 on default (7 and 1), with no unparsed records. No scheduled pass was missing before the 08:29 UTC cutoff; no overrun, aborted pass, failed/aborted/skipped job, space-driven stream deletion or PV-count mismatch was found. Maximum delay from planned time was 1.935457 seconds for shortened STS-to-MTS and 2.351970/2.359964 seconds for default transitions 0/1. All eight shortened MTS-to-LTS passes waited for the preceding transition; their maximum delay from its completion was 4.568742 seconds. These satisfy the interim five-second start-delay bound. Full-window coverage, tick-order and metrics reconciliation remain required |
| T7 | 2026-09-29 08:33:38-08:33:41 UTC | Recorded heap events through the 08:30 UTC samples | Passed | The actual `gc-heap.csv` records were filtered from each manifest start and deduplicated by component, PID, event timestamp, GC ID and before/after marker. Maximum post-GC heap in mgmt/engine/etl/retrieval was 63.16/72.04/179.77/97.21 MiB on shortened and 51.99/69.82/89.17/67.31 MiB on default. Latest recorded post-GC ETL heap was 58.22/43.39 MiB. Maximum observed ETL heap across before/after events was 254.03/254.80 MiB; these are recorded-event maxima, not continuous maxima. All eight JVM full-GC counters were zero in the separately inspected 08:20 UTC jstat rows. This extends the interim evidence only; full-window boundary coverage and pause analysis remain required |
| T8 | 2026-09-29 08:33:38-08:33:41 UTC | Both retrieval services; manifest-filtered `latency.csv` through 08:30 UTC | Passed | Each VM had 90 in-window latency samples with zero retrieval errors and zero failed representative visibility probes. Maximum recorded request duration was 99.448 ms on shortened and 99.790 ms on default. The expanded default VM's 08:30 UTC automatic sample still queried all 903 PVs and observed all six representative timestamps. These are interim retrieval checks, not exact ingestion latency or full-window acceptance |

At 08:20 UTC the default VM had 8.733 GiB free and had consumed about
0.494 GiB/hour over the preceding three hours. Continuing that rate would
have reached the collector's 2 GiB minimum near 14:58 PDT, before the scheduled
18:06 PDT finish. The online expansion removed that observed capacity risk;
retain the intervention as a test-condition change when evaluating T4-T6.
The shortened VM had 9.269 GiB free at 08:21:36 UTC and was not resized.
The scheduled finish times and observation manifests remain unchanged.

The superseded windows began on 2026-09-28 at 21:36:06.273146/09.006321 UTC
and were stopped before 24 hours to enable the additional measurements. Their
manifests, samples, final journal, preparation-stop measurements and original
tools remain under separate private `etl-soak-superseded-*` directories.
Their preparation stops took 11.780/13.202 seconds; these do not satisfy T5
for the replacement observation. Exact preservation paths are in the work
directory README and each new observation's `restart.json`.

The timing check observed at 2026-09-28 22:27:39 UTC examined the shortened
chain's two passes planned for 22:10:00 UTC. STS-to-MTS ended at
22:10:04.242661857, and MTS-to-LTS started at 22:10:08.788842393: 8.79 seconds
after the shared planned time and 4.55 seconds after the preceding pass ended.
The real pass records and deployed `ETLPassTicker.tickAll` agree with the
design's first-tick-after-completion rule. This ordering check satisfies the
corrected criterion; T4 remains In progress until the full window is evaluated.

Original 24-hour evidence analysis on 2026-09-30:

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T4 | 2026-09-30; original manifest-filtered archives | Both original 903-PV observations | Incomplete; failed assertions retained | Each has 290 full samples with maximum gaps of 300.019/300.034 seconds. Shortened completed all 288 STS-to-MTS and 24 MTS-to-LTS firings; default completed 24 and three, with no missing, duplicate or unexpected scheduled pass, failed/aborted/skipped job, overrun or PV-count mismatch. Maximum readiness-relative start delays are 3.792/4.569 seconds on shortened and 4.014/3.934 on default. All 290 metric snapshots per VM match completed counters, last-pass fields and busy times. Shortened has 14 failed full samples, including its final sample, and 124 actual recorded storage-threshold health failures. Default has zero recorded sample or retained health failures, but neither VM retains the health journal for the full window. Sampled JVM identities and boot IDs are unchanged. The appliance journals contain no OOM or forced-termination signatures; bounded kernel journal queries returned no entries and do not establish coverage. UTC intervals reach 24 hours; recorded monotonic intervals are approximately 3 ms shorter, with both retained. Default transition 1 moved no data to LTS |
| T5 | 2026-09-30 01:06:43/46 UTC terminal records | Both original observations | Passed for whole-unit shutdown | Both appliances were active before stopping and inactive with Result=success afterward. Actual stop commands returned rc=0 in 11.830/12.549 seconds against the 300-second timeout, with no forced-stop signature in the preserved appliance journal. Four complete JFR checkpoints and final journals were retained on each VM. Shortened final full collection returned rc=1 due to health failure; default returned rc=0. Successful shutdown does not establish successful final collection or overall soak acceptance |
| T7 | 2026-09-30; original-window GC aggregates | Four JVMs on both VMs, 256 MiB heaps | Analyzed | GC events were deduplicated by component, PID, GC ID and identical payload within a 2 microsecond cluster; no before/after pair is incomplete. The integer-nanosecond replay at 17:30 UTC measured maximum timestamp variation of 217/350 ns on shortened/default, superseding the earlier floating-point approximation. Maximum post-GC heap for mgmt/engine/etl/retrieval is 63.16/81.69/253.05/133.83 MiB on shortened and 51.99/74.24/89.17/67.31 on default. Maximum observed ETL heap is 255.16/254.80 MiB. Shortened ETL has four full GCs, consistent with jstat; each reduced 247.93-252.23 MiB to 26.55-28.64 MiB. Default and the other components have zero full GC. Maximum ETL pause is 118.186/22.111 ms, with total observed pauses 33.402/1.480 seconds. The retained fixed-population runs do not select a safe heap size for other loads |
| T8 | 2026-09-30; reassessed stored source timestamps | Both original retrieval services and unchanged deadband fixture | Failed for all-PV freshness assertion | HTTP errors and representative visibility failures are zero. Request maxima are 99.448/99.790 ms; P99 is 21.073/12.862 ms. Visibility upper-bound maxima are 9.722/6.695 seconds and include source age, rather than exact ingestion delay. Every full sample contains stale latest timestamps among the ten original deadband PVs, at most nine per sample. Comparing retained latest timestamps with request start minus 30 seconds yields 1499/1505 stale PV observations. The exact query-construction timestamp was not retained. The original collector accepted last-known returned data without a timestamp-window check, so its recorded 903-recent count does not establish all-PV freshness; initial and interim 903-recent claims above are superseded by this reassessment |

Private inputs, aggregate JSON, analysis scripts, report and checksums are retained
under the work directory with the `analysis-24h-` prefix. The original T6
comparison with the earlier matching load remains pending. The completed
two-hour retest is a separate observation and is excluded from these aggregates.

Focused retest preparation observations on 2026-09-30:

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T9 | 2026-09-30 07:00:28 UTC | Shortened VM, installed measurement tools and real appliance | Partial | The prior health failures were actual storage-threshold failures at 85 percent usage. The disk, partition 5 and XFS were expanded from 20 to 40 GiB with existing data preserved. Actual negative collection obtained 903 empty HTTP 200 responses and prevented observation start. The installed early-finish guard rejected an unelapsed window; the real abort preserved a final full sample and complete JFR for all four components, stopped the appliance in 11.377 seconds with rc=0 and no terminal errors, retained Incomplete and rejected repeated finish. These checks do not establish successful normal two-hour completion |
| T10 | 2026-09-30 07:03:05 UTC | Restarted shortened appliance, accepted deadband variant | Preparation verified | The post-restart full collector initially recorded HTTP 500 and retrieval errors; that pre-window evidence is retained. Subsequent real verification obtained two distinct successful health invocations and two zero-error full samples with 903 archiving PVs. Actual twenty deadband fields equal -1 and original registration CSV is unchanged. A systemd timer is active for readiness dispatch at 07:54:00 UTC, targeting observation start at 07:54:30 UTC. The observation has not opened; launch repeats actual readiness and capacity checks |
| T11 | 2026-09-30 09:13:49 UTC | Shortened VM, accepted ten-record deadband variant | Passed | The actual 7200-second manifest retained 26 full samples with zero errors and all 903 PVs recent. All 26 scheduled firings completed with no missing, duplicate or unexpected identity. Health coverage includes 233 completed invocations in the observation/final interval; failed assertions, missing coverage and incomplete GC pairs are zero. UTC finish-start interval is 7200.000216 seconds. The recorded monotonic interval is 7199.981597 seconds and is retained separately; the installed normal-finish guard allows two seconds of tolerance |
| T12 | 2026-09-30 09:13:49 UTC | Shortened VM, installed real observe.py and systemd paths | Passed | Actual normal finish began after the UTC manifest boundary, retained the final full sample, complete JFR for all four components and the final journal. Stop returned rc=0 in 11.378 seconds against the actual 300-second timeout; boot identity is unchanged and terminal errors are empty. The embedded evaluator reports Passed. The original collector hash identifies the code used throughout this trial |

The owner selected immediate start on 2026-09-30, superseding the 07:54:30 UTC
reservation. The old launch timer was stopped. The actual launcher repeated
readiness, succeeded and opened the manifest at 07:13:32.389373 UTC with
earliest finish 09:13:32.389373 UTC and duration 7200 seconds. The manifest
contains 26 expected scheduled firings. Its explicit initial sampler returned
rc=0, and the full sample at 07:13:32.623399 UTC retained zero errors.
T10 start was verified. The actual normal terminal record at 09:13:49.519860 UTC
now establishes T11/T12 Passed. The separately captured private completed
evidence replays through the shipped evaluator without changing its verdict.

Accepted collector and verification corrections on 2026-09-30:

| Scope | Environment | Observed Result | Evidence |
| --- | --- | --- | --- |
| Health collection | Control host; local shipped collector and real health recorder | Local correction verified | The collector evaluates the latest completed health invocation, requiring accepted status and completion within 120 seconds. An activating invocation does not replace that evidence. Missing, stale or failed completions remain errors; explicit readiness retains the strict completed-current-invocation requirement. Local recorder/collector tests and the terminal tests total 16 passing checks |
| Normal terminal path | Control host; shipped observe.py with external command/filesystem boundaries | Local failure handling verified | An unelapsed wall or monotonic interval cannot stop the appliance. An elapsed finish writes shutdown.json, retains collection/JFR errors and refuses a second stop. Abort writes its separate Incomplete record. Local verification does not establish the VM's normal shutdown |
| Final evaluation | Control host; test_evidence.py and real captured completed evidence | Eight checks passed at 2026-09-30 09:14 UTC | The shipped evaluator replays the actual passing observation without internal mocks. Negative tests change temporary external file copies and confirm Failed for single full-sample/freshness/health failures, Incomplete for missing scheduled passes/GC pairs or abort, and retained failures with missing final coverage. Original inputs are unchanged. Together with 16 local checks, all 24 executed checks pass |
| VM application | Shortened VM; completed control-host user service | Applied and hash-verified at 2026-09-30 09:14:44 UTC | The owner selected application after this trial ends. After actual terminal completion the prepared job ran immediately; its later timer was stopped to prevent duplication. It verified pinned sources, passed all 24 checks and installed the revised collector only after services/timers were idle. The old collector is archived. Installed hash equals the reviewed source, and the completed manifest, measurement configuration and terminal hashes remain unchanged. Service Result=success and ExecMainStatus=0. No new observation was opened; new runtime readiness for the changed tools remains unverified and requires fresh preparation proofs |

Local implementation verification on 2026-09-30:

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T13 | 2026-09-30 17:28:48 UTC | Control host; Python 3.13.5; shipped tools, original fixture and retained observations | Local checks passed; runtime pending | The complete suite ran 45 checks with zero failures and zero skips: 17 terminal/health checks, 12 evidence checks and 16 contract/aggregation checks. Real preparation ran for both durations and chains with filesystem/command boundaries replaced; wrong duration/chain, unexpected bundle entries and changed helper/JFC inputs were rejected. Independent grids match actual 288/24 and 24/3 pass identities. Schema-3 passing evidence still replays separately. Invalid grid/duration/coverage and malformed GC retain non-passing verdicts. All 18 dependency hashes match frozen bundle.json; all 59 SHA256SUMS entries match. All 38 Python files compile and parse with Python 3.9 grammar; this is not a Python 3.9 runtime execution |
| T14 | 2026-09-30 17:28:48 UTC | Control host; real installer, adjustment and preparation code with shipped fixture | Local preparation checks passed; VM pending | Initial adjustment, repeated existing-adjustment verification and repeated preparation preserve original CSV/database bytes, adjustment and completed terminal evidence. Conflicting or unrequested reapplication is rejected. Preparation checks both 7200/86400 seconds and both chains, archives the previous tools/units, installs the complete bundle and sets the bounded terminal service timeout to 45 minutes. Capacity checks bind separate historical/current measured sources, digests, duration/chain and current age. The real chain verifier reads the shipped 903 names through an external HTTP boundary and rejects wrong stores. Actual VM installation, twenty CA fields, source/resource/store-age checks and measured 24-hour headroom remain required |
| T15 | 2026-09-30; before VM application | Both VMs | Pending at local implementation completion | New health/empty-data/early-finish/abort preparation and successful real full samples require separate VM execution authority. Prior schema-3 proofs cannot qualify. Actual later executions are recorded below |
| T16 | Not run for the revised plan | Both VMs | Pending | No new observation was opened during local implementation; each chain still requires 86400 seconds in both clocks across UTC midnight |
| T17 | 2026-09-30 17:30:13 UTC | Control host; both retained original 24-hour inputs and pinned Maven source | Historical numerical replay verified; new runs pending | Frozen aggregate.py retains chain-specific pass counts, busy-time/delay/job/movement statistics and partial-day weekly usage. rate-semantics.json identifies the pinned engine/PV implementation, cumulative connection-dependent intervals, raw metric names and units; benchmark writing rows are excluded. The real retained metric-input regression preserves both arrival/write rows. Both historical outputs remain Incomplete, retaining freshness failures and missing coverage; shortened also retains health failures. New-load scheduler and metric acceptance remains T17 after T16 |
| T18 | 2026-09-30 17:28:48-17:30:13 UTC | Control host; original heap/collection/pause CSVs and approved copies of eight JVM GC logs | Historical aggregation checks passed; new coverage pending | Integer-nanosecond clusters reduce shortened heap rows from 276370 to 79002 and default from 85552 to 24076; maximum actual variation is 217/350 ns. Duplicating real exports preserves unique counts and pause totals. Exact timestamp keys retain excess heap events; conflicting real-event payloads are rejected. Each JVM's retained JFR collection IDs occur in its GC logs. Young/full/concurrent jstat values are reported separately; absent original command-time bounds remain missing coverage, including boundary count differences. Incremental GC capture tests retain rotations and reject truncation. New full-window JFR/DataLoss/rotation/jstat coverage still requires actual VM execution |
| T19 | 2026-09-30 17:28:48 UTC | Control host; shipped observe.py, external clock/filesystem/command boundaries | Local terminal checks passed; VM pending | The normal terminal path with 0.25 seconds remaining waits until the full monotonic duration. The same shipped regression executed against the preserved schema-3 observer fails at 7199.75 seconds for a required 7200 seconds. Current early-finish, repeat-stop, abort and collection-error paths retain their distinct outcomes. Final pass waiting, four complete JFRs, ETL work state, coordinated health completion and the actual whole-unit stop remain real-VM checks |
| T20 | Not run with new full-window results | Control host | Pending | T6 and the earlier-load comparison require both new completed observations; historical descriptive aggregates do not establish performance improvement |
| T21 | 2026-09-30 17:28:48 UTC | Control host; shipped aggregate.py CLI and coherent retained evidence directories | Local CLI checks passed; recipient package pending | Repeated actual CLI executions produce exactly matching parsed JSON values and no comparison mismatch for both historical inputs. Their missing coverage deliberately keeps exit status nonzero. A changed reference or missing input returns nonzero; missing input retains earlier failures. The specified sanitized two-run package, canonical snapshot, package-only evaluator replay and successful reference comparisons remain pending |

The initially verified bundle is preserved in the private
`work/soak-etl-pass-3bdf378c/schema4-approved-bundle.tar`; its bundle.json SHA256 is
`e00e1d7167a80eb1d776800be6b71754c6ce5d0aa021b95905fae678ace75ee8`.
It includes the current executable dependencies, JFC configuration, rate
definitions and historical schema-3 evaluator. The remaining schema-3 tools
are preserved under `tests/archiver-soak/etl-pass/legacy/schema3/`.
Local results are uncommitted working-tree evidence based on
`f7aba721463461ca8ea61a15819cd99041edbe5b`; no carrying commit exists yet.
The private `work/soak-etl-pass-3bdf378c/implementation-verification/` directory
retains `local-verification.json`, `legacy-finish-regression.json`,
`aggregate-replay.json`, both coherent input directories and both aggregate
JSON files. Final aggregate SHA256 values are
`05115825302bd7e49714df1825c1fd2d4004778598d2e01e7be34bd9a38f07cc`
for shortened and
`a9de01bfeebe4327bc24b0a1fc98fdf52d8adb70267eea57fd356a02737c9054`
for default. The approved GC-log copies preserve only the four manifest JVMs
and their rotations from each original run; original evidence is unchanged.

Actual VM preparation observations on 2026-10-01:

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T13 | 2026-10-01; local verification before staging at 05:37 UTC | Control host; all real retained inputs and shipped fixtures | 46 local checks passed; zero skips | The added first-boundary regression requires the real collector to issue a reverse lookup for past journal records. Actual VM journalctl returned no rows for the original --until/--lines query and one retained row with --reverse. Both collector boundary queries now use --reverse. The complete 46-check suite exits zero; result is retained in implementation-verification/local-verification-kernel-fix.json. A new complete bundle was frozen after verification; all original 24-hour failures remain visible |
| T14 | 2026-10-01 05:17:29-05:37:33 UTC | Both actual stopped deployments; separate private backups and staging paths | Preservation verified; capacity preparation pending | Both original terminal/manifest digests are recorded in schema4-staging.json and copied under separate etl-soak-before-schema4-* directories. Appliance and old timers were stopped before staging. The initial capacity-only attempt on shortened rejected an incorrect PV API path and stopped normally. Subsequent real 903-PV/four-JVM measurements retain their collection failures separately from a soak. A private probe-directory permission correction allowed actual four-component JFR dumps. Default's first data interval declined during existing-data processing and is rejected by the capacity contract; it is not converted to zero growth. Both probes stopped normally at 05:36:31/39 UTC. New capacity-only measurements use separate stable historical/current intervals before installation. Earlier 24-hour data-growth rates remain an additional projection floor; no ready/start claim is made |
| T18 | 2026-10-01 05:37:12-13 UTC | Both actual VMs; frozen corrected collector and actual journalctl | Bounded kernel path verified; full-window coverage pending | The shipped collect_kernel path retains the actual pre-boundary proof and returns complete coverage for the preparation interval on each VM, with zero observed kernel memory events. No internal function or transport is substituted in this check. This verifies the bounded current query, not a new 24-hour observation. Evidence: schema4-kernel-staging.json and each VM's live-kernel-verification directory |

The current `tests/archiver-soak/etl-pass/bundle.json` SHA256 is
`0c646646a5be06c6ea199403df23131ae4ea08aa9c74625b278df161c2a22b5c`.
The previous bundle and failed preparation records remain intact. The corrected
bundle was staged in separate directories before installation at 05:48 UTC.
`schema4-kernel-staging.json` records both exact staging
paths and bounded real verification results. Each VM's capacity-only services
record their own samples, rejected intervals, terminal state and source JSON;
these do not establish T15 or T16 success.

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T14 | 2026-10-01 05:48:03-06 UTC | Both real VMs; frozen bundle, approved fixture and preserved stores | Installation/fixture/capacity passed at this time | Both actual prepare-retest.py executions exit zero, preserve the terminal observation/tools/units and leave observation_started=false. Installed dependency hashes equal the current frozen bundle. Source pins and actual stamp are checked through the shipped preparation path. Shortened verifies the existing adjustment; default initially applies it and reads all twenty fields as -1. The original CSV and three database hashes remain preserved. Required 24-hour growth including capture allowance is 13766908018/13717123951 bytes. Original 24-hour data-growth floors are 6957496455/8840668796 bytes and do not exceed the measured data contributions. Actual available bytes are 22570323968/20118503424; projected free bytes are 8803415950/6401379473 and usage is 78.929/84.678 percent. These values satisfy the accepted 2-GiB and 85-percent conditions at installation; a changed logging policy requires new growth evidence. Private source receipts: schema4-installation.json, original-data-growth-floor.json and both capacity-installation-check.json files |
| T15 | 2026-10-01 05:51:45-05:59:02 UTC | Both actual appliances/IOCs/MariaDB/systemd; installed schema-4 tools | Partial; failed preparation retained; start refused | Both actual chain verifiers read all 903 deployed configurations and pass. Both first two-health/two-full-sample checks pass. Shortened then verifies the real health collection path while the unit is activating: starts=27, completions=26, the previous accepted completion is used and no internal function/transport is substituted. A subsequent actual full collection exits zero. Its negative retrieval check obtains 903 HTTP-200 PVs without samples and rejects observation start. Early finish and repeated finish are rejected; actual abort retains final full collection and four complete JFR files and stops in 11.218 seconds with rc=0. Final journal collection fails because journald dropped 11215 appliance messages, so abort readiness is rejected. Default's repeated health/full check fails on an actual journald report of 2010 dropped appliance messages. That failure is not treated as a transient healthy result. Neither VM has all required current runtime proofs |
| T15 | 2026-10-01 06:09:39-50 UTC | Both actual VMs; preparation held | Appliances stopped; no new observation | Shortened was already inactive after the failed abort verification. Default preparation is stopped with rc=0 in 11.120 seconds and Result=success; both health timers are stopped. No main observation.json exists on either VM. A successful preparation stop does not establish T19 success. Actual errors, original records and failed/preliminary attempts remain preserved in schema4-runtime-preparation-held.json and VM staging/evidence directories |

The original observed journal configuration is `SystemMaxUse=1G`,
`RateLimitIntervalSec=30s`, `RateLimitBurst=10000` in the existing journald
drop-in. Installed systemd 239 includes service-level LogRateLimit settings
in its shipped manual. Decision Date: 2026-10-01. The owner selected retaining
the logging detail and disabling the appliance service's rate limit.
At 06:24:34/38 UTC, both inactive preparations were preserved in distinct
directories before creating fresh preparation records. The isolated service
drop-in `50-soak-journal-rate.conf` sets `LogRateLimitIntervalSec=0` and
`LogRateLimitBurst=0`; actual daemon-reload, unit verification and effective
properties succeed. Existing stores and the frozen bundle are unchanged.
The global journald configuration is unchanged. The initial 0/0 setting did
not establish dropped-message prevention; subsequent executions are recorded
below. Fresh measured
capacity and actual T15 must pass before opening either 24-hour window.
Do not advance a journal cursor or erase a dropped-message record merely to
make a preparation sample pass.

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T14 | 2026-10-01 06:29:31-06:35:54 UTC | Both actual VMs with initial 0/0 service settings | Shortened capacity passed; default capacity rejected | Both real five-minute probes retain two successful full samples and zero shutdown journal errors. Required growth was 13752009292/13794889718 bytes; projected usage was 79.3928/85.4005 percent. Default's 40-GiB disk cannot satisfy the accepted less-than-85-percent threshold; no observation opened |
| T14 | 2026-10-01 06:40:43 UTC | Default VM and its actual hypervisor | Approved 48-GiB expansion verified | Virtual disk grew from 42949672960 to 51539607552 bytes. Actual partition 5 and XFS expansion succeeded; partitions 1-4, partition start/UUID and boot identity were preserved. Root filesystem total is 50369376256 bytes. Private default-disk-48g.json retains the actual before/after evidence |
| T14 | 2026-10-01 06:41:20-06:47:30 UTC | Default VM with 48-GiB disk and initial 0/0 settings | Capacity and shutdown journal checks passed at this time | Actual required growth is 13814281247 bytes, available 28360671232, projected free 14546389985 and projected usage 71.1206 percent. Both full samples and final shutdown journal capture have zero errors. These sources do not qualify after the later journal configuration change |
| T15 | 2026-10-01 06:37:45-06:51:13 UTC | Both real deployments with initial 0/0 settings | Shortened readiness passed at this time; default readiness rejected | Shortened completes all six runtime checks, including genuine activating health collection, 903 empty-data responses, four complete abort JFRs, an orderly 10.217-second stop and successful post-abort health/full samples. Default passes earlier checks and an orderly 10.260-second abort stop but its post-abort full sample detects Suppressed 3741 messages from the appliance service. That real failure prevents start and remains retained. No main observation exists |
| T14/T15 | 2026-10-01 07:02:30/40 UTC | Both stopped deployments | Approved 1us/10000 settings installed; runtime verification pending | Actual daemon reload and unit verification succeed; effective properties are LogRateLimitIntervalUSec=1us and LogRateLimitBurst=10000. Each previous preparation is preserved separately. All eighteen frozen dependencies and existing stores remain unchanged. New actual five-minute capacity and shutdown-journal probes began at 07:08 UTC. Installation is not proof of full-window journal coverage |
| T14 | 2026-10-01 07:08:13-07:14:27 UTC | Both actual deployments with approved 1us/10000 settings | Actual capacity and shutdown journal checks passed | Both full samples per VM and both final shutdown journal captures have zero errors; actual whole-unit stops return zero. Shortened/default required growth is 13747207630/13814372762 bytes, projected free 8252199474/14444693094 and projected usage 80.2482/71.3225 percent at measurement. Running systemd exports actual per-service interval 1 and burst 10000. Source windows, stop results and hashes are preserved under separate explicit-rate directories and schema4-journal-explicit-20261001.json. Fresh capacity was installed at 07:15:46/47 UTC with current available bytes and original 24-hour data-growth floors retained; actual 40/48-GiB disk resources are recorded |
| T15 | 2026-10-01 07:15:46-07:18:25 UTC | Both real appliances, original IOC fixture with accepted deadband override, MariaDB and systemd | Current actual runtime readiness passed | Both installed chain verifiers, initial two-health/two-full collection, genuine activating-health collection, following full collection, 903-PV empty-data rejection, abort checks and post-abort two-health/two-full checks return zero. Empty-data substitution is confined to the external clock boundary. Actual abort stops take 10.253332/10.234633 seconds on shortened/default, with zero terminal errors and four complete JFR recordings each. Early finish and repeated finish are refused. After real restart both have 903 connected/archiving/recent PVs, six visible probes, four JVMs with real heap/pause events, synchronized clocks and zero full-sample errors. Proofs bind to all eighteen frozen dependencies. Every earlier failed attempt remains separate |
| T16 | 2026-10-01 07:19:39-07:20:17 UTC | Both independent real VMs; approved 1us/10000 policy and frozen schema-4 bundle | Started; full-window outcome pending | Actual launchers return zero and open separate immutable 86400-second manifests at 07:19:39.849341/07:19:39.843094 UTC on shortened/default. Both UTC finish deadlines are on 2026-10-02 at the same respective times; monotonic starts are 214963.222810312/214921.173292255 seconds. Expected natural firings are 288/24 and 24/3. Both initial and 07:20 periodic samples succeed with all 903 PVs recent, six probes visible and zero errors. Appliance, health, sample and finish timers are active. Full duration, midnight behavior, complete coverage and final shutdown are not yet verified. Private schema4-24h-launch-20261001.json retains complete actual manifests, digests, readiness and unit observations |

Private schema4-journal-rate-recheck-20261001.json retains the initial 0/0
attempts, capacity results and the actual 3741-message failure. Later approved
1us/10000 evidence is retained separately; no earlier failure is replaced.

Actual terminal and journal observations on 2026-10-01 supersede the ongoing
state reported by the dated start row above. The private
`work/soak-etl-pass-3bdf378c/journal-scenario-basis-20261001.json` preserves the
actual read-only terminal observations and subsequent system-journal findings.
Its source records remain `/var/lib/etl-soak/abort.json`, the failed
`raw/*/sample.json` files and actual system-only journal queries on each VM.
The earliest retained system timestamp alone does not establish gap-free
coverage or absence of OOM throughout either interval.

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T16 | 2026-10-01 18:25:26.991110 UTC terminal; inspected at 21:52:50 UTC | Shortened; original frozen schema-4 bundle | Incomplete; automatically aborted | Actual abort reason is consecutive_sample_failures after kernel_journal errors at 18:20:00.244021 and 18:25:00.236807 UTC. Duration from manifest start to terminal finish is about 11 h 6 min, below 24 hours and before UTC midnight. Embedded evaluator retains final_journal, final_sample, kernel_journal and observation_duration failures plus missing coverage. Both observation timers and the appliance are inactive |
| T16 | 2026-10-01 21:35:37.251269 UTC terminal; inspected at 21:52:51 UTC | Default; original frozen schema-4 bundle | Incomplete; automatically aborted | Actual abort reason is consecutive_sample_failures after kernel_journal errors at 21:30:00.165243 and 21:35:00.159159 UTC. Duration from manifest start to terminal finish is about 14 h 16 min, below 24 hours and before UTC midnight. Embedded evaluator retains the same failed assertion classes and missing coverage. Both observation timers and the appliance are inactive |
| T18 | 2026-10-01; post-terminal read-only journal inspection | Both VMs; shipped collect_kernel and actual journalctl | Stale-anchor defect identified; correction unverified | Stored kernel cursors correspond to 2026-09-30 05:56:25.272527 UTC on shortened and 2026-10-01 06:39:45.870859 UTC on default. Their actual kernel lookups return no rows. Earliest retained system records are 2026-09-30 07:55:01.063035 and 2026-10-01 06:49:49.287537 UTC, still before trial starts. The collector retains an old kernel cursor when no new kernel record exists and rejects its later disappearance. No full-window coverage or OOM-absence conclusion follows from these findings |
| T19 | 2026-10-01; actual abort records inspected at 21:52 UTC | Both aborted observations | Orderly abort stops observed; normal terminal criterion unmet | Actual stop commands return zero in 11.540977/23.008912 seconds with inactive units and Result=success. Final full samples and final journal collection retain kernel-cursor failures; abort.json records final_sample and final_journal errors. Successful early stops do not establish T19's successful full-window final capture |
| T22 | Not executed for the journal-scenario revision | Dedicated test VM and preserved defective/candidate tools | Pending | Obsolete-anchor reproduction and candidate regression are specified above; no correction or regression execution occurred during this document update |
| T23 | Not executed for the journal-scenario revision | Dedicated test VM; real quiet system-journal intervals | Pending | Repeated quiet-kernel collection and absence of an initial kernel row require actual execution |
| T24 | Not executed for the journal-scenario revision | Dedicated test VM; live kernel/journald and terminal paths | Pending | Tagged benign events, rotation, race and final-capture comparisons require actual execution |
| T25 | Not executed for the journal-scenario revision | Disposable real journal copies and dedicated test VM | Pending | Required-record loss with an older surviving user journal and persistent failed assertions requires actual execution |
| T26 | Not executed for the journal-scenario revision | Retained actual boundary/midnight/boot inputs and test VM | Pending | Boundary continuity and changed-boot rejection require actual shipped-path execution |
| T27 | Not executed for the journal-scenario revision | Both stopped soak deployments | Preparation Pending; in-window Pending | Gap arithmetic was checked against shipped limits: 320+240=560 seconds, 320+2700=3020 seconds and factor-two allowance gives 6040 seconds. This verifies the written calculation only. Stream-write measurements, effective-cap inequalities, launch proof validation and complete in-window/terminal checks remain unexecuted; no retention-cap change or passing budget is claimed. The passing dedicated-VM preparation of 2026-10-03, recorded in the supplementary rows below, does not satisfy T27 on these deployments |
| T28 | Not executed for the journal-scenario revision | Dedicated complete test deployment and retained real abort inputs | Pending | Quiet-case non-abort and loss-case full-sample/dispatch/terminal/evaluator integration remain required |

Local journal-candidate verification supplements the pending live checks:

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T13/T14 | 2026-10-02 02:49:08 UTC | Control host; schema-5 sources and retained real runtime/export/fixture inputs | Local checks Passed; live preparation Pending | The shipped unittest discovery ran 57 checks in 37.944 seconds, rc=0 and no skips. It replays historical real evidence, exercises actual aggregation CLI comparisons, fixture checks and missing-retention-proof rejection without modifying retained inputs. Current preparation requires schema 5 and rejects schema 4. The preceding run's one missing-schema test-input error remains separately preserved; the successful run is `work/soak-etl-pass-3bdf378c/schema5-final-candidate-verification.json`. No successful new preparation or live collection is inferred |
| T27; T26 cursor-parser unit coverage | 2026-10-02 02:49:08 UTC | Control host; shipped budget arithmetic/parser code and retained actual application journal | Local unit portions Passed; live scenarios Pending | Budget arithmetic derives 560/3020-second gaps and a 6040-second horizon; byte/time/file-count failures refuse the calculation, and retained file allocation/user bytes are reserved. Actual cursor parsing and wrong-boot/missing-sequence rejection execute on preserved rows. The input is a filtered application journal, not a complete system/user sequence. No stale-anchor correction, event delivery, rotation, loss, reboot, OOM detection or final-capture integration claim follows |
| T13 | 2026-10-02; local candidate integrity check | Control host; frozen schema-5 candidate and private schema-4 preservation | Passed within local scope | `contract.verify_bundle` accepts all 39 candidate dependencies; all bundled Python sources compile. Candidate `bundle.json` SHA256 is `5673fc8cae3e272c2cfb55c07c8d2d637636e13240cbc6e5f57b008438dffd6f`. All nineteen preserved schema-4 files match the original bytes, including original bundle SHA256 `0c646646a5be06c6ea199403df23131ae4ea08aa9c74625b278df161c2a22b5c`. The candidate is not the final replacement bundle; live T22-T26/T28 and actual T27 preparation remain required |
| T26 cursor-parser unit coverage | 2026-10-02 03:26:10 UTC | Control host; actual retained 20-second all-journal export | Passed within parser-replay scope | All eleven shipped journal tests ran with no failures, errors or skips. The real validator accepts 6,399 actual records with 6,399 unique numeric entries, one sequence stream and no numeric gap. Removing one actual interior entry is rejected as missing records. Source bytes and tool hashes remain unchanged. Private `schema5-real-journal-sequence-verification.json` preserves execution evidence. This does not verify live collection, mixed-stream continuity, rotation, reboot, retention preparation or a full observation |
| T22-T28 environment input | 2026-10-02 04:31:25 UTC | Separate dedicated Rocky VM; actual libvirt resources, SSH and cloud-init | Baseline verified; deployment in progress | Actual domain has 2 vCPU, 4096 MiB assigned RAM and a 51,539,607,552-byte virtual disk. The guest reports Rocky 8.10, systemd 239, completed cloud-init with zero errors, and 48,784,998,400 root bytes available before species installation. Initial creator readiness returned nonzero because of an older SSH key at the reused address; the global known_hosts file is preserved and actual SSH verification succeeds with a separate per-VM file. The generated inventory contains only the dedicated host; all eight actual species plays select exactly one host and syntax-check returns zero. Private creation, baseline, preflight and environment records retain the evidence. Candidate instrumentation, 903-PV readiness, measured capacity and all live scenarios remain pending |
| T13/T27 dedicated deployment and prerequisite | 2026-10-02T04:45:20.648809+00:00 | Separate dedicated Rocky 8.10 VM; real species deployment and installed candidate CLI | Source/bundle/JVM checks Passed; measurement preparation Incomplete | Actual archiver-dev apply returns zero. The installed env and Maven HEADs match the two approved full pins; all four JVMs use -Xms256M and -Xmx256M, appliance and MariaDB are active, Python is 3.9.25, and the clock is synchronized. contract.verify_bundle accepts the 39 installed dependencies and candidate SHA256 remains 5673fc8cae3e272c2cfb55c07c8d2d637636e13240cbc6e5f57b008438dffd6f. Running the actual installed journal_retention.py snapshot returns 1 with FileNotFoundError for systemd in the declared PATH; the actual systemctl --version command returns zero and reports systemd 239. No live retention proof, fixture readiness, scenario pass or replacement observation is claimed. Private journal-test-deployment-verification.json and journal-test-tool-prerequisite-check.json preserve the observations |
| T13/T14 corrected version command | 2026-10-02 05:00:13 UTC local; 05:01:14 UTC installation | Control host and dedicated Rocky 8.10 VM; current schema-5 bundle | Local checks and installation Passed | Actual unittest discovery ran 57 checks in 41.694 seconds, rc=0 and no skips, using retained runtime/export/fixture inputs and the actual 20-second all-journal export. All 39 bundle dependencies verify, 81 listed checksums match, bundled Python sources compile, and nineteen original schema-4 files remain byte-identical. New bundle SHA256 is 6ffbb8a541787a237c54e058bffa44e71b096a2b3146fe471b3f1d5c9c315168. Only journal_coverage.py, journal_retention.py and bundle.json were replaced on the dedicated VM after source pins, boot and absence of an observation were checked. Previous files are preserved. Private schema5-systemctl-candidate-verification.json and journal-test-systemctl-deployment-verification.json retain the evidence |
| T23 single-collection prerequisite; T27 snapshot prerequisite | 2026-10-02T05:02:22.377393+00:00 | Dedicated VM; actual installed journal_coverage.collect and journal_retention.py snapshot | Single collection Passed; retention preparation Incomplete | Actual root-owned journal collection returns zero, validates six sequence records with one required record, and records coverage_complete=true for that one bounded interval. The actual snapshot CLI advances beyond version detection but returns 1 with Journal configuration application to the running daemon is unverified; no snapshot is produced. Private journal-test-systemctl-prerequisite-check.json and VM raw collection files preserve results. This single collection does not complete repeated quiet-interval T23, other live scenarios, retention preparation or a full observation |
| T27 journald configuration application | 2026-10-02T05:10:44.065538+00:00 | Dedicated Rocky VM; actual daemon and installed configuration | Application prerequisite Passed; preparation Pending | Preflight found one of two configuration files newer than the daemon. A scoped restart returns zero, replaces the daemon identity, and leaves journald active; both unchanged configuration files now precede daemon start. The subsequent actual snapshot reaches the missing fixture-adjustment input. Configuration caps remain persistent storage, 1 GiB and eight weeks. Private journal-test-daemon-configuration-preflight-20261002.json and journal-test-journald-application-20261002.json retain results; retained soak VMs are unchanged |
| T14 dedicated fixture readiness | 2026-10-02T05:15:17.787255+00:00 | Dedicated VM; shipped install-fixture.py, apply-fixture.py and register.py with original fixture | Fixture installation and registration Passed; full measurement readiness Pending | Actual installation, override application, registration and verify-existing commands all return zero. The actual API reports exactly 903 unique expected PVs, all connected and Being archived. The real CA check verifies all twenty MDEL/ADEL values as -1. Original databases and configuration are preserved by the shipped installers. No observation manifest was created. Private journal-test-fixture-installation-20261002.json retains commands, responses and counts |
| T27 single raw snapshot and fresh-host prerequisite | 2026-10-02T05:17:03.399818+00:00 | Dedicated VM; actual installed journal_retention.py snapshot and systemctl unit properties | Raw snapshot collected; retention proof and instrumentation Pending | The actual snapshot CLI returns zero and records the approved load and ten verified adjusted records. Sample and finish units are loaded with 4min/15min timeouts; abort is not-found while systemctl still reports its default 1min 30s timeout. That default is not an installed abort bound and this snapshot cannot qualify preparation. measurement-config.json and the instrumentation drop-in are absent, as are prior observation/terminal records. Existing retest entry points cannot initialize this fresh deployment. Private journal-test-fresh-preparation-preflight-20261002.json preserves the actual snapshot and properties. Seven qualified load measurements, hash-bound budgets, health/full samples and all required live scenarios remain pending |
| T13/T14 fresh initializer local checks | 2026-10-02T07:26:16.394059+00:00 | Control host; shipped schema-5 tools and retained real runtime/export/fixture inputs | Local checks Passed; measured preparation Pending | Actual unittest discovery ran 59 checks in 40.347 seconds, rc=0 and no skips. All 40 runtime dependencies and 82 checksums verify; nineteen original schema-4 files remain byte-identical. Candidate bundle SHA256 is 5cd0f390f42e7ed3d9bb8b9fcd88f3e42ab2dcf68d566f21912bca40c30553c6. Actual fresh-initializer guard paths reject previous observations and absent measurement inputs without changing retained evidence. Private schema5-fresh-initializer-local-verification.json records execution. These local guards do not prove fresh-VM preparation or any journal scenario |
| T14/T27 fresh instrumentation prerequisites | 2026-10-02T07:28:37.931661+00:00 | Dedicated VM; actual installed initialize-fresh.py instruments and journal_retention.py snapshot | Instrument initialization Passed; measured preparation Pending | The current 40-dependency bundle verifies. Before installing the abort unit, the actual retention CLI rejects the missing loaded sample/finish/abort prerequisite. The actual instruments command returns zero, preserves originals and records four 256M JVMs with running JFR recordings and nonempty GC logs. Real sample/finish/abort timeouts are 240/2700/2700 seconds. Existing tools are privately preserved; no observation exists. Private journal-test-fresh-initializer-deployment-20261002.json retains commands and initialization evidence. Two accepted health completions, two full samples, retention/capacity proofs and required live scenarios remain pending |
| T27 measured preparation execution | 2026-10-02T07:36:53.093134+00:00 | Dedicated VM; real initialize-fresh.py measure service | Running; no preparation verdict | The finite 45-minute oneshot service is loaded and activating with an actual process. One real journal snapshot and one GC/retrieval progress record exist; measurements.json and observation.json do not exist. The launcher wait timed out after 30 seconds while the service continued; journal-test-fresh-measurements-launch-20261002.json preserves that failure. Seven consecutive approved-load snapshots, two measured capacity windows and successful budget evaluation remain required |
| T14/T27 measurement progress and queued checks | 2026-10-02T07:48:03.568699+00:00 | Dedicated VM; actual subsystem captures and systemd jobs | Measurement running; followup waiting | Three journal snapshots and three GC/retrieval captures exist. Actual snapshot times are 07:35:39.932971, 07:40:40.014429 and 07:45:40.091088 UTC; the latest capture reports 903 recent PVs, six visible probes and all four GC components. A root-initiated followup is genuinely queued with After/Requires on the running measurement service and a finite 35-minute timeout. It runs the shipped prepare action from actual completed inputs, then verify-chain.py and verify-health.py; the latter performs two real health/full-sample checks. It preserves failures and opens no manifest. No followup result is inferred. Private journal-test-fresh-followup-launch-20261002.json records exact executable source and the successful queue operation; journal-test-chain-preflight-verified-20261002.json separately records two completed captures and one actual fixture PV matching shortened stores. This one-PV check does not replace all-903 chain verification |
| T27 dedicated measured retention budget | 2026-10-02T08:05:44.772270+00:00 calculation; observed at 08:25:26 and re-derived at 08:26:54 UTC | Dedicated VM; seven actual snapshots and shipped journal_retention calculation | Failed; preparation and dependent checks did not execute | All seven snapshots retain the actual 903-PV load and ten verified adjusted records. Six intervals last 300.064-300.084 seconds, with peak physical write bound 61,778.213 bytes/s per stream; shipped calculation requires 1,291,544,426 bytes against the effective 1,073,741,824-byte cap and fails independently. The final 4.376396-second interval records 12,210,176 written bytes, raising the bound to 2,790,006.860 bytes/s per stream, required bytes to 34,248,546,484 and required files to 259 against 100. The measurement service exits 1 and preserves its failed proof; measurements.json, preparation.json, chain/health verification and observation.json are absent. Root has 43,213,418,496 bytes free at diagnosis. No passing preparation, full-sample readiness or 24-hour launch is inferred. Actual VM measurement sources and private journal-test-fresh-measurements-result-20261002.json retain evidence; diagnose the short-interval accounting and resolve cap sufficiency before another execution |
| T27 retention budget diagnosis | 2026-10-03T06:09:18Z | Control host; shipped `journal_retention` at `55ae31a` on the seven actual dedicated-VM snapshots, the failed proof and the 07:35:00-08:06:00 UTC actual journal export (46,062 entries) | Diagnosed; correction accepted | Re-derivation reproduces the recorded values exactly: six 300.064-300.084-second intervals with write deltas of 14,544,896-18,538,496 bytes, peak 61,778.213 bytes/s, 1,291,544,426 required bytes, and 34,248,546,484 bytes with the 4.376-second final interval, equal to the failed proof's budget. `rates()` applies the one daemon `write_bytes` counter to both streams, so the rate term is counted twice; over the six intervals the user journal's allocation grew by 4,096 bytes and the system journal's by 25,165,824 bytes in 8-MiB steps. Every write delta is a multiple of 4,096 bytes; the counter records about 3.9 times the actual file growth and about 2.2 times the exported JSON size (7,368,071-7,603,388 bytes per interval). The final interval holds one 6,367-entry latency-probe burst, which each five-minute interval also contains. Counting the rate term once gives 918,404,021 bytes. Page-granular re-dirtying of journald's memory-mapped pages is the likely source of the excess over file growth; it was not tested |
| T13/T27 accounting-corrected candidate | 2026-10-03T06:12:06Z | Control host; Python 3.13.5; shipped tools with the corrected `journal_retention.py`; private evidence, archive, extracted, journal-sequence and retention-snapshot paths | Local checks Passed; live preparation Pending | `contract.py --freeze` rewrote `bundle.json` (SHA256 `e11d3ebc820f14d961bbefbf1dc1e514c2b304733fdf21ce1d8aa1f30871f98c`) and `contract.verify_bundle` accepts all 20 dependencies; all 51 `SHA256SUMS` entries verify. Unittest discovery runs 58 checks with no skips and rc=0 with every private path set, and 37 pass with 21 skipped without them. On the actual snapshots the corrected tools bound the system stream at 61,778.213 bytes/s and the user stream at 13.650 bytes/s from its allocation growth, exclude the 4.376-second final interval, and require 918,486,465 bytes and 11 files against 1,073,741,824 bytes and 100 files: passed. The new shared-counter checks fail on the tools at `55ae31a` (user bound equal to the write rate); the real-input short-interval check errors there because the interval rule does not exist. No VM was contacted |
| Second dedicated environment and fixture | 2026-10-03T07:02:04Z | A fresh Rocky 8.10 VM created by cloud-provision on the control host (2 vCPU, 4096 MiB, 48 GiB), shipped `archiver_dev` species at `8bfa611` with `common.yml`, `shortened.yml` and the full source pins | Passed | The species apply returned rc=0 with 33 successful tasks and no failed or unreachable host. The installed tools verify the 20-dependency bundle `e11d3ebc`. The species wrote the journald drop-in 49 ms before the daemon started, so the daemon ran with it, but `journal_retention.py snapshot` derives the start from the whole-second boot time and refused the application as unverified; one `systemd-journald` restart made it verifiable, after which the snapshot refused only the absent measurement units. `install-fixture.py` and `apply-fixture.py` returned rc=0 (10 records, 20 fields); `register.py` received 903 replies; all 903 PVs were connected and archiving with no unexpected PV; `--verify-existing` passed. `initialize-fresh.py instruments` returned rc=0 with four JVMs, and `check` returned rc=0 after the population reconnected. The second environment's inventory, owner and execution authority are recorded in private `work/soak-etl-pass-3bdf378c/journal-test-20261003/environment.json`, beside its step records; `journal-test-environment.json` remains the first environment's record |
| T27 measured retention budget on the second VM | 2026-10-03T07:33:25Z | Second dedicated VM; shipped `initialize-fresh.py measure` with the corrected candidate under the approved 903-PV load | Passed; first attempt failed | The first attempt at 07:02:22 UTC, 76 seconds after the instrumentation restart, stopped after one snapshot: one of 903 retrieval requests returned an HTTP error, and three later requests for the same PV returned HTTP 200. Its directory is preserved on the VM. The second attempt from 07:03:20 UTC took seven snapshots 300.074-300.128 seconds apart with every latency probe complete; write deltas per interval were 16,326,656, 17,776,640, 19,234,816, 19,619,840, 20,832,256 and 20,197,376 bytes. The system bound is 69,421.028 bytes/s and the user bound 0 bytes/s; 964,562,529 bytes and 11 files are required against 1,073,741,824 bytes and 100 files, so the budget passed with about 10 percent headroom. The capacity projection requires 11,838,250,087 bytes of growth for 86400 seconds. No observation was opened |
| T15 fresh preparation on the second VM | 2026-10-03T07:35:14Z | Second dedicated VM; shipped `initialize-fresh.py prepare` with the measured retention proof and capacity input, 86400 seconds, shortened chain | Passed; runtime verification Pending | rc=0. `preparation.json`, the copied retention proof and its sources and the capacity inputs exist under `/var/lib/etl-soak/`; the sample and finish timers are inactive and no observation exists. Deployed-chain, health, full-sample and empty/abort runtime verification remain required before launch |
| T15 readiness health check on the second VM | 2026-10-04T04:31:24Z | Second dedicated VM; shipped `verify-health.py` with bundle `e11d3ebc` | Failed; evidence retained | The first health invocation and full sample at 04:31:14 UTC had no errors, 903 archiving PVs and a passing in-window budget at the measured 69,421.028 bytes/s system bound. The second full sample, 9.419 seconds later, failed `journal_retention_budget`: `runtime()` took the interval, which held one latency-probe burst, as a 1,781,193.678 bytes/s bound and required 11,303,673,757 bytes and 89 files against 1,073,741,824 bytes and 100 files. `verify-health.py` returned rc=1 and wrote no `health-verification.json`; the timers stayed inactive and no observation exists. Both runtime snapshots and the first budget are retained privately under `journal-test-20261003/runtime-short-interval/` |
| T13/T27 in-window interval correction | 2026-10-04T04:35:07Z | Control host; Python 3.13.5; shipped tools with `interval_budget()` and the evaluator change; every private evidence path including the two runtime snapshots | Local checks Passed; preparation on a third VM Pending | `contract.py --freeze` rewrote `bundle.json` (SHA256 `7c551c4b75382acf0ab94f091fb1710b3755563dfe11368387ff4da3d35a7158`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 60 checks with no skips and rc=0 with every private path set, and 38 pass with 22 skipped without them. On the two actual runtime snapshots `interval_budget()` keeps the 69,421.028 bytes/s bound, records the 9.419-second gap and passes. The two new checks error on the tools at `31917b3` because `interval_budget()` does not exist there; the failing budget recorded on the second VM is the evidence of the earlier `runtime()` behavior |
| Third dedicated environment, preparation and readiness | 2026-10-04T05:32:51Z | A fresh Rocky 8.10 VM created by cloud-provision on the control host (2 vCPU, 4096 MiB, 48 GiB); shipped `archiver_dev` species at `31917b3` with the same variables; bundle `7c551c4b` | Passed through the empty-data check | The species apply returned rc=0 with 33 successful tasks; the journald drop-in needed the same one restart to become verifiable; fixture, deadband adjustment (10 records, 20 fields), 903-PV registration and readiness, `instruments` and `check` returned rc=0. Measurement started 300 seconds after the instrumentation restart, at 05:01:49 UTC, and passed at 05:31:55 UTC: six intervals of 300.065-300.167 seconds, write deltas rising from 16,654,336 to 19,632,128 bytes per interval, a 65,403.934 bytes/s system bound and 0 bytes/s user bound, 940,299,280 bytes and 10 files required against 1,073,741,824 bytes and 100 files. `prepare` returned rc=0 at 05:32:16 UTC. `verify-health.py` passed two health invocations and full samples; the second sample, 5.206 seconds after the first, kept the 65,403.934 bytes/s bound and passed. `verify-chain.py` verified 903 PVs on the shortened chain and `verify-runtime.py empty` returned rc=0. Private record: `journal-test-20261004a/environment.json` |
| T15 terminal-path check on the third VM | 2026-10-04T05:33:32Z | Third dedicated VM; shipped `verify-runtime.py abort` with bundle `7c551c4b` | Failed; evidence retained | Early finish and repeated finish were rejected, the abort verdict was Incomplete, the whole-unit stop returned rc=0 in 11.248 seconds and all four complete GC recordings were captured. The only terminal error was `cancel_timers`: `systemctl stop` on `etl-soak-sample.timer` and `etl-soak-finish.timer` returned 5 because the finish timer is created only when an observation opens and was not loaded. The check therefore returned rc=1 and, by design, did not restart the appliance, which remains inactive. The probe directory is preserved on the VM |
| T13 unloaded-finish-timer correction | 2026-10-04T05:37:07Z | Control host; Python 3.13.5; shipped tools with `observe.stop_loaded()`; every private evidence path | Local checks Passed; preparation on a fourth VM Pending | `contract.py --freeze` rewrote `bundle.json` (SHA256 `bbbf5d90165eaa8679e0d64daf9d053e28b61f7dad27fd923e528cfd47dd81e3`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 62 checks with no skips and rc=0 with every private path set, and 40 pass with 22 skipped without them. Through the real `observe.terminal()` with only the command boundary replaced, an abort before launch with an unloaded finish timer stops only the sample timer and records no `cancel_timers` error, while a failed stop of a loaded timer still records it. On the `observe.py` at `31917b3` the unloaded-timer case fails with `cancel_timers` in the errors, as on the third VM |
| Fourth dedicated environment, shortened chain | 2026-10-04T06:26:28Z | A fresh Rocky 8.10 VM created by cloud-provision on the control host; species at `31917b3`; bundle `bbbf5d90` | Passed through the empty-data check; abort check Failed | Species, fixture, instrumentation and check passed. Measurement started at 05:55:28 UTC, 300 seconds after the instrumentation restart, and passed at 06:25:36 UTC: six intervals of 300.065-300.176 seconds, a 68,575.520 bytes/s system bound, 959,455,659 bytes and 11 files required. `prepare`, two health checks, the chain check (903 PVs) and the empty-data check passed. In the abort check the corrected timer cancellation stopped only the loaded sample timer and recorded the finish timer as `not-found`. The only terminal error was `final_sample`: the abort probe's proof validation took a snapshot at 06:26:07.368 UTC and the final full sample another 0.293 seconds later; no writes were counted between them, but `system.journal`'s modification time had changed, and `rates()` refused the interval as changed files without write accounting. The appliance remains inactive by design. Replaying the two actual snapshots through the shipped `rates()` reproduces the refusal; they are retained privately under `journal-test-20261004e/runtime-mtime-only/`. Private record: `journal-test-20261004e/environment.json` |
| Fifth dedicated environment, default chain | 2026-10-04T06:05:26Z | A fresh Rocky 8.10 VM created by cloud-provision on the control host; species at `31917b3` with `default.yml`; bundle `bbbf5d90` | Superseded during measurement | Species, fixture, instrumentation and check passed and the measurement started. The local driver was stopped when the modification-time correction superseded bundle `bbbf5d90`; the measurement unit on the VM was left to finish and no observation exists. Private record: `journal-test-20261004g/environment.json` |
| T13 modification-time correction | 2026-10-04T06:30:50Z | Control host; Python 3.13.5; shipped tools with `journal_retention.content()`; every private evidence path including the modification-time pair | Local checks Passed; preparation on two new VMs Pending | `contract.py --freeze` rewrote `bundle.json` (SHA256 `ad70a93adcf916e28c3b6641f6e5f5ae9850f6ed79714c8d4acca84018f2d5c6`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 64 checks with no skips and rc=0 with every private path set, and 41 pass with 23 skipped without them. On the actual 0.293-second pair `rates()` returns zero for both streams and `interval_budget()` passes; a synthetic interval whose allocation grew with no counted writes is still refused. On the `journal_retention.py` at `31917b3` both new checks fail with the same refusal as on the fourth VM |
| Sixth and seventh dedicated environments, both chains | 2026-10-04T07:27:40Z | Two fresh Rocky 8.10 VMs on the control host; bundle `ad70a93a`; shortened and default chains | Measured preparation Passed on both; readiness Failed on both | Measured preparation passed: shortened 942,963,836 bytes (65,831.435 bytes/s system bound), default 935,771,642 bytes (64,654.325 bytes/s). `prepare`, two health checks and the chain check passed on both. Five minutes later a health check's full sample failed on both VMs with two errors. `journal_retention_budget`: the 317.8-second interval from the proof's last snapshot held the readiness samples' extra latency-probe bursts, measured 106,063.5 bytes/s on the default VM and required 1,185,883,313 bytes against the 1-GiB cap. `kernel_journal`: the system sequence interval had a missing number. Private records: `journal-test-20261004h/` and `journal-test-20261004i/` |
| Rocky 8 journald unlinked entries | 2026-10-04T08:26:26Z | The two VMs above; Debian 13 archiver-dev VM (systemd 257.9) on the same deploy; exploratory scripts only, no shipped tool changed | Confirmed on Rocky 8.10, not reproduced on Debian 13 | Across all journal files of the boot, 9 and 39 sequence numbers had no readable entry; `journalctl --header` showed exactly that many more entry objects in `system.journal` than `journalctl` enumerates, `journalctl --verify` passed, and neither the journal nor the kernel log reported a write failure or suppression. 903 concurrent mgmt requests from two client workers lost 65-137 lines per run on Rocky 8.10 and none with one worker; the instance's `systemd-cat` relay passed every byte by its `/proc/<pid>/io` counters. On Debian 13 the same test lost no line in four two-worker runs and the header and enumerated counts matched. Losses so far are per-request mgmt INFO lines and build output, but the loss follows bursts, not content. The interpretation that entries were written but not linked, and lost, is superseded by the row "Rocky 8 journald cause": the entries are stored and systemd 239 `journalctl` does not return them |
| T13 Maven pin move | 2026-10-04T09:07:08Z | Control host; Python 3.13.5; shipped tools with `SOURCE_PINS` and `rate-semantics.json` at Maven `254a6542`; every private evidence path | Local checks Passed; preparation on new VMs Pending | `common.yml` pins Maven `254a6542`; both `SOURCE_PINS` tables carry its full hash; `rate-semantics.json` names it as the source of the unchanged `EngineMetrics.java` definitions. `contract.py --freeze` rewrote `bundle.json` (SHA256 `cc2024251224d89946a84f8936ab3b8dab8aadb20d5cc53e21fca3cd76378f4a`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 64 checks with no skips and rc=0 with every private path set, and 41 pass with 23 skipped without them. No VM has been built at the new pin |
| Eighth dedicated environment, shortened chain | 2026-10-04T10:28:04Z | A fresh Rocky 8.10 VM created by cloud-provision on the control host; bundle `cc202425`; Maven `254a6542`; shortened chain | Passed through the chain check; readiness Failed while waiting for a closed ETL pass | Species, fixture and instrumentation passed. Measured preparation passed at 10:22:45 UTC: six 300.063-300.144-second intervals, 38,497.635 bytes/s system bound, 777,867,682 required bytes against the 1-GiB cap. `prepare`, two health completions with full samples and the chain check for all 903 PVs passed. The first full sample after the first closed pass, at 10:28:00 UTC, failed `kernel_journal`: the required interval is missing records. A read-only union scan of every journal file of the boot found 16 sequence numbers with no readable entry; 12 of them fall at 10:22:58-10:22:59 UTC among the mgmt instance's lines during the chain check. This is the Rocky 8 journald loss recorded above, not a tool defect |
| Rocky 8 journald cause | 2026-10-04T22:33:37Z | Fresh plain Rocky 8.10 guest (systemd 239-82.el8, then 239-82.el8_10.19; kernel 4.18.0-553.el8_10) and Debian 13 guest (systemd 257.9), both from cloud-provision, rate limiting disabled; the eighth dedicated VM; private reproducer `journald-burst-repro.py`; refs jeonghanlee/epicsarchiverap-env#58 | Cause found: a reader defect, no stored entry lost | One writer emitting 5000 identical lines: Rocky returns 295, exactly one per distinct realtime timestamp, with 4704 unreturned sequence numbers and a passing `journalctl --verify`; systemd 257 reading a copy of that Rocky file returns all 5000, and Debian 13 returns all 5000. Eighteen Rocky runs with unique lines (1-16 writers, up to 2000 characters, concurrent readers, user and system files, service stdout, CPU load, repeated `journalctl --sync`, the soak journald settings) lost nothing, and no run recorded suppression. On the eighth VM, 903 concurrent mgmt requests left 22, 30 and 45 unreturned numbers with two client workers and none with one; over one fixed window systemd 239 returns 21,520 mgmt entries and systemd 257 returns 21,632 from a copy of the same file. systemd v239 `sd-journal.c` `compare_with_location()` treats an entry as the current one when boot, realtime and content hash match, without comparing the sequence number; upstream commit `b17f651a17cd` (first in v248) adds that comparison, and the latest Rocky 8.10 update still returns 295 of 5000. The earlier 9, 39 and 16 unreturned numbers and the 65-137 burst lines are this defect |
| T13 unreturned-sequence correction | 2026-10-04T23:23:29Z | Control host; Python 3.13.5; shipped tools with `journal_coverage.sequence_holes()`, `account()` at every collection and the evaluator check; every private evidence path including the eighth VM's failed sample, two actual accounting records and one actual archived journal file with its systemd 239 header listing; the eighth VM and the reproduction guest for the shipped functions | Local checks Passed; collection on two later VMs Passed (row "Tenth and eleventh dedicated environments") | The eighth VM's failed interval is accepted with 12 recorded unreturned numbers, each preceded by a mgmt line of the same HTTP worker thread. The shipped `account()` found one stored entry per sequence number on the eighth VM with the appliance running (112,641 for sequence 1-112,641) and on the reproduction guest after rotation and removal of older files (944,713 for 398,896-1,343,608), although `journalctl` returns fewer. Twenty runs on the eighth VM during continuous 903-request two-worker bursts all passed, the slowest after 114 header reads in 3.14 seconds; the limit is 600 attempts. The direct header read equals `journalctl --header` on all 13 immutable files of the reproduction guest. No actual file begins before the retained range, so enumeration of such a file is covered by arithmetic checks only. `contract.py --freeze` rewrote `bundle.json` (SHA256 `9c38425c77468ee0a9283c206ba5580bab5c410f98f9d558705fe5952608a43f`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 69 checks with no skips and rc=0 with every private path set, and 43 pass with 26 skipped without them. The shipped `collect()` with the accounting had not yet run on a full collection when this row was written |
| Ninth dedicated environment, default chain | 2026-10-04T10:09:36Z | A fresh Rocky 8.10 VM created by cloud-provision on the control host; bundle `cc202425`; Maven `254a6542`; default chain | Failed at PV readiness | All 903 PVs registered, but after 90 readiness attempts 808 were connected and archiving and 95 never connected. The engine lists exactly those 95 as pending metadata gets, with CA state NEVER_CONNECTED and CAJ command thread id 2; a sample of 101 connected PVs spans thread ids 0, 1 and 3-9 and none is on 2. A loopback capture shows the IOC answering every search for the 95 at the engine's search port. In the engine JVM two sockets are bound to that one UDP port, while each other CA context holds its own port; kernel 4.18.0-553.el8_10. CAJ (jca 2.4.12, unchanged between the two Maven pins) binds every context's search socket to an ephemeral port with SO_REUSEADDR, so two contexts can share a port and only one receives the replies. The eighth VM on the same pin and eight earlier VMs connected all 903 PVs. The defect and its fix belong to epicsarchiverap-maven (jeonghanlee/epicsarchiverap-maven#26); which socket the kernel delivers to is not yet observed |
| T13 Maven pin move to the search-port correction | 2026-10-05T01:45:23Z | Control host; Python 3.13.5; shipped tools with `SOURCE_PINS`, `rate-semantics.json` and `common.yml` at Maven `aa953a44`; every private evidence path | Local checks Passed; preparation on two new VMs Passed (row "Tenth and eleventh dedicated environments") | `git diff 254a6542 aa953a44` over the packaged sources lists only `engine/pv/EngineContext.java` and `engine/pv/JCACommandThread.java`; the ETL sources and `EngineMetrics.java` are unchanged. Maven workflow run 37249019863 on `aa953a44` concluded success at 2026-10-05T01:22:57Z. `contract.py --freeze` rewrote `bundle.json` (SHA256 `68d527a0a6e4173a1d7c02e7e9abef1659fb698466ba90cc7595ae53e729567b`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 69 checks with no skips and rc=0 with every private path set, and 43 pass with 26 skipped without them. Two VMs built at this pin are recorded in the next row |
| Tenth and eleventh dedicated environments, both chains | 2026-10-05T03:13:01Z | Two fresh Rocky 8.10 VMs created by cloud-provision on the control host (2 vCPU, 4096 MiB, 48 GiB); species at `19adbfd` with `shortened.yml` and `default.yml`; bundle `68d527a0`; Maven `aa953a44`; private driver `run-to-launch-template.bash` | Passed through every readiness check; observation not started | Species rc=0 with 33 successful tasks on both. Measured preparation passed: shortened 761,106,651 required bytes (35,722.633 bytes/s system bound), default 770,412,806 (37,277.034); six intervals of 300.068-300.152 seconds on each. `prepare`, two health completions and the chain check for all 903 PVs passed, then 903 of 903 PVs archiving and connected on both chains, including the default chain after its first start. The first full sample after the first closed ETL pass had zero errors on both (shortened 02:46:01Z, default 03:07:14Z), and the empty-data and abort checks passed (stops of 11.7 and 11.2 seconds, no errors, all four complete GC recordings). Health and full samples after the abort passed on both (shortened 02:51:56Z, default 03:13:01Z). Across all full samples, systemd 239 `journalctl` did not return 5 sequence numbers on the shortened VM and 1 on the default VM, each in one full sample (02:46:01Z and 02:46:33Z) and none in any other; each was recorded and the header accounting found one stored entry per sequence number (60,632 and 83,511 entries at the last sample, no unreturned number outside the retained range). The bundle's `journal_coverage.collect()` and the evaluator's recomputation of it ran on real collection output for the first time. The retained evidence is on each VM and in its private `journal-test-<label>/` directory |
| Launch of both 24-hour observations | 2026-10-05T05:20:41Z | The two VMs of the row above; shipped `launch-retest.py` with bundle `68d527a0`; private steps `refresh-runtime-proofs.bash`, `fresh-capacity-refresh.py` and `launch-after-capacity.bash` | Both observations started; running | The first launch attempt at 05:12Z failed on both VMs with `Current capacity growth measurement is stale` and opened nothing: the current window of the preparation's capacity measurement had ended at 02:40Z and the launcher only checks that it ended within 600 seconds, it does not measure. The runtime proofs had also passed their one-hour limit twice while the decisions were pending, and were repeated (empty-data and abort checks, stops of 11.3 and 11.2 seconds, no errors, 903 of 903 PVs afterwards). A private step then took two real full samples 300 seconds apart, built a new current window from the shipped `contract` functions, kept the historical window and the previous capacity files, and `launch-retest.py` opened both observations with a 75-second target: shortened at 05:20:41Z, default at 05:20:40Z, each with an initial sample of rc 0 and earliest finish 24 hours later. At 07:05Z (1.75 hours) both had 22 error-free in-window samples, no consecutive failures or abort request, 61 (shortened) and 10 (default) closed ETL passes, journal accounting passing at 172,082 and 193,905 stored entries with no unreturned number outside the retained range, and about 39 GiB free; the journal held 129 and 137 MiB, below the 1-GiB cap. The retained evidence is on each VM and in its private `journal-test-<label>/` directory |
| First 24-hour observations, aborted at the first journal rotation | 2026-10-05T14:00:25Z | The two VMs of the row above; bundle `68d527a0`; private evidence under each VM's `aborted-evidence/` directory (evidence and real journal files, hash-listed) | Failed; both observations Incomplete | Both aborted by the abort policy after consecutive full samples failed `journal_retention_budget`: shortened at 14:00:05Z (107 in-window samples), default at 07:20:06Z (27). Until then every in-window sample had no error and the journal accounting passed (last samples 419,988 and 208,259 stored entries for the same number of sequence numbers). The first failing sample was the one after the system journal reached its 128-MiB file size and rotated (shortened 13:55:00Z, default 07:15:00Z): the 134,225,920-byte file reappeared under an archived name and `rates()` took it as new growth, so the 300-second interval measured 447,374.855 bytes/s against 25,000-60,000 bytes/s before, which fails the 1-GiB budget (3,424,768,893 required bytes) and stays in the peak bound for every later sample. The real writes in the interval were 11,563,008 bytes. The inventory already recorded the inode and device of each file. The abort itself ran as designed (stop rc 0, verdict Incomplete). Cause and fix are in the next row |
| T13 rotation accounting correction | 2026-10-05T15:19:30Z | Control host; Python 3.13.5; shipped tools with the `rates()` change and every private evidence path including the actual snapshot pair across the first rotation | Local checks Passed; preparation on new VMs Pending | `rates()` now matches files by device and inode. On the actual pair the committed code returns 447,374.855 bytes/s and the corrected code 38,539.494 bytes/s, equal to the interval's writes; `interval_budget()` passes with the first collection's bound, and both new checks (the actual pair and a synthetic rename) fail on the committed `journal_retention.py`. A file whose inode did not exist before still counts in full. `contract.py --freeze` rewrote `bundle.json` (SHA256 `cb9b8106693cd2006c6873008d9ee1712eac8357ed1e801e5b90620ad6661c3d`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 71 checks with no skips and rc=0 with every private path set, and 44 pass with 27 skipped without them. No VM has been built at this bundle |
| Twelfth and thirteenth dedicated environments, both chains | 2026-10-05T17:18:34Z | Two fresh Rocky 8.10 VMs created by cloud-provision on the control host (2 vCPU, 4096 MiB, 48 GiB); species at `19adbfd`; bundle `cb9b8106`; Maven `aa953a44`; private step `run-and-launch.bash` | Both prepared; shortened observation aborted, default observation started | Both passed every readiness check (903 of 903 PVs, first full sample after the first closed pass without errors, empty-data and abort checks, health after the abort) and were launched through the capacity refresh. The shortened observation opened at 16:56:07Z and was aborted by the abort policy at 17:10:05Z: the full samples at 17:05:00Z and 17:10:00Z each failed `sts_bytes` with `du` exit status 1, a store size measurement that races the ETL pass of that chain, which moves and removes 5-minute partitions on the same 5-minute grid as the sampler. The verdict was Incomplete with `observation_duration` and `sts_bytes` failed. The default observation opened at 17:18:34Z with an initial sample of rc 0 and an earliest finish at 2026-10-06T17:18:34Z |\n| T13 store size measurement correction | 2026-10-05T17:16:59Z | Control host; Python 3.13.5; shipped tools with `collect.tolerated_du()` and `directory_bytes()`; every private evidence path including an actual `du -sb` result captured while a directory was being rewritten | Local checks Passed; shortened preparation on a new VM Pending | `du` printed a total and `No such file or directory` messages and exited 1 on a real directory walk raced against removals on the control host; the corrected measurement accepts exactly that result and still fails on any other exit status, on an error other than a vanished file, and on an empty total, while the committed collector fails all three new checks. `contract.py --freeze` rewrote `bundle.json` (SHA256 `3e9815b03a5d33a21652da422c5274374cec1326d8b110c1be91f3e9a42588f2`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 74 checks with no skips and rc=0 with every private path set, and 46 pass with 28 skipped without them. The appliance's own partition removal was not reproduced; its exit status 1 is read from the failed samples |\n| T13 standalone schema-5 bundle | 2026-10-02 20:54:06 UTC | Control host; Python 3.13.5; shipped schema-5 tools and retained real runtime/export/fixture inputs | Local checks Passed; dedicated installation and live scenarios Pending | Earlier-schema sources were removed from the shipped tools: `BUNDLE_FILES` no longer lists the schema-3 evaluator or the nineteen schema-4 files, and the evaluator returns Incomplete with `unsupported_observation_schema` for any other schema. Actual unittest discovery ran 55 checks in 36.505 seconds, rc=0 and no skips. `contract.verify_bundle` accepts all 20 dependencies and all 51 checksums verify. Candidate bundle SHA256 is 567d629b11704a2291302eb603830e313d85a9b7bab37629a0656ec7a31c0726; it supersedes the 40-dependency candidate recorded above and is not installed on any VM. Four retained-evidence cases now relabel the pre-schema-5 input and require a non-Passed verdict with the expected failed assertion. Four cases are removed because they exercised the removed schema-3 evaluator: Passed replay, missing scheduled pass, missing GC pair and aborted observation. The current evaluator has no retained-evidence coverage for those four until a schema-5 observation completes; add them then. The removed sources remain in the private evidence directory as `legacy-sources-removed-from-tree-20261002/` |
| T13 journal budget separation | 2026-10-06T00:26:09Z | Control host; Python 3.13.5; shipped tools with `collect.budget_capture()`, `journal_retention.BudgetFailed` and the evaluator and aggregator change; every private evidence path including the complete evidence of the aborted rehearsal observation | Local checks Passed; observation on new VMs Pending | The evaluator replayed on the actual aborted rehearsal observation no longer lists `journal_retention_budget` among the failed assertions and reports the failed samples separately, while the abort and its terminal errors remain; the committed tools list it as a failed assertion, and both new checks fail on them. Any other journal failure is still raised as a sample error. `contract.py --freeze` rewrote `bundle.json` (SHA256 `11ee9c8e8737a177d133ced4563e5d406a1e41549468b02b01aeac92835f7ad1`), `contract.verify_bundle` accepts all 20 dependencies and all 51 `SHA256SUMS` entries verify. Unittest discovery runs 77 checks with no skips and rc=0 with every private path set, and 48 pass with 29 skipped without them. No VM has run this bundle |
| Replacement shortened observation | 2026-10-05T18:24:54Z | A fresh Rocky 8.10 VM created by cloud-provision on the control host (2 vCPU, 4096 MiB, 48 GiB); species at `19adbfd`; bundle `3e9815b0`; Maven `aa953a44`; private step `run-and-launch.bash` | Prepared and launched; running | Species rc=0 with every readiness check passed (903 of 903 PVs, first full sample after the first closed pass without errors, empty-data and abort checks, health after the abort, ready at 18:18:23Z); after the capacity refresh the observation opened at 18:24:54Z. At 20:05Z it had 21 error-free in-window samples, no consecutive failure and no abort request; the store size measurement that aborted the earlier shortened observation had not failed. On the default observation of the pair the first system journal rotation occurred at 20:00:00Z with bundle `cb9b8106`: the budget passed with the system bound unchanged at 51,853 bytes/s and 1,035,708,866 required bytes against 1,073,741,824, and the sequence accounting passed |
| Fourteenth and fifteenth dedicated environments, both chains, and the rehearsal environment | 2026-10-06T02:12:51Z | Three fresh Rocky 8.10 VMs created by cloud-provision on the control host (2 vCPU, 4096 MiB, 48 GiB); species at `19adbfd`; bundle `11ee9c8e`; Maven `aa953a44`; private step `run-and-launch.bash` | All three prepared and launched; two observations running | Each passed every readiness check (903 of 903 PVs archiving after the abort check, two health completions after it, empty-data and terminal-path proofs present) and was launched through the capacity refresh: the shortened observation opened at 01:36:33Z, the default observation at 02:12:51Z, each with an initial sample of rc 0 and an earliest finish 24 hours later, across UTC midnight. The third VM opened a shortened observation at 01:36:36Z for the `M25` / T8 rehearsal only. At 05:26Z the shortened observation had 46 error-free in-window samples and the default 39, each past its first system journal rotation (05:10:00Z and 04:40:00Z) with the budget passed (907,922,937 and 1,035,657,923 required bytes against 1,073,741,824) and the sequence accounting passed |
| Terminations of the earlier pair | 2026-10-06T05:28:57Z | The shortened observation VM (bundle `3e9815b0`) and the default observation VM (bundle `cb9b8106`) of the rows above | Both Incomplete; shortened aborted by policy, default stopped on owner request | The shortened observation ran from 18:24:54Z to 04:15:29Z with 120 full samples: the user journal bound rose from 614 to 27,958 bytes/s at the 04:10:00Z sample, so the retention budget required 1,100,140,027 bytes against 1,073,741,824, the samples at 04:10:00Z and 04:15:00Z failed `journal_retention_budget` with no other error, and the abort policy of that bundle ended the observation (dispatched 04:15:07Z, appliance stopped in 11.86 s with rc 0; evaluation Incomplete with `journal_retention_budget`, `observation_duration`, `final_sample` and `final_journal` failed). The ETL passes themselves had no fault; bundle `11ee9c8e` no longer aborts on this check (`D23`). The default observation ran from 17:18:34Z to 05:28:57Z with 148 full samples and no failed sample; its budget stood at 1,068,687,754 required bytes, 5,054,070 under the cap, so the owner stopped it on 2026-10-06 rather than let the same policy end it (request 05:28:35Z, appliance stopped in 12.91 s with rc 0; evaluation Incomplete with only `observation_duration` failed). The complete evidence of both (`/var/lib/etl-soak` and `/var/log/journal`) was copied to the control host and verified against the SHA256 sums made on each VM; both VMs were then removed by cloud-provision |

##### Closure Evidence

- Deployment, initial GC/latency collection, the focused retest, its actual
  normal shutdown and the accepted post-terminal collector correction are
  verified. M22 remains In progress: the original 24-hour runs retain failed
  freshness assertions and incomplete health coverage, and T6 comparison
  remains pending. The revised two-chain 24-hour plan was accepted on
  2026-09-30; code implementation and local verification of steps 1-2 are
  authorized and locally verified: the initial bundle passed 45 local checks;
  the deployed schema-4 bundle passed all 46 local
  checks. Local portions of T13/T14/T17/T18/T19/T21 are recorded above;
  their full-window or recipient-package portions, T16-T21 and T6 remain
  pending. VM application, runtime preparation and new observation execution
  were authorized on 2026-10-01. Installation and initial measured capacity
  passed, but actual T15 failures prevented start. The owner selected the
  service-specific rate-limit exception on 2026-10-01. After the initial 0/0
  setting still allowed 3741 suppressed messages on default, the separately
  approved 1us/10000 settings were installed on both VMs. Prior preparation
  failures are preserved. Fresh real capacity and shutdown journal rechecks
  passed at 07:14 UTC and real T15 runtime preparation passed on both VMs at
  07:18 UTC. Both 24-hour observations started at 07:19:39 UTC; initial and
  first periodic samples passed. Both trials later aborted with Incomplete
  verdicts after the pre-trial kernel cursor became unavailable. Shortened
  finished at 18:25:26.991110 UTC and default at 21:35:37.251269 UTC on
  2026-10-01; neither reached its 24-hour deadline or UTC midnight. The actual
  abort stops succeeded, but final collection retained errors. Both
  appliances and observation timers are inactive. The 2026-10-01 scenario
  revision adds T22-T28 and was accepted on 2026-10-01, with all seven checks pending;
  all five first-review findings are reflected in the plan.
  Local code implementation and verification were authorized on 2026-10-01.
  The schema-5 local candidate implements system-only terminal checkpoints,
  bounded all-stream sequence coverage, retention measurement/proof validation
  and runtime/evaluator budget checks. It passed 57 local checks with no skips
  at 2026-10-02 02:49:08 UTC; all nineteen original schema-4 files remain
  byte-identical. This verifies only the stated local scope.
  The subsequent dedicated-VM direction and 48-GiB disk selection are recorded;
  the actual baseline, inventory and species source/JVM/bundle checks are
  verified. The owner-selected systemctl version command is implemented and
  the new bundle passed 57 local checks with no skips at 05:00:13 UTC.
  Dedicated installation verified all 39 dependencies at 05:01:14 UTC,
  preserving the previous files. Actual journal collection succeeds for one
  bounded interval. The dedicated journald restart verifies configuration
  application at 05:10:44 UTC; fixture installation and registration verify
  all 903 expected connected/archiving PVs and twenty approved field values
  at 05:15:17 UTC. One actual snapshot succeeds at 05:17:03 UTC, but the
  abort unit and instrumentation are absent. The default timeout reported
  for a not-found abort unit is not qualified preparation evidence. A fresh
  initialization path was authorized on 2026-10-02 because existing retest
  tools require prior observation/terminal records. The new 40-dependency
  bundle passed 59 local checks at 07:26:16 UTC; actual GC/JFR initialization
  and loaded 240/2700/2700-second units are verified at 07:28:37 UTC.
  Seven actual approved-load subsystem captures completed by 08:05:40 UTC.
  The real retention-budget calculation failed at 08:05:44 UTC. Both the
  six qualified intervals and the additional short final interval exceed
  the 1-GiB cap; the latter materially increases the bound and requires
  diagnosis. The dependent preparation, all-PV chain and health/full-sample
  checks did not execute. No observation exists and no cap/policy change
  is authorized by this evidence update. The full T27 proof and replacement checks
  remain pending. T27 in-window completion is
  required at final acceptance and is not a start prerequisite;
  live collector correction and replacement observation execution are not
  established by the local checks. Runtime, launch, abort and scenario
  basis evidence are retained in the ignored work directory and on each VM;
  no external result message has been sent. The standalone schema-5 candidate
  without earlier-schema sources passed 55 local checks with no skips at
  2026-10-02 20:54:06 UTC and is not installed on any VM. Retained-evidence
  coverage of the Passed replay, missing scheduled pass, missing GC pair and
  aborted observation cases awaits a completed schema-5 observation.
  No carrying commit exists for the current code or results.

</details>

#### M23 - Add the Perl modules for the EPICS-env installed-tree utility to the EPICS OS package set

- Origin: 38560eb / M23
- GitHub Issue: #29, https://github.com/jeonghanlee/ansible-provision/issues/29
- Status: Complete

##### Summary

EPICS-env is moving its installed-tree utility from Python to Perl. The
runtime uses `JSON::PP` and `Digest::SHA`; its tests and checks use
`Test::More` and `podchecker` (`Pod::Checker`). A Rocky 8.10 base image
provides none of the four modules, and a Rocky 10.2 EPICS image lacks
`Test::More` and `Pod::Checker`. On Debian and Ubuntu the modules ship in
`perl-modules-<version>` and `libperl<version>`, which the `perl` package
depends on; `perl-base` alone does not carry them, and no Debian-family
`epics_os_packages` list names `perl`.

##### Scope

`epics_os_packages` in `inventory/group_vars/rocky8.yml` and
`inventory/group_vars/rocky10.yml` gains `perl-Digest-SHA`, `perl-JSON-PP`,
`perl-Pod-Checker` and `perl-Test-Simple`; the lists in `debian12.yml`,
`debian13.yml`, `ubuntu24.yml` and `ubuntu26.yml` gain `perl`. Both
`roles/epics` and `roles/epics_build` install the list, so the distribution
and source-build paths carry the modules alike.

Out of scope: the EPICS-env utility itself; the pkg_automation per-OS lists,
the reference baseline, whose matching change EPICS-env proposes separately;
a rocky9 vacuum, which this repository does not define; versioned Debian
package names.

##### Completion Criteria

- On each of the six vacua, after the `common`, `provenance`, `python` and
  `epics` operators apply in that order,
  `perl -MJSON::PP -MDigest::SHA -MTest::More -MPod::Checker -e 1` exits 0
  and `podchecker` is on `PATH`.
- A re-apply of the `epics` operator succeeds.

##### Dependencies And Decisions

- Requested by EPICS-env on 2026-10-02; its Perl work has not started, so
  this milestone does not block it.
- `D20` (2026-10-02): the four Rocky module packages and `perl` on the
  Debian family.
- Owner decision (2026-10-02): T2 applies the smallest product the operator
  order allows for `epics` (`common`, `provenance`, `python`, `epics` on a
  bare vacuum), not a full species. It exercises the distribution path;
  `epics_build` installs the same list with the same package commands, and
  its source-build path is observed on the next `epics_dev` apply rather
  than here.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-10-02
- Implementation Authorization: 2026-10-02
- Superseded Plan Artifacts: none

1. Add the four Rocky package names after the existing Perl entries in
   `rocky8.yml` and `rocky10.yml`.
2. Add `perl` to the four Debian-family lists.
3. Run T1 on the control host.
4. Report the commit to EPICS-env and run T2 on fresh bare vacua.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | Parse the six group_vars files as YAML; `--syntax-check` on `playbooks/operators/epics.yml` and `playbooks/operators/epics_build.yml`; resolve each module with `dnf repoquery --whatprovides 'perl(<Module>)'` on Rocky 8.10 and Rocky 10; in a throwaway container per OS, install the added names and run the module check from the Completion Criteria | control host; Rocky 8.10, Rocky 10, Debian 12, Debian 13, Ubuntu 24.04 and Ubuntu 26.04 containers | All files parse and both playbooks pass; each module resolves to the added Rocky name; the module check passes in every container |
| T2 | Integration | With a `bare` generated inventory, `make op.<operator>.<vacuum> RUNTIME_INVENTORY=<host inventory>` for `common`, `provenance`, `python` and `epics` in that order; `perl -MJSON::PP -MDigest::SHA -MTest::More -MPod::Checker -e 1` and `command -v podchecker`; re-apply with `make op.epics.<vacuum>` | Fresh rocky8, rocky10, debian12, debian13, ubuntu24 and ubuntu26 bare vacua from cloud-provision | Every apply succeeds, the module check exits 0 and `podchecker` is found on every vacuum; the re-apply succeeds |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-10-03T00:55:07Z | control host, working tree on `4e7f115`; `rockylinux/rockylinux:8.10`, a Rocky 10.2 EPICS image, `debian:12`, `debian:13`, `ubuntu:24.04` and `ubuntu:26.04` containers | Passed | The six lists parse with no duplicate entries; `--syntax-check` exits 0 for both playbooks; `git diff --check` is clean; `dnf repoquery --whatprovides` maps `Digest::SHA`, `JSON::PP`, `Pod::Checker` (and `podchecker`) and `Test::More` to `perl-Digest-SHA`, `perl-JSON-PP`, `perl-Pod-Checker` and `perl-Test-Simple` on Rocky 8.10 and 10.2; before installation the Rocky 8.10 image has none of the four modules, the Rocky 10.2 image lacks `Test::More` and `Pod::Checker`, and the Debian-family images lack `JSON::PP`; after installing the added names, the module check passes and `podchecker` is found in all six containers |
| T2 | 2026-10-03T05:14:47Z | Fresh rocky8, rocky10, debian12, debian13, ubuntu24 and ubuntu26 bare vacua from cloud-provision (4 GiB, no proxy precondition), `bare` generated inventories, working tree on `4dfb290` | Passed | On every vacuum `make op.common`, `op.provenance`, `op.python` and `op.epics` exit 0 with `failed=0` in that order; the module check prints `MODULES_OK` with `podchecker` at `/bin/podchecker` (Rocky) or `/usr/bin/podchecker` (Debian family); the `make op.epics.<vacuum>` re-apply exits 0 with `failed=0`. All test VMs were removed afterwards |

##### Closure Evidence

- Delivered in `4dfb290` (the four Rocky module packages, `perl` on the
  Debian family, this row and detail); T2 recorded in `300ccc7`.
- T1-T2 Passed against every completion criterion. #29's body was synced to
  the result and the issue was closed manually (observed closed, reason
  completed, at 2026-10-03T05:55:38Z); the `Closes #29` footer in `300ccc7`
  has no further effect when the branch reaches `master`.
- Landed: `origin/m14-middleware-reconcile` stood at `300ccc7` after its
  push; the branch is not yet merged to `master`.
- The result was reported to EPICS-env on 2026-10-02 with the commit and the
  Debian-family addition. The matching `configure/epics-packages` change in
  cloud-provision, the normative source, is cloud-provision's.

#### M24 - Split the archiver MariaDB operator into socket and TCP operators and rename the archiver-dev species

- Origin: 38560eb / M24
- GitHub Issue: #52, https://github.com/jeonghanlee/ansible-provision/issues/52; peer request from the cloud-provision session on 2026-10-05
- Status: Complete
- GitHub Projection: observed 2026-10-16T06:43:15.845854+00:00; state `closed`; reason `completed`; label `enhancement`; milestone `Backlog`; assignee `jeonghanlee`; updated 2026-10-16T06:42:05Z.

##### Summary

The archiver configuration database has separate socket-only MariaDB, loopback-TCP MariaDB and SQLite operators. The `archiver-dev-uds`, `archiver-dev-tcp` and `archiver-dev-sqlite` species select one database operator each. The MariaDB forms share task code, while the legacy `archiver-dev`, `archiver_dev` and `mariadb` names remain deprecated aliases of the socket-only form.

##### Scope

Split `roles/mariadb` and `playbooks/operators/mariadb.yml` into
`mariadb_uds` (no TCP listener, the account at `localhost` over the Unix
socket, `DB_SOCKET`) and `mariadb_tcp` (listener on `127.0.0.1:3306` only,
`skip-name-resolve`, the application account at `127.0.0.1`, the archiver
build writing that host and port, the socket still available and root still
socket-authenticated). Add the species `archiver-dev-uds` and
`archiver-dev-tcp`, keep `archiver-dev-sqlite`, and rename
`inventory/group_vars/archiver_dev.yml` to `archiver_dev_uds.yml` with a new
`archiver_dev_tcp.yml`. Keep `archiver-dev` and `archiver_dev` as a deprecated
alias of the `-uds` names. Update the names where `roles/archiver_build`, the
README, `docs/ARCHITECTURE.md`, `docs/CLOSED_DOORS.md` and the soak tools'
README use them.

Out of scope: the `archiver` distribution species and the middleware species
(cloud-provision marks them not yet implemented); the SQLite operator;
removing the alias, which follows epicsarchiverap-env's move; the soak tools'
bundle, which pins no species name.

##### Completion Criteria

- Each of the three species applies on a fresh guest and the appliance answers
  the management API.
- On `archiver-dev-uds` MariaDB has no TCP listener and the application
  connects through the socket; on `archiver-dev-tcp` it listens on
  `127.0.0.1:3306` only and the application connects to that host and port
  with the account at `127.0.0.1`.
- `archiver-dev` still resolves to `archiver-dev-uds` and says it is
  deprecated.
- A re-apply of each species succeeds.

##### Dependencies And Decisions

- Timing: `D21` set the start after the `M22` observations finish because
  their deploys read the current names. On 2026-10-06 the owner started it
  at once: every deployment in progress had finished its species stage, and
  deployed VMs are unaffected by a later change, so this row no longer
  depends on `M22`.
- `D21` (2026-10-05): the three-operator definition, the rename, the alias
  and the timing.
- Requested by cloud-provision on 2026-10-05 (its M19 closes only after this
  change lands); the landing commit goes to that session for a read-only
  check and to epicsarchiverap-env for its driver's move.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-10-06; the owner accepted the plan below
- Implementation Authorization: 2026-10-06; the role, playbook, species, group variable and reference changes, T1, and T2 on three fresh VMs from cloud-provision
- Superseded Plan Artifacts: the `D21` statement that implementation waits for the `M22` observations

1. Move `roles/mariadb` to `roles/mariadb_uds` (socket-only). Make
   `roles/mariadb_tcp` a thin role that runs the same task code in the
   loopback mode (`127.0.0.1:3306` only, `skip-name-resolve`, the application
   account at `127.0.0.1`, socket and root socket authentication kept), so
   the code is kept in one place. Keep the application-password step in both.
2. Add the operator playbooks `mariadb_uds.yml` and `mariadb_tcp.yml`, the
   species `archiver_dev_uds.yml` and `archiver_dev_tcp.yml` (the SQLite
   species stays), and the group variables `archiver_dev_uds.yml` (moved
   from `archiver_dev.yml`) and `archiver_dev_tcp.yml`
   (`mariadb_skip_networking: false`).
3. Keep `archiver_dev`, its group variables and the `mariadb` operator as
   deprecated aliases of the `-uds` names, each saying so when it runs.
4. Update the names in `configure/RELEASE`, `roles/archiver_build`, the
   README, `docs/ARCHITECTURE.md`, `docs/CLOSED_DOORS.md` and the soak README.
5. Run T1 on the control host, then T2 on three fresh guests, one per species.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Mechanism | Parse the changed group variables as YAML; `--syntax-check` on every changed operator and species playbook; resolve the alias | Control host | Every file parses and checks; `archiver-dev` resolves to the `-uds` species |
| T2 | Integration | Apply each species to a fresh guest through the generated inventory and `make <species>.<vacuum>`; read the listeners and the application's database connection; apply again | Fresh Rocky 8.10 guests from cloud-provision, one per species | The completion criteria hold on all three and the re-apply succeeds |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-10-06T01:38:30Z | Control host; ansible-core of the control host; working tree with the new roles, playbooks and group variables | Passed | `ansible-inventory --host` on a host of each group returns `mariadb_skip_networking: false` for `archiver_dev_tcp`, the socket-only default for `archiver_dev_uds` and for a host in the old `archiver_dev` group through the alias, and `archiver_db_backend: sqlite` for `archiver_dev_sqlite`. `ansible-playbook --syntax-check` passes on `mariadb`, `mariadb_uds`, `mariadb_tcp`, `archiver_dev`, `archiver_dev_uds`, `archiver_dev_tcp` and `archiver_dev_sqlite`; `--list-tasks` of `archiver_dev` shows the deprecation play and then the `mariadb_uds` tasks; `make -n` resolves `archiver_dev_tcp.rocky8`, `op.mariadb_tcp.rocky8` and the alias `archiver_dev.rocky8`. The include of the shared tasks in `mariadb_tcp` is exercised only by T2 |
| T2 | 2026-10-06T03:08Z | Three fresh Rocky 8.10 guests from cloud-provision, one per species; each species playbook run directly with the generated inventory (not through `make`) | Passed | First apply: failed=0 on all three. `archiver-dev-uds`: no listener on 3306, `skip-networking` on, account only at `localhost`, `DB_SOCKET` set, no TCP connections, management API 200. `archiver-dev-tcp`: listener on `127.0.0.1:3306` only, `skip-networking` off with `skip-name-resolve`, accounts at `127.0.0.1` and `localhost`, no `DB_SOCKET`, 16 TCP connections, management API 200. `archiver-dev-sqlite`: MariaDB inactive, `DB_BACKEND` sqlite, management API 200. First apply of `-tcp` exposed that its group variables lacked `archiver_db_socket: ""`; added before the run recorded here. Re-apply: failed=0 and changed=0 on all three. The alias on a guest was not run; T1 covers it |

##### Closure Evidence

- Implementation: 3b697e1d18617d22372557cfbe31ea4ce92e7f2b delivers the two MariaDB operators, the UDS/TCP species and group variables, the deprecated aliases and the updated references. SQLite remains independently selectable.
- Recorded mechanism verification: T1 Passed on 2026-10-06T01:38:30Z for inventory variables, playbook syntax, alias task resolution and Make target resolution.
- Recorded integration verification: T2 Passed on 2026-10-06T03:08Z on three fresh Rocky 8.10 guests. The UDS guest had no MariaDB TCP listener; the TCP guest listened only on `127.0.0.1:3306`; the SQLite guest had MariaDB inactive. Each management API returned HTTP 200, each first apply had `failed=0`, and each re-apply had `failed=0` and `changed=0`.
- Observed method: the integration runs invoked the species playbooks directly with generated inventories. Make targets and the deprecated alias were checked on the control host; a guest run through Make and a guest apply of the deprecated alias were not recorded. The original Test Plan and Verification Results remain unchanged.
- GitHub issue: #52, https://github.com/jeonghanlee/ansible-provision/issues/52; observed `closed` with reason `completed`, closed at 2026-10-16T06:42:05Z. All six acceptance criteria are checked and the closure comment records the existing results.

#### M25 - Verify independent journal recording, retention and collection

- Origin: 38560eb / M25
- Identity History: transferred on 2026-10-05 from `M22` / T22-T28 (`D22`)
- GitHub Issue: #31, https://github.com/jeonghanlee/ansible-provision/issues/31
- Status: Complete

##### Summary

In the positive observation, verify three distinct journal outcomes through the actual logging paths: required events reach journald, those records remain readable from the live journal when checked later, and the collector preserves their identity and content exactly. Separately verify correct detection of deliberate required-record loss while preserving the failed retention result. Perform an approximately one-hour basic delivery/query/collection check, a full 24-hour independent observation, and evidence reconciliation during the approximately two-hour overall result-decision period.

Journal acceptance is independent of ETL processing acceptance. An ETL movement, transformation, deletion or retrieval defect does not by itself fail the journal test. Real ETL failures and their actual application records can be logging inputs; journal success depends on its own required actions, direct reads, retention and archive comparisons.

Decision Date: 2026-10-15. The owner accepted the completed 24-hour journal recording, live-retention and exact collection result and directed issue closure without another full-day run. Normal-stop/post-stop collector verification moves to M27 and independent-recipient full-day replay moves to M28 as separate Deferred Backlog work. Both checks remain unexecuted; neither is marked Passed or gates this accepted journal measurement. Reusable source/procedures belong in Git-managed paths; raw evidence and deployment records remain private.

##### Scope

This work owns `tests/archiver-soak/journal-validation/`, its procedure, logging-path triggers, independent producer evidence, collector, direct queries, comparison, lifecycle handling and completion record. Extract only required dependencies from immutable baseline commit 649fee80561611f1494c1c3ce1f9546f6c619173. Do not import or modify the evolving `tests/archiver-soak/etl-pass/` tree. Preserve original bundles and results for their original replay.

Install under `/opt/journal-validation`, keep evidence under `/var/lib/journal-validation`, use locks under `/run/journal-validation` and units under the `journal-validation-*` namespace. Use a dedicated appliance deployment with the actual target journald/journalctl and extracted shipped collector. Retain installed versions, source/artifact identities, effective configuration and actual workload. No ETL acceptance tools, proofs, services, changes, successful observation or completion result is required.

##### Out Of Scope

Normal-stop/post-stop collector verification is owned by M27. Independent-recipient full-day replay is owned by M28. Both are independent Backlog work and do not block accepted journal recording/retention/collection or require a new 24-hour producer run.

ETL functionality/performance acceptance; changes to ETL deployments; production-wide logging policy; host sizing, disk-capacity forecasting, extrapolated retention horizons and claims beyond the observed period. Sufficient capacity for the full day is an established premise. Do not impose an inherited artificial journal size cap, a capacity study, safety multiplier or calculated retention budget as readiness or acceptance. Configure the dedicated positive test to retain the required records, preserve the actual effective settings and report actual errors.

##### Test Signals And Logging Frequencies

Use the same shipped 903-PV appliance fixture throughout the applicable scenarios and record the actual load independently of the journal verdict.

| Signal group | PV count | Configured source frequency |
| --- | --- | --- |
| General scalar, string and state | 775 | 1 Hz |
| Arrays, configured capacity 1000 elements | 8 | 1 Hz |
| Fast | 110 | 10 Hz |
| Slow | 10 | 0.1 Hz |

These are configured source frequencies, not observed archived-event counts. Source processing, MONITOR/SCAN registration and actual archived events remain distinct. Retain actual generated values, timestamps and order where used as a comparison input; do not derive observed reference counts from nominal frequency multiplied by duration or assume array occupancy from configured capacity.

| Logging path | Scheduled actual input | Producer and source evidence |
| --- | --- | --- |
| System | Identifiable record every second | Independent producer ID, sequence, expected payload, actual emission outcome and direct system-journal identity/content. |
| Kernel | Actual kernel-path test record every 10 seconds | Independent emission outcome and a matching live journal record with the actual kernel transport identity. |
| Appliance | Actual retrieval request every second | Independent request ID, unique PV/time-range tuple, action/HTTP outcome, required real application messages and unambiguous message correlation. |
| Health | Actual health execution every minute | Planned/actual action, systemd invocation identity, real service outcome and its matching live journal records. |

Freeze the event schedule and required messages before execution, and reconcile every scheduled action with the independent producer record. Skipped, failed or unresolved required actions cannot be omitted to obtain Passed. ETL pass or error messages must come from real application processing, never synthetic pass markers. The planned quiet-kernel scenario has its own explicit schedule and event accounting; it must not silently skip actions from the positive observation.

##### Execution Order And Time Allocation

| Order | Planned time | Journal work and required result |
| --- | --- | --- |
| Basic recording/query/collection check | About 1 hour | Trigger each real logging path; compare producer outcomes with direct live journal reads and collector output by identity and payload. Prove actual appliance-message correlation and retain the baseline records. |
| Long observation | At least 24 hours, alongside independent ETL observations | Keep actual logging and collection running; retain initial and planned intermediate direct reads, then re-query every required baseline and in-window record from the live journal and compare the archive. |
| Result decision | About 2 hours in the overall test schedule | Reconcile producer schedules, direct queries, archive contents and lifecycle evidence; record separate delivery, retention, collection and overall journal results. |

The separate ETL work retains its approximately three-hour functional-check allocation. ETL success is not a prerequisite for journal preparation, start, continuation or completion. Each observation has its own start, elapsed clocks, evidence and verdict. The approximately two-hour decision period is the overall schedule allocation, not two additional hours per issue.

The approximately one-hour stage is a basic functionality check, not a substitute for the full day or proof that every lifecycle scenario will finish within one hour. Include all seven required scenarios below in the execution schedule, keeping deliberate loss and restart separate from the positive 24-hour observation. Record actual setup, action, query, observation and final-check durations and report schedule conflicts before execution; never remove a stage or shorten the required observation to fit an estimate.

##### Appliance Request And Logging Contract

Before the observation start, specify the actual retrieval endpoint, registered fixture PVs, explicit time ranges, expected application message templates and correlation fields for the installed source version. Give each request an independent producer ID and a distinct PV/time-range tuple that can be matched to the application's own messages. A producer-only marker does not establish application logging.

Configure the dedicated deployment's actual `DataRetrievalServlet` logger at DEBUG, retain stdout through the real appliance-to-journald path, and verify the effective logger, appender and journal-priority filtering. Normal request diagnostics in the pinned source are DEBUG while the default root level is INFO. HTTP success alone therefore proves no application-log emission. Define the required message set for each actual request outcome in advance; do not assume one request equals one journal record.

During the basic check, execute the selected real requests and directly confirm every required application message with matching PV/time-range fields, source identity and logger/thread context where needed. Freeze the observed source fields, message format and matching rule. An access-log file or synthetic system marker cannot replace this application-journal path. Ambiguous matching, missing required messages and query errors remain failed or unresolved.

Retain planned/actual execution times, the exact request, HTTP outcome, expected messages and actual direct queries. Record action execution, evidence of application emission, journal visibility and collector preservation separately. Actual application error records may satisfy the predefined logging contract even when ETL processing is incorrect. Missing execution or emission evidence cannot be relabeled as successful delivery or hidden by changing the expected message set after the action.

##### Measurement And Independent Verdict

Before each scenario, record the question, required paths/events, generation and direct-read schedule, collection boundaries, lifecycle actions and expected live-journal/archive result at each checkpoint. Identify the scenario's required record set independently; for deliberate loss, also declare the exact IDs expected to become unavailable before the removal action. Keep an independent producer ledger with unique IDs, sequence, expected payload, planned/actual emission time and outcome. Never construct expected IDs from collector output.

For the positive full-day observation, emit and directly confirm baseline records on every required path before setting `t0`. Preserve each record's initial confirmation time, identity and content. Continue scheduled real actions and collection for at least 86400 elapsed seconds after `t0`, measured in UTC and monotonic time within the same boot. Keep initial direct-query results for all required events and execute the intermediate direct reads scheduled before the run. Other scenarios use their own declared checkpoints and expectations; deliberate loss and restart do not replace or alter this positive observation.

At the positive full-day observation's final checkpoint, directly query the running deployment's live journal for every required baseline and in-window record and compare expected identity/content. Every baseline must remain readable at least 86400 seconds after its initial direct confirmation. Later records must survive through the final read with their actual younger ages reported; they are not 24-hour-old records. An archive copy is never a substitute for a final live-journal read.

Retain first visibility, journal timestamp/cursor, boot/source identity, UTC/monotonic query times, actual command outcome and timeout/error independently of collector output. First-observed delay is an observed bound, not the exact instant of durable storage. A timeout or query error is unresolved, not Passed.

For the positive observation and the normal delivery, rotation, quiet-interval, obsolete-anchor, restart and final collection checks, independently compare all required journal records with the combined collector archive using identity and payload, not totals alone. Preserve boot, source and cursor identities, deduplicate intentional query overlap and require each record exactly once in the check's combined archive across its collection, rotation, restart and final collection boundaries. Report missing, repeated or changed identities explicitly. Separate failure-termination checks retain their failed result and follow their predeclared lifecycle expectations. Keep raw queries, producer evidence, collector records, command outcomes, hashes and real journal-file copies where required for replay.

For deliberate loss, preserve the original required record set and the predeclared expected missing IDs. Confirm those IDs are initially readable and uncollected, then establish their actual absence from the live journal and collector archive after the specified removal. Successful direct queries must support the absence claim; a query error alone is not loss evidence. The checker must report exactly the expected missing IDs and refuse complete coverage, while other required records remain present with matching identity/content and are archived exactly once. Do not require the deliberately lost records to appear in the archive, remove them from the original required set, or mark the affected retention/coverage result Passed.

For each scenario and logging path, report the purpose, planned/actual actions and times, emission evidence, initial/later visibility, actual record ages, archive comparison and verdict. A zero-event interval needs independent evidence that no required event was emitted. A confirmed violation is Failed; missing or unresolved required evidence is Incomplete; an expectation supported by complete evidence is Passed. In deliberate loss, exact expected-loss detection and refusal of complete coverage can make the checker expectation Passed; confirmed retention/collection violations remain Failed, and unresolved evidence remains Incomplete. Keep the positive observation verdict separate from negative checker results. Scenario completion requires each scenario's predeclared expectation, not preservation of records that the negative action deliberately made unavailable. Unexpected loss or missing evidence cannot satisfy the negative checker expectation.

##### Completion Criteria

- [x] The package installs, runs and completes independently of ETL acceptance tools, records, services, changes and result. A failed ETL test does not fail the journal test when all journal requirements are satisfied.
- [x] The one-hour basic check and positive full-day observation are separate. Actual elapsed durations were 3660.861488975 and 86477.42785609 monotonic seconds. The planned approximately two-hour result-decision allocation was exceeded: recording ended on 2026-10-14 UTC and complete corrected reconciliation finished on 2026-10-15 UTC. Finalization and source-matching defects did not invalidate preserved records.
- [x] The 903-PV fixture and configured source frequencies are recorded. System records occur every second, actual kernel-path records every 10 seconds, actual retrieval actions every second and real health executions every minute under the frozen positive schedule. Every required planned action is reconciled with independent producer evidence; failed, skipped or unresolved actions cannot disappear from the verdict. Observed full-day actions all reconciled: system 86400, kernel 8640, appliance retrieval 86400 and health 1440.
- [x] All four logging paths have actual emission/source evidence and successful initial direct reads with matching identity and content. Appliance requests correlate unambiguously to the actual application's required messages through its verified DEBUG/stdout-to-journald path; HTTP success or a synthetic marker alone is insufficient.
- [x] The positive observation runs for at least 86400 seconds in UTC and monotonic time within one boot after all required baselines are directly confirmed. Early stop, restart or a partial run does not satisfy this criterion. Observed elapsed time was 86477.42785609 monotonic seconds and 86477.427848 UTC seconds.
- [x] In the positive full-day observation, every baseline record is present with matching content in the final live journal at least 86400 seconds after initial direct confirmation. Every required in-window record has initial, applicable intermediate and final direct reads and survives to the final read with its actual age reported. Complete original-record comparison Passed with zero violations and zero unresolved items.
- [x] For the positive observation and normal delivery, rotation, quiet-interval, obsolete-anchor, restart and final collection checks, each check's combined collector archive contains every required record exactly once with matching identity/content across its collection, rotation, restart and final collection boundaries. Overlap is accounted for by cursor, boot and source identity; missing, repeated and changed IDs are explicit. Deliberate-loss and failure-termination checks follow their separate negative/lifecycle expectations; their failed retention/collection or terminal result cannot be relabeled Passed to satisfy this complete-archive criterion.
- [x] All seven scenarios meet their predeclared expectations. Quiet intervals and obsolete anchors cause no false loss. Deliberate loss proves actual absence of the predeclared required uncollected IDs, reports exactly the expected missing IDs and refuses complete coverage; other required records remain correctly retained/archived. Its checker expectation is Passed only with complete supporting evidence, while confirmed retention/collection violations remain Failed and unresolved evidence remains Incomplete. Expected negative results satisfy that scenario's completion criterion; they do not weaken positive preservation acceptance. Unproved boundaries cannot produce complete coverage. The current failure-termination/repeated-finish scenario excludes normal-stop/post-stop checks transferred to M27 under D28.
- [x] The completed full-day final collection and separate-process frozen CLI on the same deployment reproduced the complete Passed result and per-record comparisons exactly. Actual failure termination preserved its Failed result and repeated finish refused another stop without modifying evidence. Unexecuted normal-stop/post-stop verification and independent-recipient full-day replay are transferred to M27/M28, not claimed as Passed.
- [x] No inherited artificial size cap, capacity forecast, safety multiplier or calculated retention horizon is a readiness or success condition. Effective settings, real query/service outcomes, timeouts and errors are retained.
- [x] Complete per-path results and per-record comparisons reproduce through the exact frozen corrected tools on the recording deployment, with every original file and earlier unsuccessful result preserved. Reusable source/procedures are under tests/archiver-soak/journal-validation; raw records and deployment configuration remain private. Independent-recipient full-day acceptance belongs to M28. Conclusions are limited to the tested paths, load, actions and duration; ETL acceptance is separate.

##### Dependencies And Decisions

- D28 transfers the two unexecuted tool checks to independent M27/M28 Backlog work; neither is a dependency of M25 completion.

- D27 owns separation and supersedes the historical budget prerequisites and formula choice. No M22 merge, preparation, observation, result or completion is required.
- 2026-10-13: the owner restated the original time allocation and directed separate ETL and journal plans. M25 owns the approximately one-hour basic journal check, its independent full-day observation and its verdict within the overall two-hour decision period.
- 2026-10-13: ETL processing failure may produce legitimate journal inputs. M25 judges recording, later live visibility and archive equality independently of M22 functionality.
- 2026-10-13: positive preservation/archive equality and negative checker expectations have separate completion rules. Deliberate loss requires predeclared missing IDs, observed absence, exact detection and refusal of complete coverage; confirmed retention/collection failures remain Failed. Expected negative results satisfy only their own scenario, while the positive full-day criteria remain mandatory. This authorizes document correction only; implementation remains paused.
- Decision Date: 2026-10-13. The owner directed proceeding with issue #31 independent execution preparation after the accepted document corrections and reader recheck. This authorizes the independent package and basic-check tools under Ordered Work 1 and 2. A dedicated journal deployment is required for runtime verification; the retained ETL guests are outside this preparation. M22 implementation remains paused.
- Decision Date: 2026-10-13. The owner directed starting the next step after local preparation: prepare one fresh dedicated journal deployment and execute the approximately one-hour T1 basic check with the accepted signals, frequencies and independent verdicts. The owner separately authorized sending its VM creation request to the confirmed provider. This does not authorize the full-day observation, deliberate loss, restart scenarios or changes to retained ETL deployments.
- Decision Date: 2026-10-13. After the real health source mismatch was identified, the owner chose to stop the current basic run, preserve its Incomplete result and original evidence, verify the correction and start a fresh one-hour check. Keep the accepted signals, frequencies and duration; do not reinterpret the interrupted run as successful or replace its original tools/result.
- Decision Date: 2026-10-13. After the Passed one-hour basic result and pending independent full-day/lifecycle requirements were summarized, the owner directed proceeding. Continue the accepted journal plan independently on its dedicated deployment. Preserve prior runs and original results; declare baseline, direct-read, collection and lifecycle expectations before each action, and keep destructive-loss/restart scenarios separate from the positive full-day observation.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: scope revised and explicitly accepted on 2026-10-15 under D28; original acceptance: 2026-10-13; the owner directed proceeding with issue #31 after the accepted corrections and completed reader recheck.
- Implementation Authorization: 2026-10-15; Backlog separation, reusable source preservation, #31 evidence comment and closure are directed; no new 24-hour run. Original execution authorization: 2026-10-13; Ordered Work 1 and 2 covered independent package/basic tools and the dedicated one-hour T1 check. At 21:20 UTC, the owner directed proceeding with the summarized remaining verification, extending execution to Ordered Work 3 to 5: independent full-day retention, the separate predeclared lifecycle/negative scenarios and evidence reconciliation. Preserve originals, verify real-path readiness and confirm every required baseline before full-day t0. Deliberate loss and restart must not interrupt the positive same-boot observation. No ETL deployment changes or git/GitHub mutations are included.
- Superseded Plan Artifacts: the earlier current-plan text without the original basic-check and overall decision time allocations; historical plans/results below retain their original scope.

1. Extract the independent package from the immutable baseline with only its generation, collection, direct-query, comparison and lifecycle dependencies. Give it its own installation, fixture/lifecycle handling, evidence, locks and units. No ETL acceptance tools or journal-budget proof is required.
2. Provide independent producer ledgers and real triggers for all four logging paths at the specified frequencies. Establish the actual DEBUG application path, request/message correlation and effective source/configuration identity during the approximately one-hour basic check. Confirm baseline records before the full-day start.
3. Execute the seven scenarios through the actual target journald/journalctl and shipped collector, preserving planned/actual schedules, producer outcomes, raw direct queries and interval boundaries. Apply complete preservation/archive equality to the positive observation and normal preservation checks; apply actual-absence, exact missing-ID detection and refusal of complete coverage to deliberate loss, retaining the failed retention/collection result separately. Failure-termination checks preserve failure under their own lifecycle expectations. Keep positive retention separate from deliberate loss, restart and failure termination. Record actual durations and errors instead of storage forecasts.
4. Correct reproduced collector defects against retained real inputs and rerun affected scenarios through the shipped path. No stub, internal-function replacement or reconstructed intermediate fixture establishes integration acceptance. Preserve every unsuccessful run and its original result.
5. Complete the positive observation's at least 86400 seconds within one boot, final live reads of all its required records, complete archive comparison and same-deployment frozen replay. During the approximately two-hour overall decision period, produce the independent per-path/per-scenario results and a sanitized evidence package with frozen replay tools. Report negative checker expectations and their retained failure evidence separately from positive preservation acceptance. No journal result starts, stops, restarts or invalidates an ETL observation.

##### Test Plan

| Label | Scenario and purpose | Real action and required result |
| --- | --- | --- |
| T1 | Initial delivery | Trigger actual system/kernel/appliance/health events. Reconcile all scheduled actions and match each required emission to direct journal identity, content and source; preserve first-visibility times and collector comparison. |
| T2 | Full-day live retention | Re-query baseline and later records at planned intermediate checkpoints and after the full day. Every baseline survives at least 86400 seconds after initial confirmation; every required in-window record survives to the final live read with its actual age; archive identity/content matches exactly. |
| T3 | Rotation and concurrent collection | Emit before/during/after actual rotation, including rotation during collection. Required records remain readable and archived exactly once. Explicit rotation exercises the case without an artificial cap or an indefinite wait for natural rotation. |
| T4 | Quiet intervals and obsolete anchors | Use an explicitly scheduled quiet-kernel interval while other logging continues; separately make only a pre-window anchor unavailable while retaining all required records. Proven boundaries and required IDs remain valid; absence of events is not confused with loss, and unproved boundaries are not accepted. |
| T5 | Deliberate required-record loss | In a separate negative scenario, preserve evidence and declare the exact expected missing IDs before removing a journal file known to contain those required uncollected events. Direct queries establish actual absence; comparison reports exactly those missing IDs and refuses complete coverage, while other required records remain correctly retained/archived. The checker expectation may pass; the observed retention/collection failure remains recorded. |
| T6 | Boundaries and restart | Place actual events across adjacent collection cutoffs and a real dedicated-system restart; include UTC midnight when claimed. No omission or duplication; boot identities remain distinct; unproved continuity stays unresolved. Keep this separate from the same-boot positive observation. |
| T7 | Failure termination and repeated finish | Actual collector failure preserves the failed original, reconciles executed/cancelled actions, resumes ordinary collection from its checkpoint and stops once. Repeated finish refuses a second stop and leaves original evidence unchanged. Normal-stop/post-stop and independent-recipient full-day acceptance are M27/M28. |

##### Verification Results

Dedicated deployment preparation, three short real probes and an owner-interrupted
basic run have run. The fresh 3600-second T1 basic check completed delivery, later
live reading and collector comparison with Passed one-hour acceptance. Its exact
saved result was reproduced with the same frozen CLI on the guest and after retrieval
on the control host. The positive full-day observation completed its recording and
collection window, but final artifact-index serialization raised MemoryError before
record comparison and result publication. Recovery completed on a separate evidence copy
with unchanged frozen comparison code and exactly repeated its Incomplete verdict.
Six health completion markers were present unchanged in direct queries, the final query
and native archives, but the matcher rejected their absent journal invocation metadata.
The corrected shipped package then completed full-day record verification and exact
same-guest frozen CLI replay with Passed on the unchanged original inputs. The
original frozen Incomplete result remains preserved separately. Eight additional lifecycle/negative checks
have since completed their declared expectations and exact recipient frozen replay;
normal terminal/post-stop capture and independent-recipient full-day replay are transferred to M27/M28 without a Passed claim under D28.
The interrupted original remains Incomplete.

The independent package and basic-check tools are implemented under Ordered Work 1
and 2. `prepare.py` builds from immutable source objects and stages installation without
starting services; `basic.py` freezes producer schedules, performs actual inputs/direct
queries/collection, and replays saved evidence on the dedicated deployment. Local checks
use the real package CLIs and fixtures, plus the
real HTTP helper with only its outer HTTP boundary supplied by a local server. No
internal substitute or reconstructed journal fixture establishes runtime acceptance.

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Scope acceptance and closure | 2026-10-15T08:24:40.023070+00:00 | Actual GitHub issue read-back; local Git tracking and package build/install | Complete for accepted journal measurement | #31 closed completed; exact published body SHA256 689026100ae50e81f68885bed9e3c7cf136f24bb3cf12b37eb89ab1635352414 and exact evidence/separation comment SHA256 7bc7d5545aeef6cd0e852cd08838d225b78e3f3cc5ad78c9d78fc73b9a9288d2. Unexecuted normal-stop/post-stop verification and independent-recipient replay remain separate open Backlog issues #32/#33. The reusable health regression CLI is Git-tracked and included in the built package; 19 actual local preparation checks Passed. No new full-day run was started and no completed observation was modified. |
| T2/T7 corrected complete full-day record replay | 2026-10-15T07:36:12.853718+00:00 | Same completed positive observation; separate evidence copy and explicitly frozen corrected shipped package | Full-day delivery, preservation, collection and same-guest frozen replay Passed; M25 remains In progress | The actual full-day comparator and a separate-process frozen CLI both returned Passed with identical complete JSON results and exit status 0. Delivery, final live read, intermediate reads, baseline retention and archive comparison all Passed with zero violations and zero unresolved items. Actual confirmed action counts were system 86400, kernel 8640, appliance retrieval 86400 and health 1440; health retained both actual records for all 1440 actions, including the six previously misidentified completion markers. All 289 native collector intervals were checked. The original observation spanned 86477.42785609 monotonic seconds and 86477.427848 UTC seconds. The original code reproduced all six false negatives; the corrected direct and disk-backed matchers Passed 96 retained-record checks, including refusal of missing markers, conflicting or null invocation metadata, altered bodies, wrong primary PIDs, missing primary invocation identities and distinct duplicate markers. Nineteen actual local build/install checks Passed. The correction accepts absent journal invocation metadata only for an exact completion receipt with the required unit and stdout transport; actual health output still requires its main PID and journal invocation identity. Every raw input in the working copy matched the original. All 787482 original files, the original failed service and the earlier Incomplete result remained unchanged after both replays. Corrected package manifest SHA256 is 6ea4bb380f608d2ca3f29c4e08894fadfeca117ce4fda9b02949195615f49738; native result SHA256 is 29180cc344cfece38742841159a3663fe75be83a867f6e7939317c8ee4a12c23; per-record comparison SHA256 is 38a93a42991b163687a8041837ccf63f4c73817517e0b3a3e3d01cd12d3f4adb. Private verification receipt SHA256 is aabce1d92a8bfadab15636c538a9f1b7295f796364722552b707f1544c7e9c4b. Normal-stop/post-stop capture and independent-recipient acceptance remain separate outstanding requirements. |
| T2/T7 six unresolved health records, actual source inspection | 2026-10-15T06:33:46.557467+00:00 | Unchanged completed full-day evidence; real frozen matcher and read-only live journal | All six retained-record comparisons Passed; frozen matcher false negatives reproduced; original verdict remains Incomplete | All 1440 health commands exited 0. For sequences 356, 535, 787, 788, 1090 and 1382, the actual health message and exact completion marker were both present in original direct queries, the final live query and native archives; each complete record matched across those sources. Eligible intermediate checkpoints also retained those same records, and current live queries still returned all six actual health messages with exactly matching archived contents. Actual health messages retained the expected main PID, unit and journal invocation identity. Each completion marker retained the exact expected receipt JSON, including its action and invocation identity, and the expected stdout transport and unit, but lacked the separate journal _SYSTEMD_INVOCATION_ID field. The unchanged frozen matcher returned zero for all six because it required that journal metadata field and excluded the existing marker. This is an identification-condition defect, not missing or changed message content and not an unsuccessful health command. The previous full replay had no confirmed violations and six unresolved source sets; its Incomplete result, exact repeated CLI result and unchanged-original proof remain preserved. Diagnostic script SHA256 is 48fd528c2c58efa6ce4cf5939fa3beae48dcdddbe3c2021af0124597aecaef5a; structural evidence SHA256 is 5c9c111539c22bad7135986ae44f3509bbddbce0bf80d848b39f574f35387b8f. No acceptance condition or frozen input was changed. |
| T2 original full-day recording and finalization error | 2026-10-14T23:40:12.277304+00:00 | Original independent journal deployment; read-only frozen-code and retained-evidence inspection | Recording and collection complete; final decision Incomplete | The actual observation spanned 86477.42785609 monotonic seconds and 86477.427848 UTC seconds, with unchanged boot and journald identities. Actual completed actions were system 86400, appliance retrieval 86400, kernel 8640 and health 1440, with zero unsuccessful actions. All 289 retained collector intervals reported coverage_complete=True; three intermediate queries and the final live query were retained. The frozen driver then raised MemoryError at long.py line 503 through prepare.py line 36 while json.dumps serialized the complete artifact inventory of 787482 files. Artifact index, comparisons and result were not published; no journal failure verdict was produced. Original observation SHA256 is 561efb3603df111c07617724e68665bbfd594de62ee8426fed7b4e25dd9dc251; frozen long.py SHA256 is b5cef983d08696d4c0629479bb73931b93b0152d46360067428260d9eb46d97d. Raw-record equality and full-day acceptance remain unestablished. |
| T2/T7 full-day comparison recovery | 2026-10-14T23:59:22.856575+00:00 | Separate copy on the original journal deployment; original evidence and installed package protected by read-only paths | Actual full-size inventory serialization Passed; frozen record comparison Running; no recovered full-day verdict yet | The actual serialization fix writes JSON incrementally while preserving the existing format. Nineteen actual local package checks Passed, including byte-exact serialization of the built immutable-source record. An independent copy-on-write evidence copy completed without errors. The unchanged frozen inventory function hashed all 787482 original files; the corrected shipped serializer successfully wrote the actual 131550335-byte inventory outside the original evidence. The preservation index and copied-evidence artifact index had identical SHA256 9a748277938a80f02fce3a9181f08f7fde0968d369d68e4eb79f5972936edd27. The unchanged frozen full-day comparator is now running; the scheduled recovery then repeats the actual frozen CLI in a separate process and verifies every original file and the original failed service remain unchanged. Serialization source SHA256 is 5a714055eae9f4845c4ced875a7679633fe51987851c9465309bc1245d668f86; recovery driver SHA256 is 4eb467b83812c6d9155d4de5c6e2c3cc93f98154931aaab4e69d3434c33f5888. Original recording is not restarted and ETL deployments are not used. Normal-stop/post-stop capture and independent-recipient acceptance remain separate outstanding requirements. |
| T2 original positive full-day progress | 2026-10-14T20:01:20Z | Original independent same-run journal worker; read-only service and actual producer/collector record inspection | Running; full-day acceptance Pending | The actual worker process was present and Running. Independent completed-action counts were system 79022, appliance retrieval 79022, kernel 7903 and health 1318, with zero unsuccessful completed actions. There were 263 completed native collector intervals and three intermediate checkpoint files. These observed counts are not nominal-rate estimates; checkpoint-file presence alone is not a complete checkpoint verdict. Final live retention, archive comparison, normal stop, post-stop collection and recipient replay remain unaccepted. |
| T1 preparation only | 2026-10-13 11:04:41 UTC | Local source objects, fresh temporary staging roots and actual current-host preflight; PID 1 is not systemd and systemd/journalctl are not version 239 | 18 local preparation checks Passed; actual T1 Pending | `tests/archiver-soak/journal-validation/check-local.py` exercised build/verify/install, immutable dependency equality, private state and unit separation, conflict/tamper/configuration refusals before mutation, HTTP 200/500 receipts, and read-only refusal of absent replay evidence. Current-host readiness was false. Original receipts, frozen package and the unsuccessful initial help check are retained under `work/journal-preparation-20261013T110441Z/`; `verification.json` SHA256 `33f0d2c84880623362b7700bfb49ab79931de2eaf86baeddfa84a4245edbf27e`, package manifest SHA256 `6c2243c0f4a2647685a9067b08536d11dbb90845907d175a5c9c6d6271c754bb`. No live logging-path or shipped-collector execution is claimed. |
| T1 deployment readiness | 2026-10-13 16:37:24 UTC | Fresh dedicated Rocky 8.10 deployment; Python 3.9.25; systemd/journalctl 239 | All actual readiness checks Passed; T1 acceptance Pending | The frozen baseline playbook completed successfully. The actual appliance, private fixture IOC, retrieval logging environment, persistent current-boot journal, writable kernel path and all 903 registered fixture PVs were verified. Appliance environment source `482cf2939ea997064e4a2df64e3cb420681f4566`, appliance source `162269e7db97f527626ba0b387933a8c47e8bb57`; deployed retrieval class SHA256 `1f5623bc8b41171b5d06f21593e74a2af983a35e8cb99b2a30e8dfc8bc4981d2`. Private deployment receipts retain actual connection, versions, configuration, build stamp and service identities. |
| T1 short probe, original | 2026-10-13 16:25:38 UTC | Actual dedicated appliance, journalctl 239 and unchanged shipped collector; 60 scheduled seconds | Failed; retained unchanged | The filtered `--after-cursor` query omitted the first matching kernel record, although an independent unfiltered live query later found all six exact kernel records. Health returned status 0 with both required source messages, but post-completion unit inspection had lost its execution properties. The collector's first query rejected the caller's ISO UTC timestamp. The original result remains Failed, with later reading and collection Incomplete; result SHA256 `54548ec82c1f4029a258ec3dcb8acd49a6375ceef6448c254d2039b5b8f2b7bd`. No actual journal loss is inferred from these checker defects. |
| T1 short probe, corrected | 2026-10-13 16:39:36 UTC | Same actual dedicated deployment and unchanged shipped collector; 60 scheduled seconds, 120.204229718 actual elapsed seconds including finalization | Delivery, later live reading, collection and probe overall Passed; one-hour acceptance Incomplete; full-day Pending | Independent producer/direct-query evidence confirmed system 60/60, kernel 6/6, retrieval 60/60 with 120 required application messages, and health 1/1 with two required messages. No scheduled action was skipped or unresolved. The saved frozen CLI replay reproduced the exact result before the one-hour start. Result SHA256 `58931f5a00569ec6973ced748fd0511dd171bc250e298bfc9db79b0542e8e88c`; package manifest SHA256 `f6cce062d8ff4900632e6cb2fdd5ebf855f6463422ca07680979a5a5b6f50454`. The original and corrected probe evidence was retrieved to private `work/journal-basic-20261013/preparation-evidence.tar`, with matching guest/local SHA256 `01930d7ebade33d8f157bf1a347aae598bf2048258b41dbddb893fca864bd381`. |
| T1 first one-hour check, initial observation | 2026-10-13 16:41:30 UTC | Actual dedicated appliance, private IOC, journalctl 239 and unchanged shipped collector | Running at this observation; subsequently interrupted as recorded below | The start was 16:39:58.573731 UTC, with a frozen 3600-second schedule. At this observation, the real process was present; system 92, kernel 10, retrieval 92 and health 2 completed actions had matching source messages. Frozen schedule SHA256 `a9190d834135c26a97109d53f7cef5482a56537020877d639854aaca640bbda8`. These partial observations did not establish a completed verdict. |
| T1 first one-hour check, owner interruption | 2026-10-13 16:51:37 UTC | Same actual deployment; original tools and evidence retained | Incomplete; stopped by owner direction | The original observation ended after 699.214164771 measured seconds. Its frozen checker confirmed system 699, kernel 70, retrieval 699 and health 11; health had 12 actual executions. One terminal message matched the actual invocation and main PID but its recorded process name did not satisfy the checker's fixed `bash` condition. The owner directed interruption and a fresh corrected one-hour run. Original delivery, later live reading, collection and overall results remain Incomplete; result SHA256 `e0d33a47fab30ad4451147a757645f021487ed6907d8e6f2231c77386351bad9`. No boot, appliance or fixture restart was performed for this correction. |
| T1 health source correction | 2026-10-13 16:54:19 UTC | Original retained real producer/direct-query evidence; actual shipped source comparison and current deployment preflight | Real-record regression and readiness Passed; interrupted replay remains Incomplete | The original predicate found zero required records for the affected health action; the corrected predicate found both unchanged required messages by actual main PID, service, transport and invocation. All 12 retained real health executions matched both required messages under the corrected source rule. No internal substitute or reconstructed journal record was used. The corrected CLI replay still refused acceptance of the interrupted schedule. Local package preparation checks also passed, and the installed package manifest is `5a68cfb0e7ff8552c3186dc218b7d7f4e6b21b3aa30ee076eb430818b68164ef`. Original package and result were preserved before installation. |
| T1 short probe after health correction | 2026-10-13 16:57:14 UTC | Actual dedicated appliance, journalctl 239 and unchanged shipped collector; 60 scheduled seconds, 120.119605249 measured elapsed seconds | Delivery, later live reading, collection and probe overall Passed; one-hour Incomplete; full-day Pending | System 60/60, kernel 6/6, retrieval 60/60 with 120 required messages and health 1/1 with two required messages matched the independent producer/direct-query evidence. Final live reading, collector comparison and frozen CLI replay passed. Result SHA256 `9e4ffbd206ca078cef3c764325c9537ea066bd1f4e170b1a1a5f74a1d580363a`. Completed probes, the interrupted original and correction evidence were retrieved to private `work/journal-basic-20261013/interruption-evidence.tar`; matching guest/local SHA256 `42fac41314a9047e4b5dd1fc02964652e02970b6c963ff23f3b6ff9f6af82f37`. |
| T1 retrieved frozen evidence replay | 2026-10-13 17:02:36 UTC | Local recipient-side extraction of the hash-verified original evidence archive; each run's own frozen replay CLI | Exact saved results reproduced | The latest health-corrected short probe reproduced Passed with exit 0; the original interrupted one-hour run reproduced Incomplete with exit 1. Both complete JSON results exactly matched their saved originals. No runtime service or journal was substituted, and the original evidence was not edited. Private replay receipts are under `work/journal-basic-20261013/local-replay-*` and `local-frozen-replay.json`. |
| T1 fresh one-hour basic check | 2026-10-13 17:58:53 UTC | Actual dedicated appliance, private IOC, journalctl 239 and unchanged shipped collector | Delivery, later live reading, collection, overall and one-hour acceptance Passed; full-day Pending | The fresh start was 16:57:52.576315 UTC; 3600 scheduled seconds ended at 17:57:52.576315 UTC. Final visibility wait, live query and collection completed at 17:58:53.437811 UTC; actual elapsed time was 3660.861488975 monotonic seconds and 3660.861496 UTC seconds. Every required action was executed and directly confirmed: system 3600, kernel 360, actual retrieval 3600 with 7200 required messages, and health 60 with 120 required messages. No skipped or unresolved actions, direct-query errors or collection errors were observed; all 13 native collection intervals had complete coverage. Frozen schedule SHA256 `1a15a3fd3f19d9faa52fe9eeb71a0cd0eef8007d77561c37e28670b782a8cf6d`; result SHA256 `058251fe4bacb4719b11d8f96e5ce746b0feea46dc151d893a077ee056a0c96c`; package manifest SHA256 `5a68cfb0e7ff8552c3186dc218b7d7f4e6b21b3aa30ee076eb430818b68164ef`. Original interrupted evidence is unchanged. |
| T1 complete retrieved evidence replay | 2026-10-13 18:03:17 UTC | Original private archive and the completed run's own frozen replay CLI | Exact Passed result reproduced on guest and local recipient | Guest/local archive size and SHA256 matched: 257177600 bytes, `e8dcb796968bfd34e26699b248063a879cd18a0483b87b9921c3301a48b22f4d`. Replay exited 0 and its complete JSON exactly matched the saved original. Evidence is private `work/journal-basic-20261013/basic-002-evidence.tar`, with receipt `basic-002-local-replay.json`. The real producer, direct queries and native collector inputs were retained; no internal substitute or reconstructed journal fixture was used. |
| T2 long-path readiness probe | 2026-10-13 22:01:27 UTC | Actual dedicated appliance, journalctl 239 and unchanged native collector; 120 scheduled seconds | All positive probe components Passed; full-day Pending | Baselines on all four paths were directly confirmed before probe t0 at 21:58:27.418429 UTC. Actual elapsed time was 180.209894238 seconds including final visibility/query/collection. System 120, kernel 12, actual retrieval 120 with 240 required messages and health two with four required messages all matched their independent actions; each baseline path also matched its original confirmation. Both intermediate queries, final live read and native collection matched by identity/content. Result SHA256 `ddfe2ca93632e3d8ae2cffc0df2cfd51153c66b16b5aeb65451c6dd717a1c50e`; package manifest SHA256 `67febb2463996fbf9a4172b95b350398ef3d29e268bd92922632765618dddf8f`. The native collector and basic producer code remain byte-identical to their preserved sources. |
| T2 frozen replay and consumer check | 2026-10-13 22:02:22 to 22:20:39 UTC | Original real probe evidence and its own frozen CLI; separate filesystem-boundary derivative | Exact positive and negative verdicts reproduced on guest and local recipient | The unchanged original replay reproduced Passed. Removing one already-confirmed kernel baseline record only from a separate final-query input made the real checker report exactly that missing action: live reading and baseline retention Failed, delivery/collection Passed and overall Failed. Full-day stayed Pending. This is retained-input filesystem testing, not actual journal-file loss and not T5 acceptance. Guest/local archive SHA256 matched `7c7c88898db4fd9811608f23a3be86772beb2c0d135026151a5bb5c7b5ab9ee9`, 21032960 bytes. Local frozen CLI results exactly matched both saved guest results. Private archive and receipt: `work/journal-basic-20261013/long-probe-001-evidence.tar` and `long-probe-local-replay-001.json`. |
| T2 positive full-day observation | 2026-10-13 22:04:17 UTC; progress checked at 22:11:14 UTC | Same dedicated journal deployment; actual independent producers/direct reader/native collector | Running; full-day acceptance Pending | All four baseline paths were emitted and directly confirmed before t0 at 22:04:17.803792 UTC, monotonic `24169290936336` ns. The frozen 86400-second schedule retains system/retrieval every second, kernel every ten seconds and health every minute, direct reads every second, collection every 300 seconds and intermediate live queries at 21600/43200/64800 seconds. Planned recording end is 2026-10-14 22:04:17.803792 UTC, followed by final verification. Contract SHA256 `84477e2b778111571d8581de1e5c2280b7e6a3a9b19d69ec8af7e4db05ff81b4`. At the progress check, the actual process was present, completed outcomes were system 417, kernel 42, retrieval 417 and health seven, with zero unsuccessful outcomes and one completed native collector interval. These are actual ledger counts, not rate-times-duration estimates, and they do not establish full-day preservation. No ETL result or forecast was a start condition. |
| T2 positive full-day progress | 2026-10-14 02:47:05 UTC | Actual independent producers/direct reader/native collector; original same-boot full-day process | Running; full-day acceptance Pending | The actual process was present. Independent ledgers contained 16967 system actions, 1697 kernel actions, 16967 appliance retrieval actions and 283 health actions, with zero unsuccessful completed outcomes and 56 completed native collector intervals. These are observed counts. No intermediate six-hour checkpoint was due yet. Original t0, frozen contract, signals and final live-read requirement remain unchanged. Private `long-full-progress-003.*` receipts and `monitor-long-probe-001.py` retain and recheck this observation. |
| T4 quiet interval | 2026-10-14T09:59:30.561126+00:00 | Separate dedicated Rocky 8.10 guest; actual journalctl 239, producer and frozen collector/replay paths | Passed | A full 1200-second schedule retained zero kernel records in the declared quiet interval and complete identity/content equality for every required record. Exact guest/recipient replay and archive hashes matched. Result SHA256 `1406816f692e7e1d2bd472c2f78b31749befbcd7501883727a21b53f8f7ce097`; archive SHA256 `ba952114c0b056c764c704bc9313ae7cf9796b1b54985b0a9a1bfba5189e6268`. |
| T3 rotation outside collection | 2026-10-14T10:44:49.404352+00:00 | Separate dedicated Rocky 8.10 guest; actual journalctl 239, producer and frozen collector/replay paths | Passed | Actual rotation between completed native collections preserved every required record exactly once through the full 900-second schedule. Exact guest/recipient replay and archive hashes matched. Result SHA256 `1ef979ba9d0c27d825703f9d2bddbf6381a2c811624e2198febd0869cfb255a6`; archive SHA256 `465a0b9db2560c66ea3089972bd97585833800f71e474b819e17169e1576e24d`. |
| T3 rotation during collection | 2026-10-14T12:02:28.452455+00:00 | Separate dedicated Rocky 8.10 guest; actual journalctl 239, producer and frozen collector/replay paths | Passed | Actual rotation overlapped a real native query during the full 1200-second schedule; required records remained live and archived exactly once. Exact guest/recipient replay and archive hashes matched. Result SHA256 `c32724fc72f686116a7f76349ad8812ff9fe9765274bd0cf849d62d09c9099a3`; archive SHA256 `e22250870ccf20670a7fa5d25dda24f149b0d5ff7a66b3eb7839001188b384c9`. |
| T4 obsolete anchor | 2026-10-14T14:09:05.207257+00:00 | Separate dedicated Rocky 8.10 guest; actual journalctl 239, producer and frozen collector/replay paths | Passed | Only the pre-window anchor became unavailable. All 3766 required records remained live and archived; all five native intervals proved required-window coverage with the original checkpoint retained. Exact guest/recipient replay and archive hashes matched. Result SHA256 `e7aaea0ec61737c853f169bf1adff612b9e5a71f49d71bb8ecd3a017f9348c87`; archive SHA256 `a554b6550230e9f4e928763dec350efd1fe3da053a1000641721b83cc83a8392`. |
| T6 adjacent boundaries and reboot | 2026-10-14T15:51:29.977859+00:00 | Separate dedicated Rocky 8.10 guest; actual journalctl 239, producer and frozen collector/replay paths | Passed | Two complete 300-second segments across one actual normal reboot preserved all 1898 required records exactly once across two boot identities. Whole-case and both child frozen replays were exact; no UTC-midnight coverage is claimed. Exact guest/recipient replay and archive hashes matched. Result SHA256 `0f8f692088f43e74946aea3910b5690611bc24b00cbfa7aa9c390066a9213199`; archive SHA256 `8ebd1519fd4fd51740ffec691a3d13a492535cc5c017be0c951ed934f7cf3e3f`. |
| T7 failure termination | 2026-10-14T16:12:56.472483+00:00 | Separate dedicated Rocky 8.10 guest; actual journalctl 239, producer and frozen collector/replay paths | Expectation Passed; original Failed | The real collector CLI failed with a read-only filesystem error. The driver retained its checkpoint, reconciled 1274 executed and 631 cancelled actions, recovered ordinary collection from that checkpoint and dispatched one stop. Negative frozen replay was exact; the original failed observation was not changed. Exact guest/recipient replay and archive hashes matched. Result SHA256 `02369c61eb045c596376650ff82eaedef69d093990a4d2a6447fadac5f951a64`; archive SHA256 `d62779d2e2114791f327315c7317a984fc21289e80e16d91d314375b767caaf3`. |
| T5 actual required loss | 2026-10-14T17:27:33.430596+00:00 | Separate dedicated Rocky 8.10 guest; actual journalctl 239, producer and frozen collector/replay paths | Detection expectation Passed; original Failed | The predeclared 385 missing IDs among 2826 required records were exactly absent after actual file removal; the other 2441 remained live and archived once. Four native intervals refused complete coverage. Overall/retention/collection remain Failed with no unresolved detection evidence. Exact guest/recipient replay and archive hashes matched. Result SHA256 `19a88730b5c8e5bb332e99733fd3ec1732bcfd4c75a965e49c9dde46fb7bbeee`; archive SHA256 `7f1c2cccea56cba9845b0c9f2077f02ed0736d8630f6b3f443d509ea5c77551f`. |
| T7 repeated finish | 2026-10-14T16:13:59.178424Z | Real frozen terminal CLI and retained failed original; recipient filesystem-isolated replay | Passed | Return code 2 refused repetition, all 5873 original file hashes remained unchanged and no second stop was dispatched. Recipient execution reproduced the refusal and original-file equality. |
| Backlog separation | 2026-10-15 | Explicit owner acceptance of completed journal measurement | Transferred; not run | D28 moves normal-stop/post-stop collector verification to M27 and independent-recipient full-day replay to M28. Neither is marked Passed; neither gates the accepted 24-hour recording/retention/collection result or requires a new 24-hour producer run. |

##### Closure Evidence

- Decision Date: 2026-10-15. The owner accepts the completed journal measurement and directs issue #31 closure after separating the two unexecuted tool checks into M27/M28. Delivery, baseline/in-window live retention, intermediate/final reads and exact archive comparison Passed with zero violations and zero unresolved records. The corrected frozen CLI reproduced the complete result exactly; all 787482 original files and the earlier Incomplete result remained unchanged.
- The one-hour basic check and eight additional lifecycle/negative expectations Passed within their declared scopes. Actual deliberate loss and failure observations retain Failed; the two transferred checks remain unexecuted rather than Passed.
- Reusable source and procedures remain under tests/archiver-soak/journal-validation. Actual package build/install checks Passed 19 checks at 2026-10-15T08:07:22.185028+00:00 after packaging the health regression CLI. Raw journals, deployment configuration and operational receipts are excluded. The current source-preservation changes are uncommitted; no new commit or upstream landing is claimed. Tracker closure accepts the measured journal result independently of that publication step.
- Tracker closure observed at 2026-10-15T08:24:40.023070+00:00: #31 is closed with completed reason, Closed At 2026-10-15T08:24:37Z. The applied body and evidence/separation comment match their prepared files exactly. https://github.com/jeonghanlee/ansible-provision/issues/31#issuecomment-6187790508 records the cause, actual measurements and independent #32/#33 follow-ups. Source preservation in Git-managed paths is verified; current commit/push publication remains separate and is not claimed completed.

##### GitHub Projection

- Issue: #31, https://github.com/jeonghanlee/ansible-provision/issues/31
- Title: `Verify journal delivery, retention and collection independently`
- Observed State: closed
- Close Reason: completed
- Closed At: 2026-10-15T08:24:37Z
- Labels: `enhancement`
- Milestone: `Backlog`
- Assignee: `jeonghanlee`
- GitHub Updated At: 2026-10-15T08:24:37Z
- Last Compared: 2026-10-15T08:24:40.023070+00:00; applied body and evidence/separation comment exactly matched the prepared files, intended metadata remained unchanged and completed closure was verified.
- Body: accepted journal measurement scope with all current required checks satisfied; published body SHA256 `689026100ae50e81f68885bed9e3c7cf136f24bb3cf12b37eb89ab1635352414`. Two unexecuted tool checks are explicitly transferred to independent #32/#33 Backlog work without a Passed claim.
- Prepared Body: 2026-10-15T08:20:48.265905+00:00; applied and read back exactly before closure.
- Applied Update: 2026-10-15T08:24:40.023070+00:00; scope body, evidence/separation comment and completed closure applied and verified. The source-preservation changes remain uncommitted; no source landing is inferred from tracker closure.
- Closure Comment: https://github.com/jeonghanlee/ansible-provision/issues/31#issuecomment-6187790508; SHA256 `7bc7d5545aeef6cd0e852cd08838d225b78e3f3cc5ad78c9d78fc73b9a9288d2`.
- Prior Applied Update: 2026-10-15T07:53:45.775714+00:00; original seven-main-test checklist had six completed; body SHA256 `33f8f07554b39a2596fd33c21cc231c66d1ff165e28c5d6d30277b4d376a714e`.
- Earlier Applied Update: 2026-10-14T19:55:12.567494+00:00; original seven-main-test checklist had five completed; body SHA256 `bb83ad41f9f3f58ea0926c4bb6041bc470dc06de12e0cae418ee60c976fa910f`.

<details>
<summary>Historical combined journal study and verification</summary>

The following original plan and results are historical. Its ETL dependencies, inherited
cap, budget formula, open budget decision and compressed rehearsal are superseded by D27.
They neither authorize current execution nor define current acceptance.

##### Summary

The ETL soak (`M22`) reads the appliance's journal every five minutes and
keeps it as evidence. This row verifies that this collection is complete and
affordable over a 24-hour window: that it keeps coverage when the kernel
cursor is lost or the interval is quiet, survives rotation and file removal,
detects loss of required records, and fits the journal cap that the archiver
host sets. The checks were T22-T28 of `M22`; they moved here so that a journal
check and the ETL scheduler verdict do not decide each other.

##### Scope

The shipped collector, journal coverage and retention-budget code and the
evaluator, exercised on the dedicated Rocky 8.10 test environment and on the
soak VMs through their preparation path. The accepted procedure sections of
`M22` (Journal Scenario Procedure And Start Gate, Dedicated Journal Test
Environment, Journal Scenario Procedure and Retention Accounting Correction)
are this row's procedure until they are moved. Added to the former checks is
T8, a compressed rehearsal of the full collection path under conditions that
make rotation and file removal frequent.

Out of scope: the ETL scheduler verdict of `M22`; changes to the journal cap,
the logging policy or the VM size, each an owner decision; systemd and
journalctl behavior, which is recorded in `M22`'s results (a systemd 239
`journalctl` hides stored entries that repeat the previous one).

##### Completion Criteria

- Each of T1-T8 passes in its stated environment through the shipped paths
  with only the external clock, filesystem and command boundaries substituted.
- The collector distinguishes removal of an obsolete pre-trial kernel anchor
  from loss of required, uncollected system records; quiet intervals,
  rotation, kernel-event delivery and final collection retain demonstrable
  coverage; unresolved gaps prevent Passed; system and user journal retention
  are checked separately.
- Over a 24-hour window on the 1-GiB journal cap, the retention budget either
  holds at every full collection or fails for a stated reason that the owner
  accepts; a failure produced by a file rename or by a measurement artifact is
  a defect of the checks, not a result.

##### Dependencies And Decisions

- `D22` (2026-10-05): this row, its separation from `M22` and the added T8.
- `M22` opens an observation after T27's preparation portion (T6 here) passes;
  it does not wait for the rest of this row.
- `D23` (2026-10-06): a failed in-window budget no longer aborts an observation
  or decides the `M22` verdict; `M25` owns it.
- Owner decision still open and not made here: whether the retention budget
  keeps counting the first allocation of a new journal file as a rate (the
  calculation then leaves a 3.5-percent margin after the first rotation).
- Decision (2026-10-11): the measured preparation on a fresh `M22` guest found
  the daemon start comparison of `journal_retention.py` using the whole-second
  boot time, which refused a configuration written in the same second as the
  daemon restart; corrected under plan item 4 as a newly frozen bundle with a
  regression that fails on the truncated computation (T6).

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-10-05; the owner accepted the plan with T8 in the form below
- Implementation Authorization: 2026-10-01 for the accepted journal-scenario plan transferred from `M22` (collector and budget code, local verification, the dedicated VM plan); 2026-10-05 for T8: acquiring one fresh VM, preparing and launching it through the shipped path and running the rehearsal on it
- Superseded Plan Artifacts: the earlier T8 text that reduced the journal file size, replaced on 2026-10-05 by forced rotation and removal

1. Run T8 first on one fresh VM, the shortened chain so that the 5-minute ETL
   grid and the sampler coincide, prepared and launched through the shipped
   path with the journal settings of the soak. Natural rotation and file
   removal cannot be compressed under the shipped budget formula (the
   formula limits the write rate to what the cap holds for the horizon), so
   T8 causes them with journald's own commands, `journalctl --rotate` and
   `journalctl --vacuum-files=N`, at chosen times. Phase 1: rotate every five
   minutes just after a sample without removing files, until the budget fails
   or ten user files exist. Phase 2: vacuum to a stated number of files and
   continue rotating; the vacuum follows the first failing sample at once, so that
   no two consecutive samples fail and the abort policy does not end the run.
   Phase 3: let the run idle for an hour. Parameters:
   rotate one minute after every fifth-minute sample, at most ten rotations in
   phase 1; vacuum to four files and make six further rotations in phase 2;
   one hour in phase 3.
2. Run T1-T5 and T7 on the dedicated test environment as specified in the
   transferred procedure.
3. Record T6 from the soak preparations and observations of `M22` and from T8.
4. Report each defect found as a corrected, newly frozen bundle with a real
   regression that fails on the defective behavior.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Obsolete kernel anchor | Establish a pre-trial kernel cursor through the shipped collector, collect quiet intervals, then remove only the archived journal file containing that anchor while retaining the entire required collection interval; repeat collection twice and compare the preserved defective bundle with the candidate | Dedicated Rocky 8.10 test VM; real systemd 239 journal files; real shipped collector and fixture | Actual old cursor becomes unavailable; original collector reproduces the error; candidate retains proven interval coverage and has no kernel_journal error or false abort. An unproved interval cannot be accepted by clearing the cursor |
| T2 | Empty kernel interval | Collect at least three successive intervals containing real system records but no kernel records; also query retained files with no kernel row at or before the initial boundary | Dedicated test VM; actual journal files, collector and state persistence | Empty kernel output remains distinct from missing system-journal coverage; verified quiet intervals succeed, zero observed memory events are reported with coverage, and state survives repeated collection without depending on a pre-trial kernel row |
| T3 | Rotation and event delivery | Generate uniquely tagged benign records through the real kernel logging path before/after collection and across an actual rotation; run full and journal-only collection repeatedly, including final capture; rotate during collection in a separate case | Dedicated test VM; actual journald, journalctl, collector and terminal paths | Every independently recorded kernel marker in the required interval is archived exactly once after cursor deduplication; no omission across rotation or final capture. A collection/rotation race must establish coverage or return an explicit incomplete result |
| T4 | Required-record loss | Remove an archived system journal file containing known, not-yet-collected in-window markers; retain an older user journal and later system records; repeat with a missing application or health interval and replay the evaluator | Dedicated test VM plus preserved file copies; real collector and evaluator | Known loss or unresolved continuity cannot yield coverage_complete=true or Passed; an older user record cannot prove system coverage. Failed assertions remain visible after later successful collection; no silent reset to now |
| T5 | Boundaries and boot identity | Place actual retained records before, at and after collection cutoffs, across UTC midnight and before/after a real test-VM reboot; replay shipped paths against those real files with only the external clock/filesystem boundary substituted locally | Control host and dedicated test VM; real journal timestamps/cursors and boot IDs | Adjacent interval boundaries neither omit nor double-count records; midnight does not reset coverage. A changed boot or unavailable required boundary is rejected, including initial preparation and post-stop capture |
| T6 | Retention and capacity | Preparation: measure effective caps, system/user write rates and file sizes, then apply the calculation and bind a fresh result to each actual VM/bundle. In-window: repeat budget and continuity checks at every full collection and final capture | Soak VMs of `M22`; real journald measurements, preparation/launcher, collector and evaluator | Passing preparation permits the start of an `M22` observation. In-window, maximum gaps, the factor-two safety allowance and the byte/time inequalities are recorded and hold at every full collection through the first rotation and the first file removal, or fail for a reason the owner accepts. Disk reserve, retention and suppression remain separate assertions |
| T7 | Failure and terminal integration | Run T1's quiet/obsolete-anchor case through two real full samples; separately cause T4's required-record loss, observe two failed full samples, actual abort dispatch and journal-only final collection, then replay the frozen evaluator and attempt normal finish | Dedicated complete test deployment with the shipped 903-PV fixture, appliance, IOC, MariaDB and systemd; retained real abort inputs for local replay | Proven quiet coverage does not request abort. Real loss retains both sample failures, requests abort once, records final capture/stop outcomes, stops timers and yields Incomplete. Later success or normal finish cannot hide errors, repeat stop or turn the aborted run into Passed |
| T8 | Compressed rehearsal | Prepare one fresh VM through the shipped species and launcher on the shortened chain and open an observation; with journald's own `journalctl --rotate` and `journalctl --vacuum-files=N` cause rotations every five minutes without file removal until the budget fails or ten user files exist, then vacuum to a stated file count and continue; compare each sample, the budget and the accounting with the values the shipped functions give for the same snapshots | One fresh Rocky 8.10 VM (2 vCPU, 4096 MiB, 48 GiB) with the 903-PV fixture; a rehearsal observation, not an `M22` result | The budget fails at the number of retained user files the shipped formula predicts for the snapshot and passes again after the vacuum, the accounting matches the stored entries after every rotation and removal and the store size measurement does not fail, or each deviation is explained by a real fault; a defect found is corrected under plan item 4 before a 24-hour observation relies on the path |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | | Pending | Both schema-4 trials of 2026-10-01 aborted after the pre-trial kernel cursor became unavailable (`M22` results); the candidate has not been run on a removal of its anchor file |
| T2 | Not run | | Pending | |
| T3 | 2026-10-05T20:00:00Z | Default soak VM; bundle `cb9b8106`; and a reproduction guest with a 200-MiB cap on 2026-10-05 | Partial | The first rotation of the system journal inside an observation passed the collector, the budget and the sequence accounting, after two earlier observations aborted at that point (`M22` results). On the reproduction guest the accounting matched the stored entries across real rotations and removals. Tagged kernel markers and the rotation-during-collection case were not run |
| T4 | 2026-10-05T03:43Z | Reproduction guest | Partial | Removing one retained archived system file made `account()` refuse the retained range. The collector's required-marker loss, the missing application or health interval and the evaluator replay were not run |
| T5 | Not run | | Pending | |
| T6 | 2026-10-05T14:00:25Z | Soak VMs of `M22` | Failed in-window twice; preparation Passed | Measured preparations passed on every VM (the preparation rows of `M22`). Two 24-hour observations aborted at the first system journal rotation (14:00:05Z and 07:20:06Z) because `rates()` counted the renamed file as growth; corrected by matching files by device and inode. A later default-chain observation passed its first rotation on 2026-10-05T20:00:00Z. Calculated with the shipped formula on the actual snapshots on 2026-10-06, not observed: the default observation (user bound already at 27,958 bytes/s) needs 1,035,708,866 bytes with two retained user files and exceeds the cap of 1,073,741,824 from seven; the shortened observation (user bound 614 bytes/s) needs 926,590,667 and would need 1,091,750,951, 18,009,127 over the cap, as soon as one five-minute interval shows a full 8-MiB user file allocation, as the rehearsal and the default observation did. Observed on 2026-10-06 (the `M22` results row "Terminations of the earlier pair"): the shortened observation reached exactly that state at its 04:10:00Z sample, the user bound rising from 614 to 27,958 bytes/s and the required bytes from 926,590,667 to 1,100,140,027 with six retained files, and its bundle aborted it; the default observation stayed under the cap by 5,054,070 bytes (system bound 55,919 bytes/s from 04:50:00Z, user bound 27,961) through 148 full samples until the owner stopped it at 05:28:57Z |
| T6 | 2026-10-11T05:28:53Z, corrected and tested by 06:05Z | Fresh shortened guest of `M22` (Rocky 8.10, systemd 239) for the refusal; control host Python 3.13 for the tests | Preparation refused by a check defect; check corrected | `measure` was refused before its first snapshot because `snapshot()` computed the journald start as whole-second `btime` plus process ticks, 0.437 s before the drop-in's mtime, while systemd's microsecond start was 28 ms after it (the role writes the drop-in and restarts journald in one second). Corrected: `boot_epoch()` uses `time.time() - clock_gettime(CLOCK_BOOTTIME)` and `configuration_applied()` allows one clock tick; three new tests in `test_journal.py` use the observed values on real temporary files and a patched clock, pass on the correction, and fail on two reverted copies (whole-second truncation; `btime` read from `/proc/stat`). Full suite 120 OK, 48 skipped (baseline 117). New `journal_retention.py` SHA256 `d9210972cbc2511c57357de6bc4c0e4063ba53664cc8d1cf837a5d3353ab1d74`; bundle SHA256 `43970448a8c23f48cb43c40966e98732a652409a5fdfe3d4dfcc5e65cbfe8c17`. The refusal row of `M22`'s Separate-Environment amendment holds the guest evidence. |
| T7 | 2026-10-05T17:10:05Z | Soak VMs of `M22` | Partial | Three automatic aborts dispatched once, stopped the appliance with rc 0 and ended Incomplete (shortened 14:00:05Z, default 07:20:06Z, a later shortened 17:10:05Z). A fourth automatic abort on 2026-10-06 (shortened, bundle `3e9815b0`, two consecutive failed budget samples; dispatched 04:15:07Z, appliance stopped in 11.86 s with rc 0, Incomplete) and one owner-requested abort (default, bundle `cb9b8106`; request file written 05:28:35Z, `etl-soak-abort.service` started, appliance stopped in 12.91 s with rc 0, Incomplete with only `observation_duration` failed) behaved the same way. The quiet-coverage case without abort and required-record loss were not run |
| T8 | 2026-10-05T23:25:06Z | A fresh Rocky 8.10 VM, shortened chain, bundle `3e9815b0`; rehearsal observation opened at 22:51:08Z; rotations with `journalctl --rotate` one minute after each fifth-minute sample | Partial; the observation aborted | Five rotations were made. The budget passed through the sample after the fourth retained user file (required 1,004,185,834 bytes) and failed at 23:20:00Z and 23:25:00Z (required 1,120,200,676 and 1,128,589,284 against 1,073,741,824): the user rate bound rose from 10,139 to 27,958 bytes/s when an interval saw a full 8-MiB allocation of a new user file, and the collector keeps the peak bound for the rest of the observation. Two consecutive failed samples dispatched the abort at 23:25:06Z; the verdict was Incomplete with `journal_retention_budget` failed. The sequence accounting passed at every sample and the store size measurement did not fail. The vacuum and idle phases ran on the aborted VM and prove nothing. The driver's first readings were empty because a redirect in its helper replaced the script input, so the planned vacuum after the first failing sample did not happen; the reader was corrected afterwards. The user rate bound had risen step by step before (14, 4,457, 7,688, 10,139 bytes/s). Second rehearsal on 2026-10-06 with bundle `11ee9c8e` on a fresh VM (observation opened 01:36:36Z, rehearsal 01:49:52Z to 03:26:22Z): two rotations, `journalctl --vacuum-files=4`, six further rotations, then twelve idle five-minute samples. The budget failed from the second rotation (1,080,202,551 required bytes, rising to 1,122,145,591 with sixteen retained files) and was recorded on eighteen consecutive samples without a sample error and without an abort request; the sequence accounting passed at every sample, including across the vacuum, where the expected entries of the retained range restarted at 6,226, and the store size measurement did not fail. The rehearsal ended with a deliberate `observe.py abort` (stop 11.31 s, rc 0, Incomplete). The budget separation of `D23` is observed; the budget formula itself is still the open decision of T6 |

##### Closure Evidence

- Not complete.

</details>

#### M26 - Provision the SQLite Archiver Appliance on an existing general Rocky Linux 8.10 server

- Origin: 38560eb / M26
- Identity History: none
- GitHub Issue: none
- Status: Blocked

##### Summary

An existing general Rocky Linux 8.10 server, which the site configures itself, receives the EPICS Archiver
Appliance on the SQLite configuration database through the `archiver_server_sqlite` assembly. The server owner
sets its proxy configuration directly; this row's assembly neither writes nor checks it. It changes nothing about
proxy configuration, SSH or sudo access policy, VM accounts or the existing database service, and it applies the
existing sudo policy and clock settings of the server unchanged.

##### Scope

The group variables that keep the existing sudo policy (`common_manage_sudo=false`) and omit KVM PTP setup
(`chrony_ptp_kvm=false`), the documentation of this interface, the local contract test, the optional
`proxy_check` role with its real-target suite (available, not part of the assembly), and the installation checks
on the server itself.

Out of scope: the proxy files and values (server owner), the checker (cloud-provision owner), a proxy readiness
gate in the assembly, MariaDB stop or removal (a separate owner approval), SSH and sudo access policy, the source
pins `archiver_env_ref` and `archiver_maven_src_tag`, and any change to the cloud-scope `proxy` role.

##### Completion Criteria

- The group assembly resolves and applies without a proxy readiness gate or the schema-2 runtime lock, and the
  guard still refuses an incompatible selection before any operator runs (T1).
- When wired in, the optional `proxy_check` role proceeds only on a ready checker result and refuses with a
  fixed diagnostic on needs-change, refusal, wrong source hash, unsafe input or a non-Rocky 8.10 target, without
  writing any file or exposing any input value (T2, T3; the role is not part of the assembly).
- On the existing server, with its proxy settings set by its owner, the assembly installs the appliance at the
  pinned sources (T4).
- On that server: the four SQLite tables are present, the service account has access, four JVMs run, readiness
  and an actual health timer run succeed, three changing numeric PVs of a real IOC are collected and queried, new
  data arrives after a restart, and re-applying at the same pins changes nothing (T5).

##### Dependencies And Decisions

- `M18`: the SQLite operator and `archiver-dev-sqlite` species this assembly reuses.
- `G5` (Open): the server owner's proxy settings and the installation approval. M26 is Blocked on it; resume as
  In progress when `G5` is Complete.
- `D26` (2026-10-11): the assembly applies without a proxy readiness gate; the server owner sets the proxy
  configuration directly; `proxy_check` stays available and unwired.
- `D25` (2026-10-10): the read-only schema-3 check and its pin, superseded for the assembly wiring by `D26`; the
  removal of `op.proxy` and the schema-2 runtime lock from this assembly still stands.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-10-10; the owner accepted the proxy check wiring design (steps 1 to 4) in the working session. 2026-10-11; the owner directed removing the wiring and keeping the role available (step 5); steps 6 and 7 await `G5`
- Implementation Authorization: 2026-10-10 for steps 1 to 4 (local code, documentation, and verification on two fresh guests acquired through the cloud provider's request path); 2026-10-11 for step 5; none for steps 6 and 7 until `G5` is Complete
- Superseded Plan Artifacts: none

1. Add the `proxy_check` role: it streams the pinned checker, requires its source hash to equal the pin, runs
   `check --input-fd` as root with the private input opened read-only after become, and exposes only a fixed
   result line.
2. Use it before the group assembly (replacing the schema-2 runtime lock guard) and before `archiver_build` when
   `proxy_scope` is `general-server`; keep the cloud scope unchanged.
3. Align the interface documentation and the local contract test.
4. Verify on a fresh Rocky 8.10 guest and a fresh Debian 13 guest through the real playbooks.
5. Remove the role from the group and focused playbooks and align the documentation and local contract test;
   keep the role and its suite, to be wired in only when a site needs a gate.
6. After `G5`: apply the assembly on the server.
7. Verify the install checks of T5 on the server; stopping MariaDB is a separate owner approval and its data and
   enablement are preserved.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Local contract | Run `tests/check-general-server-contract.bash`: real Make selection, inventory resolution, syntax, eight-operator order, development check mode, guard refusals, and the absence of a proxy check or schema-2 runtime lock in the group assembly | Local controller | All checks pass |
| T2 | Real target | With the role wired in, run `tests/check-proxy-check-target.bash --target rocky8`, which drives the group and focused playbooks through Ansible with root become against the pinned checker: ready, needs-change, input absent, wrong input pin, wrong role pin, unsafe input mode and symlink, empty and relative input path, control character in a file, runtime state removed, check mode, focused `archiver_build` stop and cloud-scope skip | Fresh Rocky 8.10 guest | Ready only for matching files; every other case stops with a fixed token; protected files unchanged; no input value in output |
| T3 | Real target | With the role wired in, run `tests/check-proxy-check-target.bash --target non-rocky` against a non-Rocky target with the fixture input | Fresh Debian 13 guest | Refusal with a fixed token, no operator runs, nothing written |
| T4 | Real target | Apply the assembly with the proxy settings set by the server owner | The existing server | The assembly proceeds past the guard and the Maven settings precondition |
| T5 | Real target | Verify the SQLite tables, service account access, four JVMs, readiness, a real health timer run, three changing numeric PVs of a real IOC, new data after a restart, and a same-pin re-apply | The existing server | Each item passes |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-10-11 08:22:44 UTC | Debian controller, non-root, working tree after the wiring removal | Passed | 10 of 10 checks passed. Earlier runs: 11 of 11 at commit `e89002d` with the role wired in, and 9 of 9 on the sudo policy change alone. |
| T2 | 2026-10-11 00:26:37 UTC | Rocky 8.10 guest, key-only account with passwordless sudo, pinned checker at cloud-provision `05cf573`, role wired in at commit `d6e496e`, run through `tests/check-proxy-check-target.bash --target rocky8` | Passed | 21 of 21 cases passed through the real playbooks with root become. Protected files and the input were unchanged across the ready runs, no input value appeared in any play output, and the guest was restored to its original state. An earlier run of the same cases with a throwaway driver on 2026-10-10 20:55:57 UTC also passed 21 of 21. |
| T3 | 2026-10-11 00:26:47 UTC | Debian 13 guest, same account shape, role wired in at commit `d6e496e`, run through `tests/check-proxy-check-target.bash --target non-rocky` | Passed | 7 of 7 cases passed: input absent refused as `input-unavailable`; with the fixture input the checker refused as `runtime.os.unsupported-platform`, also under check mode; no operator ran; protected files and the input were unchanged; no value in any play output; the guest was restored. An earlier run with a throwaway driver on 2026-10-10 21:00:28 UTC also passed 7 of 7. This does not establish behavior on a host that never had the provider's default account. |
| T4 | Not run | The existing server | Pending | Needs `G5`. |
| T5 | Not run | The existing server | Pending | Needs `G5` and T4. |

##### Closure Evidence

- Not complete. Commits `2831187` and `e89002d` carry the code and documentation on `origin/m14-middleware-reconcile`;
  the wiring removal follows them. The row stays open until T4 and T5 pass on the server.

#### G1 - the production IOC server reaches the internal git host

- Origin: 38560eb / G1
- GitHub Issue: none
- Status: Complete

##### Summary

The production IOC server must reach the internal git host so that `species/iocserver.yml` can clone the EPICS
distribution as the IOC owner. Reachability is carried by the site HTTP proxy's CONNECT tunnel (an ssh
`ProxyCommand` over the proxy), not by a firewall whitelist. Responsible party: the site network and the
owner of the production IOC server. Affected work: `M4` / T2.

##### Completion Criteria

- From the production IOC server the owner's key authenticates to the internal git host and `git ls-remote`
  returns the refs.
- The live `species/iocserver.yml` apply that clones through this path passes (`M4` / T2).

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-09-03 | Passed | `species/iocserver.yml` applied on the production IOC server with `ok=25 failed=0`; the EPICS distribution was cloned from the internal git host over the proxy CONNECT tunnel (`M4` / T2). |

##### Closure Evidence

- Complete on 2026-09-03: reachability confirmed by the successful iocserver clone (`M4` / T2).

#### G2 - cloud-provision ships the middleware package baseline and the middleware VM

- Origin: 38560eb / G2
- GitHub Issue: none
- Status: Open

##### Summary

The middleware operator and species structure and the middleware OS package baseline (system OpenJDK 21,
Tomcat 9.0.121, MariaDB; no Maven package) originate in cloud-provision (`docs/milestone-e260630.md` M11, D2,
D3) as the normative source, and a middleware VM is provisionable there, before ansible-provision mirrors the
set and layers its roles. Responsible party: the cloud-provision session. Affected work: `M14`, which stays
Blocked while this gate is Open; its implementation proceeds on the branch against the M11 branch definition
(owner and cloud-provision, 2026-09-14).

##### Completion Criteria

- cloud-provision M11 merges and the middleware VM is provisionable there.
- `M14` / T2 passes against that baseline.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| Not run | Pending | The M11 merge in cloud-provision has not been observed. |

##### Closure Evidence

- Not complete.

#### G3 - epicsarchiverap-env ships a `sql.fill` that loads the configuration schema when the database and application account are provisioned externally

- Origin: 38560eb / G3
- GitHub Issue: none
- Status: Complete

##### Summary

epicsarchiverap-env's `sql.fill` loaded no schema when the database and application account are provisioned
externally, as the operator provisions them, and exited 0 anyway
(jeonghanlee/epicsarchiverap-env#47). The gate was added on 2026-09-23. Responsible party: the
epicsarchiverap-env session. Affected work: `M14`.

##### Completion Criteria

- The #47 fix commit is on `modernize` and epicsarchiverap-env records the acceptance of #47 as met: with only
  the application account, `make sql.fill` loads the schema, `make sql.show` lists `PVTypeInfo`, `PVAliases`,
  `ArchivePVRequests` and `ExternalDataServers`, and an absent database exits non-zero.
- Observing it on an archiver-dev host is `M14` / T17, not this gate.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-09-23 | Passed | The fix is `1fc20a8` on `modernize`; #47 closed with epicsarchiverap-env's acceptance recorded. `M14` / T17 passed on a Rocky 8.10 and a Debian 13 host rebuilt through the operator at that ref. |

##### Closure Evidence

- Complete on 2026-09-23: fix `1fc20a8` on `modernize`, #47 accepted by its owner.

#### G4 - Prepare two independent ETL soak environments

- Origin: 38560eb / G4
- GitHub Issue: none
- Status: Complete

##### Summary

The cloud-provision owner supplies two independent, fresh Rocky 8.10 VMs and
separate inventories for the `archiver-dev` species. Both use the existing
903-PV fixture selected on 2026-09-28. M22 depends on these inputs and the
initial capacity assessment before deployment and registration.

##### Completion Criteria

- Two distinct VM inventories are available to the controller; the VMs have
  matching baseline resources and enough storage for their observation windows.
- The default-chain PV fixture is identified, with its real IOC source and
  registration list available.
- Host identifiers and addresses stay in local inventories and evidence.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-09-28 19:45:38 UTC | Pending | Cloud-provision delivered two separate inventories and reported 4096 MiB allocated to each VM. Actual access, OS, CPU, disk, free space, cloud-init and clock state were checked independently as recorded in M22/T2. The default inventory depends on the separate known-hosts file supplied beside it; preserve both. The default-chain fixture and its storage requirement remain pending |
| 2026-09-28 21:10:29 UTC | Passed | The owner selected the existing 903-PV list for both runs. Actual inventory resolution and all eight species plays select exactly the intended single host for each run. The list has 903 unique names and the SHA256 recorded in M22; all three source IOC databases are available. The 20:22:47 UTC remote disk checks found 17.43 GiB free on the shortened VM and 17.63 GiB on the default VM. The earlier 903-PV measurements grew by 6.71 GiB per 24 hours over a 27-hour interval; this estimates data capacity, not a new default-chain result. The backing host filesystem has approximately 146 GiB free, and host MemAvailable is approximately 24.5 GiB. These inputs support deployment; actual installed footprint, logging allowance and observation headroom must still be checked in M22/T2 before PV registration |

##### Closure Evidence

- Complete on 2026-09-28: two independent inventories, the selected real fixture
  and the initial capacity assessment are available. No application deployment
  or soak acceptance is claimed by this gate.

#### G5 - The server owner prepares the proxy settings and approves the installation on the existing server

- Origin: 38560eb / G5
- GitHub Issue: none
- Status: Open

##### Summary

The server configuration owner sets the proxy configuration of the existing general server directly
(environment, DNF, and the Maven settings file `/etc/maven-proxy-settings.xml`) and approves the installation.
The assembly neither writes nor checks these files (`D26`). `M26` depends on them before its server checks.

##### Completion Criteria

- The proxy settings are in place on the server and, on a proxied host, `/etc/maven-proxy-settings.xml` exists
  (`M26` / T4).
- The owner's approval of the installation is recorded with its date.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-10-11 | Pending | On 2026-10-11 the server configuration session withdrew the private input and the checker gate and asked for the wiring removal; the installation approval and the proxy settings on the server have not been reported. |

##### Closure Evidence

- Not complete.

## Backlog

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tools | M27 | Verify collector capture around normal appliance shutdown | Carry-forward | Deferred | No | D28 | Complete the separate real checks without another full-day producer run; [detail](#m27---verify-collector-capture-around-normal-appliance-shutdown) |
| Tools | M28 | Reproduce journal results on an independent recipient | Carry-forward | Deferred | No | D28 | Complete the separate real checks without another full-day producer run; [detail](#m28---reproduce-journal-results-on-an-independent-recipient) |
| Tools | M29 | Track ETL collection-tool follow-ups | Carry-forward | Deferred | No | D29, D30, D31 | Coordinate independent child completion and retain original evidence; no combined implementation or repeat full-day run solely for tool repair; [detail](#m29---track-etl-collection-tool-follow-ups) |
| Tools | M30 | Track ETL evaluation and reporting follow-ups | Carry-forward | Deferred | No | D29, D30, D31 | Coordinate independent child completion and retain original evidence; no combined implementation or repeat full-day run solely for tool repair; [detail](#m30---track-etl-evaluation-and-reporting-follow-ups) |
| Tools | M31 | Preserve kernel cursor refusal evidence and prove interval coverage | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m31---preserve-kernel-cursor-refusal-evidence-and-prove-interval-coverage) |
| Tools | M32 | Keep kernel diagnostics independent of the ETL terminal verdict | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m32---keep-kernel-diagnostics-independent-of-the-etl-terminal-verdict) |
| Tools | M33 | Use timestamps accepted by systemd 239 journal queries | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m33---use-timestamps-accepted-by-systemd-239-journal-queries) |
| Tools | M34 | Match JFR exports to the recording process and lifetime | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m34---match-jfr-exports-to-the-recording-process-and-lifetime) |
| Tools | M35 | Persist terminal state before evaluating terminal coherence | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m35---persist-terminal-state-before-evaluating-terminal-coherence) |
| Tools | M36 | Match ETL pass times by UTC instant with nanosecond precision | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m36---match-etl-pass-times-by-utc-instant-with-nanosecond-precision) |
| Tools | M37 | Refresh preserved-tool checksums | Carry-forward | In progress | No | D31, D34, D35 | Complete independently scoped tool work from real evidence; [detail](#m37---refresh-preserved-tool-checksums) |
| Tools | M38 | Finish ETL tool independence checks across both store chains | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m38---finish-etl-tool-independence-checks-across-both-store-chains) |
| Tools | M39 | Finish partial-source ETL evidence verification on both chains | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m39---finish-partial-source-etl-evidence-verification-on-both-chains) |
| Tools | M40 | Finish all-source evidence loss and automatic-abort verification | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m40---finish-all-source-evidence-loss-and-automatic-abort-verification) |
| Tools | M41 | Verify ETL collector capture and refusal after normal shutdown | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m41---verify-etl-collector-capture-and-refusal-after-normal-shutdown) |
| Tools | M42 | Verify real collection during source-store deletion | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m42---verify-real-collection-during-source-store-deletion) |
| Tools | M43 | Reconcile retained ETL measurements and process identities | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m43---reconcile-retained-etl-measurements-and-process-identities) |
| Tools | M44 | Compare ETL busy time and workload with retained earlier results | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m44---compare-etl-busy-time-and-workload-with-retained-earlier-results) |
| Tools | M45 | Reproduce completed ETL observation reports on an independent recipient | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m45---reproduce-completed-etl-observation-reports-on-an-independent-recipient) |
| Tools | M46 | Report actual test phase durations against the agreed allocations | Carry-forward | Deferred | No | D31 | Complete independently scoped tool work from real evidence; [detail](#m46---report-actual-test-phase-durations-against-the-agreed-allocations) |
| Tools | M47 | Track journal test tooling | Carry-forward | Deferred | No | D32, D33 | Track consolidated journal criteria directly; source issue closure is not test completion; [detail](#m47---track-journal-test-tooling) |
| Tools | M48 | Track ETL test tooling | Carry-forward | Deferred | No | D32, D33 | Track consolidated etl criteria directly; source issue closure is not test completion; [detail](#m48---track-etl-test-tooling) |
| Tools | M49 | Track buffer test tooling | Carry-forward | Deferred | No | D32, D33 | Track consolidated buffer criteria directly; source issue closure is not test completion; [detail](#m49---track-buffer-test-tooling) |
| Tools | M50 | Track shared test tooling | Carry-forward | In progress | No | D32, D33, D34, D35 | Track consolidated shared criteria directly; source issue closure is not test completion; [detail](#m50---track-shared-test-tooling) |

Unassigned work is excluded from the release tally.

### Backlog Details

#### M27 - Verify collector capture around normal appliance shutdown

- Origin: 38560eb / M27
- Identity History: created from the explicitly transferred M25 condition on 2026-10-15 (D28).
- GitHub Issue: #53, https://github.com/jeonghanlee/ansible-provision/issues/53
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #32 is closed not_planned at 2026-10-17T01:11:41Z; unfinished criteria are tracked in #53. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

Normal-stop final capture and the later post-stop direct read have not been demonstrated by the positive journal observation. Verify the collector lifecycle boundary independently of the completed 24-hour recording, live-retention and archive-equality result in #31.

##### Scope

The actual normal appliance stop, final collector interval, known required records around the stop boundary, later direct journal read and combined archive comparison. Reuse `tests/archiver-soak/journal-validation/` on a separate dedicated deployment.

##### Out Of Scope

Another positive 24-hour observation; ETL acceptance or changes to ETL deployments; independent-recipient replay; claims that unexecuted normal-stop checks have passed. A missing check is not evidence of a collector defect.

##### Completion Criteria

- [ ] Declare the real source actions, expected messages, normal-stop boundary and later direct-read condition before execution; retain actual service/process identities and command outcomes.
- [ ] Run a short independent case through the real appliance, journald and shipped collector. Confirm required records before and around the actual stop; do not replace the logging path with synthetic success markers.
- [ ] Compare every declared required identity and full content with the later successful direct journal query and combined final archive. Explain overlap explicitly and report missing, changed or repeated identities.
- [ ] Dispatch the normal stop once, retain the final collector outcome and report delivery, later visibility and terminal collection separately. Missing evidence is Incomplete and confirmed loss remains Failed.
- [ ] Preserve the completed #31 originals and unsuccessful attempts. No new 24-hour recording is a prerequisite for this lifecycle case.

##### Dependencies And Decisions

- D28; Decision Date: 2026-10-15. The owner directed separate Backlog work for later execution. It is not a gate on M25 or M22; implementation is not authorized.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: the transferred condition in the earlier M25 completion plan; original results remain unchanged.

1. Specify the short real stop case and its logging contract.
2. Implement or correct only the collector normal-stop/final-capture path exposed by that case.
3. Run the real stop and later-read comparison, retaining immutable evidence and separate verdicts.

##### Test Plan

| Label | Purpose | Actual Path And Expected Result |
| --- | --- | --- |
| T1 | Normal stop and later capture | Real dedicated appliance stop, native collection and later live query; exact required-record equality. |
| T2 | Repeated terminal request | Real terminal CLI; no second stop and no original-result overwrite. |
| T3 | Failure distinction | Actual command errors and incomplete evidence remain distinct from observed record loss. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Separate future verification | Pending | Normal stop and later capture is unexecuted; completed journal measurements do not prove this check. |
| T2 | Not run | Separate future verification | Pending | Repeated terminal request is unexecuted; completed journal measurements do not prove this check. |
| T3 | Not run | Separate future verification | Pending | Failure distinction is unexecuted; completed journal measurements do not prove this check. |

##### Closure Evidence

- Not complete. Deferred by explicit dated owner decision, with no execution or Passed claim.

##### GitHub Projection

- Title: `Track journal test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #53, https://github.com/jeonghanlee/ansible-provision/issues/53
- Projection Scope: Component contract from historical source #32; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:36Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-journal.md`
- Published Body SHA256: 57226e8a00e7b8aca7c4a5143f1ff5a915bc8b13dea7b1e2f5d99d032d46305d
- Historical Source Issue: #32, https://github.com/jeonghanlee/ansible-provision/issues/32
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:11:41Z
- Historical Original Body SHA256: e78f5657a4f19188c95c1ab65d2e326597d1d0c241fadea21ad49c8fe02ffa57
- Historical Retired Body SHA256: 4a9a855859ce219f3c01ea691c54655751b94e91def73820e50fead75022f3ba

#### M28 - Reproduce journal results on an independent recipient

- Origin: 38560eb / M28
- Identity History: created from the explicitly transferred M25 condition on 2026-10-15 (D28).
- GitHub Issue: #53, https://github.com/jeonghanlee/ansible-provision/issues/53
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #33 is closed not_planned at 2026-10-17T01:11:45Z; unfinished criteria are tracked in #53. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The complete corrected 24-hour journal result was reproduced exactly by a separate frozen CLI process on the recording deployment. Reproduction on an independent recipient has not yet been executed. Verify evidence portability and replay reproducibility separately from the Passed journal recording, retention and collection measurements in #31.

##### Scope

Private transfer and member/hash verification of retained actual evidence, source/configuration identity, exact frozen comparison tools, recipient-side per-record comparison and complete-result equality. Reuse the completed observation rather than starting a new one.

##### Out Of Scope

A new 24-hour recording, live appliance operations, ETL acceptance, collector normal-stop behavior, public storage of raw records or deployment identifiers, and claims that same-deployment replay proves independent-recipient reproduction.

##### Completion Criteria

- [ ] Select the retained complete actual observation, its explicitly frozen corrected tools, saved result and per-record comparison digest. Preserve the original package and earlier unsuccessful result separately.
- [ ] Transfer the necessary evidence privately and verify every declared member/hash before replay. Keep runtime configuration and raw journal records out of Git and public issue text.
- [ ] Execute the real frozen `long.py replay` CLI on a different recipient environment without contacting or operating the original appliance or using substitute records.
- [ ] Require the complete result JSON, per-path verdicts and per-record comparison digest to match the completed result exactly. Record a transfer/hash or replay error independently; do not reinterpret it as observed journal loss.
- [ ] Verify the original evidence and saved unsuccessful results remain unchanged. No new producer schedule or 24-hour waiting period is required.

##### Dependencies And Decisions

- D28; Decision Date: 2026-10-15. The owner directed separate Backlog work for later execution. It is not a gate on M25 or M22; implementation is not authorized.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: the transferred condition in the earlier M25 completion plan; original results remain unchanged.

1. Define the portable evidence/member contract using the preserved actual observation.
2. Verify private transfer and install only the exact frozen replay dependencies on the recipient.
3. Run the real replay and compare the complete result and per-record digest while checking original preservation.

##### Test Plan

| Label | Purpose | Actual Path And Expected Result |
| --- | --- | --- |
| T1 | Private evidence transfer | Retained actual evidence and every declared member/hash match on the independent recipient. |
| T2 | Frozen full-record replay | Actual frozen replay CLI; complete result and per-record digest equal the saved observation. |
| T3 | Original preservation | Original inputs, tools and earlier unsuccessful result remain unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Separate future verification | Pending | Private evidence transfer is unexecuted; completed journal measurements do not prove this check. |
| T2 | Not run | Separate future verification | Pending | Frozen full-record replay is unexecuted; completed journal measurements do not prove this check. |
| T3 | Not run | Separate future verification | Pending | Original preservation is unexecuted; completed journal measurements do not prove this check. |

##### Closure Evidence

- Not complete. Deferred by explicit dated owner decision, with no execution or Passed claim.

##### GitHub Projection

- Title: `Track journal test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #53, https://github.com/jeonghanlee/ansible-provision/issues/53
- Projection Scope: Component contract from historical source #33; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:36Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-journal.md`
- Published Body SHA256: 57226e8a00e7b8aca7c4a5143f1ff5a915bc8b13dea7b1e2f5d99d032d46305d
- Historical Source Issue: #33, https://github.com/jeonghanlee/ansible-provision/issues/33
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:11:45Z
- Historical Original Body SHA256: eb48705ecf2b144e98bb607e9cf18c789c6fe83f37e2e1fa54755e26d5490481
- Historical Retired Body SHA256: e2cd3fb06080ce9b122340a648101bc72cbaaa2468af03950f29c42e78fae10e

#### M29 - Track ETL collection-tool follow-ups

- Origin: 38560eb / M29
- Identity History: created from explicit M22 tool-defect Backlog separation on 2026-10-15 (D29).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #34 is closed not_planned at 2026-10-17T01:11:50Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

D31 separates this coordination parent from the independent child implementations below. The retained technical criteria and T labels define transferred coverage, not one combined repair or duplicate execution. Each child has its own scope, completion criteria and real-path verification. Child completion must be established separately.

The frozen kernel-journal collector used by the two completed 24-hour ETL observations rejected the previous kernel cursor. This diagnostic failure propagated through required-pass waiting, final sampling and final journal capture, leaving the original aggregate verdicts `Incomplete` despite complete actual ETL pass sets, successful physical/HTTP comparisons and orderly shutdown.

The shortened observation retained all 312 required passes and the default observation all 27, with no missing, duplicate or unexpected passes. Their unchanged native scheduler evaluations returned `Passed`. This is an independent tool follow-up from #30; it does not block those accepted ETL processing results or reopen the journal acceptance in #31.

The remaining installation/package, source-availability, collection-failure, automatic-abort and terminal-tool checks previously listed under #30 belong here. They verify the collection and orchestration tools after actual ETL functionality has been accepted; they are not unfinished ETL processing tests. Evaluation/reporting and recipient reproduction belong to #35.

The shortened unrelated-module failure and importable-change cases completed actual preparation, capture and planned stop with matching frozen guest/recipient replay. The shortened journal-unavailable/application-file-available case retained a successful 903-job ETL pass without automatic abort and passed retained-original verification; its original short-observation and controller findings remain unchanged. Default variants remain unverified.

The shortened all-sources-unavailable case completed on 2026-10-15 UTC. Two actual full samples could read neither the journal nor any of the four configured application files. Native critical-failure counters advanced from one to two; the second sample triggered exactly one automatic abort. The whole appliance stopped with return code 0 in 11.878 seconds, final terminal capture had no errors, the original sampler configuration was restored and the appliance remained stopped. Retained actual ETL evidence also contained a successful 903-job pass during the fault. Native readers verified this behavior without changing original inputs or tools. The original controller remained `Incomplete` because its literal UTC-string comparison found no pass, while the native timestamp parser found the one matching pass. This completes only the observed shortened automatic-abort behavior; independent recipient reproduction and corrective tool implementation are separate work.

##### Scope

Coordinate the independent child issues and retain their aggregate coverage and original evidence. D30 excludes collection/evaluation/report/reproduction work from accepted ETL functionality; D31 assigns each independent deliverable below without authorizing its execution.

##### Out Of Scope

JFR process selection and terminal evaluator ordering are a separate tool follow-up. This issue does not prove the missing historical kernel-query contents, alter journal acceptance, change storage policies, introduce a journal capacity cap or require another full-day producer run.

##### Current Child Verification Boundaries

Historical kernel refusals belong to the observations' original frozen collector. The current repository candidate already preserves checkpoint stdout/stderr before cursor refusal, and the preserved v2 scenario already changes journal query formatting. Keep those existing source changes distinct from the remaining real refusal/interval verification; neither source inspection nor the accepted ETL result completes that verification.

##### Child Case Matrix And Verdict Contract

Independence coverage is a fixed two-chain/three-study-state normal-finish matrix; existing shortened failing/changed planned-abort results retain only their recorded scope. Absence and normal-finish scenario support still need candidate implementation/integration. For short independence/source-fault checks, successful scenario verification and recipient replay require exit code 0 and `expectation=Passed`; the deliberately shortened native abort/evaluator/aggregator keeps `Incomplete` and expected exit code 1, with appliance stop rc 0. Historical controller failures remain unchanged and matching failed scenario runs never establish tool completion.

##### Root Cause

In the affected frozen `tests/archiver-soak/etl-pass/collect.py`, `collect_kernel()` requires the first query entry to equal the previous cursor before writing the kernel export. The refusal was recorded in 240 shortened and 237 default in-window full samples. The affected failure path did not retain the actual failed query stdout/stderr, so the historical evidence cannot distinguish an obsolete anchor from loss of a required kernel interval.

In `tests/archiver-soak/etl-pass/observe.py`, `wait_passes()` rejects a nonzero journal-only collector exit before checking the available application ETL pass records. A kernel diagnostic failure therefore produced `required_pass_wait`, `final_sample` and `final_journal` terminal findings although required ETL processing evidence remained available.

##### Reproduction

Replay each unchanged completed observation through its actual frozen evaluator and inspect the retained cursor-refusal and terminal findings. The native pass parser/evaluator establishes complete ETL pass sets. Reproduce collector refusal and terminal propagation in a separate focused real-journald trial using the affected shipped collector and actual terminal entry point, with its outputs separate from the completed observations. The missing historical failed-query output cannot be reconstructed as proof of kernel coverage.

##### Completion Criteria

- [ ] Every independent item is linked to its own issue with a specific scope, original-evidence context and completion criteria.
- [ ] Completion is recorded from each item's actual implementation/verification or an explicit evidenced disposition; closing this tracking issue does not mark unfinished items complete.
- [ ] Original unsuccessful records and completed behavior remain distinguishable from candidate tool corrections.

Retained transferred technical coverage follows; record each result in its owning child detail rather than treating this list as one implementation.

- [ ] The real failed-query path preserves its original output and enough cursor/interval metadata to diagnose the refusal without exposing credentials or internal identifiers.
- [ ] Focused real-journald checks distinguish an obsolete anchor with independently proven interval coverage from an actual or unresolved required-interval gap; unproved coverage never becomes `Passed`.
- [ ] The actual normal-finish and replay paths keep a kernel-only diagnostic failure visible without rejecting a complete required ETL pass set.
- [ ] Genuine loss of required ETL evidence remains `Incomplete` or `Failed` as applicable, and the declared all-sources-unavailable automatic-abort expectations remain enforced.
- [ ] Both completed observations are rechecked from retained evidence with their exact original tools and a separately identified candidate; original data, failed records and verdicts remain unchanged.
- [ ] The follow-up uses retained evidence and bounded real-path checks; no new 24-hour observation is required solely to repair the collector.

- [ ] Complete collector/package independence through actual preparation, start, capture, normal terminal handling and replay on both chains with unrelated journal-study modules absent, failing and separately changed. Preserve completed shortened results; execute the unverified default variants as tool checks.
- [ ] Complete the remaining collection-source failure and automatic-abort cases using actual configured sources. Distinguish successful ETL processing from unavailable test evidence, and retain first-failure versus repeated-failure behavior.
- [ ] Verify final and post-stop application-file capture, process identity, repeated terminal refusal and restoration through the actual tools without changing completed ETL observation records.
- [ ] Exercise real collection during source-store deletion and metrics requests overlapping ETL pass completion; preserve actual request bounds and measured outputs instead of converting collection races into ETL failures.
- [ ] Preserve actual fixture/input counts, source timing and workload identity for later measurement reports; configured frequency multiplied by duration is not an observed event count.
- [ ] Keep these tool checks independent of the completed ETL functionality result in #30. Future collector corrections follow the accepted ETL verification and do not require another full-day observation solely for tool repair.

##### Dependencies And Decisions

- D29; Decision Date: 2026-10-15. Independent Deferred Backlog work, not an acceptance gate on M22 full-day ETL processing or M25 journal acceptance. Issue publication is authorized; corrective implementation is not authorized by that delegation.
- D30; Decision Date: 2026-10-15. All remaining work on the test tools is added here after actual ETL functionality acceptance. Collection/lifecycle work belongs to M29; evaluator, supplemental report and recipient reproduction belong to M30. Neither gates M22 functionality.

- D31; Decision Date: 2026-10-15. Independent child work is Deferred outside current execution. This parent coordinates child evidence and does not substitute for any child's verification or authorize corrective runtime work.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: the diagnosed tool correction formerly included in M22 final-result handling; original outcomes remain unchanged.

Retain the query arguments, return code, stdout/stderr and cursor/interval identities before a collector refusal. Distinguish an obsolete pre-window anchor from an unproved required interval using actual retained records. Recovery must prove coverage; silently clearing a cursor is insufficient.

Report kernel diagnostic coverage separately from required ETL evidence availability in periodic collection, pass waiting, normal finish, aggregation and replay. Preserve diagnostic failures, but allow complete ETL application evidence to establish the ETL result. Loss of every configured required ETL source must still remain detectable and must retain the existing ETL failure/abort behavior.

Independent membership and transferred coverage:

| Child | Independent Work | Issue Draft |
| --- | --- | --- |
| M31 | Preserve kernel cursor refusal evidence and prove interval coverage | `work/issue-kernel-cursor.md` |
| M32 | Keep kernel diagnostics independent of the ETL terminal verdict | `work/issue-etl-terminal-isolation.md` |
| M33 | Use timestamps accepted by systemd 239 journal queries | `work/issue-journal-query-time.md` |
| M37 | Refresh preserved-tool checksums | `work/issue-tool-checksums.md` |
| M38 | Finish ETL tool independence checks across both store chains | `work/issue-package-independence.md` |
| M39 | Finish partial-source ETL evidence verification on both chains | `work/issue-partial-source-availability.md` |
| M40 | Finish all-source evidence loss and automatic-abort verification | `work/issue-all-source-abort.md` |
| M41 | Verify ETL collector capture and refusal after normal shutdown | `work/issue-etl-post-stop.md` |
| M42 | Verify real collection during source-store deletion | `work/issue-collection-races.md` |

| Retained Parent Coverage | Independent Owner | Scope |
| --- | --- | --- |
| T1-T2 | M31 | Failed-query evidence and actual cursor/interval coverage |
| T3 | M32, M35, M41 | ETL evidence isolation, terminal coherence and final capture |
| T4, T8 | M39, M40 | Partial-source operation and all-source abort behavior |
| T5 | M31, M32, M34, M35, M45 | Retained originals, scoped candidate checks and recipient reproduction |
| T6, T12 | All children | Accepted functionality stays closed; bounded tool work only |
| T7 | M38 | Both-chain package independence and normal terminal/replay coverage |
| T9 | M41 | Final/post-stop capture, identity and repeated request refusal |
| T10 | M42, M43 | Real deletion overlap and measured request/pass timing |
| T11 | M43, M44 | Observed counts, source timing and comparable workload identity |
| Additional query/checksum defects | M33, M37 | CLI timestamp compatibility and preserved-source integrity |

##### Test Plan

| Label | Purpose | Actual Path And Expected Result |
| --- | --- | --- |
| T1 | Tool follow-up 1 | The real failed-query path preserves its original output and enough cursor/interval metadata to diagnose the refusal without exposing credentials or internal identifiers. |
| T2 | Tool follow-up 2 | Focused real-journald checks distinguish an obsolete anchor with independently proven interval coverage from an actual or unresolved required-interval gap; unproved coverage never becomes `Passed`. |
| T3 | Tool follow-up 3 | The actual normal-finish and replay paths keep a kernel-only diagnostic failure visible without rejecting a complete required ETL pass set. |
| T4 | Tool follow-up 4 | Genuine loss of required ETL evidence remains `Incomplete` or `Failed` as applicable, and the declared all-sources-unavailable automatic-abort expectations remain enforced. |
| T5 | Tool follow-up 5 | Both completed observations are rechecked from retained evidence with their exact original tools and a separately identified candidate; original data, failed records and verdicts remain unchanged. |
| T6 | Tool follow-up 6 | The follow-up uses retained evidence and bounded real-path checks; no new 24-hour observation is required solely to repair the collector. |
| T7 | Tool follow-up 7 | Complete collector/package independence through actual preparation, start, capture, normal terminal handling and replay on both chains with unrelated journal-study modules absent, failing and separately changed. Preserve completed shortened results; execute the unverified default variants as tool checks. |
| T8 | Tool follow-up 8 | Complete the remaining collection-source failure and automatic-abort cases using actual configured sources. Distinguish successful ETL processing from unavailable test evidence, and retain first-failure versus repeated-failure behavior. |
| T9 | Tool follow-up 9 | Verify final and post-stop application-file capture, process identity, repeated terminal refusal and restoration through the actual tools without changing completed ETL observation records. |
| T10 | Tool follow-up 10 | Exercise real collection during source-store deletion and metrics requests overlapping ETL pass completion; preserve actual request bounds and measured outputs instead of converting collection races into ETL failures. |
| T11 | Tool follow-up 11 | Preserve actual fixture/input counts, source timing and workload identity for later measurement reports; configured frequency multiplied by duration is not an observed event count. |
| T12 | Tool follow-up 12 | Keep these tool checks independent of the completed ETL functionality result in #30. Future collector corrections follow the accepted ETL verification and do not require another full-day observation solely for tool repair. |
| T13 | Coordination coverage | Inspect the actual published child links and each child's recorded verification/disposition. Every independent item is linked to its own issue with a specific scope, original-evidence context and completion criteria. |
| T14 | Coordination coverage | Inspect the actual published child links and each child's recorded verification/disposition. Completion is recorded from each item's actual implementation/verification or an explicit evidenced disposition; closing this tracking issue does not mark unfinished items complete. |
| T15 | Coordination coverage | Inspect the actual published child links and each child's recorded verification/disposition. Original unsuccessful records and completed behavior remain distinguishable from candidate tool corrections. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T2 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T3 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T4 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T5 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T6 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T7 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T8 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T9 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T10 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T11 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T12 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T2 existing shortened E4 | 2026-10-15T17:39:50.066490+00:00 | Actual stopped additional-test deployment and frozen native readers; original files read only | Passed for observed automatic-abort behavior; original controller/native short observation Incomplete | Two full fault samples at 15:55:00.707457 and 16:00:00.364564 UTC could read neither journal nor four application files; actual native counters 1 then 2 triggered one automatic abort. The appliance stopped with rc 0 in 11.878069368991419 seconds, final capture had no errors and the sampler configuration was exactly restored. One successful 903-job pass existed during the fault. Literal plannedAt comparison found zero matches; native nanosecond comparison found exactly one. Evidence: private E4-owner-verification-20261015-001.stdout SHA256 3101a45cda7378620eda34768980766c85da828a1156df3c439261e41a9240b7. All original hashes and bundle unchanged; no guest mutation. |
| T13 | Not run | Independent child issue and evidence reconciliation | Pending | Decomposition is prepared only; child correction/verification is not complete. |
| T14 | Not run | Independent child issue and evidence reconciliation | Pending | Decomposition is prepared only; child correction/verification is not complete. |
| T15 | Not run | Independent child issue and evidence reconciliation | Pending | Decomposition is prepared only; child correction/verification is not complete. |

##### Closure Evidence

- Not complete. D29 defers corrective implementation/verification. Accepted ETL processing does not establish a Passed tool correction.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #34; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #34, https://github.com/jeonghanlee/ansible-provision/issues/34
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:11:50Z
- Historical Original Body SHA256: e6f26dd5e6460c648f1ba9a295ede7df429a31cf9f1b682479a3818dc317f8d4
- Historical Retired Body SHA256: f30610fe813919c102d309d3401e81b9a9539374d6f081c3f7e5a03d150afc4e

#### M30 - Track ETL evaluation and reporting follow-ups

- Origin: 38560eb / M30
- Identity History: created from explicit M22 tool-defect Backlog separation on 2026-10-15 (D29).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #35 is closed not_planned at 2026-10-17T01:11:56Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

D31 separates this coordination parent from the independent child implementations below. The retained technical criteria and T labels define transferred coverage, not one combined repair or duplicate execution. Each child has its own scope, completion criteria and real-path verification. Child completion must be established separately.

The frozen ETL evaluator reports missing JFR export coverage and terminal coherence for two completed 24-hour observations even though the retained data supports complete current-process recordings and successful ETL processing. Correct the measurement scope and terminal evaluation order while preserving every original record and unsuccessful aggregate verdict.

This is an independent verification-tool follow-up from #30. It does not block the accepted shortened and default full-day ETL processing results and does not establish completion of the separate fault/abort or independent-recipient checks.

##### Scope

Coordinate the independent child issues and retain their aggregate coverage and original evidence. D30 excludes collection/evaluation/report/reproduction work from accepted ETL functionality; D31 assigns each independent deliverable below without authorizing its execution.

##### Out Of Scope

Kernel cursor recovery and ETL terminal isolation from kernel diagnostics are a separate collector follow-up. ETL application code, store policy, journal acceptance and unexecuted default-chain or evidence-source fault cases are unchanged.

##### Current Child Verification Boundaries

The numerical report must explicitly include per-component heap, GC cause/pause, jstat, RSS, observed input/event counts and rates, retrieval freshness/visibility, request bounds and process identity/gap/OOM evidence. Independent-recipient comparison uses a frozen post-finalization evaluator/aggregator baseline with exact input, tool/dependency/version, command, exit-code and output-hash identities. The initial embedded evaluation and any corrected-candidate baseline remain separate.

##### Root Cause

In `tests/archiver-soak/etl-pass/evaluate.py`, the complete-recording comparison counts deduplicated CSV events by component without selecting the recording PID. The CSV retains earlier JVM processes as well as the final observation process, while each final JFR belongs to one PID. For example, the shortened ETL heap comparison counts 66304 all-process rows against 59094 final-recording events; the matching-PID count is exactly 59094. The default comparison similarly counts 6266 against 6214, with exactly 6214 rows for the final PID.

On both chains, all twelve component/event-kind comparisons match when scoped to the final recording PID: heap, collection and pause events for four JVMs. Complete JFR sizes and hashes match, full-window coverage is present and recorded data-loss counts are zero. The current `jfr_export_heap_coverage`, `jfr_export_collection_coverage` and `jfr_export_pause_coverage` findings therefore arise from comparing different process populations.

In `tests/archiver-soak/etl-pass/observe.py`, `terminal()` calls the evaluator before writing `shutdown.json` or `abort.json`. The invoked `aggregate.py` reads the terminal from disk and reports `coherent_manifest_and_terminal` while only the started marker exists. Re-executing the unchanged native evaluator after the final file was persisted removes that finding on both original observations without changing any input.

The retained shortened source-availability and automatic-abort cases expose another verifier defect: actual native pass timestamps use `Z`, while the declared scheduler time uses `+00:00`. The literal string comparison returns zero matches although the shipped nanosecond timestamp parser finds exactly one matching successful 903-job pass at the same UTC instant. Preserve both original strings and original `Incomplete` controller records; correct the selection logic in the runtime/scenario checker and replay without rewriting the evidence.

##### Reproduction

Execute the actual frozen evaluator against each complete retained observation. Compare the complete-recording counts with the native deduplicated CSV records for all processes and for the recording PID separately. Compare the stored terminal evaluation with the native CLI evaluation on the same finalized originals. Preserve the kernel diagnostic failures; they are independently explained and are not expected to disappear from this issue's correction.

##### Completion Criteria

- [ ] Every independent item is linked to its own issue with a specific scope, original-evidence context and completion criteria.
- [ ] Completion is recorded from each item's actual implementation/verification or an explicit evidenced disposition; closing this tracking issue does not mark unfinished items complete.
- [ ] Original unsuccessful records and completed behavior remain distinguishable from candidate tool corrections.

Retained transferred technical coverage follows; record each result in its owning child detail rather than treating this list as one implementation.

- [ ] The real evaluator and numerical aggregator correctly reconcile retained current-process heap/collection/pause records with complete JFRs on both chains while retaining earlier-process data.
- [ ] Missing, conflicting or incomplete records in an actual retained-input copy remain detectable; no internal-function stub or reconstructed positive fixture establishes acceptance.
- [ ] A real normal-terminal invocation and subsequent offline replay agree on terminal coherence, including actual failure, interruption and repeat-terminal handling.
- [ ] Verification runs the shipped tools and actual retained evidence, with original and candidate tool identities kept separate. Original inputs, terminal bytes and failed verdicts remain unchanged.
- [ ] Results state which independent kernel diagnostic findings remain; evaluator correction does not claim historical kernel coverage or change the already accepted ETL functionality result in #30.
- [ ] Use the completed observations for regression and focused real terminal checks for ordering; a new 24-hour observation is not required solely to repair these verifier defects.

- [ ] Compare original UTC instants with the shipped timestamp parser, retaining nanosecond precision and original strings. Verify actual retained source-availability and automatic-abort inputs through the real runtime/scenario and replay paths; do not change an original controller status to satisfy the checker.
- [ ] Reconcile per-component heap, GC cause/pause, jstat, RSS, observed input/event rates, retrieval freshness/visibility, request bounds and identity/gap/OOM evidence from the already collected observations.
- [ ] Evaluate retained and focused real-input measurement regressions for source-store shrink, pass-end/request overlap, accumulation and restart. Collection-path corrections are coordinated with #34; no internal mock establishes integration acceptance.
- [ ] Produce the supplemental workload/performance comparison: last-pass and average busy time, weekly usage and actual load, concurrency, store-age and resource differences. Missing comparable historical rates prohibit an improvement claim but do not reopen ETL functionality acceptance.
- [ ] Privately transfer the retained evidence and exact frozen tools to an independent recipient, verify declared members/hashes and reproduce complete result JSON and numerical reports. Keep original unsuccessful findings, raw operational data and deployment identifiers out of public Git.
- [ ] Record actual preparation, processing, waiting, observation and analysis times against the agreed one-hour journal, three-hour ETL, parallel full-day and two-hour overall decision allocations as supplemental reporting; do not impose a new observation to complete the report.
- [ ] Complete these evaluator/report/reproduction checks after the accepted ETL functionality result. Their completion is not a gate on #30 and no new 24-hour data-production run is required solely for these corrections or analyses.

##### Dependencies And Decisions

- D29; Decision Date: 2026-10-15. Independent Deferred Backlog work, not an acceptance gate on M22 full-day ETL processing or M25 journal acceptance. Issue publication is authorized; corrective implementation is not authorized by that delegation.
- D30; Decision Date: 2026-10-15. All remaining work on the test tools is added here after actual ETL functionality acceptance. Collection/lifecycle work belongs to M29; evaluator, supplemental report and recipient reproduction belong to M30. Neither gates M22 functionality.

- D31; Decision Date: 2026-10-15. Independent child work is Deferred outside current execution. This parent coordinates child evidence and does not substitute for any child's verification or authorize corrective runtime work.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: the diagnosed tool correction formerly included in M22 final-result handling; original outcomes remain unchanged.

Bind each JFR/CSV comparison to its component, process and recording lifetime. Preserve earlier-process rows and evaluate their own scope where required instead of deleting them to force equality. Real in-scope missing, duplicated, conflicting or truncated data must remain detectable.

Make terminal persistence and evaluation consistent so the aggregate path observes the terminal being evaluated. Preserve repeat-terminal refusal, failure visibility and crash/retry behavior; do not publish an unverified successful verdict to bypass the missing-terminal check.

Independent membership and transferred coverage:

| Child | Independent Work | Issue Draft |
| --- | --- | --- |
| M34 | Match JFR exports to the recording process and lifetime | `work/issue-jfr-process-scope.md` |
| M35 | Persist terminal state before evaluating terminal coherence | `work/issue-terminal-order.md` |
| M36 | Match ETL pass times by UTC instant with nanosecond precision | `work/issue-utc-pass-match.md` |
| M43 | Reconcile retained ETL measurements and process identities | `work/issue-measurement-report.md` |
| M44 | Compare ETL busy time and workload with retained earlier results | `work/issue-workload-comparison.md` |
| M45 | Reproduce completed ETL observation reports on an independent recipient | `work/issue-etl-recipient-replay.md` |
| M46 | Report actual test phase durations against the agreed allocations | `work/issue-elapsed-time-report.md` |

| Retained Parent Coverage | Independent Owner | Scope |
| --- | --- | --- |
| T1-T2 | M34 | Recording process/lifetime matching and real retained-input negatives |
| T3 | M35, M41 | Terminal persistence, actual stop and repeated/interrupted requests |
| T4-T6, T13 | All children | Original/candidate identities, diagnostic limits and accepted functionality |
| T7 | M36 | UTC instant matching through actual scenario and replay paths |
| T8 | M43 | Numerical measurements, observed rates and process identities |
| T9 | M42, M43 | Source shrink, request/pass overlap, accumulation and process restart |
| T10 | M44 | Comparable measured busy time and workload |
| T11 | M45 | Independent full-day recipient result/report reproduction |
| T12 | M46 | Actual elapsed phase reporting against agreed allocations |

##### Test Plan

| Label | Purpose | Actual Path And Expected Result |
| --- | --- | --- |
| T1 | Tool follow-up 1 | The real evaluator and numerical aggregator correctly reconcile retained current-process heap/collection/pause records with complete JFRs on both chains while retaining earlier-process data. |
| T2 | Tool follow-up 2 | Missing, conflicting or incomplete records in an actual retained-input copy remain detectable; no internal-function stub or reconstructed positive fixture establishes acceptance. |
| T3 | Tool follow-up 3 | A real normal-terminal invocation and subsequent offline replay agree on terminal coherence, including actual failure, interruption and repeat-terminal handling. |
| T4 | Tool follow-up 4 | Verification runs the shipped tools and actual retained evidence, with original and candidate tool identities kept separate. Original inputs, terminal bytes and failed verdicts remain unchanged. |
| T5 | Tool follow-up 5 | Results state which independent kernel diagnostic findings remain; evaluator correction does not claim historical kernel coverage or change accepted functionality in #30. |
| T6 | Tool follow-up 6 | Use the completed observations for regression and focused real terminal checks for ordering; a new 24-hour observation is not required solely to repair these verifier defects. |
| T7 | Tool follow-up 7 | Compare original UTC instants with the shipped timestamp parser, retaining nanosecond precision and original strings. Verify actual retained source-availability and automatic-abort inputs through the real runtime/scenario and replay paths; do not change an original controller status to satisfy the checker. |
| T8 | Tool follow-up 8 | Reconcile per-component heap, GC cause/pause, jstat, RSS, observed input/event rates, retrieval freshness/visibility, request bounds and identity/gap/OOM evidence from the already collected observations. |
| T9 | Tool follow-up 9 | Evaluate retained and focused real-input measurement regressions for source-store shrink, pass-end/request overlap, accumulation and restart. Collection-path corrections are coordinated with #34; no internal mock establishes integration acceptance. |
| T10 | Tool follow-up 10 | Produce the supplemental workload/performance comparison: last-pass and average busy time, weekly usage and actual load, concurrency, store-age and resource differences. Missing comparable historical rates prohibit an improvement claim but do not reopen ETL functionality acceptance. |
| T11 | Tool follow-up 11 | Privately transfer the retained evidence and exact frozen tools to an independent recipient, verify declared members/hashes and reproduce complete result JSON and numerical reports. Keep original unsuccessful findings, raw operational data and deployment identifiers out of public Git. |
| T12 | Tool follow-up 12 | Record actual preparation, processing, waiting, observation and analysis times against the agreed one-hour journal, three-hour ETL, parallel full-day and two-hour overall decision allocations as supplemental reporting; do not impose a new observation to complete the report. |
| T13 | Tool follow-up 13 | Complete these evaluator/report/reproduction checks after the accepted ETL functionality result. Their completion is not a gate on #30 and no new 24-hour data-production run is required solely for these corrections or analyses. |
| T14 | Coordination coverage | Inspect the actual published child links and each child's recorded verification/disposition. Every independent item is linked to its own issue with a specific scope, original-evidence context and completion criteria. |
| T15 | Coordination coverage | Inspect the actual published child links and each child's recorded verification/disposition. Completion is recorded from each item's actual implementation/verification or an explicit evidenced disposition; closing this tracking issue does not mark unfinished items complete. |
| T16 | Coordination coverage | Inspect the actual published child links and each child's recorded verification/disposition. Original unsuccessful records and completed behavior remain distinguishable from candidate tool corrections. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T2 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T3 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T4 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T5 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T6 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T7 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T8 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T9 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T10 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T11 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T12 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T13 | Not run | Retained real-input or bounded future runtime verification | Pending | Candidate corrective verification is not established by the original accepted ETL result. |
| T14 | Not run | Independent child issue and evidence reconciliation | Pending | Decomposition is prepared only; child correction/verification is not complete. |
| T15 | Not run | Independent child issue and evidence reconciliation | Pending | Decomposition is prepared only; child correction/verification is not complete. |
| T16 | Not run | Independent child issue and evidence reconciliation | Pending | Decomposition is prepared only; child correction/verification is not complete. |

##### Closure Evidence

- Not complete. D29 defers corrective implementation/verification. Accepted ETL processing does not establish a Passed tool correction.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #35; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #35, https://github.com/jeonghanlee/ansible-provision/issues/35
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:11:56Z
- Historical Original Body SHA256: 7ec602ee63c6a55ac10a79e54ac6af08dec019bc109d34976c76641484c3bbfd
- Historical Retired Body SHA256: 20cac5c83b898cec983521fda96ac63e60ad10bc525a3d7d35f785d28565d632

#### M31 - Preserve kernel cursor refusal evidence and prove interval coverage

- Origin: 38560eb / M31
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #36 is closed not_planned at 2026-10-17T01:12:02Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The frozen collector used by the completed full-day observations refused a previous cursor in 240 shortened and 237 default full-window samples without retaining the failed query output. Those original records cannot distinguish an obsolete pre-window anchor from a missing required kernel interval.

##### Scope

Identify the historical frozen collector and the current candidate by their own complete manifests and source hashes. Preserve the existing checkpoint-output change, complete any missing query/result/cursor metadata and verify the real refusal and interval-coverage paths. Do not clear a cursor or invent missing historical output.

Affected source: `tests/archiver-soak/etl-pass/collect.py`.

Out of scope: ETL terminal verdict isolation, JFR matching, and reconstructing missing historical query bytes.

##### Root Cause

The affected frozen version of `collect_kernel()` required the first query entry to equal the previous cursor and raised before preserving the failed query stdout/stderr. That historical mechanism must not be attributed unchanged to the current repository candidate.

##### Current Source And Remaining Verification

The repository candidate at 3ff784e has collector SHA256 7444a7b2f0d2383b7d77cfdad1f5511e3b6e0d4cb23c5b1b651d309e3bd0db7b and writes `kernel-checkpoint-journal.jsonl` and `kernel-checkpoint-journal.stderr` before rejecting an unavailable cursor. This source change is present; it does not establish actual refusal-path verification, complete query/return-code/cursor metadata or required-interval coverage. The historical output remains unavailable.

##### Completion Criteria

- [ ] Historical frozen tools and the current candidate are identified separately by complete manifests/source hashes; the existing checkpoint-output change is distinguished from unverified behavior.
- [ ] A real refused candidate query preserves stdout/stderr, return code, original arguments and cursor/interval metadata.
- [ ] An actual obsolete-anchor case with independently proved required coverage is distinguished from a real or unresolved required-interval gap.
- [ ] Unproved coverage remains `Incomplete` or `Failed`; original full-day records and unsuccessful verdicts stay unchanged.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Verify the original and candidate identities, then run the actual candidate collector against real journal rotation/anchor cases in a separate bounded environment. Inspect persisted query outputs and interval evidence; retained historical failures explain the original defect but do not prove candidate coverage. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #36; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #36, https://github.com/jeonghanlee/ansible-provision/issues/36
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:02Z
- Historical Original Body SHA256: 835e80de97131e19c3b6e8368b82498b194c4edb60706c7a3ad25d7a9bd19843
- Historical Retired Body SHA256: 60811fe3b7a63c73ee248cd095be5d2af36a22b122f2b377a0c095b9197b4b23

#### M32 - Keep kernel diagnostics independent of the ETL terminal verdict

- Origin: 38560eb / M32
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #37 is closed not_planned at 2026-10-17T01:12:07Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

Complete actual ETL pass sets and successful physical/HTTP checks were followed by `required_pass_wait`, `final_sample` and `final_journal` findings because kernel diagnostic collection failed. The two observations contain 312/312 and 27/27 required passes.

##### Scope

Evaluate required ETL sources independently from kernel diagnostics through periodic collection, pass waiting, normal finish and replay. Keep every diagnostic finding visible.

Affected source: `tests/archiver-soak/etl-pass/observe.py`, `tests/archiver-soak/etl-pass/collect.py`, `tests/archiver-soak/etl-pass/evaluate.py`.

Out of scope: Repairing kernel cursor coverage or changing ETL application scheduling/storage.

##### Root Cause

`observe.py` rejects a nonzero journal-only collector exit before checking the available application ETL pass records. Diagnostic availability and required processing evidence are treated as the same condition.

##### Completion Criteria

- [ ] A real kernel-only diagnostic failure does not invalidate complete required application ETL evidence at pass waiting or normal finish.
- [ ] Missing required ETL evidence still refuses complete acceptance and preserves the applicable abort policy.
- [ ] The actual terminal CLI and retained-input replay agree while keeping original diagnostic and unsuccessful aggregate findings.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Execute the actual collector/terminal path with real configured evidence sources in a bounded dedicated case, then replay retained originals. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #37; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #37, https://github.com/jeonghanlee/ansible-provision/issues/37
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:07Z
- Historical Original Body SHA256: 00f908ce907c86c79151bb74fb81eb830bd1a8fbb5452cef35c6fb4339009a49
- Historical Retired Body SHA256: 67a5f3b303cd5bc4572be567ce588262d246c6e0c6150f6ee37f3e1eda178af3

#### M33 - Use timestamps accepted by systemd 239 journal queries

- Origin: 38560eb / M33
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #38 is closed not_planned at 2026-10-17T01:12:13Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The original source-availability controller in `run-etl-fault.py` passed an ISO timestamp directly to `journalctl --since`. The actual systemd 239 command returned 1 with a timestamp-parse error after a successful ETL pass and orderly shutdown.

##### Scope

Preserve the original controller failure and the existing v2 formatting change with separate source identities. Verify the real systemd 239 query against the declared UTC interval, retain the original precise boundary separately and correct only any remaining interval-selection defect. Record query rounding or filtering explicitly; command acceptance alone does not prove exact coverage.

Affected source: `tests/archiver-soak/etl-scenarios/run-etl-fault.py`, `tests/archiver-soak/etl-scenarios/run-etl-fault-v2.py`.

Out of scope: Comparing equivalent pass timestamp strings, kernel cursor recovery, and accepting missing historical query output.

##### Root Cause

The original scenario query used an application timestamp without matching the installed `journalctl` syntax. The preserved v2 source already changes this formatting, so the original parser failure and remaining boundary verification are separate.

##### Current Source And Remaining Verification

The preserved original controller has SHA256 65acfd262aface090e995dfd5dc77d5b5dba4d9dc90067721653952c8c8da378. The preserved `run-etl-fault-v2.py` has SHA256 881444b6201ded6e8d1de642d1cc4290c914dbdb3a19bfd2bceb3e54827af65a and formats the query boundary as `%Y-%m-%d %H:%M:%S UTC`. This existing whole-second formatting change is not proof that the exact declared interval or original subsecond precision is preserved. No candidate boundary-verification result is claimed here.

##### Completion Criteria

- [ ] Original and v2 controller hashes are recorded separately, and existing source formatting is distinguished from actual interval verification.
- [ ] The actual systemd 239 query accepts the candidate argument and establishes the intended interval against independently identified real records, including subsecond boundaries; any query rounding/filtering and the original precise timestamp are explicit.
- [ ] A rejected query retains its arguments, stdout/stderr and return code and is not reported as successful coverage.
- [ ] Successful ETL evidence remains separate from a query-argument error; the original failed controller record is unchanged.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Run the real installed `journalctl` against actual retained/real journal records at independently identified UTC boundaries. Compare original and v2 argument behavior, including the rejected original argument and subsecond interval edges, without rewriting original records. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #38; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #38, https://github.com/jeonghanlee/ansible-provision/issues/38
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:13Z
- Historical Original Body SHA256: 36b660c6c7e58b16dee91433701b359893c9e230b955bbcbf8a88bc6c66ffac1
- Historical Retired Body SHA256: 9c83fae39efd46158d3a1961f6c31bac174ced6e6dac2254fc76ca314c7701ba

#### M34 - Match JFR exports to the recording process and lifetime

- Origin: 38560eb / M34
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #39 is closed not_planned at 2026-10-17T01:12:18Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The final JFR belongs to one PID, but the evaluator counts CSV events from earlier JVMs too. Shortened ETL heap counts are 66304 across processes versus 59094 in the final recording; the matching-PID count is exactly 59094. Default counts similarly reconcile at 6214 rather than 6266.

##### Scope

Bind comparisons to component, PID and recording lifetime while retaining earlier-process rows and verifying their own declared scope.

Affected source: `tests/archiver-soak/etl-pass/evaluate.py`, `tests/archiver-soak/etl-pass/evidence.py`, `tests/archiver-soak/diagnostics/full-day.py`.

Out of scope: Terminal persistence order, kernel coverage, and new JVM restart fault acceptance.

##### Root Cause

The complete-recording comparison selects the component without selecting the recording PID and lifetime. All twelve component/event-kind counts per chain match within the actual final recording scope.

##### Completion Criteria

- [ ] The real evaluator and aggregator reconcile heap, collection and pause records with both chains' complete recordings using actual process/lifetime identities.
- [ ] Earlier-process records remain available; missing, conflicting, duplicated or truncated in-scope evidence still fails the real path.
- [ ] Original recordings, exports, unsuccessful verdicts and independent kernel findings remain unchanged.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M30/#35. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Execute the shipped evaluator/aggregator on retained actual multi-process recordings and real retained-input negative derivatives. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #39; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #39, https://github.com/jeonghanlee/ansible-provision/issues/39
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:18Z
- Historical Original Body SHA256: 072fce69a17ef7784b48eaf6ea512d627564c8286098e6edfce2da8bdc2b3d10
- Historical Retired Body SHA256: fc585144bc7ce08a68a5659e323594714bcc3a8e83fbf27fbfd360a40c808038

#### M35 - Persist terminal state before evaluating terminal coherence

- Origin: 38560eb / M35
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #40 is closed not_planned at 2026-10-17T01:12:25Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The initial terminal evaluation reports `coherent_manifest_and_terminal`, but executing the unchanged native evaluator after final persistence removes that finding on both completed observations.

##### Scope

Make terminal persistence and evaluation consistent while preserving crash visibility, interrupted writes, repeated-terminal refusal and the original evidence.

Affected source: `tests/archiver-soak/etl-pass/observe.py`, `tests/archiver-soak/etl-pass/evaluate.py`, `tests/archiver-soak/etl-pass/aggregate.py`.

Out of scope: JFR process selection, source-access fault production, and reopening accepted ETL functionality.

##### Root Cause

`observe.py` calls the evaluator before writing `shutdown.json` or `abort.json`; the aggregate reader sees only the started marker.

##### Completion Criteria

- [ ] A real normal terminal invocation and subsequent replay agree on the exact terminal state being evaluated.
- [ ] Actual failure/interruption and repeated-terminal cases retain failure visibility and do not dispatch another stop.
- [ ] No unverified successful terminal is written to bypass coherence checks; original completed observation bytes remain unchanged.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M30/#35. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Exercise the shipped terminal CLI in bounded real normal/failure/repeat cases and replay each actual retained terminal. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #40; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #40, https://github.com/jeonghanlee/ansible-provision/issues/40
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:25Z
- Historical Original Body SHA256: 8d5c3f69533a0cabb079b2a033dda5bb59103ec47d462dc7caf31633ccd89da3
- Historical Retired Body SHA256: 7e07ab771198fbd86242b2f9f86faf7ccb71da6c4c9169d1bed4ea21bbf9a403

#### M36 - Match ETL pass times by UTC instant with nanosecond precision

- Origin: 38560eb / M36
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #41 is closed not_planned at 2026-10-17T01:12:30Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

Actual fault-case pass records use `Z`, while the declaration uses `+00:00`. Literal comparison finds zero matches; the shipped nanosecond parser finds one successful 903-job pass at the same instant.

##### Scope

Use the shipped nanosecond timestamp parser for pass selection and ordering while retaining original timestamp strings.

Affected source: `tests/archiver-soak/etl-scenarios/run-etl-fault.py`, `tests/archiver-soak/etl-scenarios/run-etl-fault-v2.py`, `tests/archiver-soak/etl-scenarios/replay-etl-fault.py`, `tests/archiver-soak/etl-pass/evidence.py`.

Out of scope: Formatting `journalctl` arguments, repairing JFR scope, or claiming full-day duration for short fault cases.

##### Root Cause

The runtime/scenario checker compares timestamp text instead of its UTC instant. This produced unsuccessful controller findings independently of actual ETL processing.

##### Completion Criteria

- [ ] Actual source-availability and automatic-abort records select exactly the matching transition, invocation and UTC instant.
- [ ] Nanosecond differences, wrong invocation, duplicate matches and genuinely missing passes remain detectable.
- [ ] Runtime/scenario and frozen replay paths agree without rewriting an original controller verdict or timestamp.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M30/#35. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Run the real checker/replay paths over retained fault-case inputs and real retained-record derivatives with changed identities/times. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #41; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #41, https://github.com/jeonghanlee/ansible-provision/issues/41
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:30Z
- Historical Original Body SHA256: 4c6f0a297ce7095013b18d3579a02256c1221f5c699388c96d8230f70813b667
- Historical Retired Body SHA256: d4047244760114c545b1fabb6c27995c14eb92741a835e794109e58ff13182aa

#### M37 - Refresh preserved-tool checksums

- Origin: 38560eb / M37
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #56, https://github.com/jeonghanlee/ansible-provision/issues/56
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #42 is closed not_planned at 2026-10-17T01:13:17Z; unfinished criteria are tracked in #56. Original issue references below are historical and do not create an active source-issue dependency.
- Status: In progress

##### Summary

The parent source manifest at `19264a9a87194dc0302512ce4251ebea0ef1bc24` had three deliberately removed source paths, sixteen hash mismatches and twenty current sources omitted across the existing manifests. The local correction covers all current Git-managed source members independently of immutable observation bundles.

##### Scope

Define the current source scope and regenerate/check the repository source manifest independently of each observation's immutable frozen bundle.

Affected source: `tests/archiver-soak/README.md`, its parent `SHA256SUMS` and `docs/test-tool-reuse-summary.md`; remove the duplicate uncommitted local checker/suite after backup. The two child source manifests are checked but remain unchanged. The shared checker is owned by dev-env at `4c633385302cea3dcbc5b1c0f37f6eb8b6104b91`.

Out of scope: Changing installed observation bundles, repairing collectors/evaluators, or altering accepted functionality results.

##### Root Cause

The prior manifest retained journal modules removed by ETL/Journal separation and older tool hashes; its membership differed from the current reusable source sets.

##### Completion Criteria

- [x] The real checksum CLI verifies every current entry and declared required source.
- [x] Missing, omitted, duplicate, removed or deliberately changed actual source files are detected.
- [x] Private runtime data and original observation manifests are never regenerated or included.

##### Dependencies And Decisions

- D35; Decision Date: 2026-10-18. Reuse the committed common checker directly; remove the two uncommitted local implementations after verified private backup. Historical local results remain distinct from current shared-checker integration.
- D34; Decision Date: 2026-10-16. Reactivate checksum work only. Replace the parent repository source manifest with current-source hashes; retain its prior state in Git. Keep this independent tool work outside the release tally. Other tool components remain deferred.
- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: 2026-10-16 for option 1; 2026-10-18 for the D35 amendment removing duplicate local implementations and using the common checker with the same project coverage.
- Implementation Authorization: 2026-10-16 for the checksum component; 2026-10-18 for the explicitly requested D35 deduplication. No other shared-tool implementation is authorized.
- Superseded Plan Artifacts: generic draft retained at `19264a9a87194dc0302512ce4251ebea0ef1bc24`; pre-deduplication plan and both local scripts retained in `work/source-checker-dedup-fu6jzviu/before/`.

1. Preserve the current source hashes and actual native checksum results in private evidence. Establish that the three obsolete entries were deliberately removed by `3ff784e7e664db35fa2ac5b72ceccd48238ebceb`.
2. Preserve and remove the uncommitted local `check-sources.py` and `test_checksums.py`. Configure the committed common `test-framework/scripts/check-sources.py` with this checkout as `--inventory-root` and all three `--manifest` paths. Keep independent Git membership, canonical regular-file paths and native checksum verification; add no local wrapper or duplicate suite.
3. Document complete source coverage in `tests/archiver-soak/README.md` and regenerate only the parent `SHA256SUMS`. Cover every current source file and both child manifests; exclude only the parent manifest itself. Preserve child manifest bytes, frozen bundle/source identities and all original runtime evidence.
4. Run bounded project integration through the actual common checker on the complete checkout and separately retained real source copies. Verify missing/omitted/duplicate/stale/changed entries, unsafe paths, symlinks and preserved originals. Generic regressions remain owned by the common skill; preserve project invocation receipts privately. Repository landing and GitHub updates need separate authorization.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Current source integrity | Run the shared checker with the declared project inventory and three manifests, plus native `sha256sum --check --strict` in each manifest directory. | Control host, current Git-managed reusable sources | All required source members covered exactly once per manifest and all three native checksum checks pass. |
| T2 | CLI regression | Run the shared shipped CLI on separately retained copies of actual project sources, plus real native checksum calls. Include omissions/deletions hidden by native checksum success. The generic suite remains in the common skill. | Control host, temporary real source copies | Intact copies pass; missing, omitted, duplicate, stale, changed, malformed or unsafe inputs fail with an explicit reason. |
| T3 | Preservation | Compare all pre-existing non-target source hashes with the private baseline, including both child manifests, `etl-pass/bundle.json` and `journal-validation/source.json`. Inspect the changed path list. | Original checkout and private `work/checksum-refresh-22lovz11/baseline.json` | Only the declared README/source manifest, reuse summary, duplicate-script removals and scoped canonical records change; no installed observation, private runtime input or frozen manifest is rewritten. |
| T4 | Shared checker integration | Verify the common package against its carrying commit; run the documented project invocation and bounded real-copy fault matrix; compare originals and other canonical details with the pre-deduplication backup. | Control host and retained real project source copies | Complete three-manifest coverage passes; declared faults fail for the expected reason; removed scripts are backed up and all non-target/frozen sources remain unchanged. |

##### Verification Results

Historical T1-T3 below describe the pre-deduplication local implementation and remain unchanged. T4 records the current common-checker integration separately.

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-10-17T06:51:10.441861+00:00 | Control host, Python 3.13.5, actual current source checkout and GNU checksum CLI | Passed locally | Parent manifest verifies 98 files, including both unchanged child manifests; child checks verify 5 and 17 files. The shipped checker establishes complete Git membership and all three native CLI checks return 0. Actual pre-correction checker returns 1 with obsolete entries, missing members and the original hash mismatches. Receipts: `work/checksum-refresh-22lovz11/current-checks.json`, `work/checksum-refresh-22lovz11/legacy-check.json`, `work/checksum-refresh-22lovz11/source-members.json`. |
| T2 | 2026-10-17T06:51:11.352350+00:00 | Control host, isolated copies of actual shipped source files; shipped checker subprocess and native checksum CLI, without internal substitutes | Passed locally | All 12 tests pass. Actual changed sources, missing files, omitted and duplicate entries, deleted source plus deleted entry, stale entries, missing child manifest, malformed entries, path escape and symlinks are rejected. Omitted/duplicate/deleted-entry cases establish checker failure even when native checksum verification succeeds. Intact source copies pass; private/frozen copy contents remain unchanged. Receipt: `work/checksum-refresh-22lovz11/regressions.json`. |
| T3 | 2026-10-17T06:51:52.341111+00:00 | Original source checkout and baseline carrying commit | Passed locally | All 95 pre-existing non-target source files are byte-identical to the baseline, including both child manifests, `etl-pass/bundle.json` and `journal-validation/source.json`. All 53 other canonical work details remain unchanged. Only the parent README/source manifest, new checker/tests and these scoped work records change. Receipt: `work/checksum-refresh-22lovz11/preservation.json`; baseline: `work/checksum-refresh-22lovz11/baseline.json`. |
| T4 | 2026-10-18T18:02:02.562508+00:00 | Control host; committed shared checker and actual checkout/retained project copies | Passed locally | All 19 declared project integration cases meet expected outcomes; 70 real command receipts retain stdout/stderr/status and input identities. Parent coverage is 96 members; child coverage is 5/17. Both documented Bash invocations pass. All 95 non-target sources, both child manifests, frozen identities and 53 other canonical details are unchanged; both removed scripts are backed up. Shared package bytes match dev-env `4c633385302cea3dcbc5b1c0f37f6eb8b6104b91`. Receipts: `work/source-checker-dedup-fu6jzviu/integration.json`, `documented-commands.json` and `preservation.json` in the same directory. |

##### Closure Evidence

- Historical local T1-T3 checks passed under D34; current shared-checker integration and preservation passed as T4 under D35; completion criteria above describe those observed checks. Original runtime observations and accepted ETL/Journal/Buffer conclusions are unchanged.
- Status remains In progress pending a separately authorized source commit/landing and checksum-only issue update. No GitHub checkbox, issue closure or other shared-tool completion is claimed.

##### GitHub Projection

- Title: `Track shared test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #56, https://github.com/jeonghanlee/ansible-provision/issues/56
- Projection Scope: Component contract from historical source #42; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:45Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Projection Difference: local checksum implementation/criteria are verified; the published issue body remains unchanged pending separate Issue authorization.
- Prepared Body: `work/issue-tools-shared.md`
- Published Body SHA256: 991316dabf5a9f3ac639c6550aa1a090cd16b43f0aa719c0e0afa8f477e906c2
- Historical Source Issue: #42, https://github.com/jeonghanlee/ansible-provision/issues/42
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:13:17Z
- Historical Original Body SHA256: 91f87e0eec44f033d9584ab0ad3b92f6e266d1183deeb73b070aa2c6f316fa49
- Historical Retired Body SHA256: 443f83435287c3ec1cdefc9769116c01069ec1a12568dc429dbb0b7ff4ea6d81

#### M38 - Finish ETL tool independence checks across both store chains

- Origin: 38560eb / M38
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #43 is closed not_planned at 2026-10-17T01:12:35Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The shortened failing-module and importable-change cases have actual preparation, capture, planned-abort and matching guest/recipient evidence. The complete absent/failing/changed matrix, particularly default variants and remaining terminal paths, is not established.

##### Scope

Complete the six declared normal-finish independence cases and exact recipient replays, preserving the two recorded shortened planned-abort results. Implement or integrate the absent-study and normal-finish candidate paths that the preserved payloads do not yet support; identify them separately from original executed sources.

Affected source: `tests/archiver-soak/etl-scenarios/apply-journal-challenge.py`, `tests/archiver-soak/etl-scenarios/run-etl-independence-v2.py`, `tests/archiver-soak/etl-scenarios/replay-etl-independence.py`, `tests/archiver-soak/etl-scenarios/run.py`, `tests/archiver-soak/etl-pass/observe.py`, `tests/archiver-soak/etl-pass/contract.py`.

Out of scope: Partial/all-source availability faults, journal acceptance, or another full-day producer run solely for this tool matrix.

##### Case Matrix

The required normal-finish scope is exactly two chains (`shortened` and `default`) times three unrelated-study states: absent, failing import and importable change. Each of the six normal-finish cases covers preparation, start, collection, normal terminal handling, restoration and exact recipient replay with an unchanged native ETL dependency bundle. The separately recorded planned-abort cells describe existing evidence; they do not substitute for normal finish or silently add four new planned-abort runs to this issue.

| Chain | Unrelated Study State | Recorded Planned-Abort Scope | Normal-Finish Case | Normal-Finish Recipient Replay |
| --- | --- | --- | --- | --- |
| shortened | absent | Not run | Not run | Not run |
| shortened | failing | Recorded Passed: preparation/start/capture/abort/restoration and exact guest/recipient replay | Not run | Not run |
| shortened | changed | Recorded Passed: preparation/start/capture/abort/restoration and exact guest/recipient replay | Not run | Not run |
| default | absent | Not run | Not run | Not run |
| default | failing | Not run | Not run | Not run |
| default | changed | Not run | Not run | Not run |

##### Execution Support

The preserved `apply-journal-challenge.py`, `run-etl-independence-v2.py` and `replay-etl-independence.py` currently implement only the failing-import and importable-change planned-abort paths. The absent challenge and normal-finish scenario/replay support remain to be implemented or integrated as separately identified candidate paths. Absence applies to the unrelated study subject outside the native ETL bundle; it never removes a required ETL dependency. Before any future execution, declare the real installed normal-finish CLI, supported bounded observation contract and expected terminal findings without changing an original clock, duration or terminal record. Preserve the original executed payloads and frozen observation identities.

##### Recorded Scope

The shortened failing-import planned-abort case was recorded on 2026-10-14 with archive SHA256 75626ead8368bce2733af77bd6493945c1642a9c45e0a4f1a227563ced7b9e25. The shortened importable-change planned-abort case was recorded on 2026-10-14 with archive SHA256 8e91244ba5dc61f3b01656d0d628f3561ffe50e9fe80dd0842124d9e57822e63. Both retained preparation/start/capture, orderly explicit abort, restoration and exactly matching guest/recipient scenario results with the same 23-file schema-6 native bundle SHA256 4ec0987e3a788a44dbd6173ffdb3e41ef47074b87e9f33ffbfbc351612053f9d. Their original short native observations remain `Incomplete`; no normal-finish case is established by these records.

##### Verdict And Exit Codes

Tool acceptance is the scenario expectation plus the specific invariants below, not equality of two unsuccessful runs. The immutable historical controller record keeps its recorded exit code and result; the requirements for a corrected candidate are prospective and do not rewrite that record.

| Command Or Result | Expected Exit Code | Required Meaning |
| --- | --- | --- |
| Historical runtime/controller record | Keep the recorded code | Preserve the original result, bytes and tool identity; never relabel a historical controller failure as success |
| Corrected candidate runtime/controller | 0 | All declared runtime assertions, source restoration and native terminal capture complete; the controller may leave its expectation Pending until scenario verification |
| Short-case native abort CLI | 1 | `terminal_kind=abort`, `verdict=Incomplete`, no terminal capture errors and actual appliance stop rc 0 |
| Short-case native evaluator and aggregator | 1 for each CLI | Preserve the exact `Incomplete` verdict and declared original findings for the deliberately shortened observation; no full-day acceptance is inferred |
| Scenario verifier and independent recipient replay | 0 for each CLI | `expectation=Passed` on both sides, all scenario assertions satisfied and exact complete results/identities reproduced |

A wrong exit code, a failed scenario assertion, unavailable required verification evidence or an unexplained result difference prevents tool completion even if both sides fail identically. Record expected native missing/failed checks separately from scenario failures. Keep the accepted ETL behavior distinct from a controller, collection or replay error.

For a normal-finish case, declare and verify `terminal_kind=finish`, actual appliance stop rc 0, restoration and the exact terminal state evaluated by replay. The native terminal/evaluator/aggregator exit code must match its saved verdict: 0 for `Passed` and 1 for `Incomplete` or `Failed`. Unrelated native findings remain visible and separately identified; this independence issue does not require them to disappear. The candidate scenario verifier and recipient replay themselves must exit 0 and report `expectation=Passed` for the declared independence assertions. Do not apply a shortened-abort expected result to a normal finish.

##### Completion Criteria

- [ ] All six chain/study-state normal-finish rows have actual preparation/start/capture/normal-terminal/restoration and exact recipient replay evidence; recorded planned-abort results remain separately identified.
- [ ] The unrelated subject is actually absent, fails import or remains importable after its declared change as applicable; the complete native ETL dependency bundle and actual runtime identities remain unchanged throughout each case.
- [ ] Candidate support for absent-study and normal-finish paths is identified separately; no preserved planned-abort payload or result is relabeled normal finish.
- [ ] Scenario verification and recipient replay each exit 0 with `expectation=Passed` and satisfy the declared assertions; matching failed runs alone never complete a row.
- [ ] Native terminal/evaluator/aggregator exit codes and saved verdicts follow the explicit short-abort or normal-finish contract, while original bytes and unsuccessful findings remain unchanged.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

Use the six-row scope matrix and preserve the two recorded planned-abort evidence sets. After separate execution authorization and candidate-path preparation, run each real normal-finish case through preparation/start/capture/terminal/restoration and exact independent-recipient scenario replay. Check every actual CLI receipt against the separate scenario/native verdict contract; reuse retained inputs without rewriting originals.

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | shortened / absent / normal finish | Real preparation/start/capture/normal terminal/restoration and exact independent-recipient replay with the declared absent unrelated-study state on the shortened chain. Required ETL dependencies stay unchanged; scenario expectation Passed and actual CLI receipts satisfy the verdict contract. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T2 | shortened / failing / normal finish | Real preparation/start/capture/normal terminal/restoration and exact independent-recipient replay with the declared failing unrelated-study state on the shortened chain. Required ETL dependencies stay unchanged; scenario expectation Passed and actual CLI receipts satisfy the verdict contract. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T3 | shortened / changed / normal finish | Real preparation/start/capture/normal terminal/restoration and exact independent-recipient replay with the declared changed unrelated-study state on the shortened chain. Required ETL dependencies stay unchanged; scenario expectation Passed and actual CLI receipts satisfy the verdict contract. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T4 | default / absent / normal finish | Real preparation/start/capture/normal terminal/restoration and exact independent-recipient replay with the declared absent unrelated-study state on the default chain. Required ETL dependencies stay unchanged; scenario expectation Passed and actual CLI receipts satisfy the verdict contract. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T5 | default / failing / normal finish | Real preparation/start/capture/normal terminal/restoration and exact independent-recipient replay with the declared failing unrelated-study state on the default chain. Required ETL dependencies stay unchanged; scenario expectation Passed and actual CLI receipts satisfy the verdict contract. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T6 | default / changed / normal finish | Real preparation/start/capture/normal terminal/restoration and exact independent-recipient replay with the declared changed unrelated-study state on the default chain. Required ETL dependencies stay unchanged; scenario expectation Passed and actual CLI receipts satisfy the verdict contract. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T7 | Scenario/native result distinction | Check actual candidate controller, scenario verifier, replay and native terminal/evaluator/aggregator receipts against the separate short-abort or normal-finish verdict contract; matching failures never establish scenario success. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T2 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T3 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T4 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T5 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T6 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T7 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #43; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #43, https://github.com/jeonghanlee/ansible-provision/issues/43
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:35Z
- Historical Original Body SHA256: fcdb081256da410989e1c4839859f6590da0f3b6422a2ffed41fcaa82288dcf8
- Historical Retired Body SHA256: f92276ed6c8cb16d1acf9a4d7e2107d172a23ded4eab75dd1e6ee30b228ad61e

#### M39 - Finish partial-source ETL evidence verification on both chains

- Origin: 38560eb / M39
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #44 is closed not_planned at 2026-10-17T01:12:41Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The shortened journal-unavailable/application-file-available case retained two actual fault samples, one successful 903-job pass, no automatic abort, source restoration and orderly stop. Exact completed scenario replay and the default variant remain unverified.

##### Scope

Complete the remaining actual partial-source controller/scenario verification and exact recipient replay on both chains. Preserve the accepted shortened source-availability behavior and original unsuccessful controller record, and judge corrected tool execution with a separate explicit verdict/exit-code contract.

Affected source: `tests/archiver-soak/etl-scenarios/run-etl-fault-v2.py`, `tests/archiver-soak/etl-scenarios/replay-etl-fault.py`, `tests/archiver-soak/diagnostics/source-available.py`.

Out of scope: All-sources-unavailable abort behavior, default behavior inferred from shortened evidence, and reopening ETL data-processing acceptance.

##### Verdict And Exit Codes

Tool acceptance is the scenario expectation plus the specific invariants below, not equality of two unsuccessful runs. The immutable historical controller record keeps its recorded exit code and result; the requirements for a corrected candidate are prospective and do not rewrite that record.

| Command Or Result | Expected Exit Code | Required Meaning |
| --- | --- | --- |
| Historical runtime/controller record | Keep the recorded code | Preserve the original result, bytes and tool identity; never relabel a historical controller failure as success |
| Corrected candidate runtime/controller | 0 | All declared runtime assertions, source restoration and native terminal capture complete; the controller may leave its expectation Pending until scenario verification |
| Short-case native abort CLI | 1 | `terminal_kind=abort`, `verdict=Incomplete`, no terminal capture errors and actual appliance stop rc 0 |
| Short-case native evaluator and aggregator | 1 for each CLI | Preserve the exact `Incomplete` verdict and declared original findings for the deliberately shortened observation; no full-day acceptance is inferred |
| Scenario verifier and independent recipient replay | 0 for each CLI | `expectation=Passed` on both sides, all scenario assertions satisfied and exact complete results/identities reproduced |

A wrong exit code, a failed scenario assertion, unavailable required verification evidence or an unexplained result difference prevents tool completion even if both sides fail identically. Record expected native missing/failed checks separately from scenario failures. Keep the accepted ETL behavior distinct from a controller, collection or replay error.

##### Completion Criteria

- [ ] Actual journal failure with all required configured application files available preserves ETL pass evidence and does not trigger an evidence-loss abort.
- [ ] Both chains have declared fault/recovery boundaries, real sampler identity, exact restoration and actual bounded stop evidence.
- [ ] Corrected candidate runtime/controller execution exits 0 with complete runtime evidence; historical controller errors and their original exit codes remain unchanged.
- [ ] The scenario verifier and independent recipient replay each exit 0 with `expectation=Passed`, satisfy all declared source-availability assertions and reproduce exact complete results/identities; equality of two failed checks is insufficient.
- [ ] The deliberately shortened native abort/evaluator/aggregator retains its exact `Incomplete` verdict and expected exit code 1, with actual appliance stop rc 0; no full-day acceptance is claimed.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Shortened retained behavior and candidate verification | Use retained actual shortened inputs and separately authorized default-case inputs with the preserved source-access paths and separately identified candidate fixes. Compare actual controller, terminal, evaluator, aggregator and guest/recipient scenario-verifier receipts against the explicit verdict table. A preserved historical controller error stays separate from prospective candidate acceptance and accepted ETL behavior. Preserve accepted shortened behavior separately from unexecuted corrected-controller and exact recipient claims. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T2 | Default bounded case and recipient replay | Run the actual declared default-chain scenario with separately identified candidate tools and verify all scope assertions, exact restoration and recipient equality. Scenario expectation Passed does not change the deliberately shortened native Incomplete result. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T3 | Scenario/native result distinction | Read actual per-CLI receipts and saved verdicts for both chains; candidate controller/verifier/replay success is separate from native abort/evaluator/aggregator exit code 1. Wrong codes or matching failed scenario checks do not establish completion. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T2 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T3 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #44; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #44, https://github.com/jeonghanlee/ansible-provision/issues/44
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:41Z
- Historical Original Body SHA256: 679a14a94343b77c0915a18713e4e309e41b5360fa04a7f34f89f93e8517f540
- Historical Retired Body SHA256: 06683d8b4391da23eb09cf1c0e6548c22a9492c0aff439937adc6f2e3d3b9af5

#### M40 - Finish all-source evidence loss and automatic-abort verification

- Origin: 38560eb / M40
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #45 is closed not_planned at 2026-10-17T01:12:47Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

In the shortened case, two actual unavailable-source full samples advanced critical counters from one to two and triggered exactly one automatic abort. The appliance stopped with rc 0 in 11.878 seconds and its source configuration was restored. Default behavior and exact completed recipient scenario replay remain unverified.

##### Scope

Complete the remaining both-chain evidence-loss/automatic-abort controller/scenario checks and exact recipient replay. Preserve first-failure versus repeated-failure behavior and the accepted shortened result; use explicit scenario, native-evaluation and exit-code criteria for tool completion.

Affected source: `tests/archiver-soak/etl-scenarios/etl-fault-sampler.py`, `tests/archiver-soak/etl-scenarios/run-etl-fault-v2.py`, `tests/archiver-soak/diagnostics/automatic-abort.py`.

Out of scope: Partial-source operation, another full-day producer run, or treating unavailable test evidence as an ETL data-loss finding.

##### Verdict And Exit Codes

Tool acceptance is the scenario expectation plus the specific invariants below, not equality of two unsuccessful runs. The immutable historical controller record keeps its recorded exit code and result; the requirements for a corrected candidate are prospective and do not rewrite that record.

| Command Or Result | Expected Exit Code | Required Meaning |
| --- | --- | --- |
| Historical runtime/controller record | Keep the recorded code | Preserve the original result, bytes and tool identity; never relabel a historical controller failure as success |
| Corrected candidate runtime/controller | 0 | All declared runtime assertions, source restoration and native terminal capture complete; the controller may leave its expectation Pending until scenario verification |
| Short-case native abort CLI | 1 | `terminal_kind=abort`, `verdict=Incomplete`, no terminal capture errors and actual appliance stop rc 0 |
| Short-case native evaluator and aggregator | 1 for each CLI | Preserve the exact `Incomplete` verdict and declared original findings for the deliberately shortened observation; no full-day acceptance is inferred |
| Scenario verifier and independent recipient replay | 0 for each CLI | `expectation=Passed` on both sides, all scenario assertions satisfied and exact complete results/identities reproduced |

A wrong exit code, a failed scenario assertion, unavailable required verification evidence or an unexplained result difference prevents tool completion even if both sides fail identically. Record expected native missing/failed checks separately from scenario failures. Keep the accepted ETL behavior distinct from a controller, collection or replay error.

##### Completion Criteria

- [ ] The first actual critical sample does not prematurely abort; the declared consecutive failure triggers exactly one native abort.
- [ ] Both chains retain real source-access failure, sampler/process identity, counter sequence, actual appliance stop rc 0 and exact restoration evidence.
- [ ] Corrected candidate runtime/controller execution exits 0 with complete runtime evidence; historical controller errors and their original exit codes remain unchanged.
- [ ] The scenario verifier and independent recipient replay each exit 0 with `expectation=Passed`, satisfy all declared counter/abort/restoration assertions and reproduce exact complete results/identities; equality of two failed checks is insufficient.
- [ ] The deliberately shortened native abort/evaluator/aggregator retains its exact `Incomplete` verdict and expected exit code 1; source unavailability and successful automatic abort are not relabeled an ETL data-loss failure or full-day acceptance.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Shortened retained behavior and candidate verification | Use the actual fault sampler, native automatic-abort unit and retained state history with separately identified candidate controller/replay fixes. Verify each chain through actual two-failure/single-abort/restoration evidence and exact recipient replay; classify actual CLI receipts with the explicit verdict table while preserving original unsuccessful controller/native records. Preserve accepted shortened behavior separately from unexecuted corrected-controller and exact recipient claims. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T2 | Default bounded case and recipient replay | Run the actual declared default-chain scenario with separately identified candidate tools and verify all scope assertions, exact restoration and recipient equality. Scenario expectation Passed does not change the deliberately shortened native Incomplete result. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |
| T3 | Scenario/native result distinction | Read actual per-CLI receipts and saved verdicts for both chains; candidate controller/verifier/replay success is separate from native abort/evaluator/aggregator exit code 1. Wrong codes or matching failed scenario checks do not establish completion. | Retained actual inputs and separately authorized bounded dedicated environment | Scoped scenario assertions and exact recipient comparison established; original evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T2 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |
| T3 | Not run | Scoped future candidate/recipient verification | Pending | Existing accepted behavior remains recorded separately; no new candidate case or exact recipient execution is claimed. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #45; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #45, https://github.com/jeonghanlee/ansible-provision/issues/45
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:47Z
- Historical Original Body SHA256: 3a356bbe83dadf95f19be431971c08cf8818e19acebb8b8ed725e57cedcd5b87
- Historical Retired Body SHA256: ffb6f5413fb7c396794f67c46de26f1d2f16e726ecc389df88837b5b926d94f4

#### M41 - Verify ETL collector capture and refusal after normal shutdown

- Origin: 38560eb / M41
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #46 is closed not_planned at 2026-10-17T01:12:52Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

Successful whole-appliance stops are already recorded, but the separate ETL collection-tool contract for final/post-stop application-file capture, process identity and repeated terminal requests is not complete.

##### Scope

Verify actual ETL collector and terminal behavior before/after normal stop and on a repeated request using separately retained inputs.

Affected source: `tests/archiver-soak/etl-pass/pass_source.py`, `tests/archiver-soak/etl-pass/collect.py`, `tests/archiver-soak/etl-pass/observe.py`.

Out of scope: The separate journal collector verification in #32, product shutdown optimization, and another full-day producer run.

##### Completion Criteria

- [ ] Actual final/post-stop capture retains all required application-file bytes with the original invocation, PID, inode and prefix identity.
- [ ] A changed invocation, wrong PID, truncation or missing final record refuses complete evidence.
- [ ] Repeated terminal invocation dispatches no second stop and leaves original evidence unchanged; real replay reproduces the result.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Run the actual collector, terminal CLI and source reader around a bounded real appliance stop and repeated request. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #46; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #46, https://github.com/jeonghanlee/ansible-provision/issues/46
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:52Z
- Historical Original Body SHA256: 2c32ca81c2ec2a29b7e7f5752bc4f953cd8267fa3551ed42eec5c328eea0b0de
- Historical Retired Body SHA256: 10bc62d816a02e3c0a4c03b927fa73253c52d5a2f959a68b1ab75f19ed62248e

#### M42 - Verify real collection during source-store deletion

- Origin: 38560eb / M42
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #47 is closed not_planned at 2026-10-17T01:12:57Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The shipped parser correctly consumed an actual retained deletion-race command result with rc 1 and a valid size, but that retained-input check does not recreate live collection during source-file removal.

##### Scope

Complete the bounded real collector/storage race check with actual process/request timing, measured outputs and preserved command results.

Affected source: `tests/archiver-soak/etl-pass/collect.py`, `tests/archiver-soak/etl-pass/test_contract.py`.

Out of scope: New ETL storage-failure product tests, forcing data loss in accepted observations, or classifying normal metrics overlap as a defect.

##### Completion Criteria

- [ ] A real source-file removal overlaps the native collector measurement and the overlap is independently recorded.
- [ ] Measured surviving sizes and actual command status are preserved; a tolerated disappearing file does not hide unrelated command failures.
- [ ] The actual collected result and frozen retained-input evaluation agree without reconstructed stdout or internal substitutes.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M29/#34. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Execute the actual collector while source-store deletion occurs in a dedicated bounded case, then replay its real command result. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #47; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #47, https://github.com/jeonghanlee/ansible-provision/issues/47
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:12:57Z
- Historical Original Body SHA256: f330f7e241e52434b11e6b3e1ac6e625235a29d42b1d23ce0feabc5c5ab03f9b
- Historical Retired Body SHA256: 840a69b06211751b9a83bca9f0d84c8578ac9bc19ca153cb165edc423fce6f0c

#### M43 - Reconcile retained ETL measurements and process identities

- Origin: 38560eb / M43
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #48 is closed not_planned at 2026-10-17T01:13:02Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

Actual complete observations and raw measurements exist, but the supplemental per-component numerical reconciliation is unfinished. The three shortened metrics request overlaps have zero metric failed assertions and zero metric missing coverage; they are not three failed comparisons.

##### Scope

Produce one reproducible per-component report from retained actual heap, GC cause/pause, jstat, RSS, observed input/event counts and rates, retrieval freshness/visibility, request bounds and process identity/gap/OOM evidence. Keep unknown historical fields explicit.

Affected source: `tests/archiver-soak/etl-pass/aggregate.py`, `tests/archiver-soak/etl-pass/measure.py`, `tests/archiver-soak/etl-pass/rate-semantics.json`, `tests/archiver-soak/diagnostics/full-day.py`.

Out of scope: Changing ETL functionality acceptance, rewriting raw measurements, or a fresh full-day producer run solely for reporting.

##### Completion Criteria

- [ ] Per-component heap, GC cause and pause, jstat, RSS and observed input/event counts and rates reconcile with actual process/lifetime identities and time ranges; units, provenance and rate denominators are explicit.
- [ ] Retrieval freshness and visibility are reported with actual query/request/response bounds. Process identity continuity, evidence gaps and OOM or forced-termination findings are reported explicitly; absent evidence is not recorded as zero events or complete coverage.
- [ ] Actual request/pass overlaps, accumulation and process changes are evaluated from retained records and remain distinct from failed assertions.
- [ ] Configured rates and array capacity are never used as observed event counts or actual lengths; missing data is stated rather than invented.
- [ ] Retained-input and bounded real measurement regressions cover accumulation, process restart and pass-end/request overlap; actual coverage and unresolved cases remain explicit.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M30/#35. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Run the shipped native numerical readers/aggregator on completed actual observations and account explicitly for every declared report field. Keep retained-input reporting separate from separately authorized bounded real accumulation/restart/overlap regression cases; neither internal substitutes nor a fresh full-day producer run establish this report. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #48; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #48, https://github.com/jeonghanlee/ansible-provision/issues/48
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:13:02Z
- Historical Original Body SHA256: e2b7d61eed476c033e4c015e40b0c3be806f6163a70733ee8e8b43afcb73ba6f
- Historical Retired Body SHA256: d6d54f47924b44edf42db1f6d17ca50fe4dcc85e7ce640ccd063191f8519629d

#### M44 - Compare ETL busy time and workload with retained earlier results

- Origin: 38560eb / M44
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #49 is closed not_planned at 2026-10-17T01:13:07Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The deployment verification originally requested comparison with the earlier 0.69-second average and 0.18-percent weekly usage. That supplemental comparison has not been completed.

##### Scope

Compare last/average busy time and weekly usage using consistent intervals and explicit population, source-rate, concurrency, store-age and resource differences.

Affected source: `tests/archiver-soak/etl-pass/aggregate.py`, `tests/archiver-soak/etl-pass/rate-semantics.json`.

Out of scope: ETL functionality acceptance, host sizing, capacity forecasts, or new data production solely to make a comparison.

##### Completion Criteria

- [ ] The report uses the actual pinned metric meanings and comparable observed intervals; the retired running-sum interpretation is excluded.
- [ ] Workload and fixture differences are explicit, including absent comparable historical rates.
- [ ] No improvement/regression claim is made when the retained inputs cannot support it; no missing measurement is replaced by a prediction.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M30/#35. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Compare actual completed-observation reports with retained earlier workload evidence through the shipped numerical aggregation path. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #49; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #49, https://github.com/jeonghanlee/ansible-provision/issues/49
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:13:07Z
- Historical Original Body SHA256: 9896b1e567fe7f077d8ca5322b0b4f927c98c13bbc7b1e3948d76696274678d7
- Historical Retired Body SHA256: 3966f8cec6467e18e4cd53129a11879aa0a963e978d5099e8f5312438940cb5e

#### M45 - Reproduce completed ETL observation reports on an independent recipient

- Origin: 38560eb / M45
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #50 is closed not_planned at 2026-10-17T01:13:12Z; unfinished criteria are tracked in #54. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

Both full-day ETL functionality results are accepted from real retained evidence, but exact independent-recipient reproduction of the complete full-day JSON and numerical reports remains unfinished.

##### Scope

Freeze a per-chain comparison baseline from the unchanged finalized observation using its exact original offline evaluator and aggregator, then privately transfer the evidence, complete frozen dependencies and baseline to an independent recipient. Compare original-tool results only with that original-tool baseline; corrected candidate tools require a separate identified baseline.

Affected source: `tests/archiver-soak/etl-pass/evaluate.py`, `tests/archiver-soak/etl-pass/aggregate.py`, `tests/archiver-soak/diagnostics/full-day.py`.

Out of scope: The separate journal full-day recipient work in #33, short fault-case recipient checks, or another full-day producer run.

##### Comparison Baseline

The comparison baseline consists of the complete evaluator JSON and complete numerical-aggregator JSON produced after the original terminal file was persisted. The initial evaluation embedded in that terminal is retained as historical evidence, not used as the expected post-finalization offline result. For each chain, record the exact CLI arguments, input/member manifest, terminal hash, complete frozen tool/dependency hashes, schema and interpreter version, exit codes and output SHA256 values before transfer. Baseline generation and recipient comparison remain unexecuted follow-up work; do not invent baseline hashes or overwrite the initial result.

##### Completion Criteria

- [ ] Before transfer, freeze actual post-finalization evaluator and aggregator outputs for each chain, with the exact input/terminal identities, full tool/dependency hashes and versions, CLI arguments, exit codes and complete-output SHA256 values.
- [ ] Every declared archive member, saved baseline and frozen dependency matches before actual recipient execution.
- [ ] The recipient executes the same original frozen offline CLIs at the original declared paths and reproduces the complete baseline JSON bytes/hashes, per-check findings, numerical outputs and exit codes without normalization or rewritten inputs/identities.
- [ ] The initial embedded evaluation and original unsuccessful findings remain unchanged. Any corrected candidate has its own tool identity and post-finalization baseline; it is never compared with the original-tool baseline as if the tools were identical.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M30/#35. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | After final persistence, execute the real original frozen offline evaluator and aggregator at the declared input paths and freeze their complete outputs and identity manifest. Privately transfer and verify those inputs/baselines, then run the same CLIs in an independent isolated recipient namespace and compare exact outputs and exit codes. Keep live-service diagnostics and any corrected-candidate baseline separate. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Component contract from historical source #50; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issue: #50, https://github.com/jeonghanlee/ansible-provision/issues/50
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:13:12Z
- Historical Original Body SHA256: 35e199b23df1d8ee1ed5e96b60748e8f350d6fd6e4615339c6561b45b64d06d9
- Historical Retired Body SHA256: 2c41158ccbaa2b29033832fd69f3cdc789963fc29c5a73ea73696f5f63633c59

#### M46 - Report actual test phase durations against the agreed allocations

- Origin: 38560eb / M46
- Identity History: created by independent tool-work decomposition on 2026-10-15 (D31).
- GitHub Issue: #56, https://github.com/jeonghanlee/ansible-provision/issues/56
- Tracking Consolidation: D33, Decision Date: 2026-10-16. Historical source #51 is closed not_planned at 2026-10-17T01:13:22Z; unfinished criteria are tracked in #56. Original issue references below are historical and do not create an active source-issue dependency.
- Status: Deferred

##### Summary

The agreed schedule reserves approximately one hour for journal basics, three hours for ETL functionality, parallel full-day observations and two hours overall for the result decision. Actual preparation, waiting and analysis durations have not been consolidated against those allocations.

##### Scope

Derive the actual phase intervals from preserved UTC/monotonic execution records, separating preparation, processing, waiting, observation and result analysis.

Affected source: `tests/archiver-soak/etl-pass/observe.py`, `tests/archiver-soak/journal-validation/basic.py`, `tests/archiver-soak/journal-validation/long.py`.

Out of scope: New runtime tests, ETL or journal functionality reacceptance, and predicted durations substituted for measured intervals.

##### Completion Criteria

- [ ] Each reported duration identifies actual start/end evidence and separates simultaneous work from elapsed wall time.
- [ ] Waiting for default-chain scheduling is recorded explicitly; it is not presented as successful processing time.
- [ ] Schedule conflicts and missing boundaries are disclosed without changing the agreed allocation, shortening an observation or inventing times.

##### Dependencies And Decisions

- D31; Decision Date: 2026-10-15. Independent Backlog work is excluded from current execution; accepted M22/#30 ETL functionality and M25/#31 journal results remain complete.
- Coordination: M30/#35. This is a tracking relationship, not an invented sequential execution dependency.
- Preserve original inputs, frozen tool identities and unsuccessful outcomes. Reuse retained evidence and bounded real-path checks; no new full-day producer run solely for tool correction or reporting.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Preserve and identify actual existing inputs, original outcomes and frozen/candidate source boundaries.
2. Perform only the scoped correction or follow-up after separate execution authorization.
3. Execute the declared real path and record actual results without replacing internal path segments or rewriting original observations.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real-path tool verification | Reconcile actual controller/observation/terminal records and phase receipts already retained from the completed work. | Retained actual inputs and separately authorized bounded environment where required | All completion criteria established with explicit actual coverage; original unsuccessful evidence unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Scoped future real-path verification | Pending | Original accepted behavior explains scope only; it does not establish completion of this follow-up. |

##### Closure Evidence

- Not complete. D31 excludes this independent follow-up from current execution; no candidate correction or follow-up acceptance is claimed.

##### GitHub Projection

- Title: `Track shared test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #56, https://github.com/jeonghanlee/ansible-provision/issues/56
- Projection Scope: Component contract from historical source #51; current tracking uses its section in the consolidated issue.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:45Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-shared.md`
- Published Body SHA256: 991316dabf5a9f3ac639c6550aa1a090cd16b43f0aa719c0e0afa8f477e906c2
- Historical Source Issue: #51, https://github.com/jeonghanlee/ansible-provision/issues/51
- Historical Source State: closed
- Historical Source Reason: not_planned
- Historical Source Closed At: 2026-10-17T01:13:22Z
- Historical Original Body SHA256: 68d2900c8145b4678bfa6a18d0edae84e59146ea7d60b2d90496abc3c5efbc12
- Historical Retired Body SHA256: 9e4f63517f977731df0ca3b9839a07d230b8f38ad92c6a9fbbd9483059d5c6fd

#### M47 - Track journal test tooling

- Origin: 38560eb / M47
- Identity History: created as a test-type coordination entry on 2026-10-16 (D32); no existing identity is replaced.
- GitHub Issue: #53, https://github.com/jeonghanlee/ansible-provision/issues/53
- Status: Deferred

##### Summary

Consolidate the remaining journal test-tool work into one active issue while preserving every original acceptance condition and evidence record.

##### Scope

All remaining component work is tracked directly in this issue. Source issue references identify preserved historical records; retiring those issues does not complete their checks or require their reopening. Every unmet criterion in the transferred contracts remains active here. Journal tooling remains independent of accepted ETL functionality.

Component canonical identities remain independent under this single GitHub projection:

- M27: historical source #32; unfinished work is tracked in #53.
- M28: historical source #33; unfinished work is tracked in #53.

Source GitHub issues were retired for consolidation at 2026-10-17T01:14:10.675787+00:00. Component work is not Complete; current tracking is #53 and the retired source metadata is recorded in component details.

##### Detailed Work Summary

These summaries preserve the recorded scope. Each linked issue retains its full acceptance criteria and original evidence; a summary or group checkbox does not replace that verification.

###### #32 - Verify collector capture around normal appliance shutdown

- Problem and evidence: Normal-stop final capture and the later live journal read are unexecuted collector checks.
- Remaining work: Declare source actions and stop/read boundaries; run the shipped collector around one real normal stop.
- Done when: All required identities/content match the later live query and final archive; overlap is explained, no second stop occurs and missing evidence is distinct from confirmed loss.

###### #33 - Reproduce journal results on an independent recipient

- Problem and evidence: Full-day replay matched on the recording deployment; independent-recipient replay is unexecuted.
- Remaining work: Privately transfer actual evidence and frozen tools, verify every declared member/hash and execute the frozen replay CLI on another recipient.
- Done when: Complete JSON, per-path verdicts and comparison digest match exactly; original successful and unsuccessful records remain unchanged.

##### Existing Evidence

The full-day journal result is accepted in #31. Normal-stop/post-stop capture and independent-recipient replay remain unexecuted checks, not demonstrated journal loss. Earlier corrected health-record matching and inventory-processing failures remain historical tool findings.

##### Out Of Scope

ETL or buffer product changes, reopening #31, new full-day recording solely for tool repair, shared checksum ownership, or publishing raw records and deployment identifiers.

##### Completion Criteria

- [ ] Every transferred collector-lifecycle and independent-recipient criterion below is verified through its declared real path. Closing a source issue for consolidation satisfies no test.
- [ ] Preserve accepted journal/ETL results, immutable original inputs and unsuccessful attempts; keep missing evidence and confirmed record loss distinct.
- [ ] Record actual per-criterion evidence here without another full-day producer solely for tool repair or reproduction.

##### Transferred Acceptance Criteria

All criteria below remain active in the replacement issue. Source closure is administrative; actual verification is still required. The source scopes, evidence and real-path methods remain in their component canonical details and are copied completely into the prepared public body.

###### Source #32 - Verify collector capture around normal appliance shutdown

- [ ] Declare the real source actions, expected messages, normal-stop boundary and later direct-read condition before execution; retain actual service/process identities and command outcomes.
- [ ] Run a short independent case through the real appliance, journald and shipped collector. Confirm required records before and around the actual stop; do not replace the logging path with synthetic success markers.
- [ ] Compare every declared required identity and full content with the later successful direct journal query and combined final archive. Explain overlap explicitly and report missing, changed or repeated identities.
- [ ] Dispatch the normal stop once, retain the final collector outcome and report delivery, later visibility and terminal collection separately. Missing evidence is Incomplete and confirmed loss remains Failed.
- [ ] Preserve the completed #31 originals and unsuccessful attempts. No new 24-hour recording is a prerequisite for this lifecycle case.



###### Source #33 - Reproduce journal results on an independent recipient

- [ ] Select the retained complete actual observation, its explicitly frozen corrected tools, saved result and per-record comparison digest. Preserve the original package and earlier unsuccessful result separately.
- [ ] Transfer the necessary evidence privately and verify every declared member/hash before replay. Keep runtime configuration and raw journal records out of Git and public issue text.
- [ ] Execute the real frozen `long.py replay` CLI on a different recipient environment without contacting or operating the original appliance or using substitute records.
- [ ] Require the complete result JSON, per-path verdicts and per-record comparison digest to match the completed result exactly. Record a transfer/hash or replay error independently; do not reinterpret it as observed journal loss.
- [ ] Verify the original evidence and saved unsuccessful results remain unchanged. No new producer schedule or 24-hour waiting period is required.



##### Dependencies And Decisions

- D33; Decision Date: 2026-10-16. Consolidate GitHub tracking into four issues; copy every original contract and retire twenty source issues with reason not planned. This supersedes D32's plan to keep those twenty GitHub issues open. Independent canonical component work and future tool execution remain Deferred.
- Primary links are coordination relationships, not a new sequential execution dependency. Each existing issue retains its original criteria, source identities and evidence; no original result is rewritten.
- Accepted M22/#30 ETL and M25/#31 journal results remain complete. The completed buffer acceptance in jeonghanlee/epicsarchiverap-maven#29 remains separate.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: earlier representative-only issue projection under D32.

1. Preserve each component's original scope, criteria, evidence and source identity in this issue; use source issue links as historical provenance.
2. After separate tool-execution authorization, perform the scoped real-path corrections and checks, retaining explicit scenario/native verdicts and immutable originals.
3. Update the per-component criteria from actual results. Shared evidence may satisfy overlapping criteria without inventing duplicate campaigns.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Lifecycle | Run the real normal-stop collector and later live-query comparison specified by #32. | Separate dedicated deployment | Exact required-record equality; errors visible and no duplicate stop. |
| T2 | Recipient replay | Run the exact frozen full-record CLI and private member verification specified by #33. | Independent recipient | Complete result and digest match; original inputs unchanged. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Separate dedicated deployment | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |
| T2 | Not run | Independent recipient | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |

##### Closure Evidence

- Tool work is not complete. GitHub tracking consolidation completed under D33 at 2026-10-17T01:14:10.675787+00:00: replacement #53 is open and all its source issues are closed not_planned with exact body/comment readback. Original criteria and unsuccessful evidence remain active; source closure establishes no tool verification.

##### GitHub Projection

- Title: `Track journal test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #53, https://github.com/jeonghanlee/ansible-provision/issues/53
- Projection Scope: Complete consolidated body containing all original source contracts and additional declared tooling work.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:36Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-journal.md`
- Published Body SHA256: 57226e8a00e7b8aca7c4a5143f1ff5a915bc8b13dea7b1e2f5d99d032d46305d
- Historical Source Issues: #32, #33

#### M48 - Track ETL test tooling

- Origin: 38560eb / M48
- Identity History: created as a test-type coordination entry on 2026-10-16 (D32); no existing identity is replaced.
- GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Status: Deferred

##### Summary

Consolidate the remaining ETL test-tool work into one active issue while preserving every original acceptance condition and evidence record.

##### Scope

All remaining component work is tracked directly in this issue. Source issue references identify preserved historical records; retiring those issues does not complete their checks or require their reopening. Every unmet criterion in the transferred contracts remains active here. Shared source checksums and cross-test phase timing are owned by the shared tools issue.

Component canonical identities remain independent under this single GitHub projection:

- M29: historical source #34; unfinished work is tracked in #54.
- M30: historical source #35; unfinished work is tracked in #54.
- M31: historical source #36; unfinished work is tracked in #54.
- M32: historical source #37; unfinished work is tracked in #54.
- M33: historical source #38; unfinished work is tracked in #54.
- M34: historical source #39; unfinished work is tracked in #54.
- M35: historical source #40; unfinished work is tracked in #54.
- M36: historical source #41; unfinished work is tracked in #54.
- M38: historical source #43; unfinished work is tracked in #54.
- M39: historical source #44; unfinished work is tracked in #54.
- M40: historical source #45; unfinished work is tracked in #54.
- M41: historical source #46; unfinished work is tracked in #54.
- M42: historical source #47; unfinished work is tracked in #54.
- M43: historical source #48; unfinished work is tracked in #54.
- M44: historical source #49; unfinished work is tracked in #54.
- M45: historical source #50; unfinished work is tracked in #54.

Source GitHub issues were retired for consolidation at 2026-10-17T01:14:10.675787+00:00. Component work is not Complete; current tracking is #54 and the retired source metadata is recorded in component details.

##### Detailed Work Summary

These summaries preserve the recorded scope. Each linked issue retains its full acceptance criteria and original evidence; a summary or group checkbox does not replace that verification.

###### #34 - Fix kernel journal collection and ETL terminal isolation

- Problem and evidence: Kernel refusal propagated into terminal findings despite accepted ETL processing. This existing issue coordinates collection, source-availability and lifecycle work.
- Remaining work: Complete its independent collection children and original criteria; retain shared #42/#51 links and original source identities.
- Done when: Every original criterion has real evidence; kernel diagnostics, required ETL evidence and accepted processing results remain separate.

###### #35 - Fix ETL JFR scope and terminal evaluation order

- Problem and evidence: JFR process scope, terminal ordering and UTC matching caused tool findings; measurement/reporting and recipient work are unfinished.
- Remaining work: Complete its independent evaluator/reporting children and original criteria, retaining shared #42/#51 links.
- Done when: Real evaluator/reporting paths satisfy the original criteria; original/candidate identities and independent kernel findings remain explicit.

###### #36 - Preserve kernel cursor refusal evidence and prove interval coverage

- Problem and evidence: Frozen cursor refusals affected 240 shortened and 237 default samples without saved failed-query bytes. Candidate checkpoint-output changes exist but coverage is unverified.
- Remaining work: Identify original/candidate tools and exercise real refused-query, obsolete-anchor and interval-gap cases.
- Done when: Outputs, status, arguments and cursor/interval identity persist; required coverage is independently proved where possible and historical unknowns are not declared successful.

###### #37 - Keep kernel diagnostics independent of the ETL terminal verdict

- Problem and evidence: Kernel-only failure produced pass-wait/final-sample/final-journal findings despite complete required ETL passes.
- Remaining work: Verify actual collection, pass waiting, normal terminal handling and replay using independent configured ETL sources.
- Done when: Kernel failure stays visible without rejecting complete ETL evidence; real required-evidence loss still prevents acceptance and preserves the abort policy.

###### #38 - Use timestamps accepted by systemd 239 journal queries

- Problem and evidence: Systemd 239 refused the original ISO query argument. V2 formatting exists but exact subsecond interval selection is unverified.
- Remaining work: Run the real query at independently identified UTC boundaries, retaining original precision and explicit rounding/filtering.
- Done when: The intended interval is established; refused arguments/output/status persist and query errors remain separate from ETL processing.

###### #39 - Match JFR exports to the recording process and lifetime

- Problem and evidence: CSV counts included prior JVMs while final JFRs belonged to one process. Matching-PID counts reconcile on both chains.
- Remaining work: Bind real evaluator/aggregator comparisons to component, PID and recording lifetime while preserving earlier-process rows.
- Done when: Both chains reconcile in scope and real missing, duplicated, conflicting or truncated evidence remains detectable; originals are unchanged.

###### #40 - Persist terminal state before evaluating terminal coherence

- Problem and evidence: Evaluation preceded terminal persistence; unchanged reevaluation afterward removed the coherence finding on both observations.
- Remaining work: Verify actual normal-terminal, failure/interruption, repeated-request and replay paths.
- Done when: Runtime/replay evaluate the same persisted terminal, errors stay visible, no second stop occurs and unverified success cannot bypass coherence checks.

###### #41 - Match ETL pass times by UTC instant with nanosecond precision

- Problem and evidence: Literal equivalent-UTC comparison found zero passes; the native nanosecond parser found one successful 903-job pass.
- Remaining work: Select by UTC instant in real runtime/scenario and replay paths while retaining original timestamp text.
- Done when: Exactly the correct transition/invocation/time matches; nanosecond differences, wrong identity, duplicates and missing passes are detected without rewriting verdicts.

###### #43 - Finish ETL tool independence checks across both store chains

- Problem and evidence: Two shortened failing/changed-module planned-abort cases have recipient evidence. None of the six required normal-finish cases is established.
- Remaining work: Prepare separately identified absent-study/normal-finish support and verify two chains times three study states through normal finish/restoration and recipient replay.
- Done when: All six rows satisfy original assertions; scenario/recipient exit 0 with expectation Passed, native verdict/exit contracts hold and planned-abort originals are not relabeled.

###### #44 - Finish partial-source ETL evidence verification on both chains

- Problem and evidence: The shortened partial-source case retained two fault samples, one successful pass and no automatic abort. Default behavior and completed scenario replay are unverified.
- Remaining work: Complete actual both-chain fault/recovery, corrected controller verification and exact independent-recipient replay.
- Done when: Original assertions hold; corrected controller/scenario/recipient commands succeed, short native Incomplete/exit-1 and stop rc 0 remain explicit and historical errors are preserved.

###### #45 - Finish all-source evidence loss and automatic-abort verification

- Problem and evidence: Shortened all-source failure advanced counters one to two and triggered one automatic abort with orderly stop/restoration. Default and completed recipient replay are unverified.
- Remaining work: Complete actual both-chain counter/abort/restoration evidence, corrected controller verification and recipient replay.
- Done when: No premature first-failure abort occurs; repeated failure aborts once, all original command/verdict contracts hold and short native Incomplete originals remain unchanged.

###### #46 - Verify ETL collector capture and refusal after normal shutdown

- Problem and evidence: Successful appliance stops do not establish the separate final/post-stop application-file capture and repeat-terminal contract.
- Remaining work: Run the real collector/source reader and terminal CLI around a bounded normal stop and repeat request.
- Done when: Required bytes and invocation/PID/inode/prefix identity persist; incomplete/wrong evidence is refused, replay agrees and no second stop or original overwrite occurs.

###### #47 - Verify real collection during source-store deletion

- Problem and evidence: The parser consumed a retained real deletion-race result, but live collection during source-file removal is unexecuted.
- Remaining work: Run native collection during real source-store deletion and independently record overlap and command results.
- Done when: Measured surviving sizes/status persist, unrelated errors remain visible and actual collected/replayed results agree without reconstructed output.

###### #48 - Reconcile retained ETL measurements and process identities

- Problem and evidence: Measurements exist but per-component reconciliation is unfinished. Three shortened request/pass overlaps had zero metric failures and zero missing coverage.
- Remaining work: Reconcile actual process/lifetime-scoped resource/event/retrieval/identity/gap/OOM evidence and declared accumulation/restart/overlap regressions.
- Done when: Units, intervals, denominators and coverage are explicit; actual counts are used, unknowns are disclosed and normal overlap is not called failed comparison.

###### #49 - Compare ETL busy time and workload with retained earlier results

- Problem and evidence: The retained earlier busy-time/weekly-usage comparison is unfinished.
- Remaining work: Use pinned metric meanings and comparable actual intervals, stating workload, rate, concurrency, store-age and resource differences.
- Done when: Supported comparisons reproduce; unavailable historical rates stay explicit and unsupported improvement/regression claims or predictions are excluded.

###### #50 - Reproduce completed ETL observation reports on an independent recipient

- Problem and evidence: Exact independent-recipient reproduction of complete finalized ETL JSON/numerical reports is unfinished on both chains.
- Remaining work: Freeze actual post-finalization original evaluator/aggregator outputs and identities, privately transfer them and run identical frozen CLIs at declared paths.
- Done when: Complete bytes/hashes, findings, numbers and exit codes match without normalization; embedded initial evaluations remain historical and corrected candidates use separate baselines.

##### Existing Evidence

Both completed full-day processing observations are accepted in #30: all 312 and 27 required passes were present, physical/HTTP comparisons succeeded and normal stops completed. Original aggregate `Incomplete` records remain unchanged. Confirmed tool defects and incomplete tool matrices are separate work. Completed shortened fault behavior does not prove unexecuted default-chain or normal-finish cases.

##### Out Of Scope

Reopening #30/#31, changing application scheduling/storage, predicting event counts or capacity, calling normal metrics overlap a defect, or a new full-day producer solely for tool repair/reporting.

##### Completion Criteria

- [ ] Every transferred collection, evaluation, lifecycle, scenario and reporting criterion below is verified. Preserve original chain matrices, process identities, scenario/native verdicts and exit-code contracts.
- [ ] Preserve the accepted ETL/journal results and every immutable original input and unsuccessful finding. Missing historical failed-query output remains unknown.
- [ ] Close this issue only when actual evidence satisfies its criteria; the closure of source issues and identical failed replays establish no verification.

##### Transferred Acceptance Criteria

All criteria below remain active in the replacement issue. Source closure is administrative; actual verification is still required. The source scopes, evidence and real-path methods remain in their component canonical details and are copied completely into the prepared public body.

###### Source #34 - Fix kernel journal collection and ETL terminal isolation

- [ ] The real failed-query path preserves its original output and enough cursor/interval metadata to diagnose the refusal without exposing credentials or internal identifiers.
- [ ] Focused real-journald checks distinguish an obsolete anchor with independently proven interval coverage from an actual or unresolved required-interval gap; unproved coverage never becomes `Passed`.
- [ ] The actual normal-finish and replay paths keep a kernel-only diagnostic failure visible without rejecting a complete required ETL pass set.
- [ ] Genuine loss of required ETL evidence remains `Incomplete` or `Failed` as applicable, and the declared all-sources-unavailable automatic-abort expectations remain enforced.
- [ ] Both completed observations are rechecked from retained evidence with their exact original tools and a separately identified candidate; original data, failed records and verdicts remain unchanged.
- [ ] The follow-up uses retained evidence and bounded real-path checks; no new 24-hour observation is required solely to repair the collector.

- [ ] Complete collector/package independence through actual preparation, start, capture, normal terminal handling and replay on both chains with unrelated journal-study modules absent, failing and separately changed. Preserve completed shortened results; execute the unverified default variants as tool checks.
- [ ] Complete the remaining collection-source failure and automatic-abort cases using actual configured sources. Distinguish successful ETL processing from unavailable test evidence, and retain first-failure versus repeated-failure behavior.
- [ ] Verify final and post-stop application-file capture, process identity, repeated terminal refusal and restoration through the actual tools without changing completed ETL observation records.
- [ ] Exercise real collection during source-store deletion and metrics requests overlapping ETL pass completion; preserve actual request bounds and measured outputs instead of converting collection races into ETL failures.
- [ ] Preserve actual fixture/input counts, source timing and workload identity for later measurement reports; configured frequency multiplied by duration is not an observed event count.
- [ ] Keep these tool checks independent of the completed ETL functionality result in #30. Future collector corrections follow the accepted ETL verification and do not require another full-day observation solely for tool repair.



###### Source #35 - Fix ETL JFR scope and terminal evaluation order

- [ ] The real evaluator and numerical aggregator correctly reconcile retained current-process heap/collection/pause records with complete JFRs on both chains while retaining earlier-process data.
- [ ] Missing, conflicting or incomplete records in an actual retained-input copy remain detectable; no internal-function stub or reconstructed positive fixture establishes acceptance.
- [ ] A real normal-terminal invocation and subsequent offline replay agree on terminal coherence, including actual failure, interruption and repeat-terminal handling.
- [ ] Verification runs the shipped tools and actual retained evidence, with original and candidate tool identities kept separate. Original inputs, terminal bytes and failed verdicts remain unchanged.
- [ ] Results state which independent kernel diagnostic findings remain; evaluator correction does not claim historical kernel coverage or change the already accepted ETL functionality result in #30.
- [ ] Use the completed observations for regression and focused real terminal checks for ordering; a new 24-hour observation is not required solely to repair these verifier defects.

- [ ] Compare original UTC instants with the shipped timestamp parser, retaining nanosecond precision and original strings. Verify actual retained source-availability and automatic-abort inputs through the real runtime/scenario and replay paths; do not change an original controller status to satisfy the checker.
- [ ] Reconcile per-component heap, GC cause/pause, jstat, RSS, observed input/event rates, retrieval freshness/visibility, request bounds and identity/gap/OOM evidence from the already collected observations.
- [ ] Evaluate retained and focused real-input measurement regressions for source-store shrink, pass-end/request overlap, accumulation and restart. Collection-path corrections are coordinated with #34; no internal mock establishes integration acceptance.
- [ ] Produce the supplemental workload/performance comparison: last-pass and average busy time, weekly usage and actual load, concurrency, store-age and resource differences. Missing comparable historical rates prohibit an improvement claim but do not reopen ETL functionality acceptance.
- [ ] Privately transfer the retained evidence and exact frozen tools to an independent recipient, verify declared members/hashes and reproduce complete result JSON and numerical reports. Keep original unsuccessful findings, raw operational data and deployment identifiers out of public Git.
- [ ] Record actual preparation, processing, waiting, observation and analysis times against the agreed one-hour journal, three-hour ETL, parallel full-day and two-hour overall decision allocations as supplemental reporting; do not impose a new observation to complete the report.
- [ ] Complete these evaluator/report/reproduction checks after the accepted ETL functionality result. Their completion is not a gate on #30 and no new 24-hour data-production run is required solely for these corrections or analyses.



###### Source #36 - Preserve kernel cursor refusal evidence and prove interval coverage

- [ ] Historical frozen tools and the current candidate are identified separately by complete manifests/source hashes; the existing checkpoint-output change is distinguished from unverified behavior.
- [ ] A real refused candidate query preserves stdout/stderr, return code, original arguments and cursor/interval metadata.
- [ ] An actual obsolete-anchor case with independently proved required coverage is distinguished from a real or unresolved required-interval gap.
- [ ] Unproved coverage remains `Incomplete` or `Failed`; original full-day records and unsuccessful verdicts stay unchanged.



###### Source #37 - Keep kernel diagnostics independent of the ETL terminal verdict

- [ ] A real kernel-only diagnostic failure does not invalidate complete required application ETL evidence at pass waiting or normal finish.
- [ ] Missing required ETL evidence still refuses complete acceptance and preserves the applicable abort policy.
- [ ] The actual terminal CLI and retained-input replay agree while keeping original diagnostic and unsuccessful aggregate findings.



###### Source #38 - Use timestamps accepted by systemd 239 journal queries

- [ ] Original and v2 controller hashes are recorded separately, and existing source formatting is distinguished from actual interval verification.
- [ ] The actual systemd 239 query accepts the candidate argument and establishes the intended interval against independently identified real records, including subsecond boundaries; any query rounding/filtering and the original precise timestamp are explicit.
- [ ] A rejected query retains its arguments, stdout/stderr and return code and is not reported as successful coverage.
- [ ] Successful ETL evidence remains separate from a query-argument error; the original failed controller record is unchanged.



###### Source #39 - Match JFR exports to the recording process and lifetime

- [ ] The real evaluator and aggregator reconcile heap, collection and pause records with both chains' complete recordings using actual process/lifetime identities.
- [ ] Earlier-process records remain available; missing, conflicting, duplicated or truncated in-scope evidence still fails the real path.
- [ ] Original recordings, exports, unsuccessful verdicts and independent kernel findings remain unchanged.



###### Source #40 - Persist terminal state before evaluating terminal coherence

- [ ] A real normal terminal invocation and subsequent replay agree on the exact terminal state being evaluated.
- [ ] Actual failure/interruption and repeated-terminal cases retain failure visibility and do not dispatch another stop.
- [ ] No unverified successful terminal is written to bypass coherence checks; original completed observation bytes remain unchanged.



###### Source #41 - Match ETL pass times by UTC instant with nanosecond precision

- [ ] Actual source-availability and automatic-abort records select exactly the matching transition, invocation and UTC instant.
- [ ] Nanosecond differences, wrong invocation, duplicate matches and genuinely missing passes remain detectable.
- [ ] Runtime/scenario and frozen replay paths agree without rewriting an original controller verdict or timestamp.



###### Source #43 - Finish ETL tool independence checks across both store chains

- [ ] All six chain/study-state normal-finish rows have actual preparation/start/capture/normal-terminal/restoration and exact recipient replay evidence; recorded planned-abort results remain separately identified.
- [ ] The unrelated subject is actually absent, fails import or remains importable after its declared change as applicable; the complete native ETL dependency bundle and actual runtime identities remain unchanged throughout each case.
- [ ] Candidate support for absent-study and normal-finish paths is identified separately; no preserved planned-abort payload or result is relabeled normal finish.
- [ ] Scenario verification and recipient replay each exit 0 with `expectation=Passed` and satisfy the declared assertions; matching failed runs alone never complete a row.
- [ ] Native terminal/evaluator/aggregator exit codes and saved verdicts follow the explicit short-abort or normal-finish contract, while original bytes and unsuccessful findings remain unchanged.



###### Source #44 - Finish partial-source ETL evidence verification on both chains

- [ ] Actual journal failure with all required configured application files available preserves ETL pass evidence and does not trigger an evidence-loss abort.
- [ ] Both chains have declared fault/recovery boundaries, real sampler identity, exact restoration and actual bounded stop evidence.
- [ ] Corrected candidate runtime/controller execution exits 0 with complete runtime evidence; historical controller errors and their original exit codes remain unchanged.
- [ ] The scenario verifier and independent recipient replay each exit 0 with `expectation=Passed`, satisfy all declared source-availability assertions and reproduce exact complete results/identities; equality of two failed checks is insufficient.
- [ ] The deliberately shortened native abort/evaluator/aggregator retains its exact `Incomplete` verdict and expected exit code 1, with actual appliance stop rc 0; no full-day acceptance is claimed.



###### Source #45 - Finish all-source evidence loss and automatic-abort verification

- [ ] The first actual critical sample does not prematurely abort; the declared consecutive failure triggers exactly one native abort.
- [ ] Both chains retain real source-access failure, sampler/process identity, counter sequence, actual appliance stop rc 0 and exact restoration evidence.
- [ ] Corrected candidate runtime/controller execution exits 0 with complete runtime evidence; historical controller errors and their original exit codes remain unchanged.
- [ ] The scenario verifier and independent recipient replay each exit 0 with `expectation=Passed`, satisfy all declared counter/abort/restoration assertions and reproduce exact complete results/identities; equality of two failed checks is insufficient.
- [ ] The deliberately shortened native abort/evaluator/aggregator retains its exact `Incomplete` verdict and expected exit code 1; source unavailability and successful automatic abort are not relabeled an ETL data-loss failure or full-day acceptance.



###### Source #46 - Verify ETL collector capture and refusal after normal shutdown

- [ ] Actual final/post-stop capture retains all required application-file bytes with the original invocation, PID, inode and prefix identity.
- [ ] A changed invocation, wrong PID, truncation or missing final record refuses complete evidence.
- [ ] Repeated terminal invocation dispatches no second stop and leaves original evidence unchanged; real replay reproduces the result.



###### Source #47 - Verify real collection during source-store deletion

- [ ] A real source-file removal overlaps the native collector measurement and the overlap is independently recorded.
- [ ] Measured surviving sizes and actual command status are preserved; a tolerated disappearing file does not hide unrelated command failures.
- [ ] The actual collected result and frozen retained-input evaluation agree without reconstructed stdout or internal substitutes.



###### Source #48 - Reconcile retained ETL measurements and process identities

- [ ] Per-component heap, GC cause and pause, jstat, RSS and observed input/event counts and rates reconcile with actual process/lifetime identities and time ranges; units, provenance and rate denominators are explicit.
- [ ] Retrieval freshness and visibility are reported with actual query/request/response bounds. Process identity continuity, evidence gaps and OOM or forced-termination findings are reported explicitly; absent evidence is not recorded as zero events or complete coverage.
- [ ] Actual request/pass overlaps, accumulation and process changes are evaluated from retained records and remain distinct from failed assertions.
- [ ] Configured rates and array capacity are never used as observed event counts or actual lengths; missing data is stated rather than invented.
- [ ] Retained-input and bounded real measurement regressions cover accumulation, process restart and pass-end/request overlap; actual coverage and unresolved cases remain explicit.



###### Source #49 - Compare ETL busy time and workload with retained earlier results

- [ ] The report uses the actual pinned metric meanings and comparable observed intervals; the retired running-sum interpretation is excluded.
- [ ] Workload and fixture differences are explicit, including absent comparable historical rates.
- [ ] No improvement/regression claim is made when the retained inputs cannot support it; no missing measurement is replaced by a prediction.



###### Source #50 - Reproduce completed ETL observation reports on an independent recipient

- [ ] Before transfer, freeze actual post-finalization evaluator and aggregator outputs for each chain, with the exact input/terminal identities, full tool/dependency hashes and versions, CLI arguments, exit codes and complete-output SHA256 values.
- [ ] Every declared archive member, saved baseline and frozen dependency matches before actual recipient execution.
- [ ] The recipient executes the same original frozen offline CLIs at the original declared paths and reproduces the complete baseline JSON bytes/hashes, per-check findings, numerical outputs and exit codes without normalization or rewritten inputs/identities.
- [ ] The initial embedded evaluation and original unsuccessful findings remain unchanged. Any corrected candidate has its own tool identity and post-finalization baseline; it is never compared with the original-tool baseline as if the tools were identical.



##### Dependencies And Decisions

- D33; Decision Date: 2026-10-16. Consolidate GitHub tracking into four issues; copy every original contract and retire twenty source issues with reason not planned. This supersedes D32's plan to keep those twenty GitHub issues open. Independent canonical component work and future tool execution remain Deferred.
- Primary links are coordination relationships, not a new sequential execution dependency. Each existing issue retains its original criteria, source identities and evidence; no original result is rewritten.
- Accepted M22/#30 ETL and M25/#31 journal results remain complete. The completed buffer acceptance in jeonghanlee/epicsarchiverap-maven#29 remains separate.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: earlier representative-only issue projection under D32.

1. Preserve each component's original scope, criteria, evidence and source identity in this issue; use source issue links as historical provenance.
2. After separate tool-execution authorization, perform the scoped real-path corrections and checks, retaining explicit scenario/native verdicts and immutable originals.
3. Update the per-component criteria from actual results. Shared evidence may satisfy overlapping criteria without inventing duplicate campaigns.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Detailed coverage | Execute each linked issue's actual collector/controller/terminal/evaluator/reader/replay path with its declared inputs. | Retained evidence and separately authorized bounded deployments | Every original criterion has actual evidence; unexecuted cells remain explicit. |
| T2 | Scope isolation | Compare immutable originals and accepted #30/#31 records with separately identified candidate results. | Retained original and candidate records | Original bytes preserved; tool findings separate from accepted functionality. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Retained evidence and separately authorized bounded deployments | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |
| T2 | Not run | Retained original and candidate records | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |

##### Closure Evidence

- Tool work is not complete. GitHub tracking consolidation completed under D33 at 2026-10-17T01:14:10.675787+00:00: replacement #54 is open and all its source issues are closed not_planned with exact body/comment readback. Original criteria and unsuccessful evidence remain active; source closure establishes no tool verification.

##### GitHub Projection

- Title: `Track ETL test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
- Projection Scope: Complete consolidated body containing all original source contracts and additional declared tooling work.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:40Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-etl.md`
- Published Body SHA256: b6a0ab483695713866a62fe7ccf6cb65a4f04514238fa3adce424715686417f0
- Historical Source Issues: #34, #35, #36, #37, #38, #39, #40, #41, #43, #44, #45, #46, #47, #48, #49, #50

#### M49 - Track buffer test tooling

- Origin: 38560eb / M49
- Identity History: created as a test-type coordination entry on 2026-10-16 (D32); no existing identity is replaced.
- GitHub Issue: #55, https://github.com/jeonghanlee/ansible-provision/issues/55
- Status: Deferred

##### Summary

Make the retained sample-buffer delay-injection, replay and progress tools reusable without changing completed product acceptance in jeonghanlee/epicsarchiverap-maven#29.

##### Scope

All remaining component work is tracked directly in this issue. Source issue references identify preserved historical records; retiring those issues does not complete their checks or require their reopening. Every unmet criterion in the transferred contracts remains active here. Installation/source-preservation work belongs to the shared tools issue; Maven code/test implementation remains Maven-owned.

Component canonical identities remain independent under this single GitHub projection:

- Replay, progress and Maven assertion-coverage work retains its declared scope; shared installer/source preservation belongs to M50.

Source GitHub issues were retired for consolidation at 2026-10-17T01:14:10.675787+00:00. Component work is not Complete; current tracking is #55 and the retired source metadata is recorded in component details.

##### Detailed Work Summary

These summaries preserve the recorded scope. Each linked issue retains its full acceptance criteria and original evidence; a summary or group checkbox does not replace that verification.

###### Compact pass replay

- Problem and evidence: Full JSONL passes validate; compact last-position passes were falsely refused after write-list compaction.
- Remaining work: Define supported full/compact contracts and exercise the real replay with retained valid and inadequate-exposure inputs.
- Done when: Declared valid input works, inadequate exposure stays detectable and omitted writes are never invented; accepted live results stay unchanged.

###### Observation progress

- Problem and evidence: Actual bounds are saved while progress can remain Starting until the first hourly update.
- Remaining work: Publish active state with start/cutoff and verify the actual runner path in a bounded case.
- Done when: Active state is immediate and hourly checkpoints, monotonic bounds and final verdict remain intact.

###### Maven assertion coverage

- Problem and evidence: Pinned sources lack direct absent-property and specified one-second zero-loss assertions; deployment receipts establish separate coverage.
- Remaining work: Describe actual assertion coverage and record the two gaps as Maven-owned follow-up work.
- Done when: Coverage and ownership are explicit; receipts are not called execution of absent assertions and no Maven edit or product reacceptance is implied.

##### Existing Evidence

The shipped `validate_pass()` accepts all 25 eligible preflight and 1152 main full JSONL records but rejects 12 preflight and 576 main compact last-position records. It uses `len(writes) - 1`, while compact records keep only first/last writes plus `write_count`. Live validation ran before compaction; this replay defect does not overturn the accepted four-hour result.

The runner records actual start/cutoff before its first hourly status update, leaving an active observation marked `Starting`. Maven sources at jeonghanlee/epicsarchiverap-maven@629533a37ef889ffe3203d97538038eaaec95283 lack a direct absent-property assertion in `SampleBufferMarginPropertyTest` and a one-second zero-loss assertion in the 1500 ms control of `SampleBufferMarginTest`. Deployment receipts independently establish effective margin 1.0 and zero non-fast control loss; narrower assertions do not establish a product defect.

##### Out Of Scope

Reopening jeonghanlee/epicsarchiverap-maven#29, editing Maven code here, a new full campaign solely for replay/reporting repair, publishing raw traces/PB/private configuration, or claiming broader exact equality than originally measured.

##### Completion Criteria

- [ ] Define explicit full and compact replay input contracts. Run the real validator/replay against retained actual records; valid declared inputs are accepted and missing, duplicate or inadequate delay exposure remains detectable. Never invent omitted writes.
- [ ] Publish active observation state and actual start/cutoff immediately when recording begins, preserving hourly checkpoints, final state and monotonic bounds.
- [ ] Describe actual Maven assertion coverage and record the two assertion gaps as Maven-owned follow-up work. Keep deployment receipts distinct from unit-test execution; Maven code/tests remain owned by that repository.
- [ ] Preserve original full JSONL, compact records, source identities, initial unsuccessful preflight and accepted product results. Keep expected control loss separate from the zero-loss positive window.
- [ ] Document reusable signals, timing, target selection, actual exposure, trace/PB boundaries and verdict interpretation. Exact fast-PV equality and slower-PV activity/counter coverage stay distinct.

##### Dependencies And Decisions

- D33; Decision Date: 2026-10-16. Consolidate GitHub tracking into four issues; copy every original contract and retire twenty source issues with reason not planned. This supersedes D32's plan to keep those twenty GitHub issues open. Independent canonical component work and future tool execution remain Deferred.
- Primary links are coordination relationships, not a new sequential execution dependency. Each existing issue retains its original criteria, source identities and evidence; no original result is rewritten.
- Accepted M22/#30 ETL and M25/#31 journal results remain complete. The completed buffer acceptance in jeonghanlee/epicsarchiverap-maven#29 remains separate.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: earlier representative-only issue projection under D32.

1. Preserve each component's original scope, criteria, evidence and source identity in this issue; use source issue links as historical provenance.
2. After separate tool-execution authorization, perform the scoped real-path corrections and checks, retaining explicit scenario/native verdicts and immutable originals.
3. Update the per-component criteria from actual results. Shared evidence may satisfy overlapping criteria without inventing duplicate campaigns.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Replay | Execute the shipped validator/replay on retained full/compact preflight/main records and actual missing-delay records. | Retained actual buffer evidence | Explicit schemas prevent false last-position refusals; inadequate exposure detected. |
| T2 | Progress | Execute the real runner start/progress path and inspect persisted state, bounds, checkpoints and terminal record. | Separately authorized bounded deployment | Active state visible before the first hourly checkpoint; final record intact. |
| T3 | Coverage accounting | Read pinned Maven assertions and independent deployment receipts and record their separate coverage. | Pinned Maven sources and preserved receipts | No absent assertion is reported as executed. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Retained actual buffer evidence | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |
| T2 | Not run | Separately authorized bounded deployment | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |
| T3 | Not run | Pinned Maven sources and preserved receipts | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |

##### Closure Evidence

- Tool work is not complete. GitHub tracking consolidation completed under D33 at 2026-10-17T01:14:10.675787+00:00: replacement #55 is open and all its source issues are closed not_planned with exact body/comment readback. Original criteria and unsuccessful evidence remain active; source closure establishes no tool verification.

##### GitHub Projection

- Title: `Track buffer test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #55, https://github.com/jeonghanlee/ansible-provision/issues/55
- Projection Scope: Complete consolidated body containing all original source contracts and additional declared tooling work.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:42Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-buffer.md`
- Published Body SHA256: 68475d0897f4a062b6984649f43b95503f985c3d16e73e33a1317461468bbe63
- Historical Source Issues: none; buffer tooling scope is declared directly here.

#### M50 - Track shared test tooling

- Origin: 38560eb / M50
- Identity History: created as a test-type coordination entry on 2026-10-16 (D32); no existing identity is replaced.
- GitHub Issue: #56, https://github.com/jeonghanlee/ansible-provision/issues/56
- Status: In progress

##### Summary

Consolidate the remaining shared test-tool work into one active issue while preserving every original acceptance condition and evidence record.

##### Scope

All remaining component work is tracked directly in this issue. Source issue references identify preserved historical records; retiring those issues does not complete their checks or require their reopening. Every unmet criterion in the transferred contracts remains active here. Current reusable-source manifests stay separate from immutable observation manifests.

Component canonical identities remain independent under this single GitHub projection:

- M37: historical source #42; unfinished work is tracked in #56.
- M46: historical source #51; unfinished work is tracked in #56.

Source GitHub issues were retired for consolidation at 2026-10-17T01:14:10.675787+00:00. Component work is not Complete; current tracking is #56 and the retired source metadata is recorded in component details.

##### Detailed Work Summary

These summaries preserve the recorded scope. Each linked issue retains its full acceptance criteria and original evidence; a summary or group checkbox does not replace that verification.

###### #42 - Refresh preserved-tool checksums

- Problem and evidence: The recorded reusable-source manifest check found three missing files and sixteen hash mismatches.
- Remaining work: Historical local source correction and real CLI/copy checks passed under M37. D35 replaces duplicate local scripts with the committed common checker; all 19 bounded project integration cases and preservation checks passed as M37/T4. Commit/landing remain outstanding. The scoped GitHub update remains outstanding.
- Done when: Missing, omitted, duplicate, removed and changed files are detected; immutable observation manifests and private runtime data are untouched.

###### #51 - Report actual test phase durations against the agreed allocations

- Problem and evidence: Actual phase durations have not been consolidated against agreed one-hour journal, three-hour ETL, parallel full-day and two-hour decision allocations.
- Remaining work: Reconcile retained UTC/monotonic boundaries, separating preparation, processing, waiting, observation and analysis.
- Done when: Measured elapsed/simultaneous work, default scheduling waits and missing boundaries are explicit; original allocations are unchanged.

###### Reusable source and procedure preservation

- Problem and evidence: Reviewed buffer sources/procedures are preserved privately but not yet imported into Git-managed locations.
- Remaining work: Preserve reusable sources/procedures with original/candidate identity and explicit dependencies, excluding deployment-specific inputs.
- Done when: Reusable files are trackable; raw captures, PB data, operational logs, credentials and private configuration stay excluded.

###### Installer dependencies

- Problem and evidence: The buffer installer defines ETL commands whose collector/observer dependencies are absent from its bundle; the campaign did not use them.
- Remaining work: Declare inputs, pins, service effects and prerequisites; verify the real packaged installer separately.
- Done when: Every installed command has its actual declared dependencies and effects, originals remain intact and no unobserved runtime failure is claimed.

##### Existing Evidence

The baseline source manifest check reported three missing source files and sixteen mismatched hashes. M37 retains the original local correction evidence: 98-file parent coverage, passing 5/17-file child checks and twelve local real-copy regression tests before D35. Current shared-checker integration passed 19 declared cases with 96 parent and 5/17 child members; original sources and historical results remain intact. Source landing remains outstanding. Current-source manifests and immutable observation-specific manifests have different ownership. The retained buffer fixture installer writes ETL units referring to `collect.py` and `observe.py`, neither included in its 18-file bundle. That campaign uses its own runner, so no missing-dependency runtime failure is claimed. Setup embeds one-deployment paths/pins and is not a repeatable Ansible role.

##### Out Of Scope

Test-specific repairs owned by other groups, altering original evidence/frozen manifests, public raw-data imports, inherited capacity caps, or repeated long observations solely for preservation/reporting.

##### Completion Criteria

- [x] Complete the transferred checksum criteria from #42 through the actual checksum CLI and current-source coverage check, detecting missing, omitted, duplicate, removed or changed files without regenerating original observation manifests.
- [ ] Preserve reusable buffer sources/procedures in Git-managed locations with explicit original/candidate identity and dependencies. Exclude raw captures, PB data, operational logs, credentials and deployment-specific configuration.
- [ ] Make installation inputs, pins, service effects and prerequisites explicit. Install only commands whose declared dependencies are supplied; validate the real installer in a separate bounded environment and preserve originals.
- [ ] Complete the transferred phase-report criteria from #51 from actual start/end records against approximately one-hour journal basics, three-hour ETL processing, parallel full-day observations and two-hour result decision allocations. Separate preparation, processing, waiting, observation and analysis; never predict missing times.
- [ ] Document shared source/evidence selection, privacy, transfer/member verification, original/candidate replay and verdict handling while retaining each test's own signals, timing and acceptance criteria.

##### Transferred Acceptance Criteria

All criteria below remain active in the replacement issue. Source closure is administrative; actual verification is still required. The source scopes, evidence and real-path methods remain in their component canonical details and are copied completely into the prepared public body.

###### Source #42 - Refresh preserved-tool checksums

- [x] The real checksum CLI verifies every current entry and declared required source.
- [x] Missing, omitted, duplicate, removed or deliberately changed actual source files are detected.
- [x] Private runtime data and original observation manifests are never regenerated or included.



###### Source #51 - Report actual test phase durations against the agreed allocations

- [ ] Each reported duration identifies actual start/end evidence and separates simultaneous work from elapsed wall time.
- [ ] Waiting for default-chain scheduling is recorded explicitly; it is not presented as successful processing time.
- [ ] Schedule conflicts and missing boundaries are disclosed without changing the agreed allocation, shortening an observation or inventing times.



##### Dependencies And Decisions

- D35; Decision Date: 2026-10-18. M37 uses the committed common checker instead of duplicate local scripts. Only this source-check component is active; other shared work remains unauthorized.
- D34; Decision Date: 2026-10-16. M37 checksum work is active within this group. All other shared component plans remain draft and unauthorized; group completion is not implied.
- D33; Decision Date: 2026-10-16. Consolidate GitHub tracking into four issues; copy every original contract and retire twenty source issues with reason not planned. This supersedes D32's plan to keep those twenty GitHub issues open. Independent canonical component work and future tool execution remain Deferred.
- Primary links are coordination relationships, not a new sequential execution dependency. Each existing issue retains its original criteria, source identities and evidence; no original result is rewritten.
- Accepted M22/#30 ETL and M25/#31 journal results remain complete. The completed buffer acceptance in jeonghanlee/epicsarchiverap-maven#29 remains separate.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: earlier representative-only issue projection under D32.

1. Preserve each component's original scope, criteria, evidence and source identity in this issue; use source issue links as historical provenance.
2. After separate tool-execution authorization, perform the scoped real-path corrections and checks, retaining explicit scenario/native verdicts and immutable originals.
3. Update the per-component criteria from actual results. Shared evidence may satisfy overlapping criteria without inventing duplicate campaigns.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Source preservation | Run the actual checksum CLI and coverage checks specified by #42 on current sources and isolated real copies. | Reusable source tree and isolated copies | All required sources covered; frozen observation manifests unchanged. |
| T2 | Installation | Run the actual packaged installer/preflight using declared inputs and inspect generated units and dependencies. | Separately authorized bounded deployment | Commands have real dependencies and declared service effects; private inputs excluded. |
| T3 | Phase reporting | Reconcile retained controller/observation/terminal timestamps and phase receipts as specified by #51. | Retained completed-test records | Measured intervals distinguish overlap/waiting and disclose missing boundaries. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-10-17T06:51:10.441861+00:00 | Actual current source checkout and isolated real copies | Passed locally | M37 T1-T3: 98 parent members, 5/17 child members, twelve real CLI regression tests and unchanged frozen/source identities. Scope is checksum work only; commit/landing and the published checkbox update remain outstanding. |
| T1 | 2026-10-18T18:02:02.562508+00:00 | Committed common checker; actual checkout and retained project copies | Passed locally | M37/T4: 19 project integration cases and the documented commands pass; current coverage is 96 parent and 5/17 child members. Duplicate local scripts are privately preserved and removed; all 95 non-target sources and frozen manifests are unchanged. Evidence: `work/source-checker-dedup-fu6jzviu/integration.json` and `preservation.json`. This does not complete other shared-tool criteria. |
| T2 | Not run | Separately authorized bounded deployment | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |
| T3 | Not run | Retained completed-test records | Pending | Future scoped verification is not established by grouping or by a historical result outside this check. |

##### Closure Evidence

- Checksum-only checks passed under M37/D34; shared-checker integration and duplicate removal passed under D35/M37/T4. All other shared criteria remain unchecked and unauthorized; overall tool work is not complete.
- Tool work is not complete. GitHub tracking consolidation completed under D33 at 2026-10-17T01:14:10.675787+00:00: replacement #56 is open and all its source issues are closed not_planned with exact body/comment readback. Original criteria and unsuccessful evidence remain active; source closure establishes no tool verification.

##### GitHub Projection

- Title: `Track shared test tooling`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Assignee: `jeonghanlee`
- Issue: #56, https://github.com/jeonghanlee/ansible-provision/issues/56
- Projection Scope: Complete consolidated body containing all original source contracts and additional declared tooling work.
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Observed Assignees: `jeonghanlee`
- Observed Updated At: 2026-10-17T01:09:45Z
- Last Compared: 2026-10-17T01:14:10.675787+00:00; exact body/metadata and source body/comment preservation with not_planned closure verified by live readback.
- Prepared Body: `work/issue-tools-shared.md`
- Published Body SHA256: 991316dabf5a9f3ac639c6550aa1a090cd16b43f0aa719c0e0afa8f477e906c2
- Historical Source Issues: #42, #51

## History

| Reset Date | Prior State Commit |
| --- | --- |
| 2026-08-17 | 38560eb9a1d2d761420d0f313328020e548c45c7 |
