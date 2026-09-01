# Seam Contract: cloud-provision and ansible-provision

## Scope

Canonical contract for the seam between the two VM-provisioning
repositories, plus the register of projects that consume them. It answers
one question: for a given piece of work, which repository owns it.

The dependency is directional:

- `cloud-provision` — VM lifecycle: create, bake golden images, destroy.
- `ansible-provision` — uses cloud-provision's VMs to install and
  configure software into them.
- Consumer projects — use the pair as the substrate to install and
  in-depth test their own software.

Cloud-side detail is authoritative in `cloud-provision/docs/ARCHITECTURE.md`
sections 5 (VM Naming Convention), 11 (Hand-off), and 12 (Bake Pipeline).
This file holds the responsibility boundary, the cross-repo naming
contract, and the consumer register; it does not duplicate those sections.

## Responsibility Boundary

| Work | Owning repo |
|---|---|
| Create, bake, or destroy a VM; golden image | cloud-provision |
| VM naming convention, OS variant definition | cloud-provision |
| VM name and resolved address | cloud-provision |
| Species-to-group mapping and generated host inventory | cloud-provision generator |
| Stable group relationships and group variables | ansible-provision |
| Role or playbook that installs or configures software | ansible-provision |
| EPICS OS build dependency package set (source of truth) | cloud-provision |
| Consumer software build logic and its own tests | the consumer repo |

## Naming Contract

These names must agree across the seam for one consumer. A mismatch is the
drift this document exists to prevent. Bake-time and runtime identities are
distinct: the build host is provisioned while baking the golden image; the
runtime host boots that image.

| Field | Defined in | iocrunner | ethercat |
|---|---|---|---|
| Bake source variant | cloud-provision | `<os>` base (`rocky8` / `debian13`) | `debian13-rtbase` |
| Runtime variant | cloud-provision | `<os>-iocrunner` or `<os>-iocrunner-nfs` (flavor) | `debian13-ethercat` |
| Bake-time generated groups | cloud-provision generator | vacuum + `iocrunner` or `iocrunner_nfs` | vacuum + `rtbase` |
| Runtime generated groups | cloud-provision generator | vacuum only (`--species bare`) when Ansible use is requested | vacuum + `ethercat` |
| Bake-time assembly | ansible-provision | `species/iocrunner.yml` or `species/iocrunner_nfs.yml` (flavor flag) | `species/rtbase.yml` |
| Runtime assembly | ansible-provision | none (boots baked image) | `species/ethercat.yml` |

The actual host name and address never appear in the maintained inventory.
`inventory/lab.ini` provides only group relationships; generated host
inventories carry the current identity across the seam.

## EPICS OS Build Dependencies

The OS packages an image needs to build IOCs, and to build EPICS-env from
source, are a normative artifact that crosses the seam.

| Field | Defined in | Value |
|---|---|---|
| Package source of truth | cloud-provision | `configure/epics-packages`: one verbatim per-OS list, guarded by `tests/check-epics-packages.bash`, referenced from both `P_epics` and `P_epics-build` in `docs/OPERATOR_MODEL.md` |
| Package mirror | ansible-provision | `epics_os_packages` in each vacuum's `inventory/group_vars/<os>.yml`, installed by `roles/epics` (distribution) and `roles/epics_build` (source) |

The lists carry OS-specific package names that differ by family and version, so
the mirror is per vacuum rather than a canonical set with a spelling map.
cloud-provision owns the source; ansible-provision keeps its own installer list
and re-mirrors when the source changes.

### Distribution OS coverage

The `epics` role (`P_epics`) installs a pre-built EPICS-env by sparse-checking
out `<epics_env_version>/<epics_os_dir>/<epics_base_version>` from
EPICS-env-distribution, so it requires a published tree for the vacuum's
`epics_os_dir`. The `epics_build` role (`P_epics-build`) builds from source and
requires no published tree.

At EPICS-env-distribution 1.2.2 the published OS trees are `debian-13`,
`rocky-8.10`, `rocky-10.2`, and `ubuntu-24.04`. A vacuum whose `epics_os_dir`
has no published tree (currently `debian-12` and `ubuntu-26.04`) can be
provisioned only through the source-build path until the tree is published
(tracked at jeonghanlee/EPICS-env-distribution#4). Each vacuum sets its
`epics_os_dir` in `inventory/group_vars/<os>.yml`.

## Consumer Register

Open and growing. Two kinds of row share this table: consumer projects that
consume the VM substrate through a dedicated baked variant (epics-ioc-runner,
ethercat-env), and app-role workloads installed on the base VM (con, procServ,
conserver). The "Dedicated variant?" column tells them apart.

| Consumer / workload | Installs / tests | Dedicated variant? | cloud-provision | ansible-provision | Seam status |
|---|---|---|---|---|---|
| epics-ioc-runner | ioc-runner install + integration test | Yes | `bake_iocrunner_image.bash`, `*-iocrunner` | `species/iocrunner.yml` / `species/iocrunner_nfs.yml` (the `iocrunner` role runs inside the assembly) | Complete |
| ethercat-env | EtherCAT R2-12 install + validation | Yes | `bake_ethercat_image.bash`, `debian13-ethercat` / `debian13-rtbase` — present | `species/rtbase.yml`, `species/ethercat.yml` (`rt`, `ethercat` roles) | Present, unverified end-to-end |
| con | con build + install | No (operator on the base VM) | base variant | `operators/con.yml` (`con` role) | Complete |
| procServ-env | procServ build + install | No (operator on the base VM) | base variant | `operators/procserv.yml` (`procserv` role) | Complete |
| conserver-env | conserver build + install | No (operator on the base VM) | base variant | `operators/conserver.yml` (`conserver` role) | Complete |

epics-ioc-runner's multi-user runbook scenarios extend its seam with the
`testusers` fixture (`roles/testusers`, `playbooks/operators/testusers.yml`),
applied inside the iocrunner species assembly; fresh Rocky 8 and Debian 13
variants verified the account and linger state on 2026-07-05. See
`docs/test_users_handoff.md`.

Going forward, a new VM-needing project either claims a cloud-provision
variant or rides the base VM, adds its host group and playbook in
ansible-provision, and records a row here. Seam status stays Partial until
both sides exist.

Authoring rule (added 2026-07-04, review rs20260702_083212): before
writing or changing a row that asserts the state of the OTHER side of
the seam, verify that side on disk at authoring time (list the scripts,
run `make -n` on the named targets). The original ethercat row claimed
assets "absent" that already existed when the row was written —
authoring-time verification, not periodic sweeps, is what prevents
that class of defect.

## Open Seam Gap

EtherCAT: both sides now exist — `cloud-provision` carries
`bin/bake_ethercat_image.bash` plus the `debian13-ethercat` /
`debian13-rtbase` variants, and this repository carries
`species/rtbase.yml` / `species/ethercat.yml`. The remaining gap is that
no end-to-end run has been executed (bake, boot, run the ethercat
assembly, archive evidence). Readiness items before that first run are tracked
in the cloud-provision work register's deferred EtherCAT acceptance entry.

EPICS distribution OS coverage: the `epics` (distribution) path needs a
published EPICS-env-distribution tree per vacuum, and `debian-12` /
`ubuntu-26.04` are not published at 1.2.2 (see EPICS OS Build Dependencies,
Distribution OS coverage; tracked at jeonghanlee/EPICS-env-distribution#4).
Those vacua provision only through the source-build path until the trees ship.
