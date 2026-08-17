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

- Release line: master
- Milestone index: 25130ef
- Canonical path: `docs/milestone-25130ef.md`
- Canonical branch or ref: `master`
- Git upstream: `origin/master`
- Remote tracker: `jeonghanlee/ansible-provision`, GitHub milestone `Backlog`

Next session entry point: resume `G1` — select or implement a GCC 15 compatible
`iocStats` revision for Ubuntu 26. When `G1` is Complete, `M1` restores
`In progress` and reruns the complete Ubuntu 26 source-build path with the `gz`
flavor and repeated-run checks.

Status tally: 0 Complete, 1 Blocked. External gates: 0 Complete, 1 Open.

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env source-build environment | Carry-forward | Blocked | No | G1 | Rocky 8, Debian 13, Rocky 10, Ubuntu 24, and Ubuntu 26 pass the complete source-build matrix; [detail](#m1---epics-env-source-build-environment) |
| Gates | G1 | Ubuntu 26 `iocStats` compatibility with GCC 15 | External gate | Open | No | | A compatible `iocStats` revision or correction is selected and the complete Ubuntu 26 path passes; [detail](#g1---ubuntu-26-iocstats-compatibility-with-gcc-15) |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D1 | Local `T` labels identify verification inside their owning work detail and are not independent work IDs. | Prior canonical register, prior state commit `25130ef` |

### Milestone Details

#### M1 - EPICS-env Source-Build Environment

- Origin: 25130ef / M1
- Identity History: new reset-generation identity; prior scope and evidence are reachable from commit `25130ef`
- GitHub Issue: #7, https://github.com/jeonghanlee/ansible-provision/issues/7
- Status: Blocked

##### Summary

Dedicated build hosts compile EPICS-env and EPICS-env-support from source,
install vendor libraries into the release tree, and validate the installed
runtime without changing `site.yml`.

##### Scope

Run the source-build layers on Rocky 8, Debian 13, Rocky 10, Ubuntu 24, and
Ubuntu 26, including the `gz` flavor and repeated-run checks.

Out of scope: binary-distribution deployment and golden-image baking for these
source-build hosts.

##### Completion Criteria

- Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass both source-build layers and checks.
- Ubuntu 26 passes both layers and all runtime checks after the GCC 15 compatibility condition is resolved.
- Vendor libraries have no retained absolute-path dependency findings.

##### Dependencies And Decisions

- `G1` is Open; resume as `In progress` after the Ubuntu 26 compatibility condition is complete.
- `D1` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: accepted plan preserved from prior state commit `25130ef`
- Implementation Authorization: prior owner-authorized implementation plan and verification evidence
- Superseded Plan Artifacts: none

1. Build the base and support layers on the supported source-build matrix.
2. Keep vendor libraries inside the release tree and run dependency checks.
3. Select or implement an `iocStats` compatibility correction for Ubuntu 26 and rerun the complete path.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Build and re-run the current EPICS-env path | Rocky 8 | Base and support layers pass; rerun is idempotent. |
| T2 | Integration | Build and re-run the current EPICS-env path | Debian 13 | Layered tree and dependency checks pass. |
| T3 | Integration | Build vendor libraries inside the release tree | Debian 13 | No absolute-path dependency findings remain. |
| T4 | Integration | Build the EPICS-env-support layer | Debian 13 | Support layer and checks pass. |
| T5 | Matrix | Build configured source-build hosts | Rocky 10, Ubuntu 24, Ubuntu 26 | Rocky 10 and Ubuntu 24 pass; Ubuntu 26 passes after `G1`. |
| T6 | Integration | Build the `gz` flavor through both source-build roles | Rocky 10 and Ubuntu 24 | Installed flags and dependency checks pass. |
| T7 | Idempotency | Re-run the support role | Rocky 8 | Installed-tree skip is observed with `changed=0` and `failed=0`. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-28 | Rocky 8 | Passed | Fresh layers, `changed=0`, and `check_deps.bash` passed |
| T2 | 2026-07-28 | Debian 13 | Passed | Commits `5c4f7fc` and `0148514` |
| T3 | 2026-07-28 | Debian 13 | Passed | Commit `5c4f7fc`, absolute paths reduced from 9 to 0 |
| T4 | 2026-07-28 | Debian 13 | Passed | Commit `0148514` |
| T5 | 2026-07-28 | Rocky 10, Ubuntu 24, Ubuntu 26 | Partial | Rocky 10 and Ubuntu 24 passed; Ubuntu 26 layer 1 exited 2 in `iocStats` under GCC 15 |
| T6 | 2026-07-28 | Rocky 10 and Ubuntu 24 | Passed | `-g0 -gz=zlib` and `check_deps.bash` passed |
| T7 | 2026-07-28 | Rocky 8 | Passed | `EPICS_ENV_SUPPORT_BUILD_SKIPPED`, `changed=0`, `failed=0` |

##### Closure Evidence

- `M1` remains Blocked by `G1`. GitHub #7 is open; its live state was observed on 2026-08-16.

##### GitHub Projection

- Title: `EPICS-env source-build verification matrix`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-16; GitHub updated 2026-08-16T08:33:22Z

#### G1 - Ubuntu 26 IOCStats Compatibility With GCC 15

- Origin: 25130ef / G1
- GitHub Issue: #7, https://github.com/jeonghanlee/ansible-provision/issues/7
- Status: Open

##### Summary

Ubuntu 26 source-build verification is waiting for an `iocStats` compatibility
correction that supports GCC 15.

##### Completion Criteria

- A selected compatible `iocStats` revision or correction builds the first layer.
- The support layer and all remaining Ubuntu 26 checks pass.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-08-06 | Open | Prior run exited 2 in `iocStats` `devIocStatsAnalog.c`; GitHub #7 remains open. |

##### Closure Evidence

- Gate remains Open and blocks `M1`.

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
