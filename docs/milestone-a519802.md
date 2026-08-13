# Work Register

## Scope

This document is the canonical work register for the `master` release line of
`ansible-provision` after the reset carried by prior state commit `a519802`.
It records unfinished deliverables, external gates, accepted plans, and
verification needed to continue the current generation.

**Out of scope:** completed work remains reachable in the prior state commit;
detailed operating procedures remain in the linked runbooks; EtherCAT execution
remains in the owner's separate tracker.

- Release line: master
- Milestone index: a519802
- Canonical path: `docs/milestone-a519802.md`
- Canonical branch or ref: `master`
- Git upstream: `origin/master`
- Remote tracker: `jeonghanlee/ansible-provision`, GitHub milestone `Backlog`

Next session entry point: resume `G1` with the clean current-head bake path.
Recheck the three source refs, use the latest released `epics-ioc-runner` tag
as the Gate-grade baseline (`1.2.3` at this session close), obtain owner
direction before cleaning any running `testbed-debian13-server` domain, then
run the Rocky 8 and Debian 13 bakes and `epics-ioc-runner/gate/RUNBOOK.md`.

Status tally: 1 Complete, 2 Blocked. External gates: 0 Complete, 2 Open.

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env source-build environment | Carry-forward | Blocked | No | G2 | Rocky 8, Debian 13, Rocky 10, Ubuntu 24, and Ubuntu 26 pass the complete source-build matrix; [detail](#m1---epics-env-source-build-environment) |
| Release | M2 | Version 1.0 release convention | Carry-forward | Blocked | No | G1 | Consumer release gate, matching tags, and the next version-scoped register are complete; [detail](#m2---version-10-release-convention) |
| Docs | M3 | epics-ioc-runner runbook reference repair | Carry-forward | Complete | No | | All three repository references name `epics-ioc-runner/gate/RUNBOOK.md`; [detail](#m3---epics-ioc-runner-runbook-reference-repair) |
| Gates | G1 | Owner-selected consumer release-gate bake and release authorization | External gate | Open | No | | Owner selects the release-gate bake and authorizes the matching tag sequence; [detail](#g1---owner-selected-consumer-release-gate-bake-and-release-authorization) |
| Gates | G2 | Ubuntu 26 `iocStats` compatibility with GCC 15 | External gate | Open | No | | A compatible `iocStats` revision or correction is selected and the complete Ubuntu 26 path passes; [detail](#g2---ubuntu-26-iocstats-compatibility-with-gcc-15) |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D1 | Local `T` labels identify verification inside their owning work detail and are not independent work IDs. | Prior canonical register, prior state commit `a519802` |
| D2 | Use bare-number release tags jointly with `cloud-provision` at an accepted consumer release gate. | Prior canonical register, U8, 2026-07-03 |

### Milestone Details

#### M1 - EPICS-env Source-Build Environment

- Origin: a519802 / M1
- Identity History: new reset-generation identity; prior scope and evidence are reachable from commit `a519802`
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

- `G2` is Open; resume as `In progress` after the Ubuntu 26 compatibility condition is complete.
- `D1` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: accepted plan preserved from prior state commit `a519802`
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
| T5 | Matrix | Build configured source-build hosts | Rocky 10, Ubuntu 24, Ubuntu 26 | Rocky 10 and Ubuntu 24 pass; Ubuntu 26 passes after `G2`. |
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

- `M1` remains Blocked by `G2`. GitHub #7 is open; its live state was observed on 2026-08-06.

##### GitHub Projection

- Title: `EPICS-env source-build verification matrix`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-06; GitHub updated 2026-07-29T00:20:45Z

#### M2 - Version 1.0 Release Convention

- Origin: a519802 / M2
- Identity History: new reset-generation identity; prior scope and evidence are reachable from commit `a519802`
- GitHub Issue: none
- Status: Blocked

##### Summary

The first repository-family 1.0 release is cut from an accepted consumer
release-gate bake, followed by a fresh version-scoped register.

##### Scope

Satisfy the agreed scope, run the consumer release gate, create matching
bare-number tags, and preserve the released register.

Out of scope: selecting or executing the release sequence without owner authorization.

##### Completion Criteria

- `G1` is Complete.
- The consumer release gate passes, matching tags are created, and the next register is opened.

##### Dependencies And Decisions

- `G1` is Open; resume as `In progress` after owner release authorization.
- `D2` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: accepted release convention preserved from prior state commit `a519802`
- Implementation Authorization: none for the release sequence; owner authorization is required
- Superseded Plan Artifacts: none

1. Select and pass the consumer release-gate bake.
2. Execute the matching tag sequence only after owner authorization.
3. Preserve the released register and open the next version-scoped register.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Scope | Confirm agreed 1.0 scope A, B1, B2, C1, and C3 | Repository and consumer project | Scope is satisfied. |
| T2 | Release gate | Run the consumer release-gate bake | Consumer environment | Bake passes. |
| T3 | Release execution | Create matching bare-number tags | Repository family | Tags match across repositories. |
| T4 | Release documentation | Preserve released register and open next register | Repository | New version-scoped register is available. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-03 | Repository and consumer project | Passed | Agreed scope recorded in prior state commit `a519802` |
| T2 | Not run | Consumer environment | Pending | Requires `G1` |
| T3 | Not run | Repository family | Pending | Requires `G1` and owner authorization |
| T4 | Not run | Repository | Pending | Follows T3 |

##### Closure Evidence

- `M2` is Blocked by open `G1`. No release mutation is authorized in this reset generation.

#### M3 - epics-ioc-runner Runbook Reference Repair

- Origin: a519802 / M3
- Identity History: added to the current generation from GitHub issue #11 after the 2026-08-12 code comparison
- GitHub Issue: #11, https://github.com/jeonghanlee/ansible-provision/issues/11
- Status: Complete

##### Summary

The repository references the consumer runbook at its current `gate/RUNBOOK.md` path.

##### Scope

Update the three references in `docs/test_users_handoff.md`, `roles/test_users/tasks/main.yml`, and `roles/test_users/defaults/main.yml`.

Out of scope: `test_users` role behavior and automatic verification of the external consumer repository path.

##### Completion Criteria

- No tracked ansible-provision file names the stale consumer runbook path.
- The three affected files reference `epics-ioc-runner/gate/RUNBOOK.md` or its local `gate/RUNBOOK.md` suffix.

##### Dependencies And Decisions

- No M or G dependencies.
- The consumer path and source commit `6b009b4` are recorded by GitHub issue #11.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner selected option 1 in chat, 2026-08-12
- Implementation Authorization: owner selected option 1 in chat, 2026-08-12
- Superseded Plan Artifacts: none

1. Replace the stale consumer runbook path in the handoff document and the two role comments.
2. Scan the repository for the old path and confirm the three intended new references.
3. Run the affected playbook syntax check and `git diff --check`.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Documentation | Scan tracked repository files for the old and new paths | ansible-provision | The old path is absent and three intended new references are present. |
| T2 | Syntax | Run `ansible-playbook --syntax-check playbooks/07_test_users.yml` | Local environment | The playbook exits with status 0. |
| T3 | Integrity | Run `git diff --check` | Repository | No whitespace errors are reported. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-12 | ansible-provision | Passed | The old path scan returned no matches; the new path scan returned three intended references. |
| T2 | 2026-08-12 | Local environment | Passed | `ANSIBLE_LOCAL_TEMP=/tmp/ansible-provision-local-tmp ansible-playbook --syntax-check playbooks/07_test_users.yml` exited 0. |
| T3 | 2026-08-12 | Repository | Passed | `git diff --check` exited 0. |

##### Closure Evidence

- The three local references are corrected and the affected playbook passes syntax validation.
- GitHub #11 remains open; no GitHub mutation was authorized in this scope.

##### GitHub Projection

- Title: `Repoint the three epics-ioc-runner runbook references after the file moved to gate/RUNBOOK.md`
- Labels: `documentation`
- GitHub Milestone: `Backlog`
- Observed State: open
- Observed Labels: `documentation`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-12; GitHub updated 2026-08-01T20:34:58Z

#### G1 - Owner-Selected Consumer Release-Gate Bake and Release Authorization

- Origin: a519802 / G1
- GitHub Issue: none
- Status: Open

##### Summary

The first release gate and matching tag sequence require owner selection and
authorization.

##### Concrete Meaning

`G1` is the decision record for one specific `epics-ioc-runner` consumer
release gate. The release-gate bake is the fresh-image acceptance run in which
`cloud-provision` produces the `rocky8-iocrunner` and `debian13-iocrunner`
variants, `ansible-provision` supplies the configured image contents, and the
consumer release-gate checks run against fresh consumers.

`G1` is not branch creation, tag creation, or release-register creation. It
records which accepted bake is the Version 1.0 release basis and authorizes
`M2` to execute the matching tag sequence.

##### Required Decision Record

| Field | Required content |
| --- | --- |
| Selected bake | Bake date, variant names, image identities, and sidecar identities |
| Source refs | `ansible-provision`, `cloud-provision`, EPICS-env, and consumer refs used by the bake |
| Consumer evidence | Fresh-consumer release-gate result, including the consumer suite and `validate_iocrunner_bake.bash` result |
| Release point | The exact repository-family release point and matching bare-number tag sequence to be authorized |
| Authorization | Owner authorization for the selected bake and the matching tag sequence |

##### Completion Criteria

- The required decision record identifies one selected consumer release-gate bake.
- Fresh consumers from the selected bake pass the consumer release-gate checks.
- The owner authorization for the selected bake and matching tag sequence is recorded.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-08-06 | Pending | No selected G1 bake record or owner release authorization is recorded. |

##### Closure Evidence

- Gate remains Open and blocks `M2`.

#### G2 - Ubuntu 26 IOCStats Compatibility With GCC 15

- Origin: a519802 / G2
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
| Gates | G3 | Owner decision on Ansible SSH master reuse | External gate | Open | No | | Owner selects a mitigation path or records a Keep verdict with evidence; [detail](#g3---owner-decision-on-ansible-ssh-master-reuse) |

Unassigned work belongs here; the release tally above excludes this section.

### Backlog Details

#### G3 - Owner Decision on Ansible SSH Master Reuse

- Origin: a519802 / G3
- Identity History: added to the current generation from GitHub issue #10 after the 2026-08-12 code comparison
- GitHub Issue: #10, https://github.com/jeonghanlee/ansible-provision/issues/10
- Status: Open

##### Summary

Ansible's default SSH multiplexing can retain a control master keyed by a reused testbed address after a VM is destroyed and recreated.

##### Scope

Run a real testbed recreate check, then either select a configuration mitigation or record an owner-approved Keep verdict.

Out of scope: `cloud-provision`, where the related operator SSH path is already handled, and the operator's own `~/.ssh/config`.

##### Completion Criteria

- The real destroy-and-recreate path is observed.
- If stale-master behavior is observed, an authorized mitigation prevents the recreated host from inheriting the stale socket and the real Ansible path passes.
- If the behavior is not observed or the exposure is accepted, the owner decision and reasoning are recorded in `docs/CLOSED_DOORS.md`.

##### Dependencies And Decisions

- Owner decision is required before changing `ansible.cfg` SSH behavior.
- No D reference is required until the owner selects a Keep verdict.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner selected option 1 in chat, 2026-08-12
- Implementation Authorization: none for SSH configuration changes in this scope
- Superseded Plan Artifacts: none

1. Recreate a testbed VM at a reused address and run the real Ansible connection path.
2. Record whether a stale control master affects the new VM.
3. Apply an owner-selected mitigation or record the Keep verdict and its evidence.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Destroy and recreate a testbed VM at the same address, then run the affected Ansible path | Testbed VM | The connection either passes without stale-master behavior or produces observed evidence for the selected mitigation. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-12 | Local repository | Pending | The current `ansible.cfg` has no `[ssh_connection]` section; the real recreate test has not run. |

##### Closure Evidence

- Gate remains Open. The selected option 1 scope intentionally leaves SSH configuration unchanged pending the real recreate check and owner decision.

##### GitHub Projection

- Title: `Ansible reuses an SSH master keyed on a reused address`
- Labels: `bug`
- GitHub Milestone: `Backlog`
- Observed State: open
- Observed Labels: `bug`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-12; GitHub updated 2026-08-01T06:52:38Z

## History

| Reset Date | Prior State Commit |
| --- | --- |
| 2026-08-06 | a51980286459dde442e7aa59ed11d2e5b46201cd |
