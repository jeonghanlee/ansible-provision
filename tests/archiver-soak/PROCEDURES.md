# Shared Test Evidence Procedures

## Scope

Use this procedure to select reusable sources and private evidence, verify a
transfer, and interpret original or candidate replay results. It connects the
existing tools; each test retains its own signals, timing, exposure and
acceptance rules.

**Out of scope:** deployment, starting or stopping an observation, replacing an
installed bundle, repairing a test, and deciding product acceptance from a
generic helper result. Follow the [ETL contracts](README.md#execution-contracts),
[Journal procedures](journal-validation/README.md), and
[scenario contracts](etl-scenarios/README.md) for those operations. Current work
and verification status belong to the [canonical record](../../docs/milestone-38560eb.md).

## 1. Select The Claim And Actual Inputs

Record the question, original observation and tool identities, required input
members, expected native result, comparison fields and allowed output location
before running a command. Select the complete population required by that claim,
including unsuccessful attempts and controls. A summary or retained hash does
not supply a missing raw input.

For retained archives, check the archive and inventory hashes against the
independently retained preservation record. Inspect the member list and excluded
files before extraction. Extract only into a fresh private location; reject
absolute paths, traversal, unsupported links and special files. Compare the
required extracted members with the preserved list and hashes. An archive hash
alone proves neither extraction completeness nor suitability for replay.

If a required original was retired, record the unavailable member and the claim
it prevents. Do not reconstruct observations from summaries, regenerate their
manifests, or launch another long observation as an implicit recovery step.

| Test | Evidence and interpretation that remain test-specific |
| --- | --- |
| ETL | Chain, store transitions, planned pass times, producer lifetime, actual physical/HTTP data, measurement coverage and terminal facts. Scheduling waits are not processing time. |
| Journal | Producer schedule, exact source identities, direct-query bounds, collector intervals, retention/restart windows and frozen package. A short basic probe does not satisfy one-hour or full-day acceptance. |
| Buffer | Actual write-delay exposure, full/compact record contract, original unsuccessful preflight, expected-loss control and positive window. Exact fast-PV equality differs from slower-PV activity/counter coverage. |

Preserve UTC text and precision for correlation, and use the declared monotonic
clock and boot boundaries for elapsed requirements. Do not add overlapping
durations or substitute configured rates, array capacity or zero error counters
for observed records, lengths or fault exposure.

## 2. Keep Sources And Private Evidence Separate

Reusable scripts, fixtures and procedures belong under this source tree. Keep
raw captures, PB exports, JFR/CSV data, operational logs, command receipts,
credentials, host/VM identifiers and deployment-specific configuration in private
storage outside it. An ignored directory prevents accidental Git selection; it
does not make its contents safe to share.

Use role names and replaceable paths in public instructions. Inspect both file
content and metadata before export. If an authorized export needs redaction,
retain the original privately and identify the export as a separate derivative;
do not present it as byte-identical replay evidence.

| Source selection | Integrity record | Use |
| --- | --- | --- |
| Current reusable checkout | Parent and child `SHA256SUMS`, with independent Git membership | Check the current source population, including procedures. |
| Original observation | Its recorded package/bundle and evidence member records | Reproduce the original execution with its original tools. |
| Candidate tools | Separate source identity and member record | Evaluate a correction on verified copies without replacing originals. |

Run the actual [current source checker](README.md#current-source-integrity).
The parent manifest includes child manifests; updating a child requires updating
the parent entry. Update hashes only for intentionally changed reusable files.
Never refresh an original observation manifest to make current tools match it.
For a candidate copy, retain the owning Git checkout as the independent
inventory; missing files must not disappear from both sides of the check.

The shared `test-framework` helpers are external tools, not members of this
repository's source manifest. Select a verified helper package and retain its
script hashes, interpreter identity and declared executable dependencies with
the private invocation. A hash check does not install prerequisites or establish
that an installed service uses the checked files.

## 3. Package And Verify An Eligible Command Receipt

Use `bundle-evidence.py` only for a completed, trusted, read-only command receipt
with frozen input/tool trees and matching same-prefix `.stdout` and `.stderr`
files. The source-check and comparison suites produce this contract. Their
`.input.json` metadata files are not command receipts.

The receipt must contain actual `argv`, `cwd`, `native_returncode`, distinct
`input_root`/`package_root`, available `input_snapshot`/`tool_snapshot`, complete
`input_members`/`tool_members`, and executable `dependencies` with resolved paths
and hashes. Members include modes and regular-file hashes or supported directory
and relative-link identities. An unfinished status, missing snapshot or current
filesystem reconstruction cannot substitute for this execution record.

Another producer's `returncode` field does not make its receipt compatible.
Adapt only an actual completed child status into a separate receipt, retain the
original streams and mapping, and supply the complete frozen contract. Validate
that adapter through the real pack/verify/replay path before claiming support.
Do not send lifecycle, service-control or fault-injection commands to this helper.

Use POSIX Python 3.8 or later. Set `transfer` to the selected shared helper and
replace every private example path. Each output must be new, below an existing
private parent and outside the frozen trees:

```bash
transfer=/path/to/test-framework/scripts/bundle-evidence.py
receipt=/private/retained/command.json
python3 -B "$transfer" pack --receipt "$receipt" --output /private/pack-001
```

This form requires a captured `cwd`. Only when the recorded command needs no
external working-directory content, use the alternative `pack --empty-cwd`
option. It declares a fresh empty working directory; replay must still prove
agreement. Path arguments must be complete arguments under captured roots or
declared executable dependencies. Embedded paths and arbitrary shell commands
are unsupported.

Keep the returned `manifest_sha256` independently of the bundle being sent. Copy
the complete `bundle` with modes and supported relative symlinks intact; the
helper does not perform the transfer. For a local copy to a new destination:

```bash
bundle=/private/pack-001/bundle
received=/private/received-bundle
cp -a -- "$bundle" "$received"
bundle=$received
pin=REPLACE_WITH_INDEPENDENTLY_RETAINED_SHA256
python3 -B "$transfer" verify --bundle "$bundle" --manifest-sha256 "$pin" --output /private/verify-001
```

Replace `pin` with the retained 64-character lowercase digest. A digest obtained
only from the received directory is not an independent integrity check.
Verification checks the exact manifest/helper identity, complete membership,
modes, hashes and recipient executable hashes. It does not run the target or
version probes. Stop on unusable inputs or mismatches; preserve the report and
resolve the missing evidence instead of editing the frozen manifest.

## 4. Replay Originals And Candidates Separately

For an eligible transferred receipt, replay on fresh copies:

```bash
python3 -B "$transfer" replay --bundle "$bundle" --manifest-sha256 "$pin" --output /private/replay-001
```

The recipient must have the identical helper and declared executables. Replay
checks executable hashes and recorded packaging-time version-probe results,
verifies copied membership immediately before launch, and runs the real argument
array without a shell. It records command bytes and native status before judging
agreement, then checks that the bundle and read-only copies are unchanged.
Inherited environment, shared libraries and undeclared subprocess dependencies
are not a fully frozen environment. A same-host replay does not prove another
recipient's behavior.

The helper reproduces the recorded tools; it is not a corrected-tool comparator.
Use a separate original replay and candidate result for a correction. Verify the
same required evidence against the original independent member record before
each launch, identify the candidate tools/dependencies, and declare the expected
change and unchanged fields before comparison. Keep stdout, stderr, native
status, input/tool hashes and before/after integrity checks for both runs.

Use the native test entry point when an observation is not an eligible portable
receipt:

- Journal: run the saved package's `basic.py replay` or `long.py replay` on a
  verified evidence copy, as described in its README. Full-day replay enforces
  the original frozen helpers and tool identity. Replacing those bytes is not
  an original replay; preserve any refusal when evaluating a candidate.
- ETL: follow [terminal replay](README.md#terminal-command-receipts-and-replay)
  with explicit, non-overlapping input/tool/output paths and a compatible JFR
  executable. `--action replay` does not run start/finish/abort. Runtime agreement
  is an additional declared check, not an assumption about historical results.
- Buffer: select its retained runner and explicit full or compact input contract.
  Omitted writes cannot be reconstructed from `write_count`; a generic record
  comparison does not replace the real delay/exposure validator. Keep unavailable
  main-trace inputs distinct from available preflight records.

Explicit CLI paths do not necessarily relocate paths embedded in historical
inputs. Check the selected entry point before running it. In particular,
[diagnostic modes](diagnostics/README.md#execution-contract) can still query live
services or original files; copying an archive alone does not supply those
dependencies. Never run such a mode as if it were a portable offline replay.

For `compare-evidence.py`, configure actual source/lifetime keys, timestamp
precision, numeric units and full or compact fields. Preserve occurrence counts;
compare exact UTC instants rather than timestamp spellings. Its Passed result
covers only the declared records and fields, not producer completeness or product
acceptance. Do not remove differing paths or fields merely to obtain agreement.

## 5. Interpret And Retain Results

Read the native result and the wrapper report separately. Exit conventions belong
to each entry point; there is no universal mapping from a process exit to product
acceptance.

| Operation | Required interpretation |
| --- | --- |
| Source checker | Status 0 means selected membership and checksums pass; 1 reports a check/input/tool error, and argument errors use 2. No product verdict is established. |
| Portable receipt replay | Operation Passed/0 means native status and raw output agree on unchanged verified copies. Failed/1 means executed output/status differs; Incomplete/2 means required evidence or execution is unusable. |
| Same-host source/comparison suite replay | Inspect `matches_recorded` and the native status. Reproducing an expected native failure can return 1. |
| ETL terminal replay | Read `replay_verdict`, each consumer's native findings and `lifecycle_verdict` separately. A Passed replay can preserve Incomplete product/lifecycle evidence. |
| Native Journal or ETL evaluation | Read named acceptance, violation and missing-coverage fields. These CLIs can return 1 for either Failed or Incomplete; the report supplies the distinction. |

A reproduced native failure can therefore be successful replay agreement. An
expected negative test can pass its expectation while the underlying observation
remains Failed or Incomplete. A confirmed violation remains visible when another
claim lacks evidence. CLI help, syntax checks, a matching subset and skipped tests
do not establish runtime coverage.

Preserve successful and unsuccessful command receipts, arguments/cwd, UTC and
elapsed bounds, streams, native statuses, frozen identities, output comparisons
and unresolved claims. The portable helper writes `command.running.json`, final
`command.json` and raw streams before `result.json`; retain partial files after
interruption. INT/TERM returns 130/143 there; a forced kill may leave no final
report. An incomplete package without its final manifest is not a usable bundle.

Keep original outcomes unchanged. Record candidate findings separately and retain
all required evidence before any cleanup. A source check, transfer verification,
replay agreement and product acceptance are distinct claims in the final record.
