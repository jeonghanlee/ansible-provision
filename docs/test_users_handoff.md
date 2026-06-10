# Handoff: multi-user test fixture accounts (test_users)

The `test_users` role and `playbooks/07_test_users.yml` are tracked in the
tree but **not wired and not applied**: they are absent from `site.yml` and
from the `CONFIG_SITE` playbook lists, so no make target or import runs them.
This document is the plan to activate them.

## Purpose

Bake the user accounts the epics-ioc-runner `docs/testplan.md` multi-user
scenarios need into the iocrunner-test golden, following the `04_nfs_sim`
precedent: a test/sim aid applied on top of `site.yml` during the bake, never
part of the product `site.yml`.

The test plan itself is the source of truth and lives in the other repo:
`/data/gitsrc/epics-ioc-runner/docs/testplan.md`. This role only provisions
its fixtures.

## Review status

Owner review: **conditionally approved**. Both conditions are satisfied:

- `set -e` at the top of each multi-line raw block (operator/observer/local) in
  `roles/test_users/tasks/main.yml`, so an early account failure cannot be
  masked by a later success.
- `docs/testplan.md` references qualified with the repo name
  (`epics-ioc-runner docs/testplan.md`) in tasks, defaults, playbook.

`ansible-playbook --syntax-check` passed with the role. The first run needed a
writable Ansible local tmp due to the sandbox — re-run with
`ANSIBLE_LOCAL_TEMP=/tmp` (or `ANSIBLE_HOME=/tmp/ansible`) if you hit the same.

Application is paused by the owner; activate per "Remaining work" when ready.

## Design decisions (settled — do not re-litigate)

- **`raw` module, not `user`/`group` modules** — mirrors `nfs_sim` so it runs on
  the freshly booted bake VM without Python.
- **Not in `site.yml`** — applied only as a bake step, so plain base images and
  the ethercat variant never get test accounts.
- **`hosts: nfs_sim_nodes`** — the bake build VM (`testbed-rocky8-server` /
  `testbed-debian13-server`) is in that group; matches `04_nfs_sim`.
- **Passwordless accounts** — the test model drives them via `sudo -u <user>`
  from `vmadmin`, not direct SSH; operators reach the `%ioc` NOPASSWD sudoers
  path. Passwordless is the correct fixture posture, not a gap.

## Accounts

| Account | Group `ioc` | Role in epics-ioc-runner `docs/testplan.md` |
| :-- | :-: | :-- |
| `opa`, `opb` | yes | operators — full system-mode lifecycle (sudoers `%ioc` gate) |
| `obs` | no | observer — negative control, state changes denied at the sudo gate |
| `usera`, `userb` | no | local-mode users (linger on) — `systemctl --user` isolation |

The product accounts (`ioc-srv`, `ioc` group) are NOT created here; they come
from `setup-system-infra.bash` via the `app_ioc_runner` role. This role only
adds the test fixtures and joins the operators to the existing `ioc` group.

## Tracked artifacts (in tree, unwired)

| Path | State |
| :-- | :-- |
| `roles/test_users/defaults/main.yml` | tracked, unwired |
| `roles/test_users/tasks/main.yml` | tracked, unwired |
| `playbooks/07_test_users.yml` | tracked, absent from `site.yml` and `CONFIG_SITE` |

## Ordering dependency

`07_test_users.yml` must run AFTER `site.yml` + `04_nfs_sim.yml`, because the
operators join the `ioc` group that `app_ioc_runner` creates. The first task
verifies the group exists and fails if the order is wrong. The bake step is
therefore inserted right after the `04_nfs_sim` step.

## Remaining work (activation — not done)

1. cloud-provision — edit `bin/bake_iocrunner_image.bash`: add the
   `07_test_users.yml` step right after the `04_nfs_sim` step and renumber the
   `Step N/6` labels to `N/7`. Snippet:

   ```bash
   # --- new step block (insert after the 04_nfs_sim subshell) ---
   printf "\nStep 5/7: Apply 07_test_users.yml on %s\n" "${VM_NAME}"
   ( cd "${ANSIBLE_DIR}" && "${ANSIBLE_PLAYBOOK_BIN}" \
       -i inventory/testbed.ini --limit "${VM_NAME}" playbooks/07_test_users.yml )

   # --- label changes elsewhere in the script (every N/6 becomes N/7) ---
   #   "Step 1/6: Boot"                          -> "Step 1/7: ..."
   #   "Step 2/6: Refresh known_hosts for VM IP" -> "Step 2/7: ..."
   #   "Step 3/6: Apply ansible site.yml"        -> "Step 3/7: ..."
   #   "Step 4/6: Apply 04_nfs_sim.yml"          -> "Step 4/7: ..."
   #   "Step 5/6: Shutdown and flatten qcow2"    -> "Step 6/7: ..."
   #   "Step 6/6: Cleanup build VM"              -> "Step 7/7: ..."
   ```

2. Re-bake both goldens:
   - `make -C /data/gitsrc/cloud-provision bake.rocky8`
   - `make -C /data/gitsrc/cloud-provision bake.debian13`

## Verify after bake

Provision a fresh variant from the rebaked golden (a clean reprovision, so you
test the golden and not a leftover overlay), then check the accounts:

- `make -C /data/gitsrc/cloud-provision rocky8-iocrunner.server.clean rocky8-iocrunner.server`
- `make -C /data/gitsrc/cloud-provision rocky8-iocrunner.server.status`
- `ssh vmadmin@<ip> 'getent group ioc; id opa; id obs; ls /var/lib/systemd/linger'`

Expect: `ioc` group lists `opa,opb`; `id opa` shows `ioc`; `id obs` has no `ioc`;
`usera` and `userb` appear under the linger directory.

## Notes

- The accounts created at runtime on the currently-running testbed are a
  bootstrap in the overlay only (for immediate scenario runs); the bake makes
  them durable in the golden. A `.clean` drops the overlay bootstrap.
- Nothing here touches epics-ioc-runner. The product `site.yml` is unchanged.
