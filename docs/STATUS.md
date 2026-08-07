# ansible-provision Verification Status

## Scope

This document records observed role-by-OS and source-build verification.
`docs/milestone-a519802.md` defines deliverables and the `T.k` checks required
to close them.

**Out of scope:** architecture and data flow are defined in
`docs/ARCHITECTURE.md`; deferred work is indexed through the milestone
register.

**Last updated:** 2026-08-06

## Status Legend

| Symbol | Meaning |
| :-- | :-- |
| ✓ | Applied and independently verified. |
| ? | Applied, but the current result has not been independently verified. |
| ✗ | Observed broken; the note names the failure. |
| — | Not applied on this OS or host. |

## Provisioning Role x OS Matrix

| Role | Playbook | Rocky 8 | Debian 13 |
| :-- | :-- | :-: | :-: |
| `base_os` | `01_base` | ✓ | ✓ |
| `app_con` | `02_apps` | ✓ | ✓ |
| `app_procserv` | `02_apps` | ✓ | ✓ |
| `app_conserver` | `02_apps` | ✓ | ✓ |
| `app_epics` | `03_epics` | ✓ | ✓ |
| `app_ioc_runner` | `03_epics` | ✓ | ✓ |
| `nfs_sim` | `04_nfs_sim` | ✓ | ✓ |
| `test_users` | `07_test_users` | ✓ | ✓ |

### Current-Golden Boundary

Fresh Rocky 8 and Debian 13 server variants backed by the 2026-07-28
iocrunner goldens passed the current-image checks:

- Rocky 8 `01_base` repeated with `changed=0` and `failed=0`.
- Both login activation scripts selected EPICS-env 1.2.2, the correct OS
  directory, and EPICS Base 7.0.10; `caget -h` returned success.
- ServiceTestIOC commit `91d42b2` declared `pvxsIoc pvxs` and built
  successfully on Rocky 8, closing the role-to-golden link check for
  `libevent-devel`.
- The installed IOC runner passed local and system lifecycle suites on both
  operating systems. Debian 13 local log-rotation steps were optional and
  skipped because `/usr/sbin` was outside the unprivileged user path.

The provenance correction has landed in pushed commits `ansible-provision`
`6ced253` and `cloud-provision` `c4ba7fd`; documentation follow-up commits
`ansible-provision` `d4f09c2` and `cloud-provision` `b972dc0` were the GitHub
`origin/master` baseline for final acceptance. Production Rocky 8 and Debian 13
IOC runner bakes passed, fresh consumers booted, VM manifests matched the
sidecar manifests by SHA-256, and both consumers passed
`validate_iocrunner_bake.bash`.

## EPICS-env Source-Build Matrix

| Host OS | `epics_env_build` | `epics_env_support_build` | Evidence |
| :-- | :-: | :-: | :-- |
| Rocky 8 | ✓ | ✓ | Fresh internal-flavor layers produced 64 entries; runtime gates and `check_deps.bash` passed, and both role re-runs reported `changed=0`. |
| Debian 13 | ✓ | ✓ | Commits `9dfd5a1` and `0148514`: layered tree built; `check_deps` exit 0. |
| Rocky 10 | ✓ | ✓ | Fresh `gz` layers produced 64 entries; all runtime gates and `check_deps.bash` passed. |
| Ubuntu 24 | ✓ | ✓ | Fresh `gz` layers produced 64 entries; all runtime gates and `check_deps.bash` passed. |
| Ubuntu 26 | ✗ | — | On 2026-07-28, `08_epics_env_build.yml` with `epics_env_build_flavor=gz` exited 2: GCC 15 rejected incompatible function pointers in `iocStats` `devIocStatsAnalog.c`. |

| Build property | Status | Evidence |
| :-- | :-: | :-- |
| Vendor libraries installed inside the release tree | ✓ | Commit `5c4f7fc`; absolute-path dependency findings reduced from 9 to 0. |
| `internal` flavor | ✓ | Used by the recorded core-host builds. |
| `gz` flavor | ✓ | Rocky 10 and Ubuntu 24 passed both source-build roles with installed `-g0 -gz=zlib` flags. |
| Base-layer repeated-run skip | ✓ | Commit `9dfd5a1`. |
| Support-layer repeated-run skip | ✓ | Rocky 8 emitted `EPICS_ENV_SUPPORT_BUILD_SKIPPED` with `changed=0` and `failed=0`. |

The Rocky 10 and Ubuntu 24 `gz` scans found `.debug_info` only in
`MCoreUtils-1.2.3/lib/linux-x86_64/libmcoreutils.so`. This is informational
under the verification policy and did not change the gate results.

## NFS Simulation Evidence

`04_nfs_sim` passed on the Rocky 8 and Debian 13 iocrunner server validation
hosts. The verification covered the `simulation` namespace, export and mount
state, ownership and permissions, regular-user writes, and denial of
root-owned writes through `root_squash`.

IOC runner validation no longer runs as root inside the 0750 NFS mount.
Commit `3ea5c20` keeps local source-root checks in `03_epics`; the consumer's
tar-push and suite flow owns NFS-side coverage.

## Test Fixture Evidence

Fresh Rocky 8 and Debian 13 variants from the 2026-07-05 goldens verified:

- `opa` and `opb` belong to `ioc`.
- `obs` does not belong to `ioc`.
- `usera` and `userb` have systemd linger enabled.
- The fixture survives a clean reprovision from each golden.

## IOC Runner Version Selector

The optional `ioc_runner_version` inventory selector is implemented in
`app_ioc_runner`, and the provenance record carries the requested ref beside
the resolved commit. The two local suites were rerun on 2026-08-06 at
repository `0082a56`:

- `tests/check-ioc-runner-version-selector.bash`: 22/22. The suite extracts the
  deployed role shell body and runs it against Git fixtures, covering the unset
  no-op, tag, branch, and commit selection, tag precedence over a same-named
  branch, and by-name failure for an unknown ref, a ref deleted upstream, an
  unreadable HEAD, and a cleared selector on an already-pinned checkout.
- `tests/check-bake-provenance-recorder.bash`: 35/35, covering the unset
  six-field application record, the selected seven-field record, and the
  rejected malformed forms.

Rocky 8 and Debian 13 bakes with an unset selector, a released tag, and a
nonexistent selector were observed on 2026-08-01. The unset and pinned bakes
completed 10/10; the pinned manifests carried `requested=1.2.2` beside the
resolved `fd14875...` commit; the nonexistent selector failed before publish.
`cloud-provision` accepts the `requested` field and takes `-r <ref>` as of
`8ad180a`; the selector work is complete and remains reachable from prior
state commit `a519802`. It is not active work in this reset generation.

## EtherCAT Validation

EtherCAT is a separate Debian 13 bake and live-VM validation path.

| Component | Playbook | Host group | Status |
| :-- | :-- | :-- | :-: |
| `ethercat_base` | `05_ethercat_base` | `ethercat_build` | — |
| `app_ethercat` | `06_ethercat` | `ethercat_nodes` | — |

The roles and playbooks are present. No accepted end-to-end bake and live
R2-12 result is recorded in this repository.

## Open Verification

| Milestone checks | Required observation |
| :-- | :-- |
| `M1/T5`, `G2` | Resolve the Ubuntu 26 `iocStats` GCC 15 compatibility condition, then run layer 2 and all verification gates. |

## Update Protocol

Update this matrix and `docs/milestone-a519802.md` with the substantive change when a
role, supported OS boundary, version selector, or observed verification result
changes. Record a pass only when the real shipped path and fixtures ran.
