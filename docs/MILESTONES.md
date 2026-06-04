# ansible-provision Milestones

## Scope

This document is the canonical work register for `ansible-provision`.
It consolidates implementation milestones, carry-forward work, external
gates, and conceptual-integrity findings that need owner decisions.

Supporting evidence remains in `docs/STATUS.md` and `TODO.md`; those
documents are not competing status registers.

Next session entry point: final review and commit preparation after V7
closure.

## Completion Model

The project is complete when all supported role and OS combinations in
`docs/STATUS.md` are verified end-to-end, known broken paths are fixed,
and the generated VMs provide the command-line tools required by the IOC
runtime workflows.

Each milestone closes only when its acceptance criteria pass on the real
testbed. Syntax checks alone are necessary but not sufficient.

## Work Register

| Topic | Work unit | Type | Status | Evidence or next action |
|---|---|---|---|---|
| Base OS | Milestone 1: Base OS parity | Milestone | Complete | `docs/STATUS.md` marks `base_os` verified on Rocky 8 and Debian 13. |
| Applications | Milestone 2: Application role reliability | Milestone | Complete | `docs/STATUS.md` marks `app_con`, `app_procserv`, and `app_conserver` verified on both OS families. |
| EPICS | Milestone 3: EPICS environment deployment | Milestone | Complete | `docs/STATUS.md` marks `app_epics` verified on both OS families. |
| IOC runner | Milestone 4: IOC runner deployment | Milestone | Complete | `docs/STATUS.md` marks `app_ioc_runner` verified on both OS families. |
| NFS simulation | Milestone 5: NFS simulation and cross-OS closure | Milestone | Complete | `docs/STATUS.md` marks `nfs_sim` verified on Rocky 8 and Debian 13 ioc-runner server validation hosts. |
| Repository identity | Public baseline and validation boundary | Design gate | Implemented | README and architecture describe a public Linux baseline, validation defaults, testbed defaults, and site overlays. |
| Makefile topology | Server-only NFS simulation targets | Design gate | Implemented | `04_nfs_sim` node targets are generated only for configured server node IDs. |
| Host setup | SSH key existence check | Carry-forward | Open | `TODO.md` tracks a warning for missing `~/.ssh/id_ed25519.pub` or `~/.ssh/id_rsa.pub` in `bin/setup_host.bash`. |

## Conceptual Integrity Findings

| Finding | Reality rank | Evidence | Fate to decide |
|---|---|---|---|
| Direct CLI examples disagree with the repository's no-Python operational contract. | Latent but reachable | `docs/ANSIBLE_CLI.md:50`, `docs/ANSIBLE_CLI.md:53`, `docs/ANSIBLE_CLI.md:56`, and `docs/ANSIBLE_CLI.md:59` use `shell` or `setup`; `playbooks/01_base.yml:5`, `playbooks/02_apps.yml:5`, and `playbooks/03_epics.yml:5` set `gather_facts: false`. | Replace the `shell` and `setup` examples with `raw`, or explicitly label them as post-bootstrap Python-dependent commands. |
| Pattern targets treat every playbook as valid for every OS and node, but `04_nfs_sim.yml` is scoped only to `nfs_sim_nodes`. | Resolved in design | `configure/CONFIG_SITE` now separates all-node and server-only playbooks; `configure/RULES_ANSIBLE` generates server-only node targets only from `SERVER_NODE_IDS`. | Verify `make help.detail` and confirm unsupported `04_nfs_sim.<os>.node1` targets are no longer generated. |
| `app_ioc_runner` and `nfs_sim` need separate local and NFS source-root coverage. | Already decided | `inventory/group_vars/all.yml` keeps the default local `path_ioc_runner_root`; `playbooks/04_nfs_sim.yml` overrides `path_ioc_runner_root` and `path_ioc_runner_src` for the NFS simulation path and enables `ioc_runner_force_setup`; `roles/nfs_sim/defaults/main.yml` keeps the simulation symlink separate from the local testbed source root. | Keep this split and verify both `03_epics` local coverage and `04_nfs_sim` NFS coverage on the testbed. |
| NFS simulation paths carried a site-specific namespace. | Resolved in defaults | `roles/nfs_sim/defaults/main.yml` uses `nfs_sim_namespace: simulation` to build export and mount roots. | Keep site namespaces in overlays, not public defaults. |

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
- The `epics-ioc-runner` source tree is available from the local source
  root during `03_epics`.
- The `epics-ioc-runner` source tree is available from the NFS-backed
  simulation source root during `04_nfs_sim`.
- `ioc-runner list -vv` and `ioc-runner inspect -h` run successfully.
- Target-specific `ioc-runner inspect <ioc>` is covered by lifecycle
  tests that create or install an IOC target.
- Lifecycle tests that depend on inspect pass their assertions.

### Verification

```bash
make 03_epics.rocky8.server
make 03_epics.debian13.server
```

Post-apply verification:

```bash
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner -V"
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner list -vv"
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner inspect -h"
```

## Milestone 5: NFS Simulation and Cross-OS Closure

### Objective

Validate the NFS simulation role and close the role-by-OS matrix.

### Acceptance Criteria

- `04_nfs_sim` applies successfully on the configured NFS simulation
  hosts.
- Export paths, ownership, permissions, and service state match the
  documented architecture.
- `app_ioc_runner` applies successfully from the NFS-backed simulation
  source root without replacing the local source root.
- Rocky 8 and Debian 13 both complete `01_base`, `02_apps`, `03_epics`,
  and `04_nfs_sim`.
- `docs/STATUS.md` has no unverified, broken, or not-yet-applied
  entries for supported role and OS combinations.
- Open items in `docs/STATUS.md` are either resolved or moved to
  `TODO.md` as explicitly deferred work.

### Verification

Default-inventory target topology:

```bash
make 04_nfs_sim.rocky8.server.check
make 04_nfs_sim.debian13.server.check
make 04_nfs_sim.rocky8.server
make 04_nfs_sim.debian13.server
make check
```

V7 completion evidence used the NFS/ioc-runner validation hosts from a
temporary inventory:

```bash
ANSIBLE_LOCAL_TEMP=/tmp/ansible-local ANSIBLE_SSH_CONTROL_PATH_DIR=/tmp/ansible-cp ansible-playbook -i /tmp/ansible-provision-nfs-v7.ini -e @inventory/group_vars/all.yml playbooks/04_nfs_sim.yml
```

Validated hosts:

| OS | Host | Address |
|---|---|---|
| Rocky 8 | `testbed-rocky8-iocrunner-server` | `192.168.122.150` |
| Debian 13 | `testbed-debian13-iocrunner-server` | `192.168.122.50` |

### Status

Complete for Rocky 8 and Debian 13 ioc-runner server validation hosts.
The NFS simulation uses the `simulation` namespace, keeps the local source
root separate from `gitsrc-nfs-sim`, and verifies root_squash behavior.

## Update Protocol

When a milestone is completed, update this document and `docs/STATUS.md`
in the same commit as the substantive change. The commit message should
name the milestone and the role or OS boundary that changed.
