# Preserved ETL Scenario Payloads

## Scope

This directory preserves the executed preparation, unrelated-module challenge, source-unavailability, automatic-abort and replay payloads. The sources retain their actual checks, including unsuccessful controller comparisons. They provide a traceable starting point for collector and verifier maintenance.

**Out of scope:** connection inventories, SSH transport, automatic VM selection, private run data, accepting unexecuted default cases, and executing a new observation as part of source preservation.

## Components And Data Flow

| Component | Sources |
| --- | --- |
| Preparation and finite worker launch | `prepare-etl-nextcase-v3.py`, `prepare-etl-nextcase-v4.py`, `launch-etl-nextcase-preparation-v2.py`, `launch-etl-nextcase-runtime-v3.py` |
| Unrelated journal-module challenge | `apply-journal-challenge.py`, `run-etl-independence-v2.py` |
| Native readiness and actual fault boundary | `etl-native-preflight-v2.py`, `preflight-etl-fault-boundary.py` |
| Actual source-access faults | `etl-fault-sampler.py`, `run-etl-fault.py`, `run-etl-fault-v2.py` |
| Frozen checks and private evidence archives | `replay-etl-fault.py`, `replay-etl-independence.py`, `archive-etl-fault-v4.py`, `archive-etl-independence-v6.py` |

A caller supplies a private JSON payload. `run.py` verifies this directory's source manifest, exposes the existing `ROLE` and `PAYLOAD` interface and runs one named preserved payload. Optional arguments after `--` reach that payload's actual CLI. The runner never selects a VM or supplies authorization.

Launch and preparation payloads consume source bytes/hashes and absolute deployed paths from their declared payload keys. Their callers must supply those inputs explicitly; missing fields stop execution. Do not fill a configuration from a historical VM inventory or copy a private operational JSON file into this source directory.

## Execution Boundary

These payloads target the original isolated Rocky Linux 8.10/Python 3.9/systemd 239 deployment and its frozen native ETL tools. They can modify service units, source visibility, evidence directories and appliance state. Run them only on an explicitly selected dedicated test environment under the operator's authorization. Source preservation does not authorize execution.

Inspect `run.py --help` and the selected source before creating its private payload. The JSON must declare `role` as `etl`; `chain`, `case`, source hashes and deployed file paths follow the selected source's own contract. The payload files are executed source copies, not a claim that every historical variant or recipient replay succeeded.

Use `../diagnostics/` for retained-record analysis. An original short observation's `Incomplete` status and a successful negative-scenario expectation remain separate. Original data and manifests are never rewritten to make a checker succeed.

## Maintenance Boundaries

Collection, preparation, module independence and lifecycle work belongs to [#34](https://github.com/jeonghanlee/ansible-provision/issues/34). UTC pass matching and evaluation/reporting work belongs to [#35](https://github.com/jeonghanlee/ansible-provision/issues/35). Preserve original source copies and evidence identities when comparing a corrected candidate.

The local `SHA256SUMS` covers this source directory. Each recorded observation's native bundle is a separate immutable input. An edit requires a new source manifest and explicit real-path verification; it does not retroactively change the source identity of earlier observations.

