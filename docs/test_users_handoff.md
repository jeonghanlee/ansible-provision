# Multi-User Test Fixture Accounts

## Scope

This document defines the `test_users` fixture accounts, their bake-time
placement, ordering, and verification.

**Out of scope:** product IOC accounts are created by `app_ioc_runner`;
consumer scenarios are defined in `epics-ioc-runner/docs/testplan.md`.

## Purpose

The iocrunner golden images carry fixed accounts for the consumer's
multi-user authorization and user-service scenarios. The fixture is applied
during the golden bake and is not part of the product `site.yml`.

## Integration

| Component | Integration |
| :-- | :-- |
| `roles/test_users/defaults/main.yml` | Defines fixture account and group inputs. |
| `roles/test_users/tasks/main.yml` | Creates the accounts through Python-free `raw` tasks. |
| `playbooks/07_test_users.yml` | Targets `nfs_sim_nodes`; available through server-only Make targets. |
| `configure/CONFIG_SITE` | Includes `07_test_users` in `SERVER_ONLY_PLAYBOOKS`. |
| cloud-provision `bake_iocrunner_image.bash` | Runs `07_test_users.yml` after `04_nfs_sim.yml` as Step 6/9. |
| `site.yml` | Excludes the fixture by design. |

## Accounts

| Account | Member of `ioc` | Consumer role |
| :-- | :-: | :-- |
| `opa` | Yes | Operator with system-mode lifecycle access. |
| `opb` | Yes | Second operator for ownership and concurrency scenarios. |
| `obs` | No | Observer negative control; state-changing actions are denied. |
| `usera` | No | Local-mode user with linger enabled. |
| `userb` | No | Second local-mode user with linger enabled. |

The `ioc-srv` account and `ioc` group are product infrastructure from
`app_ioc_runner`. This fixture adds only test accounts and group membership.

## Ordering and Data Flow

1. `site.yml` creates the product IOC infrastructure.
2. `04_nfs_sim.yml` creates the NFS simulation boundary.
3. `07_test_users.yml` verifies that the `ioc` group exists and creates the
   fixture accounts.
4. cloud-provision removes site-proxy state, finalizes the bake manifest, and
   flattens the golden image.
5. Fresh variants expose the accounts to the consumer test plan.

## Verification

The 2026-07-05 Rocky 8 and Debian 13 fresh variants established the following
accepted state:

- `opa` and `opb` exist and belong to `ioc`.
- `obs` exists and does not belong to `ioc`.
- `usera` and `userb` have systemd linger enabled.
- A clean reprovision from each golden preserves the fixture.

Future verification must use a fresh variant from the golden under test. A
running overlay with manually created accounts is not evidence for the golden.
