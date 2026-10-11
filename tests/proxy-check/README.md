# Proxy Check Target Verification

`tests/check-proxy-check-target.bash` executes the `proxy_check` role through
`ansible-playbook` against one dedicated guest with Ansible become. It uses the
pinned cloud-provision checker and the producer's shipped unmarked fixture.
No role task, wrapper, checker, filesystem operation, or SSH connection is
replaced. The local controller check is `tests/check-general-server-contract.bash`.

## Preconditions

- One disposable guest assigned to this test by its VM provider, reachable by
  key-only SSH with Ansible become to root. The suite rewrites the six proxy
  files and a private input; it must never run on a production host.
- The provider's domain UUID for that guest. The suite compares it with the
  target's DMI product UUID and stops before any change on a mismatch.
- A runtime inventory file that defines the host, and an existing account on
  the target to serve as the checkout owner (`epics_ioc_engineers`).
- A cloud-provision checkout whose `bin/proxy_contract.bash` equals the SHA-256
  pinned in `roles/proxy_check/defaults/main.yml`, with
  `tests/fixtures/proxy-general-server-unmarked` and
  `tests/fixtures/proxy-general-server-artifacts.tsv`. The suite refuses a
  checker whose hash differs from the pin.

## Usage

```bash
tests/check-proxy-check-target.bash --inventory <file> --host <name> --uuid <uuid> --target rocky8 --owner <account>
tests/check-proxy-check-target.bash --inventory <file> --host <name> --uuid <uuid> --target non-rocky --owner <account>
```

| Option | Meaning |
| --- | --- |
| `--inventory` | Runtime inventory that defines `--host` |
| `--host` | Inventory host name of the guest |
| `--uuid` | Provider-verified domain UUID of the guest |
| `--target` | `rocky8` for a Rocky Linux 8.10 guest; `non-rocky` for any other OS |
| `--owner` | Existing account on the target used as the checkout owner |
| `--contract-root` | cloud-provision checkout; default is the sibling directory |
| `--input-path` | Private input path on the target; default `/etc/server-configuration/proxy-check.input` |
| `--runtime-dir` | Producer runtime state directory; default `/run/cloud-provision` |
| `--logs` | Directory for per-case play logs; default is inside the workspace |

The suite adds the host to the `rocky8` and `archiver_server_sqlite` groups of
a temporary inventory so that the assembly guard reaches the checker. It exits
nonzero on any failed case. `KEEP_WORKSPACE=1` retains the workspace.

## Guest state and restoration

Before the first change the suite copies the six artifact files, the private
input path, and the runtime directory to a guest-local backup directory and
records the original state of each path. It refuses to run when that backup
directory already exists. On exit, including after a failure, it restores every
path from the backup, removes the input directory only when the suite created
it, and compares the restored state with the original snapshot.

## Cases

| Target | Cases |
| --- | --- |
| `rocky8` | Input absent; other values (needs-change, with and without `--check`); matching unmarked files (ready, with and without `--check`, protected files unchanged); runtime state removed; different desired value; input pin differs from the executed source; role pin differs from the staged source; input mode 0644; input symlink; empty and relative input path; control character in a file; focused `archiver_build` stops before any build task; cloud scope skips the check; no input value in any play output |
| `non-rocky` | Input absent; fixture input refused with `runtime.os.unsupported-platform` with and without `--check`; no operator runs; protected files unchanged; no input value in any play output |

The result establishes the role and checker behavior on the tested target
with root become. It does not establish behavior on a host that never carried
the provider's default account, and it does not install the Archiver.
