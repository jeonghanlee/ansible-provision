# Buffer Verification Sources

## Scope

Preserve the buffer observer, native write-delay shim, decoder, campaign tools
and retained-input diagnostics. This directory contains reusable source, its
original identity and build procedures. The [work register](../../../docs/milestone-38560eb.md)
owns verification results and remaining work under M50 and M49.

Out of scope: installation acceptance, another appliance campaign, changes to
completed product acceptance, raw traces, native PB, logs, credentials and
deployment inventories. Use the [shared procedures](../PROCEDURES.md) for
private evidence and separate original/candidate results.

## Components And Data Flow

| Source | Function | Required inputs |
| --- | --- | --- |
| `Agent.java`, `observer.mf` | Instrument the actual sample buffer, writer and PlainPB append methods | JDK internal ASM exports; `bootstrap.jar` |
| `Trace.java` | Capture actual input events, swaps, passes and counters | Installed fast-target list; native shim; actual engine classes |
| `shim.c` | Delay the real native write and retain measured exposure | Linux, JNI headers, pthreads; observer control file |
| `PBDecode.java` | Decode captured inputs and physical PB with the appliance implementation | Appliance classes and dependency JARs; fast-target list |
| `runner.py` | Drive bounded preflight/main observations and compare native evidence | Installed fixture, observer, shim, decoder and running appliance dependencies |
| `campaign.py` | Check frozen identities and sequence preflight before main | Successful setup; preflight verdict and configuration |
| `setup.py` | Install the pinned tools and fixture on an empty appliance | Explicit staging directory; pinned appliance/environment and root privileges |
| `install-fixture.py` | Install only the buffer fixture IOC unit | Inactive appliance/IOC, empty MariaDB, shipped fixture and softIoc |
| `fast.txt`, `fixture-sha256.json` | Identify the 110 fast PVs and original fixture bytes | Shared 903-PV fixture |
| `source-diagnostics/TransformCheck.java` | Verify transformed class bytes and callback insertion | Built observer and actual appliance classes/dependencies |
| `source-diagnostics/verify_retained.py` | Compare retained native inputs/PB and reject missing exposure | Explicit archive, output directory and runner; installed decoder/fixtures |
| `source-diagnostics/test_pass_replay.py` | Check full/compact pass validation and negative evidence copies | Actual preflight full JSONL, compact JSON and initial missing-delay JSON; actual runner/fixtures |

The observer captures inputs before buffering. The shim delays the filesystem
write while preserving the actual write. The decoder uses the appliance PB
implementation; the runner compares timestamps, value bits, status, severity,
order and multiplicity. Importing `runner.py` reads installed fixtures, so a
source-only check must compile it without importing it.

## Source Identity And Shared Files

`source.json` records the original hashes of all 18 deployed bundle members
and both source diagnostics. Ten deployed text files and both diagnostics
are present here. Six identical shared files use their existing repository
paths. The two JARs are build outputs; their original hashes remain recorded,
but generated binaries are excluded from Git.

| Staging filename | Shared source |
| --- | --- |
| `aasoak.db` | [fixtures/aasoak.db](../fixtures/aasoak.db) |
| `load1.db` | [fixtures/load1.db](../fixtures/load1.db) |
| `load2.db` | [fixtures/load2.db](../fixtures/load2.db) |
| `retest-deadband.db` | [fixtures/retest-deadband.db](../fixtures/retest-deadband.db) |
| `pvs-all.csv` | [fixtures/pvs-all.csv](../fixtures/pvs-all.csv) |
| `register.py` | [etl-pass/register.py](../etl-pass/register.py) |

The buffer-local `install-fixture.py` derives from the original shared installer
and creates only the IOC unit. The shared ETL installer and its frozen bundle
retain their original bytes. Other source adaptations are explicit configuration
inputs in `setup.py` and `verify_retained.py`. Imported hashes are separate from
original hashes. The runner validates both existing full and compact pass
records as specified below; other observation/comparison logic is preserved.
The parent [SHA256SUMS](../SHA256SUMS) identifies the current sources; it does
not replace any immutable observation manifest. Run the parent README's
complete source check before using a candidate.

## Local Build And Transformer Check

Use a Linux host with JDK 21, GCC with C11/pthreads support, Python 3.8 or
later, and an actual built appliance `WEB-INF/classes` and `WEB-INF/lib`.
The decoder and transformer check must use those real classes and dependency
JARs. Record the appliance commit, class/dependency hashes and tool versions
with build results. A build against a different revision establishes only
that revision's source compatibility, not the pinned installation contract.

From this source directory, set `buffer_web` to the actual built appliance's
`WEB-INF` directory and build into a fresh private directory:

```bash
buffer_source=$PWD
buffer_web=/path/to/appliance/WEB-INF
buffer_build=$(mktemp -d)
buffer_java=$(dirname "$(dirname "$(readlink -f /usr/bin/javac)")")
buffer_exports=(--add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED)
buffer_exports+=(--add-exports java.base/jdk.internal.org.objectweb.asm.commons=ALL-UNNAMED)
buffer_cp="$buffer_web/classes:$buffer_web/lib/*"
mkdir "$buffer_build/agent" "$buffer_build/bootstrap" "$buffer_build/classes"
javac -proc:none "${buffer_exports[@]}" -d "$buffer_build/agent" "$buffer_source/Agent.java"
javac -proc:none -d "$buffer_build/bootstrap" "$buffer_source/Trace.java"
jar --create --file "$buffer_build/bootstrap.jar" --no-manifest -C "$buffer_build/bootstrap" buffer29
buffer_manifest="$buffer_source/observer.mf"
jar --create --file "$buffer_build/observer.jar" --manifest "$buffer_manifest" -C "$buffer_build/agent" buffer29
buffer_includes=("-I$buffer_java/include" "-I$buffer_java/include/linux")
buffer_cc=(-std=c11 -Wall -Wextra -Werror -fPIC -shared -pthread)
gcc "${buffer_cc[@]}" "${buffer_includes[@]}" "$buffer_source/shim.c" -o "$buffer_build/libbuffer29.so"
javac -proc:none -cp "$buffer_cp" -d "$buffer_build/classes" "$buffer_source/PBDecode.java"
buffer_check="$buffer_source/source-diagnostics/TransformCheck.java"
javac -proc:none "${buffer_exports[@]}" -d "$buffer_build/classes" "$buffer_check"
buffer_check_cp="$buffer_build/classes:$buffer_build/observer.jar:$buffer_build/bootstrap.jar:$buffer_cp"
java -Xverify:all "${buffer_exports[@]}" -cp "$buffer_check_cp" TransformCheck "$buffer_web/classes"
```

The transformer check loads the real observer and actual transformed class
bytes through the JVM verifier. It checks one callback at each of the four
declared insertion points. It does not attach the agent or run an appliance.
Keep generated artifacts private. Different compilers, JAR metadata or native
toolchains can change binary hashes; rebuilds are candidates, not the original
observation's binaries.

## Configuration And Installation Contract

`BUFFER_SOURCE_DIR` is required when importing or executing `setup.py`. It
names an absolute staging directory containing the ten deployed text sources,
the two built JARs and all six shared files listed above. Use this directory's
`install-fixture.py` in that staging directory. The staging directory must not point
directly at this source directory, which deliberately does not duplicate shared
files or contain generated JARs.

The preserved installer requires appliance source
`629533a37ef889ffe3203d97538038eaaec95283` and environment source
`482cf2939ea997064e4a2df64e3cb420681f4566`; it also checks ancestry of `6c6b973a`
and six installed classes against the built appliance. These pins are part of
the supported contract, not deployment credentials.

The installation layout is fixed: `/opt/epicsarchiverap-maven`, the environment
checkout under `/opt/epicsarchiverap-env-src/epicsarchiverap-env`, tools under
`/usr/local/share/buffer29` and `/usr/local/share/etl-soak`, and private output
under `/var/lib/buffer29` and `/var/lib/etl-soak`. Required services include
systemd, the appliance and socket-accessible MariaDB with an empty `archappl`
database. The shared installer requires the `mid-srv` account, `mid` group and
EPICS 7.0.10 `softIoc` from the Rocky 8.10 EPICS 1.3.0 layout declared in its
`SOFTIOC` constant. Root, Git, Python, JDK tools, GCC, `mysql`, `readlink`,
`systemctl` and `systemd-analyze` are required. The runner uses the local
appliance management API and the installed registration client.

Setup stops the appliance, creates tool/output directories, installs the IOC
unit, restricts Channel Access to loopback, adds the deadband database,
compiles the shim/decoder, and adds Java-agent and `LD_PRELOAD` configuration.
It preserves configuration backups and writes frozen identities. It refuses
an existing campaign; it is not an idempotent Ansible role. Campaign execution
then starts/stops services and registers PVs. These are separate live operations,
not part of the local build procedure above.

The buffer fixture installer creates `etl-soak-ioc.service` only. It creates
no `etl-soak-sample.service`, `etl-soak-sample.timer` or
`etl-soak-finish.service`; those ETL commands belong to the separate shared
installer. The buffer campaign uses its own runner. Existing units are not
removed; installation requires a dedicated empty appliance. Actual installation
verification remains recorded under M50 separately from source/build checks.

## Bounded Installation Verification

Use a fresh dedicated appliance with the declared source pins and prerequisites.
Prepare the staging directory as specified above, retain its complete member
list and hashes, and preserve original configuration and command output. Run
setup with an explicit source directory:

```bash
buffer_stage=/path/to/buffer-staging
sudo env BUFFER_SOURCE_DIR="$buffer_stage" /usr/bin/python3 "$buffer_stage/setup.py"
sudo systemctl cat etl-soak-ioc.service
systemctl show etl-soak-sample.service -p LoadState
systemctl show etl-soak-sample.timer -p LoadState
systemctl show etl-soak-finish.service -p LoadState
```

Setup must exit zero, preserve configuration backups, compile the native shim
and decoder, and write frozen tool/fixture identities matching installed files.
The IOC command must load the three shipped databases and deadband override.
All three unused ETL units must report `LoadState=not-found`. Verify actual
JVM transformation against the pinned installed classes using the build check
above, and import the installed runner/campaign without invoking their main
functions. Missing prerequisites are Incomplete, not a successful installation.

Check the real IOC and Channel Access path on loopback, then stop it normally:

```bash
buffer_bin=/opt/epics/1.3.0/rocky-8.10/7.0.10/base/bin/linux-x86_64
buffer_ca=(env EPICS_CA_ADDR_LIST=127.0.0.1 EPICS_CA_AUTO_ADDR_LIST=NO)
sudo systemctl start etl-soak-ioc.service
"${buffer_ca[@]}" "$buffer_bin/caget" -w 10 -t AASOAK:FAST:CH01 AASOAK:S1:CH01 AASOAK:SLOW:CH01
"${buffer_ca[@]}" "$buffer_bin/caget" -w 10 -t AASOAK:DB:CH01.MDEL AASOAK:DB:CH01.ADEL
sudo systemctl stop etl-soak-ioc.service
systemctl show etl-soak-ioc.service -p ActiveState -p MainPID
```

The three real fixture PVs must be readable; both deadband values must be `-1`.
After normal stop the IOC must be inactive with no main PID. A second setup
invocation must refuse the existing campaign before changing frozen identities
or configuration. Preserve that native refusal separately from the successful
first invocation. Keep actual original/candidate unit files and confirm the
unit audit rejects the original ETL sample/timer/finish definitions.

Bound the installation and IOC checks to 900 seconds after prerequisites;
retain native streams, statuses, installed source/dependency identities and
final service state before evaluation. Verify complete evidence membership and
hashes after transfer, then end use of the guest while keeping its disk and
evidence. This verifies installation and IOC dependencies only.

## Retained-Input Diagnostic Contract

`verify_retained.py` requires three explicit absolute paths:

| Environment variable | Input |
| --- | --- |
| `BUFFER_REPLAY_OUTPUT` | New private directory; an existing directory is refused |
| `BUFFER_REPLAY_ARCHIVE` | Actual retained initial-preflight archive containing `preflight/` |
| `BUFFER_REPLAY_RUNNER` | Identified candidate runner with installed fixture/decoder dependencies |

The diagnostic checks actual passes 15 and 16, decodes retained input/native PB
and compares the declared interval ending 20 seconds before the verdict. Its
900-second decoder/comparison deadline and `acceptance_preflight=false` remain
unchanged. Freeze and verify the full private input set before execution;
source preservation does not establish a replay result.

## Full And Compact Pass Records

The validator checks completed native-write passes. Eligible phases 2 and 3
alternate the first and last native write; phase 4 uses the first write for
the expected-loss control. Every eligible pass requires exactly one injection,
measured wait at least the requested delay and no native error. Last-position
injection requires the final native flush.

| Form | Required write evidence | Last native-write position |
| --- | --- | --- |
| Full `passes.jsonl` record | Every write, with positions `0` through `len(writes) - 1`; no `write_count` field | `len(writes) - 1` |
| Compact `passes.json` record | Positive integer `write_count` and exactly the first/last writes at positions `0` and `write_count - 1`; a single write is retained once | `write_count - 1` |

`write_count` is the observed count saved after the live pass was validated;
it is not the retained list length or buffer capacity. A compact record does
not retain intermediate writes and cannot independently establish their PVs,
values or timestamps. Pass validation establishes injection placement and
delay evidence, not event equality or product acceptance.

## Preflight Pass Regression

Use separately frozen copies of actual preflight full JSONL, compact JSON
and the initial unsuccessful preflight JSON. Preserve the original member
list, hashes and tools before testing; verify each copy before launching a
fresh process, and retain native output/status. The regression checks matching
full/compact identities and boundary writes, accepts valid records, rejects
the actual initial pass 16 without injection, and rejects negative copies
with missing/duplicate injection, inadequate wait, native error, wrong
alternation, absent final flush or inconsistent write counts/positions.
These negative copies are separate from the unchanged positive inputs.

The runner imports the installed fast-target and all-PV fixtures. On a local
Linux host with Python 3.8 or later and `bwrap`, supply those actual shipped
fixtures through a read-only filesystem namespace. Set the source and input
paths to their actual locations:

```bash
buffer_source=/absolute/path/to/tests/archiver-soak/buffer-validation
buffer_fixture=/absolute/path/to/tests/archiver-soak/fixtures
buffer_inputs=/absolute/path/to/frozen/preflight-inputs
buffer_test="$buffer_source/source-diagnostics/test_pass_replay.py"
buffer_fs=(bwrap --ro-bind / / --tmpfs /usr/local/share)
buffer_fs+=(--dir /usr/local/share/buffer29 --dir /usr/local/share/etl-soak)
buffer_fs+=(--ro-bind "$buffer_source" /usr/local/share/buffer29)
buffer_fs+=(--ro-bind "$buffer_fixture" /usr/local/share/etl-soak)
buffer_args=(--runner "$buffer_source/runner.py" --full "$buffer_inputs/corrected-passes.jsonl")
buffer_args+=(--compact "$buffer_inputs/corrected-passes.json" --initial "$buffer_inputs/initial-passes.json")
"${buffer_fs[@]}" -- python3 -B "$buffer_test" "${buffer_args[@]}"
```

The script imports and calls the actual validator without replacing any
internal function. Fixtures and input records are real files. It prints JSON
with each case outcome and exits zero only when all selected cases pass;
`--case NAME` selects one reported case for a scratch source mutation.
Bound each command to 60 seconds and preserve the complete receipts outside
the read-only namespace. The expected baseline defect is false refusal of
compact last-position records. It must fail before the correction and pass
afterwards, using the same frozen inputs.

This check covers the retained preflight inputs only. Original main pass
inputs are unavailable; their revalidation remains Incomplete. Existing
four-hour acceptance and recorded comparisons remain separate historical
results. This offline pass check performs no installation, live capture,
decoder/PB comparison, service lifecycle or new product acceptance. Progress
reporting and Maven assertion accounting remain separate M49/#55 work.
