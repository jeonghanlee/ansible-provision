#!/usr/bin/env bash
#
# Verify Make inventory preflight and arbitrary generated-host selection.

set -euo pipefail

declare -g SCRIPT_DIR
declare -g TOP
declare -g WORKSPACE
declare -g RUNTIME_INVENTORY

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOP="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKSPACE="$(mktemp -d /tmp/ansible-runtime-inventory-test.XXXXXX)"
RUNTIME_INVENTORY="${WORKSPACE}/runtime.ini"

function cleanup {
    local rc=$?

    if [[ "${rc}" != "0" ]]; then
        printf "Retained workspace: %s\n" "${WORKSPACE}" >&2
        return "${rc}"
    fi
    rm -rf -- "${WORKSPACE}"
    return "${rc}"
}

trap cleanup EXIT

if make -s -C "${TOP}" ping ANSIBLE_CMD=true > "${WORKSPACE}/missing.log" 2>&1; then
    printf "%s\n" "Error: default inventory succeeded without RUNTIME_INVENTORY" >&2
    exit 1
fi
grep -Fq 'RUNTIME_INVENTORY is required' "${WORKSPACE}/missing.log"

printf "%s\n" \
    '[rocky8]' \
    'custom-prefix-rocky8-arbitrary ansible_host=192.168.122.201 ansible_user=vmadmin' \
    > "${RUNTIME_INVENTORY}"

make -s -C "${TOP}" ping ANSIBLE_CMD=true \
    RUNTIME_INVENTORY="${RUNTIME_INVENTORY}"

make -n -C "${TOP}" bare.rocky8 \
    RUNTIME_INVENTORY="${RUNTIME_INVENTORY}" \
    ANSIBLE_LIMIT=custom-prefix-rocky8-arbitrary \
    | grep -Fq -- '--limit custom-prefix-rocky8-arbitrary'

make -s -C "${TOP}" ping ANSIBLE_CMD=true INVENTORY="${RUNTIME_INVENTORY}"

printf "[ PASS ] default group inventory refuses a missing generated host source\n"
printf "[ PASS ] generated inventory and arbitrary host limit reach Make targets\n"
printf "[ PASS ] a site-owned complete inventory remains supported\n"
printf "Summary: 3 passed / 3 total\n"
