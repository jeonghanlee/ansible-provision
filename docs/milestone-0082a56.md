# Work Register

## Scope

This document is the canonical work register for the `master` release line of
`ansible-provision`. It records deliverables, dependencies, implementation
plans, verification results, and live GitHub metadata.

**Out of scope:** detailed operating procedures remain in the linked runbooks;
EtherCAT execution remains in the owner's separate tracker; GitHub issue
mutation remains subject to the repository Git workflow.

- Release line: master
- Milestone index: 0082a56
- Canonical path: `docs/milestone-0082a56.md`
- Canonical branch or ref: `master`
- Git upstream: `origin/master`
- Remote tracker: `jeonghanlee/ansible-provision`, GitHub milestone `Backlog`

Next session entry point: resolve `G6`, then update the gate and `M.4` in this
document. `M.13` has no remaining code or issue-closure work; its selector and
provenance implementation is present and verified.

Status tally: 11 Complete, 2 Blocked. External gates: 5 Complete, 2 Open.

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core | M.1 | Base OS readiness | Milestone | Complete | No | G.1 | Rocky 8 and Debian 13 base readiness and generated PVXS IOC checks pass; [detail](#m1---base-os-readiness) |
| Core | M.2 | Application role reliability | Milestone | Complete | No | | Application roles build, install, and fail on build errors on both supported OS families; [detail](#m2---application-role-reliability) |
| Core | M.3 | EPICS binary-distribution deployment | Milestone | Complete | No | G.1 | Binary distribution, login activation, and version-path checks pass on both supported OS families; [detail](#m3---epics-binary-distribution-deployment) |
| Core | M.4 | EPICS-env source-build environment | Carry-forward | Blocked | No | G.2, G.6 | Rocky 8, Debian 13, Rocky 10, and Ubuntu 24 pass; Ubuntu 26 requires the GCC 15 compatibility condition; [detail](#m4---epics-env-source-build-environment) |
| Core | M.5 | IOC runner deployment | Milestone | Complete | No | G.1 | Installed IOC runner smoke and lifecycle checks pass on both supported OS families; [detail](#m5---ioc-runner-deployment) |
| Core | M.6 | NFS simulation | Milestone | Complete | No | | Export, mount, ownership, permission, and root-squash checks pass on both supported OS families; [detail](#m6---nfs-simulation) |
| Core | M.7 | Test fixtures and bake provenance | Carry-forward | Complete | No | G.1 | Fixture, de-proxy, manifest, provenance, and fresh-consumer checks pass; [detail](#m7---test-fixtures-and-bake-provenance) |
| Core | M.8 | Repository architecture and operating documentation | Carry-forward | Complete | No | | Public baseline, overlay boundary, playbook topology, and raw-task contract are documented; [detail](#m8---repository-architecture-and-operating-documentation) |
| Core | M.9 | Current status synchronization | Carry-forward | Complete | No | G.3 | Register, verification matrix, architecture, fixture, and linked issue observations agree; [detail](#m9---current-status-synchronization) |
| Core | M.10 | EtherCAT verification transfer | Carry-forward | Complete | No | | Roles remain present and live acceptance is recorded in the owner's separate tracker; [detail](#m10---ethercat-verification-transfer) |
| Release | M.11 | Version 1.0 release convention | Carry-forward | Blocked | No | G.4 | Consumer release gate, matching tags, and next version-scoped register are completed; [detail](#m11---version-10-release-convention) |
| Core | M.12 | Review decisions and conceptual-integrity closure | Carry-forward | Complete | No | | Review decisions and finding dispositions remain discoverable; [detail](#m12---review-decisions-and-conceptual-integrity-closure) |
| Core | M.13 | Consumer-selectable IOC runner version | Milestone | Complete | No | G.5, G.7 | Selector, provenance record, cloud caller, validator, bake observations, and linked issue state agree; [detail](#m13---consumer-selectable-ioc-runner-version) |
| Gates | G.1 | Fresh variants from the 2026-07-28 Rocky 8 and Debian 13 iocrunner goldens | External gate | Complete | No | | Fresh server variants passed the required runtime checks. [detail](#g1---fresh-variants-from-the-2026-07-28-rocky-8-and-debian-13-iocrunner-goldens) |
| Gates | G.2 | Configured Rocky 8, Rocky 10, Ubuntu 24, and Ubuntu 26 EPICS-env build hosts | External gate | Complete | No | | Fresh hosts were created and source-build runs were observed on all four operating systems. [detail](#g2---configured-rocky-8-rocky-10-ubuntu-24-and-ubuntu-26-epics-env-build-hosts) |
| Gates | G.3 | GitHub issue mutation authorization | External gate | Complete | No | | Authorization was provided and linked issue observations were reconciled. [detail](#g3---github-issue-mutation-authorization) |
| Gates | G.4 | Owner-selected consumer release-gate bake and release authorization | External gate | Open | No | | Owner selects the release-gate bake and authorizes the tag sequence; [detail](#g4---owner-selected-consumer-release-gate-bake-and-release-authorization) |
| Gates | G.5 | `cloud-provision` accepts `requested` and passes the selector through the bake command | External gate | Complete | No | | `cloud-provision#26` landed in `8ad180a`; its suite reported 43/43. [detail](#g5---cloud-provision-selector-interface) |
| Gates | G.6 | Ubuntu 26 `iocStats` compatibility with GCC 15 | External gate | Open | No | | A compatible `iocStats` revision or correction is selected and the complete Ubuntu 26 path passes. [detail](#g6---ubuntu-26-iocstats-compatibility-with-gcc-15) |
| Gates | G.7 | GitHub issue #9 closure or owner exception | External gate | Complete | No | | Issue #9 was closed after body reconciliation as a duplicate of the independently implemented `pkg_automation` caller stage. [detail](#g7---github-issue-9-closure-or-owner-exception) |

### Decisions

| ID | Decision | Source |
| --- | --- | --- |
| D.1 | `M.x` identifies a deliverable; `T.k` is verification inside that milestone and is not an independent work identifier. | User direction, 2026-07-28 |
| D.2 | Keep `04_nfs_sim` free of `app_ioc_runner`; root-principal validation is incompatible with the root-squash mount. | U7 amendment, commit `3ea5c20` |
| D.3 | Keep EtherCAT roles in this repository and track live acceptance separately. | User direction, 2026-07-05 |
| D.4 | Use GitHub issues for cross-repository or externally referenced work, synchronized after local document review. | U4 plus user direction, 2026-07-28 |
| D.5 | Use bare-number release tags jointly with `cloud-provision` at an accepted consumer release gate. | U8, 2026-07-03 |

### Milestone Details

#### M.1 - Base OS Readiness

- Origin: 0082a56 / M.1
- Identity History: identifier preserved from the legacy register
- GitHub Issue: #8, https://github.com/jeonghanlee/ansible-provision/issues/8
- Status: Complete

##### Summary

Rocky 8 and Debian 13 hosts provide the system packages, time service, sudo
path behavior, and operator prerequisites required by higher layers.

##### Scope

Apply the base role, verify standard tools, resolve the Rocky 8 sudo path, and
build a generated PVXS IOC on the current Rocky 8 golden.

Out of scope: application roles, EPICS source builds, and EtherCAT live
acceptance.

##### Completion Criteria

- Base role repeated-run checks pass on Rocky 8 and Debian 13.
- Required tools and the generated PVXS IOC build pass.
- The Rocky 8 `libevent-devel` dependency is present for generated IOC linking.

##### Dependencies And Decisions

- `G.1` is Complete. `D.1` and `D.4` apply.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail, carried from `docs/MILESTONES.md`
- Implementation Authorization: prior committed implementation and verification evidence
- Superseded Plan Artifacts: none

1. Apply the base role and verify its repeated-run behavior on both supported OS families.
2. Verify the required tools, sudo path, SSH-key warning, and generated PVXS IOC build.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Apply `01_base` twice | Rocky 8 | Second run reports `changed=0` and `failed=0`. |
| T2 | Integration | Apply `01_base` twice | Debian 13 | Second run is idempotent. |
| T3 | Runtime | Verify `git`, `make`, `lsof`, `ss`, and `socat` | Rocky 8 and Debian 13 | All required tools resolve. |
| T4 | Build | Build generated PVXS IOC | Current Rocky 8 golden | Build exits 0 and produces the executable. |
| T5 | Runtime | Resolve `con` and `conserver` through sudo `secure_path` | Rocky 8 | Both commands resolve. |
| T6 | Static and runtime | Run `setup_host.bash` without a supported public key | Control host | The missing-key condition is reported. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-28 | Rocky 8 golden | Passed | `docs/MILESTONES.md`, `changed=0`, `failed=0` |
| T2 | 2026-07-04 | Debian 13 | Passed | `docs/STATUS.md` |
| T3 | 2026-07-04 | Rocky 8 and Debian 13 | Passed | Status snapshot in `docs/MILESTONES.md` |
| T4 | 2026-07-04 | Rocky 8 golden | Passed | ServiceTestIOC `91d42b2`, generated executable |
| T5 | 2026-07-02 | Rocky 8 | Passed | Commit `c5b3fbe` |
| T6 | 2026-07-04 | Control host | Passed | `bin/setup_host.bash` Ed25519 and RSA checks |

##### Closure Evidence

- All six checks have observed evidence. GitHub #8 is closed; live state was observed on 2026-08-06.

##### GitHub Projection

- Title: `rocky8 lacks libevent-devel; generated IOCs fail to link against pvxs`
- Labels: `bug`
- GitHub Milestone: none
- Observed State: closed
- Observed Labels: `bug`
- Observed Milestone: none
- Last Compared: 2026-08-06; GitHub updated 2026-07-18T08:13:30Z

#### M.2 - Application Role Reliability

- Origin: 0082a56 / M.2
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

The `app_con`, `app_procserv`, and `app_conserver` roles fail on build errors
and install usable binaries on both supported OS families.

##### Scope

Apply and re-run the three application roles, verify installed binaries, and
verify that build or environment-script failures cannot report success.

Out of scope: EPICS application deployment and EtherCAT roles.

##### Completion Criteria

- Each application role passes apply and re-run checks on Rocky 8 and Debian 13.
- Installed binaries are usable on both OS families.
- Build and environment-script failures return failure.

##### Dependencies And Decisions

- None. `D.1` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail, carried from `docs/MILESTONES.md`
- Implementation Authorization: prior committed implementation and verification evidence
- Superseded Plan Artifacts: none

1. Apply and re-run the three application roles on both supported OS families.
2. Verify installed binaries and failure propagation.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Apply and re-run `app_con` | Rocky 8 and Debian 13 | Both runs pass. |
| T2 | Integration | Apply and re-run `app_procserv` | Rocky 8 and Debian 13 | Both runs pass. |
| T3 | Integration | Apply and re-run `app_conserver` | Rocky 8 and Debian 13 | Both runs pass. |
| T4 | Runtime | Verify `con`, `procServ`, and `conserver` | Rocky 8 and Debian 13 | Installed commands run from their expected paths. |
| T5 | Failure path | Force application build or environment-script failure | Role test environment | Ansible reports failure. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-04 | Rocky 8 and Debian 13 | Passed | `docs/STATUS.md` |
| T2 | 2026-07-04 | Rocky 8 and Debian 13 | Passed | `docs/STATUS.md` |
| T3 | 2026-07-04 | Rocky 8 and Debian 13 | Passed | `docs/STATUS.md` |
| T4 | 2026-07-04 | Rocky 8 and Debian 13 | Passed | Independent binary checks |
| T5 | 2026-07-04 | Role test environment | Passed | Commit `cc8e686`, targeted V1-V2 checks |

##### Closure Evidence

- All five checks have observed evidence and the application roles are complete.

#### M.3 - EPICS Binary-Distribution Deployment

- Origin: 0082a56 / M.3
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

`app_epics` installs the selected EPICS-env binary distribution and deploys a
working login activation script on Rocky 8 and Debian 13.

##### Scope

Bake both supported OS variants, verify login activation, run `caget -h`, and
match installed EPICS-env and EPICS Base versions to inventory selectors.

Out of scope: source-built EPICS-env hosts and release tagging.

##### Completion Criteria

- Rocky 8 and Debian 13 bakes complete with EPICS-env 1.2.2.
- Login activation, `caget -h`, and installed path checks pass on fresh variants.

##### Dependencies And Decisions

- `G.1` is Complete. `D.1` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail, carried from `docs/MILESTONES.md`
- Implementation Authorization: prior committed implementation and verification evidence
- Superseded Plan Artifacts: none

1. Install the selected binary distribution through `app_epics`.
2. Verify login activation and installed version identity on both OS families.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Bake | Bake Rocky 8 with EPICS-env 1.2.2 | Rocky 8 | Bake passes. |
| T2 | Bake | Bake Debian 13 with EPICS-env 1.2.2 | Debian 13 | Bake passes. |
| T3 | Runtime | Source `/etc/profile.d/epics-env.sh` | Fresh variants | Login activation succeeds. |
| T4 | Runtime | Run `caget -h` | Fresh variants | Command exits 0. |
| T5 | Runtime | Match EPICS-env, OS directory, and EPICS Base selectors | Fresh variants | Installed values match inventory. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-28 | Rocky 8 | Passed | Commit `1efca35` |
| T2 | 2026-07-28 | Debian 13 | Passed | Commit `1efca35` |
| T3 | 2026-07-28 | Rocky 8 and Debian 13 | Passed | Fresh variant login checks |
| T4 | 2026-07-28 | Rocky 8 and Debian 13 | Passed | `caget -h` returned success |
| T5 | 2026-07-28 | Rocky 8 and Debian 13 | Passed | Installed paths: EPICS-env 1.2.2, EPICS Base 7.0.10 |

##### Closure Evidence

- All five checks have observed evidence on fresh variants.

#### M.4 - EPICS-env Source-Build Environment

- Origin: 0082a56 / M.4
- Identity History: identifier preserved from the legacy register
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

- `G.2` is Complete.
- `G.6` is Open; resume as `In progress` after the Ubuntu 26 compatibility condition is complete.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail and GitHub #7 plan
- Implementation Authorization: prior committed implementation and verification evidence
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
| T5 | Matrix | Build configured source-build hosts | Rocky 10, Ubuntu 24, Ubuntu 26 | Rocky 10 and Ubuntu 24 pass; Ubuntu 26 passes after `G.6`. |
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

- `M.4` remains Blocked by `G.6`. GitHub #7 is open and its current live state was observed on 2026-08-06.

##### GitHub Projection

- Title: `EPICS-env source-build verification matrix`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Observed State: open
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-06; GitHub updated 2026-07-29T00:20:45Z

#### M.5 - IOC Runner Deployment

- Origin: 0082a56 / M.5
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

IOC runner hosts provide the installed runtime, source tree, inspection
commands, and consumer lifecycle behavior required by `epics-ioc-runner`.

##### Scope

Verify stamped metadata, inspection commands, local source-root behavior, the
NFS-side consumer path, and fresh EPICS-env 1.2.2 golden behavior.

Out of scope: live EtherCAT validation and consumer release tagging.

##### Completion Criteria

- Local and infrastructure smoke checks pass on accepted goldens.
- Fresh Rocky 8 and Debian 13 goldens pass the local, infrastructure, and system suites.

##### Dependencies And Decisions

- `G.1` is Complete. `D.2` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail, carried from `docs/MILESTONES.md`
- Implementation Authorization: prior committed implementation and verification evidence
- Superseded Plan Artifacts: none

1. Deploy the IOC runner runtime and source tree through `03_epics`.
2. Run local and consumer lifecycle checks on both accepted OS variants.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Runtime | Run `ioc-runner -V` | Accepted goldens | Stamped metadata is reported. |
| T2 | Runtime | Run `ioc-runner list -vv` and `ioc-runner inspect -h` | Accepted goldens | Both commands pass. |
| T3 | Integration | Verify source tree from the local source root | `03_epics` | Local source path is available. |
| T4 | Consumer integration | Exercise tar-push and consumer suite | NFS-side path | Consumer lifecycle checks pass. |
| T5 | Integration | Repeat smoke and lifecycle checks | Fresh Rocky 8 and Debian 13 goldens | All required suites pass. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Prior accepted golden verification | Accepted goldens | Passed | `docs/MILESTONES.md` |
| T2 | Prior accepted golden verification | Accepted goldens | Passed | `docs/MILESTONES.md` |
| T3 | Prior accepted golden verification | `03_epics` | Passed | Local source-root verification |
| T4 | Prior accepted release gate | NFS-side consumer path | Passed | `epics-ioc-runner` 1.2.0 release gate |
| T5 | 2026-07-28 | Fresh Rocky 8 and Debian 13 goldens | Passed | Rocky local 75/75, infrastructure 40/40, system 77/77; Debian local 63/63, infrastructure 41/41, system 77/77 |

##### Closure Evidence

- All five checks have observed evidence. Local Debian log-rotation steps were optional and skipped because `/usr/sbin` was outside the unprivileged user path.

#### M.6 - NFS Simulation

- Origin: 0082a56 / M.6
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

The `nfs_sim` role provides a loopback NFS export and mount that reproduces the
intended namespace, ownership, permissions, and root-squash boundary.

##### Scope

Apply `04_nfs_sim` on Rocky 8 and Debian 13, verify export and mount state,
and confirm regular-user writes and root-squashed writes.

Out of scope: running `app_ioc_runner` as root inside the root-squashed mount.

##### Completion Criteria

- Both supported OS variants pass export, mount, ownership, permission, and service checks.
- Root-squash behavior is observed and local IOC runner checks remain in `03_epics`.

##### Dependencies And Decisions

- `D.2` is resolved.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail and review `rs20260702_083212`
- Implementation Authorization: prior committed implementation and verification evidence
- Superseded Plan Artifacts: none

1. Apply the NFS simulation role on both supported OS families.
2. Verify the namespace and root-squash boundary without adding IOC runner validation to this role.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Integration | Apply `04_nfs_sim` | Rocky 8 | Role passes. |
| T2 | Integration | Apply `04_nfs_sim` | Debian 13 | Role passes. |
| T3 | Runtime | Verify export, mount, ownership, permissions, and service state | Both OS families | All values match the simulation contract. |
| T4 | Security boundary | Verify simulation-owner write and root-owned write denial | Both OS families | Root-squash behavior passes. |
| T5 | Boundary | Keep local and NFS-side IOC runner validation in their owning paths | Repository and consumer flow | No root-principal validation is added to `04_nfs_sim`. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-04 | Rocky 8 | Passed | `testbed-rocky8-iocrunner-server` |
| T2 | 2026-07-04 | Debian 13 | Passed | `testbed-debian13-iocrunner-server` |
| T3 | 2026-07-04 | Both OS families | Passed | `docs/STATUS.md` |
| T4 | 2026-07-04 | Both OS families | Passed | Root-squash verification |
| T5 | 2026-07-04 | Repository and consumer flow | Passed | Commit `3ea5c20`, review `rs20260702_083212` |

##### Closure Evidence

- All five checks have observed evidence and the ownership boundary is preserved.

#### M.7 - Test Fixtures and Bake Provenance

- Origin: 0082a56 / M.7
- Identity History: identifier preserved from the legacy register
- GitHub Issue: #6, https://github.com/jeonghanlee/ansible-provision/issues/6
- Status: Complete

##### Summary

The iocrunner golden bake installs multi-user fixtures, removes site-proxy
state, and records image and installed-source identities.

##### Scope

Run the fixture playbook in the bake, verify account and linger state, remove
proxy state, write the image and sidecar manifests, and validate installed
source identity on fresh consumers.

Out of scope: selector-specific provenance, which belongs to `M.13`.

##### Completion Criteria

- Fixture, de-proxy, manifest, sidecar, source identity, and fresh-consumer checks pass on both supported OS variants.
- Clean tagged, clean untagged, and dirty source states remain distinguishable.

##### Dependencies And Decisions

- `G.1` is Complete. `D.1` and `D.4` apply.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail and GitHub #6 acceptance
- Implementation Authorization: prior committed implementation and verification evidence
- Superseded Plan Artifacts: none

1. Apply `07_test_users.yml` after `04_nfs_sim.yml` in the bake.
2. De-proxy the image, record source and image identities, and validate fresh consumers.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Bake | Run `07_test_users.yml` after `04_nfs_sim.yml` | iocrunner bake | Fixture playbook runs in the required order. |
| T2 | Runtime | Verify `opa`, `opb`, `obs`, and user linger | Fresh Rocky 8 and Debian 13 variants | Account and linger state matches the contract. |
| T3 | Bake security | Scan for configured proxy state before flattening | Bake | Remnants fail the bake. |
| T4 | Provenance | Write in-image manifest and sidecar | Rocky 8 and Debian 13 bakes | Both manifests exist. |
| T5 | Provenance | Record repository revisions, selectors, base image, and `pip3 freeze` | Production bakes | Records are non-empty and auditable. |
| T6 | Consumer integration | Validate dirty or untagged source identity | Fresh Rocky 8 and Debian 13 consumers | Manifest state matches installed `ioc-runner -V`. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-05 | iocrunner bake | Passed | `bake_iocrunner_image.bash`, Step 6/9 |
| T2 | 2026-07-05 | Fresh Rocky 8 and Debian 13 variants | Passed | Fixture and linger checks |
| T3 | 2026-07-05 | Bake | Passed | De-proxy scan fails on remnants |
| T4 | 2026-07-29 | Production bakes | Passed | In-image and sidecar manifests |
| T5 | 2026-07-29 | Production bakes | Passed | ansible-provision `d4f09c2`, cloud-provision `b972dc0` |
| T6 | 2026-07-30 | Fresh Rocky 8 and Debian 13 consumers | Passed | `validate_iocrunner_bake.bash`; GitHub #6 closed |

##### Closure Evidence

- All six checks have observed evidence. GitHub #6 is closed; live state was observed on 2026-08-06.

##### GitHub Projection

- Title: `Write a provenance manifest into the iocrunner golden at bake time`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Observed State: closed
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-06; GitHub updated 2026-07-30T01:35:14Z

#### M.8 - Repository Architecture and Operating Documentation

- Origin: 0082a56 / M.8
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

Repository documentation describes the public baseline, inventory and overlay
boundaries, role topology, raw-task contract, and standalone workflows.

##### Scope

Document public defaults, site override points, Make target topology, raw-task
rules, standalone modes, and the `cloud-provision` responsibility boundary.

Out of scope: live runtime verification not recorded in the status companion.

##### Completion Criteria

- Architecture and operating documentation describe the current repository boundaries.
- Documentation does not claim unverified runtime behavior.

##### Dependencies And Decisions

- `D.1` and `D.4` apply.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail
- Implementation Authorization: prior committed documentation updates and verification evidence
- Superseded Plan Artifacts: none

1. Align the README, architecture, raw-style, standalone, and seam documents with the repository structure.
2. Record runtime status only in the status companion and canonical register.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Documentation | Inspect public defaults and site override points | Repository | Documentation matches configuration. |
| T2 | Documentation | Inspect all-node and server-only Make topology | Repository | Target ownership is accurate. |
| T3 | Documentation | Inspect raw-task and no-Python contract | Repository | Contract is explicit. |
| T4 | Documentation | Inspect standalone control-host and local-clone modes | Repository | Both modes are documented. |
| T5 | Documentation | Inspect `cloud-provision` responsibility boundary | Repository | Seam ownership is explicit. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-04 | Repository | Passed | `README.md`, `docs/ARCHITECTURE.md` |
| T2 | 2026-07-04 | Repository | Passed | `README.md`, `Makefile`, `configure/CONFIG_SITE` |
| T3 | 2026-07-04 | Repository | Passed | `docs/RAW_STYLE.md` |
| T4 | 2026-07-04 | Repository | Passed | `docs/STANDALONE.md` |
| T5 | 2026-07-04 | Repository | Passed | `docs/SEAM.md` |

##### Closure Evidence

- All five documentation checks have observed evidence.

#### M.9 - Current Status Synchronization

- Origin: 0082a56 / M.9
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

The register, verification matrix, architecture description, fixture
document, and linked GitHub issue observations describe the same state.

##### Scope

Register issues #7 and #8, playbooks 08 and 09, source-build roles, current
fixture claims, EPICS-env 1.2.2 documentation, and observed linked issue state.

Out of scope: changing the implementation represented by those records.

##### Completion Criteria

- Local documents and linked issue observations agree with committed work.
- Documentation checks and the complete diff have been reviewed.

##### Dependencies And Decisions

- `G.3` is Complete. `D.4` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted work register detail
- Implementation Authorization: prior committed synchronization updates
- Superseded Plan Artifacts: none

1. Reconcile status, architecture, fixture, and issue observations after substantive changes.
2. Preserve the distinction between local canonical status and live GitHub metadata.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Documentation | Register issues #7, #8, and post-2026-07-05 commits | Repository and GitHub | Current work is represented. |
| T2 | Documentation | Register playbooks 08 and 09 and source-build roles | Repository | Architecture and status agree. |
| T3 | Documentation | Inspect `test_users` activation claims | Repository | Stale claims are removed. |
| T4 | Documentation | Compare EPICS-env version documentation with inventory | Repository | Version is 1.2.2 throughout. |
| T5 | Static | Run documentation checks and inspect the complete diff | Repository | Checks pass and no required change is omitted. |
| T6 | External state | Compare linked GitHub #6, #7, and #8 | GitHub | Live issue state is recorded. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-31 | Repository and GitHub | Passed | Register and verification matrix |
| T2 | 2026-07-31 | Repository | Passed | Playbooks 08 and 09 and source-build roles |
| T3 | 2026-07-31 | Repository | Passed | README, architecture, seam, and fixture updates |
| T4 | 2026-07-31 | Repository | Passed | EPICS-env 1.2.2 records |
| T5 | 2026-07-31 | Repository | Passed | `git diff --check`, Make help, structure counts, syntax checks |
| T6 | 2026-08-06 | GitHub | Passed | Issues #6 and #8 closed; #7 open |

##### Closure Evidence

- The pre-migration register carried the synchronization evidence. Current live metadata is recorded in the linked milestone details.

#### M.10 - EtherCAT Verification Transfer

- Origin: 0082a56 / M.10
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

The repository retains EtherCAT roles and playbooks while live validation
ownership and acceptance remain in the owner's separate tracker.

##### Scope

Retain `ethercat_base`, `app_ethercat`, playbooks 05 and 06, and transfer live
acceptance and readiness follow-ups.

Out of scope: accepting the first EtherCAT bake or live R2-12 run here.

##### Completion Criteria

- Required roles and playbooks remain present.
- The separate ownership and unverified live state are recorded.

##### Dependencies And Decisions

- `D.3` is resolved.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner direction recorded 2026-07-05
- Implementation Authorization: owner direction recorded 2026-07-05
- Superseded Plan Artifacts: none

1. Preserve the EtherCAT roles and playbooks.
2. Keep live acceptance in the owner's separate tracker.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Static | Verify EtherCAT roles and playbooks remain present | Repository | Required components exist. |
| T2 | Documentation | Verify first bake and live R2-12 run are not accepted here | Repository | Unverified state is explicit. |
| T3 | Transfer | Verify U10 and readiness follow-ups are transferred | Repository and owner tracker | Ownership is explicit. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-05 | Repository | Passed | Roles and playbooks remain present |
| T2 | 2026-07-05 | Repository | Passed | `docs/STATUS.md` and `docs/SEAM.md` |
| T3 | 2026-07-05 | Repository and owner tracker | Passed | Commit `4a93bc3` |

##### Closure Evidence

- Live EtherCAT acceptance is deliberately outside this register under `D.3`.

#### M.11 - Version 1.0 Release Convention

- Origin: 0082a56 / M.11
- Identity History: identifier preserved from the legacy register
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

- `G.4` is Complete.
- The consumer release gate passes, matching tags are created, and the next register is opened.

##### Dependencies And Decisions

- `G.4` is Open; resume as `In progress` after owner release authorization.
- `D.5` applies.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: prior accepted release convention and owner direction
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
| T1 | 2026-07-03 | Repository and consumer project | Passed | Agreed scope recorded in the prior register |
| T2 | Not run | Consumer environment | Pending | Requires `G.4` |
| T3 | Not run | Repository family | Pending | Requires `G.4` and owner authorization |
| T4 | Not run | Repository | Pending | Follows T3 |

##### Closure Evidence

- `M.11` is Blocked by open `G.4`. No release mutation has been authorized in this session.

#### M.12 - Review Decisions and Conceptual-Integrity Closure

- Origin: 0082a56 / M.12
- Identity History: identifier preserved from the legacy register
- GitHub Issue: none
- Status: Complete

##### Summary

Repository-wide review decisions and deliberate keep, replace, retire, or
relocate outcomes remain discoverable after the review session.

##### Scope

Preserve the ten-lens review outcome, documentation and raw-task corrections,
fixture and provenance work, EtherCAT transfer, decisions U1-U10, and finding
dispositions.

Out of scope: reopening resolved review findings without a new owner decision.

##### Completion Criteria

- Review phases A through D and decisions U1-U10 remain recorded.
- Conceptual-integrity finding dispositions remain discoverable.

##### Dependencies And Decisions

- `D.1` through `D.5` apply.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: review session `rs20260702_083212` and convergence `conv20260702_190045`
- Implementation Authorization: review acceptance and owner direction recorded in prior commits
- Superseded Plan Artifacts: none

1. Preserve review outcomes, decision records, and finding dispositions.
2. Keep resolved outcomes discoverable in the canonical register and repository documents.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Review record | Inspect ten-lens review outcome | Repository | Review outcome is recorded. |
| T2 | Documentation | Inspect Phase A synchronization | Repository | Documentation truth is synchronized. |
| T3 | Code review | Inspect Phase B raw-task corrections | Repository | Required code corrections are present. |
| T4 | Integration | Inspect Phase C fixture, de-proxy, and provenance work | Repository and bake records | Phase C evidence is present. |
| T5 | Transfer | Inspect Phase D EtherCAT transfer | Repository | Transfer is recorded. |
| T6 | Decision record | Inspect decisions U1-U10 | Repository | Decisions remain present. |
| T7 | Finding record | Inspect conceptual-integrity dispositions | Repository | All findings have dispositions. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-07-02 | Repository | Passed | Review `rs20260702_083212`; convergence `conv20260702_190045` |
| T2 | 2026-07-04 | Repository | Passed | Commits `2439e6c` and `bde669f` |
| T3 | 2026-07-04 | Repository | Passed | Commits `cc8e686`, `13d2910`, `544c487`, and `4623e35` |
| T4 | 2026-07-05 | Repository and bake records | Passed | Commits `9910fe2`, `abe9979`, and cloud-provision `a8bdbd4` |
| T5 | 2026-07-05 | Repository | Passed | Commit `4a93bc3` |
| T6 | 2026-07-05 | Repository | Passed | Decisions remain summarized in the legacy register and migrated here |
| T7 | 2026-07-05 | Repository | Passed | Finding dispositions remain recorded |

##### Closure Evidence

- All seven review checks have observed evidence and no unresolved review decision is recorded.

#### M.13 - Consumer-Selectable IOC Runner Version

- Origin: 0082a56 / M.13
- Identity History: identifier preserved from the legacy register
- GitHub Issue: #9, https://github.com/jeonghanlee/ansible-provision/issues/9
- Status: Complete

##### Summary

The `app_ioc_runner` role accepts an `ioc_runner_version` selector so a golden
image carries the runner requested by the caller. The bake manifest records the
requested ref beside the resolved commit. Both repository halves are present;
the linked issue remains open.

##### Scope

Select a tag, branch, or commit-ish before installation, retain the unset
selector as a no-op, reject an invalid selector by name, record the requested
ref, and validate the Rocky 8 and Debian 13 bake path.

Out of scope: changing the unset default behavior, changing `epics-ioc-runner`,
changing EPICS distribution pinning, or marking completion while the linked
issue remains open without an owner exception. The pre-existing recorder
validation laxity is recorded in `docs/CLOSED_DOORS.md`.

##### Completion Criteria

- Unset selector preserves the existing default-branch behavior.
- A released tag selects the same commit on both supported OS families.
- The manifest distinguishes requested ref and resolved commit.
- A nonexistent ref fails by name and does not publish an image.
- GitHub #9 is closed after projection reconciliation, or the owner records an explicit exception.

##### Dependencies And Decisions

- `G.5` is Complete.
- `G.7` is Complete.
- `D.1` and `D.4` apply.

##### Implementation Plan

- Plan Status: accepted
- Plan Acceptance: owner-approved plan recorded in the legacy register, 2026-07-28
- Implementation Authorization: owner request to inspect the issue, update the milestone, and implement, 2026-08-06
- Superseded Plan Artifacts: none

1. Add the optional selector to inventory and resolve it to one commit before installation. Landed in `75f16c3` and `ca2a9de`.
2. Extend the provenance record with the requested selector while preserving schema-1 compatibility. Landed in `75f16c3`.
3. Pass the selector through the `cloud-provision` bake caller and accept the requested record field. Landed in `cloud-provision` `8ad180a`; `G.5` is Complete.
4. Run the real bake matrix and local shipped tests; close the milestone only when code, bake evidence, and linked issue state agree.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Bake | Run unset selector bakes | Rocky 8 and Debian 13 | Ten-step bakes pass and the six-field record has no `requested=` field. |
| T2 | Bake and consumer integration | Run a released-tag bake with `-r 1.2.2` and boot fresh consumers | Rocky 8 and Debian 13 | Installed `ioc-runner -V` reports the commit for tag `1.2.2`. |
| T3 | Provenance integration | Read `/etc/iocrunner-bake.manifest` and sidecar after a pinned bake | Rocky 8 and Debian 13 | Requested ref and resolved commit are both present and match. |
| T4 | Failure integration | Run a bake with a nonexistent selector | Debian 13 | Step 4 fails by name, no fallback occurs, and no image is published. |
| T5 | Shipped logic | Run `tests/check-ioc-runner-version-selector.bash` | Local Linux host, repository `0082a56` | The extracted shipped role body passes all selector cases. |
| T6 | Shipped recorder | Run `tests/check-bake-provenance-recorder.bash` | Local Linux host, repository `0082a56` | The shipped recorder passes both record shapes and malformed-input checks. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-08-01 | Rocky 8 and Debian 13, host `Neutron` | Passed | Both unset-selector bakes completed 10/10 with six-field records. |
| T2 | 2026-08-01 | Rocky 8 and Debian 13, host `Neutron` | Passed | Pinned bakes with `-r 1.2.2`; fresh consumers reported `1.2.2 (fd14875)`. |
| T3 | 2026-08-01 | Rocky 8 and Debian 13, host `Neutron` | Passed | Manifest record carried `commit=fd14875df5fdbfcb362d194e81bf74c1de960daa state=clean-tagged tag=1.2.2 requested=1.2.2`. |
| T4 | 2026-08-01 | Debian 13, host `Neutron` | Passed | Failure message named `9.9.9-nonexistent`; no fallback, publish, or archive replacement occurred. |
| T5 | 2026-08-06 | Local Linux host, repository `0082a56` | Passed | `tests/check-ioc-runner-version-selector.bash`: 22/22. |
| T6 | 2026-08-06 | Local Linux host, repository `0082a56` | Passed | `tests/check-bake-provenance-recorder.bash`: 35/35. |

##### Closure Evidence

- The implementation and all six verification checks have observed evidence.
- `G.5` and `G.7` are Complete. GitHub #9 was closed as a duplicate after its body was reconciled with the implementation and verification evidence.
- No code change remains for `M.13`.

##### GitHub Projection

- Title: `Make the baked ioc-runner version selectable by the caller`
- Labels: `enhancement`
- GitHub Milestone: `Backlog`
- Observed State: closed
- Observed Labels: `enhancement`
- Observed Milestone: `Backlog`
- Last Compared: 2026-08-06; GitHub updated 2026-08-07T06:21:49Z

#### G.1 - Fresh Variants From the 2026-07-28 Rocky 8 and Debian 13 Iocrunner Goldens

- Origin: 0082a56 / G.1
- GitHub Issue: none
- Status: Complete

##### Summary

Fresh server variants backed by the accepted Rocky 8 and Debian 13 iocrunner
goldens provide the runtime environments required by `M.1`, `M.3`, and `M.5`.

##### Completion Criteria

- Both fresh variant families pass the required runtime checks.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-07-28 | Passed | Fresh server variants and current-image checks |

##### Closure Evidence

- Gate closed before the current canonical migration and remains complete.

#### G.2 - Configured Rocky 8, Rocky 10, Ubuntu 24, and Ubuntu 26 EPICS-env Build Hosts

- Origin: 0082a56 / G.2
- GitHub Issue: none
- Status: Complete

##### Summary

The configured source-build hosts required by `M.4` were created and the
current source-build runs were observed.

##### Completion Criteria

- All four configured operating-system hosts exist and are reachable for the source-build matrix.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-07-28 | Passed | Fresh hosts and current source-build runs on all four operating systems |

##### Closure Evidence

- Gate closed. Ubuntu 26 build failure remains separately represented by `G.6`.

#### G.3 - GitHub Issue Mutation Authorization

- Origin: 0082a56 / G.3
- GitHub Issue: none
- Status: Complete

##### Summary

Authorization for the prior linked issue reconciliation was provided and the
local register recorded the observed state.

##### Completion Criteria

- Authorized issue observations and local reconciliation are recorded.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-07-28 | Passed | GitHub #6 reconciliation recorded in the prior register |

##### Closure Evidence

- Gate closed in the prior work register.

#### G.4 - Owner-Selected Consumer Release-Gate Bake and Release Authorization

- Origin: 0082a56 / G.4
- GitHub Issue: none
- Status: Open

##### Summary

The first release gate and matching tag sequence require owner selection and
authorization.

##### Completion Criteria

- Owner selects the consumer release-gate bake and authorizes the release sequence.
- The selected bake passes and the authorization is recorded.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-08-06 | Pending | No repository tag or owner release authorization is recorded. |

##### Closure Evidence

- Gate remains Open and blocks `M.11`.

#### G.5 - Cloud-provision Selector Interface

- Origin: 0082a56 / G.5
- GitHub Issue: cloud-provision#26
- Status: Complete

##### Summary

`cloud-provision` accepts the optional `requested` application-record field and
passes the selector through the bake command.

##### Completion Criteria

- The validator accepts one optional requested ref for `app_ioc_runner`.
- The bake command accepts `-r <ref>` and passes it to the caller.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-08-01 | Passed | `cloud-provision` `8ad180a`; its suite reported 43/43. |

##### Closure Evidence

- Gate closed and `M.13/T.2` and `M.13/T.3` were released.

#### G.6 - Ubuntu 26 IOCStats Compatibility With GCC 15

- Origin: 0082a56 / G.6
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

- Gate remains Open and blocks `M.4`.

#### G.7 - GitHub Issue 9 Closure or Owner Exception

- Origin: 0082a56 / G.7
- GitHub Issue: #9, https://github.com/jeonghanlee/ansible-provision/issues/9
- Status: Complete

##### Summary

The linked issue must be closed after the local canonical content is
reconciled, or the owner must record an explicit exception before `M.13` can
be marked Complete.

##### Completion Criteria

- GitHub #9 is observed closed after projection reconciliation, or an owner exception names the waived closure condition.

##### Verification Results

| Observed At | Result | Evidence |
| --- | --- | --- |
| 2026-08-06 | Passed | GitHub #9 is closed in milestone `Backlog` after its body was reconciled and the duplicate close reason was recorded. |

##### Closure Evidence

- Gate is Complete and `M.13` is Complete.

## Backlog

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

No unassigned work is currently recorded. New unassigned work belongs here;
the release tally above excludes this section.

### Backlog Details

No backlog details are currently recorded.

## Migration Notes

The legacy register `docs/MILESTONES.md` remains in the repository as a
historical migration source. Its identifiers, accepted plans, observed results,
decisions, and evidence were transferred here without deleting that source.
This document is the current authority for status, dependencies, plans, tests,
and closure evidence.
