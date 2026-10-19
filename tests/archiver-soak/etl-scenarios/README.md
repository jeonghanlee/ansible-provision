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

A caller supplies a private JSON payload. `run.py` verifies this directory's source manifest, exposes the existing `ROLE` and `PAYLOAD` interface and runs one named preserved payload. Optional arguments after `--` reach that payload's actual CLI. The runner never selects a VM or supplies authorization.

Launch and preparation payloads consume source bytes/hashes and absolute deployed paths from their declared payload keys. Their callers must supply those inputs explicitly; missing fields stop execution. Do not fill a configuration from a historical VM inventory or copy a private operational JSON file into this source directory.

## Live Execution Boundary

These payloads target the original isolated Rocky Linux 8.10/Python 3.9/systemd 239 deployment and its frozen native ETL tools. They can modify service units, source visibility, evidence directories and appliance state. Run them only on an explicitly selected dedicated test environment under the operator's authorization. Source preservation does not authorize execution.

Inspect `run.py --help` and the selected source before creating its private payload. The JSON must declare `role` as `etl`; `chain`, `case`, source hashes and deployed file paths follow the selected source's own contract. The payload files are executed source copies, not a claim that every historical variant or recipient replay succeeded.

An original short observation's `Incomplete` status and a successful negative-scenario expectation remain separate. Original data and manifests are never rewritten to make a checker succeed.

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

