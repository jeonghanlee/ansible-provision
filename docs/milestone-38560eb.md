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

Next session entry point: Preserve all M22 services, fixtures and original failed-run evidence.
Both additional environments now run the latest approved artifacts with 903 connected PVs.
The 2026-10-09 automatic cold executions completed their recorded physical/HTTP
startup and regular-repeat checks but ended Incomplete at an overly strict initial
chunk-key comparison. The owner selected the bounded correction and retained-record
recheck. Both separate recheck proofs Passed; original result and evidence hashes
remain unchanged. Source and retained-evidence review 2 accepted the correction and
both separate recheck proofs after independent archive/hash inspection. Separate recheck results cannot satisfy the original complete
focused-proof gate. The Retained-Record Recheck Proof Consumer Amendment (2026-10-09)
defines the consumer acceptance conditions; it was accepted and its local implementation
and rehearsal authorized on 2026-10-10, while every guest operation needs its own
recorded execution authority. Complete it before continuity, instrumentation, measured
preparation and either 24-hour observation; do not reseed or restart the existing
services to bypass that gate.
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

Status tally: 20 Complete, 1 In progress, 0 Not started, 1 Deferred, 1 Blocked. 4 external gates (3 Complete, 1 Open).

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
| Core | M22 | Verify the ETL pass scheduler on two parallel store chains | Milestone | In progress | No | M17, M21, G4 | Both fixed-ref deployments run for at least 24 hours across UTC midnight with the same 903-PV fixture; pass timing and metrics match the scheduler design, normal-load passes do not overrun, each unit stops within its configured timeout, and the earlier soak comparison is recorded; [detail](#m22---verify-the-etl-pass-scheduler-on-two-parallel-store-chains) |
| Core | M23 | Add the Perl modules for the EPICS-env installed-tree utility to the EPICS OS package set | Milestone | Complete | No | D20 | `epics_os_packages` carries `perl-Digest-SHA`, `perl-JSON-PP`, `perl-Pod-Checker` and `perl-Test-Simple` on rocky8 and rocky10 and `perl` on debian12, debian13, ubuntu24 and ubuntu26; after the `epics` operator applies on each vacuum, the four modules load and `podchecker` runs; delivered in `4dfb290`, verified on all six vacua (`300ccc7`); [detail](#m23---add-the-perl-modules-for-the-epics-env-installed-tree-utility-to-the-epics-os-package-set) |
| Core | M24 | Split the archiver MariaDB operator into socket and TCP operators and rename the archiver-dev species | Milestone | In progress | No | D21 | Operators `mariadb_uds` and `mariadb_tcp` and species `archiver-dev-uds`, `archiver-dev-tcp` and `archiver-dev-sqlite` exist with the group variables `archiver_dev_uds.yml`, `archiver_dev_tcp.yml` and `archiver_dev_sqlite.yml`; each species deploys on a fresh guest with its database reachable exactly as the cloud-provision definition states; the old `archiver-dev` name still resolves for a limited period; [detail](#m24---split-the-archiver-mariadb-operator-into-socket-and-tcp-operators-and-rename-the-archiver-dev-species) |
| Core | M25 | Verify journal collection integrity and retention for the ETL soak | Milestone | In progress | No | D22 | The journal checks formerly T22-T28 of the ETL soak (kernel-journal coverage after cursor loss and in quiet intervals, rotation and event delivery, detection of required-record loss, boundaries and boot identity, the retention budget in preparation and in a 24-hour window, and abort and terminal integration) each pass in their stated environment, including a compressed rehearsal of the full collection path under a reduced journal cap; [detail](#m25---verify-journal-collection-integrity-and-retention-for-the-etl-soak) |
| Gate | G1 | the production IOC server reaches the internal git host | External gate | Complete | No | | Reachability achieved through the site HTTP proxy's CONNECT tunnel (an ssh `ProxyCommand` over the proxy), not a firewall whitelist: the owner's key authenticates and `git ls-remote` returns the refs; confirmed 2026-09-03 by the successful iocserver clone (M4/T2) |
| Gate | G2 | cloud-provision ships the middleware package baseline and the middleware VM | External gate | Open | No | | The middleware operator/species structure and OS package baseline (system OpenJDK 21, Tomcat 9.0.121, MariaDB; no Maven package) originate in cloud-provision (`docs/milestone-e260630.md` M11) as the normative source and a middleware VM is provisionable there, before ansible-provision mirrors the set and layers its roles; owned by the cloud-provision session |
| Gate | G3 | epicsarchiverap-env ships a `sql.fill` that loads the configuration schema when the database and application account are provisioned externally | External gate | Complete | No | | Complete when the jeonghanlee/epicsarchiverap-env#47 fix commit is on `modernize` and epicsarchiverap-env records #47's acceptance as met: with only the application account, `make sql.fill` loads the schema, `make sql.show` lists `PVTypeInfo`, `PVAliases`, `ArchivePVRequests` and `ExternalDataServers`, and an absent database exits non-zero. Observing it on an archiver-dev host is M14/T17, not this gate; owned by the epicsarchiverap-env session; met 2026-09-23: the fix is `1fc20a8` on `modernize`, and #47 closed with epicsarchiverap-env's acceptance recorded |
| Gate | G4 | Prepare two independent ETL soak environments | External gate | Complete | No | | Two fresh archiver-dev VM inventories are available; the owner selected the same existing 903-PV fixture for both chains, and initial disk and host capacity were assessed on 2026-09-28; [detail](#g4---prepare-two-independent-etl-soak-environments) |

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
- GitHub Issue: none; external request `jeonghanlee/epicsarchiverap-maven#12`
- Status: In progress

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
| Bundle freeze and replacement step literal (Ordered Work 4) | Frozen locally; independent review requested | 2026-10-10T10:50Z. `contract.py --freeze` rewrote `bundle.json` with exactly one changed member, `focused.py` `4265dfac…` to `c8952f75baab751281de87b5cfa571c6fa43c519bb4376252c765c16a8ef86b9`; `verify_bundle` passes on the 24 members. Frozen `bundle.json` SHA256 `5168ca0e495ea8720704bada64f3297b8c12d48ae2037acfb4762f9cb237cd15`, filled into `ACCEPTED_BUNDLE_SHA256` of `replace-bundle.py`, whose SHA256 was then `eb66af7961cdef8e68718c04bf9bb50ca6a6a60117aada9332c53ed1dd1593ba`. After the independent review of 2728000 the step refuses a symbolic link or non-regular file in the installed directory or the bundle and prints the single recovery `mv`; its SHA256 is now `7ef22236e7fb66712b2a5e6760ce267f6d00fa1b85983cc6413465dd0009bae3`, and `bundle.json` and `focused.py` are unchanged. A proof-chain and proof-result case was added to the consumer tests; 59 tests OK, 27 skipped. The shipped command line replaced a scratch copy of the previous bundle and rolled it back: installed files equal the frozen files, the extra file survived, and the previous `focused.py` returned. Evidence: 58 tests OK, 27 skipped; 55 `SHA256SUMS` entries match. The scratch run used the host `systemctl`, which reported the three units inactive, and no guest. The T29/T30 local results above ran with the same `focused.py` SHA256. |
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
- GitHub Issue: none; peer request from the cloud-provision session on 2026-10-05
- Status: In progress

##### Summary

cloud-provision decided that the archiver configuration database is three
operators and that every archiver species carries exactly one (`D21`). This
repository has one `mariadb` role whose `mariadb_skip_networking` switch picks
the socket-only or the loopback TCP mode, the species `archiver-dev` and
`archiver-dev-sqlite`, and the group variables `archiver_dev.yml` and
`archiver_dev_sqlite.yml`. The cloud-provision inventory generator already
rejects the name `archiver-dev`.

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

- Not started.

#### M25 - Verify journal collection integrity and retention for the ETL soak

- Origin: 38560eb / M25
- Identity History: transferred on 2026-10-05 from `M22` / T22-T28 (`D22`)
- GitHub Issue: none
- Status: In progress

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
| T7 | 2026-10-05T17:10:05Z | Soak VMs of `M22` | Partial | Three automatic aborts dispatched once, stopped the appliance with rc 0 and ended Incomplete (shortened 14:00:05Z, default 07:20:06Z, a later shortened 17:10:05Z). A fourth automatic abort on 2026-10-06 (shortened, bundle `3e9815b0`, two consecutive failed budget samples; dispatched 04:15:07Z, appliance stopped in 11.86 s with rc 0, Incomplete) and one owner-requested abort (default, bundle `cb9b8106`; request file written 05:28:35Z, `etl-soak-abort.service` started, appliance stopped in 12.91 s with rc 0, Incomplete with only `observation_duration` failed) behaved the same way. The quiet-coverage case without abort and required-record loss were not run |
| T8 | 2026-10-05T23:25:06Z | A fresh Rocky 8.10 VM, shortened chain, bundle `3e9815b0`; rehearsal observation opened at 22:51:08Z; rotations with `journalctl --rotate` one minute after each fifth-minute sample | Partial; the observation aborted | Five rotations were made. The budget passed through the sample after the fourth retained user file (required 1,004,185,834 bytes) and failed at 23:20:00Z and 23:25:00Z (required 1,120,200,676 and 1,128,589,284 against 1,073,741,824): the user rate bound rose from 10,139 to 27,958 bytes/s when an interval saw a full 8-MiB allocation of a new user file, and the collector keeps the peak bound for the rest of the observation. Two consecutive failed samples dispatched the abort at 23:25:06Z; the verdict was Incomplete with `journal_retention_budget` failed. The sequence accounting passed at every sample and the store size measurement did not fail. The vacuum and idle phases ran on the aborted VM and prove nothing. The driver's first readings were empty because a redirect in its helper replaced the script input, so the planned vacuum after the first failing sample did not happen; the reader was corrected afterwards. The user rate bound had risen step by step before (14, 4,457, 7,688, 10,139 bytes/s). Second rehearsal on 2026-10-06 with bundle `11ee9c8e` on a fresh VM (observation opened 01:36:36Z, rehearsal 01:49:52Z to 03:26:22Z): two rotations, `journalctl --vacuum-files=4`, six further rotations, then twelve idle five-minute samples. The budget failed from the second rotation (1,080,202,551 required bytes, rising to 1,122,145,591 with sixteen retained files) and was recorded on eighteen consecutive samples without a sample error and without an abort request; the sequence accounting passed at every sample, including across the vacuum, where the expected entries of the retained range restarted at 6,226, and the store size measurement did not fail. The rehearsal ended with a deliberate `observe.py abort` (stop 11.31 s, rc 0, Incomplete). The budget separation of `D23` is observed; the budget formula itself is still the open decision of T6 |

##### Closure Evidence

- Not complete.

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

## Backlog

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

Unassigned work belongs here; the release tally above excludes this section.

## History

| Reset Date | Prior State Commit |
| --- | --- |
| 2026-08-17 | 38560eb9a1d2d761420d0f313328020e548c45c7 |
