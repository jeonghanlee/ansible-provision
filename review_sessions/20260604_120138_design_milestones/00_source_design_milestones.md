Session ID: rs20260604_120138
Session Root: `/data/gitsrc/ansible-provision/review_sessions/20260604_120138_design_milestones`
Artifact ID: source20260604_120138
Artifact Type: source
Acting As Role: User
Author Agent ID: user
Author Transport: chat
Author Model: human
Target Artifact ID: none
Supersedes Artifact ID: none

# Source: Design Milestones For Repository Reorientation

## Background

The historical `ansible-alsu-linux-os` repository appears to be the
original internal attempt to unify ALS-U Controls Linux systems. It
contains VM provisioning, local verification inventories, OS baseline
roles, network/runtime roles, and site-specific operational roles.

The current `ansible-provision` repository should not import that
internal repository wholesale. The intended direction is to use this
repository as an externally shareable baseline, with ALS-U-specific
details left to an overlay or separate internal repository.

## Design Goal

Reorient `ansible-provision` around two explicit layers:

1. A public Linux system unification baseline.
2. An EPICS and IOC operational validation layer that proves the
   baseline supports local and NFS-backed operating conditions.

## Non-Goals

- Do not import ALS-U internal NTP hosts, proxy hosts, vault tokens,
  GitLab URLs, network names, DHCP/TFTP/Cockpit/camera details, or
  site-specific user identities.
- Do not reuse `ansible-alsu-linux-os` as the implementation base.
- Do not make VM provisioning depend on internal infrastructure.
- Do not start implementation until reviewer convergence and an
  approved development plan exist.

## Proposed Design Milestones

| ID | Milestone | Deliverable | Verification |
| --- | --- | --- | --- |
| DM1 | Define repository purpose and boundaries | Rewrite top-level docs so the repository is a public Linux provisioning baseline with EPICS validation, not a cloud-provision-only app deployer. | Docs name public baseline, overlay boundary, supported OS set, and non-goals. |
| DM2 | Establish Linux baseline architecture | Reorganize role descriptions around OS packages, time sync, shell tools, runtime dependencies, firewall, and Python policy. | Architecture doc maps every baseline role to a Linux unification function. |
| DM3 | Preserve testbed VM separation | Decide whether VM lifecycle stays in `cloud-provision` or whether a small public `virt/` layer is added here; document the source of truth. | One documented VM path exists with no competing testbed instructions. |
| DM4 | Split public defaults from site overlays | Ensure all public defaults are generic and identify overlay variables for internal NTP, proxy, users, repositories, and network shape. | No internal ALS-U-only values are required to run the public baseline. |
| DM5 | Define EPICS operational validation layer | Keep con, procServ, conserver, EPICS, ioc-runner, and NFS simulation as validation of the baseline rather than the repository's sole purpose. | Milestones and architecture separate baseline duties from validation duties. |
| DM6 | Validate local and NFS ioc-runner source roots | Preserve local `03_epics` coverage and NFS-backed `04_nfs_sim` coverage through variableized source roots. | Syntax checks pass and testbed apply proves both local and NFS source-root paths. |
| DM7 | Rationalize Makefile target topology | Align generated Make targets with playbook host scope, especially `04_nfs_sim` server-only behavior. | Help output and dry-run targets do not imply unsupported node scope. |
| DM8 | Remove stale artifacts and narrative drift | Remove unused templates and rewrite documents toward architecture, functional specifications, and data flow. | `rg` shows no stale template references; docs avoid troubleshooting history. |
| DM9 | Create a reviewer-approved implementation plan | Convert accepted review findings into a staged development plan with file-level changes and verification IDs. | Facilitator convergence exists and user approves the named plan before implementation. |

## Review Questions

1. Are the milestone boundaries correct for a public baseline plus
   site overlay model?
2. Should VM lifecycle remain outside this repository, or should a
   minimal public VM verification layer be added?
3. Is EPICS validation properly scoped as proof of the Linux baseline
   rather than as the primary repository identity?
4. Which milestones should be prerequisite gates before code edits?
