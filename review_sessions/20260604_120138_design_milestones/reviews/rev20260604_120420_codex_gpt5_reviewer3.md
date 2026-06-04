Session ID: rs20260604_120138
Session Root: `/data/gitsrc/ansible-provision/review_sessions/20260604_120138_design_milestones`
Artifact ID: rev20260604_120420
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
- Target Path Allowed: `reviews/rev20260604_120420_codex_gpt5_reviewer3.md` is within this role's write scope.
- Re-Anchor Trigger: user direction at 12:04:20

# Reviewer 3 Report: VM/Testbed Lifecycle, Makefile Topology, Verification Gates

## Reviewed Scope

Reviewed `00_source_design_milestones.md` against the current repository
shape, focusing on VM/testbed lifecycle ownership, generated Makefile
targets, and verification gates before implementation.

## Findings

### R3-F1: DM3 must be a prerequisite gate before public-baseline rewrites

DM3 is currently phrased as a design milestone, but it should gate DM1,
DM2, and DM7. The repository still presents `cloud-provision` as the VM
source of truth in `README.md:3` and `README.md:17`, while the source
milestones explicitly ask whether a public `virt/` layer should be added.
If documentation is rewritten before this decision, the repository can
end up with two competing testbed lifecycle models.

Recommendation: mark DM3 as the first required owner decision. Keep
`cloud-provision` as the only documented VM lifecycle until the review
session converges on adding or rejecting a minimal public `virt/` layer.

### R3-F2: DM7 should define per-playbook topology, not only clean help text

The current Makefile model generates the same group and node targets for
every playbook listed in `configure/RELEASE:4`. The generator in
`configure/RULES_FUNC:13` through `configure/RULES_FUNC:45` has no
per-playbook host-scope concept, so it emits node targets for
`04_nfs_sim` even though `playbooks/04_nfs_sim.yml:4` targets only
`nfs_sim_nodes`. This is visible in generated output:
`make -n 04_nfs_sim.rocky8.node1` emits an ansible-playbook command
limited to `testbed-rocky8-node1`.

Recommendation: make DM7 deliverable explicit: introduce a playbook
topology model that distinguishes all-node stages from server-only or
out-of-band validation stages. Help text cleanup should be verification,
not the design itself.

### R3-F3: DM6 needs an apply-level verification gate, not syntax-only closure

The source milestone correctly requires both local and NFS-backed
ioc-runner source roots, and the current `04_nfs_sim` playbook overrides
`path_ioc_runner_root` and `path_ioc_runner_src` in
`playbooks/04_nfs_sim.yml:10` through `playbooks/04_nfs_sim.yml:15`.
However, `site.yml:3` through `site.yml:5` excludes `04_nfs_sim`, so
`make all` and `make check` do not exercise that layer. Syntax checks
can prove the playbook parses, but they cannot prove root_squash
behavior or NFS-backed `app_ioc_runner` execution.

Recommendation: DM6 should close only after real testbed apply on both
server hosts, plus post-apply checks for NFS mount state, source-root
location, `ioc-runner -V`, and `ioc-runner inspect`.

### R3-F4: DM9 should convert reviewer findings into ordered gates

The proposed milestones are valid, but DM9 should not be a generic plan
creation step. It should explicitly order the gates that block
implementation: VM lifecycle decision first, Makefile topology second,
then documentation and milestone register rewrites. Without that order,
implementation can start by rewriting purpose text while the testbed
source of truth remains unsettled.

Recommendation: DM9 deliverable should be a staged plan with gate IDs,
each gate naming the artifact that closes it and the commands or apply
checks required to pass.

## Reviewer 3 Position

The milestone set is directionally correct for a public Linux baseline
with an EPICS and IOC validation layer. The main change needed before
implementation is to promote VM lifecycle and Makefile topology from
ordinary milestones into explicit prerequisite gates.
