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

Next session entry point: no active blocked work in this generation. `M1`
(4-OS source-build) is Complete; `M2` (Ubuntu 26 source-build) is Deferred to
EPICS-env 1.3.1 or later, tracked at `jeonghanlee/EPICS-env#63`; the resolving
mechanism (the C17 bridge) already exists in EPICS-env at
`jeonghanlee/EPICS-env#29`.

Status tally: 1 Complete, 1 Deferred. No external gates.

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env 4-OS source-build environment | Carry-forward | Complete | No | | Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass both source-build layers and checks; [detail](#m1---epics-env-4-os-source-build-environment) |
| Core | M2 | Ubuntu 26 source-build (deferred) | Carry-forward | Deferred | No | D2 | Owner adds Ubuntu 26 back to the matrix in EPICS-env 1.3.1 or later and the complete Ubuntu 26 path passes; [detail](#m2---ubuntu-26-source-build-deferred) |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D1 | Local `T` labels identify verification inside their owning work detail and are not independent work IDs. | Prior canonical register, prior state commit `25130ef` |
| D2 | Ubuntu 26 is excluded from the current source-build matrix and deferred to EPICS-env 1.3.1 or a later version. The 1.3.0 gate matrix does not include Ubuntu 26, and the `iocStats` GCC 15 fix is owned by EPICS-env. | Owner decision, 2026-08-17 |

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
