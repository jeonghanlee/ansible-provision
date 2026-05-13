# ansible-provision Verification Status

Living document tracking which role × OS combinations have been
verified end-to-end on a real testbed, distinct from the structural
description in ARCHITECTURE.md.

**Last updated:** 2026-05-13
**See also:** `TODO.md` for deferred feature work; this file tracks
verification state and known defects.

## Status legend

| Symbol | Meaning |
|--------|---------|
| ✓      | Applied and verified — binary/config landed, idempotent rerun observed |
| ?      | Applied; ansible reported ok but artefact not independently verified |
| ✗      | Known broken — bug filed in Open Items below |
| —      | Not yet applied on this OS |

## Role × OS matrix

| Role            | Playbook    | rocky8 | debian13 |
|-----------------|-------------|--------|----------|
| base_os         | 01_base     | ✓      | ✓        |
| app_con         | 02_apps     | ✓      | ✓        |
| app_procserv    | 02_apps     | ✓      | ✓        |
| app_conserver   | 02_apps     | ✓      | ✓        |
| app_epics       | 03_epics    | ✓      | ✓        |
| app_ioc_runner  | 03_epics    | ?      | ?        |
| nfs_sim         | 04_nfs_sim  | —      | —        |

`?` indicates that the role has been applied and the installed
artifact exists, but one or more acceptance criteria remain open.

## Open items

### A. app_ioc_runner version stamping
`03_epics` applies successfully across Rocky 8 and Debian 13, and
`ioc-runner -V` reports `1.0.8-dev` on all hosts. The commit date
metadata still reports `unknown`, so full ioc-runner closure remains
part of Milestone 4.

### B. NFS simulation paths unexercised
Rocky 8 and Debian 13 VMs are running, and `01_base`, `02_apps`,
and `03_epics` are verified across `server`, `node1`, and `node2`.
`04_nfs_sim` remains unrun.

### C. SSH key existence check missing in setup_host.bash
`bin/setup_host.bash` installs `ansible-core` but does not verify
the operator has an SSH keypair. ansible reaches managed nodes
over SSH, so a missing key surfaces only at first ping. Check for
`~/.ssh/id_ed25519.pub` or `~/.ssh/id_rsa.pub` and warn if absent
(mirrors the sister `cloud-provision` repo). Tracked in
`TODO.md`.

## Update protocol

When a role × OS combination is applied or verified, update the
matrix and the relevant Open Item in the same commit as the
substantive change. Do not let the matrix drift behind the code.
