# Retained Archiver Diagnostics

## Scope

These entry points inspect actual ETL records through the observation's frozen native tools. They preserve physical/HTTP checkpoints and separate collection or evaluator findings from the accepted ETL functionality result.

**Out of scope:** provisioning, connection settings, starting another long observation, repairing a collector or evaluator, changing original evidence, and production operation.

## Entry Points

| File | Inputs | Output and execution boundary |
| --- | --- | --- |
| `physical.py` | A running dedicated deployment, its frozen tools and original focused inputs | Reads all 903 effective configurations, decodes four policy representatives and compares physical/HTTP contents; writes a new checkpoint directory |
| `full-day.py` | A stopped recording deployment, completed observation and exact frozen bundle | Runs the native evaluator and reads pass/JFR/checkpoint evidence; emits a diagnostic JSON result |
| `source-available.py` | Actual shortened journal-unavailable/application-file-available records, preservation inventory and frozen bundle | Runs native readers/evaluation/aggregation into a new private output directory; preserves the original short observation's unsuccessful verdict |
| `automatic-abort.py` | Actual shortened all-sources-unavailable records and frozen bundle | Verifies the recorded two-failure counter, single abort, source restoration, successful pass and actual stopped unit; emits diagnostic JSON |

The recording tools are under `../etl-pass/` and `../journal-validation/`; additional-test preparation and fault-producing payloads are under `../etl-scenarios/`. These diagnostic entry points are separate from the deployed bundle: preserving them does not change an installed manifest or the identity of an earlier observation.

## Execution Contract

Use Python 3.9 or later and the observation's original dependency bundle. Run `--help` to inspect each CLI. The physical checker imports the installed modules from `/usr/local/share/etl-soak`; its `--chain` and `--mode` select the declared running observation and checkpoint.

The other diagnostics accept explicit `--input`, `--tools` and scenario inputs. The source-available checker additionally requires `--case-root`, `--preservation`, `--expected-bundle-sha256` and a new `--output` directory. The automatic-abort checker requires `--case-root`. The full-day checker requires `--chain`.

Preserve original absolute paths when replaying a retained archive in an isolated namespace. Explicit CLI paths select inputs; they do not rewrite absolute paths or identity fields inside those inputs. The full-day and automatic-abort entry points query the actual appliance unit, and the source-available entry point reads original application files. An arbitrary archive directory on another host does not supply that runtime state.

The physical final mode returns zero to let ordinary terminal collection proceed even when the separate physical result is unsuccessful. Read its `result.json` to decide physical acceptance. A diagnostic process exit alone is never the ETL or journal verdict.

The source-available and automatic-abort checks retain their observed shortened-case scope. They do not establish the default variants, complete a deliberately shortened 24-hour observation, or claim exact independent-recipient replay. CLI preservation and syntax checks are distinct from executing these adapted entry points against real retained inputs.

## Evidence And Source Integrity

Keep connection files, SSH keys, VM/host identities, application configuration, journal exports, PB files, JFR/CSV data, producer ledgers and command receipts outside this directory. Diagnostic output also belongs in private evidence storage.

Use this directory's `SHA256SUMS` to verify its reusable source files. The parent source manifest and each actual observation's frozen bundle are separate integrity contracts; do not replace the original observation's manifest with current repository hashes.

## Follow-up Boundaries

| Contract | Owning issue |
| --- | --- |
| Kernel cursor coverage, terminal isolation, query arguments and preparation/source/lifecycle checks | [#34](https://github.com/jeonghanlee/ansible-provision/issues/34) |
| JFR process scope, terminal persistence order, UTC comparison, numerical reports and recipient replay | [#35](https://github.com/jeonghanlee/ansible-provision/issues/35) |
| Journal collector normal-stop/post-stop verification | [#32](https://github.com/jeonghanlee/ansible-provision/issues/32) |
| Independent recipient reproduction of the journal full-day result | [#33](https://github.com/jeonghanlee/ansible-provision/issues/33) |
| Completed journal recording/retention/collection and corrected source-matching checks | [#31](https://github.com/jeonghanlee/ansible-provision/issues/31) |

Collector, evaluator and replay repairs use retained evidence and bounded real-path checks. They do not require another full-day producer run solely to repair a test tool.

