# ansible-provision Verification Status

## Scope

This document records observed role-by-OS and source-build verification.
`docs/MILESTONES.md` defines deliverables and the `T.k` checks required to
close them.

**Out of scope:** architecture and data flow are defined in
`docs/ARCHITECTURE.md`; deferred work is indexed through the milestone
register.

**Last updated:** 2026-07-28

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
| `base_os` | `01_base` | ? | ✓ |
| `app_con` | `02_apps` | ✓ | ✓ |
| `app_procserv` | `02_apps` | ✓ | ✓ |
| `app_conserver` | `02_apps` | ✓ | ✓ |
| `app_epics` | `03_epics` | ? | ? |
| `app_ioc_runner` | `03_epics` | ? | ? |
| `nfs_sim` | `04_nfs_sim` | ✓ | ✓ |
| `test_users` | `07_test_users` | ✓ | ✓ |

### Current-Golden Boundary

Commit `1efca35` records successful Rocky 8 and Debian 13 iocrunner golden
bakes with EPICS-env 1.2.2 on 2026-07-28. The bake proves that the selected
distribution path exists and that the provisioning stack completes. It does
not replace the independent login-shell, EPICS command, IOC runner, or
generated-IOC checks in `M.1`, `M.3`, and `M.5`; the affected current-image
cells therefore remain `?`.

Rocky 8 includes `libevent-devel` after `026f859`. Installing that package on
the prior running golden changed the same generated IOC from link failure to
pass, but the complete role-to-current-golden-to-generated-IOC path has not
been observed in one run.

## EPICS-env Source-Build Matrix

| Host OS | `epics_env_build` | `epics_env_support_build` | Evidence |
| :-- | :-: | :-: | :-- |
| Rocky 8 | ? | — | Commit `9dfd5a1` verified the initial path; the current vendor-install rewrite has not run on Rocky 8. |
| Debian 13 | ✓ | ✓ | Commits `9dfd5a1` and `0148514`: layered tree built; `check_deps` exit 0. |
| Rocky 10 | — | — | Inventory entry only. |
| Ubuntu 24 | — | — | Inventory entry only. |
| Ubuntu 26 | — | — | Inventory entry only. |

| Build property | Status | Evidence |
| :-- | :-: | :-- |
| Vendor libraries installed inside the release tree | ✓ | Commit `5c4f7fc`; absolute-path dependency findings reduced from 9 to 0. |
| `internal` flavor | ✓ | Used by the recorded core-host builds. |
| `gz` flavor | — | Code path added by `1732f77`; no observed run recorded. |
| Base-layer repeated-run skip | ✓ | Commit `9dfd5a1`. |
| Support-layer repeated-run skip | — | No observed repeated run recorded after `0148514`. |

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
| `M.1/T.1`, `M.1/T.4` | Re-run `01_base` and build a generated PVXS IOC on the current Rocky 8 golden. |
| `M.3/T.3-T.5` | Source the login environment, run `caget -h`, and verify version paths on both current goldens. |
| `M.4/T.1`, `M.4/T.5-T.7` | Run the current Rocky 8 path, additional build hosts, `gz` flavor, and support-layer repeated-run check. |
| `M.5/T.5` | Run IOC runner smoke and consumer lifecycle checks on both current goldens. |

## Update Protocol

Update this matrix and `docs/MILESTONES.md` with the substantive change when a
role, supported OS boundary, version selector, or observed verification result
changes. Record a pass only when the real shipped path and fixtures ran.
