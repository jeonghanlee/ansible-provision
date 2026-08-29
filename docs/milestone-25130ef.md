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

The next EPICS-env verification is the 1.3.0 gate, whose OS matrix excludes
Ubuntu 26; Ubuntu 26 source-build is therefore deferred to EPICS-env 1.3.1 or a
later version (see `M2` and `D2`).

- Release line: master
- Milestone index: 25130ef
- Canonical path: `docs/milestone-25130ef.md`
- Canonical branch or ref: `master`
- Git upstream: `origin/master`
- Remote tracker: `jeonghanlee/ansible-provision`, GitHub milestone `Backlog`

Next session entry point: `M4` (operator/species provisioning model), the active
milestone. `M4/T1` — syntax-check the species playbooks and confirm
`configure/RELEASE` and `inventory/lab.ini` enumerate them — is runnable now;
`M4/T3` applies `operators/proxy.yml` on a proxied host; `M4/T2` (iocserver on
the production IOC server) is blocked on `G1`. `M3` (base_os/app role hardening) is Deferred per
`D3`: the old model is retired, so its Debian 13 re-verification is not pursued.
`M1` (4-OS source-build) is Complete; `M2` (Ubuntu 26 source-build) is Deferred
to EPICS-env 1.3.1 or later (`jeonghanlee/EPICS-env#63`; C17 bridge at
`jeonghanlee/EPICS-env#29`).

Status tally: 1 Complete, 1 In progress, 2 Deferred. 1 external gate (Open).

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env 4-OS source-build environment | Carry-forward | Complete | No | | Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass both source-build layers and checks; [detail](#m1---epics-env-4-os-source-build-environment) |
| Core | M2 | Ubuntu 26 source-build (deferred) | Carry-forward | Deferred | No | D2 | Owner adds Ubuntu 26 back to the matrix in EPICS-env 1.3.1 or later and the complete Ubuntu 26 path passes; [detail](#m2---ubuntu-26-source-build-deferred) |
| Core | M3 | base_os/app role hardening from the production IOC server deployment | Carry-forward | Deferred | No | D3 | Deferred per D3 (old model retired); the base/app surface is re-verified under the operator model (M4); [detail](#m3---base_osapp-role-hardening-from-the production IOC server-deployment) |
| Core | M4 | Operator/species provisioning model | Milestone | In progress | No | G1 | Vacua, single-role operators, and species assemblies replace the staged model, iocserver registered; P_proxy role implemented with live apply pending and the live iocserver run blocked on G1; [detail](#m4---operatorspecies-provisioning-model) |
| Gate | G1 | the production IOC server added to the the internal git host clone whitelist | External gate | Open | No | | Network team whitelists the production IOC server so the EPICS distribution clone and a live iocserver run reach the internal git host; blocks M4/T2 |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D1 | Local `T` labels identify verification inside their owning work detail and are not independent work IDs. | Prior canonical register, prior state commit `25130ef` |
| D2 | Ubuntu 26 is excluded from the current source-build matrix and deferred to EPICS-env 1.3.1 or a later version. The 1.3.0 gate matrix does not include Ubuntu 26, and the `iocStats` GCC 15 fix is owned by EPICS-env. | Owner decision, 2026-08-17 |
| D3 | The staged old model (`01_base`/`02_apps`/`03_epics`) and its retained roles `base_os` and `app_epics` are retired; the operator/species model supersedes them. Removing the old roles and playbooks is separate follow-up work. | Owner decision, 2026-08-29 |

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

#### M2 - Ubuntu 26 Source-Build (Deferred)

- Origin: 25130ef / M2
- Identity History: split from `M1` on 2026-08-17 by owner decision `D2`; carries the former Ubuntu 26 gate scope (prior generation `G2`).
- GitHub Issue: #7, https://github.com/jeonghanlee/ansible-provision/issues/7. EPICS-env 1.3.1+ backlog: `jeonghanlee/EPICS-env#63`, https://github.com/jeonghanlee/EPICS-env/issues/63
- Status: Deferred

##### Summary

Ubuntu 26 source-build is deferred. The build fails only on Ubuntu 26 because
GCC 15 defaults to C23, which breaks the `iocStats` `devIocStatsAnalog.c`
`DEVSUPFUN`/`DSET` initializers.

##### Scope

Add Ubuntu 26 back to the source-build matrix and pass the complete Ubuntu 26
path once EPICS-env 1.3.1 or a later version covers it.

Out of scope: the `iocStats` GCC 15 fix itself, which EPICS-env owns.

##### Completion Criteria

- EPICS-env 1.3.1 or later covers Ubuntu 26, and the complete Ubuntu 26
  source-build path (both layers, `gz` flavor, repeated-run checks) passes.

##### Dependencies And Decisions

- `D2` defers this row (owner decision, 2026-08-17). It is not Ready while
  Deferred and returns to `Not started` only by owner decision when EPICS-env
  1.3.1+ covers Ubuntu 26.
- Resolution mechanism owned by EPICS-env: the C17 bridge in
  `jeonghanlee/EPICS-env#29` (closed). `configure/RULES_MODS_CONFIG` adds
  `$(SRC_PATH_IOCSTATS)` to `MODS_C17_SRC_PATHS`, so `conf.modules.c17` writes
  `USR_CFLAGS += -std=gnu17` into the module's `CONFIG_SITE.local`; both the
  internal (`conf.modules`) and public (`conf.gz.modules`) paths depend on it.

##### Implementation Plan

- Plan Status: draft
- Plan Acceptance: none
- Implementation Authorization: none
- Superseded Plan Artifacts: none

1. When EPICS-env 1.3.1+ covers Ubuntu 26, re-add Ubuntu 26 to the source-build
   matrix and rerun the complete path.
2. Before treating the bridge as a source/version problem, confirm it fired:
   check the Ubuntu 26 build tree's `iocStats/configure/CONFIG_SITE.local` for
   `-std=gnu17`. The prior failure may have been the `MODS_C17_BRIDGE`
   OS/compiler detection not firing rather than a missing fix.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Matrix | Build the complete source-build path with EPICS-env 1.3.1+ | Ubuntu 26 | Both layers, the `gz` flavor, and dependency/idempotency checks pass. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Ubuntu 26 | Deferred | Prior run exited 2 in `iocStats` `devIocStatsAnalog.c` under GCC 15; deferred to EPICS-env 1.3.1+ per `D2`. |

##### Closure Evidence

- Deferred by owner decision `D2` (2026-08-17): Ubuntu 26 is out of the 1.3.0
  gate matrix and re-added in EPICS-env 1.3.1 or later. The `iocStats` GCC 15
  mechanism already exists in EPICS-env (`#29`, C17 bridge). EPICS-env filed the
  1.3.1+ backlog issue `jeonghanlee/EPICS-env#63` ("Ensure the C17 bridge fires
  for iocStats on Ubuntu 26 GCC 15 in the source-build path"), whose body
  cross-references `ansible-provision#7`.

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

Implemented, live verification pending:

- P_proxy: an optional precondition operator that applies the site proxy
  contract to an existing server by streaming cloud-provision
  `bin/proxy_contract.bash` in apply mode, so the logic is not duplicated.
  Design converged with the cloud-provision owner (ADR-20260820); `roles/proxy`
  and `playbooks/operators/proxy.yml` are implemented (stage the shipped script
  plus a schema-1 input, then run apply as root). A live apply on a proxied
  host is the remaining T3 verification.

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
| T1 | Partial | debian12 (epics_dev) | Species playbooks and registration landed (`92f04c4`, `08ec916`, `60d2c2c`). Live partial evidence: after `35f00fe`, `epics_dev` applied on a real debian12 host (PLAY RECAP `ok=15 changed=4 failed=0`), installing EPICS-env 1.3.0 / base 7.0.10 layers 1+2 at `/opt/epics/1.3.0/debian-12/7.0.10`, observed by the cloud-provision session. A full syntax and enumeration pass across every species is still pending. |
| T2 | Blocked | Rocky 8 (the production IOC server) | Blocked by `G1`: the production IOC server cannot reach the internal git host for the EPICS distribution clone. |
| T3 | Not run | Debian / Rocky | `roles/proxy` and `operators/proxy.yml` implemented (consume the shipped `proxy_contract.bash` in apply mode, no reimplementation). A live apply on a proxied host (the production IOC server) is pending. |

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
