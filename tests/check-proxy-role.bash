#!/usr/bin/env bash
# Executes the shipped proxy role on one dedicated Rocky guest and validates
# reconciliation against the producer's independent artifact fixture.

set -euo pipefail

declare -g SCRIPT_DIR
declare -g TOP
declare -g WORKSPACE
declare -g CONTRACT_FIXTURE
declare -g PRODUCER_ROOT
declare -g CONTRACT_SCRIPT
declare -g PRODUCER_COMMIT

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOP="$(cd "${SCRIPT_DIR}/.." && pwd)"
PRODUCER_ROOT="${PROXY_CONTRACT_ROOT:-${TOP}/../cloud-provision}"
CONTRACT_SCRIPT="${PRODUCER_ROOT}/bin/proxy_contract.bash"
CONTRACT_FIXTURE="${PROXY_CONTRACT_FIXTURE:-${PRODUCER_ROOT}/tests/fixtures/proxy-artifacts.tsv}"

: "${RUNTIME_INVENTORY:?Set RUNTIME_INVENTORY to the dedicated guest inventory}"
: "${TARGET_HOST:?Set TARGET_HOST to the dedicated guest inventory name}"
: "${PROXY_TEST_UUID:?Set PROXY_TEST_UUID to its provider-verified domain UUID}"
: "${PROXY_CONTRACT_REF:?Set PROXY_CONTRACT_REF to the landed producer commit or tag}"

if [[ ! -f "${RUNTIME_INVENTORY}" || ! -f "${CONTRACT_FIXTURE}" || ! -f "${CONTRACT_SCRIPT}" ]]; then
    printf '%s\n' 'Error: inventory, producer contract, or artifact fixture is missing' >&2
    exit 1
fi
for required in python3 git ansible-playbook sha256sum cmp; do
    resolved="$(command -v "${required}")"
    if [[ ! -x "${resolved}" ]]; then
        printf 'Error: required executable is unavailable: %s\n' "${required}" >&2
        exit 1
    fi
done
if [[ ! "${PROXY_TEST_UUID}" =~ ^[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$ ]]; then
    printf '%s\n' 'Error: PROXY_TEST_UUID must be a domain UUID' >&2
    exit 1
fi

umask 0077
WORKSPACE="$(mktemp -d /tmp/ansible-proxy-role-test.XXXXXX)"

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

PRODUCER_COMMIT="$(git -C "${PRODUCER_ROOT}" rev-parse --verify "${PROXY_CONTRACT_REF}^{commit}")"
test -n "$(git -C "${PRODUCER_ROOT}" branch -r --contains "${PRODUCER_COMMIT}")"
git -C "${PRODUCER_ROOT}" show "${PRODUCER_COMMIT}:bin/proxy_contract.bash" > "${WORKSPACE}/committed-contract.bash"
git -C "${PRODUCER_ROOT}" show "${PRODUCER_COMMIT}:tests/fixtures/proxy-artifacts.tsv" > "${WORKSPACE}/committed-artifacts.tsv"
cmp -- "${CONTRACT_SCRIPT}" "${WORKSPACE}/committed-contract.bash"
cmp -- "${CONTRACT_FIXTURE}" "${WORKSPACE}/committed-artifacts.tsv"
printf 'producer_commit=%s\n' "${PRODUCER_COMMIT}" > "${WORKSPACE}/source-ref.txt"

python3 - "${CONTRACT_FIXTURE}" "${WORKSPACE}/vars.json" "${PROXY_TEST_UUID}" "${CONTRACT_SCRIPT}" "${TARGET_HOST}" "${WORKSPACE}/completed.json" <<'PYTHON'
import csv
import hashlib
import json
import pathlib
import sys

with open(sys.argv[1], encoding="ascii", newline="") as source:
    artifacts = [row for row in csv.DictReader(source, delimiter="\t") if row["os"] == "rocky"]
if not artifacts or len({row["identity"] for row in artifacts}) != len(artifacts):
    raise SystemExit("Error: producer fixture has no unique Rocky artifact set")
for artifact in artifacts:
    artifact["stat_mode"] = format(int(artifact["mode"], 8), "o")
with open(sys.argv[2], "w", encoding="ascii") as target:
    json.dump({"proxy_role_test_uuid": sys.argv[3].lower(),
               "proxy_role_test_artifacts": artifacts,
               "proxy_role_test_target_host": sys.argv[5],
               "proxy_role_test_receipt": sys.argv[6],
               "proxy_contract_path": str(pathlib.Path(sys.argv[4]).resolve()),
               "proxy_role_test_contract_sha": hashlib.sha256(pathlib.Path(sys.argv[4]).read_bytes()).hexdigest()}, target)
PYTHON

sha256sum "${TOP}/roles/proxy/tasks/main.yml" "${TOP}/roles/proxy/defaults/main.yml" \
    "${CONTRACT_SCRIPT}" "${CONTRACT_FIXTURE}" "${SCRIPT_DIR}/check-proxy-role.bash" \
    "${SCRIPT_DIR}/proxy-role/"*.yml > "${WORKSPACE}/source-sha256.txt"

if ! ANSIBLE_CONFIG="${TOP}/ansible.cfg" ANSIBLE_NOCOLOR=1 \
    ANSIBLE_LOCAL_TEMP="${WORKSPACE}/ansible-local" \
    ANSIBLE_SSH_CONTROL_PATH_DIR="${WORKSPACE}/ansible-cp" \
    ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${RUNTIME_INVENTORY}" \
    --limit "${TARGET_HOST}" -e "@${WORKSPACE}/vars.json" \
    "${SCRIPT_DIR}/proxy-role/verify.yml" > "${WORKSPACE}/ansible.log" 2>&1; then
    printf '%s\n' '[ FAIL ] actual proxy role reconciliation; inspect the private workspace' >&2
    exit 1
fi

python3 - "${WORKSPACE}/completed.json" "${WORKSPACE}/vars.json" <<'PYTHON'
import json
import pathlib
import sys

receipt = pathlib.Path(sys.argv[1])
if not receipt.is_file() or receipt.stat().st_size == 0:
    raise SystemExit("Error: the dedicated guest did not complete the actual suite")
with open(sys.argv[2], encoding="ascii") as source:
    variables = json.load(source)
expected = {"schema": 1,
            "host": variables["proxy_role_test_target_host"],
            "uuid": variables["proxy_role_test_uuid"],
            "contract_sha256": variables["proxy_role_test_contract_sha"]}
with receipt.open(encoding="ascii") as source:
    if json.load(source) != expected:
        raise SystemExit("Error: the suite completion receipt does not match the assigned guest and source")
PYTHON

printf '%s\n' '[ PASS ] actual proxy role reconciliation on the dedicated guest'
