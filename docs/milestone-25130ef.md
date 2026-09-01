# Work Register

## Scope

This document is the canonical work register for the `master` release line of
`ansible-provision` after the reset carried by prior state commit `25130ef`.
It records unfinished deliverables, external gates, accepted plans, and
verification needed to continue the current generation.

**Out of scope:** completed work remains reachable in the prior state commit;
detailed operating procedures remain in the linked runbooks; EtherCAT execution
remains in the owner's separate tracker.

The prior generation's Version 1.0 release convention — the joint
`iocrunner-gate-1.0.0` tag on `cloud-provision` (`2b77a97`) and
`ansible-provision` (`3981c21`), naming the gate environment that bakes and
runs the `epics-ioc-runner` consumer gate — was executed under the prior
generation and, together with its completed milestones, is retained at commit
`25130ef`.

The 1.3.0 EPICS-env gate ran its source-build OS matrix. Ubuntu 26 was
initially outside that matrix, but the C17 bridge shipped under 1.3.0
(`jeonghanlee/EPICS-env#29`) and its firing on the Ubuntu 26 source-build path
was confirmed (`jeonghanlee/EPICS-env#63`), so Ubuntu 26 now passes as well
(see `M2` and `D4`).

- Release line: master
- Milestone index: 25130ef
- Canonical path: `docs/milestone-25130ef.md`
- Canonical branch or ref: `master`
- Git upstream: `origin/master`
- Remote tracker: `jeonghanlee/ansible-provision`, GitHub milestone `Backlog`

Next session entry point: `M6` (verify the four non-golden vacua) — LAB-cloud
applies the iocrunner species Live per vacuum and reports; record each per-vacuum
result. `M5` (EPICS OS package set) is Complete: the golden pair is verified on
both acquisition paths and `pkg_automation` is retired. `M4` (operator/species
provisioning model) remains active. `M4/T1` (species syntax-check and `configure/RELEASE` / `inventory/lab.ini`
enumeration) and `M4/T3` (P_proxy apply and full-species re-apply idempotency)
are verified; `M4/T2` (iocserver on the production IOC server) is the only remaining check and
is blocked on `G1`. `M3` (base_os/app role hardening) is Deferred per
`D3`: the old model is retired, so its Debian 13 re-verification is not pursued.
`M1` (4-OS source-build) and `M2` (Ubuntu 26 source-build) are both Complete;
the C17 bridge (`jeonghanlee/EPICS-env#29`) fires on Ubuntu 26 and its
source-build path was confirmed (`jeonghanlee/EPICS-env#63`).

Status tally: 3 Complete, 1 In progress, 1 Deferred, 2 Not started. 1 external gate (Open).

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env 4-OS source-build environment | Carry-forward | Complete | No | | Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass both source-build layers and checks; [detail](#m1---epics-env-4-os-source-build-environment) |
| Core | M2 | Ubuntu 26 source-build | Carry-forward | Complete | No | D4 | Ubuntu 26 passes the complete source-build path (both layers, `gz` flavor, repeated-run checks) with the C17 bridge active; [detail](#m2---ubuntu-26-source-build) |
| Core | M3 | base_os/app role hardening from the production IOC server deployment | Carry-forward | Deferred | No | D3 | Deferred per D3 (old model retired); the base/app surface is re-verified under the operator model (M4); [detail](#m3---base_osapp-role-hardening-from-the production IOC server-deployment) |
| Core | M4 | Operator/species provisioning model | Milestone | In progress | No | G1 | Vacua, single-role operators, and species assemblies replace the staged model, iocserver registered; P_proxy role implemented and verified (apply and full-species re-apply idempotency), and the live iocserver run blocked on G1; [detail](#m4---operatorspecies-provisioning-model) |
| Core | M5 | Restore the EPICS OS package set into the operator model | Milestone | Complete | No | D5 | `epics_os_packages` installed by `roles/epics` and `roles/epics_build`, `pkg_automation.bash` retired; verified on the golden pair (rocky8, debian13) across both acquisition paths; four non-golden vacua moved to `M6`; [detail](#m5---restore-the-epics-os-package-set-into-the-operator-model) |
| Core | M6 | Verify EPICS OS build dependencies on the four non-golden vacua | Milestone | Not started | Yes | D6 | rocky10, debian12, ubuntu24, ubuntu26 install `epics_os_packages` and link a sample IOC, verified by Live-mode species apply per vacuum; [detail](#m6---verify-epics-os-build-dependencies-on-the-four-non-golden-vacua) |
| Core | M7 | Harden the epics_build source build against a dropped connection | Milestone | Not started | Yes | D7 | The `epics_build` raw build survives or cleanly resumes an SSH drop without leaving a half-built tree; [detail](#m7---harden-the-epics_build-source-build-against-a-dropped-connection) |
| Gate | G1 | the production IOC server added to the the internal git host clone whitelist | External gate | Open | No | | Network team whitelists the production IOC server so the EPICS distribution clone and a live iocserver run reach the internal git host; blocks M4/T2 |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D1 | Local `T` labels identify verification inside their owning work detail and are not independent work IDs. | Prior canonical register, prior state commit `25130ef` |
| D2 | Ubuntu 26 is excluded from the current source-build matrix and deferred to EPICS-env 1.3.1 or a later version. The 1.3.0 gate matrix does not include Ubuntu 26, and the `iocStats` GCC 15 fix is owned by EPICS-env. | Owner decision, 2026-08-17 |
| D3 | The staged old model (`01_base`/`02_apps`/`03_epics`) and its retained roles `base_os` and `app_epics` are retired; the operator/species model supersedes them. Removing the old roles and playbooks is separate follow-up work. | Owner decision, 2026-08-29 |
| D4 | Ubuntu 26 source-build is no longer deferred. The C17 bridge shipped under milestone 1.3.0 (`jeonghanlee/EPICS-env#29`), and `jeonghanlee/EPICS-env#63` (closed 2026-08-24) confirmed it fires for `iocStats` on the Ubuntu 26 source-build path; the complete `gz` path passed on 2026-08-27. Supersedes `D2`. | Owner decision, 2026-08-30 |
| D5 | The EPICS OS package regression (`M5`) is fixed across all six vacua, `pkg_automation` is removed from `roles/epics_build` in the same change, ansible-provision drafts the cloud `docs/IMAGE_WORKFLOW.md` change for LAB-cloud to land, and the milestone and GitHub issue are recorded before implementation begins. | Owner decision, 2026-08-31 |
| D6 | `M5` closes on the golden pair (rocky8, debian13), verified on both acquisition paths. The four non-golden vacua (rocky10, debian12, ubuntu24, ubuntu26) have no iocrunner golden pipeline; they carry the same package lists (names dry-run-verified) and move to `M6` for Live-mode verification. The cloud-side golden bake-matrix expansion stays a separate cloud-provision item. | Owner decision, 2026-08-31 |
| D7 | The `epics_build` source-build fragility surfaced during `M5` verification (LAB-cloud Finding B) is hardened as `M7`, not accepted. `M5`'s fix removed the known trigger (the NetworkManager restart); `M7` addresses the underlying structure so a dropped connection cannot leave a half-built tree. | Owner decision, 2026-08-31 |

### Milestone Details

#### M1 - EPICS-env 4-OS Source-Build Environment

- Origin: 25130ef / M1
- Identity History: new reset-generation identity; prior scope and evidence are reachable from commit `25130ef`. Ubuntu 26 was split out to `M2` (Deferred) by owner decision `D2` on 2026-08-17, narrowing this row to the four passing OSes.
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
- Plan Acceptance: accepted plan preserved from prior state commit `25130ef`
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
| T2 | 2026-07-28 | Debian 13 | Passed | Commits `5c4f7fc` and `0148514` |
| T3 | 2026-07-28 | Debian 13 | Passed | Commit `5c4f7fc`, absolute paths reduced from 9 to 0 |
| T4 | 2026-07-28 | Debian 13 | Passed | Commit `0148514` |
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

- Origin: 25130ef / M2
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

#### M3 - base_os/app role hardening from the production IOC server deployment

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
  local connection (`593f161`).
- chrony.conf directives became site-overridable variables; a `trim_blocks`
  newline drop that joined the pool lines and broke `chronyd` restart was fixed
  with a `+%}` control (`1f1e996`, `6069b54`).
- Rocky `python` default set to 3.9 via an `alternatives --install` of the
  unversioned-python master link before `--set` (`9ba3b13`, Rocky-only).
- con/procServ/conserver gained branch/tag/commit version pinning (`bf6b798`).
- `app_epics` clones the distribution as the IOC owner, sparse and tag-pinned,
  into a group-writable install root, so a host with no root ssh key can pull
  from an internal remote (`88e569b`).

**Out of scope:** the the production IOC server deployment record and its site-specific
overrides live in the `server-configuration` repository, not here.

##### Verification Results

| Check | Result | OS | Evidence |
| --- | --- | --- | --- |
| T1 | Verified | Rocky 8 | the production IOC server: `01_base`/`02_apps` completed, chrony synced (`^*`, Reach 377), `python --version` 3.9.25 from a clean 3.6.8 state, con/procServ/console/conserver installed. |
| T2 | Not run | Debian 13 | os-detect, chrony render, version pinning, and epics owner-clone touch the shared/Debian path but were exercised only through `--syntax-check`; a Debian 13 run is pending. |

#### M4 - Operator/species provisioning model

Origin: 25130ef / M4

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
  `92f04c4`, `08ec916`, and `60d2c2c`, matched char-for-char to the SOT
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
cloud-provision); the the production IOC server site record and overrides (the
`server-configuration` repository); EtherCAT live execution (owner's separate
tracker).

##### Completion Criteria

Every named species assembly resolves and applies in operator-model order,
iocserver applies cleanly on the production IOC server, and P_proxy is either built and applied
or explicitly deferred by owner decision.

##### Dependencies And Decisions

- `G1` (the production IOC server the internal git host whitelist) blocks the live iocserver run
  (`T2`); resume `T2` as Not started when `G1` closes.
- P_proxy depends on cloud-provision shipping `bin/proxy_contract.bash` as the
  single authority; the SOT P_proxy precondition lands together with the
  `roles/proxy` implementation.

Plan Status: draft
Plan Acceptance: none
Implementation Authorization: none
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
| T1 | Passed | control host; debian12 (epics_dev) | All eight species playbooks (`bare`, `epics_dev`, `ethercat`, `iocrunner`, `iocrunner_nfs`, `iocserver`, `nfs_sim`, `rtbase`) pass `ansible-playbook --syntax-check`, and every species is enumerated in `configure/RELEASE` `SPECIES_PLAYBOOKS` with its `inventory/lab.ini` group present for every non-bare species (bare is vacuum-only by design); no stray non-vacuum groups. Registration landed in `92f04c4`, `08ec916`, `60d2c2c`. Live evidence: after `35f00fe`, `epics_dev` applied on a real debian12 host (PLAY RECAP `ok=15 changed=4 failed=0`) installing EPICS-env 1.3.0 / base 7.0.10 layers 1+2 at `/opt/epics/1.3.0/debian-12/7.0.10`, and the `gz` flavor of the same path also passed (`make build.gz`, `ok=15 changed=4 failed=0`), both observed by the cloud-provision session. |
| T2 | Blocked | Rocky 8 (the production IOC server) | Blocked by `G1`: the production IOC server cannot reach the internal git host for the EPICS distribution clone. |
| T3 | Passed | Debian 13, Rocky 8 | Apply verified 2026-08-31 via proxied iocrunner golden-image bakes: `proxy_contract.bash` applied with proxy seal `clean=true`, and the proxied `pip` installed `epicscorelibs`, `softioc`, and `cothread` (added to `P_python` in `a9a5d04`), closing #16. Full-species re-apply idempotency verified the same day: a second `species/iocrunner.yml` apply on the same VM ran `failed=0 changed=0` on both OSes, pip reported "Requirement already satisfied", the proxy artifacts were byte-identical with seal `clean=true`, and the installed-tree fingerprint (pip freeze, dpkg/rpm sets, ioc accounts, EPICS path) was identical between runs. The SOT P_proxy definition landed one-to-one at cloud-provision `8654990`. |

#### M5 - Restore the EPICS OS package set into the operator model

- Origin: 25130ef / M5
- GitHub Issue: #18, https://github.com/jeonghanlee/ansible-provision/issues/18
- Status: Complete

##### Summary

The operator rewrite (`724b381`) retired `base_os` and dropped its `pkg_standard`
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
| T1 | 2026-08-31 | rocky8, debian13 | Passed | Distribution: iocrunner golden bakes install the set (`net-snmp-devel` + `libnetsnmp.so` on the fresh VM). Source: `epics_dev` builds and installs EPICS-env clean with `pkg_automation` removed (rocky8 `24c9dc9`, debian13 `0d08692`, recap `failed=0`). |
| T2 | 2026-08-31 | rocky8, debian13 | Passed | `ServiceTestIOC` built with the snmp module links: `-lnetsnmp` resolves against the installed `libnetsnmp.so`; no "cannot find -lnetsnmp" on either OS. |

##### Closure Evidence

- Complete 2026-08-31. Golden pair verified on both acquisition paths; `pkg_automation` retired from `roles/epics_build`. Along the way the rocky8 list gained `cmake`, `re2c`, `patch` and the debian lines `cmake`/`re2c` (source-build tools the old `pkg_standard` seed lacked), and the `epics_build` OS update excludes `kernel*` and `NetworkManager*` to keep the SSH session alive during a source build. The four non-golden vacua carry the same lists and move to `M6`.

#### M6 - Verify EPICS OS build dependencies on the four non-golden vacua

- Origin: 25130ef / M6
- Status: Not started

##### Summary

The EPICS OS build dependencies (`M5`) are declared for all six vacua and installed
by `roles/epics` and `roles/epics_build`. rocky8 and debian13 are verified end to
end; the four non-golden vacua (rocky10, debian12, ubuntu24, ubuntu26) have no
iocrunner golden pipeline, so verify them by Live-mode species apply per vacuum.

##### Scope

For each of rocky10, debian12, ubuntu24, ubuntu26: apply the iocrunner species live
to a fresh proxied VM, confirm the EPICS OS build dependencies install (net-snmp dev
package + `libnetsnmp.so` present) and a sample IOC (`ServiceTestIOC` with the snmp
module) links, then discard the VM.

Out of scope: the cloud-provision iocrunner golden bake-matrix expansion (bake,
publish, consumer boot, validation) for these OSes — a separate cloud-provision
milestone.

##### Completion Criteria

- Each of the four vacua installs `epics_os_packages` on a fresh Live-mode apply.
- A sample IOC links against the installed EPICS environment on each.

##### Dependencies And Decisions

- Origin decision `D6` (2026-08-31): split from `M5` at its close.
- The package lists and role code are already in place (`M5`); names dry-run-verified
  by LAB-cloud on 2026-08-31 (rocky10 needs `P_common`'s EPEL+CRB, which the species
  order provides).

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. LAB-cloud pre-checks package names by dry-run per OS (done 2026-08-31).
2. LAB-cloud applies the iocrunner species Live to a fresh VM per vacuum and checks
   net-snmp evidence + IOC link, then discards the VM.
3. Record per-vacuum verification here.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Live-mode iocrunner species apply, inspect packages + IOC link | rocky10, debian12, ubuntu24, ubuntu26 | `epics_os_packages` install; a sample IOC links against the installed EPICS environment. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | four vacua | Pending | Names dry-run-verified 2026-08-31 (rocky10 32, debian12 43, ubuntu24 40, ubuntu26 40); live apply pending. |

##### Closure Evidence

- Pending.

#### M7 - Harden the epics_build source build against a dropped connection

- Origin: 25130ef / M7
- Status: Not started

##### Summary

`roles/epics_build` runs the whole EPICS-env source build as one long
`ansible.builtin.raw` task over SSH. During `M5` verification (LAB-cloud Finding
B), a dropped SSH connection left the remote shell still running on the VM — the
build kept progressing while ansible reported the task failed — so a failed run
can leave a half-built tree, and a same-VM retry can race the surviving shell or
see partial state. `M5`'s fix (`1c1cabc`, excluding `kernel*`/`NetworkManager*`
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
  B). `M5`'s `1c1cabc` removed the known trigger; this row addresses the
  structure.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. Choose the structure (detached/resumable unit vs clean-on-retry guard).
2. Implement in `roles/epics_build`.
3. Verify with a real source-build run, including a simulated connection drop.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Source build with a mid-build connection drop, then retry | rocky8 or debian13 | No half-built tree survives; the build completes or cleanly resumes with no surviving-shell race. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | golden pair | Pending | — |

##### Closure Evidence

- Pending.

## Backlog

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

No unassigned work in this generation. Unassigned work belongs here; the
release tally above excludes this section.

## History

| Reset Date | Prior State Commit |
| --- | --- |
| 2026-08-17 | 25130eff4adb5b0101d9ce68c4e8e10eef232cb6 |
