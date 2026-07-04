# Raw Style Contract

The platform constraint behind this repository: the Rocky 8 targets
cannot support Python-backed ansible modules, so every dual-OS and
bake-path task uses `ansible.builtin.raw` with `gather_facts: false`.
This page names the house conventions that make raw safe. New and
edited tasks follow them; deviations need a recorded reason.

## Conventions

1. **`set -e` in every multi-command raw block.** A raw task fails
   only on nonzero rc; without `set -e` a failed middle command is
   masked by a succeeding tail (the historical app_con/app_procserv
   defect).
2. **Trailing assertion for every install/build block.** End with
   `test -x <binary>` (or `test -f`/`test -d` as appropriate) so the
   task proves its postcondition instead of implying it. Reference
   shape: `roles/app_conserver/tasks/main.yml`.
3. **Quoted heredocs for file payloads** (`<< 'EOF'`): Jinja templates
   the content; the target shell must not expand it.
4. **Jinja-to-shell-variable, then quote.** Assign a templated value
   to a shell variable once and use `"${var}"` thereafter, for any
   value used more than once or containing a path
   (`roles/app_ioc_runner/tasks/main.yml` shape).
5. **Honest change reporting where change visibility matters**
   (decision U6, review rs20260702_083212): mutating blocks that an
   operator would want to see in PLAY RECAP use the sentinel pattern —
   print `changed`/`unchanged` and set
   `changed_when: "<reg>.stdout | trim == 'changed'"`
   (see the chrony and sudoers tasks in `roles/base_os`).
   `changed_when: false` is correct for pure probes and for
   validation-harness tasks; it is not a default for mutations.
6. **Validated, atomic writes for privileged config.** Build in a
   same-filesystem temp file, validate (`visudo -cf` for sudoers),
   set mode/owner, then `mv -f` (atomic rename). Never copy over a
   live privileged file.
7. **Explicit failure paths.** On a guard or validation failure, print
   one clear line to stderr and `exit 1`; never `|| true` away a
   mutating command's failure.

## Two Playbook Species

- **Convergent provisioning** (01-04, 07): idempotent; re-runs
  converge or skip; guards protect completed work.
- **Run-once validation harness** (06_ethercat): deliberately
  non-convergent — it re-clones and re-executes by design and says so
  in its role header. Do not "fix" a harness into convergence.

## Module-Use Boundary

Raw-only everywhere, with one scoped exception for Debian-13-only
LIVE roles — see `ARCHITECTURE.md` section 5 ("Module-Use Boundary").
Never modules on a bake path.

## Check Mode

`ansible.builtin.raw` is skipped in check mode. `make check` and the
`.check` targets validate inventory, reachability, and template
rendering only — they are not a change preview (stated in README and
ANSIBLE_CLI).
