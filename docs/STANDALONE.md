# Provisioning a Standalone VM

How to apply this repository to a single VM that is NOT part of the
cloud-provision testbed. Two modes cover every case: a separate
control host driving the VM over ssh, or the VM provisioning itself
from a local clone. Both work because every dual-OS task here is
`ansible.builtin.raw` with `gather_facts: false` — no Python is
required on the managed side, and localhost needs nothing special.

The override contract behind these recipes is `ARCHITECTURE.md`
section 7; this page is the recipe only.

## Common Prerequisites

- Target OS: Rocky 8 or Debian 13.
- A sudo-capable account on the target. The stack runs become
  non-interactively (`ansible.cfg`: `become_ask_pass = False`), so
  either grant NOPASSWD sudo or append
  `ANSIBLE_OPTS=--ask-become-pass` to every make command.
- Outbound network from the target: `02_apps`/`03_epics` clone build
  sources from GitHub. On a proxied site, apply the injection layers
  from `cloud-provision/docs/RUNBOOK_BAKE.md` to the target VM (a
  standalone VM keeps them; the de-proxy step is a golden-bake
  concern).
- The custom inventory MUST live under `inventory/` next to the
  shipped `group_vars/`, or every baseline variable is silently lost
  (ARCHITECTURE.md section 7, custom-inventory caveat).
- Identity invariant: the connecting/invoking account equals
  `epics_ioc_engineers[0]`, and its home directory exists —
  `path_ioc_runner_root` derives from it.

## Mode 1 — Control Host over SSH

On the control host: clone this repository, `make setup`
(ansible-core), and have an ssh key accepted by the target account.

`inventory/mysite.ini`:

```ini
[rocky8]
myvm  ansible_host=10.0.0.42  ansible_user=opctrl

[ioc_nodes:children]
rocky8

[all_nodes:children]
rocky8
```

Use the `[debian13]` group for a Debian target — the OS group selects
`epics_os_dir` and the package lists. `ansible_host` is the address
ansible connects to; drop it when the inventory label itself resolves.

```bash
echo "INVENTORY=inventory/mysite.ini" > configure/CONFIG_SITE.local
```

Adjust the Ansible-plane values (at minimum `epics_ioc_engineers` in
`inventory/group_vars/all.yml`), then:

```bash
make ping
make 01_base
make 02_apps
make 03_epics
```

`make all` runs the three site.yml stages in one pass. Optional
extras: add the host to `[nfs_sim_nodes]` and run `make 04_nfs_sim`
and/or `make 07_test_users` when the root_squash simulation or the
consumer test fixtures are wanted.

Trust note: `ansible.cfg` disables host-key checking (testbed
posture). Point this at hosts outside an isolated network only after
reconsidering that setting.

## Mode 2 — Local Clone (self-provisioning)

Clone this repository ON the target VM and run it against localhost.
No ssh, no key exchange, no control host.

On the VM: clone, then `make setup` (installs ansible-core from the
OS repositories).

`inventory/mysite.ini`:

```ini
[rocky8]
localhost  ansible_connection=local

[ioc_nodes:children]
rocky8

[all_nodes:children]
rocky8
```

`ansible_host`/`ansible_user` are unnecessary — `ansible_connection=local`
executes directly as the invoking user, with become for the root
steps. Everything else is identical to Mode 1: the
`CONFIG_SITE.local` override, the `epics_ioc_engineers` adjustment,
and the same make targets (`make ping` trivially passes).

## Choosing Between Them

| Situation | Mode |
| --- | --- |
| Several VMs, one operator seat, keys managed centrally | 1 (control host) |
| One box configuring itself; no second machine available | 2 (local clone) |
| Golden-image bake pipeline | Neither — that path is owned by cloud-provision (`RUNBOOK_BAKE.md`) |
