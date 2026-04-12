# ansible-provision Architecture

## 1. Overview

Ansible-based application provisioner for libvirt/KVM testbed VMs.
Operates on top of `cloud-provision` base images and deploys the full
EPICS control system stack across Rocky 8 and Debian 13 nodes.

---

## 2. Provisioning Flow

```
[ cloud-provision ]
     |
     | VMs running, SSH accessible (vmadmin)
     | Static IPs assigned via libvirt DHCP reservation
     |
     V
[ ansible-provision ]
     |
     | 01_base.yml  →  base_os role
     |                 - OS packages (dnf / apt)
     |                 - chrony NTP
     |
     | 02_apps.yml  →  app_con, app_procserv, app_conserver roles
     |                 - Build from source via Makefile repos
     |
     | 03_epics.yml →  app_epics, app_ioc_runner roles
     |                 - EPICS-env-distribution (binary, depth 1)
     |                 - epics-ioc-runner infrastructure setup
     |
     V
[ Nodes ready for IOC deployment ]
```

---

## 3. Directory Structure

```
ansible-provision/
├── Makefile                         (entry point)
├── ansible.cfg                      (defaults: inventory, become, python)
├── site.yml                         (master playbook)
├── configure/                       (EPICS-style Makefile system)
│   ├── CONFIG / RULES               (aggregators)
│   ├── RELEASE                      (playbook/group/node matrix)
│   ├── CONFIG_SITE                  (inventory path, .local override)
│   ├── CONFIG_VARS                  (ansible command variables)
│   ├── RULES_FUNC                   (dynamic target macros)
│   ├── RULES_ANSIBLE                (playbook targets)
│   └── RULES_VARS                   (env inspection)
├── inventory/
│   ├── testbed.ini                  (static IPs from cloud-provision)
│   └── group_vars/
│       ├── all.yml                  (site-independent variables)
│       ├── rocky8.yml               (epics_os_dir: rocky-8)
│       └── debian13.yml             (epics_os_dir: debian-13)
├── playbooks/
│   ├── 01_base.yml
│   ├── 02_apps.yml
│   └── 03_epics.yml
└── roles/
    ├── base_os/
    ├── app_con/
    ├── app_procserv/
    ├── app_conserver/
    ├── app_epics/
    └── app_ioc_runner/
```

---

## 4. Inventory and Network

Static IPs are inherited from `cloud-provision` DHCP reservations.
No dynamic inventory is required.

```
192.168.122.10   testbed-debian13-server   [debian13, ioc_nodes]
192.168.122.11   testbed-debian13-node1    [debian13, ioc_nodes]
192.168.122.12   testbed-debian13-node2    [debian13, ioc_nodes]
192.168.122.100  testbed-rocky8-server     [rocky8,   ioc_nodes]
192.168.122.101  testbed-rocky8-node1      [rocky8,   ioc_nodes]
192.168.122.102  testbed-rocky8-node2      [rocky8,   ioc_nodes]
```

**Inventory groups:**

| Group | Members |
|---|---|
| `rocky8` | server, node1, node2 |
| `debian13` | server, node1, node2 |
| `ioc_nodes` | rocky8 + debian13 |
| `all_nodes` | rocky8 + debian13 |

---

## 5. Role Architecture

### Build Pattern

`app_con`, `app_procserv`, `app_conserver` follow an identical pattern:

```
stat binary → skip if exists
  │
  └── block:
        git clone → make targets → install
      always:
        rm -rf src/
```

### EPICS Binary Distribution

`app_epics` clones a pre-built binary distribution (no compilation):

```
git clone --depth 1 EPICS-env-distribution → path_epics_local
  │
  └── deploy /etc/profile.d/epics-env.sh
        source setEpicsEnv.bash (version + OS specific path)
```

EPICS path resolution:

```
{{ path_epics_local }}/{{ epics_env_version }}/{{ epics_os_dir }}/{{ epics_base_version }}/setEpicsEnv.bash
```

| Variable | rocky8 | debian13 |
|---|---|---|
| `epics_os_dir` | `rocky-8` | `debian-13` |
| `epics_env_version` | `1.2.0` | `1.2.0` |
| `epics_base_version` | `7.0.10` | `7.0.10` |

### ioc-runner Infrastructure

`app_ioc_runner` sets up system-wide IOC management:

```
setup-system-infra.bash --full
  ├── groupadd ioc
  ├── useradd ioc-srv (nologin, isolated)
  ├── mkdir /etc/procServ.d (2770, root:ioc)
  ├── /etc/sudoers.d/10-epics-ioc (systemctl epics-@*.service)
  └── /etc/systemd/system/epics-@.service (procServ template)

ioc-runner CLI install
  ├── copy bin/ioc-runner → /usr/local/bin/
  ├── inject git hash + build date
  └── copy completion → /etc/bash_completion.d/

mkdir /opt/epics-iocs (2775, root:ioc)
usermod -aG ioc {{ epics_ioc_engineers }}
```

---

## 6. OS Differences

| Concern | Rocky 8 | Debian 13 |
|---|---|---|
| Package manager | `dnf` | `apt` |
| Task file | `redhat.yml` | `debian.yml` |
| SSL headers | `openssl-devel` | `libssl-dev` |
| EPICS os dir | `rocky-8` | `debian-13` |
| EPICS repo | `EPEL + PowerTools` required | standard apt |

---

## 7. Variable Scoping

| Scope | File | Contents |
|---|---|---|
| All hosts | `group_vars/all.yml` | repos, paths, packages, NTP |
| Rocky 8 | `group_vars/rocky8.yml` | `epics_os_dir: rocky-8` |
| Debian 13 | `group_vars/debian13.yml` | `epics_os_dir: debian-13` |
| Site override | `configure/CONFIG_SITE.local` | `INVENTORY`, `PLAYBOOK_DIR` |
