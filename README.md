# ansible-provision

Ansible provisioning for the image operator model defined in cloud-provision
`docs/IMAGE_WORKFLOW.md` (Operator definition): five vacua (debian13, rocky8,
rocky10, ubuntu24, ubuntu26), one role per operator, one playbook per
operator, and one assembly playbook per species.

* First-pass VM source of truth: [cloud-provision](https://github.com/jeonghanlee/cloud-provision)
* EPICS environment: [EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution)

This repository does not own VM lifecycle, site network identity, internal
package mirrors, proxy policy, or production deployment secrets. Site-specific
values belong in inventory or `configure/CONFIG_SITE.local` overlays; the
full override contract (which value goes in which plane) is in
`docs/ARCHITECTURE.md` section 7. Baking behind a site proxy is a
cloud-provision procedure: see `cloud-provision/docs/RUNBOOK_BAKE.md`.

Trust posture: `ansible.cfg` disables host-key checking and assumes
passwordless become on the lab NAT. Do not point this configuration
at non-lab hosts as-is.

## Prerequisites

Install ansible-core on the control host:

```bash
make setup
```

Provisioning targets must be running via `cloud-provision`. The maintained
`inventory/lab.ini` contains group relationships and no host rows;
`cloud-provision/bin/generate_ansible_inventory.bash` supplies the actual VM
name, resolved address, and groups as a second inventory source.

## Makefile Workflow

Set `RUNTIME_INVENTORY` to a generated host inventory before running a target.
Set `ANSIBLE_LIMIT` to the generated VM name when a target must select an
arbitrary run-specific name.

### Connectivity

```bash
make ping RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

### Provision a species

```bash
make bare.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make iocrunner.debian13 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make iocrunner_nfs.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make epics_dev.ubuntu24 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini ANSIBLE_LIMIT=actual-vm-name
```

### Run one operator

```bash
make op.common.rocky10 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make op.nfs_sim.debian13 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

### Dry Run

```bash
make bare.rocky8.check RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

Raw tasks are skipped in check mode: `check` validates inventory,
reachability, and template rendering only - it does not preview changes.

### Configuration

```bash
make vars
make PRINT.INVENTORY
```

---

## Direct CLI Workflow

```bash
ansible all -i inventory/lab.ini -i /tmp/cloud-provision-host.ini -m raw -a "uptime"
ansible-playbook -i inventory/lab.ini -i /tmp/cloud-provision-host.ini playbooks/species/bare.yml
ansible-playbook -i inventory/lab.ini -i /tmp/cloud-provision-host.ini playbooks/species/iocrunner.yml --limit debian13
ansible-playbook -i inventory/lab.ini -i /tmp/cloud-provision-host.ini playbooks/operators/common.yml --limit actual-vm-name
```

---

## Inventory

```
inventory/lab.ini                  # Host-free lab group relationships (vacua and species)
inventory/group_vars/all.yml       # Values shared by more than one operator
inventory/group_vars/<vacuum>.yml  # Per-vacuum values (epics_os_dir, python overrides)
```

Supply a generated host inventory to Make without replacing the maintained
group relationships:

```bash
make bare.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

`INVENTORY` remains overridable for a site-owned complete inventory.

Standalone (non-lab) VMs: see [docs/STANDALONE.md](docs/STANDALONE.md).

---

## Operators

One role per operator; each role's `defaults/` owns the values only it
consumes. The operator definition in cloud-provision `docs/IMAGE_WORKFLOW.md`
is the normative statement of content and order.

| Operator | Role | Source |
|---|---|---|
| P_common | `common` | OS package manager |
| P_rt | `rt` | Debian PREEMPT_RT packages |
| P_provenance | `provenance` | - |
| P_epics | `epics` | [jeonghanlee/EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution) |
| P_epics-build | `epics_build` | [jeonghanlee/EPICS-env](https://github.com/jeonghanlee/EPICS-env) |
| P_epics-support | `epics_support` | [jeonghanlee/EPICS-env-support](https://github.com/jeonghanlee/EPICS-env-support) |
| P_procserv | `procserv` | [jeonghanlee/procServ-env](https://github.com/jeonghanlee/procServ-env) |
| P_conserver | `conserver` | [jeonghanlee/conserver-env](https://github.com/jeonghanlee/conserver-env) |
| P_con | `con` | [jeonghanlee/con](https://github.com/jeonghanlee/con) |
| P_nfs-sim | `nfs_sim` | - |
| P_iocrunner | `iocrunner` | [jeonghanlee/epics-ioc-runner](https://github.com/jeonghanlee/epics-ioc-runner) |
| P_testusers | `testusers` | - |
| P_ethercat | `ethercat` | [jeonghanlee/ethercat-env](https://github.com/jeonghanlee/ethercat-env) (bundle) |

## Species Assemblies

| Assembly | Product |
|---|---|
| `species/bare.yml` | P_common |
| `species/iocrunner.yml` | P_testusers P_iocrunner (P_con P_conserver P_procserv) P_epics P_provenance on bare |
| `species/iocrunner_nfs.yml` | P_nfs-sim on iocrunner |
| `species/epics_dev.yml` | P_epics-support P_epics-build on bare |
| `species/nfs_sim.yml` | P_nfs-sim on bare |
| `species/rtbase.yml` | P_rt on bare |
| `species/ethercat.yml` | P_ethercat on the rtbase golden |
