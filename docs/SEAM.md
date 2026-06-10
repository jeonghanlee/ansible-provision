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
| Static IP allocation and network scheme | cloud-provision (read-only mirror in ansible-provision inventory) |
| Inventory host groups | ansible-provision |
| Role or playbook that installs or configures software | ansible-provision |
| Consumer software build logic and its own tests | the consumer repo |

## Naming Contract

These names must agree across the seam for one consumer. A mismatch is the
drift this document exists to prevent. Bake-time and runtime identities are
distinct: the build host is provisioned while baking the golden image; the
runtime host boots that image.

| Field | Defined in | iocrunner | ethercat |
|---|---|---|---|
| Bake source variant | cloud-provision | `<os>` base (`rocky8` / `debian13`) | `debian13-rtbase` |
| Runtime variant (`make <variant>.server`) | cloud-provision | `<os>-iocrunner` | `debian13-ethercat` |
| Bake-time inventory target | ansible-provision inventory | `testbed-<os>-server` | `ethercat_build` |
| Runtime host (boots the variant) | ansible-provision inventory | `testbed-<os>-iocrunner-server` | `ethercat_nodes` |
| Bake-time playbook | ansible-provision | `site.yml` + `04_nfs_sim.yml` | `05_ethercat_base.yml` |
| Runtime playbook | ansible-provision | none (boots baked image) | `06_ethercat.yml` |

Per cloud-provision section 11, the IP scheme in `inventory/testbed.ini`
is a shared contract: any change requires coordinated updates in both
repositories.

## Consumer Register

Open and growing. Two kinds of row share this table: consumer projects that
consume the VM substrate through a dedicated baked variant (epics-ioc-runner,
ethercat-env), and app-role workloads installed on the base VM (con, procServ,
conserver). The "Dedicated variant?" column tells them apart.

| Consumer / workload | Installs / tests | Dedicated variant? | cloud-provision | ansible-provision | Seam status |
|---|---|---|---|---|---|
| epics-ioc-runner | ioc-runner install + integration test | Yes | `bake_iocrunner_image.bash`, `*-iocrunner` | `site.yml` + `04_nfs_sim.yml` (`app_ioc_runner`) | Complete |
| ethercat-env | EtherCAT R2-12 install + validation | Yes | `bake_ethercat_image.bash`, `debian13-ethercat` / `debian13-rtbase` — absent | `05_ethercat_base.yml`, `06_ethercat.yml` (`ethercat_base`, `app_ethercat`) | Partial |
| con | con build + install | No (base VM app role) | base variant | `02_apps.yml` (`app_con`) | Complete |
| procServ-env | procServ build + install | No (base VM app role) | base variant | `02_apps.yml` (`app_procserv`) | Complete |
| conserver-env | conserver build + install | No (base VM app role) | base variant | `02_apps.yml` (`app_conserver`) | Complete |

Going forward, a new VM-needing project either claims a cloud-provision
variant or rides the base VM, adds its host group and playbook in
ansible-provision, and records a row here. Seam status stays Partial until
both sides exist.

## Open Seam Gap

EtherCAT is the current partial seam. `playbooks/05_ethercat_base.yml` is the
bake-time layer that `cloud-provision/bin/bake_ethercat_image.bash` would
invoke, and `playbooks/06_ethercat.yml` assumes a baked `debian13-ethercat`
runtime VM (from `make debian13-ethercat.server`). Neither the bake script nor
the `debian13-ethercat` / `debian13-rtbase` variants exist in cloud-provision
yet, so EtherCAT provisioning cannot run end-to-end until the cloud side is
built.
