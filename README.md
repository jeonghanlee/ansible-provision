# ansible-provision

Ansible-based provisioner for cloud-provision testbed VMs.
Deploys con, procServ, conserver, EPICS, and ioc-runner on Rocky 8 and Debian 13.

* Testbed VM provisioner: [cloud-provision](https://github.com/jeonghanlee/cloud-provision)
* EPICS environment: [EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution)

## Prerequisites

Testbed VMs must be running via `cloud-provision` before executing any playbook.

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
```

```bash
make 01_base.rocky8                # OS group
make 01_base.rocky8.server         # single VM
```

### Dry Run

```bash
make check                         # full stack dry run
make 01_base.rocky8.server.check
```

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
inventory/testbed.ini              # Rocky 8 + Debian 13 static IPs
inventory/group_vars/all.yml       # Site-independent variables
inventory/group_vars/rocky8.yml    # Rocky 8 specific (epics_os_dir)
inventory/group_vars/debian13.yml  # Debian 13 specific (epics_os_dir)
```

Override inventory path via:

```bash
echo "INVENTORY=inventory/custom.ini" > configure/CONFIG_SITE.local
```

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

## Playbook Layers

| Playbook | Roles | Hosts |
|---|---|---|
| `01_base.yml` | `base_os` | all nodes |
| `02_apps.yml` | `app_con`, `app_procserv`, `app_conserver` | all nodes |
| `03_epics.yml` | `app_epics`, `app_ioc_runner` | ioc nodes |
