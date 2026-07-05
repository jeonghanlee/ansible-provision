# ansible-provision Milestones

## Scope

This document is the canonical work register for `ansible-provision`.
It consolidates implementation milestones, carry-forward work, external
gates, and conceptual-integrity findings that need owner decisions.

Supporting evidence remains in `docs/STATUS.md` and `TODO.md`; those
documents are not competing status registers.

Next session entry point: Phases A, B, and C are COMPLETE and Phase D
is retired to the owner's separate tracking (2026-07-05) — the goldens
carry the fixture accounts, zero proxy remnants, and a provenance
manifest. The only remaining register item is the U8 release
convention: the 1.0 definition (A + B1/B2 + C1 + C3) is SATISFIED, so
the first tag (jointly with cloud-provision) can be cut at the next
consumer release-gate bake, User-run.

## Completion Model

The project is complete when all supported role and OS combinations in
`docs/STATUS.md` are verified end-to-end, known broken paths are fixed,
and the generated VMs provide the command-line tools required by the IOC
runtime workflows.

Each milestone closes only when its acceptance criteria pass on the real
testbed. Syntax checks alone are necessary but not sufficient.

The EtherCAT/RT validation harness (`ethercat_base`, `app_ethercat`) is
tracked separately under "EtherCAT Validation Harness" below and is **not**
part of this completion model: it validates the external `ethercat-env`
buildout on a Debian 13 bake + live-VM topology, and acceptance of that
buildout belongs to `ethercat-env` (M16/D2).

## Work Register

| Topic | Work unit | Type | Status | Evidence or next action |
|---|---|---|---|---|
| Base OS | Milestone 1: Base OS parity | Milestone | Complete | `docs/STATUS.md` marks `base_os` verified on Rocky 8 and Debian 13. |
| Applications | Milestone 2: Application role reliability | Milestone | Complete | `docs/STATUS.md` marks `app_con`, `app_procserv`, and `app_conserver` verified on both OS families. |
| EPICS | Milestone 3: EPICS environment deployment | Milestone | Complete | `docs/STATUS.md` marks `app_epics` verified on both OS families. Resolves GH #1 (Rocky 8 `epics_os_dir` mismatch) via per-OS `epics_os_dir` in `group_vars`; GH #1 closed 2026-06-09. |
| IOC runner | Milestone 4: IOC runner deployment | Milestone | Complete | `docs/STATUS.md` marks `app_ioc_runner` verified on both OS families. |
| NFS simulation | Milestone 5: NFS simulation and cross-OS closure | Milestone | Complete | `docs/STATUS.md` marks `nfs_sim` verified on Rocky 8 and Debian 13 ioc-runner server validation hosts. Resolves GH #2 (ioc-runner source on NFS-backed home) via the `04_nfs_sim.yml` source-root override (mechanism since removed by 3ea5c20 — see the dated amendments in Milestones 4 and 5); GH #2 closed 2026-06-09. |
| Repository identity | Public baseline and validation boundary | Design gate | Implemented | README and architecture describe a public Linux baseline, validation defaults, testbed defaults, and site overlays. |
| Makefile topology | Server-only NFS simulation targets | Design gate | Implemented | `04_nfs_sim` node targets are generated only for configured server node IDs. |
| Host setup | SSH key existence check | Carry-forward | Complete | `bin/setup_host.bash` warns when neither `~/.ssh/id_ed25519.pub` nor `~/.ssh/id_rsa.pub` is present, mirroring the `cloud-provision` host setup. |
| Base OS | RHEL sudo secure_path verification | Carry-forward | Complete | Verified 2026-07-02 on the rocky8 iocrunner golden: `sudo -n which con conserver` resolves `/usr/local/{bin,sbin}` (drop-in c5b3fbe). Scope: Rocky 8 only; Debian 13 needs no drop-in — its default secure_path already includes `/usr/local` (ARCHITECTURE.md OS-differences). |
| EtherCAT validation | EtherCAT/RT base image layer (`ethercat_base`, `05_ethercat_base`) | Validation harness | Implemented, unverified | Code present; bake-time prerequisite layer on `ethercat_build`. Verification is an external gate — cloud-provision `bake_ethercat_image.bash` then flatten to the `ethercat-debian13` golden image. Outside the core completion model. |
| EtherCAT validation | EtherCAT R2-12 live validation (`app_ethercat`, `06_ethercat`) | Validation harness | Implemented, unverified | Code present; clones `ethercat-env` and runs its target graph + RT reboot on the baked VM (`ethercat_nodes`). Verification is an external gate — live `debian13-ethercat` VM; acceptance belongs to `ethercat-env` (M16/D2). Outside the core completion model. |
| ioc-runner test fixtures | Multi-user `test_users` accounts (`roles/test_users`, `07_test_users`) | Carry-forward | Tracked, unwired | Role and playbook in tree but absent from `site.yml` / `CONFIG_SITE`; activation (B) pending a `07_test_users` bake step in cloud-provision `bake_iocrunner_image.bash`, re-bake, and verify. Plan: `docs/test_users_handoff.md`. |
| NFS bake fix | Drop app_ioc_runner from `04_nfs_sim`; default stdout callback | Carry-forward | Complete (review closed) | `3ea5c20` removes app_ioc_runner from `playbooks/04_nfs_sim.yml`; `3ccc8b8` sets the stdout callback to default. **Review closed 2026-07-03 (10-reviewer convergence, session rs20260702_083212): the removal is justified — in-place bake-time validation is impossible UNDER BECOME-ROOT against the root_squash 0750 nfs_sim mount (root maps to nobody), and no intended coverage was lost: the local source-root pass stays in `03_epics` and NFS-side coverage relocated to the consumer's tar-push + suite flow (epics-ioc-runner 1.2.0 release gate PASSED on goldens baked with the fix). The callback change stands; a `requirements.yml` collection install was REJECTED (cosmetic benefit; new proxied network fetch; one more unpinned input).** Origin: epics-ioc-runner M19 V002 bake on the site bake host (2026-06-26). |

| Full-repo review | 10-reviewer review convergence (rs20260702_083212) | Review | Complete | Ten lenses (raw IaC, bake seam, consumer coverage, docs coherence, security/ops, adversarial cross-check, EtherCAT, config architecture, operator experience, repo-family conventions). All Round-1 verdicts sustained under adversarial attack; outcome = Phases A-D below + decisions U1-U10. Authoritative convergence: conv20260702_190045 (session-local; verdict substance recorded in these rows). |
| Review follow-up | Phase A: documentation truth-sync | Carry-forward | Complete (2026-07-04, commits 2439e6c/bde669f + cloud-provision 4e99811) | One sitting, no behavior change: post-3ea5c20 sweep (README:128; ARCHITECTURE.md:38-41/:199-204/:215/:231/:51; SEAM.md:45/:62 + ethercat row to "present, unverified end-to-end"; register rows 40/42 issue-close notes; row 58 superseded-with-new-fate; M4/M5 dated amendment notes); site-overlay contract section (two planes, override points, custom-inventory caveat, vmadmin invariant); Update Protocol trigger extension (composition-or-claim-invalidating commits sweep the mirroring docs); honest dry-run wording (README, ANSIBLE_CLI, make help); README Roles (10) + Playbook Layers (01-07) discoverability; STATUS.md re-anchor + events; test_users defaults comment; TODO.md pointer stub (U3); site-identity string generalization (U9); cloud-provision ARCHITECTURE IP table (.70/.80). |
| Review follow-up | Phase B: raw-contract code must-dos | Carry-forward | Complete (2026-07-04, commits cc8e686/13d2910/544c487/4623e35; verified V1-V5 per handoff20260704_031000, integration rides the next re-bake) | B1 `set -e` + trailing `test -x` in app_con/app_procserv (silent-build-failure fix, empirically reproduced); B2 atomic sudoers replace (same-fs mktemp + `mv -f`); B3 one-page raw style contract doc (Tier-A patterns; playbook species; bake-path-raw-only vs Debian-13-live-module boundary); B4 config cleanup — delete `proxy_enabled` (or wire per U2) + `path_epics_src` + shadowed python lists, derive `path_ioc_runner_root` from `epics_ioc_engineers[0]`, gitignore `*.local`; B5 app_epics `test -f` before the profile.d write. |
| Review follow-up | Phase C: bake pipeline (BOTH bake scripts; cross-repo with cloud-provision) | Carry-forward | Complete (2026-07-05; ansible 9910fe2 + cloud a8bdbd4; both goldens re-baked and verified on fresh variants: fixture accounts baked [ioc=opa,opb; obs outside; usera/userb linger], proxy remnants NONE, manifest in-image + sidecar; consumer testplan fixture paragraph synced) | C1 wire 07_test_users into the bake + two-token make wiring + re-bake + verify + sync the consumer testplan fixture paragraph; C2 de-proxy cleanup before flatten + in-image remnant grep acceptance + proxied-site runbook in cloud-provision docs (placeholder values only) + failed-bake recovery paragraph; C3 provenance manifest in-image + sidecar (bake date, ansible-provision HEAD, cloud-provision HEAD, per-repo rev-parse before `rm -rf`, EPICS env/base versions, base image identity, `pip3 freeze`); C4 bake scripts honor INVENTORY/VM_PREFIX from one source. |
| Review follow-up | Phase D: EtherCAT verification readiness | Carry-forward | Retired from this register (2026-07-05, User direction) | The EtherCAT verification work is tracked separately by the owner outside this register; the U10(a)/(b) strictness decisions and the R7 readiness items (persist bundle HEAD + log retrieval; GRUB parse-miss FAIL per U10c; 7-step end-to-end run) move with it. The ethercat roles/playbooks stay in this repository (keep-in-repo verdict unchanged, split trigger recorded in the review convergence). |
| Policy | Review decisions U1-U10 | Decision record | Decided 2026-07-03 | U1 phases A+B now / C at re-bake / D when scheduled; U2 proxy runbook-first (role optional after); U3 TODO stub; U4 GitHub issues only for cross-repo/externally referenced items; U5 `repo_*_ref` pinning introduced empty-default, pinned at release-gate bakes (scope: git refs + pip + ethercat bundle); U6 selective sentinel `changed_when`; U7 dated amendment notes; U8 adopt family release convention jointly with cloud-provision — bare-number tags at release-gate bakes, register snapshot-restart, 1.0 = A + B1/B2 + C1 + C3 (retro-0.9 and CHANGELOG decided at tag time); U9 site-identity strings generalized in tracked files; U10 (c) decided FAIL-at-bake, (a)/(b) deferred. |

## Conceptual Integrity Findings

| Finding | Reality rank | Evidence | Fate to decide |
|---|---|---|---|
| Direct CLI examples disagree with the repository's no-Python operational contract. | Resolved in docs | `docs/ANSIBLE_CLI.md` uses `-m raw` for every ad-hoc example (lines 50, 53, 56, 59); no `shell` or `setup` module remains, consistent with `gather_facts: false` in `playbooks/01_base.yml:5`, `playbooks/02_apps.yml:5`, and `playbooks/03_epics.yml:5`. | Keep ad-hoc examples on `raw`; do not reintroduce `shell` or `setup` in public docs. |
| Pattern targets treat every playbook as valid for every OS and node, but `04_nfs_sim.yml` is scoped only to `nfs_sim_nodes`. | Resolved in design | `configure/CONFIG_SITE` now separates all-node and server-only playbooks; `configure/RULES_ANSIBLE` generates server-only node targets only from `SERVER_NODE_IDS`. | Verify `make help.detail` and confirm unsupported `04_nfs_sim.<os>.node1` targets are no longer generated. |
| `app_ioc_runner` and `nfs_sim` need separate local and NFS source-root coverage. | Superseded (2026-07-04, 3ea5c20) | Historical: `playbooks/04_nfs_sim.yml` overrode `path_ioc_runner_root`/`path_ioc_runner_src` and enabled `ioc_runner_force_setup`; that block was removed by 3ea5c20 because become-root cannot operate inside the root_squash 0750 nfs_sim mount. `inventory/group_vars/all.yml` still keeps the default local `path_ioc_runner_root`; `roles/nfs_sim/defaults/main.yml` still keeps the simulation symlink separate. | New fate: local coverage stays in `03_epics`; NFS-side coverage relocated to the consumer's tar-push + suite flow (epics-ioc-runner 1.2.0 gate PASS). Do not re-add app_ioc_runner to `04_nfs_sim` — root-principal in-place validation is impossible under root_squash by design. |
| NFS simulation paths carried a site-specific namespace. | Resolved in defaults | `roles/nfs_sim/defaults/main.yml` uses `nfs_sim_namespace: simulation` to build export and mount roots. | Keep site namespaces in overlays, not public defaults. |

## Milestone 1: Base OS Parity

### Objective

Establish a reliable base OS layer for Rocky 8 and Debian 13.

### Acceptance Criteria

- `01_base` applies successfully on Rocky 8 and Debian 13 hosts.
- Required operator and runtime tools are present after provisioning:
  `git`, `make`, `lsof`, `ss`, and `socat`.
- NTP service is installed, configured, enabled, and running.
- A second run is idempotent at the provisioning contract level.

### Verification

```bash
make 01_base.rocky8.server.check
make 01_base.debian13.server.check
make 01_base.rocky8.server
make 01_base.debian13.server
```

Post-apply verification:

```bash
ansible rocky8 -i inventory/testbed.ini -m raw -a "command -v lsof ss socat"
ansible debian13 -i inventory/testbed.ini -m raw -a "command -v lsof ss socat"
```

## Milestone 2: Application Role Reliability

### Objective

Make the application build roles fail visibly and verify their installed
artifacts.

### Acceptance Criteria

- `app_con`, `app_procserv`, and `app_conserver` fail on build or
  install errors instead of reporting ok after a partial failure.
- `con`, `procServ`, and `conserver` binaries are installed at the
  expected paths.
- The Rocky 8 `app_conserver` missing-binary defect is resolved.
- Debian 13 application roles are applied and independently verified.

### Verification

```bash
make 02_apps.rocky8.server.check
make 02_apps.debian13.server.check
make 02_apps.rocky8.server
make 02_apps.debian13.server
```

Post-apply verification:

```bash
ansible all -i inventory/testbed.ini -m raw -a "command -v con procServ conserver"
```

## Milestone 3: EPICS Environment Deployment

### Objective

Install and validate the EPICS runtime environment on both supported OS
families.

### Acceptance Criteria

- `03_epics` applies successfully on Rocky 8 and Debian 13 hosts.
- `epics_os_dir` resolves to an upstream-supported directory on each OS.
- `/etc/profile.d/epics-env.sh` sources successfully at login.
- EPICS base version and environment version match inventory selectors.
- Required EPICS commands are available in a login shell.

### Verification

```bash
make 03_epics.rocky8.server.check
make 03_epics.debian13.server.check
make 03_epics.rocky8.server
make 03_epics.debian13.server
```

Post-apply verification:

```bash
ansible all -i inventory/testbed.ini -m raw -a "bash -lc 'source /etc/profile.d/epics-env.sh && caget -h'"
```

## Milestone 4: IOC Runner Deployment

### Objective

Provision IOC runner hosts with the runtime, source tree, and inspection
dependencies required by `epics-ioc-runner`.

### Acceptance Criteria

- `ioc-runner` is installed at the expected path.
- `ioc-runner -V` reports stamped build metadata, not `unreleased`.
- The `epics-ioc-runner` source tree is available from the local source
  root during `03_epics`.
- The `epics-ioc-runner` source tree is available from the NFS-backed
  simulation source root during `04_nfs_sim`.
  *(Amended 2026-07-04: satisfied at acceptance time; the `04_nfs_sim`
  source-root mechanism was later removed by 3ea5c20. NFS-side
  coverage now lives in the consumer's tar-push + suite flow. Retained
  as the historical basis of the Complete status.)*
- `ioc-runner list -vv` and `ioc-runner inspect -h` run successfully.
- Target-specific `ioc-runner inspect <ioc>` is covered by lifecycle
  tests that create or install an IOC target.
- Lifecycle tests that depend on inspect pass their assertions.

### Verification

```bash
make 03_epics.rocky8.server
make 03_epics.debian13.server
```

Post-apply verification:

```bash
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner -V"
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner list -vv"
ansible all -i inventory/testbed.ini -m raw -a "ioc-runner inspect -h"
```

## Milestone 5: NFS Simulation and Cross-OS Closure

### Objective

Validate the NFS simulation role and close the role-by-OS matrix.

### Acceptance Criteria

- `04_nfs_sim` applies successfully on the configured NFS simulation
  hosts.
- Export paths, ownership, permissions, and service state match the
  documented architecture.
- `app_ioc_runner` applies successfully from the NFS-backed simulation
  source root without replacing the local source root.
  *(Amended 2026-07-04: satisfied at acceptance time; this pass was
  removed by 3ea5c20 — become-root cannot operate inside the
  root_squash mount. Coverage relocated to the consumer flow. Retained
  as the historical basis of the Complete status.)*
- Rocky 8 and Debian 13 both complete `01_base`, `02_apps`, `03_epics`,
  and `04_nfs_sim`.
- `docs/STATUS.md` has no unverified, broken, or not-yet-applied
  entries for supported role and OS combinations.
- Open items in `docs/STATUS.md` are either resolved or moved to
  `TODO.md` as explicitly deferred work.

### Verification

Default-inventory target topology:

```bash
make 04_nfs_sim.rocky8.server.check
make 04_nfs_sim.debian13.server.check
make 04_nfs_sim.rocky8.server
make 04_nfs_sim.debian13.server
make check
```

V7 completion evidence used the NFS/ioc-runner validation hosts from a
temporary inventory:

```bash
ANSIBLE_LOCAL_TEMP=/tmp/ansible-local ANSIBLE_SSH_CONTROL_PATH_DIR=/tmp/ansible-cp ansible-playbook -i /tmp/ansible-provision-nfs-v7.ini -e @inventory/group_vars/all.yml playbooks/04_nfs_sim.yml
```

Validated hosts:

| OS | Host | Address |
|---|---|---|
| Rocky 8 | `testbed-rocky8-iocrunner-server` | `192.168.122.150` |
| Debian 13 | `testbed-debian13-iocrunner-server` | `192.168.122.50` |

### Status

Complete for Rocky 8 and Debian 13 ioc-runner server validation hosts.
The NFS simulation uses the `simulation` namespace, keeps the local source
root separate from `gitsrc-nfs-sim`, and verifies root_squash behavior.

## EtherCAT Validation Harness

This scope is **outside the M1-M5 completion model**. It validates the
external `ethercat-env` buildout, not the core Linux provisioning baseline,
and runs on a Debian 13 bake + live-VM topology rather than the
`rocky8`/`debian13` server matrix.

### Components

- `ethercat_base` (`playbooks/05_ethercat_base.yml`, group `ethercat_build`):
  bake-time prerequisite layer — build toolchain, running-kernel headers,
  dkms, and the PREEMPT_RT kernel + headers installed but never made the boot
  default (decision D2). Applied on the transient rtbase build host and
  flattened into the `ethercat-debian13` golden image by cloud-provision's
  `bake_ethercat_image.bash`.
- `app_ethercat` (`playbooks/06_ethercat.yml`, group `ethercat_nodes`): live
  R2-12 validation — clones `ethercat-env` from a controller-side git bundle
  and runs its pre-reboot, RT boot-default change, reboot, post-reboot, and
  removal target sequences for real, capturing per-target logs under
  `/opt/ethercat-validation/logs`.

### Status

Code present, **unverified**. Verification is an external gate: it requires
the baked `ethercat-debian13` golden image and a live VM run, and the GRUB
menuentry parse is flagged best-effort pending its first real run. Acceptance
of the underlying buildout belongs to `ethercat-env` (M16/D2).

## Update Protocol

When a milestone is completed, update this document and `docs/STATUS.md`
in the same commit as the substantive change. The commit message should
name the milestone and the role or OS boundary that changed.

Additionally (extended 2026-07-04, review rs20260702_083212):

- Any commit that changes a playbook's role composition, or that
  invalidates a statement in this register, the `docs/STATUS.md`
  matrix or notes, or a recorded acceptance criterion, updates those
  documents in the same commit. The structure-mirroring locations are
  README.md (Playbook Layers, Roles), `docs/ARCHITECTURE.md`
  (sections 2, 3, 5), and `docs/SEAM.md` (consumer register).
- When a GitHub issue changes state, the next documentation commit
  reflects it in the affected register rows.
