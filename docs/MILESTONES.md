# ansible-provision Milestones

> Historical migration source. The current canonical register is
> [docs/milestone-38560eb.md](milestone-38560eb.md). This file is retained to
> preserve the pre-migration register and its historical evidence.

## Scope

This document is the pre-migration work register for `ansible-provision`. It
records project deliverables as `M.x` milestones and the verification required
to close each milestone as `T.k` checks.

**Out of scope:** detailed operating procedures remain in the linked runbooks,
and EtherCAT execution remains in the owner's separate tracker.

Mode: historical source. The canonical register owns current status, plans,
verification, and linked GitHub reconciliation.

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

## Now / Next (2026-08-01)

- In progress: `M.13`. The `ansible-provision` half landed in `75f16c3` and
  `ca2a9de`; the `cloud-provision` half landed on 2026-07-31 and `G.5` is
  Closed. No bake verification has run.
- Completed now: `G.5` closed.
- Ready now: all four `M.13` bake checks — `T.1` and `T.4` need only an
  owner-run bake, and `T.2` and `T.3` are no longer gated.
- External wait: Ubuntu 26 `iocStats` compatibility for `M.4/T.5`, and the
  first release gate (`G.4`).

Next session entry point: run the `M.13` Rocky 8 and Debian 13 bakes. The
unset and nonexistent-selector cases close `T.1` and `T.4`; a bake with
`-r <tag>` closes `T.2` and `T.3` and is the only observation of the join
between the two repositories, which no suite on either side covers.

Tally: 13 milestones - ✅ 10 · 🔒 2 · 🔄 1.

## Milestone Summary

| ID | Deliverable | Type | Status | Evidence or next action |
| :-- | :-- | :-- | :-- | :-- |
| M.1 | Base OS readiness | Milestone | ✅ | The current Rocky 8 golden passed an idempotent base-role re-run and a generated PVXS IOC build. |
| M.2 | Application role reliability | Milestone | ✅ | Both supported OS families passed the application role checks. |
| M.3 | EPICS binary-distribution deployment | Milestone | ✅ | Both fresh variants passed login activation, `caget -h`, and version-path checks. |
| M.4 | EPICS-env source-build environment | Milestone | 🔒 | Rocky 8, Rocky 10, and Ubuntu 24 passed; Ubuntu 26 is blocked by GCC 15 errors in `iocStats`. |
| M.5 | IOC runner deployment | Milestone | ✅ | Both fresh variants passed installed-runner local and system lifecycle suites. |
| M.6 | NFS simulation | Milestone | ✅ | Rocky 8 and Debian 13 passed export, mount, ownership, and root-squash checks. |
| M.7 | Test fixtures and bake provenance | Carry-forward | ✅ | Final production Rocky 8 and Debian 13 IOC runner bakes passed from GitHub `origin/master`; fresh consumers passed manifest and installed-component validation. |
| M.8 | Repository architecture and operating documentation | Carry-forward | ✅ | Public baseline, overlay boundary, playbook topology, and raw-task contract are documented. |
| M.9 | Current status synchronization | Carry-forward | ✅ | Local documents and linked GitHub issue state were reconciled on 2026-07-28. |
| M.10 | EtherCAT verification transfer | Carry-forward | ✅ (retired) | The owner moved live EtherCAT verification to separate tracking on 2026-07-05. |
| M.11 | Version 1.0 release convention | External gate | 🔒 | Wait for the next consumer release-gate bake and User-run tag sequence. |
| M.12 | Review decisions and conceptual-integrity closure | Carry-forward | ✅ | Review outcomes, decisions U1-U10, and finding dispositions are recorded. |
| M.13 | Consumer-selectable ioc-runner version | Milestone | 🔄 | GitHub #9. The selector, the provenance field, and their local suites landed in `75f16c3` and `ca2a9de`; the `cloud-provision` counterpart landed on 2026-07-31, closing `G.5`. Only the bake verifications remain, and all four are now runnable. |

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
| T.5 | Record repository revisions, version selectors, base-image identity, and `pip3 freeze`. | ✅ | Final production Rocky 8 and Debian 13 bakes from GitHub `origin/master` recorded `ansible-provision` `d4f09c2`, `cloud-provision` `b972dc0`, EPICS-env `1.2.2`, EPICS base `7.0.10`, base-image SHA-256 values, and non-empty `pip3` records. |
| T.6 | Make a dirty or untagged installed source visibly distinguishable in the manifest. | ✅ | Fresh `rocky8-iocrunner.server` and `debian13-iocrunner.server` consumers passed `validate_iocrunner_bake.bash`; retained source state records matched installed `ioc-runner -V`. GitHub #6 closed at 2026-07-29 18:35 PDT; the state was observed on 2026-07-30 with `gh issue view 6`. |

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
| T.6 | Reconcile GitHub #6 and any other linked issue state. | ✅ | GitHub #6 is closed, GitHub #7 is open, and GitHub #8 is closed. These states were observed on 2026-07-31 with `gh issue view 6`, `gh issue view 7`, and `gh issue view 8`. |

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

## M.13 Consumer-Selectable IOC Runner Version

### Deliverable

The target state for M.13 is that the `app_ioc_runner` role accepts an
`ioc_runner_version` selector, so a golden image carries a runner the caller
chose rather than whatever the default branch pointed at on the bake date. The
bake manifest records the requested ref beside the resolved commit, keeping the
two distinguishable. Completing this milestone requires coordinated changes in
`ansible-provision` and the `cloud-provision` bake caller and validator; an
Ansible-only change cannot pass the consumer bake validation. Tracked as GitHub
#9; the consuming release-gate work is `epics-ioc-runner` #130.

### Implementation Boundary And Plan

Plan status: the `ansible-provision` half is authorized and implemented. The
`cloud-provision` half was never authorized here and is tracked as `G.5`, now
Closed. Both halves are in place; only the bake verifications remain.

1. In `ansible-provision`, add the optional selector to inventory and make
   `app_ioc_runner` resolve it to one commit before installation. An unset
   selector remains a no-op; an invalid selector fails by name. Landed in
   `75f16c3` and hardened for re-baked hosts by `ca2a9de`.
2. In `ansible-provision`, extend the IOC runner provenance record with the
   requested selector while retaining schema-1 compatibility for existing
   application records. Landed in `75f16c3`.
3. In `cloud-provision`, pass the selector through the bake command and update
   the manifest validator so the requested selector and resolved commit are
   accepted and checked as one record. Landed on 2026-07-31 in
   `cloud-provision` `8ad180a`; `G.5` is Closed.
4. Run the repository recorder and validator tests, then execute the real
   Rocky 8 and Debian 13 bake matrix for unset, released-tag, and nonexistent
   selector cases. Close M.13 only after both repositories and the consumer
   release-gate evidence agree.

The operating constraint recorded here while `G.5` was Open — keep
`ioc_runner_version` empty in real bakes, because the `cloud-provision`
validator rejected the `requested` field — no longer applies and is lifted.
That validator now accepts one optional `requested=<ref>` on `app_ioc_runner`,
and the bake command takes `-r <ref>`. A set selector is the intended path for
`T.2` and `T.3`.

Out of scope: changing the default behavior when the selector is unset,
changing `epics-ioc-runner` itself, or marking any verification complete before
the real bake path runs. A pre-existing laxity in the recorder's manifest
validation, where a field injected before `recorded_at=` is absorbed by the
application-record shape glob, was examined on 2026-07-31 and deferred by owner
decision; it predates this milestone and is unchanged by `75f16c3` and
`ca2a9de`.

### Test Plan

All four checks are runnable now; `T.2` and `T.3` were released when `G.5`
completed on 2026-07-31. They use the `cloud-provision` entry point, which
defaults to a sibling `../ansible-provision` and takes `-a <dir>` when the
checkouts sit elsewhere. `T.2` and `T.3` pass the selector to that entry point
as `-r <ref>` rather than through an inventory edit.

`T.1` runs on both operating systems with `ioc_runner_version` left empty, so
no inventory change is needed:

    bash cloud-provision/bin/bake_iocrunner_image.bash -o rocky8
    bash cloud-provision/bin/bake_iocrunner_image.bash -o debian13

Each bake must pass all ten steps, including the in-image validation at step 8.
Step 9 prints the published manifest sidecar; read the runner record from it:

    awk '$1 == "app_ioc_runner" {print NF - 1}' <sidecar path>

`T.1` passes when that count is 6, the record carries no `requested=` field, and
the four other application records are unchanged.

`T.4` runs on one operating system, because the failure is in the role and is
independent of the target OS. Set `ioc_runner_version` in
`inventory/group_vars/all.yml` to a ref that does not exist, run one bake, and
require that step 4 stops with
`app_ioc_runner: requested ioc_runner_version not found: <ref>`, that no image
is published, and that no fallback to the default branch occurs. Restore the
inventory file afterwards; it is tracked, and the probe value must not be
committed.

A pinned bake was blocked while `G.5` was Open, because the recorder wrote the
`requested` field and the `cloud-provision` validator then rejected it at step
8 for a reason unrelated to the selector. That is resolved: the validator
accepts the field, and the selector is given to the bake command as `-r <ref>`.

| T | Verification | Status | Evidence or completion condition |
| :-- | :-- | :-- | :-- |
| T.1 | Bake with `ioc_runner_version` unset. | ✅ | Rocky 8 and Debian 13 bakes with no selector completed 10/10 on 2026-08-01, host `Neutron`, and each wrote the unchanged six-field record `commit=85b6d904d9a2283833f2c2be274e1567beb47d2e state=clean-untagged tag=-` with no `requested=` field. The default is a no-op. |
| T.2 | Bake with `ioc_runner_version` set to a released tag on both supported OS families, passed as `-r <ref>`. | ✅ | Released by `G.5` on 2026-08-01 and run the same day, host `Neutron`, with `-r 1.2.2` on both families. Fresh consumers booted from the published images report `epics-ioc-runner version 1.2.2 (fd14875)`, and `fd14875df5fdbfcb362d194e81bf74c1de960daa` is the commit `refs/tags/1.2.2` resolves to upstream. Note for future readers: the version string alone does not distinguish a pinned image from an unpinned one, because it reports `1.2.2` in both cases — only the commit differs. |
| T.3 | Read `/etc/iocrunner-bake.manifest` after a pinned bake. | ✅ | The pinned bakes wrote `commit=fd14875df5fdbfcb362d194e81bf74c1de960daa state=clean-tagged tag=1.2.2 requested=1.2.2`. Requested ref and resolved commit are both present and distinguishable, and the in-image manifest matches the published sidecar record on both families. |
| T.4 | Bake with a ref that does not exist. | ✅ | A Debian 13 bake with `-r 9.9.9-nonexistent` failed at step 4 with `app_ioc_runner: requested ioc_runner_version not found: 9.9.9-nonexistent` from `roles/app_ioc_runner/tasks/main.yml:27`. It did not fall back to the default branch, never reached the publish step, and left the previously published golden and its archive entries untouched. Observed 2026-08-01, host `Neutron`. |
| T.5 | Exercise the shipped selector logic against real repositories. | ✅ | `tests/check-ioc-runner-version-selector.bash` extracts the deployed `app_ioc_runner` shell body and runs it against Git fixtures: 22/22 observed on 2026-07-31 at `ca2a9de`. Its earlier 18-check form reported 16/18 against `75f16c3`, isolating exactly the two re-bake defects that `ca2a9de` fixes. |
| T.6 | Exercise the provenance recorder for both record shapes. | ✅ | `tests/check-bake-provenance-recorder.bash`: 35/35 observed on 2026-07-31 at `ca2a9de`, covering the unset six-field record, the selected seven-field record, and the rejected malformed forms. |

## External Gates

| G | Condition | Blocks | Status | Evidence |
| :-- | :-- | :-- | :-- | :-- |
| G.1 | Fresh variants from the 2026-07-28 Rocky 8 and Debian 13 iocrunner goldens | M.1/T.4, M.3/T.3-T.5, M.5/T.5 | Closed | Fresh server variants backed by both current goldens passed the required runtime checks on 2026-07-28. |
| G.2 | Configured Rocky 8, Rocky 10, Ubuntu 24, and Ubuntu 26 EPICS-env build hosts | M.4/T.1, M.4/T.5-T.7 | Closed | Fresh hosts were created and current source-build runs were observed on all four operating systems on 2026-07-28. |
| G.3 | GitHub issue mutation authorization | M.9/T.6 | Closed | Authorization was provided and GitHub #6 was reconciled on 2026-07-28. |
| G.4 | Owner-selected consumer release-gate bake and release authorization | M.11/T.2-T.4 | Open | No repository tag exists as of 2026-07-28. |
| G.5 | `cloud-provision` accepts the `requested` application-record field and passes the selector through the bake command | M.13/T.2-T.3 | Closed | Tracked as cloud-provision#26, filed 2026-07-31 and landed the same day in `8ad180a`. Read against that repository on 2026-08-01: `parse_app_record` at `bin/validate_iocrunner_bake.bash:93-97` accepts one optional `requested=<ref>` on `app_ioc_runner` only, checked for shape and not tied to `tag` or `state`; `bin/bake_iocrunner_image.bash:346` takes `-r <ref>` and `:536` passes `-e ioc_runner_version=` to `site.yml` alone, while the calls at `:538`, `:545`, and `:551` pass only `-i` and `--limit`. Its suite reports 43/43. The earlier reading recorded here — extra fields rejected, no invocation passing a selector — described the state before `8ad180a` and was left in place after it landed. The gate covers the interface only: that a pinned bake yields an image whose `ioc-runner -V` reports the requested commit is observed by `T.2` and `T.3`, not here, because the fake `ansible-playbook` in the `cloud-provision` suite records the argument and stops. |

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
