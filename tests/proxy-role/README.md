# Proxy Role Verification

The suite executes `roles/proxy` through `ansible-playbook` on one dedicated
Rocky Linux 8.10 guest. It uses the shipped cloud-provision contract and its
independent `tests/fixtures/proxy-artifacts.tsv` inventory. No role function,
renderer, filesystem operation, SSH connection, or service command is replaced.

## Preconditions

- A prepared Rocky Linux 8.10 guest assigned to this test by its VM provider,
  with the site baseline and producer proxy artifacts present.
- Its private runtime inventory, inventory name, and provider-verified domain
  UUID. The play requires exactly that inventory host and verifies the UUID
  and OS before changing files.
- Key-only SSH and the guest's configured Ansible become access.
- A landed cloud-provision commit or tag containing reconciliation support,
  visible on a remote-tracking branch. The runner requires the actual script
  and fixture to match that commit byte for byte. `PROXY_CONTRACT_ROOT` selects
  another checkout; `PROXY_CONTRACT_FIXTURE` selects the matching fixture path.

The suite changes proxy configuration to a reserved test endpoint. It removes
or changes managed files deliberately and must run only on its dedicated guest.
It does not install Archiver, use a production host, or remove a VM.

## Scope selection

`PROXY_TEST_SCOPE` defaults to `cloud`, using the producer's
`tests/fixtures/proxy-artifacts.tsv` and schema-1 completion receipt.
`general-server` selects `tests/fixtures/proxy-general-server-artifacts.tsv`,
schema-2 input and lock checks, and a completion receipt containing the scope.
Use producer commit `bbd689211e537b2f42cc3cf09e674049f5150fbc` for general-server.
The script and selected fixture must match the landed producer revision.

The general-server guest must have neither a `vmadmin` account nor its home.
Use its provider-assigned existing SSH account. The suite checks that condition
before mutations, then checks account databases and excluded SSH/sudo settings
after every successful reconciliation. The original cloud sequence retains
its default scope. The real-target suite remains gated by the provider UUID
for either scope.

For controller-only checks, `make check-general-server-contract` executes
actual Make expansion, inventory resolution, Ansible syntax, and the SQLite
assembly expansion. It also executes the shipped read-only group guard on
localhost with an unspecified checkout owner and requires rejection. The complete
development SQLite assembly runs in check mode to verify its skipped-build
conditions, using the controller's real OS probes. This does not reconcile proxy
artifacts or provision the controller. Run this check before the dedicated-guest suite.

After the general-server role suite and its receipt succeed, the runner adds
temporary membership in `archiver_server_sqlite` for the same verified guest
and runs that complete assembly in check mode. Its read-only prerequisite uses
the existing root account as the test checkout owner. Provisioning raw tasks
remain skipped. A failed full-group check makes the runner fail.

Both runners remove inherited Ansible tag filters before verification. The
guest runner explicitly selects all tags with no skipped tags for its suite and
group check. The group check requires both Archiver drift and build-wait tasks
to be reached; a successful recap alone is insufficient.

`bash tests/check-proxy-role-tag-contract.bash` verifies this behavior locally.
It observes and forwards the guest runner's real Ansible calls in both scopes,
using empty inventories and requiring receipt refusal. It then executes the
complete local contract with inherited run, skip, and Make tag filters. This
check requires the landed producer checkout and establishes tag selection and
local check-mode behavior, without executing a guest suite.

## Execution

Run from the ansible-provision checkout after setting the values from the
provider's private handoff:

```bash
export RUNTIME_INVENTORY=/path/to/dedicated-guest.ini
export TARGET_HOST=dedicated-guest
export PROXY_TEST_UUID='<provider-verified-domain-uuid>'
export PROXY_CONTRACT_REF='<landed-producer-commit-or-tag>'
KEEP_WORKSPACE=1 bash tests/check-proxy-role.bash
```

The runner captures the Ansible log, generated test variables, producer commit,
committed input files, and source checksums in a private temporary workspace.
Every successful role application checks the actual staged script against the recorded
contract SHA-256. The runner retains that workspace on failure
or when `KEEP_WORKSPACE=1`; otherwise it removes the workspace after success.
The final task writes a private controller completion receipt only after all
guest assertions and the fresh SSH check succeed. The runner requires that
receipt to match the assigned host, UUID, and contract hash before reporting
success. Empty inventories and hosts outside the play cannot report success.
The general-server runner also requires its complete group check to succeed
with no changes or unreachable hosts. Syntax checks alone do not establish
reconciliation behavior.

## Test Assertions

- Missing Maven settings are repaired while the profile marker exists.
- Every fixture identity recovers from missing content, ownership changes,
  mode changes, and managed content changes.
- Shared files retain unrelated environment, Git, DNF, and SSH settings.
- Shared modes `0600` and `0640` survive unchanged; unsafe `0666` modes return
  to the fixture baseline.
- Identical reapplication reports unchanged and preserves managed content and
  inode, link count, mtime/ctime, and SELinux context, including a caller that
  still supplies `proxy_force=true`.
- Linked control files and a writable runtime directory are rejected. Test
  controls are restored through `always` tasks covering preparation and refusal
  checks. A preparation command that fails restores its own partial changes.
- Proxy URLs containing shell substitution, heredoc termination, or trailing
  newlines fail without executing commands or changing final artifacts.
- The guest's real `sshd` validates its configuration and remains active; a
  fresh SSH connection retains the configured become access.
- The complete general-server assembly runs through every imported operator
  in check mode and safely handles the skipped build result.

After testing, return a finished notice to the VM provider. VM shutdown and
disk retention follow the provider's resource authorization.
