# ansible-provision Milestones

## Scope

This document is the canonical work register for `ansible-provision`. It
records project deliverables as `M.x` milestones and the verification required
to close each milestone as `T.k` checks.

**Out of scope:** detailed operating procedures remain in the linked runbooks,
and EtherCAT execution remains in the owner's separate tracker.

Mode: register-authoritative. This file is the local source of truth; linked
GitHub issues must be reconciled to it after document review.

## Format

- `M.x` identifies a deliverable.
- `T.k` identifies one verification required to close its containing `M.x`.
  `T.k` numbering restarts within each milestone and is not an independent work
  identifier.
- `G.x` identifies an external condition or operator action.
- `D.x` identifies a durable decision.
- Status: ✅ Complete · 🔄 In progress · ⬜ Not started · ⚠️ Conditional ·
  🔒 Blocked.
- A milestone is Complete only when every required `T.k` has observed evidence.
  A clean syntax check does not replace a live execution requirement.

## Now / Next (2026-07-29)

- In progress: `M.7/T.5-T.6`.
- Ready now: P009 final real-path acceptance from clean pushed commits
  `ansible-provision` `6ced253` and `cloud-provision` `c4ba7fd`.
- External wait: Ubuntu 26 `iocStats` compatibility for `M.4/T.5` and the
  first release gate (`G.4`).

Next session entry point: run the final production IOC runner bakes for Rocky 8
and Debian 13 from the clean pushed commits, then boot fresh
`rocky8-iocrunner.server` and `debian13-iocrunner.server` consumers and compare
their manifests against the running systems.

Tally: 12 milestones - ✅ 9 · 🔄 1 · 🔒 2.

## Milestone Summary

| ID | Deliverable | Type | Status | Evidence or next action |
| :-- | :-- | :-- | :-- | :-- |
| M.1 | Base OS readiness | Milestone | ✅ | The current Rocky 8 golden passed an idempotent base-role re-run and a generated PVXS IOC build. |
| M.2 | Application role reliability | Milestone | ✅ | Both supported OS families passed the application role checks. |
| M.3 | EPICS binary-distribution deployment | Milestone | ✅ | Both fresh variants passed login activation, `caget -h`, and version-path checks. |
| M.4 | EPICS-env source-build environment | Milestone | 🔒 | Rocky 8, Rocky 10, and Ubuntu 24 passed; Ubuntu 26 is blocked by GCC 15 errors in `iocStats`. |
| M.5 | IOC runner deployment | Milestone | ✅ | Both fresh variants passed installed-runner local and system lifecycle suites. |
| M.6 | NFS simulation | Milestone | ✅ | Rocky 8 and Debian 13 passed export, mount, ownership, and root-squash checks. |
| M.7 | Test fixtures and bake provenance | Carry-forward | 🔄 | Provenance implementation and preliminary real-path review passed; final production bakes and fresh consumer comparison remain. |
| M.8 | Repository architecture and operating documentation | Carry-forward | ✅ | Public baseline, overlay boundary, playbook topology, and raw-task contract are documented. |
| M.9 | Current status synchronization | Carry-forward | ✅ | Local documents and linked GitHub issue state were reconciled on 2026-07-28. |
| M.10 | EtherCAT verification transfer | Carry-forward | ✅ (retired) | The owner moved live EtherCAT verification to separate tracking on 2026-07-05. |
| M.11 | Version 1.0 release convention | External gate | 🔒 | Wait for the next consumer release-gate bake and User-run tag sequence. |
| M.12 | Review decisions and conceptual-integrity closure | Carry-forward | ✅ | Review outcomes, decisions U1-U10, and finding dispositions are recorded. |

## M.1 Base OS Readiness

### Deliverable

Rocky 8 and Debian 13 hosts provide the system packages, time service, sudo
path behavior, and operator prerequisites required by the higher layers.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Apply `01_base` twice on Rocky 8. | ✅ | The current golden received a second real `01_base` run: `changed=0`, `failed=0`. |
| T.2 | Apply `01_base` twice on Debian 13. | ✅ | `docs/STATUS.md` records applied and idempotent verification. |
| T.3 | Verify `git`, `make`, `lsof`, `ss`, and `socat`. | ✅ | Verified on both supported OS families before the 2026-07-04 status snapshot. |
| T.4 | Build a generated PVXS IOC on the current Rocky 8 golden. | ✅ | ServiceTestIOC `91d42b2` declares `pvxsIoc pvxs`; the real build produced its executable with exit 0. |
| T.5 | Resolve `con` and `conserver` through the Rocky 8 sudo `secure_path`. | ✅ | Verified 2026-07-02; commit `c5b3fbe`. |
| T.6 | Warn when no supported SSH public key exists. | ✅ | `bin/setup_host.bash` checks Ed25519 and RSA public-key paths. |

## M.2 Application Role Reliability

### Deliverable

The `app_con`, `app_procserv`, and `app_conserver` roles fail on build errors
and install usable binaries on both supported OS families.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Apply and re-run `app_con` on Rocky 8 and Debian 13. | ✅ | Role-by-OS verification is recorded in `docs/STATUS.md`. |
| T.2 | Apply and re-run `app_procserv` on Rocky 8 and Debian 13. | ✅ | Role-by-OS verification is recorded in `docs/STATUS.md`. |
| T.3 | Apply and re-run `app_conserver` on Rocky 8 and Debian 13. | ✅ | Role-by-OS verification is recorded in `docs/STATUS.md`. |
| T.4 | Verify `con`, `procServ`, and `conserver` at their installed paths. | ✅ | Independent binary checks passed on both OS families. |
| T.5 | Confirm application build or environment-script failures cannot report success. | ✅ | Commit `cc8e686`; targeted verification V1-V2 passed. |

## M.3 EPICS Binary-Distribution Deployment

### Deliverable

`app_epics` installs the selected EPICS-env binary distribution and deploys a
working login activation script on Rocky 8 and Debian 13.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Bake Rocky 8 with EPICS-env 1.2.2. | ✅ | Commit `1efca35` records a successful 2026-07-28 iocrunner golden bake. |
| T.2 | Bake Debian 13 with EPICS-env 1.2.2. | ✅ | Commit `1efca35` records a successful 2026-07-28 iocrunner golden bake. |
| T.3 | Source `/etc/profile.d/epics-env.sh` on fresh variants from both goldens. | ✅ | Real login activation succeeded on both current variants. |
| T.4 | Run `caget -h` on both fresh variants. | ✅ | The installed `caget` returned success on both current variants. |
| T.5 | Match the installed EPICS-env, OS directory, and EPICS Base versions to inventory selectors. | ✅ | Observed paths are 1.2.2 with `rocky-8.10` or `debian-13`, and EPICS Base 7.0.10. |

## M.4 EPICS-env Source-Build Environment

### Deliverable

Dedicated build hosts compile EPICS-env and EPICS-env-support from source,
install vendor libraries into the release tree, and validate the installed
runtime without changing `site.yml`.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Build and re-run the current EPICS-env path on Rocky 8. | ✅ | On 2026-07-28, fresh `08_epics_env_build.yml` and `09_epics_env_support_build.yml` runs produced a 64-entry tree; the layer-1 re-run had `changed=0`, and all gates including `check_deps.bash` passed. |
| T.2 | Build and re-run the current EPICS-env path on Debian 13. | ✅ | Commits `5c4f7fc` and `0148514`: the current layered tree passed `check_deps`. |
| T.3 | Build vendor libraries inside the Debian 13 release tree with no absolute-path dependency findings. | ✅ | Commit `5c4f7fc`: `check_deps` reduced from 9 absolute paths to 0. |
| T.4 | Build the EPICS-env-support layer on Debian 13. | ✅ | Commit `0148514`: full layered tree and `check_deps` exit 0. |
| T.5 | Build the configured Rocky 10, Ubuntu 24, and Ubuntu 26 matrix hosts. | 🔒 | On 2026-07-28, Rocky 10 and Ubuntu 24 passed both `gz` layers and all gates. Ubuntu 26 `08_epics_env_build.yml` exited 2 in `iocStats` because GCC 15 rejects incompatible device-support function pointers; layer 2 and the gates were not run after this failure. |
| T.6 | Build the `gz` flavor through both source-build roles. | ✅ | Rocky 10 and Ubuntu 24 passed both source-build roles with installed `-g0 -gz=zlib` flags and `check_deps.bash` exit 0. `MCoreUtils` retained `.debug_info` on both hosts as an informational finding. |
| T.7 | Re-run the support role and observe its installed-tree skip. | ✅ | The Rocky 8 support-role re-run emitted `EPICS_ENV_SUPPORT_BUILD_SKIPPED`, with `changed=0` and `failed=0`. |

## M.5 IOC Runner Deployment

### Deliverable

IOC runner hosts provide the installed runtime, source tree, inspection
commands, and consumer lifecycle behavior required by `epics-ioc-runner`.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Report stamped metadata from `ioc-runner -V`. | ✅ | Verified on the prior accepted goldens. |
| T.2 | Run `ioc-runner list -vv` and `ioc-runner inspect -h`. | ✅ | Verified on the prior accepted goldens. |
| T.3 | Provide the source tree from the local source root during `03_epics`. | ✅ | The prior IOC runner deployment verification established the local path. |
| T.4 | Exercise the NFS-side consumer path through tar-push and the consumer suite. | ✅ | The epics-ioc-runner 1.2.0 release gate passed on the accepted goldens. |
| T.5 | Repeat the smoke and lifecycle checks on fresh EPICS-env 1.2.2 goldens. | ✅ | Rocky 8: local 75/75, infrastructure 40/40, system 77/77. Debian 13: local 63/63, infrastructure 41/41, system 77/77; optional local log rotation skipped because `/usr/sbin` was outside the user path. |

## M.6 NFS Simulation

### Deliverable

The `nfs_sim` role provides a loopback NFS export and mount that reproduces
the intended namespace, ownership, permissions, and root-squash boundary on
both supported OS families.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Apply `04_nfs_sim` on Rocky 8. | ✅ | Verified on `testbed-rocky8-iocrunner-server`. |
| T.2 | Apply `04_nfs_sim` on Debian 13. | ✅ | Verified on `testbed-debian13-iocrunner-server`. |
| T.3 | Verify export, mount, ownership, permissions, and service state. | ✅ | Recorded in `docs/STATUS.md`. |
| T.4 | Verify the simulation owner can write and root-owned writes are denied. | ✅ | Recorded root-squash verification passed. |
| T.5 | Keep local IOC runner validation in `03_epics` and NFS-side coverage in the consumer flow. | ✅ | Commit `3ea5c20`; review session `rs20260702_083212` accepted the boundary. |

## M.7 Test Fixtures and Bake Provenance

### Deliverable

The iocrunner golden bake installs the multi-user test fixtures, removes
site-proxy state, and records image and installed-source identities.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Run `07_test_users.yml` after `04_nfs_sim.yml` in the bake. | ✅ | cloud-provision `bake_iocrunner_image.bash` runs it as Step 6/9. |
| T.2 | Verify `opa` and `opb` in `ioc`, `obs` outside it, and linger for `usera` and `userb`. | ✅ | Fresh Rocky 8 and Debian 13 variants passed on 2026-07-05. |
| T.3 | Verify no configured proxy state remains before flattening. | ✅ | The bake fails when its de-proxy scan finds a remnant. |
| T.4 | Write `/etc/iocrunner-bake.manifest` and the image sidecar. | ✅ | In-image and sidecar manifests were verified during Phase C. |
| T.5 | Record repository revisions, version selectors, base-image identity, and `pip3 freeze`. | 🔄 | Implementation committed in `ansible-provision` `6ced253` and `cloud-provision` `c4ba7fd`; preliminary Rocky 8 and Debian 13 bakes passed. Final production bake comparison remains. |
| T.6 | Make a dirty or untagged installed source visibly distinguishable in the manifest. | 🔄 | Manifest state now records `clean-tagged`, `clean-untagged`, or `dirty`; final production bake comparison remains before closing GitHub #6. |

## M.8 Repository Architecture and Operating Documentation

### Deliverable

The documentation describes the public baseline, inventory and overlay
boundaries, role topology, raw-task contract, and standalone workflows without
claiming unverified runtime behavior.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Document public defaults and site override points. | ✅ | `README.md` and `docs/ARCHITECTURE.md`. |
| T.2 | Document all-node and server-only Make target topology. | ✅ | `README.md`, `Makefile`, and `configure/CONFIG_SITE`. |
| T.3 | Document the raw-task contract and no-Python boundary. | ✅ | `docs/RAW_STYLE.md`. |
| T.4 | Document standalone control-host and local-clone modes. | ✅ | `docs/STANDALONE.md`. |
| T.5 | Document the cloud-provision responsibility boundary. | ✅ | `docs/SEAM.md`. |

## M.9 Current Status Synchronization

### Deliverable

The canonical register, verification matrix, architecture description, fixture
document, and linked GitHub issues describe the same current state.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Register GitHub #7, GitHub #8, and commits after 2026-07-05. | ✅ | Recorded in this register and the verification matrix. |
| T.2 | Register playbooks 08 and 09 and their source-build roles. | ✅ | Recorded in the register, architecture, and status documents. |
| T.3 | Replace stale `test_users` activation-pending claims. | ✅ | Updated the README, architecture, seam, and fixture documents. |
| T.4 | Align EPICS-env version documentation with 1.2.2. | ✅ | `docs/ARCHITECTURE.md` and `docs/STATUS.md` now match inventory. |
| T.5 | Run documentation checks and inspect the complete diff. | ✅ | `git diff --check`, Make help output, M/T structure counts, and playbook syntax checks passed. |
| T.6 | Reconcile GitHub #6 and any other linked issue state. | ✅ | GitHub #6 remains open with its current gap documented and is assigned to `Backlog`, `enhancement`, and `jeonghanlee`; GitHub #7 and #8 remain closed. |

## M.10 EtherCAT Verification Transfer

### Deliverable

The repository retains the EtherCAT roles and playbooks while live validation
ownership and acceptance remain in the owner's separate tracker.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Retain `ethercat_base`, `app_ethercat`, and playbooks 05 and 06. | ✅ | Components remain in the repository. |
| T.2 | Record that the first bake and live R2-12 run are not accepted here. | ✅ | `docs/STATUS.md` and `docs/SEAM.md` mark the path unverified. |
| T.3 | Transfer U10 and readiness follow-ups with the work. | ✅ | User direction recorded 2026-07-05 in commit `4a93bc3`. |

## M.11 Version 1.0 Release Convention

### Deliverable

The first repository-family 1.0 release is cut from an accepted consumer
release-gate bake, and the next cycle starts with a fresh version-scoped
register.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Satisfy the agreed 1.0 scope: A, B1, B2, C1, and C3. | ✅ | The scope is recorded as satisfied. |
| T.2 | Run the consumer release-gate bake selected for the tag point. | 🔒 | Requires `G.4`. |
| T.3 | Create matching bare-number tags in the repository family. | 🔒 | User-run release sequence after T.2. |
| T.4 | Preserve the released register and open the next version-scoped register. | 🔒 | Follows T.3. |

## M.12 Review Decisions and Conceptual-Integrity Closure

### Deliverable

Repository-wide review decisions and deliberate keep, replace, retire, or
relocate outcomes remain discoverable after the original review session.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Record the ten-lens repository review outcome. | ✅ | Review session `rs20260702_083212`; convergence `conv20260702_190045`. |
| T.2 | Complete documentation truth synchronization. | ✅ | Phase A commits `2439e6c` and `bde669f`. |
| T.3 | Complete the required raw-task code corrections. | ✅ | Phase B commits `cc8e686`, `13d2910`, `544c487`, and `4623e35`. |
| T.4 | Complete the fixture, de-proxy, and provenance bake work. | ✅ | Phase C commits `9910fe2`, `abe9979`, and cloud-provision `a8bdbd4`. |
| T.5 | Record the EtherCAT transfer. | ✅ | Phase D retired by commit `4a93bc3`. |
| T.6 | Preserve decisions U1-U10. | ✅ | Decisions remain summarized below. |
| T.7 | Preserve all conceptual-integrity finding dispositions. | ✅ | The four finding outcomes remain summarized below. |

## External Gates

| G | Condition | Blocks | Status | Evidence |
| :-- | :-- | :-- | :-- | :-- |
| G.1 | Fresh variants from the 2026-07-28 Rocky 8 and Debian 13 iocrunner goldens | M.1/T.4, M.3/T.3-T.5, M.5/T.5 | Closed | Fresh server variants backed by both current goldens passed the required runtime checks on 2026-07-28. |
| G.2 | Configured Rocky 8, Rocky 10, Ubuntu 24, and Ubuntu 26 EPICS-env build hosts | M.4/T.1, M.4/T.5-T.7 | Closed | Fresh hosts were created and current source-build runs were observed on all four operating systems on 2026-07-28. |
| G.3 | GitHub issue mutation authorization | M.9/T.6 | Closed | Authorization was provided and GitHub #6 was reconciled on 2026-07-28. |
| G.4 | Owner-selected consumer release-gate bake and release authorization | M.11/T.2-T.4 | Open | No repository tag exists as of 2026-07-28. |

## Decisions

| D | Decision | Decided in |
| :-- | :-- | :-- |
| D.1 | `M.x` identifies a deliverable; `T.k` is verification inside that milestone and is not a separate work identifier. | User direction, 2026-07-28 |
| D.2 | Keep `04_nfs_sim` free of `app_ioc_runner`; root-principal in-place validation is incompatible with the root-squash mount. | U7 amendment, commit `3ea5c20` |
| D.3 | Keep EtherCAT roles in this repository and track live acceptance separately. | User direction, 2026-07-05 |
| D.4 | Use GitHub issues for cross-repository or externally referenced work, synchronized after local document review. | U4 plus User direction, 2026-07-28 |
| D.5 | Use bare-number release tags jointly with cloud-provision at an accepted consumer release gate. | U8, 2026-07-03 |

## Conceptual-Integrity Findings

| Finding | Disposition | Durable rule |
| :-- | :-- | :-- |
| Direct CLI examples conflicted with the no-Python contract. | Resolved | Keep public ad-hoc examples on `raw`; do not reintroduce `shell` or `setup`. |
| Pattern targets treated every playbook as valid for every node. | Resolved | Generate server-only targets from `SERVER_NODE_IDS`. |
| IOC runner local and NFS source-root checks were coupled. | Superseded | Keep local checks in `03_epics`; keep NFS-side checks in the consumer flow. |
| NFS paths carried a site namespace. | Resolved | Keep the public default at `simulation`; use site overlays for site names. |

## Previous ID Mapping

| Previous ID or row | Current location |
| :-- | :-- |
| Milestone 1 | M.1 |
| Milestone 2 | M.2 |
| Milestone 3 | M.3 |
| Milestone 4 | M.5 |
| Milestone 5 | M.6 |
| EtherCAT validation rows and Phase D | M.10 |
| `test_users`, Phase C, and provenance rows | M.7 |
| Review phases A and B | M.8 and M.12 |
| U1-U10 decision row | M.12 and Decisions |
| GitHub #7 source-build work | M.4 |
| GitHub #8 Rocky 8 package fix | M.1/T.4 |

## Update Protocol

- Update this register and `docs/STATUS.md` with the substantive change when a
  role, supported OS boundary, version selector, or verification result changes.
- Record only observed verification. A successful syntax check, clean bake, or
  manual package experiment does not replace an unexecuted runtime path.
- Reconcile linked GitHub issue state after local document review and under the
  repository Git workflow authorization rules.
- Preserve the `M.x` deliverable and `T.k` verification distinction.
