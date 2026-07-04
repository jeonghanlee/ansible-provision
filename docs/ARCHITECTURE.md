# ansible-provision Architecture

## 1. Overview

Ansible-based Linux system unification baseline for Rocky 8 and Debian 13.
The repository installs common operating-system services and validates EPICS
operation above that baseline. The first-pass validation environment uses
`cloud-provision` VMs, but VM lifecycle is not owned by this repository.

---

## 2. Provisioning Flow

```
[ cloud-provision ]
     |
     | VMs running, SSH accessible through example testbed inventory
     | Static IPs assigned outside this repository
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
[ Linux nodes ready for EPICS IOC validation ]

(out-of-band, not in site.yml)
04_nfs_sim.yml → nfs_sim role
                 - loopback NFS export with root_squash
                 - exposes an NFS-mounted simulation source root
                 (ioc-runner validation over that root is NOT done at
                  bake time — root-principal access is impossible under
                  root_squash by design; coverage lives in the consumer's
                  tar-push + suite flow. See docs/MILESTONES.md.)

05_ethercat_base.yml → ethercat_base role   (ethercat_build host;
                 invoked by the cloud-provision ethercat bake)
06_ethercat.yml      → app_ethercat role    (ethercat_nodes; live
                 R2-12 validation harness, run directly)
07_test_users.yml    → test_users role      (nfs_sim_nodes; consumer
                 test fixtures — bake activation pending)
```

---

## 3. Directory Structure

```
ansible-provision/
├── Makefile                         (entry point)
├── ansible.cfg                      (defaults: inventory, become)
├── site.yml                         (master playbook)
├── configure/                       (EPICS-style Makefile system)
│   ├── CONFIG / RULES               (aggregators)
│   ├── RELEASE                      (appname, playbook stages)
│   ├── CONFIG_SITE                  (inventory path, topology, .local override)
│   ├── CONFIG_VARS                  (ansible command variables)
│   ├── RULES_FUNC                   (dynamic target macros)
│   ├── RULES_SETUP                  (host setup, tool checks)
│   ├── RULES_ANSIBLE                (playbook targets)
│   └── RULES_VARS                   (env inspection)
├── inventory/
│   ├── testbed.ini                  (example validation inventory)
│   └── group_vars/
│       ├── all.yml                  (site-independent variables)
│       ├── rocky8.yml               (epics_os_dir: rocky-8.10)
│       └── debian13.yml             (epics_os_dir: debian-13)
├── playbooks/
│   ├── 01_base.yml
│   ├── 02_apps.yml
│   ├── 03_epics.yml
│   ├── 04_nfs_sim.yml
│   ├── 05_ethercat_base.yml
│   ├── 06_ethercat.yml
│   └── 07_test_users.yml
└── roles/
    ├── base_os/
    ├── app_con/
    ├── app_procserv/
    ├── app_conserver/
    ├── app_epics/
    ├── app_ioc_runner/
    ├── nfs_sim/
    ├── test_users/
    ├── ethercat_base/
    └── app_ethercat/
```

---

## 4. Inventory and Network

The bundled inventory is an example validation inventory. Static IPs and
the default `vmadmin` SSH identity are testbed defaults inherited from the
first-pass `cloud-provision` environment, not public baseline requirements.
Production and site deployments should supply their own inventory.

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
| `nfs_sim_nodes` | rocky8-server, debian13-server |

---

## 5. Role Architecture

The raw-task house conventions (set -e, trailing assertions, quoted
heredocs, sentinel changed_when, validated atomic writes) are codified
in [`RAW_STYLE.md`](RAW_STYLE.md); roles below follow them.

### Build Pattern

`app_con`, `app_procserv`, `app_conserver` follow an identical raw
pattern (a single `ansible.builtin.raw` block; there is no
ansible-level block/always structure):

```
existence guard: skip when the installed binary is present
  │
  └── raw shell:
        git clone → make targets → install → rm -rf src/
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
| `epics_os_dir` | `rocky-8.10` | `debian-13` |
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
  ├── clone epics-ioc-runner → {{ path_ioc_runner_root }}/epics-ioc-runner
  ├── copy bin/ioc-runner → /usr/local/bin/
  ├── inject git hash + build date
  ├── copy completion → /etc/bash_completion.d/
  └── verify ioc-runner -V, list -vv, and inspect help

mkdir /opt/epics-iocs (2775, root:ioc)
usermod -aG ioc {{ epics_ioc_engineers }}
```

### NFS root_squash Simulation

`nfs_sim` is an out-of-band role applied only to `nfs_sim_nodes`
(rocky8-server + debian13-server). It is not part of `site.yml`
and is invoked via `playbooks/04_nfs_sim.yml`. The role reproduces
the production NFS root_squash environment on a single host, so
that epics-ioc-runner install and build flows can be exercised
against the same permission shape they meet in deployment:

```
install nfs-utils / nfs-kernel-server
  │
  ├── /srv/nfs/simulation/vmadmin/gitsrc  (export source, vmadmin:vmadmin)
  │
  ├── /etc/exports.d/nfs_sim.exports
  │     127.0.0.1: rw,sync,root_squash,no_subtree_check,fsid=10
  │
  ├── /home/nfs/simulation/vmadmin/gitsrc (mount point, fstab persistent)
  │     127.0.0.1:/srv/... nfs rw,soft,_netdev
  │
  └── ~vmadmin/gitsrc-nfs-sim -> /home/nfs/simulation/vmadmin/gitsrc
```

After application, root-owned operations under the testbed user's
`gitsrc-nfs-sim` symlink are squashed to nobody by the kernel NFS client
over the loopback mount, with no second host required. The regular
`03_epics` path keeps the local source root from `path_ioc_runner_root`.
`04_nfs_sim` deliberately runs NO ioc-runner pass over the mount: the
playbook runs become-root, and under root_squash the root principal
cannot read, traverse, or execute inside the 0750 vmadmin-owned export —
that is the fixture working as designed, so root-principal in-place
validation is impossible by construction (3ea5c20). Consumer-side
coverage (tar-push + suite flow in epics-ioc-runner) owns validation
over this topology. `nfs_sim_namespace`, `nfs_sim_user`, and
`nfs_sim_group` are validation defaults and may be overridden in site
or testbed overlays.

### Module-Use Boundary (EtherCAT exception)

Dual-OS roles and every bake-path role are raw-only: the Rocky 8
targets cannot support Python-backed ansible modules (the platform
constraint behind this repository's raw style). The Debian-13-only
LIVE validation role `app_ethercat` is the sole exception — it may use
target-side modules (`copy`) because its hosts boot a Debian 13 image
where target Python is guaranteed, and it never runs on the bake path
(`05_ethercat_base` on the pristine rtbase build host stays fully
raw). New roles follow the same rule: raw-only unless the role is
Debian-13-live-only, and never modules on a bake path.

---

## 6. OS Differences

| Concern | Rocky 8 | Debian 13 |
|---|---|---|
| Package manager | `dnf` | `apt` |
| Task file    | `redhat.yml` | `debian.yml` |
| SSL headers  | not explicitly listed (arrive transitively; parity with Debian is an open item) | `libssl-dev` |
| EPICS os dir | `rocky-8.10` | `debian-13` |
| EPICS repo   | `EPEL + PowerTools` required | standard apt |
| Python pip   | `pip3.9` (system-wide)   | apt packages + `pip3 --break-system-packages` (EPICS only) |
| sudo secure_path | drop-in adds `/usr/local/{sbin,bin}` | default already includes `/usr/local` |
| Firewall | firewalld enforced, EPICS CA/PVA ports opened | no packet filter installed — permissive by design on the isolated testbed NAT |

---

## 7. Site-Overlay Contract

There are TWO independent override planes; a value is reachable only
from its own plane. The Make plane cannot set an Ansible variable.

**Make plane** — `configure/CONFIG_SITE.local` (and `RELEASE.local`):
overrides `INVENTORY`, `PLAYBOOK_DIR`, `OS_GROUPS`, `NODE_IDS`,
`VM_PREFIX`, and the playbook topology lists. Two search locations,
later include wins: `$(TOP)/../CONFIG_SITE.local` (out-of-tree — the
recommended home for anything naming site identity) then
`$(TOP)/configure/CONFIG_SITE.local`. These files are gitignored;
never commit them.

**Ansible plane** — group_vars edits, a custom inventory, or
`ANSIBLE_OPTS='-e key=value'`: reaches users, paths, repos, package
lists, NTP servers. Caveat: Ansible loads group_vars from the
INVENTORY FILE'S directory — an out-of-tree custom inventory silently
loses every baseline variable under `inventory/group_vars/`. A custom
inventory must either live under `inventory/` next to the shipped
group_vars or carry its own complete group_vars tree.

**Intended site override points** (and their plane):

| Value | Plane / home |
|---|---|
| `INVENTORY`, `VM_PREFIX`, topology | Make / CONFIG_SITE.local |
| `ntp_servers` | Ansible / group_vars/all.yml |
| `epics_ioc_engineers` | Ansible / group_vars/all.yml |
| `path_ioc_runner_root` | Ansible / group_vars/all.yml (derived from `epics_ioc_engineers[0]`) |
| `nfs_sim_user` / `nfs_sim_group` / `nfs_sim_namespace` | Ansible / roles/nfs_sim/defaults (override via inventory vars) |
| `epics_env_version` / `epics_base_version` | Ansible / group_vars/all.yml |

**Identity invariant** (must hold; only partially derived): the SSH
user (`ansible_user`), the first IOC engineer
(`epics_ioc_engineers[0]`), and the NFS simulation owner
(`nfs_sim_user`) are the same account on the testbed, and
`path_ioc_runner_root` lives under that account's home. Overriding one
without the others fails late (clone/chown into the wrong home).

**Known consumers that bypass the Make plane**: `ansible.cfg` pins
`inventory/testbed.ini` for the Direct CLI workflow, and the
cloud-provision bake scripts pass the same path literally — a
CONFIG_SITE.local `INVENTORY` override affects make targets only
(closing this is tracked as Phase C4 in `docs/MILESTONES.md`).

| Scope | File | Contents |
|---|---|---|
| Public baseline defaults | `group_vars/all.yml` | package lists, public GitHub repos, pool NTP |
| Validation defaults | `group_vars/all.yml`, `roles/nfs_sim/defaults/main.yml` | EPICS versions, ioc-runner source root, NFS simulation namespace |
| Testbed defaults | `inventory/testbed.ini`, `group_vars/all.yml` | example IPs, `vmadmin` SSH user, example IOC engineer user |
| OS defaults | `group_vars/rocky8.yml`, `group_vars/debian13.yml` | OS-specific EPICS binary directory selectors; OS python package lists (sole owners) |
