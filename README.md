# ansible-provision

Ansible provisioning for the image operator model defined in cloud-provision
[`docs/IMAGE_WORKFLOW.md`](https://github.com/jeonghanlee/cloud-provision/blob/master/docs/IMAGE_WORKFLOW.md) (Operator definition): six vacua (debian12, debian13,
rocky8, rocky10, ubuntu24, ubuntu26), one role per operator, one playbook per
operator, and one assembly playbook per species.

* First-pass VM source of truth: [cloud-provision](https://github.com/jeonghanlee/cloud-provision)
* EPICS environment: [EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution)

This repository does not own VM lifecycle, site network identity, internal
package mirrors, proxy policy, or production deployment secrets. Site-specific
values belong in inventory or `configure/CONFIG_SITE.local` overlays; the
full override contract (which value goes in which plane) is in
`docs/ARCHITECTURE.md` section 7. Baking behind a site proxy is a
cloud-provision procedure: see `cloud-provision/docs/RUNBOOK_BAKE.md`.

Trust posture: `ansible.cfg` disables host-key checking and assumes
passwordless become on the lab NAT. Do not point this configuration
at non-lab hosts as-is.

## Prerequisites

Install ansible-core on the control host:

```bash
make setup
```

Provisioning targets must be running via `cloud-provision`. The maintained
`inventory/lab.ini` contains group relationships and no host rows;
`cloud-provision/bin/generate_ansible_inventory.bash` supplies the actual VM
name, resolved address, and groups as a second inventory source.

## Makefile Workflow

Set `RUNTIME_INVENTORY` to a generated host inventory before running a target.
Set `ANSIBLE_LIMIT` to the generated VM name when a target must select an
arbitrary run-specific name.

### Connectivity

```bash
make ping RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

### Provision a species

```bash
make bare.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make iocrunner.debian13 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make iocrunner_nfs.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make epics_dev.ubuntu24 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini ANSIBLE_LIMIT=actual-vm-name
```

### Run one operator

```bash
make op.common.rocky10 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make op.nfs_sim.debian13 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

### Dry Run

```bash
make bare.rocky8.check RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

Raw tasks are skipped in check mode: `check` validates inventory,
reachability, and template rendering only - it does not preview changes.

### Configuration

```bash
make vars
make PRINT.INVENTORY
```

---

## Direct CLI Workflow

```bash
ansible all -i inventory/lab.ini -i /tmp/cloud-provision-host.ini -m raw -a "uptime"
ansible-playbook -i inventory/lab.ini -i /tmp/cloud-provision-host.ini playbooks/species/bare.yml
ansible-playbook -i inventory/lab.ini -i /tmp/cloud-provision-host.ini playbooks/species/iocrunner.yml --limit debian13
ansible-playbook -i inventory/lab.ini -i /tmp/cloud-provision-host.ini playbooks/operators/common.yml --limit actual-vm-name
```

---

## Inventory

```
inventory/lab.ini                  # Host-free lab group relationships (vacua and species)
inventory/group_vars/all.yml       # Values shared by more than one operator
inventory/group_vars/<vacuum>.yml  # Per-vacuum values (epics_os_dir, python overrides)
```

Supply a generated host inventory to Make without replacing the maintained
group relationships:

```bash
make bare.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

`INVENTORY` remains overridable for a site-owned complete inventory.

Standalone (non-lab) VMs: see [docs/STANDALONE.md](docs/STANDALONE.md).

---

## Operators

One role per operator; each role's `defaults/` owns the values only it
consumes. The operator definition in cloud-provision [`docs/IMAGE_WORKFLOW.md`](https://github.com/jeonghanlee/cloud-provision/blob/master/docs/IMAGE_WORKFLOW.md)
is the normative statement of content and order.

| Operator | Role | Source |
|---|---|---|
| P_proxy | `proxy` | [jeonghanlee/cloud-provision](https://github.com/jeonghanlee/cloud-provision) (proxy contract, applied not reimplemented) |
| P_common | `common` | OS package manager |
| P_java | `java` | Distribution OpenJDK 21 JDK packages |
| P_tomcat | `tomcat` | Apache Tomcat 9.0.121 binary tarball |
| P_mariadb | `mariadb` | Distribution MariaDB server packages |
| P_sqlite | `sqlite` | Distribution SQLite command-line package |
| P_archiver-build | `archiver_build` | [jeonghanlee/epicsarchiverap-env](https://github.com/jeonghanlee/epicsarchiverap-env) |
| P_rt | `rt` | Debian PREEMPT_RT packages |
| P_provenance | `provenance` | - |
| P_python | `python` | OS package manager |
| P_epics | `epics` | [jeonghanlee/EPICS-env-distribution](https://github.com/jeonghanlee/EPICS-env-distribution) |
| P_epics-build | `epics_build` | [jeonghanlee/EPICS-env](https://github.com/jeonghanlee/EPICS-env) |
| P_epics-support | `epics_support` | [jeonghanlee/EPICS-env-support](https://github.com/jeonghanlee/EPICS-env-support) |
| P_procserv | `procserv` | [jeonghanlee/procServ-env](https://github.com/jeonghanlee/procServ-env) |
| P_conserver | `conserver` | [jeonghanlee/conserver-env](https://github.com/jeonghanlee/conserver-env) |
| P_con | `con` | [jeonghanlee/con](https://github.com/jeonghanlee/con) |
| P_nfs-sim | `nfs_sim` | - |
| P_iocrunner | `iocrunner` | [jeonghanlee/epics-ioc-runner](https://github.com/jeonghanlee/epics-ioc-runner) |
| P_testusers | `testusers` | - |
| P_ethercat | `ethercat` | [jeonghanlee/ethercat-env](https://github.com/jeonghanlee/ethercat-env) (bundle) |

### Java

Run `java` after `common`, using the existing runtime inventory:

```bash
make op.java.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

The operator installs the distribution OpenJDK 21 JDK, selects `java` and
`javac`, and writes `/etc/profile.d/java.sh` for subsequent login shells.
It uses the Java package subset of the cloud-provision middleware baseline:
`java-21-openjdk` and `java-21-openjdk-devel` on RedHat, and
`openjdk-21-jdk-headless` on Debian. Maven belongs to the application wrapper.

The default `JAVA_HOME` is `/usr/lib/jvm/java-21-openjdk` on RedHat and
`/usr/lib/jvm/java-21-openjdk-amd64` on Debian. Override `java_home` in site
inventory for another distribution JDK path or architecture. Package lists
(`pkg_java_redhat`, `pkg_java_debian`), family paths (`java_home_redhat`,
`java_home_debian`), and `java_profile` are role defaults. Service units and
non-login build commands must supply `JAVA_HOME` explicitly; they do not
automatically read the login profile.

### Tomcat

Run `tomcat` after `common` and `java`:

```bash
make op.tomcat.rocky8 RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
```

The operator verifies the Apache archive against the pinned SHA-512, installs
`/opt/apache-tomcat-9.0.121` as root-owned shared files, and links
`/opt/tomcat9` to that directory. `/etc/profile.d/tomcat.sh` exports
`CATALINA_HOME` for subsequent login shells. Re-apply verifies the archive's
regular-file list, file hashes, root ownership, directory mode `0755`, file
modes `0644` or `0755`, and executable `bin/*.sh` scripts. Added, missing,
modified, inaccessible, or non-regular files cause an explicit failure instead
of being overwritten.

Site inventory can override `tomcat_version`, `tomcat_sha512`,
`tomcat_archive_url`, `tomcat_install_parent`, `tomcat_home`, and
`tomcat_profile`. A version change requires its matching checksum; previous
version directories remain available. The install directory, home link, and
profile must be separate paths; none may contain another. Parent directories
must already exist, be root-owned, allow directory traversal by all users,
and prohibit group/other writes.

This operator supplies the shared Tomcat distribution. The application owns
`CATALINA_BASE`, instance configuration, and service startup; epicsarchiverap-env supplies
the Archiver Appliance instances. Services must set `JAVA_HOME` and
`CATALINA_HOME` explicitly. See the Apache
[multiple-instance instructions](https://tomcat.apache.org/tomcat-9.0-doc/RUNNING.txt).

### MariaDB

Run `mariadb` after `common`; it needs no private variables:

```bash
export RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
make op.mariadb.rocky8
```

The application account password is made and kept on the target. The operator
reads it from a root-only file, `mariadb_password_file` (default
`/etc/ansible-provision/mariadb-<user>.pass`, mode 0600 in a 0700 directory),
and creates that file with a random 32-character password when it is absent.
The password reaches the database client only on its standard input, so it
appears in no command argument and never crosses the connection; the operator
works over SSH and over a local connection alike, and the target needs no
Python. A site that wants its own password writes the file before the first
apply: one line of 12-128 letters, digits or `._~+-`.

When the application account already exists but the file does not, the
operator stops without changing anything, because a running appliance may still
log in with the password the account holds. This is the case on a host set up
before the password file existed. Either write the account's current password
into the file, if it meets the rule above, or apply once with
`-e mariadb_password_rotate=true` to replace it with a generated one. The epicsarchiverap-env
default `archappl` is too short to keep, so a host still on it takes the second
way. To rotate later, remove the file and apply with
`-e mariadb_password_rotate=true`. After any change of the password, an
installed appliance needs `-e archiver_force_reinstall=true` to take it, since
the install stamp does not record the password.

The operator installs `mariadb-server`, enables `mariadb.service`, and creates
the `archappl` database with `utf8mb4`. The `archappl` application account at
`localhost` receives all privileges on that database, without global
privileges or `GRANT OPTION`. `mariadb_database` and `mariadb_user` accept
1-32 lowercase letters or digits, starting with a letter; system names are
reserved. An existing database with another charset or an existing application
account with privileges outside that scope causes failure without changing
those database/account definitions.

The application account uses password authentication without additional TLS
requirements. Existing `REQUIRE SSL`, `X509`, cipher, issuer or subject
requirements, an explicitly expired password, or an account lock cause a
visible failure before account changes. Resolve that policy separately before
re-applying; the operator does not remove those restrictions. This check runs
after package and service configuration.

| OS family | Unix domain socket | Managed server configuration |
|---|---|---|
| RedHat | `/run/mariadb/mariadb.sock` | `/etc/my.cnf.d/zz-ansible-archiver.cnf` |
| Debian | `/run/mysqld/mysqld.sock` | `/etc/mysql/mariadb.conf.d/99-ansible-archiver.cnf` |

By default `mariadb_skip_networking: true` disables TCP. Setting it to `false`
allows TCP on `127.0.0.1` alongside the socket. The systemd drop-in
`/etc/systemd/system/mariadb.service.d/archiver.conf` recreates the runtime
directory with mode `0755`; local clients can reach the socket and must pass
database authentication. Root management uses `root@localhost` with
`unix_socket` authentication. Provisioning requires passwordless local root
access through the socket, as provided by a fresh distribution installation;
it converts that root account to socket-only authentication. Socket-activated `mariadb.socket` must be
disabled before applying the service configuration.

Security setup removes all anonymous accounts and every root account except
`root@localhost` using `DROP USER`. This is stricter than the distribution
secure-installation, which keeps root at `127.0.0.1` and `::1`: under loopback
TCP those are reachable, and this role gives no root account a password. With
TCP off it also drops the application account's `127.0.0.1` host. It drops the
`test` database, including its data, and deletes database grants for `test` and
the default `test_*` patterns, including orphan grant rows. Other databases and
other accounts are preserved. Privileges are reloaded on every apply, including
when no persistent rows need changing.

Re-apply compares configuration and account state and reports actual changes.
Service configuration changes restart MariaDB; unchanged re-apply preserves
the running service. Package lists are available as `pkg_mariadb_redhat` and
`pkg_mariadb_debian` defaults.

epicsarchiverap-env owns the schema, its separate `admin` account workflow, application
commands, and Tomcat JDBC configuration. From `90e4a04` its `DB_SOCKET` moves
every one of those connections onto one socket, which `archiver_build` sets, so
the `archiver_dev` species runs on the socket-only default.

### Archiver

Run `archiver_build` after `java`, `tomcat`, and `mariadb` (or `sqlite` for the
SQLite species), or apply the whole species in one run:

```bash
export RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
# one operator
make op.archiver_build.rocky8
# or the whole species
make archiver_dev.rocky8
# or the SQLite species
make archiver_dev_sqlite.rocky8
```

The operator drives epicsarchiverap-env's make sequence, which clones and builds epicsarchiverap-maven
from source internally, and installs the four appliance instances under
`/opt/epicsarchiverap-maven`, served by `epicsarchiverap-maven.service` as the
`mid-srv` service account. The build runs as a detached systemd unit, so a
dropped connection cannot leave a half-built tree behind. The play polls that
unit to a success sentinel and reports nothing until it finishes. Expect several
minutes on a host with a cold Maven cache. The build unit keeps its own output:
read `journalctl -u archiver-build.service` on the target while it runs, or
after it fails. `archiver_env_ref` pins epicsarchiverap-env and `archiver_maven_src_tag`
pins the epicsarchiverap-maven source. The operator passes Maven flags through epicsarchiverap-env's
`MAVEN_FLAGS` hook, so `archiver_env_ref` must be `84b38e5` or later; an older
ref reads `MAVEN_OPTS` instead, and a proxied build then cannot reach Maven
Central.

The instances serve on 17665 (mgmt), 17666 (engine), 17667 (etl) and 17668
(retrieval). Management lives under mgmt, for example
`http://<host>:17665/mgmt/bpl/getApplianceInfo`. mgmt answers 500 for roughly
20 to 30 seconds after a start while it initialises, so a single check issued
immediately reads as a failure that is not one.

The appliance authenticates to MariaDB as the application account over the
socket the `mariadb` operator manages: `archiver_db_socket` defaults to `auto`,
which is `/run/mariadb/mariadb.sock` on Rocky and `/run/mysqld/mysqld.sock` on
Debian, written to epicsarchiverap-env as `DB_SOCKET`; an absolute path names
another socket. `DB_SOCKET` needs `archiver_env_ref` at `90e4a04` or later: an
older ref ignores it and its appliance still connects over TCP, which the
default then leaves closed, so PV configuration would not persist. An empty `archiver_db_socket` falls back to TCP at
`archiver_db_host`:`archiver_db_port` and needs `mariadb_skip_networking: false`
beside it, since the default closes TCP and drops the `127.0.0.1` account. The build reads the password from the file the `mariadb` operator made
on the same host (`archiver_db_password_file`, which follows
`mariadb_password_file`) and passes it to epicsarchiverap-env as `DB_USER_PASS`; the
generated `../CONFIG_SITE.local` that carries it is readable by root only. A
build refuses to start when that file is missing.

A host installed over loopback TCP by an earlier operator moves to the socket in
one run: apply the species with `-e archiver_force_reinstall=true`. The
`mariadb` step runs first and closes TCP, so the running appliance loses its
database until the rebuild later in the same run installs and starts it on the
socket; a run without the flag stops at the changed knob set and leaves the
appliance in that state until the species is applied again with the flag.

Maven reads a proxy only from a settings file. This operator consumes the file
the cloud-provision proxy contract owns at `/etc/maven-proxy-settings.xml` and
writes none of its own. On a proxied host that does not carry it, the operator
refuses before starting a build rather than failing inside Maven. That file
arrives at provisioning, so a host provisioned before the contract covered Maven
is recreated through cloud-provision's `bin/create_vm.bash` rather than rebuilt
in place.

`archiver_java_heapsize` (default `256M`) sets the heap of every instance
explicitly; four instances at a 1G heap oversubscribe a 4 GB host. A changed
knob does not reach an appliance that is already installed. The operator
records the knob set at install time, and a later re-apply that wants a
different set is refused with the difference named, stopping the run instead of
rebuilding. To rebuild, add `-e archiver_force_reinstall=true` to
`ANSIBLE_OPTS`, for example `ANSIBLE_OPTS='-e archiver_force_reinstall=true'`.
An installed appliance whose four instances are not all running is repaired with
a service restart.

The store policy of each tier is set with `archiver_store_sts_granularity`,
`archiver_store_sts_hold`, `archiver_store_mts_granularity`,
`archiver_store_mts_hold` and `archiver_store_lts_granularity`, which need
`archiver_env_ref` at `9eed006` or later. Empty leaves the epicsarchiverap-env default: STS
`PARTITION_HOUR` hold 2, MTS `PARTITION_DAY` hold 2, LTS `PARTITION_YEAR`. A
granularity is one of `PARTITION_5MIN`, `PARTITION_15MIN`, `PARTITION_30MIN`,
`PARTITION_HOUR`, `PARTITION_DAY`, `PARTITION_MONTH` and `PARTITION_YEAR`. The
three granularities are set together or not at all, strictly finer to coarser
from STS to LTS; a hold is a positive integer. The operator refuses any other
value before a build starts. The values are part of the recorded knob set, so
changing them on an installed appliance needs `archiver_force_reinstall`. A test
host that watches samples reach all three tiers within hours uses STS
`PARTITION_5MIN` hold 2, MTS `PARTITION_HOUR` hold 2 and LTS `PARTITION_DAY`;
real deployments keep the defaults.

The appliance logs only to the journal: `epicsarchiverap-maven.service` runs the
four Tomcats in the foreground, each under its own identifier, so one instance
is read with `journalctl -u epicsarchiverap-maven.service -t archappl-mgmt`
(likewise `archappl-engine`, `archappl-etl`, `archappl-retrieval`), and there is
no `catalina.out`. An `archiver_env_ref` at this layout needs
`archiver_maven_src_tag` at epicsarchiverap-maven `67be91d7` or later. The operator writes a
journald drop-in, `/etc/systemd/journald.conf.d/50-archiver.conf`, that keeps
the host's whole journal, not only the appliance's entries, persistent for eight
weeks within 1G (`archiver_journal_*`). These values are not part of the
recorded knob set: a changed value is written on the next apply, and journald
restarts only when the file changes. `archiver_root_logger_level`
sets the appliance's root log level (empty keeps epicsarchiverap-env's `INFO`; one of `OFF`,
`FATAL`, `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`, `ALL`) and is part of the
recorded knob set; a running appliance's levels change without a rebuild
through `/opt/epicsarchiverap-maven/archappl.bash loglevel <component> [<logger> [<level>]]`.

The `archiver_dev_sqlite` species keeps the appliance configuration in SQLite
instead of MariaDB: the `sqlite` operator installs only the `sqlite3` tool
(`sqlite` on Rocky, `sqlite3` on Debian) in place of `mariadb`, and its group
sets `archiver_db_backend: sqlite`, which `archiver_build` writes to
epicsarchiverap-env as `DB_BACKEND` (from `bbe0968`). The database is
`<archiver_storage_top>/config/archappl.sqlite`, owned by the service account;
epicsarchiverap-env creates and reads it with `sqlite3` run as that account,
and the operator checks its tables through `make sql.show` so root never
opens the file. No MariaDB server, account, password file or socket is
involved, and `archiver_db_socket`, `archiver_db_host`, `archiver_db_port` and
`archiver_db_password_file` apply to the `mariadb` backend only. The backend is
part of the recorded knob set. The cloud-provision generator emits the
`archiver_dev_sqlite` group for `--species archiver-dev-sqlite`.

After `sql.fill` the operator counts the tables in the configuration database and
stops the build before install when there are none or they cannot be counted: an
appliance on an empty database archives and serves, but never persists PV
configuration. A forced reinstall stops the running appliance before it builds,
so a build stopped at that check leaves the previous appliance stopped; the
build log names how to start it again.

## Species Assemblies

| Assembly | Product |
|---|---|
| `species/bare.yml` | P_common |
| `species/iocrunner.yml` | P_testusers P_iocrunner (P_epics or P_epics-build) P_python (P_con P_conserver P_procserv) P_provenance on bare |
| `species/iocrunner_nfs.yml` | P_nfs-sim on iocrunner |
| `species/iocserver.yml` | P_iocrunner (P_epics or P_epics-build) P_python (P_con P_conserver P_procserv) P_provenance on bare |
| `species/epics_dev.yml` | P_epics-support P_epics-build P_python on bare |
| `species/nfs_sim.yml` | P_nfs-sim on bare |
| `species/rtbase.yml` | P_rt on bare |
| `species/ethercat.yml` | P_ethercat on the rtbase golden |
| `species/archiver_dev.yml` | P_archiver-build P_mariadb P_tomcat P_java (P_epics or P_epics-build) P_python P_provenance on bare |
| `species/archiver_dev_sqlite.yml` | P_archiver-build P_sqlite P_tomcat P_java (P_epics or P_epics-build) P_python P_provenance on bare |
