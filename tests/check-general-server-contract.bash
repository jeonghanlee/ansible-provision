#!/usr/bin/env bash
# Exercises real Make and Ansible selection, inventory resolution, and the
# read-only general-server guard. It does not provision the controller.
set -euo pipefail

# Verification selects its own tags, including the explicit guard-only probes.
unset ANSIBLE_RUN_TAGS ANSIBLE_SKIP_TAGS ANSIBLE_TAGS

declare -g TOP WORKSPACE
TOP="$(cd "$(dirname "$0")/.." && pwd)"
umask 0077
WORKSPACE="$(mktemp -d /tmp/ansible-general-server-test.XXXXXX)"

function cleanup {
    local rc=$?
    if [[ "${rc}" != 0 || "${KEEP_WORKSPACE:-0}" == 1 ]]; then
        printf 'Retained workspace: %s\n' "${WORKSPACE}" >&2
        return "${rc}"
    fi
    rm -rf -- "${WORKSPACE}"
    return "${rc}"
}
trap cleanup EXIT

export ANSIBLE_CONFIG="${TOP}/ansible.cfg"
export ANSIBLE_LOCAL_TEMP="${WORKSPACE}/ansible-local"
export ANSIBLE_NOCOLOR=1

printf '%s\n' '[rocky8]' 'localhost ansible_connection=local ansible_become=false' \
    '[archiver_server_sqlite]' 'localhost' > "${WORKSPACE}/runtime.ini"
printf '%s\n' '---' "# ${WORKSPACE}/site.yml" 'epics_ioc_engineers: [root]' > "${WORKSPACE}/site.yml"

make -n -s -C "${TOP}" archiver_server_sqlite.rocky8 \
    RUNTIME_INVENTORY="${WORKSPACE}/runtime.ini" > "${WORKSPACE}/make.log"
grep -Fq -- "-i inventory/lab.ini -i ${WORKSPACE}/runtime.ini" "${WORKSPACE}/make.log"
grep -Fq -- '--limit rocky8 playbooks/species/archiver_server_sqlite.yml' "${WORKSPACE}/make.log"
printf '%s\n' '[ PASS ] Make selects the shipped group, runtime inventory, and Rocky limit'

ansible-inventory -i "${TOP}/inventory/lab.ini" -i "${WORKSPACE}/runtime.ini" \
    --host localhost > "${WORKSPACE}/host.json"
python3 - "${WORKSPACE}/host.json" <<'PYTHON'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as source:
    host = json.load(source)
expected = {
    "proxy_scope": "general-server",
    "archiver_db_backend": "sqlite",
    "archiver_env_ref": "e2ade5a184098379424ed87972ff308490eeedec",
    "archiver_maven_src_tag": "af2e734857dab01105576086adeca0d4f318d6ee",
    "epics_ioc_engineers": [],
    "epics_os_dir": "rocky-8.10",
}
for key, value in expected.items():
    if host.get(key) != value:
        raise SystemExit("Error: inventory does not resolve " + key)
PYTHON
printf '%s\n' '[ PASS ] Inventory resolves system-only scope, SQLite, full source pins, and explicit site owner'

for playbook in species/archiver_server_sqlite species/archiver_dev_sqlite operators/proxy; do
    ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${WORKSPACE}/runtime.ini" \
        --syntax-check "${TOP}/playbooks/${playbook}.yml" >> "${WORKSPACE}/syntax.log" 2>&1
done
ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${WORKSPACE}/runtime.ini" \
    --syntax-check -e "@${WORKSPACE}/site.yml" \
    "${TOP}/playbooks/species/archiver_server_sqlite.yml" >> "${WORKSPACE}/syntax.log" 2>&1
ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${WORKSPACE}/runtime.ini" \
    --syntax-check "${TOP}/tests/proxy-role/verify.yml" >> "${WORKSPACE}/syntax.log" 2>&1
printf '%s\n' '[ PASS ] General-server, development, proxy, site inputs, and role suite pass Ansible syntax'

for species in archiver_server_sqlite archiver_dev_sqlite; do
    ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${WORKSPACE}/runtime.ini" \
        --list-tasks "${TOP}/playbooks/species/${species}.yml" > "${WORKSPACE}/${species}.tasks"
done
python3 - "${WORKSPACE}" <<'PYTHON'
from pathlib import Path
import re
import sys

workspace = Path(sys.argv[1])
expected = ["common", "provenance", "python", "epics", "java", "tomcat", "sqlite", "archiver_build"]
for species in ("archiver_server_sqlite", "archiver_dev_sqlite"):
    text = (workspace / (species + ".tasks")).read_text()
    operators = re.findall(r"Apply the (\w+) operator", text)
    if operators != expected:
        raise SystemExit("Error: unexpected assembly: " + repr(operators))
    if "mariadb" in text.lower():
        raise SystemExit("Error: SQLite assembly selected a MariaDB task")
PYTHON
printf '%s\n' '[ PASS ] Ansible expands the same eight SQLite operators in order'

# Execute the complete imported assembly so skipped raw results reach every
# consumer condition. This check uses the controller's actual OS probes.
make -s -C "${TOP}" archiver_dev_sqlite.rocky8.check \
    RUNTIME_INVENTORY="${WORKSPACE}/runtime.ini" ANSIBLE_LIMIT=localhost \
    ANSIBLE_TAGS= ANSIBLE_OPTS="-e @${WORKSPACE}/site.yml" > "${WORKSPACE}/full-check.log" 2>&1
grep -Eq '^localhost[[:space:]]+:.*changed=0.*unreachable=0.*failed=0' "${WORKSPACE}/full-check.log"
grep -Fq 'TASK [archiver_build : Stop on configuration drift against the installed appliance]' "${WORKSPACE}/full-check.log"
grep -Fq 'TASK [archiver_build : Wait for the detached archiver build to finish]' "${WORKSPACE}/full-check.log"
printf '%s\n' '[ PASS ] Complete development assembly check mode handles skipped build results'

# Only the shipped always-tagged, read-only preflight runs on localhost.
if ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${WORKSPACE}/runtime.ini" \
    --limit localhost --check --tags always \
    "${TOP}/playbooks/species/archiver_server_sqlite.yml" > "${WORKSPACE}/guard.log" 2>&1; then
    printf '%s\n' 'Error: the actual group guard accepted an unspecified EPICS owner' >&2
    exit 1
fi
grep -Fq 'epics_ioc_engineers must select an existing checkout owner' "${WORKSPACE}/guard.log"
printf '%s\n' '[ PASS ] Actual read-only guard rejects the cloud account default before provisioning'

function expect_guard_refusal {
    local label="$1" expected="$2" inventory="$3" override="$4"
    if ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${inventory}" \
        --limit localhost --check --tags always -e "@${WORKSPACE}/site.yml" \
        -e "${override}" "${TOP}/playbooks/species/archiver_server_sqlite.yml" \
        > "${WORKSPACE}/${label}.log" 2>&1; then
        printf 'Error: the actual group guard accepted %s\n' "${label}" >&2
        exit 1
    fi
    grep -Fq -- "${expected}" "${WORKSPACE}/${label}.log"
    printf '[ PASS ] Actual read-only guard rejects %s before provisioning\n' "${label}"
}

printf '%s\n' '[rocky8]' 'localhost ansible_connection=local ansible_become=false' \
    > "${WORKSPACE}/missing-group.ini"
expect_guard_refusal missing-membership \
    'archiver_server_sqlite and rocky8 memberships are required' "${WORKSPACE}/missing-group.ini" '{}'
expect_guard_refusal cloud-scope \
    'general-server proxy scope and SQLite backend are required' "${WORKSPACE}/runtime.ini" '{"proxy_scope":"cloud"}'
expect_guard_refusal mariadb-backend \
    'general-server proxy scope and SQLite backend are required' "${WORKSPACE}/runtime.ini" '{"archiver_db_backend":"mariadb"}'
printf '%s\n' 'Summary: 9 passed / 9 total'
