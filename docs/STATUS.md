# ansible-provision Verification Status

Living document tracking which role × OS combinations have been
verified end-to-end on a real testbed, distinct from the structural
description in ARCHITECTURE.md.

Canonical roll-up: `docs/MILESTONES.md`.

**Last updated:** 2026-06-04
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
| app_ioc_runner  | 03_epics    | ✓      | ✓        |
| nfs_sim         | 04_nfs_sim  | ✓      | ✓        |

## Open items

### A. NFS simulation paths verified
`04_nfs_sim` was applied on the Rocky 8 and Debian 13 ioc-runner
server validation hosts. The simulation namespace was mounted at
`/home/nfs/simulation/vmadmin/gitsrc`, old `alsu` namespace entries
were absent, vmadmin writes succeeded, root-owned writes were denied by
root_squash, and `ioc-runner` smoke checks passed.

### B. SSH key existence check missing in setup_host.bash
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
