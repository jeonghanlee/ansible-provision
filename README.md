# ansible-provision

Ansible baseline for unifying Linux systems across Rocky 8 and Debian 13.
The baseline installs common operating-system services and validates EPICS
operations through con, procServ, conserver, EPICS, ioc-runner, and an
NFS root_squash simulation.

* First-pass VM source of truth: [cloud-provision](https://github.com/jeonghanlee/cloud-provision)
* EPICS environment: [EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution)

This repository does not own VM lifecycle, site network identity, internal
package mirrors, proxy policy, or production deployment secrets. Site-specific
values belong in inventory or `configure/CONFIG_SITE.local` overlays; the
full override contract (which value goes in which plane) is in
`docs/ARCHITECTURE.md` section 7. Baking behind a site proxy is a
cloud-provision procedure: see `cloud-provision/docs/RUNBOOK_BAKE.md`.

Trust posture: `ansible.cfg` disables host-key checking and assumes
passwordless become on the testbed NAT. Do not point this configuration
at non-testbed hosts as-is.

## Prerequisites

Install ansible-core on the control host:

```bash
make setup
```

Validation VMs must be running via `cloud-provision`. The maintained
`inventory/testbed.ini` contains group relationships and no host rows;
`cloud-provision/bin/generate_ansible_inventory.bash` supplies the actual VM
name, resolved address, and workload group as a second inventory source.

From the cloud-provision checkout, generate one ordinary Rocky 8 server entry:

```bash
bin/create_vm.bash -o rocky8 -n server -s | bin/generate_ansible_inventory.bash --status-input --os-type rocky8 --role nfs-sim-node > /tmp/cloud-provision-host.ini
```

## Makefile Workflow

Set `RUNTIME_INVENTORY` to a generated host inventory before running a target.
Set `ANSIBLE_LIMIT` to the generated VM name when a per-node target must select
an arbitrary prefix or run-specific name.

### Connectivity

```bash
make ping RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

### Provision

```bash
make all RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make 01_base RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make 02_apps RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make 03_epics RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make 04_nfs_sim RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

```bash
make 01_base.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make 01_base.rocky8.server RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini ANSIBLE_LIMIT=actual-vm-name
make 04_nfs_sim.rocky8.server RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini ANSIBLE_LIMIT=actual-vm-name
```

### Dry Run

```bash
make check RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make 01_base.rocky8.server.check RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini ANSIBLE_LIMIT=actual-vm-name
```

Raw tasks are skipped in check mode: `check` validates inventory,
reachability, and template rendering only — it does not preview
changes.

### Options

```bash
make 01_base RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini ANSIBLE_TAGS=base ANSIBLE_OPTS=-v
make 02_apps RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini ANSIBLE_LIMIT=rocky8
```

### Configuration

```bash
make vars
make PRINT.INVENTORY
```

---

## Direct CLI Workflow

```bash
ansible all -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini -m raw -a "uptime"
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini site.yml
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini playbooks/01_base.yml
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini playbooks/02_apps.yml
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini playbooks/03_epics.yml
```

```bash
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini site.yml --limit rocky8
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini site.yml --limit actual-vm-name
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini site.yml --tags epics
ansible-playbook -i inventory/testbed.ini -i /tmp/cloud-provision-host.ini site.yml -C
```

---

## Inventory

```
inventory/testbed.ini              # Host-free testbed group relationships
inventory/group_vars/all.yml       # Baseline and validation defaults
inventory/group_vars/rocky8.yml    # Rocky 8 specific (epics_os_dir)
inventory/group_vars/debian13.yml  # Debian 13 specific (epics_os_dir)
```

Supply a generated host inventory to Make without replacing the maintained
group relationships:

```bash
make 01_base RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

`INVENTORY` remains overridable for a site-owned complete inventory.

Standalone (non-testbed) VMs: see
[docs/STANDALONE.md](docs/STANDALONE.md) for the control-host-over-ssh
and local-clone recipes.

---

## Roles

| Role | Description | Source |
|---|---|---|
| `base_os` | Base packages, chrony NTP | OS package manager |
| `app_con` | con console utility | [jeonghanlee/con](https://github.com/jeonghanlee/con) |
| `app_procserv` | procServ process manager | [jeonghanlee/procServ-env](https://github.com/jeonghanlee/procServ-env) |
| `app_conserver` | conserver serial console server | [jeonghanlee/conserver-env](https://github.com/jeonghanlee/conserver-env) |
| `app_epics` | EPICS binary distribution | [jeonghanlee/EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution) |
| `app_ioc_runner` | epics-ioc-runner infrastructure | [jeonghanlee/epics-ioc-runner](https://github.com/jeonghanlee/epics-ioc-runner) |
| `nfs_sim` | NFS root_squash simulation (loopback export + remount) | — |
| `test_users` | Multi-user test fixture accounts applied during the iocrunner golden bake | - |
| `ethercat_base` | EtherCAT/RT bake-time prerequisite layer (Debian 13 rtbase) | — |
| `app_ethercat` | EtherCAT R2-12 live validation harness | [jeonghanlee/ethercat-env](https://github.com/jeonghanlee/ethercat-env) (bundle) |
| `epics_env_build` | EPICS-env built from source (base + all modules incl. asyn) | [jeonghanlee/EPICS-env](https://github.com/jeonghanlee/EPICS-env) |
| `epics_env_support_build` | EPICS-env-support AreaDetector modules, layered on the epics_env_build install | [jeonghanlee/EPICS-env-support](https://github.com/jeonghanlee/EPICS-env-support) |

## Playbook Layers

| Playbook | Roles | Hosts |
|---|---|---|
| `01_base.yml` | `base_os` | all nodes |
| `02_apps.yml` | `app_con`, `app_procserv`, `app_conserver` | all nodes |
| `03_epics.yml` | `app_epics`, `app_ioc_runner` | ioc nodes |
| `04_nfs_sim.yml` | `nfs_sim` (ioc-runner validation relocated to the consumer's tar-push + suite flow; see docs/milestone-a519802.md) | `nfs_sim_nodes` (server-only, out-of-band, not in `site.yml`) |
| `05_ethercat_base.yml` | `ethercat_base` | `ethercat_build` (out-of-band: invoked by the cloud-provision ethercat bake; no make target) |
| `06_ethercat.yml` | `app_ethercat` | `ethercat_nodes` (out-of-band: run directly with ansible-playbook; no make target) |
| `07_test_users.yml` | `test_users` | `nfs_sim_nodes` (server-only make targets; part of the iocrunner golden bake — see docs/test_users_handoff.md) |
| `08_epics_env_build.yml` | `epics_env_build` | `epics_env_build` (out-of-band: heavy from-source build, not in `site.yml`) |
| `09_epics_env_support_build.yml` | `epics_env_support_build` | `epics_env_build` (out-of-band: layered on 08, not in `site.yml`) |
