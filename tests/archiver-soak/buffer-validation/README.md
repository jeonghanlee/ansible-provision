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
| `fast.txt`, `fixture-sha256.json` | Identify the 110 fast PVs and original fixture bytes | Shared 903-PV fixture |
| `source-diagnostics/TransformCheck.java` | Verify transformed class bytes and callback insertion | Built observer and actual appliance classes/dependencies |
| `source-diagnostics/verify_retained.py` | Compare retained native inputs/PB and reject missing exposure | Explicit archive, output directory and runner; installed decoder/fixtures |

The observer captures inputs before buffering. The shim delays the filesystem
write while preserving the actual write. The decoder uses the appliance PB
implementation; the runner compares timestamps, value bits, status, severity,
order and multiplicity. Importing `runner.py` reads installed fixtures, so a
source-only check must compile it without importing it.

## Source Identity And Shared Files

`source.json` records the original hashes of all 18 deployed bundle members
and both source diagnostics. Nine deployed text files and both diagnostics
are present here. Seven identical shared files use their existing repository
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
| `install-fixture.py` | [etl-pass/install-fixture.py](../etl-pass/install-fixture.py) |

The only source adaptations are explicit configuration inputs in `setup.py`
and `verify_retained.py`. Their imported hashes are separate from the original
hashes. Function bodies and the observation/comparison logic are preserved.
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
names an absolute staging directory containing the nine deployed text sources,
the two built JARs and all seven shared files listed above. It must not point
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

Setup stops the appliance, creates tool/output directories, installs IOC and
ETL units, restricts Channel Access to loopback, adds the deadband database,
compiles the shim/decoder, and adds Java-agent and `LD_PRELOAD` configuration.
It preserves configuration backups and writes frozen identities. It refuses
an existing campaign; it is not an idempotent Ansible role. Campaign execution
then starts/stops services and registers PVs. These are separate live operations,
not part of the local build procedure above.

The shared fixture installer also defines sample/finish units referring to
`collect.py` and `observe.py`. The preserved buffer bundle does not supply those
files or their dependency closure; the buffer campaign uses its own runner.
Installation is therefore still an unfinished M50 criterion. Do not treat this
source package as a verified deployable bundle or infer an observed runtime
failure from that missing dependency alone.

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

The compact-write comparison and progress reporting retain their original
behavior. Their separate M49/#55 work remains unfinished. A successful build
or transformer check does not establish those behaviors or new product acceptance.
