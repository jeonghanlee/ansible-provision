# ansible-provision

Ansible-based provisioner for cloud-provision testbed VMs.
Deploys con, procServ, conserver, EPICS, and ioc-runner on Rocky 8 and Debian 13.

* Testbed VM provisioner: [cloud-provision](https://github.com/jeonghanlee/cloud-provision)
* EPICS environment: [EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution)

## Prerequisites

Testbed VMs must be running via `cloud-provision` before executing any playbook.

```bash
# Verify connectivity
ansible all -m ping
```

## Inventory

```
inventory/testbed.ini          # Rocky 8 + Debian 13 static IPs
inventory/group_vars/all.yml   # Site-independent variables
inventory/group_vars/rocky8.yml
inventory/group_vars/debian13.yml
```

## Workflow

```bash
ansible-playbook site.yml                     # full stack
ansible-playbook playbooks/01_base.yml        # base OS only
ansible-playbook playbooks/02_apps.yml        # con, procServ, conserver
ansible-playbook playbooks/03_epics.yml       # EPICS + ioc-runner
```

```bash
ansible-playbook site.yml --limit rocky8      # single OS group
ansible-playbook site.yml --limit testbed-rocky8-server
ansible-playbook site.yml --tags epics        # single role
ansible-playbook site.yml -C                  # dry run
```

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
