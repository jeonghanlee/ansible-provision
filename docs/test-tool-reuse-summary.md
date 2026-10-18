# Test Tool Reuse Summary

Prevent repeated long tests caused by collection, finalization or verification errors. The categories distinguish reusable procedures from current implementations; each implementation needs a short real test in its target environment.

## 1 Reuse Procedures Without Changes

- Define the objective, required evidence and success criteria before execution. Separate independent functional results, diagnostic errors and expected fault outcomes; missing required evidence remains Incomplete.
- Exercise the real collection, normal stop, final save, evaluation and replay in a short run before a long observation. Include failure and interruption paths.
- Preserve original evidence, tools and results; correct and replay separate copies. Report actual progress, duration and coverage instead of predicted counts.

## 2 Reuse With Small Adaptations

- Source membership and checksum checks: configure roots, manifests and exclusions. Example: [shared check-sources.py](https://github.com/jeonghanlee/dev-env/blob/4c633385302cea3dcbc5b1c0f37f6eb8b6104b91/shared/skills/test-framework/scripts/check-sources.py).
- Evidence comparison: adapt field names, record formats and units; compare actual identities, process lifetimes and equivalent timestamps at the required precision. Declare full versus compact input contracts.
- Transfer and replay receipts: configure dependencies, paths and commands; retain member hashes, command output, errors and exit status before evaluating results.

## 3 Keep Domain Implementations Separate

- Journal: systemd 239 queries, journal cursors, boot/invocation matching and live-retention checks.
- ETL: IOC/PV fixtures, PB encoding/decoding, STS/MTS/LTS scheduling, physical/HTTP equality and source-fault scenarios.
- Buffer: Java instrumentation, delay injection, sample-buffer behavior and frequency-specific loss assertions.

These implementations are domain examples; another product or backend can require substantial rewriting.

Source work: [Journal #53](https://github.com/jeonghanlee/ansible-provision/issues/53), [ETL #54](https://github.com/jeonghanlee/ansible-provision/issues/54), [Buffer #55](https://github.com/jeonghanlee/ansible-provision/issues/55), [Shared #56](https://github.com/jeonghanlee/ansible-provision/issues/56).
