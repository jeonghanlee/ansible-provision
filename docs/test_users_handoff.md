# Multi-User Test Fixture Accounts

## Scope

This document defines the `testusers` fixture accounts, their bake-time
placement, ordering, and verification.

**Out of scope:** the product IOC account and group are created by
`roles/iocrunner`; consumer scenarios are defined in
`epics-ioc-runner/gate/RUNBOOK.md`, which verifies these
accounts as a precondition and never creates them.

## Purpose

The iocrunner golden images carry fixed accounts for the consumer's
multi-user authorization and user-service scenarios. The fixture is applied
during the golden bake as part of the `iocrunner` species and is not part of
the `iocserver` species, which provisions a production IOC server.

## Integration

| Component | Integration |
| :-- | :-- |
| `roles/testusers/defaults/main.yml` | Defines fixture account and group inputs. |
| `roles/testusers/tasks/main.yml` | Creates the accounts through Python-free `raw` tasks. |
| `playbooks/operators/testusers.yml` | Targets `vacua`; run alone as `make op.testusers.<vacuum> RUNTIME_INVENTORY=<host inventory>`. |
| `configure/RELEASE` | Lists `testusers` in `OPERATOR_PLAYBOOKS`. |
| `playbooks/species/iocrunner.yml` | Imports the operator last, after `iocrunner`. |
| `playbooks/species/iocrunner_nfs.yml` | Applies the `iocrunner` species, then `nfs_sim`. |
| `playbooks/species/iocserver.yml` | Excludes the fixture by design. |
| cloud-provision `bin/bake_iocrunner_image.bash` | Applies the `iocrunner` or `iocrunner_nfs` species assembly as Step 4/8. |

## Accounts

| Account | Member of `ioc` | Consumer role |
| :-- | :-: | :-- |
| `opa` | Yes | Operator with system-mode lifecycle access. |
| `opb` | Yes | Second operator for ownership and concurrency scenarios. |
| `obs` | No | Observer negative control; state-changing actions are denied. |
| `usera` | No | Local-mode user with linger enabled. |
| `userb` | No | Second local-mode user with linger enabled. |
| `opc` | Yes | Operator with linger enabled, for one account running an IOC in local mode and then as a system service. |

The `ioc-srv` account and `ioc` group are product infrastructure from
`roles/iocrunner`, which runs the runner's `setup-system-infra.bash --full`.
This fixture adds only test accounts and group membership.

## Ordering and Data Flow

1. cloud-provision boots a fresh VM, resolves its address, and stamps the bake
   manifest (bake Steps 1-3).
2. The bake applies the species assembly (Step 4): the species operators
   install the IOC stack, the `iocrunner` operator creates the product IOC
   infrastructure, and `testusers`, the last operator of the `iocrunner`
   species, verifies that the `ioc` group exists and creates the fixture
   accounts. The `iocrunner-nfs` flavor then applies `nfs_sim`, which
   creates the NFS simulation boundary.
3. cloud-provision finalizes and validates the provenance, seals the proxy
   artifact contract, and shuts down and publishes the validated golden pair
   (Steps 5-8).
4. Fresh variants expose the accounts to the consumer test plan.

## Verification

The 2026-07-05 Rocky 8 and Debian 13 fresh variants established the following
accepted state:

- `opa` and `opb` exist and belong to `ioc`.
- `obs` exists and does not belong to `ioc`.
- `usera` and `userb` have systemd linger enabled.
- A clean reprovision from each golden preserves the fixture.

On 2026-09-28 fresh Rocky 8.10 and Debian 13 hosts applied through the
`iocrunner` species established `opc` in `ioc` with systemd linger enabled,
the other five accounts unchanged, and an unchanged re-apply of the operator;
the check on a fresh variant from the golden follows the next iocrunner bake.

Future verification must use a fresh variant from the golden under test. A
running overlay with manually created accounts is not evidence for the golden.
