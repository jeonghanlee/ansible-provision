Session ID: rs20260604_120138
Session Root: `/data/gitsrc/ansible-provision/review_sessions/20260604_120138_design_milestones`
Artifact ID: rev20260604_120138
Artifact Type: review_report
Acting As Role: Reviewer
Author Agent ID: codex_gpt5
Author Transport: codex
Author Model: GPT-5
Target Artifact ID: source20260604_120138
Supersedes Artifact ID: none

## Role Assertion

- Agent: codex_gpt5
- Acting As: Reviewer
- Role Source: explicit user direction in session rs20260604_120138 on 2026-06-04
- Artifact Type Allowed: yes; Reviewer may publish review_report per role-permissions.md.
- Target Path Allowed: `reviews/rev20260604_120138_codex_gpt5_initial.md` is within this role's write scope.
- Re-Anchor Trigger: session start

## Reviewed Scope

Reviewed the proposed design milestones in `00_source_design_milestones.md`
against the current `ansible-provision` working tree and the historical
shape of `/data/gitsrc/ansible-alsu-linux-os`.

Workflow size: M.

## Findings

### C1: Purpose Reframing Is Correct But Needs Strong Front-Matter

The source correctly reframes the repository around a public Linux
unification baseline plus EPICS validation. This should become the
first milestone because downstream role and Makefile decisions depend
on the repository identity.

Evidence:

- `README.md` currently describes an Ansible-based provisioner for
  cloud-provision testbed VMs.
- `docs/MILESTONES.md` currently tracks role verification before it
  states the public baseline model.

### C2: VM Lifecycle Is The Main Design Decision

DM3 is the critical fork. `ansible-alsu-linux-os` embedded a `virt/`
layer, but `ansible-provision` currently points at `cloud-provision`.
Both are defensible; allowing both to remain active would recreate
the same conceptual overlap.

Evidence:

- `ansible-alsu-linux-os/virt/create_vm.bash` owns VM image acquisition,
  seed generation, and readiness checks.
- `ansible-provision/README.md` points to `cloud-provision` as the
  testbed VM provisioner.

### C3: EPICS Validation Should Stay As A Validation Layer

DM5 and DM6 correctly keep EPICS and ioc-runner as proof that the Linux
baseline supports real control-system workflows. They should not become
the top-level repository identity.

Evidence:

- `playbooks/03_epics.yml` and `playbooks/04_nfs_sim.yml` validate
  application and NFS-backed operational behavior.
- `inventory/group_vars/all.yml` now separates `path_ioc_runner_root`
  from `path_ioc_runner_src`.

## Required Decisions

| ID | Decision | Blocks |
| --- | --- | --- |
| RD1 | Decide whether VM lifecycle remains delegated to `cloud-provision` or a minimal public `virt/` layer is added. | DM3, DM7 |
| RD2 | Decide whether `docs/MILESTONES.md` should become a design-first register or whether a separate design document should drive the rewrite. | DM1, DM9 |

## Verification Notes

Future implementation should include at least:

- `git diff --check`
- `ansible-playbook --syntax-check site.yml`
- `ansible-playbook --syntax-check playbooks/04_nfs_sim.yml`
- `make help.detail`
