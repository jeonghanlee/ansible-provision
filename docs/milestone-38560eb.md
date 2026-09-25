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

Next session entry point: the archiver-dev soak at aa-env `9eed006`. The schema
load is fixed: aa-env's `sql.fill` fix (G3, jeonghanlee/epicsarchiverap-env#47)
is on `modernize` at `1fc20a8`, and M14/T17 passed on a Rocky 8.10 and a Debian 13
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
restart. M14/T21, the one-day load test on the same host, started at
2026-09-25T09:46:12Z with 400 more 1 Hz scalars (500 PVs); a host timer adds 300
1 Hz scalars, 100 10 Hz scalars under the VeryFast policy and three
1000-element waveforms at 15:46Z (903 PVs), and another runs four retrieval
clients from 21:46Z for 6 h, each reading a random PV over a one-hour or one-day
window with a 2 s pause between requests. The heap stays at 256M so the result
compares with T20, and an instance lost to it is recorded as the limit (owner
decision 2026-09-25). The two end events are run by hand after
2026-09-26T09:46Z, with their times recorded, as T21 describes; the day-1 soak
IOC is `aasoak9-ioc.service`. The soak writes
its 5-minute CSVs (host, per-process, per-log-stream, per-tier first arrival,
retrieval, appliance metrics) and the load clients write `retrieval-load.csv`,
all to
`/var/tmp/aasoak9/` on the soak host from tools installed under
`/usr/local/share/aasoak9/`; the tool sources are local working files, not in
this repository. The IOCs, the sampler and the step timers are transient units
(`aasoak9-*`) that a reboot does not restore, so check
`systemctl list-units 'aasoak9*'` before reading the CSVs as a continuous
record. The pilot host - the Rocky 8.10 archiver-dev host kept from T17's
original three at `6a026d4` - was removed on 2026-09-25 after its records were
kept. Separately, M15 (lab-VM clocks from the KVM PTP clock in `common`) is in
progress under its plan accepted and authorized on 2026-09-25. The rest of the M14 scope is untouched:
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
remain aa-env responsibilities.
The full `archiver-dev` path follows aa-env and aa-maven readiness; M14 remains
Blocked on G2 for completion.

Milestone summary: `M13` (RedHat python provisioning
for EPICS source builds) is Complete: rocky8 and rocky10 clean operator runs,
pyDevSup builds on both, full public gz matrix 6/6 (issue #25). `M14` (middleware
server provisioning) is Blocked on `G2` (cloud-provision ships the middleware
package baseline and the middleware VM). Every other milestone is Complete
except `M3` (Deferred per `D3`); the one open external gate is `G2`. `M12` (keep
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

Status tally: 12 Complete, 1 In progress, 0 Not started, 1 Deferred, 1 Blocked. 3 external gates (2 Complete, 1 Open).

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env 4-OS source-build environment | Carry-forward | Complete | No | | Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass both source-build layers and checks; [detail](#m1---epics-env-4-os-source-build-environment) |
| Core | M2 | Ubuntu 26 source-build | Carry-forward | Complete | No | D4 | Ubuntu 26 passes the complete source-build path (both layers, `gz` flavor, repeated-run checks) with the C17 bridge active; [detail](#m2---ubuntu-26-source-build) |
| Core | M3 | base_os/app role hardening from production deployment | Carry-forward | Deferred | No | D3 | Deferred per D3 (old model retired); the base/app surface is re-verified under the operator model (M4); [detail](#m3---base_osapp-role-hardening-from-production-deployment) |
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
| Core | M15 | Discipline lab-VM clocks from the KVM PTP clock in the common operator | Milestone | In progress | No | D17 | On a KVM guest the `common` operator loads `ptp_kvm`, links `/dev/ptp_kvm` through a udev rule gated on the KVM clock name, and adds a PHC refclock to the chrony configuration it writes, so `timedatectl` reports the clock synchronized with PHC0 selected; where no KVM PTP clock exists the configuration carries no refclock and the site pools serve as before; the first `apt update` on the Debian path retries on a signature-date failure; [detail](#m15---discipline-lab-vm-clocks-from-the-kvm-ptp-clock-in-the-common-operator) |
| Gate | G1 | the production IOC server reaches the internal git host | External gate | Complete | No | | Reachability achieved through the site HTTP proxy's CONNECT tunnel (an ssh `ProxyCommand` over the proxy), not a firewall whitelist: the owner's key authenticates and `git ls-remote` returns the refs; confirmed 2026-09-03 by the successful iocserver clone (M4/T2) |
| Gate | G2 | cloud-provision ships the middleware package baseline and the middleware VM | External gate | Open | No | | The middleware operator/species structure and OS package baseline (system OpenJDK 21, Tomcat 9.0.121, MariaDB; no Maven package) originate in cloud-provision (`docs/milestone-e260630.md` M11) as the normative source and a middleware VM is provisionable there, before ansible-provision mirrors the set and layers its roles; owned by the cloud-provision session |
| Gate | G3 | aa-env ships a `sql.fill` that loads the configuration schema when the database and application account are provisioned externally | External gate | Complete | No | | Complete when the jeonghanlee/epicsarchiverap-env#47 fix commit is on `modernize` and aa-env records #47's acceptance as met: with only the application account, `make sql.fill` loads the schema, `make sql.show` lists `PVTypeInfo`, `PVAliases`, `ArchivePVRequests` and `ExternalDataServers`, and an absent database exits non-zero. Observing it on an archiver-dev host is M14/T17, not this gate; owned by the aa-env session; met 2026-09-23: the fix is `1fc20a8` on `modernize`, and #47 closed with aa-env's acceptance recorded |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D1 | Local `T` labels identify verification inside their owning work detail and are not independent work IDs. | Prior canonical register, prior state commit `38560eb` |
| D2 | Ubuntu 26 is excluded from the current source-build matrix and deferred to EPICS-env 1.3.1 or a later version. The 1.3.0 gate matrix does not include Ubuntu 26, and the `iocStats` GCC 15 fix is owned by EPICS-env. | Owner decision, 2026-08-17 |
| D3 | The staged old model (`01_base`/`02_apps`/`03_epics`) and its retained roles `base_os` and `app_epics` are retired; the operator/species model supersedes them. Removing the old roles and playbooks is separate follow-up work. | Owner decision, 2026-08-29 |
| D4 | Ubuntu 26 source-build is no longer deferred. The C17 bridge shipped under milestone 1.3.0 (`jeonghanlee/EPICS-env#29`), and `jeonghanlee/EPICS-env#63` (closed 2026-08-24) confirmed it fires for `iocStats` on the Ubuntu 26 source-build path; the complete `gz` path passed on 2026-08-27. Supersedes `D2`. | Owner decision, 2026-08-30 |
| D5 | The EPICS OS package regression (`M5`) is fixed across all six vacua, `pkg_automation` is removed from `roles/epics_build` in the same change, ansible-provision drafts the cloud `docs/IMAGE_WORKFLOW.md` change for LAB-cloud to land, and the milestone and GitHub issue are recorded before implementation begins. | Owner decision, 2026-08-31 |
| D6 | `M5` closes on the golden pair (rocky8, debian13), verified on both acquisition paths. The four non-golden vacua (rocky10, debian12, ubuntu24, ubuntu26) have no iocrunner golden pipeline; they carry the same package lists (names dry-run-verified) and move to `M6` for Live-mode verification. The cloud-side golden bake-matrix expansion stays a separate cloud-provision item. | Owner decision, 2026-08-31 |
| D7 | The `epics_build` source-build fragility surfaced during `M5` verification (LAB-cloud Finding B) is hardened as `M7`, not accepted. `M5`'s fix removed the known trigger (the NetworkManager restart); `M7` addresses the underlying structure so a dropped connection cannot leave a half-built tree. | Owner decision, 2026-08-31 |
| D8 | The chrony per-server `minpoll`/`maxpoll` and `keyfile`/`leapsectz` directives dropped by the operator rewrite (`0012e2d`) are restored into `roles/common`, mirroring the `M5` EPICS-package regression from the same rewrite. Empty defaults keep the baseline render unchanged; site overrides (the production IOC server) render the production directives. | Owner decision, 2026-09-02 |
| D9 | With `epics_install_group` set, the EPICS install root stays `root:<group>` `2775` (setgid) and gains a default ACL on local disk plus a system-wide git `safe.directory` on the deploy server, so any group member can run git on the single shared repository and write into it. Owner-owned roots (one deployer only), per-user `safe.directory` (per-member setup), a per-member subdirectory layout (the ioc-runner per-engineer model, unsuited to a single distribution tree), and a dedicated deploy account were rejected for the one-server-deploys/many-hosts-read topology. Site prerequisites (consistent group GID, `root_squash` pinning deploy to the filesystem server, NFSv4 idmapping) stay in the site provisioning record. | Owner decision, 2026-09-02 |
| D11 | The con, procServ, and conserver roles and the EPICS role drop the install-once guard so a re-apply installs the requested version, replacing the installed one; whether the installed version matches the requested one is verified by the separate site verification tool, not by these roles. `con_version` is a git tag on the con repository, while `procserv_version` and `conserver_version` select a wrapper-repo ref whose upstream daemon version is pinned inside the wrapper (`configure/RELEASE` `SRC_TAG`), so the role controls the wrapper ref only. The EPICS distribution checkout adds `epics_clone_mode`: `minimal` (default) is a shallow, blob-filtered, single-OS sparse checkout for a Docker or single-OS host; `full` is a plain clone of every OS tree for a production NFS server. Both modes re-check out the requested tag in place, full disables sparse so a mode switch expands correctly, and an unknown mode value fails loudly. The roles keep `changed_when: false`. | Owner decision, 2026-09-04 |
| D10 | EPICS firewall ports are opened per service in site-configurable firewalld zones (`epics_ca_zone`, `epics_pva_zone`; empty keeps the default zone for single-homed hosts) because a multi-homed IOC server binds CA and PVA to different interfaces and zones, where the default zone carries no interface. The role validates that a named zone exists and fails loudly rather than silently skipping; it does not create zones (site infrastructure). The port sets follow the protocol constants — CA 5064 TCP+UDP and 5065 UDP, PVA 5075 TCP+UDP and 5076 UDP — dropping the previously opened 5065/TCP, which is not an EPICS port. | Owner decision, 2026-09-03 |
| D12 | The rocky-family in-place cloud-init upgrade run by `roles/epics_build`'s `dnf update` fires rpm's tmpfiles trigger, which resets `/run/cloud-init` to 0700 until the next boot and breaks an unprivileged `cloud-init status`. The fix lands in the role that causes it, not cloud-provision's cloud-init templates: cloud-provision recorded a Closed Door (2026-09-08, commit `47c1bb5`) because a template runcmd would move the proxy apply out of last position (proxy ADR D018). The role writes an `/etc/tmpfiles.d/cloud-init.conf` override (`d /run/cloud-init 0755 root root - -`) that shadows the vendor rule and applies it immediately with `systemd-tmpfiles --create`, chosen over a one-shot `chmod` because the override also survives a later `systemd-tmpfiles --create`. Rocky family only; debian ships no such rule. Mirrors the 2026-08-17 vmadmin-home 0700 precedent, fixed in ansible-provision. | Owner decision, 2026-09-09 |
| D13 | The RedHat-family python provisioning gap - no Python dev headers, so a pyDevSup C extension fails with `Python.h` missing on Rocky - is fixed in `roles/python` by mirroring the Debian `python3-dev`: add `python3-devel` to the default `pkg_python_redhat` (reaching rocky10 and any generic RedHat vacuum) and `python39-devel` to the rocky8 override (matching its 3.9 module). The milestone and GitHub issue (#25) are recorded before the code change; implementation status and live rocky verification (T2) are tracked in the M13 detail. | Owner decision, 2026-09-10 |
| D14 | The rocky8 python operator set only the unversioned `python` alternative, leaving `python3` at the system 3.6, so pyDevSup built against absent 3.6 headers. The operator now sets a `runtime_python_alts` list of name -> path pairs, applying each only when its alternatives group exists and failing loudly when a present group cannot be set (replacing the silent `\|\| true`). rocky8 sets `python3 -> /usr/bin/python3.9` (the versioned target pyDevSup reads) and `python -> /usr/bin/python3` (which then follows python3 to 3.9); setting `python -> python3.9` directly is avoided because the unversioned `python` group does not reliably register `python3.9`. The system python 3.6 is kept, not removed: RHEL8 platform-python depends on it, so the supported switch is alternatives. | Owner decision, 2026-09-11 |
| D15 | Middleware server provisioning (a middleware server, the middleware counterpart of the IOC dev host) is built in ansible-provision the same way the IOC species are: a new `java` operator role pins a non-system OpenJDK/Maven (dnf module stream + `alternatives`, with override keys `maven_module_version`/`pkg_java`/`java_alternatives_path` and a Maven settings template) and a middleware species layers it on `common`+`epics`, with Phoebus as the middleware application and a middleware group analogous to `ioc`. The internal lineage origin these repos derive from is a substance reference only (OpenJDK 21 + Maven 3.8, Phoebus); internal endpoints stay out of this public repository and are supplied through the site override layer. The cloud-provision package baseline and the middleware VM are the normative source and land first (G2). Sub-decisions left pending: increment scope (Java/Maven runtime first vs with Phoebus), the middleware group name and GID policy, the pinned Java default version, and the species name and target vacuum. | Owner decision, 2026-09-11 |
| D16 | Middleware server provisioning follows the cloud-provision middleware plan (`docs/milestone-e260630.md` M11, D2, D3): system Java (the distribution OpenJDK 21 with `JAVA_HOME` at the distribution path), no non-system pin and no Maven package (aa-maven supplies Maven 3.9.9 through its Maven Wrapper on the source-build path only), Tomcat 9.0.121 as the shared `CATALINA_HOME` and MariaDB (SQLite later) as the Archiver Appliance baseline, the Archiver Appliance and Phoebus installed from their binary distribution repositories (aa-distribution, phoebus-distribution) with source-build alternatives, and service group `mid` / user `mid-srv` parallel to `ioc` / `ioc-srv`. Supersedes the pinned non-system OpenJDK/Maven and Phoebus-build substance of `D15`; the ansible-provision-way build and the site override layer from `D15` stand. | Owner decision, 2026-09-12 |
| D17 | The lab-VM time-sync fix handed off by cloud-provision (jeonghanlee/cloud-provision#44: lab VMs never reach NTP sync because the public pools are unreachable behind the site proxy, and one Debian apply failed its first `apt update` on a signature date) is implemented in ansible-provision's `common` operator, the single writer of `chrony.conf`, not in cloud-init. | Owner decision, 2026-09-25 |

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
cloud-provision `docs/IMAGE_WORKFLOW.md` states the requirement first (LAB-cloud
writes it).

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
  for LAB-cloud; record the milestone and issue before starting.
- Cloud-first ordering: the normative operator definition (cloud-provision
  `docs/IMAGE_WORKFLOW.md`, LAB-cloud single-writer) lands before the ansible
  implementation.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner decisions 2026-08-31 (`D5`)
- Implementation Authorization: owner, 2026-08-31
- Superseded Plan Artifacts: none

1. Reconcile the per-OS EPICS package list (`work/plan-epics-os-packages.md`, Phase 0).
2. Draft the cloud `docs/IMAGE_WORKFLOW.md` change; LAB-cloud lands it.
3. Install the list in `roles/epics`; remove `pkg_automation.bash` from `roles/epics_build`.
4. Re-bake per OS via LAB-cloud; verify.

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
- Package names dry-run-verified by LAB-cloud on 2026-08-31 (rocky10 needs `P_common`'s
  EPEL+CRB, which the species order provides).

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Distribution path: LAB-cloud Live-applies the `iocrunner` species per OS with a
   published tree (rocky10, ubuntu24), checks net-snmp + IOC link, discards the VM.
2. Source-build path: LAB-cloud Live-applies the `epics_dev` species per OS (all four),
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
`ansible.builtin.raw` task over SSH. During `M5` verification (LAB-cloud Finding
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

- Origin decision `D7` (2026-08-31): harden rather than accept (LAB-cloud Finding
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
`D7`'s intent; LAB-cloud validated the direction by manually detaching the build
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
| T1 | 2026-09-01 | rocky8 (lab-rocky8-epics-dev-t1) | Passed | Real path on a fresh rocky8 VM at master 72fa9a9: after the build unit went active, killing the local ansible process left the detached unit still building (single unit, no orphan); a retry reported `EPICS_ENV_BUILD_RUNNING` (changed=false, no second build); a genuine dnf failure was reported `FAILED rc=2` without hanging; a full `epics_dev` run completed (`ok=18 changed=6 failed=0`, Wait `DONE`, install tree `/opt/epics/1.3.0/rocky-8.10/7.0.10/setEpicsEnv.bash`, success sentinel present); a re-apply was idempotent (`ok=4 changed=0`). |

##### Closure Evidence

- T1 passed 2026-09-01 on a fresh rocky8 VM (lab-rocky8-epics-dev-t1, provisioned
  by LAB-cloud) against ansible-provision master 72fa9a9 (role commit 91a9470):
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
  package: the source-build path obtains Maven 3.9.9 through the aa-maven
  Maven Wrapper (`./mvnw`).
- A `tomcat` operator: Tomcat 9.0.121 (Apache tarball) as the shared
  `CATALINA_HOME` only; the Archiver Appliance instance skeleton, `server.xml`
  / `context.xml`, and schema stay with aa-env.
- A `mariadb` operator: the MariaDB server with the `archappl` database and
  user, kept a separable module because aa-env replaces it with SQLite later.
- Application operators `archiver` and `phoebus`: install the aa-distribution
  WARs and the phoebus-distribution binary, each paired with a source-build
  operator (`archiver-build` builds aa-maven at its freeze tag with `./mvnw`
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
repositories (aa-env and phoebus-env); the Archiver Appliance instance layout
and schema (aa-env); the site override values (the `server-configuration`
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
- `G3` (added 2026-09-23, Complete 2026-09-23): aa-env's `sql.fill` loaded no
  schema when the database and application account are provisioned externally,
  as this operator provisions them, and exited 0 anyway
  (jeonghanlee/epicsarchiverap-env#47, owned by the aa-env session). Fixed in
  `1fc20a8` on `modernize`; #47 closed with aa-env's acceptance recorded. The
  operator's post-`sql.fill` table check stays as a guard. `M14` stays Blocked
  while `G2` is Open and resumes as In progress when it is Complete.
- `D15` (owner, 2026-09-11): build it the ansible-provision way; internal
  specifics via the site override layer. Its pinned non-system Java/Maven and
  Phoebus-build substance is superseded by `D16`.
- `D16` (owner, 2026-09-12): system Java with `JAVA_HOME`, no Maven package
  (aa-maven wrapper on the source-build path), Tomcat 9.0.121 and MariaDB as
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
  confirmation with aa-maven on ownership.
- Increment order (2026-09-15): add the standalone `java` operator first and
  reuse `proxy`, `common`, `provenance`, `python`, and `epics` unchanged.
  Tomcat, MariaDB, and the full `archiver-dev` assembly follow; aa-env and
  aa-maven are required for the application path.
- EPICS distribution selector (2026-09-15): use 1.3.0 as the `epics` role
  default, with Base 7.0.10. Existing operator behavior remains unchanged.
- `archiver_build` realization (owner, 2026-09-18): the operator drives aa-env's
  make sequence (aa-env clones and builds aa-maven from source internally); it
  does not build aa-maven separately. Runs as root like the other build
  operators - no build-user split, since aa-env's internal sudo no-ops when
  already root and `make install` chowns the instances to `mid-srv:mid`
  regardless. Pinned aa-env `fb43522` and aa-maven `SRC_TAG=3c96141d`; the aa-env
  pin moved to `e06c554` on 2026-09-21, to `6a026d4` on 2026-09-22 and to
  `1fc20a8` on 2026-09-23 (see the increment status). Variable
  placement: `configure/RELEASE.local` (SRC_TAG) and `../CONFIG_SITE.local` -
  one directory above the checkout, which survives the OS-conf rewrite -
  (AA_USERID/AA_GROUPID, DB name/user/pass, DB_HOST_NAME=127.0.0.1,
  DB_HOST_PORT, JAVA_HOME/TOMCAT_HOME). Pre-create `mid`/`mid-srv` with a
  site-set GID (ioc/ioc-srv precedent); default `als` overlay; skip aa-env
  `db.secure`/`db.addAdmin`/`db.create` (the `mariadb` operator makes the DB and
  account) and `install_os_packages.bash` (the operators supply the packages).
  Checkout at `/opt/epicsarchiverap-env-src`. Boundary: aa-env owns each make
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
- archiver_build authorization: 2026-09-18 (drive aa-env's make sequence as root
  in order: `init` -> `db.conf` -> `conf.archapplproperties` -> `build.mvn` ->
  `sql.fill` -> `conf.storage` -> `install` -> `sd_start`; never `make build`
  wholesale, which bundles the root `conf.storage`. Realization per the
  2026-09-18 sub-decision above.)
- Superseded Plan Artifacts: none

Developed before `G2` rather than after: `G2` completes when cloud-provision M11
merges to master, which follows M11/T2, which needs these M14 roles - so the
non-deadlocking path is to develop on the branch against the M11 branch
definition now (owner + LAB-CLOUD, 2026-09-14).

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
   Database creation uses aa-env's `utf8mb4` default. Schema, the separate admin
   workflow, and JDBC/client transport configuration remain with aa-env.
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
| T17 | Integration | Apply the `archiver_build` build steps (`init`, `db.conf`, `conf.archapplproperties`, `build.mvn`) as root with the pinned aa-env ref (`fb43522` when this ran) + aa-maven `SRC_TAG=3c96141d`; inspect the produced WARs and the als overlay in `WEB-INF/classes`, and the schema load by the configuration database's tables (`make sql.show`), never by `sql.fill`'s exit status | Rocky 8.10 and Debian 13 archiver-dev VMs, and a freshly provisioned host | The four `aa-*-{mgmt,engine,etl,retrieval}.war` build with the als `appliances.xml`/`archappl.properties`/`policies.py` packed; `sql.fill` loads the schema over TCP as `archappl@'127.0.0.1'`, and the database holds `PVTypeInfo`, `PVAliases`, `ArchivePVRequests` and `ExternalDataServers` |
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
| T17 | 2026-09-23T09:05:24Z | The current three archiver-dev hosts (Rocky 8.10 x2, Debian 13): T17's original third host, and two hosts rebuilt through this operator on 2026-09-21 after the original run; all three installed at aa-env `6a026d4` since 2026-09-22 | Failed | The build half holds, observed 2026-09-21T06:23:08Z: our `archiver_build` operator ran `init`, `db.conf`, `conf.archapplproperties` and `build.mvn` as root on the original three hosts, and the als classpathfiles are packed as required: `appliances.xml`, `archappl.properties` and `policies.py` are each present in `WEB-INF/classes` of all four deployed webapps, generated into `site-template/siteid/classpathfiles` by `copy.sitespecific` within `build.mvn`. The two proxy defects in the increment status below - the detached unit carrying no proxy, and Maven not reading one from the environment - blocked that run first and had to be fixed. The schema half fails: `sql.fill` loaded nothing on any host. The 2026-09-21 result counted the load as executed because `sql.fill` exited 0 under `set -e`, but the exit status does not show the load. Inspected on the current three hosts: the configuration database exists and holds zero tables (`information_schema.tables` count 0); mgmt on every host logs `Table 'archappl.PVTypeInfo' doesn't exist` at each start, when it loads PV configuration from the database (`Loading PVTypeInfo from persistence`), and on the host where PVs were registered it logs the same error, and the same for `PVAliases`, on each registration. Cause, read from aa-env's scripts: `query_from_sql_file` first checks the database through `isDb`, which logs in as the admin account (`DB_ADMIN`, default `admin`) that this mode never creates, so the check reports the database absent; the not-found path prints `There is no >> archappl << in the dababase` beside the MariaDB `Access denied for user 'admin'` error - both lines stand in every build log - and then ends in a bare `exit`, which returns 0. The operator now counts the tables right after `sql.fill` and stops when there are none or the count cannot be read (fifth defect in the increment status below). |
| T17 | 2026-09-23T22:10:06Z | A Rocky 8.10 and a Debian 13 archiver-dev host rebuilt through this operator (`a3f9949`) at aa-env `1fc20a8` with `archiver_force_reinstall=true`; both hosts were removed afterwards | Passed | Observed between 22:07:52Z and 22:10:06Z on both hosts: the install stamp carries `envref=1fc20a8`; `CONFIG_SITE.local` carries `MAVEN_FLAGS:=-gs /etc/maven-proxy-settings.xml`, and the build log shows its use and `BUILD SUCCESS`; the four WARs carry the als classpathfiles; `sql.fill` loaded the schema and the operator's table check let the build continue, its first run inside a build; `make sql.show` lists `ArchivePVRequests`, `ExternalDataServers`, `PVAliases` and `PVTypeInfo`; mgmt answers 200, aa-env's health service and timer are installed, and mgmt logs no persistence error. The host then carrying the soak, now the pilot host, stayed at `6a026d4` with an empty configuration database; T17 there was the remaining check (owner decision 2026-09-23). |
| T17 | 2026-09-24T09:15:13Z | The soak host: a fresh Rocky 8.10 archiver-dev VM, the full species applied from `dca2255` at aa-env `9eed006` with the README test store values | Passed | The apply ran 08:49:29Z-09:08:21Z with `failed=0`. The install stamp carries `envref=9eed006` and the store values; `CONFIG_SITE.local` carries `MAVEN_FLAGS` and the five store lines; the installed `policies.py` and the copy packed into the mgmt webapp carry `PARTITION_5MIN` hold 2, `PARTITION_HOUR` hold 2 and `PARTITION_DAY`; the build log shows the settings file and `BUILD SUCCESS`; the database holds the four tables; all four JVMs run `-Xms256M -Xmx256M`; the health service and timer are installed; mgmt answered 200 at 09:09:03Z once initialised and logs no missing-table error. After 100 PVs were registered, `PVTypeInfo` held 100 rows at 09:15:13Z. This settles the remaining check the 2026-09-23 row named, on a new host instead of the old one (owner decision 2026-09-24). |
| T20 | 2026-09-25T09:27:24Z | The soak host (Rocky 8.10, 2 vCPU, 3.6 GiB) at operator `dca2255`, aa-env `9eed006` and the README test store values; 100 PVs registered at 2026-09-24T09:09:52Z | Passed | Over 23.9 h of 5-minute samples: the installed `policies.py` carries the test values and T17 passed on this host (row above); STS held all 100 PVs at 09:15Z, MTS at 09:30Z and LTS at 12:15Z, and the second LTS day partition existed for all 100 by 03:15Z on 2026-09-25, about 3 h 15 min after midnight; the unit stayed active with four instances, mgmt 200 and health success in every sample, one PID per JVM all day and kernel OOM 0; retrieval returned the full sample count in every window after the first. The appliance was restarted at 09:25:03Z on 2026-09-25, about 9 h 25 min after midnight: four new JVMs, mgmt 200 at 09:26:01Z, `PVTypeInfo` still 100 rows and all 100 PVs Being archived again, no missing-table error; archiving paused 55 s for the 1 Hz, 10 Hz and waveform PVs and 60 s for a 0.1 Hz PV. Resources: CPU idle mean 96%, MemAvailable 1.23-1.50 GB, no swap; JVM RSS 374-500 MiB each, heap used at most 241 MiB of 256M (etl), full GC 0; `/arch` 3.60 GB, of which LTS 3.11 GB (a 1000-element waveform about 0.69 GB per day, a 1 Hz scalar about 1.9 MB). Logs: the four logs directories together about 480 KB/h; mgmt `catalina.out` 151 KB/h, engine `catalina.out` 133 KB/h plus its dated JULI file 126 KB/h (CA client beacon and duplicate-response records), retrieval 52 KB/h, etl none after startup; ERROR 3, all during mgmt initialisation, and Exception 0. |
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
privilege split and the ordered make sequence are no longer derived from aa-env's
Makefiles - both were executed and observed (T17, T18). Four defects surfaced in
that first end-to-end run and are resolved in the role, a fifth was found
later on the current hosts, two of them rebuilt after that run, and a sixth came
with the fix for the fifth:

- A detached `systemd-run` unit inherits no `/etc/profile.d`, so the build carried
  no proxy and could not fetch Maven. The build script now sources the proxy
  contract profile itself. The systemd-level equivalent is open on cloud-provision's
  side, so this stays until that is settled.
- Maven takes a proxy only from a settings file. Measured against the pinned
  aa-maven source with Maven 3.9.16: the shell proxy variables, `mvn
  -Dhttps.proxyHost`, and `MAVEN_OPTS` carried as JVM startup arguments each leave
  Maven Central unreachable, while a settings file selected with `-gs` resolves.
  That file belongs to the cloud-provision proxy contract (`0099673`); this
  operator consumes it and generates none, and a proxied host without it is
  refused before the build starts rather than failing inside mvn.
- Four appliance instances at aa-env's default 1G heap each oversubscribe a 4 GB
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
  Failed at `6a026d4`). aa-env's `sql.fill` checked the database through the admin account
  before loading, and in this mode no admin account exists: the separate admin
  workflow is left to aa-env (MariaDB design above), while aa-env's own install
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
  check passed. aa-env fixed `sql.fill` in `1fc20a8`
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

Pinned aa-env ref moved to `e06c554` (2026-09-21). `fb43522` is its ancestor, and
nothing under `site-template/`, `scripts/`, `configure/CONFIG_SITE` or
`configure/CONFIG_SRC` differs between the two, so every override this operator
writes carries across unchanged; what did change is the build recipe, which now
passes `-DskipTests` (only the flag is observable here; aa-env reports the tests
moved to aa-maven CI), and `debian13.pkgs`,
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

Pinned aa-env ref moved to `6a026d4` (2026-09-22, `247f350`). It is seven commits
ahead of `e06c554`, and its one policy change sets the MTS store to
`PARTITION_DAY` (from `PARTITION_MONTH`, `hold=2` unchanged). All three current
archiver-dev hosts were force-reinstalled at `6a026d4` around 2026-09-22T00:29Z,
as their install stamps and JVM start times show; every observation after that,
including the T17 schema inspection, comes from that ref.

Pinned aa-env ref moved to `1fc20a8` (2026-09-23). It is twelve commits ahead of
`6a026d4` and carries the `sql.fill` fix (G3), a 256M heap default, a systemd
health timer for missing instances and the removal of the jsvc path. It also
renames aa-env's Maven flag hook from `MAVEN_OPTS` to `MAVEN_FLAGS` (`84b38e5`),
so the operator now writes `MAVEN_FLAGS` and needs `84b38e5` or later. Two hosts
were rebuilt at `1fc20a8` with `archiver_force_reinstall=true` on 2026-09-23 for
the T17 re-run and then removed; the pilot host stayed installed at `6a026d4`
until it was removed on 2026-09-25.

Pinned aa-env ref moved to `9eed006` (2026-09-24). It is nine commits ahead of
`1fc20a8` and renders the store granularity and hold of each tier from Make
variables (`ARCHAPPL_STS_GRANULARITY`, `ARCHAPPL_STS_HOLD`,
`ARCHAPPL_MTS_GRANULARITY`, `ARCHAPPL_MTS_HOLD`, `ARCHAPPL_LTS_GRANULARITY`;
jeonghanlee/epicsarchiverap-env#50). Their defaults are the previous values, so
an install that sets none keeps STS `PARTITION_HOUR` hold 2, MTS `PARTITION_DAY`
hold 2 and LTS `PARTITION_YEAR`. aa-env checks each name and hold in
`conf.policies` but leaves the order across tiers to the caller. The operator
exposes the five as `archiver_store_*`, writes only those that are set, and
refuses a partial, unknown, out-of-order or non-positive set before a build
starts. The rest of the range makes the database backup, listing and restore
exit non-zero on failure, paths this operator does not call. The config stamp
now carries the store values, so every installed host reports drift on its next
plain re-apply and moves only with `archiver_force_reinstall=true`. Verified
before any host run: the rendered launch step accepts the empty, full and
hold-only sets and refuses eight malformed ones before stopping anything; fed
the `CONFIG_SITE.local` lines the rendered build step writes, aa-env `9eed006`'s
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
`archiver-dev` assembly remain unverified until aa-env and aa-maven integration.

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
- Status: In progress

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

## Backlog

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

No unassigned work in this generation. Unassigned work belongs here; the
release tally above excludes this section.

## History

| Reset Date | Prior State Commit |
| --- | --- |
| 2026-08-17 | 38560eb9a1d2d761420d0f313328020e548c45c7 |
