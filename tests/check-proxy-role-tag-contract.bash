#!/usr/bin/env bash
# Observes real Ansible calls from the shipped runner without replacing them.
# Empty inventories prevent guest execution; the full local assembly remains real.
set -euo pipefail

declare -g TOP WORKSPACE REAL_ANSIBLE PRODUCER_ROOT PRODUCER_REF
TOP="$(cd "$(dirname "$0")/.." && pwd)"
REAL_ANSIBLE="$(command -v ansible-playbook)"
test -x "${REAL_ANSIBLE}"
PRODUCER_ROOT="${PROXY_CONTRACT_ROOT:-${TOP}/../cloud-provision}"
PRODUCER_REF="${PROXY_CONTRACT_REF:-$(git -C "${PRODUCER_ROOT}" rev-parse HEAD)}"
umask 0077
WORKSPACE="$(mktemp -d /tmp/ansible-proxy-tag-test.XXXXXX)"

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

mkdir "${WORKSPACE}/bin"
printf '%s\n' '[rocky8]' > "${WORKSPACE}/empty.ini"
cat > "${WORKSPACE}/bin/ansible-playbook" <<'PYTHON'
#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

capture = Path(os.environ["PROXY_ROLE_TAG_CAPTURE"])
with capture.open("a", encoding="ascii") as target:
    json.dump({"run_tags": os.environ.get("ANSIBLE_RUN_TAGS"),
               "skip_tags": os.environ.get("ANSIBLE_SKIP_TAGS"),
               "arguments": sys.argv[1:]}, target)
    target.write("\n")
real_ansible = os.environ["PROXY_ROLE_REAL_ANSIBLE"]
os.execv(real_ansible, [real_ansible] + sys.argv[1:])
PYTHON
chmod 0700 "${WORKSPACE}/bin/ansible-playbook"

for scope in cloud general-server; do
    rc=0
    PATH="${WORKSPACE}/bin:${PATH}" PROXY_ROLE_REAL_ANSIBLE="${REAL_ANSIBLE}" \
        PROXY_ROLE_TAG_CAPTURE="${WORKSPACE}/${scope}.jsonl" \
        ANSIBLE_RUN_TAGS=never ANSIBLE_SKIP_TAGS=archiver_build \
        RUNTIME_INVENTORY="${WORKSPACE}/empty.ini" TARGET_HOST=absent-test-target \
        PROXY_TEST_UUID=00000000-0000-0000-0000-000000000000 \
        PROXY_CONTRACT_REF="${PRODUCER_REF}" PROXY_TEST_SCOPE="${scope}" \
        KEEP_WORKSPACE=1 bash "${TOP}/tests/check-proxy-role.bash" \
        > "${WORKSPACE}/${scope}.log" 2>&1 || rc=$?
    test "${rc}" -eq 1
    grep -Fq 'the dedicated guest did not complete the actual suite' "${WORKSPACE}/${scope}.log"
    python3 - "${WORKSPACE}/${scope}.jsonl" "${TOP}/tests/proxy-role/verify.yml" <<'PYTHON'
import json
import sys

with open(sys.argv[1], encoding="ascii") as source:
    calls = [json.loads(line) for line in source]
if len(calls) != 1:
    raise SystemExit("Error: expected one real Ansible call before receipt refusal")
call = calls[0]
if call["run_tags"] is not None or call["skip_tags"] is not None:
    raise SystemExit("Error: caller tag filters reached the actual Ansible process")
arguments = call["arguments"]
if arguments[-1] != sys.argv[2]:
    raise SystemExit("Error: the shipped guest suite was not selected")
for option, value in (("--tags", "all"), ("--skip-tags", "")):
    if option not in arguments or arguments[arguments.index(option) + 1] != value:
        raise SystemExit("Error: explicit complete-suite tag selection is missing")
PYTHON
    printf '[ PASS ] %s runner removes tag filters and rejects the empty guest inventory\n' "${scope}"
done

ANSIBLE_RUN_TAGS=never ANSIBLE_SKIP_TAGS=archiver_build ANSIBLE_TAGS=always \
    KEEP_WORKSPACE=1 bash "${TOP}/tests/check-general-server-contract.bash" \
    > "${WORKSPACE}/local-contract.log" 2>&1
grep -Fxq 'Summary: 9 passed / 9 total' "${WORKSPACE}/local-contract.log"
printf '%s\n' '[ PASS ] Full local contract reaches the build consumers despite caller tag filters'
printf '%s\n' 'Summary: 3 passed / 3 total'
