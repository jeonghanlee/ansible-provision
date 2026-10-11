#!/usr/bin/env bash
# tests/check-proxy-check-target.bash
# Real-target verification of the proxy_check role. Runs the shipped group and
# focused playbooks through ansible-playbook with Ansible become on one dedicated
# guest, using the pinned cloud-provision checker and its shipped unmarked fixture.
# No role task, wrapper, checker, filesystem operation, or SSH connection is
# replaced. The guest is restored from a guest-local backup before the script
# exits. Requires a disposable guest assigned to this test; see
# tests/proxy-check/README.md.
set -uo pipefail

declare -g TOP SELF_NAME WORKSPACE LOGS INVENTORY HOST TARGET OWNER UUID
declare -g CONTRACT_ROOT INPUT_PATH RUNTIME_DIR PIN CHECKER FIXTURE ARTIFACTS
declare -g BACKUP_DIR MUTATED RC PIP_PATH
declare -a FILES=() KEEP_PATHS=()
declare -i PASS=0 FAIL=0
TOP="$(cd "$(dirname "$0")/.." && pwd)"
SELF_NAME="$(basename "$0")"
INPUT_PATH=/etc/server-configuration/proxy-check.input
RUNTIME_DIR=/run/cloud-provision
BACKUP_DIR=/root/proxy-check-suite-backup
CONTRACT_ROOT="${TOP}/../cloud-provision"
LOGS=""
MUTATED=0
RC=0
readonly BAD_PIN=0000000000000000000000000000000000000000000000000000000000000000
readonly GROUP_PLAYBOOK=species/archiver_server_sqlite
readonly FOCUSED_PLAYBOOK=operators/archiver_build

function usage {
    printf 'Usage: %s --inventory FILE --host NAME --uuid UUID --target rocky8|non-rocky --owner ACCOUNT\n' "${SELF_NAME}"
    printf '       [--contract-root DIR] [--input-path PATH] [--runtime-dir DIR] [--logs DIR]\n'
}

function die {
    printf 'Error: %s\n' "$1" >&2
    exit 2
}

function parse_args {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --inventory) INVENTORY="${2:-}"; shift 2 ;;
            --host) HOST="${2:-}"; shift 2 ;;
            --uuid) UUID="${2:-}"; shift 2 ;;
            --target) TARGET="${2:-}"; shift 2 ;;
            --owner) OWNER="${2:-}"; shift 2 ;;
            --contract-root) CONTRACT_ROOT="${2:-}"; shift 2 ;;
            --input-path) INPUT_PATH="${2:-}"; shift 2 ;;
            --runtime-dir) RUNTIME_DIR="${2:-}"; shift 2 ;;
            --logs) LOGS="${2:-}"; shift 2 ;;
            -h|--help) usage; exit 0 ;;
            *) usage >&2; die "unknown argument: $1" ;;
        esac
    done
}

function validate_args {
    local name
    for name in INVENTORY HOST UUID TARGET OWNER; do
        if [[ -z "${!name:-}" ]]; then
            usage >&2
            die "missing required option for ${name}"
        fi
    done
    [[ -r "${INVENTORY}" ]] || die "inventory is not readable: ${INVENTORY}"
    [[ "${TARGET}" == rocky8 || "${TARGET}" == non-rocky ]] || die "--target must be rocky8 or non-rocky"
    [[ "${UUID}" =~ ^[0-9a-fA-F-]{36}$ ]] || die "--uuid must be the provider domain UUID"
    [[ "${INPUT_PATH}" == /* && "${INPUT_PATH}" != *[!A-Za-z0-9_./-]* ]] || die "--input-path must be a plain absolute path"
    [[ "${RUNTIME_DIR}" == /* && "${RUNTIME_DIR}" != *[!A-Za-z0-9_./-]* ]] || die "--runtime-dir must be a plain absolute path"
}

function derive_inputs {
    CONTRACT_ROOT="$(cd "${CONTRACT_ROOT}" 2> /dev/null && pwd)" || die "contract root does not exist"
    CHECKER="${CONTRACT_ROOT}/bin/proxy_contract.bash"
    FIXTURE="${CONTRACT_ROOT}/tests/fixtures/proxy-general-server-unmarked"
    ARTIFACTS="${CONTRACT_ROOT}/tests/fixtures/proxy-general-server-artifacts.tsv"
    PIN="$(sed -n 's/^proxy_check_contract_sha256: "\([0-9a-f]\{64\}\)"$/\1/p' "${TOP}/roles/proxy_check/defaults/main.yml")"
    [[ -n "${PIN}" ]] || die "role default pin not found"
    if ! grep -Fq 'role: proxy_check' "${TOP}/playbooks/${GROUP_PLAYBOOK}.yml" \
        || ! grep -Fq 'role: proxy_check' "${TOP}/playbooks/${FOCUSED_PLAYBOOK}.yml"; then
        die "the proxy_check role is not wired into the group and focused playbooks; see README.md"
    fi
    [[ -f "${CHECKER}" && -d "${FIXTURE}" && -f "${ARTIFACTS}" ]] || die "checker or fixture missing under ${CONTRACT_ROOT}"
    if [[ "$(sha256sum -- "${CHECKER}" | cut -d' ' -f1)" != "${PIN}" ]]; then
        die "checker source does not match the pinned SHA-256"
    fi
    local os identity path rest
    while IFS=$'\t' read -r os identity path rest; do
        if [[ "${os}" == rocky ]]; then
            FILES+=("${path}")
            if [[ "${identity}" == pip ]]; then
                PIP_PATH="${path}"
            fi
        fi
    done < "${ARTIFACTS}"
    [[ "${#FILES[@]}" -gt 0 && -n "${PIP_PATH:-}" ]] || die "artifact paths not found in ${ARTIFACTS}"
    KEEP_PATHS=("${FILES[@]}" "${INPUT_PATH}")
}

function root_raw {
    ansible -i "${WORKSPACE}/inventory.ini" "${HOST}" -m raw -a "$1" \
        -e ansible_become=true -e ansible_become_flags=-n 2>&1
}

function snap {
    root_raw "for f in ${KEEP_PATHS[*]}; do if [ -e \$f ]; then stat -c '%n %u:%g %a %h %s %Y' \$f; sha256sum \$f; else echo \"\$f absent\"; fi; done" \
        | grep -v -E 'CHANGED|Shared connection|UNREACHABLE'
}

function put_file {
    local src="$1" dest="$2" mode="$3" b64
    b64="$(base64 -w0 < "${src}")"
    root_raw "umask 077; mkdir -p -- \$(dirname ${dest}); printf %s '${b64}' | base64 -d > ${dest}.tmp && chmod ${mode} ${dest}.tmp && chown root:root ${dest}.tmp && mv -f ${dest}.tmp ${dest}" > /dev/null
}

function make_input {
    local pin="$1" url="$2" out="${WORKSPACE}/input.tmp"
    sed -e "s|^script_sha256=.*|script_sha256=${pin}|" -e "s|^proxy_url=.*|proxy_url=${url}|" \
        "${FIXTURE}/desired.input" > "${out}"
    put_file "${out}" "${INPUT_PATH}" 0600
    rm -f -- "${out}"
}

function install_fixture_files {
    local f
    for f in "${FILES[@]}"; do
        put_file "${FIXTURE}${f}" "${f}" 0644
    done
}

function backup_guest {
    local parent
    parent="$(dirname "${INPUT_PATH}")"
    root_raw "if [ -e ${BACKUP_DIR} ]; then echo backup-exists; else mkdir -m 0700 ${BACKUP_DIR} && for f in ${KEEP_PATHS[*]}; do if [ -e \$f ]; then cp -a --parents \$f ${BACKUP_DIR}; fi; done; if [ -d ${RUNTIME_DIR} ]; then cp -a ${RUNTIME_DIR} ${BACKUP_DIR}/runtime-dir; fi; if [ -d ${parent} ]; then touch ${BACKUP_DIR}/parent-existed; fi; echo backup-ready; fi" | grep -Fq backup-ready
}

function restore_guest {
    local parent
    parent="$(dirname "${INPUT_PATH}")"
    root_raw "for f in ${KEEP_PATHS[*]}; do rm -f \$f; if [ -e ${BACKUP_DIR}\$f ]; then cp -a ${BACKUP_DIR}\$f \$f; fi; done; rm -f ${INPUT_PATH}.link; if [ ! -e ${BACKUP_DIR}/parent-existed ]; then rmdir ${parent} 2>/dev/null; fi; rm -rf ${RUNTIME_DIR}; if [ -d ${BACKUP_DIR}/runtime-dir ]; then cp -a ${BACKUP_DIR}/runtime-dir ${RUNTIME_DIR}; fi" > /dev/null
}

function cleanup {
    local rc=$?
    if [[ "${MUTATED}" == 1 ]]; then
        restore_guest
        snap > "${WORKSPACE}/snap-restored-on-exit.txt"
        if [[ -f "${WORKSPACE}/snap-original.txt" ]] && ! diff -q "${WORKSPACE}/snap-original.txt" "${WORKSPACE}/snap-restored-on-exit.txt" > /dev/null; then
            printf 'Error: guest differs from its original state after restore; backup kept at %s\n' "${BACKUP_DIR}" >&2
            rc=1
        fi
    fi
    if [[ "${rc}" != 0 || "${KEEP_WORKSPACE:-0}" == 1 ]]; then
        printf 'Retained workspace: %s\n' "${WORKSPACE}" >&2
        return "${rc}"
    fi
    rm -rf -- "${WORKSPACE}"
    return "${rc}"
}

function run_play {
    local label="$1" playbook="$2"
    shift 2
    ansible-playbook -i "${TOP}/inventory/lab.ini" -i "${WORKSPACE}/inventory.ini" --limit "${HOST}" \
        -e "@${WORKSPACE}/site.yml" -e ansible_become=true -e ansible_become_flags=-n "$@" \
        "${TOP}/playbooks/${playbook}.yml" > "${LOGS}/${label}.log" 2>&1
    RC=$?
}

function verdict {
    if [[ "$1" == 1 ]]; then
        PASS=$((PASS + 1))
        printf '[ PASS ] %s: %s\n' "$2" "$3"
    else
        FAIL=$((FAIL + 1))
        printf '[ FAIL ] %s: %s\n' "$2" "$3"
    fi
}

function expect_fail_token {
    local label="$1" token="$2"
    if [[ "${RC}" != 0 ]] && grep -Fq -- "${token}" "${LOGS}/${label}.log"; then
        verdict 1 "${label}" "play failed with '${token}'"
    else
        verdict 0 "${label}" "rc=${RC}; expected failure with '${token}'"
    fi
}

function expect_ok {
    local label="$1" note="$2"
    if [[ "${RC}" == 0 ]] && grep -Eq "^${HOST}[[:space:]]+:.*failed=0" "${LOGS}/${label}.log"; then
        verdict 1 "${label}" "${note}"
    else
        verdict 0 "${label}" "rc=${RC}; expected success"
    fi
}

function expect_same_snapshot {
    local label="$1" before="$2" after="$3" note="$4"
    if diff -q "${before}" "${after}" > /dev/null; then
        verdict 1 "${label}" "${note}"
    else
        verdict 0 "${label}" "protected files changed"
    fi
}

function verify_target_identity {
    local uuid_seen os_id os_version release
    uuid_seen="$(root_raw 'cat /sys/class/dmi/id/product_uuid' | grep -E -o '[0-9A-Fa-f-]{36}' | head -1 | tr '[:upper:]' '[:lower:]')"
    [[ "${uuid_seen}" == "$(printf '%s' "${UUID}" | tr '[:upper:]' '[:lower:]')" ]] || die "target UUID does not match --uuid; nothing was changed"
    release="$(root_raw "grep -E '^(ID|VERSION_ID)=' /etc/os-release" | tr -d '"')"
    os_id="$(printf '%s\n' "${release}" | grep -E -o '^ID=[a-z0-9._-]+' | head -1)"
    os_version="$(printf '%s\n' "${release}" | grep -E -o '^VERSION_ID=[0-9.]+' | head -1)"
    if [[ "${TARGET}" == rocky8 ]]; then
        [[ "${os_id}" == ID=rocky && "${os_version}" == VERSION_ID=8.10 ]] || die "--target rocky8 requires Rocky Linux 8.10"
    else
        if [[ "${os_id}" == ID=rocky && "${os_version}" == VERSION_ID=8.10 ]]; then
            die "--target non-rocky requires a target that is not Rocky Linux 8.10"
        fi
    fi
    printf 'Target identity verified: %s %s\n' "${os_id}" "${os_version}"
}

function run_rocky_cases {
    local before="${WORKSPACE}/snap-ready-before.txt" after="${WORKSPACE}/snap-ready-after.txt"

    printf '== input file absent\n'
    run_play c01-input-absent "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token c01-input-absent 'proxy_check status=refused detail=input-unavailable'

    printf '== input present, files hold other values\n'
    make_input "${PIN}" http://proxy.example.org:3128
    run_play c02-other-values "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token c02-other-values 'proxy_check status=needs-change detail=none'
    run_play c02b-other-values-check "${GROUP_PLAYBOOK}" --tags always -C
    expect_fail_token c02b-other-values-check 'proxy_check status=needs-change detail=none'

    printf '== matching unmarked files, runtime state as found\n'
    install_fixture_files
    snap > "${before}"
    run_play c03-ready "${GROUP_PLAYBOOK}" --tags always
    expect_ok c03-ready 'ready, checker exit 0'
    run_play c03b-ready-check "${GROUP_PLAYBOOK}" --tags always -C
    expect_ok c03b-ready-check 'ready under --check (checker still executed)'
    snap > "${after}"
    expect_same_snapshot c03c-snapshot "${before}" "${after}" 'protected files and input unchanged by the checks'

    printf '== runtime state removed\n'
    root_raw "rm -rf ${RUNTIME_DIR}" > /dev/null
    run_play c04-no-runtime-state "${GROUP_PLAYBOOK}" --tags always
    expect_ok c04-no-runtime-state 'ready with no runtime state'

    printf '== different desired value\n'
    make_input "${PIN}" http://other.example.org:3128
    run_play c05-different "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token c05-different 'proxy_check status=needs-change detail=none'

    printf '== private input pin differs from the executed source\n'
    make_input "${BAD_PIN}" http://proxy.example.org:3128
    run_play c06-input-pin "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token c06-input-pin 'proxy_check status=refused'

    printf '== role pin differs from the staged source\n'
    make_input "${PIN}" http://proxy.example.org:3128
    run_play c07-role-pin "${GROUP_PLAYBOOK}" --tags always -e "proxy_check_contract_sha256=${BAD_PIN}"
    expect_fail_token c07-role-pin 'proxy_check status=refused detail=source-mismatch'

    printf '== unsafe input mode and symlink\n'
    root_raw "chmod 0644 ${INPUT_PATH}" > /dev/null
    run_play c08-mode "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token c08-mode 'proxy_check status=refused'
    make_input "${PIN}" http://proxy.example.org:3128
    root_raw "ln -sfn ${INPUT_PATH} ${INPUT_PATH}.link" > /dev/null
    run_play c08b-symlink "${GROUP_PLAYBOOK}" --tags always -e "proxy_check_input_path=${INPUT_PATH}.link"
    expect_fail_token c08b-symlink 'proxy_check status=refused detail=input-unavailable'
    root_raw "rm -f ${INPUT_PATH}.link" > /dev/null

    printf '== input path unset or relative\n'
    run_play c09-empty "${GROUP_PLAYBOOK}" --tags always -e 'proxy_check_input_path='
    expect_fail_token c09-empty 'proxy_check status=refused detail=invalid-input-path'
    run_play c09b-relative "${GROUP_PLAYBOOK}" --tags always -e 'proxy_check_input_path=etc/proxy-check.input'
    expect_fail_token c09b-relative 'proxy_check status=refused detail=invalid-input-path'

    printf '== control character in a configuration file\n'
    root_raw "printf '# x\\177\\n' >> ${PIP_PATH}" > /dev/null
    run_play c10-control-char "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token c10-control-char 'proxy_check status=refused'
    put_file "${FIXTURE}${PIP_PATH}" "${PIP_PATH}" 0644

    printf '== focused archiver_build operator\n'
    make_input "${PIN}" http://other.example.org:3128
    run_play c11-focused-stop "${FOCUSED_PLAYBOOK}" --tags archiver_build
    expect_fail_token c11-focused-stop 'proxy_check status=needs-change detail=none'
    if grep -Fq 'archiver_build :' "${LOGS}/c11-focused-stop.log"; then
        verdict 0 c11b-no-build 'an archiver_build task ran after a failed check'
    else
        verdict 1 c11b-no-build 'no archiver_build task ran after a failed check'
    fi
    make_input "${PIN}" http://proxy.example.org:3128
    run_play c11c-focused-ready "${FOCUSED_PLAYBOOK}" --tags archiver_build -C
    if grep -Fq 'proxy_check : Require a ready proxy check' "${LOGS}/c11c-focused-ready.log"; then
        verdict 1 c11c-focused-ready 'focused operator ran the proxy check under --check'
    else
        verdict 0 c11c-focused-ready 'focused operator did not run the proxy check'
    fi
    run_play c11d-focused-cloud "${FOCUSED_PLAYBOOK}" --tags archiver_build -C -e proxy_scope=cloud
    if grep -A1 'proxy_check : Run the read-only proxy check' "${LOGS}/c11d-focused-cloud.log" | grep -Fq 'skipping:'; then
        verdict 1 c11d-focused-cloud 'cloud scope skips the proxy check'
    else
        verdict 0 c11d-focused-cloud 'cloud scope did not skip the proxy check'
    fi
}

function run_non_rocky_cases {
    local with_input="${WORKSPACE}/snap-with-input.txt" after="${WORKSPACE}/snap-after.txt"

    printf '== input file absent\n'
    run_play d01-input-absent "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token d01-input-absent 'proxy_check status=refused detail=input-unavailable'

    printf '== fixture input on a non-Rocky target\n'
    make_input "${PIN}" http://proxy.example.org:3128
    snap > "${with_input}"
    run_play d02-non-rocky "${GROUP_PLAYBOOK}" --tags always
    expect_fail_token d02-non-rocky 'proxy_check status=refused detail=runtime.os.unsupported-platform'
    run_play d02b-non-rocky-check "${GROUP_PLAYBOOK}" --tags always -C
    expect_fail_token d02b-non-rocky-check 'proxy_check status=refused detail=runtime.os.unsupported-platform'
    if grep -Fq 'Apply the common operator' "${LOGS}/d02-non-rocky.log"; then
        verdict 0 d02c-no-operator 'an operator ran after the refusal'
    else
        verdict 1 d02c-no-operator 'no operator ran after the refusal'
    fi
    snap > "${after}"
    expect_same_snapshot d03-snapshot "${with_input}" "${after}" 'protected files and input unchanged'
}

function main {
    parse_args "$@"
    validate_args
    derive_inputs
    WORKSPACE="$(mktemp -d /tmp/proxy-check-target.XXXXXX)"
    trap cleanup EXIT
    LOGS="${LOGS:-${WORKSPACE}/logs}"
    mkdir -p "${LOGS}"
    export ANSIBLE_CONFIG="${TOP}/ansible.cfg" ANSIBLE_NOCOLOR=1 ANSIBLE_LOCAL_TEMP="${WORKSPACE}/ansible-local"
    { cat "${INVENTORY}"; printf '\n[rocky8]\n%s\n\n[archiver_server_sqlite]\n%s\n' "${HOST}" "${HOST}"; } > "${WORKSPACE}/inventory.ini"
    printf '%s\n' '---' "# ${WORKSPACE}/site.yml" "epics_ioc_engineers: [${OWNER}]" \
        "proxy_check_input_path: ${INPUT_PATH}" > "${WORKSPACE}/site.yml"

    verify_target_identity
    MUTATED=1
    if ! backup_guest; then
        MUTATED=0
        die "guest backup could not be created or already exists at ${BACKUP_DIR}"
    fi
    snap > "${WORKSPACE}/snap-original.txt"

    if [[ "${TARGET}" == rocky8 ]]; then
        run_rocky_cases
    else
        run_non_rocky_cases
    fi

    printf '== no input value in any play output\n'
    if grep -l -E 'example\.org|:3128' "${LOGS}"/*.log > "${WORKSPACE}/leaks.txt" 2> /dev/null && [[ -s "${WORKSPACE}/leaks.txt" ]]; then
        verdict 0 no-leak "values found in $(tr '\n' ' ' < "${WORKSPACE}/leaks.txt")"
    else
        verdict 1 no-leak 'no input value in any play output'
    fi

    printf '== restore\n'
    restore_guest
    MUTATED=0
    snap > "${WORKSPACE}/snap-restored.txt"
    expect_same_snapshot restore "${WORKSPACE}/snap-original.txt" "${WORKSPACE}/snap-restored.txt" 'guest matches its original state'
    root_raw "rm -rf ${BACKUP_DIR}" > /dev/null
    printf 'Summary: %d passed / %d failed\n' "${PASS}" "${FAIL}"
    [[ "${FAIL}" == 0 ]]
}

main "$@"
