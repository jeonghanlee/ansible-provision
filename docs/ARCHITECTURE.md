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
     | VMs running, SSH accessible through the example lab inventory
     | Static IPs assigned outside this repository
     |
     V
[ ansible-provision ]
     |
     | species assembly (playbooks/species/<species>.yml)
     |   = operator playbooks imported in the operator definition's order
     |     (cloud-provision docs/IMAGE_WORKFLOW.md is normative)
     |
     | bare       -> common
     | iocrunner  -> common, provenance, con, conserver, procserv,
     |               python, epics, iocrunner, testusers
     | iocrunner_nfs -> iocrunner + nfs_sim
     | iocserver  -> common, provenance, con, conserver, procserv,
     |               python, epics, iocrunner
     | epics_dev  -> common, python, epics_build, epics_support
     | nfs_sim    -> common, nfs_sim
     | rtbase     -> common, rt
     | ethercat   -> ethercat (on the rtbase golden)
     |
     V
[ Linux nodes ready for EPICS IOC validation ]

Every operator also has its own playbook under playbooks/operators/
for a single-operator run (make op.<operator>).
```

---

## 3. Directory Structure

```
ansible-provision/
|-- Makefile                         (entry point)
|-- ansible.cfg                      (defaults: inventory, become)
|-- configure/                       (EPICS-style Makefile system)
|   |-- CONFIG / RULES               (aggregators)
|   |-- RELEASE                      (appname, species and operator lists)
|   |-- CONFIG_SITE                  (inventory path, vacua, .local override)
|   |-- CONFIG_VARS                  (ansible command variables)
|   |-- RULES_FUNC                   (dynamic target macros)
|   |-- RULES_SETUP                  (host setup, tool checks)
|   |-- RULES_ANSIBLE                (species and operator targets)
|   `-- RULES_VARS                   (env inspection)
|-- inventory/
|   |-- lab.ini                      (host-free lab group relationships)
|   `-- group_vars/
|       |-- all.yml                  (values shared by more than one operator)
|       |-- debian12.yml             (epics_os_dir: debian-12)
|       |-- debian13.yml             (epics_os_dir: debian-13)
|       |-- rocky8.yml               (epics_os_dir, rocky 3.9 python overrides)
|       |-- rocky10.yml              (epics_os_dir: rocky-10.2)
|       |-- ubuntu24.yml             (epics_os_dir: ubuntu-24.04)
|       `-- ubuntu26.yml             (epics_os_dir: ubuntu-26.04)
|-- playbooks/
|   |-- operators/                   (one playbook per operator, 15)
|   `-- species/                     (one assembly per species, 8)
`-- roles/                           (one role per operator, 15; plus 2 legacy)
    |-- common/      rt/          provenance/  python/
    |-- proxy/       epics/       epics_build/ epics_support/
    |-- procserv/    conserver/   con/
    |-- nfs_sim/     iocrunner/   testusers/   ethercat/
    `-- base_os/     app_epics/   (legacy, retired per D3; removal pending)
```

---

## 4. Inventory and Network

`inventory/lab.ini` owns stable group relationships and contains no host
rows. `cloud-provision/bin/generate_ansible_inventory.bash` receives the actual
VM name, resolved IPv4 address, OS selector, and species and writes a
temporary host inventory. Ansible receives both sources, so group variables
remain in this repository while VM identity remains owned by cloud-provision.

Production and site deployments may provide a complete inventory instead.

**Inventory groups:**

| Group | Members |
|---|---|
| `vacua` | Parent of the six vacuum groups |
| `debian12`, `debian13`, `rocky8`, `rocky10`, `ubuntu24`, `ubuntu26` | Generated hosts of that vacuum |
| `iocrunner`, `iocrunner_nfs` | Generated ioc-runner bake hosts, per golden flavor |
| `epics_dev` | Generated EPICS build hosts |
| `nfs_sim` | Generated NFS-simulation hosts |
| `rtbase` | Generated `debian13-rtbase` bake hosts |
| `ethercat` | Generated `debian13-ethercat` runtime hosts |

---

## 5. Role Architecture

The raw-task house conventions (set -e, trailing assertions, quoted
heredocs, sentinel changed_when, validated atomic writes) are codified
in [`RAW_STYLE.md`](RAW_STYLE.md); roles below follow them.

### Proxy Precondition

The `proxy` role is the optional `P_proxy` precondition, applied before
`P_common` and every fetch on a site that reaches the network only through a
proxy. It does not reimplement the proxy artifact set: it streams the
single-authority `bin/proxy_contract.bash` from the control-host
cloud-provision checkout to the target and runs it in apply mode.

```
raw shell (root):
  stage /run/cloud-provision/proxy_contract.bash (0700)
    │
    ├── /run/cloud-provision/proxy-contract.input (0600)
    │     schema=1 / proxy_url=<injected> / script_sha256=<staged hash>
    │
    └── bash proxy_contract.bash apply   (self-hash guard; os auto-detected)
```

The proxy URL is never committed; it is injected per host (`-e proxy_url=` or a
site override) and the role fails when it is unset. Apply installs the
ADR-20260820 artifact set (`profile.d`, `/etc/environment`, apt or dnf, sudo,
sshd, ssh-environment, pip, gitconfig). Golden-mode seal stays on the
cloud-provision bake side; this role is the Live/Instant apply path. The role
skips when the `profile.d` marker is already present unless `proxy_force` is
set.

### Build Pattern

`con`, `procserv`, `conserver` follow an identical raw
pattern (a single `ansible.builtin.raw` block; there is no
ansible-level block/always structure):

```
existence guard: skip when the installed binary is present
  │
  └── raw shell:
        git clone → make targets → install → rm -rf src/
```

### EPICS Binary Distribution

The `epics` role clones a pre-built binary distribution (no compilation):

```
git clone --depth 1 EPICS-env-distribution -> path_epics_local
  |
  `-- deploy /etc/profile.d/epics-env.sh
        source setEpicsEnv.bash (version + OS specific path)
```

EPICS path resolution:

```
{{ path_epics_local }}/{{ epics_env_version }}/{{ epics_os_dir }}/{{ epics_base_version }}/setEpicsEnv.bash
```

| Variable | rocky8 | debian13 |
|---|---|---|
| `epics_os_dir` | `rocky-8.10` | `debian-13` |
| `epics_env_version` | `1.2.2` | `1.2.2` |
| `epics_base_version` | `7.0.10` | `7.0.10` |

### Shared Install-Root Ownership

When `epics_install_group` is set, the `epics` role treats the install root
(`path_epics_local`, e.g. `/opt/epics`) as a group-shared tree that one server
deploys and many hosts read:

```
Prepare the install root (<group> = epics_install_group):
  chgrp <group>; chmod 2775            root:<group>, setgid
  setfacl -d -m g:<group>:rwx          default ACL (local disk)
  setfacl -d -m o::rx
  git config --system safe.directory <path_epics_local>
```

- Group members deploy through the setgid group bit and the default ACL. Git
  creates content in an ACL-bearing directory bypassing the deployer's umask, so
  the ACL grants the group write on newly cloned content — cloned files carry
  effective group `rw`, directories `rwx` — and a second deployer can update a
  first deployer's tree.
- The system-wide `safe.directory` lets any group member run git on the single
  shared repository despite git's repository-owner check. It is set only on the
  deploy server, not on read-only clients.
- `o+rx` lets any account, including the `ioc-srv` service account, read and
  traverse the tree to link against its shared libraries.

Deployment (`git clone`/`pull`) runs on the one host that owns the local
filesystem — the NFS server when the tree is exported. Other hosts mount it
read-only. Default ACLs apply only on local disk; a tree that is itself an NFS
mount cannot carry them and relies on the setgid group and a group-write umask
(`002`).

Site prerequisites (owned by the site provisioning record in
`server-configuration`, not this role):

| Prerequisite | Why |
|---|---|
| Consistent `<group>` GID on every host | An NFS-shared tree resolves group ownership by GID; a mismatched GID breaks group access on clients |
| `root_squash` export pins deploy to the fs server | Client root is squashed, so git writes must run on the filesystem-owning server |
| NFSv4 idmapping domain consistency | Mismatched idmapd domains render owners as `nobody` |
| World-readable tree | `o+rx` exposes the EPICS tree to every user on every client; accepted because the environment is not secret |

### EPICS-env Source Builds

`epics_build` and `epics_support` run through the `epics_dev` species
assembly on dedicated build hosts. The base layer installs vendor libraries inside the
EPICS-env release tree before building EPICS Base and modules. The support
layer then sources the installed environment and adds AreaDetector modules.

```
operators/epics_build.yml
  |-- package automation
  |-- uldaq and open62541 -> <release>/vendor
  `-- EPICS-env -> /opt/epics/<version>/<os>/<base>

operators/epics_support.yml
  `-- EPICS-env-support -> <installed environment>/modules
```

The `internal` flavor uses the normal build target. The `gz` flavor selects
the reduced-debug build target. Both roles detect an installed result and skip
it on a repeated run.

### ioc-runner Infrastructure

The `iocrunner` role sets up system-wide IOC management:

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

`nfs_sim` is applied through `operators/nfs_sim.yml`, inside the
`nfs_sim` and `iocrunner_nfs` species assemblies. The role reproduces
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

After application, root-owned operations under the lab user's
`gitsrc-nfs-sim` symlink are squashed to nobody by the kernel NFS client
over the loopback mount, with no second host required. The regular
iocrunner path keeps the local source root from `path_ioc_runner_root`.
The nfs_sim operator deliberately runs NO ioc-runner pass over the mount:
the playbook runs become-root, and under root_squash the root principal
cannot read, traverse, or execute inside the 0750 vmadmin-owned export —
that is the fixture working as designed, so root-principal in-place
validation is impossible by construction (3ea5c20). Consumer-side
coverage (tar-push + suite flow in epics-ioc-runner) owns validation
over this topology. `nfs_sim_namespace`, `nfs_sim_user`, and
`nfs_sim_group` are validation defaults and may be overridden in site
or lab overlays.

### Module-Use Boundary (EtherCAT exception)

Dual-OS roles and every bake-path role are raw-only: the Rocky 8
targets cannot support Python-backed ansible modules (the platform
constraint behind this repository's raw style). The Debian-13-only
LIVE validation role `ethercat` is the sole exception — it may use
target-side modules (`copy`) because its hosts boot a Debian 13 image
where target Python is guaranteed, and it never runs on the bake path
(the `rt` operator on the pristine rtbase build host stays fully
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
| Firewall | firewalld enforced, EPICS CA/PVA ports opened | no packet filter installed — permissive by design on the isolated lab NAT |

---

## 7. Site-Overlay Contract

There are TWO independent override planes; a value is reachable only
from its own plane. The Make plane cannot set an Ansible variable.

**Make plane** - `configure/CONFIG_SITE.local` (and `RELEASE.local`):
overrides `INVENTORY`, `PLAYBOOK_DIR`, `OS_GROUPS`, `NODE_IDS`,
`VM_PREFIX`, and the playbook topology lists. Two search locations,
later include wins: `$(TOP)/../CONFIG_SITE.local` (out-of-tree - the
recommended home for anything naming site identity) then
`$(TOP)/configure/CONFIG_SITE.local`. These files are gitignored;
never commit them.

**Ansible plane** - group_vars edits, a custom inventory, or
`ANSIBLE_OPTS='-e key=value'`: reaches users, paths, repos, package
lists, NTP servers. Caveat: Ansible loads group_vars from the
INVENTORY FILE'S directory - an out-of-tree custom inventory silently
loses every baseline variable under `inventory/group_vars/`. A custom
inventory must either live under `inventory/` next to the shipped
group_vars or carry its own complete group_vars tree.

**Intended site override points** (and their plane):

| Value | Plane / home |
|---|---|
| `INVENTORY`, `RUNTIME_INVENTORY`, `VM_PREFIX`, topology | Make / CONFIG_SITE.local |
| `ntp_servers` | Ansible / group_vars/all.yml |
| `epics_ioc_engineers` | Ansible / group_vars/all.yml |
| `path_ioc_runner_root` | Ansible / group_vars/all.yml (derived from `epics_ioc_engineers[0]`) |
| `nfs_sim_user` / `nfs_sim_group` / `nfs_sim_namespace` | Ansible / roles/nfs_sim/defaults (override via inventory vars) |
| `epics_env_version` / `epics_base_version` | Ansible / group_vars/all.yml |
| `chrony_*` (`driftfile`, `makestep`, `rtcsync`, `logdir`, `minpoll`, `maxpoll`, `keyfile`, `leapsectz`) | Ansible / group_vars/all.yml (empty poll/keyfile/leapsectz omit the directive) |
| `con_version` / `procserv_version` / `conserver_version` / `ioc_runner_version` | Ansible / group_vars/all.yml (branch, tag, or commit; empty clones default HEAD) |
| `repo_epics` / `epics_install_group` | Ansible / group_vars/all.yml (empty group leaves the install root owned by the IOC engineer) |
| `runtime_python_alt_path` | Ansible / group_vars per OS (`rocky8.yml` selects `/usr/bin/python3.9`) |

**Identity invariant** (must hold; only partially derived): the SSH
user (`ansible_user`), the first IOC engineer
(`epics_ioc_engineers[0]`), and the NFS simulation owner
(`nfs_sim_user`) are the same account on the lab, and
`path_ioc_runner_root` lives under that account's home. Overriding one
without the others fails late (clone/chown into the wrong home).

**Known consumers that bypass the Make plane**: `ansible.cfg` selects
`inventory/lab.ini` for stable group relationships. The cloud-provision
bake and EPICS-env scripts pass that file plus one generated inventory for
each actual VM. Direct CLI use must do the same.

| Scope | File | Contents |
|---|---|---|
| Public baseline defaults | `group_vars/all.yml` | package lists, public GitHub repos, pool NTP |
| Validation defaults | `group_vars/all.yml`, `roles/nfs_sim/defaults/main.yml` | EPICS versions, ioc-runner source root, NFS simulation namespace |
| Lab defaults | `inventory/lab.ini`, `group_vars/all.yml` | group relationships and example IOC engineer user |
| OS defaults | `group_vars/<vacuum>.yml` | `epics_os_dir` (EPICS binary directory selector); `epics_os_packages` (EPICS OS build dependencies, mirrored per vacuum from cloud-provision `configure/epics-packages`); OS python package lists |
