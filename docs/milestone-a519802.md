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

Next session entry point: `G1` is decided — the `iocrunner-gate-1.0.0` release
basis is the 2026-08-17 Gate-grade bake (baseline `epics-ioc-runner` `1.2.3`,
all gate steps passed on both goldens). The next release action is `M2`: cut the
joint `iocrunner-gate-1.0.0` annotated tag on `cloud-provision` (`2b77a97`) and
`ansible-provision` (`3981c21`) under a release delegation, then open the next
version-scoped register. `M1` stays blocked on `G2` (Ubuntu 26 `iocStats` under
GCC 15). The 2026-08-17 fresh consumers at `192.168.122.150` and
`192.168.122.50` are still up for any release verification.

Status tally: 4 Complete, 1 In progress, 1 Blocked. External gates: 1 Complete, 1 Open.

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M1 | EPICS-env source-build environment | Carry-forward | Blocked | No | G2 | Rocky 8, Debian 13, Rocky 10, Ubuntu 24, and Ubuntu 26 pass the complete source-build matrix; [detail](#m1---epics-env-source-build-environment) |
| Release | M2 | Version 1.0 release convention | Carry-forward | In progress | No | G1 | Consumer release gate, matching tags, and the next version-scoped register are complete; [detail](#m2---version-10-release-convention) |
| Docs | M3 | epics-ioc-runner runbook reference repair | Carry-forward | Complete | No | | All three repository references name `epics-ioc-runner/gate/RUNBOOK.md`; [detail](#m3---epics-ioc-runner-runbook-reference-repair) |
| Runtime | M4 | Generated Ansible host inventory contract | Milestone | Complete | No | | Generated runtime inventories and site-owned complete inventories both pass the shipped Make contract; [detail](#m4---generated-ansible-host-inventory-contract) |
| Runtime | M5 | Configured IOC runner installation destination | Milestone | Complete | No | | The real role installs and verifies the default and alternate destinations on Debian 13 and Rocky 8; [detail](#m5---configured-ioc-runner-installation-destination) |
| Runtime | M6 | IOC runner CLI resolution at a non-default destination | Milestone | Complete | No | | The role's post-install verification resolves ioc-runner at a non-default `path_ioc_runner_bin` without relying on PATH; [detail](#m6---ioc-runner-cli-resolution-at-a-non-default-destination) |
| Gates | G1 | Owner-selected consumer release-gate bake and release authorization | External gate | Complete | No | | Owner selected the 2026-08-17 Gate-grade bake and the `iocrunner-gate-1.0.0` tag name as the Version 1.0 basis; [detail](#g1---owner-selected-consumer-release-gate-bake-and-release-authorization) |
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

- `M1` remains Blocked by `G2`. GitHub #7 is open; its live state was observed on 2026-08-16.

##### GitHub Projection

- Title: `EPICS-env source-build verification matrix`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-16; GitHub updated 2026-08-16T08:33:22Z

#### M2 - Version 1.0 Release Convention

- Origin: a519802 / M2
- Identity History: new reset-generation identity; prior scope and evidence are reachable from commit `a519802`
- GitHub Issue: none
- Status: In progress

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

- `G1` is Complete (2026-08-17); `M2` resumed `In progress` to execute the `iocrunner-gate-1.0.0` tag sequence under a release delegation.
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
- GitHub #11 is closed; its live state was observed on 2026-08-16.

##### GitHub Projection

- Title: `Repoint the three epics-ioc-runner runbook references after the file moved to gate/RUNBOOK.md`
- Labels: `documentation`
- GitHub Milestone: `Backlog`
- Observed State: closed
- Observed Labels: `documentation`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-16; GitHub updated 2026-08-16T08:33:30Z

#### M4 - Generated Ansible Host Inventory Contract

- Origin: a519802 / M4
- Identity History: added to the current generation from shipped commit `50925d4` after the 2026-08-16 code comparison
- GitHub Issue: none
- Status: Complete

##### Summary

The stable inventory owns group relationships while callers supply resolved
host identities through a generated runtime inventory or a site-owned complete
inventory.

##### Scope

Keep `inventory/testbed.ini` free of host identities, require
`RUNTIME_INVENTORY` when that group inventory is used, preserve arbitrary host
selection, and continue supporting a complete inventory selected through
`INVENTORY`.

Out of scope: generating runtime inventory content, changing VM identity, and
changing site-owned inventory files.

##### Completion Criteria

- `inventory/testbed.ini` contains stable group relationships and no host entries.
- Make refuses the default group inventory when `RUNTIME_INVENTORY` is absent.
- A generated inventory and arbitrary `ANSIBLE_LIMIT` reach the requested Make target.
- A site-owned complete inventory remains supported without `RUNTIME_INVENTORY`.

##### Dependencies And Decisions

- No M, G, or D dependencies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner directed reconciliation from shipped code on 2026-08-16
- Implementation Authorization: implementation is carried by owner-authored commit `50925d4`
- Superseded Plan Artifacts: none

1. Remove fixed host entries from the stable group inventory.
2. Add the generated runtime inventory to the Make command path and reject a missing source.
3. Preserve explicit site-owned complete inventories and verify both paths through the shipped Make target.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Contract | Run the shipped Make check without `RUNTIME_INVENTORY` | Local Make path | The default group inventory is rejected. |
| T2 | Integration | Run the shipped Make check with a generated inventory and arbitrary host limit | Local Make path | The requested host reaches the generated Make target. |
| T3 | Compatibility | Run the shipped Make check with a complete inventory through `INVENTORY` | Local Make path | The complete inventory remains supported. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-16 | Local Make path | Passed | `make check-runtime-inventory-contract`; missing generated source was rejected. |
| T2 | 2026-08-16 | Local Make path | Passed | `make check-runtime-inventory-contract`; generated inventory and arbitrary host limit reached the target. |
| T3 | 2026-08-16 | Local Make path | Passed | `make check-runtime-inventory-contract`; site-owned complete inventory remained supported. |

##### Closure Evidence

- Commit `50925d4` carries the runtime inventory contract, documentation, and shipped check.
- The shipped check passed 3 of 3 on 2026-08-16 against the current committed tree.

#### M5 - Configured IOC Runner Installation Destination

- Origin: a519802 / M5
- Identity History: added to the current generation from GitHub issue #13 after the 2026-08-16 code comparison; assigned from Backlog to Milestone on completion (see Assignment History)
- GitHub Issue: #13, https://github.com/jeonghanlee/ansible-provision/issues/13
- Status: Complete

##### Summary

The `app_ioc_runner` role passes the configured `path_ioc_runner_bin` to the
shipped setup path as `IOC_RUNNER_SCRIPT_DEST` and ensures the destination parent
directory exists, so the runner installs and verifies at the configured
destination rather than only the default.

##### Scope

Pass `path_ioc_runner_bin` to `setup-system-infra.bash --full` as
`IOC_RUNNER_SCRIPT_DEST`, create the destination parent directory before the
setup call, and preserve the default destination and the installed identity
check.

Out of scope: consumer lifecycle-suite selection, source-mode behavior,
`epics-ioc-runner/gate/RUNBOOK.md`, setup deployment semantics, and
`cloud-provision` validation behavior. Those consumer changes belong to
`jeonghanlee/epics-ioc-runner#145`. Setup-side parent-directory robustness is
filed as `jeonghanlee/epics-ioc-runner#147`.

##### Completion Criteria

- With the default inventory value, the real role installs or retains `/usr/local/bin/ioc-runner` and verifies its `-V` identity on Debian 13 and Rocky 8.
- With an alternate absolute `path_ioc_runner_bin`, the real role runs the shipped setup path, installs at that exact destination, and verifies its `-V` identity on Debian 13 and Rocky 8.
- No staged or hand-copied executable substitutes for the shipped setup path during verification.

##### Dependencies And Decisions

- No M, G, or D dependencies block the local implementation.
- `jeonghanlee/epics-ioc-runner#145` owns downstream consumer selection and lifecycle verification.
- `jeonghanlee/epics-ioc-runner#147` tracks the optional setup-side parent-directory robustness follow-up.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner selected the plan in chat, 2026-08-16
- Implementation Authorization: owner authorized implementation in chat, 2026-08-16
- Superseded Plan Artifacts: none

1. Export the resolved `path_ioc_runner_bin` as `IOC_RUNNER_SCRIPT_DEST` for the shipped setup invocation.
2. Create the destination parent directory with `install -d "$(dirname "${bin}")"` before invoking setup.
3. Preserve the default inventory value and the existing installed identity check.
4. Run the real role with the default and alternate destinations on Debian 13 and Rocky 8.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Run the real `app_ioc_runner` role with the default destination | Debian 13 and Rocky 8 | The role installs or retains `/usr/local/bin/ioc-runner`, and its real `-V` identity matches the retained checkout. |
| T2 | Integration | Run the real `app_ioc_runner` role with an alternate absolute destination | Debian 13 and Rocky 8 | The shipped setup installs at the configured path, and the role verifies the real `-V` identity there. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-16 | Debian 13 and Rocky 8 | Passed | Real role at tag `1.2.3` (`4868a25`); `/usr/local/bin/ioc-runner -V` reports `1.2.3 (4868a25)` on both. |
| T2 | 2026-08-16 | Debian 13 and Rocky 8 | Passed | Real role with `path_ioc_runner_bin=/opt/tools/bin/ioc-runner`; the shipped setup installs there and `-V` reports `1.2.3 (4868a25)` on both. |

##### Closure Evidence

- `roles/app_ioc_runner/tasks/main.yml` passes `IOC_RUNNER_SCRIPT_DEST="${bin}"` and runs `install -d "$(dirname "${bin}")"` before the shipped setup call.
- The real role path is verified on Debian 13 and Rocky 8 at tag `1.2.3`; the default and alternate destinations both install and verify their `-V` identity.
- T2 first surfaced a setup-side gap (missing destination parent directory), handled caller-side here and filed as `jeonghanlee/epics-ioc-runner#147` for setup robustness.

##### GitHub Projection

- Title: `Pass path_ioc_runner_bin to setup-system-infra.bash as IOC_RUNNER_SCRIPT_DEST`
- Labels: `bug`
- GitHub Milestone: `Backlog`
- Observed State: closed
- Observed Labels: `bug`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-16; GitHub updated 2026-08-16T16:29:09Z

#### M6 - IOC Runner CLI Resolution at a Non-Default Destination

- Origin: a519802 / M6
- Identity History: added to the current generation from the M5 third-person review on 2026-08-16; assigned from Backlog to Milestone on completion (see Assignment History)
- GitHub Issue: #14, https://github.com/jeonghanlee/ansible-provision/issues/14
- Status: Complete

##### Summary

The `app_ioc_runner` role's final "Verify ioc-runner command" step now resolves
the ioc-runner CLI at the configured `path_ioc_runner_bin` instead of the bare
`ioc-runner`, so post-install verification succeeds at a non-default destination
that is not on PATH.

##### Scope

Make the role's post-install verification resolve the ioc-runner CLI at the
configured destination for a non-default `path_ioc_runner_bin` by invoking
`${bin}` directly.

Out of scope: the shipped setup's own symlink policy, which belongs to
`epics-ioc-runner`. M5 already verifies the configured destination through the
`${bin}` identity check; this item covers only the bare-command verification
step.

##### Completion Criteria

- With a non-default `path_ioc_runner_bin` outside PATH and no prior default install present, the role's post-install verification passes on Debian 13 and Rocky 8.

##### Dependencies And Decisions

- No M, G, or D dependencies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner accepted the plan in chat, 2026-08-17
- Implementation Authorization: owner authorized implementation in chat, 2026-08-17
- Superseded Plan Artifacts: none

1. Resolve the ioc-runner CLI at `${bin}` in the role's post-install verification instead of the bare command.
2. Run the real role with a non-default destination outside PATH, with no prior default install, on Debian 13 and Rocky 8.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Run the real role with a non-default `path_ioc_runner_bin` outside PATH on a host with no prior default install | Debian 13 and Rocky 8 | The post-install verification resolves and passes at the configured destination. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-17 | Debian 13 | Passed | Clean host (no default, no `/usr/bin` symlink): before the fix the verify step failed with `ioc-runner: not found` (rc 127); after the fix it passes and `/opt/tools/bin/ioc-runner -V` reports `1.2.3` (`4868a25`). |
| T1 | 2026-08-17 | Rocky 8 | Passed | Clean host: the fix passes; the shipped setup creates `/usr/bin/ioc-runner -> /opt/tools/bin/ioc-runner` (RHEL only), so the bare-command gap does not arise here and the fix is harmless. |

##### Closure Evidence

- `roles/app_ioc_runner/tasks/main.yml` "Verify ioc-runner command" resolves `${bin}` (= `path_ioc_runner_bin`) for `-V`, `list -vv`, and `inspect -h`; no bare `ioc-runner` command invocation remains in any role.
- OS asymmetry: the gap manifests only on non-RHEL (Debian), because the shipped setup creates a `/usr/bin` symlink for RHEL families; the fix is verified real on Debian (before and after) and confirmed harmless on Rocky 8.
- 2026-08-17 supporting context: epics-ioc-runner M17 (#145) verified on two golden consumers that the alternate destination the role deploys is selected and run (default, alternate, and source modes; runner `1.2.3` `ddb558d-dirty`), with the default install coexisting.

#### G1 - Owner-Selected Consumer Release-Gate Bake and Release Authorization

- Origin: a519802 / G1
- GitHub Issue: none
- Status: Complete

##### Summary

The first release gate and matching tag sequence require owner selection and
authorization.

##### Concrete Meaning

`G1` is the decision record for one `epics-ioc-runner` consumer release gate.
The release-gate bake is the fresh-image acceptance run in which
`cloud-provision` produces the `rocky8-iocrunner` and `debian13-iocrunner`
variants, `ansible-provision` supplies the configured image contents, and the
consumer release-gate checks run against fresh consumers.

The `1.0.0` release names the gate environment — the pinned `cloud-provision`
and `ansible-provision` pair that bakes the golden and runs the gate — and is
version-agnostic in the `epics-ioc-runner` version it exercises. The
`epics-ioc-runner` version is a separate input to that gate; the version passed
through one run is recorded as that run's payload, not as part of the `1.0.0`
identity. The joint tag carries the name `iocrunner-gate-1.0.0` so it stays
distinct from other golden lines the same pair supports.

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

##### Recorded Decision (2026-08-17)

| Field | Recorded content |
| --- | --- |
| Selected bake | 2026-08-17 golden pair: `iocrunner-rocky8-20260817T083735Z-536321164923.qcow2` (bake `08:39:32Z`, sidecar sha256 `7c3f93f4…`) and `iocrunner-debian13-20260817T084259Z-ad954136c034.qcow2` (bake `08:44:51Z`, sidecar sha256 `9000f6e6…`); baked runner `commit=4868a251 tag=1.2.3 state=clean-tagged requested=1.2.3` |
| Source refs | `ansible-provision` `3981c21`, `cloud-provision` `2b77a97`, `epics-ioc-runner` `1.2.3` (`4868a25`); the golden carries EPICS-env `1.2.2` and EPICS base `7.0.10` |
| Consumer evidence | `validate_iocrunner_bake.bash` valid on both; `GATE SUITES PASS hosts=2` (Debian `614 na=0`, Rocky `614 na=12`); root_squash `SQUASH REPRODUCED` with zero layout warnings on both; 14/14 multi-user scenarios on both. Evidence: `epics-ioc-runner/work/gate-suites-20260817T085522Z-3870975/` |
| Release point | Joint bare-number tag `iocrunner-gate-1.0.0` on `cloud-provision` `2b77a97` and `ansible-provision` `3981c21`; `epics-ioc-runner` keeps `1.2.3` and is referenced through the bake manifest, not re-tagged |
| Authorization | Owner confirmed the release basis and the `iocrunner-gate-1.0.0` tag name on 2026-08-17 and directed this record; tag execution is `M2` and requires a separate release delegation |

##### Completion Criteria

- The required decision record identifies one selected consumer release-gate bake.
- Fresh consumers from the selected bake pass the consumer release-gate checks.
- The owner authorization for the selected bake and matching tag sequence is recorded.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-08-17 | Pass (Gate grade) | Fresh 1.2.3-baseline goldens and fresh consumers on Rocky 8 and Debian 13; `validate_iocrunner_bake.bash` valid on both; `GATE SUITES PASS hosts=2` (Debian `SUITES OK 614 na=0`, Rocky `SUITES OK 614 na=12`); root_squash `SQUASH REPRODUCED`, layout warnings 0, bare hash `4868a25` on both; multi-user 14/14 on both. Control head `4868a251`, dirty=false. Evidence: `epics-ioc-runner/work/gate-suites-20260817T085522Z-3870975/` (Debian log sha256 `65559e31…`, Rocky log sha256 `04c81f55…`) |

##### Closure Evidence

- The Gate-grade run passed on both goldens (suites, root_squash, multi-user) at baseline `1.2.3`; the owner selected this bake and the `iocrunner-gate-1.0.0` tag name as the Version 1.0 release basis on 2026-08-17.
- `G1` records the decision and authorizes `M2` to execute the matching tag sequence. The `iocrunner-gate-1.0.0` tags on `cloud-provision` and `ansible-provision` are not yet cut; that execution is `M2` and requires a separate release delegation.

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
| Gates | G3 | Owner decision on Ansible SSH master reuse | External gate | Complete | No | | Owner records a Keep verdict after the real recreate path shows no stale master; [detail](#g3---owner-decision-on-ansible-ssh-master-reuse) |

Unassigned work belongs here; the release tally above excludes this section.

### Backlog Details

#### G3 - Owner Decision on Ansible SSH Master Reuse

- Origin: a519802 / G3
- Identity History: added to the current generation from GitHub issue #10 after the 2026-08-12 code comparison
- GitHub Issue: #10, https://github.com/jeonghanlee/ansible-provision/issues/10
- Status: Complete

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
| T1 | 2026-08-16 | Testbed VM rocky8 `.100` | Passed | Real destroy-recreate observed; no stale master. The idle master was reaped by `ControlPersist=60s` before the recreate completed, and the reconnect reached the fresh VM (`up 2 min`, `rc=0`) through a new master. |

##### Closure Evidence

- Gate closed by an owner-approved Keep verdict recorded in `docs/CLOSED_DOORS.md` on 2026-08-16.
- The real recreate path shows no stale control master; `ansible.cfg` is left unchanged. `host_key_checking=False` already neutralizes the separate reused-address `known_hosts` warning.

##### GitHub Projection

- Title: `Ansible reuses an SSH master keyed on a reused address`
- Labels: `bug`
- GitHub Milestone: `Backlog`
- Observed State: closed
- Observed Labels: `bug`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-16; GitHub updated 2026-08-16T09:40:04Z

## Assignment History

| Date | Work | From | To | Synchronization Commit |
| --- | --- | --- | --- | --- |
| 2026-08-16 | M5 | Backlog | Milestone | this synchronization commit |
| 2026-08-17 | M6 | Backlog | Milestone | this synchronization commit |

## History

| Reset Date | Prior State Commit |
| --- | --- |
| 2026-08-06 | a51980286459dde442e7aa59ed11d2e5b46201cd |
