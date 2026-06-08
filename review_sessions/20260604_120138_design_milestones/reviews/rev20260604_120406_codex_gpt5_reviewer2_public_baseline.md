Session ID: rs20260604_120138
Session Root: `/data/gitsrc/ansible-provision/review_sessions/20260604_120138_design_milestones`
Artifact ID: rev20260604_120406
Artifact Type: review_report
Acting As Role: Reviewer 2
Date: 2026-06-04
Start Time: 12:01:38
Finalized At: 2026-06-04 12:04:06
Author Agent ID: codex_gpt5
Author Transport: codex
Author Model: GPT-5
Target Artifact ID: source20260604_120138
Supersedes Artifact ID: none
Reviewer Agent ID: codex_gpt5_reviewer2
Reviewer Model: GPT-5
Repository: `/data/gitsrc/ansible-provision`
Review Mode: static review
Workflow Size: M
Skill References: `agent-review-convergence`, `technical-discussion`

## Role Assertion

- Agent: codex_gpt5_reviewer2
- Acting As: Reviewer 2
- Role Source: explicit user direction in session rs20260604_120138 on 2026-06-04.
- Artifact Type Allowed: yes (Reviewer may publish review_report).
- Target Path Allowed: yes (`reviews/rev20260604_120406_codex_gpt5_reviewer2_public_baseline.md` is within Reviewer write scope).
- Re-Anchor Trigger: user direction

## Executive Summary

The proposed design milestones point in the right direction for a public,
shareable Linux baseline with site overlays. The main gap is that the current
repository still presents itself as a cloud-provision testbed application
deployer, while the proposed milestones want it to become a baseline
architecture with EPICS/ioc-runner as validation.

## Reviewed Scope

- `00_source_design_milestones.md`
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/MILESTONES.md`
- `inventory/group_vars/all.yml`
- `inventory/testbed.ini`
- `ansible.cfg`
- `configure/CONFIG_SITE`
- `configure/RULES_FUNC`

## Findings

### R2-F1: DM1 Must Precede The Other Milestones

Severity: high

The proposed DM1 is correctly named, but it should be treated as a gate before
DM2 through DM8. The current repository identity still says "cloud-provision
testbed VMs" and "deploys con, procServ, conserver, EPICS, and ioc-runner",
which makes the validation layer read like the primary product.

Evidence:

- `README.md:3` defines the repository as a provisioner for
  cloud-provision testbed VMs.
- `README.md:4` leads with application deployment.
- `docs/ARCHITECTURE.md:5` calls it an application provisioner.
- `docs/ARCHITECTURE.md:13` through `docs/ARCHITECTURE.md:40` make
  cloud-provision the first architectural node and EPICS readiness the terminal
  state.

Recommendation: make DM1 a prerequisite gate and require the first edit stage
to rewrite the top-level purpose, boundary, and layer model before role or
Makefile restructuring.

### R2-F2: DM3 Needs A Strong "One Testbed Source Of Truth" Decision

Severity: high

DM3 asks whether VM lifecycle stays in `cloud-provision` or a minimal public
`virt/` layer is added. This is the right decision point, but it must be closed
before changing inventory or Make targets. The repository currently hardcodes a
specific testbed topology in multiple places, so adding a second VM lifecycle
path without first choosing ownership would make the public baseline less
shareable.

Evidence:

- `ansible.cfg:2` defaults to `inventory/testbed.ini`.
- `configure/CONFIG_SITE:1` also defaults to `inventory/testbed.ini`.
- `configure/CONFIG_SITE:5` through `configure/CONFIG_SITE:8` define a testbed
  topology shape.
- `docs/ARCHITECTURE.md:84` through `docs/ARCHITECTURE.md:107` documents fixed
  cloud-provision addresses and groups.

Recommendation: keep DM3 as an early prerequisite gate. My preference is to
keep VM lifecycle outside this repository for the first reorientation, then
document `inventory/testbed.ini` as an example inventory rather than the
baseline's identity.

### R2-F3: DM4 Should Separate Public Defaults From Validation Defaults

Severity: medium

DM4 correctly names site-overlay separation, but the current defaults combine
generic baseline values, public validation repositories, fixed local users, and
EPICS validation settings in one `all.yml`. That is not site-internal leakage,
but it weakens the public/shareable baseline boundary because public baseline
defaults and validation-layer defaults are not separated.

Evidence:

- `inventory/group_vars/all.yml:7` through `inventory/group_vars/all.yml:9`
  defines public NTP defaults.
- `inventory/group_vars/all.yml:19` through `inventory/group_vars/all.yml:43`
  defines baseline packages.
- `inventory/group_vars/all.yml:45` through `inventory/group_vars/all.yml:50`
  defines validation-layer repositories.
- `inventory/group_vars/all.yml:56` and `inventory/group_vars/all.yml:76`
  assume the `vmadmin` user for ioc-runner paths and IOC engineer membership.

Recommendation: expand DM4 to require variable classification, for example
baseline defaults, validation defaults, testbed defaults, and overlay-required
site values. This can remain documentation-first, but the implementation plan
should eventually move or label these groups so an external user can see which
settings are reusable and which are testbed-specific.

### R2-F4: DM5 And DM6 Correctly Preserve EPICS As Validation

Severity: low

DM5 and DM6 are correctly scoped. They protect an important acceptance layer
without letting EPICS or NFS become the repository identity.

Evidence:

- `docs/MILESTONES.md:12` through `docs/MILESTONES.md:13` identifies the next
  entry point as NFS-backed ioc-runner verification.
- `docs/MILESTONES.md:40` through `docs/MILESTONES.md:42` records the remaining
  local/NFS source-root and target-topology conceptual integrity findings.
- `inventory/group_vars/all.yml:56` through `inventory/group_vars/all.yml:59`
  now supports source-root override and forced setup.

Recommendation: keep DM5 and DM6, but place them after the baseline and overlay
boundary decisions. They should verify the architecture, not define it.

## Required Decisions

| ID | Decision | Blocks |
| --- | --- | --- |
| R2-D1 | Is DM1 a hard prerequisite gate before all implementation edits? | DM2-DM8 |
| R2-D2 | Should the first implementation keep VM lifecycle delegated to `cloud-provision` and treat `inventory/testbed.ini` as an example? | DM3, DM7 |
| R2-D3 | Should DM4 explicitly classify variables into baseline, validation, testbed, and overlay-required groups? | DM2, DM4, DM5 |

## Recommended Implementation Order

1. DM1: rewrite repository identity and boundaries.
2. DM3: decide and document VM lifecycle ownership.
3. DM4: classify defaults and overlay boundaries.
4. DM2 and DM5: map roles into baseline versus validation layers.
5. DM6 and DM7: finish local/NFS ioc-runner validation and target topology.
6. DM8: remove stale artifacts and narrative drift.
7. DM9: convert converged decisions into the approved implementation plan.

## Verification Notes

Static verification for the implementation plan should include:

- `git diff --check`
- `make help.detail`
- `ansible-playbook --syntax-check site.yml`
- `ansible-playbook --syntax-check playbooks/04_nfs_sim.yml`
- `rg -n "cloud-provision|testbed VMs|application provisioner" README.md docs`

Runtime verification should remain tied to the chosen VM source of truth and
must prove both the local `03_epics` ioc-runner source root and the NFS-backed
`04_nfs_sim` source root.
