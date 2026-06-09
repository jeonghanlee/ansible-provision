# ansible-provision Verification Status

Living document tracking which role × OS combinations have been
verified end-to-end on a real testbed, distinct from the structural
description in ARCHITECTURE.md.

Canonical roll-up: `docs/MILESTONES.md`.

**Last updated:** 2026-06-09
**See also:** `TODO.md` for deferred feature work; this file tracks
verification state and known defects.

## Status legend

| Symbol | Meaning |
|--------|---------|
| ✓      | Applied and verified — binary/config landed, idempotent rerun observed |
| ?      | Applied; ansible reported ok but artefact not independently verified |
| ✗      | Known broken — documented in Verification notes below |
| —      | Not yet applied on this OS |

## Role × OS matrix

| Role            | Playbook    | rocky8 | debian13 |
|-----------------|-------------|--------|----------|
| base_os         | 01_base     | ✓      | ✓        |
| app_con         | 02_apps     | ✓      | ✓        |
| app_procserv    | 02_apps     | ✓      | ✓        |
| app_conserver   | 02_apps     | ✓      | ✓        |
| app_epics       | 03_epics    | ✓      | ✓        |
| app_ioc_runner  | 03_epics    | ✓      | ✓        |
| nfs_sim         | 04_nfs_sim  | ✓      | ✓        |

## Verification notes

### NFS simulation paths verified
`04_nfs_sim` was applied on the Rocky 8 and Debian 13 ioc-runner
server validation hosts. The simulation namespace was mounted at
`/home/nfs/simulation/vmadmin/gitsrc`, old `alsu` namespace entries
were absent, vmadmin writes succeeded, root-owned writes were denied by
root_squash, and `ioc-runner` smoke checks passed.

## EtherCAT validation (Debian 13, separate scope)

Tracked outside the role × OS matrix above: EtherCAT is a Debian 13-only
bake + live-VM validation harness for the external `ethercat-env` buildout,
not part of the core completion model. See `docs/MILESTONES.md`.

| Component      | Playbook         | Host group            | Status |
|----------------|------------------|-----------------------|--------|
| ethercat_base  | 05_ethercat_base | ethercat_build (bake) | —      |
| app_ethercat   | 06_ethercat      | ethercat_nodes (live) | —      |

Verification requires the baked `ethercat-debian13` golden image and a live
VM run; not yet exercised end-to-end.

## Update protocol

When a role × OS combination is applied or verified, update the
matrix and the relevant Open Item in the same commit as the
substantive change. Do not let the matrix drift behind the code.
