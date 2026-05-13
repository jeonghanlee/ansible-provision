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
| app_epics       | 03_epics    | —      | —        |
| app_ioc_runner  | 03_epics    | ?      | —        |
| nfs_sim         | 04_nfs_sim  | —      | —        |

`?` rows share the same structural risk: `raw` shell with no
`set -e` plus `changed_when: false` masks step failures as ok. See
the silent-failure project memory for detail.

## Open items

### A. app_ioc_runner version stamping
Pre-fix: `ioc-runner -V` showed commit/install dates as
`unreleased`. Role re-cp-ed the binary after setup-system-infra
ran and stamped a nonexistent `RUNNER_BUILD_DATE`. Role cleaned
up; rerun on a fresh substrate not yet performed.

### B. app_epics path mismatch
`epics_os_dir` was hardcoded `rocky-8` against an upstream layout
of `rocky-8.10`. Value corrected; 03_epics has never been applied
on any host.

### C. debian13 EPICS and NFS simulation paths unexercised
Debian 13 VMs are running and `01_base` is verified across
`server`, `node1`, and `node2`. `02_apps` is also verified across
all debian13 hosts. `03_epics` and `04_nfs_sim` remain unrun on
debian13.

### D. SSH key existence check missing in setup_host.bash
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
