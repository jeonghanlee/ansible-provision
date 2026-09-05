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

Next session entry point: none - every milestone is Complete except `M3`
(Deferred per `D3`); no external gate is Open. New work starts a new milestone
row. `M7` (harden the epics_build source build) is
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

Status tally: 10 Complete, 0 In progress, 1 Deferred. 1 external gate (Complete).

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
| Core | M7 | Harden the epics_build source build against a dropped connection | Milestone | Complete | Yes | D7 | The `epics_build` raw build survives or cleanly resumes an SSH drop without leaving a half-built tree; [detail](#m7---harden-the-epics_build-source-build-against-a-dropped-connection) |
| Core | M8 | Restore chrony poll/key/leap directives dropped by the operator rewrite | Milestone | Complete | No | D8 | `roles/common` renders per-server `minpoll`/`maxpoll` and `keyfile`/`leapsectz` when set and omits them when empty; production render verified on the production IOC server 2026-09-03; [detail](#m8---restore-chrony-pollkeyleap-directives-dropped-by-the-operator-rewrite) |
| Core | M9 | Share the EPICS install root safely across group deployers | Milestone | Complete | No | D9 | `roles/epics` prepares a group-shared install root (`root:<group>` `2775`, default ACL, system-wide git `safe.directory`) so any group member can clone and write; verified on the production IOC server 2026-09-03; [detail](#m9---share-the-epics-install-root-safely-across-group-deployers) |
| Core | M10 | Route EPICS firewall ports to per-service zones on a multi-homed IOC server | Milestone | Complete | No | D10 | `roles/epics` opens the CA and PVA port sets each in a site-configurable firewalld zone (empty keeps the default zone), validates the zone exists, and carries the protocol-correct port set; verified on the production IOC server 2026-09-03 (second apply `failed=0`, PVA zone carries UDP 5075); [detail](#m10---route-epics-firewall-ports-to-per-service-zones-on-a-multi-homed-ioc-server) |
| Core | M11 | Install the requested version in the app and EPICS roles | Milestone | Complete | No | D11 | The con/procServ/conserver and EPICS roles drop the install-once guard and install the requested version on every apply (EPICS re-checks out the tag; `epics_clone_mode` picks minimal single-OS or full multi-OS); verified on the production IOC server 2026-09-04 (con 1.1.0 replaced by 1.2.0, full mode carries every OS tree, second apply `failed=0`); delivered in `fd4ff1c`/`13bc8e6`; [detail](#m11---install-the-requested-version-in-the-app-and-epics-roles) |
| Gate | G1 | the production IOC server reaches the internal git host | External gate | Complete | No | | Reachability achieved through the site HTTP proxy's CONNECT tunnel (an ssh `ProxyCommand` over the proxy), not a firewall whitelist: the owner's key authenticates and `git ls-remote` returns the refs; confirmed 2026-09-03 by the successful iocserver clone (M4/T2) |

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
