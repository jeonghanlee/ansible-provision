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

Validation VMs must be running via `cloud-provision` before executing the
example inventory.

## Makefile Workflow

### Connectivity

```bash
make ping
```

### Provision

```bash
make all                           # site.yml on all nodes
make 01_base                       # base OS on all nodes
make 02_apps                       # con, procServ, conserver on all nodes
make 03_epics                      # EPICS + ioc-runner on ioc nodes
make 04_nfs_sim                    # NFS root_squash simulation on server nodes
```

```bash
make 01_base.rocky8                # OS group
make 01_base.rocky8.server         # single VM
make 04_nfs_sim.rocky8.server      # server-only validation target
```

### Dry Run

```bash
make check                         # connectivity + templating check
make 01_base.rocky8.server.check
```

Raw tasks are skipped in check mode: `check` validates inventory,
reachability, and template rendering only — it does not preview
changes.

### Options

```bash
make 01_base ANSIBLE_TAGS=base ANSIBLE_OPTS=-v
make 02_apps ANSIBLE_LIMIT=rocky8
```

### Configuration

```bash
make vars
make PRINT.INVENTORY
```

---

## Direct CLI Workflow

```bash
ansible all -m raw -a "uptime"
ansible-playbook site.yml
ansible-playbook playbooks/01_base.yml
ansible-playbook playbooks/02_apps.yml
ansible-playbook playbooks/03_epics.yml
```

```bash
ansible-playbook site.yml --limit rocky8
ansible-playbook site.yml --limit testbed-rocky8-server
ansible-playbook site.yml --tags epics
ansible-playbook site.yml -C
```

---

## Inventory

```
inventory/testbed.ini              # Example Rocky 8 + Debian 13 validation inventory
inventory/group_vars/all.yml       # Baseline and validation defaults
inventory/group_vars/rocky8.yml    # Rocky 8 specific (epics_os_dir)
inventory/group_vars/debian13.yml  # Debian 13 specific (epics_os_dir)
```

Override inventory path via:

```bash
echo "INVENTORY=inventory/custom.ini" > configure/CONFIG_SITE.local
```

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
| `test_users` | Multi-user test fixture accounts for the consumer testplan (bake activation pending) | — |
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
| `04_nfs_sim.yml` | `nfs_sim` (ioc-runner validation relocated to the consumer's tar-push + suite flow; see docs/MILESTONES.md) | `nfs_sim_nodes` (server-only, out-of-band, not in `site.yml`) |
| `05_ethercat_base.yml` | `ethercat_base` | `ethercat_build` (out-of-band: invoked by the cloud-provision ethercat bake; no make target) |
| `06_ethercat.yml` | `app_ethercat` | `ethercat_nodes` (out-of-band: run directly with ansible-playbook; no make target) |
| `07_test_users.yml` | `test_users` | `nfs_sim_nodes` (server-only make targets; part of the iocrunner golden bake — see docs/test_users_handoff.md) |
| `08_epics_env_build.yml` | `epics_env_build` | `epics_env_build` (out-of-band: heavy from-source build, not in `site.yml`) |
| `09_epics_env_support_build.yml` | `epics_env_support_build` | `epics_env_build` (out-of-band: layered on 08, not in `site.yml`) |
