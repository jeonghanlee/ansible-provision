# Preserved ETL Scenario Payloads

## Scope

This directory provides preparation, unrelated-module challenge, source-unavailability, automatic-abort and replay payloads. Both fault runtime variants and the replay share the native package's UTC pass checker. An explicit retained-input mode checks that component on a control host without running a live fault scenario. Historical sources and outcomes remain in their original frozen packages and Git history.

**Out of scope:** connection inventories, SSH transport, automatic VM selection, private run data, accepting unexecuted default cases, and executing a new observation as part of source preservation.

## Components And Data Flow

| Component | Sources |
| --- | --- |
| Preparation and finite worker launch | `prepare-etl-nextcase-v3.py`, `prepare-etl-nextcase-v4.py`, `launch-etl-nextcase-preparation-v2.py`, `launch-etl-nextcase-runtime-v3.py` |
| Unrelated journal-module challenge | `apply-journal-challenge.py`, `run-etl-independence-v2.py` |
| Native readiness and actual fault boundary | `etl-native-preflight-v2.py`, `preflight-etl-fault-boundary.py` |
| Actual source-access faults | `etl-fault-sampler.py`, `run-etl-fault.py`, `run-etl-fault-v2.py` |
| Frozen checks and private evidence archives | `replay-etl-fault.py`, `replay-etl-independence.py`, `archive-etl-fault-v4.py`, `archive-etl-independence-v6.py` |
| Retained-pass CLI regression | `test-retained-pass.py`, both fault runtime variants, `replay-etl-fault.py`, `../etl-pass/evidence.py` |
| Native journal query and capture regression | `test-journal-query.py`, both fault runtime variants, `../etl-pass/evidence.py` |

A caller supplies a private JSON payload. `run.py` verifies this directory's source manifest, exposes the existing `ROLE` and `PAYLOAD` interface and runs one named preserved payload. Optional arguments after `--` reach that payload's actual CLI. The runner never selects a VM or supplies authorization.

Launch and preparation payloads consume source bytes/hashes and absolute deployed paths from their declared payload keys. Their callers must supply those inputs explicitly; missing fields stop execution. Do not fill a configuration from a historical VM inventory or copy a private operational JSON file into this source directory.

## Live Execution Boundary

These payloads target the original isolated Rocky Linux 8.10/Python 3.9/systemd 239 deployment and its frozen native ETL tools. They can modify service units, source visibility, evidence directories and appliance state. Run them only on an explicitly selected dedicated test environment under the operator's authorization. Source preservation does not authorize execution.

Inspect `run.py --help` and the selected source before creating its private payload. The JSON must declare `role` as `etl`; `chain`, `case`, source hashes and deployed file paths follow the selected source's own contract. The payload files are executed source copies, not a claim that every historical variant or recipient replay succeeded.

An original short observation's `Incomplete` status and a successful negative-scenario expectation remain separate. Original data and manifests are never rewritten to make a checker succeed.

## Journal Query Component

Both fault runtime variants call `evidence.capture_case_journals` after terminal capture. This operation reads `observation.json`, uses its precise `started_at` and derives the sampler and abort units from `observe.SAMPLER` and `collect.ABORT_UNIT`. It queries both roles independently with the normal 60-second deadline. Query diagnostics remain separate from ETL pass evidence.

`started_at` requires `YYYY-MM-DDTHH:MM:SS`, optional one-to-nine fractional digits, and `Z` or a valid `+HH:MM`/`-HH:MM` offset. The native lower argument is whole-second UTC rounded down. Selection retains each complete record exactly when its decimal `__REALTIME_TIMESTAMP` in epoch microseconds, multiplied by 1000, is at least the original integer nanosecond bound. There is no upper, fault-end or current-boot filter. Native `-u` matching also includes systemd's messages about the unit.

Raw stdout/stderr, argv, original/native bound, source identities, process lifetime, deadline and actual termination facts are saved before evaluation. Each role has `actual-*-journal.json`, `.stdout`, `.stderr` and a separate `.selected.jsonl`. Identical occurrences remain counted; conflicting cursors, duplicate JSON fields and missing cursor/boot/realtime identities are unusable. Process-name fields are optional. A failed or unreadable query is Incomplete and cannot establish an empty interval.

Use Python 3.9 or newer and the actual systemd 239 binary for native compatibility. Component mode runs before live ETL preflight or service changes. Its private payload has `role`, `chain`, `case`, `mode`, `contract` and `output`, using the same validated chain/case values as retained-pass mode. Use `mode: "check-journal-query"` for native queries or `mode: "check-journal-capture"` for selection over proven native captures. The latter cannot establish native query acceptance. Unknown modes are refused.

The journal context uses these fields:

| Field | Required input |
| --- | --- |
| `schema`, `chain`, `case` | `1` and the payload's declared chain/case |
| `candidate` | Frozen complete `archiver-soak` source tree, including both scenario callers, their manifest and the native package |
| `inputs` | Frozen actual observation copy, independent expectation and full expected JSONL records |
| `native` | Frozen complete selected native journal files; these become explicit `--file` inputs |
| `comparison` | Frozen common comparator source and its required dependencies |
| `unit_roles` | `sampler` and `abort`, matching the production modules |
| `observation`, `expectation`, `comparator` | Canonical relative paths below their respective roots |
| `native_command` | Actual `path`, `sha256` and effective component `uid`; optional `query_uid` declares an isolated unreadable-source control |
| `timeout_seconds` | Optional finite positive component deadline; normal production retains 60 seconds |
| `captures`, `capture_roles` | Capture-only mode's frozen receipts, native originals, marked derivatives and provenance mappings |

Each frozen specification is an object with absolute `root`, absolute `manifest` and independently pinned manifest `sha256`. The manifest contains a nonempty `members` object mapping every canonical relative regular-file name to its SHA-256. Keep the manifest outside its root. Missing, extra, changed or linked members prevent queries. `contract` and the fresh `output` must be absolute; output cannot overlap any frozen input or package root.

The expectation supplies the untouched `lower_bound`, independently calculated `query_lower_bound`, production `unit_roles`, per-role `records` paths and per-role `allow_empty` flags. Derive records from a successful broad native unit query without `--since`, then use independently observed stored timestamps to select its complete due population. Declare an expected empty selection explicitly. Do not derive expectations from the candidate query.

The common `compare-evidence.py` CLI compares each usable role separately with `format=jsonl`, identity fields `__CURSOR` and `_BOOT_ID`, numeric field `__REALTIME_TIMESTAMP` in epoch microseconds, no ISO timestamp fields and full records (`fields=null`). Native and comparator outcomes have separate receipts. A completed component returns Passed/0 only when both required roles agree; an observed difference returns Failed/1 even alongside another unresolved role; otherwise missing or unusable evidence returns Incomplete/2. An interrupted collector retains actual status 130 or 143 and its child's final outcome. Normal execution does not require a comparator or expected-input file.

For capture-only mode, `capture_roles` maps each role to `receipt`, `provenance`, `native_stdout`, `native_stderr`, `stdout` and `stderr` paths below `captures`. Preserve the original native receipt unchanged. Provenance pins its hash, both native byte-file hashes and `original_returncode`, and names any controlled derivative. Malformed or missing-field derivatives establish capture validation only.

```bash
scenarios=/path/to/frozen/archiver-soak/etl-scenarios
payload=/path/to/private/journal-payload.json
python3 -B "$scenarios/run.py" --source run-etl-fault.py --payload "$payload"
python3 -B "$scenarios/run.py" --source run-etl-fault-v2.py --payload "$payload"
```

Use a different fresh output for each invocation. The context cannot override production units or supply a replacement preformatted bound.

## Journal Regression Inputs And Execution

Create the fixture only on an authorized isolated target where both production unit names are unused. Two finite test-owned writers use those exact names; a third unit supplies unrelated records. Record every declared marker and acknowledge each through real journald, including cursor, boot, stored realtime and writer completion. Require at least three distinct stored timestamps per selected role and a fractional bound with real earlier records in the same second. Record actual marker cadence and elapsed time; these bounded writers do not establish an ETL scenario or full-day retention.

After writers stop, retain successful `journalctl --sync` and `--rotate` receipts. Select the complete closed archived population from recorded journal roots, checking native headers. Record membership, sizes and hashes before copying to a fresh native directory; re-enumerate originals and require exact source/copy agreement. Run actual native verification and broad unit queries on the copies, accounting for all markers before freezing expected inputs. Preserve unsuccessful attempts. Never vacuum, repair or recreate original files from JSON output.

The reusable regression CLI requires a private complete configuration:

```bash
cases=/path/to/private/journal-cases.json
output=/path/to/private/fresh-journal-results
python3 -B "$scenarios/test-journal-query.py" --cases "$cases" --output "$output"
```

The configuration has `cases`, `cell_inventory`, `snapshot_guard`, `archive_guard` and `dependency_guard`. `cases` contains exactly the 60 IDs in `test-journal-query.py`'s `CASES`. Each entry supplies `id` and `runs`; each run identifies `caller`, frozen `contract`/`contract_sha256`, optional component `mode`, and `expected` component `status`, `verdict` and per-role `groups`. Expected group fields assert actual receipt values; `native_nonzero` and `native_status_retained` require an observed integer native status. A guard entry uses `caller: "runner"` and executes once.

`cell_inventory` pins a separate `path`/`sha256` JSON file with complete `[case, caller, role, collector_signal]` cells, derived independently from the declared applicability. All normal native, capture and component-guard cases cover both callers and both roles. Original parser refusal uses the original caller; rounded-extra exposure uses v2. Preserve pre-fix packages with their original formatter and unfiltered selection. Both corrected controls use the same original inputs. Replay cases execute fresh verified copies. Wrong-bound/unit packages change the actual production operation, have valid complete manifests and must reach native queries; integrity refusal does not expose that defect.

`snapshot_guard` uses the frozen native-member specification. `archive_guard` pins a `manifest`/`sha256` whose JSON contains actual journal `roots` and complete selected archived `members`, each with `path`, `size` and `sha256`. `dependency_guard` similarly pins a JSON `files` mapping of actual resolved execution dependencies to hashes. Verify all originals and copied inputs before and after each launch. Source consumption checks inspect both normal call sites independently of actual native behavior checks.

The four exact/one-microsecond/one-nanosecond boundary cases declare `target_role` and run a separate observation copy at each role's own observed entry instant for both callers. Both unit queries still run; the required cell identifies the role whose actual timestamp supplies that boundary.

Process-fault runs additionally declare `target_role`, optional `collector_signal` (2 or 15), and positive `maximum_attempts`. Each timeout and child-signal case targets each role for both callers; collector interruption covers both signals for each role/caller. The runner stops only the identified owned native query, confirms its stopped state, records measured exposure and then lets the deadline expire or applies the declared signal. An early exit leaves that attempt unmet; a retry starts in a new directory only after termination is confirmed. Finalization retains partial output, actual native status and child termination. Unconfirmed termination prevents another process-fault case.

The runner preserves every attempt, per-role expectation, actual native/component outcome and final coverage. Omitted, duplicate or unknown cases are rejected before launch; separate child invocations verify those guards without recursion. The snapshot-change guard modifies a test copy only. Suite status zero means every required cell ran and met its stated expectation, including intentional negative outcomes. It does not accept ETL functionality, missing historical output, full fault/abort scenarios or an independent recipient. Run `test-retained-pass.py` separately on actual retained E3/E4 evidence after shared-module or dispatcher changes.

## Retained-Pass Component

Use Python 3.9 or newer on a control host. This mode reads private retained files and separate original/candidate native packages, then writes only a fresh result directory. It runs before live preflight, service queries, source changes or observation setup. It does not establish complete fault handling, normal finish, restoration, recipient replay or full-day behavior. Other retained-record analysis remains available under `../diagnostics/`.

Prepare an original native package containing its unchanged `bundle.json` and all declared source members. Bind its hashes to the original observation and scenario declaration. Prepare a separate candidate native package containing every source named by `contract.BUNDLE_FILES` from the selected candidate source tree. Create its new bundle only inside that private candidate directory:

```bash
native=/path/to/private/candidate-native
python3 -B "$native/contract.py" --freeze "$native"
```

Never regenerate an original observation's bundle or compare candidate hashes with the old observation's `tool_hashes`. Freeze external member manifests for the original package, candidate package and selected input directory separately. Each member manifest is a JSON object with a nonempty `members` object mapping canonical relative regular-file paths to SHA-256 values. Its own SHA-256 is independently pinned in the context below. The declared members must equal the complete directory membership; symlinks and path traversal are rejected. Keep member manifests outside the directories they describe.

A private context uses this structure; all root, manifest, contract and output paths must be absolute. The input names and field paths are explicit mappings to the actual captures, not synthesized observations:

```json
{
  "schema": 1,
  "original": {
    "root": "/private/original-native",
    "manifest": "/private/original-members.json",
    "sha256": "<original-member-manifest-sha256>"
  },
  "candidate": {
    "root": "/private/candidate-native",
    "manifest": "/private/candidate-members.json",
    "sha256": "<candidate-member-manifest-sha256>"
  },
  "inputs": {
    "root": "/private/inputs",
    "manifest": "/private/input-members.json",
    "sha256": "<input-member-manifest-sha256>"
  },
  "callers": {
    "run-etl-fault.py": "<candidate-caller-sha256>",
    "run-etl-fault-v2.py": "<candidate-caller-sha256>",
    "replay-etl-fault.py": "<candidate-caller-sha256>"
  },
  "checks": [
    {
      "name": "E3",
      "case": "E3",
      "chain": "shortened",
      "declaration": "E3/declaration.json",
      "observation": "E3/observation.json",
      "passes": "E3/passes.jsonl",
      "identity": {"path": "E3/identity.json", "field": ["identity"]},
      "begin": {"path": "E3/identity.json", "field": ["observed_at"]},
      "end": {"path": "E3/upper-bound.json", "field": ["recorded_at"]}
    }
  ]
}
```

The declaration must supply `case`, `chain`, `tool_hashes` and `target_native_sts_pass` with integer `transition`, positive integer `cadence` in seconds and `planned_at`. The observation supplies the original `tool_hashes`. The identity reference resolves to nonempty `boot_id` and `invocation_id` strings. Bind that independently captured process lifetime to the selected source and measured interval. Each begin/end reference resolves to an actual original timestamp. Declare the meaning of a conservative measurement bound explicitly; do not manufacture a missing restoration time. Pass inputs contain the complete selected native JSONL population with original cursors, invocation fields and messages.

For a runtime variant, create a private payload with `role: "etl"`, `chain`, `case`, `mode: "check-retained-pass"`, `contract` and `output`. The latter two fields contain absolute paths to the context and a fresh output directory. Both variants use the existing runner:

```bash
scenarios=/path/to/selected/source/etl-scenarios
payload=/path/to/private/retained-payload.json
python3 -B "$scenarios/run.py" --source run-etl-fault.py --payload "$payload"
python3 -B "$scenarios/run.py" --source run-etl-fault-v2.py --payload "$payload"
```

Use a different fresh `output` for each invocation. Its parent must exist. The replay component accepts the same context directly:

```bash
pass_contract=/path/to/private/context.json
pass_output=/path/to/private/fresh-result
python3 -B "$scenarios/replay-etl-fault.py" --check-retained-pass --contract "$pass_contract" --output "$pass_output"
```

An unrecognized non-null runtime `mode` returns `Incomplete`/2 before live execution. Omitting `mode` retains the live scenario contract. Full replay requires `--case` and keeps its original stage, source, fault and terminal requirements.

### Matching And Results

The native pass parser preserves source-cursor deduplication. The checker requires exactly one distinct pass matching transition, cadence, appliance invocation and the exact planned UTC instant, then applies the existing successful-pass execution contract. Identical repeated cursors deduplicate; conflicting payloads at one cursor are unusable, and distinct matching cursors remain ambiguous. Original strings and selected payload fields remain unchanged.

Every required timestamp must use `YYYY-MM-DDTHH:MM:SS`, optional one-to-nine fractional digits, and `Z` or `+HH:MM`/`-HH:MM`. Offset hours must be 00-23 and minutes 00-59. Missing timezones, invalid dates/offsets, non-string values and excess precision are unusable. Selection and inclusive `begin <= startedAt <= endedAt <= end` comparison use integer UTC nanoseconds without rounding or a tolerance.

| Tool result | Native status | Meaning |
| --- | --- | --- |
| `Passed` | 0 | Exactly one declared successful pass lies inside the valid interval |
| `Failed` | 1 | Usable evidence establishes a missing/ambiguous pass, execution violation or interval violation |
| `Incomplete` | 2 | Required evidence, source identity, invocation or parsing is unusable |

The private `result.json` retains individual checks, selected records, separate original/candidate identities and native status. A confirmed violation in one complete group remains `Failed` alongside an independently unusable group. Stdout reports only the aggregate verdict, reason and native status. These are component tool results; they do not rewrite an original controller result or determine ETL product acceptance.

### CLI Regression

`test-retained-pass.py` requires actual E3 and E4 fixture contexts. Supply this private case configuration:

```json
{
  "phase": "corrected",
  "fixtures": {
    "E3": "/private/E3-context.json",
    "E4": "/private/E4-context.json"
  },
  "scenario_root": "/path/to/selected/source/etl-scenarios",
  "common_root": "/path/to/complete/test-framework"
}
```

Each fixture context contains one check for its named case. The runner rejects a missing case or a fixture mapped to the other case before starting commands. Add `expected_witness` to that check as a `path`/`field` reference to an independently accepted original pass receipt. The regression uses this reference only for interval-edge controls; declaration and independent identity establish the expected matching values. Keep its source/hash provenance with the private input contract. Do not derive expectations from the checker under test.

```bash
pass_cases=/path/to/private/cases.json
pass_results=/path/to/private/fresh-regression
python3 -B "$scenarios/test-retained-pass.py" --cases "$pass_cases" --output "$pass_results"
```

The runner copies real inputs, native packages and scenario sources, then starts all three actual CLIs. It covers equivalent offsets/fractions, one-nanosecond differences, identity/cadence changes, missing/duplicate/conflicting records, invalid timestamps/bounds, unsuccessful execution, integrity and invocation failures. Known positive selections also run through the shipped common `compare-evidence.py` CLI. That compact comparison selects transition, invocation, planned time and cadence in seconds; other fields remain outside the common comparison and are retained for the native domain checks. Separate common controls cover changed identity/time, missing/extra occurrences and unusable inputs.

Fresh processes repeat positive and missing-pass cases on verified separate copies. Receipts preserve before-launch snapshots, argv/cwd, interpreter/tool identities, actual execution times, stdout/stderr, native statuses and replay agreement. Exit 0 means every expected case outcome was observed; expected negative commands may return 1 or 2. A missing required fixture or case cannot become a skipped success.

The `pre-fix` phase runs only the unchanged positive fixtures through all three CLIs and expects the original literal-comparison defect: zero matches and `Failed`/1. Run it against a separately identified production extraction frozen before the UTC correction. It is defect exposure, not an unchanged historical binary or complete-scenario acceptance. Keep that extraction and its receipts separate from the corrected candidate.

## Maintenance Boundaries

ETL test-tool work is tracked in [#54](https://github.com/jeonghanlee/ansible-provision/issues/54). The canonical milestone document owns component scope and observed completion. Preserve original source copies and evidence identities when comparing a corrected candidate.

The local `SHA256SUMS` covers this source directory. Each recorded observation's native bundle is a separate immutable input. An edit requires a new source manifest and explicit real-path verification; it does not retroactively change the source identity of earlier observations.

