#!/usr/bin/env bash
#
# Verifies the shipped bake recorder in an isolated root mount namespace.

set -euo pipefail

declare -g SCRIPT_DIR
declare -g TOP
declare -g RECORDER
declare -g WORKSPACE
declare -g CHECKOUT
declare -g TEST_TOTAL=0
declare -g TEST_PASSED=0
declare -g TEST_FAILED=0
declare -ag FAILED_DETAILS=()

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOP="$(cd "${SCRIPT_DIR}/.." && pwd)"
RECORDER="${TOP}/roles/bake_provenance/files/record-iocrunner-source.bash"

function cleanup {
    local rc=$?
    if [[ -n "${WORKSPACE:-}" && -d "${WORKSPACE}" ]]; then
        rm -rf "${WORKSPACE}"
    fi
    return "${rc}"
}

trap cleanup EXIT

function record_pass {
    local name="$1"
    TEST_TOTAL=$((TEST_TOTAL + 1))
    TEST_PASSED=$((TEST_PASSED + 1))
    printf "[ PASS ] %s\n" "${name}"
}

function record_fail {
    local name="$1"
    local detail="$2"
    TEST_TOTAL=$((TEST_TOTAL + 1))
    TEST_FAILED=$((TEST_FAILED + 1))
    FAILED_DETAILS+=("${name}: ${detail}")
    printf "[ FAIL ] %s\n" "${name}" >&2
    printf "  %s\n" "${detail}" >&2
}

function expect_success {
    local name="$1"
    shift
    if "$@"; then
        record_pass "${name}"
    else
        record_fail "${name}" "command returned nonzero"
    fi
}

function expect_failure {
    local name="$1"
    shift
    if "$@"; then
        record_fail "${name}" "command unexpectedly succeeded"
    else
        record_pass "${name}"
    fi
}

function run_isolated {
    local etc_dir="$1"
    local mode="$2"
    shift 2

    # shellcheck disable=SC2016
    unshare -Ur -m /bin/bash -c '
        set -e
        mount --make-rprivate /
        mount --bind "$1" /etc
        shift
        recorder="$1"
        mode="$2"
        shift 2
        if [[ "${mode}" == "plain" ]]; then
            exec /bin/bash "${recorder}" "$@"
        fi
        exec env GIT_DIR=/nonexistent "${recorder}" "$@"
    ' _ "${etc_dir}" "${RECORDER}" "${mode}" "$@"
}

function write_header {
    local manifest="$1"
    cat > "${manifest}" <<'EOF'
# iocrunner golden bake manifest
manifest_schema 1
bake_date 2026-07-29T00:00:00Z
os_type rocky8
cloud-provision 1111111111111111111111111111111111111111
ansible-provision 2222222222222222222222222222222222222222
epics_env_version 1.2.2
epics_base_version 7.0.10
base_image schema=1 name=base.qcow2 sha256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
EOF
    chmod 0644 "${manifest}"
}

function expect_record {
    local name="$1"
    local manifest="$2"
    local pattern="$3"

    if grep -Eq "${pattern}" "${manifest}"; then
        record_pass "${name}"
    else
        record_fail "${name}" "record did not match ${pattern}"
    fi
}

function test_interrupted_write {
    local etc_dir="$1"
    local manifest="${etc_dir}/iocrunner-bake.manifest"
    local before="${etc_dir}/manifest.before"
    local index

    for ((index = 0; index < 200000; index++)); do
        printf "pip3 package-%06d==1\n" "${index}" >> "${manifest}"
    done
    cp "${manifest}" "${before}"

    # shellcheck disable=SC2016
    if ! unshare -Ur -m /bin/bash -c '
        set -e
        mount --make-rprivate /
        mount --bind "$1" /etc
        recorder="$2"
        checkout="$3"
        before="$4"
        "${recorder}" app_con https://github.com/jeonghanlee/con "${checkout}" &
        pid=$!
        while ! compgen -G "/etc/.iocrunner-bake.manifest.tmp.*" >/dev/null; do
            kill -0 "${pid}" 2>/dev/null || exit 1
        done
        kill -STOP "${pid}"
        kill -TERM "${pid}"
        kill -CONT "${pid}"
        if wait "${pid}"; then
            exit 1
        fi
        if ! cmp -s /etc/iocrunner-bake.manifest "${before}"; then
            printf "%s\n" "interrupted recorder replaced the manifest" >&2
            exit 2
        fi
        if compgen -G "/etc/.iocrunner-bake.manifest.tmp.*" >/dev/null; then
            printf "%s\n" "interrupted recorder left a temporary file" >&2
            exit 3
        fi
    ' _ "${etc_dir}" "${RECORDER}" "${CHECKOUT}" "${before}"; then
        record_fail "interrupted write remains atomic" "final file changed or temporary file remained"
        return
    fi
    record_pass "interrupted write remains atomic"
}

function print_summary {
    printf "Summary: %s passed / %s total\n" "${TEST_PASSED}" "${TEST_TOTAL}"
    if [[ "${TEST_FAILED}" -gt "0" ]]; then
        printf "Failures:\n" >&2
        printf "  %s\n" "${FAILED_DETAILS[@]}" >&2
        return 1
    fi
}

WORKSPACE="$(mktemp -d /tmp/bake-provenance-recorder-test.XXXXXX)"
chmod 0755 "${WORKSPACE}"
CHECKOUT="${WORKSPACE}/checkout"
git init -q "${CHECKOUT}"
git -C "${CHECKOUT}" config user.name "Recorder Test"
git -C "${CHECKOUT}" config user.email "recorder@example.invalid"
printf "%s\n" "source" > "${CHECKOUT}/source.txt"
git -C "${CHECKOUT}" add source.txt
git -C "${CHECKOUT}" -c core.hooksPath=/dev/null commit -q -m "Create source fixture"

declare -g ETC_DIR="${WORKSPACE}/etc"
declare -g MANIFEST="${ETC_DIR}/iocrunner-bake.manifest"
mkdir "${ETC_DIR}"
chmod 0755 "${ETC_DIR}"
cp -a /etc/alternatives "${ETC_DIR}/"
cp /etc/passwd /etc/group /etc/nsswitch.conf "${ETC_DIR}/"

expect_success "absent manifest is a no-op" \
    run_isolated "${ETC_DIR}" direct app_con https://github.com/jeonghanlee/con "${CHECKOUT}"
if [[ ! -e "${MANIFEST}" ]]; then
    record_pass "absent manifest remains absent"
else
    record_fail "absent manifest remains absent" "recorder created the manifest"
fi

expect_failure "unknown application is rejected" \
    run_isolated "${ETC_DIR}" direct app_unknown https://example.invalid/repo "${CHECKOUT}"
expect_failure "plain Bash execution is rejected" \
    run_isolated "${ETC_DIR}" plain app_con https://github.com/jeonghanlee/con "${CHECKOUT}"

write_header "${MANIFEST}"
expect_success "clean untagged checkout records" \
    run_isolated "${ETC_DIR}" direct app_con https://github.com/jeonghanlee/con "${CHECKOUT}"
expect_record "clean untagged state is exact" "${MANIFEST}" \
    '^app_con schema=1 repo=https://github.com/jeonghanlee/con commit=[0-9a-f]{40} state=clean-untagged tag=- recorded_at=.*Z$'

git -C "${CHECKOUT}" tag zeta
git -C "${CHECKOUT}" tag alpha
expect_success "clean tagged checkout records" \
    run_isolated "${ETC_DIR}" direct app_procserv https://github.com/jeonghanlee/procServ-env "${CHECKOUT}"
expect_record "tag selection is deterministic" "${MANIFEST}" \
    '^app_procserv .* state=clean-tagged tag=alpha recorded_at=.*Z$'

printf "%s\n" "dirty" >> "${CHECKOUT}/source.txt"
expect_success "dirty checkout records" \
    run_isolated "${ETC_DIR}" direct app_conserver https://github.com/jeonghanlee/conserver-env "${CHECKOUT}"
expect_record "dirty state takes precedence" "${MANIFEST}" \
    '^app_conserver .* state=dirty tag=- recorded_at=.*Z$'

expect_success "repeated recording succeeds" \
    run_isolated "${ETC_DIR}" direct app_con https://github.com/jeonghanlee/con "${CHECKOUT}"
if [[ "$(grep -c '^app_con ' "${MANIFEST}")" == "1" ]]; then
    record_pass "repeated recording keeps one record"
else
    record_fail "repeated recording keeps one record" "duplicate app_con record found"
fi

cp "${MANIFEST}" "${WORKSPACE}/valid.manifest"
printf "%s\n" "bad header" > "${MANIFEST}"
expect_failure "malformed header is rejected" \
    run_isolated "${ETC_DIR}" direct app_con https://github.com/jeonghanlee/con "${CHECKOUT}"
cp "${WORKSPACE}/valid.manifest" "${MANIFEST}"

rm -f "${MANIFEST}"
ln -s "${WORKSPACE}/valid.manifest" "${MANIFEST}"
expect_failure "symbolic-link manifest is rejected" \
    run_isolated "${ETC_DIR}" direct app_con https://github.com/jeonghanlee/con "${CHECKOUT}"
rm "${MANIFEST}"
mkdir "${MANIFEST}"
expect_failure "non-regular manifest is rejected" \
    run_isolated "${ETC_DIR}" direct app_con https://github.com/jeonghanlee/con "${CHECKOUT}"
rmdir "${MANIFEST}"

cp "${WORKSPACE}/valid.manifest" "${MANIFEST}"
chmod 0777 "${ETC_DIR}"
expect_failure "unsafe parent is rejected" \
    run_isolated "${ETC_DIR}" direct app_con https://github.com/jeonghanlee/con "${CHECKOUT}"
chmod 0755 "${ETC_DIR}"

test_interrupted_write "${ETC_DIR}"
print_summary
