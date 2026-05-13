# ansible-provision Milestones

## Scope

This document defines the implementation milestones required to bring
the provisioning stack from partial role verification to full
cross-OS validation.

**Out of scope:** Current pass/fail state is tracked in `docs/STATUS.md`.
Deferred feature requests that are not required for the provisioning
baseline are tracked in `TODO.md`.

## Completion Model

The project is complete when all supported role and OS combinations in
`docs/STATUS.md` are verified end-to-end, known broken paths are fixed,
and the generated VMs provide the command-line tools required by the IOC
runtime workflows.

Each milestone closes only when its acceptance criteria pass on the real
testbed. Syntax checks alone are necessary but not sufficient.

## Milestone 1: Base OS Parity

### Objective

Establish a reliable base OS layer for Rocky 8 and Debian 13.

### Acceptance Criteria

- `01_base` applies successfully on Rocky 8 and Debian 13 hosts.
- Required operator and runtime tools are present after provisioning:
  `git`, `make`, `lsof`, `ss`, and `socat`.
- NTP service is installed, configured, enabled, and running.
- A second run is idempotent at the provisioning contract level.

### Verification

```bash
make 01_base.rocky8.server.check
make 01_base.debian13.server.check
make 01_base.rocky8.server
make 01_base.debian13.server
```

Post-apply verification:

```bash
ansible rocky8 -i inventory/testbed.ini -m raw -a "command -v lsof ss socat"
ansible debian13 -i inventory/testbed.ini -m raw -a "command -v lsof ss socat"
```

## Milestone 2: Application Role Reliability

### Objective

Make the application build roles fail visibly and verify their installed
artifacts.

### Acceptance Criteria

- `app_con`, `app_procserv`, and `app_conserver` fail on build or
  install errors instead of reporting ok after a partial failure.
- `con`, `procServ`, and `conserver` binaries are installed at the
  expected paths.
- The Rocky 8 `app_conserver` missing-binary defect is resolved.
- Debian 13 application roles are applied and independently verified.

### Verification

```bash
make 02_apps.rocky8.server.check
make 02_apps.debian13.server.check
make 02_apps.rocky8.server
make 02_apps.debian13.server
```

Post-apply verification:

```bash
ansible all -i inventory/testbed.ini -m raw -a "command -v con procServ conserver"
```

## Milestone 3: EPICS Environment Deployment

### Objective

Install and validate the EPICS runtime environment on both supported OS
families.

### Acceptance Criteria

- `03_epics` applies successfully on Rocky 8 and Debian 13 hosts.
- `epics_os_dir` resolves to an upstream-supported directory on each OS.
- `/etc/profile.d/epics-env.sh` sources successfully at login.
- EPICS base version and environment version match inventory selectors.
- Required EPICS commands are available in a login shell.

### Verification

```bash
make 03_epics.rocky8.server.check
make 03_epics.debian13.server.check
make 03_epics.rocky8.server
make 03_epics.debian13.server
```

Post-apply verification:

```bash
ansible all -i inventory/testbed.ini -m raw -a "bash -lc 'source /etc/profile.d/epics-env.sh && caget -h'"
```

## Milestone 4: IOC Runner Deployment

### Objective

Provision IOC runner hosts with the runtime, source tree, and inspection
dependencies required by `epics-ioc-runner`.

### Acceptance Criteria

- `ioc-runner` is installed at the expected path.
- `ioc-runner -V` reports stamped build metadata, not `unreleased`.
- The `epics-ioc-runner` source tree is available in the intended
  NFS-backed home location for iocrunner VMs.
- `ioc-runner inspect` returns complete output, including socket and
  client PID information.
- Lifecycle tests that depend on inspect pass their assertions.

### Verification

```bash
make 03_epics.rocky8.server
make 03_epics.debian13.server
```

Post-apply verification:

```bash
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner -V"
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner inspect"
```

## Milestone 5: NFS Simulation and Cross-OS Closure

### Objective

Validate the NFS simulation role and close the role-by-OS matrix.

### Acceptance Criteria

- `04_nfs_sim` applies successfully on the configured NFS simulation
  hosts.
- Export paths, ownership, permissions, and service state match the
  documented architecture.
- Rocky 8 and Debian 13 both complete `01_base`, `02_apps`, `03_epics`,
  and `04_nfs_sim`.
- `docs/STATUS.md` has no unverified, broken, or not-yet-applied
  entries for supported role and OS combinations.
- Open items in `docs/STATUS.md` are either resolved or moved to
  `TODO.md` as explicitly deferred work.

### Verification

```bash
make 04_nfs_sim.rocky8.server.check
make 04_nfs_sim.debian13.server.check
make 04_nfs_sim.rocky8.server
make 04_nfs_sim.debian13.server
make check
```

## Update Protocol

When a milestone is completed, update this document and `docs/STATUS.md`
in the same commit as the substantive change. The commit message should
name the milestone and the role or OS boundary that changed.
