#!/usr/bin/env bash
#
# Verifies the shipped app_ioc_runner version-selector logic against real Git
# repositories. The shell under test is extracted from the role file itself, so
# the checks exercise the deployed code rather than a copy of it.
#
# Boundary substitutions, and nothing else:
#   - Jinja inventory values become fixture paths (the Ansible templating edge).
#   - sudo is shimmed away because the harness already runs as the target owner.
#   - The span ends before the provenance recorder call, which needs an
#     installed manifest and is covered by check-bake-provenance-recorder.bash.

set -euo pipefail

declare -g SCRIPT_DIR
declare -g TOP
declare -g ROLE_TASKS
declare -g WORKSPACE
declare -g SHIM_DIR
declare -g UPSTREAM
declare -g BLOCK
declare -g TEST_TOTAL=0
declare -g TEST_PASSED=0
declare -g TEST_FAILED=0
declare -ag FAILED_DETAILS=()

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOP="$(cd "${SCRIPT_DIR}/.." && pwd)"
ROLE_TASKS="${TOP}/roles/iocrunner/tasks/main.yml"

function cleanup {
    local rc=$?
    if [[ -n "${WORKSPACE:-}" && -d "${WORKSPACE}" ]]; then
        rm -rf "${WORKSPACE}"
    fi
    return "${rc}"
}

trap cleanup EXIT

function die {
    printf "error: %s\n" "$*" >&2
    exit 1
}

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

# Extracts the deployment task's shell body up to the provenance recorder call.
function extract_block {
    local extracted

    extracted="$(awk '
        /^- name: Deploy epics-ioc-runner infrastructure$/ { found = 1; next }
        found && /^  ansible\.builtin\.raw: \|$/ { body = 1; next }
        body && /record-iocrunner-source/ { exit }
        body { sub(/^    /, ""); print }
    ' "${ROLE_TASKS}")"

    [[ -n "${extracted}" ]] || die "could not extract the deployment task body"

    # Each substituted line must remain a bare inventory assignment, so that
    # logic added to one is never replaced silently by the harness.
    local marker
    for marker in owner src repo bin ref; do
        [[ "$(grep -c "^${marker}=" <<< "${extracted}")" == "1" ]] \
            || die "expected exactly one ${marker}= assignment in the task body"
        grep -Eq "^${marker}=\"\{\{[^\"]*\}\}\"$" <<< "${extracted}" \
            || die "${marker}= is no longer a bare inventory assignment"
    done
    grep -q '^set -e$' <<< "${extracted}" || die "task body does not set -e"

    printf "%s\n" "${extracted}"
}

# Runs the extracted block with the inventory values bound to fixture paths.
function run_block {
    local src="$1"
    local ref="$2"
    local script="${WORKSPACE}/block.bash"

    sed \
        -e "s|^owner=.*|owner=\"root\"|" \
        -e "s|^src=.*|src=\"${src}\"|" \
        -e "s|^repo=.*|repo=\"${UPSTREAM}\"|" \
        -e "s|^bin=.*|bin=\"${WORKSPACE}/unused-ioc-runner\"|" \
        -e "s|^ref=.*|ref=\"${ref}\"|" \
        <<< "${BLOCK}" > "${script}"

    PATH="${SHIM_DIR}:${PATH}" unshare -Ur /bin/bash "${script}"
}

function expect_block_success {
    local name="$1"
    local src="$2"
    local ref="$3"
    local output

    if output="$(run_block "${src}" "${ref}" 2>&1)"; then
        record_pass "${name}"
    else
        record_fail "${name}" "block exited nonzero: ${output}"
    fi
}

function expect_block_failure {
    local name="$1"
    local src="$2"
    local ref="$3"
    local expected="$4"
    local output

    if output="$(run_block "${src}" "${ref}" 2>&1)"; then
        record_fail "${name}" "block unexpectedly succeeded"
        return
    fi
    if [[ "${output}" == *"${expected}"* ]]; then
        record_pass "${name}"
    else
        record_fail "${name}" "expected message '${expected}', observed: ${output}"
    fi
}

function expect_head_commit {
    local name="$1"
    local src="$2"
    local expected="$3"
    local observed

    observed="$(git -C "${src}" rev-parse HEAD)"
    if [[ "${observed}" == "${expected}" ]]; then
        record_pass "${name}"
    else
        record_fail "${name}" "expected HEAD ${expected}, observed ${observed}"
    fi
}

function expect_head_attached {
    local name="$1"
    local src="$2"

    if git -C "${src}" symbolic-ref -q HEAD >/dev/null; then
        record_pass "${name}"
    else
        record_fail "${name}" "HEAD is detached"
    fi
}

function print_summary {
    printf "Summary: %s passed / %s total\n" "${TEST_PASSED}" "${TEST_TOTAL}"
    if [[ "${TEST_FAILED}" -gt "0" ]]; then
        printf "Failures:\n" >&2
        printf "  %s\n" "${FAILED_DETAILS[@]}" >&2
        return 1
    fi
}

WORKSPACE="$(mktemp -d /tmp/ioc-runner-selector-test.XXXXXX)"
chmod 0755 "${WORKSPACE}"

SHIM_DIR="${WORKSPACE}/shim"
mkdir "${SHIM_DIR}"
cat > "${SHIM_DIR}/sudo" <<'EOF'
#!/bin/bash
# The role calls `sudo -u <owner> <command>`; the harness already runs as that
# owner, so drop the flag and execute the command unchanged.
if [[ "$1" == "-u" ]]; then
    shift 2
fi
exec "$@"
EOF
chmod 0755 "${SHIM_DIR}/sudo"

# Upstream fixture: a default branch, a release tag, a disposable branch, and a
# tag deliberately shadowed by a same-named branch.
declare -g SEED="${WORKSPACE}/seed"
UPSTREAM="${WORKSPACE}/upstream.git"
git init -q -b main "${SEED}"
git -C "${SEED}" config user.name "Selector Test"
git -C "${SEED}" config user.email "selector@example.invalid"
printf "%s\n" "one" > "${SEED}/file.txt"
git -C "${SEED}" add file.txt
git -C "${SEED}" -c core.hooksPath=/dev/null commit -q -m "Create the first commit"
declare -g TAG_COMMIT
TAG_COMMIT="$(git -C "${SEED}" rev-parse HEAD)"
git -C "${SEED}" tag release-1.0.0
git -C "${SEED}" tag shadowed

git -C "${SEED}" checkout -q -b feature-x
printf "%s\n" "two" > "${SEED}/file.txt"
git -C "${SEED}" -c core.hooksPath=/dev/null commit -q -am "Extend the fixture on a branch"
declare -g BRANCH_COMMIT
BRANCH_COMMIT="$(git -C "${SEED}" rev-parse HEAD)"

git -C "${SEED}" checkout -q -b shadowed
printf "%s\n" "three" > "${SEED}/file.txt"
git -C "${SEED}" -c core.hooksPath=/dev/null commit -q -am "Diverge a branch that shadows a tag"

git -C "${SEED}" checkout -q main
printf "%s\n" "four" > "${SEED}/file.txt"
git -C "${SEED}" -c core.hooksPath=/dev/null commit -q -am "Advance the default branch"
declare -g MAIN_COMMIT
MAIN_COMMIT="$(git -C "${SEED}" rev-parse HEAD)"

git -C "${SEED}" checkout -q -b gone
git -C "${SEED}" checkout -q main
git clone -q --bare "${SEED}" "${UPSTREAM}"

BLOCK="$(extract_block)"

# A fresh host with no selector reproduces the pre-selector behavior.
declare -g SRC_FRESH="${WORKSPACE}/fresh/epics-ioc-runner"
expect_block_success "unset selector clones the default branch" "${SRC_FRESH}" ""
expect_head_commit "unset selector leaves the default-branch commit" "${SRC_FRESH}" "${MAIN_COMMIT}"
expect_head_attached "unset selector leaves HEAD attached" "${SRC_FRESH}"

# Re-running without a selector must not disturb an existing checkout.
expect_block_success "unset selector re-run is a no-op" "${SRC_FRESH}" ""
expect_head_commit "unset selector re-run keeps the commit" "${SRC_FRESH}" "${MAIN_COMMIT}"

# A released tag pins the checkout.
declare -g SRC_TAG="${WORKSPACE}/tagged/epics-ioc-runner"
expect_block_success "released tag is selectable" "${SRC_TAG}" "release-1.0.0"
expect_head_commit "released tag pins its commit" "${SRC_TAG}" "${TAG_COMMIT}"

# A tag wins over a branch of the same name.
declare -g SRC_SHADOW="${WORKSPACE}/shadowed/epics-ioc-runner"
expect_block_success "shadowed name resolves" "${SRC_SHADOW}" "shadowed"
expect_head_commit "tag wins over a same-named branch" "${SRC_SHADOW}" "${TAG_COMMIT}"

# A branch resolves through its remote-tracking ref.
declare -g SRC_BRANCH="${WORKSPACE}/branch/epics-ioc-runner"
expect_block_success "branch is selectable" "${SRC_BRANCH}" "feature-x"
expect_head_commit "branch pins its upstream commit" "${SRC_BRANCH}" "${BRANCH_COMMIT}"

# An explicit commit resolves through the hex arm.
declare -g SRC_SHA="${WORKSPACE}/sha/epics-ioc-runner"
expect_block_success "abbreviated commit is selectable" "${SRC_SHA}" "${TAG_COMMIT:0:12}"
expect_head_commit "abbreviated commit pins its commit" "${SRC_SHA}" "${TAG_COMMIT}"

# An unknown selector fails by name instead of falling back.
declare -g SRC_MISSING="${WORKSPACE}/missing/epics-ioc-runner"
expect_block_failure "unknown selector fails by name" "${SRC_MISSING}" "release-9.9.9" \
    "requested ioc_runner_version not found: release-9.9.9"

# Reviewer finding 1: clearing the selector must not silently leave a pinned
# checkout in place, because the record would then omit the requested ref.
declare -g SRC_UNPIN="${WORKSPACE}/unpin/epics-ioc-runner"
expect_block_success "pinned checkout is prepared" "${SRC_UNPIN}" "release-1.0.0"
expect_block_failure "cleared selector rejects a pinned checkout" "${SRC_UNPIN}" "" \
    "ioc_runner_version is unset"

# Reviewer finding 2: a selector deleted upstream must fail by name rather than
# resolve from a stale remote-tracking ref retained by the image.
declare -g SRC_STALE="${WORKSPACE}/stale/epics-ioc-runner"
expect_block_success "branch present upstream is selectable" "${SRC_STALE}" "gone"
git -C "${UPSTREAM}" branch -q -D gone
expect_block_failure "deleted upstream branch fails by name" "${SRC_STALE}" "gone" \
    "requested ioc_runner_version not found: gone"

# A selector deleted upstream as a tag must also stop resolving locally.
declare -g SRC_STALE_TAG="${WORKSPACE}/stale-tag/epics-ioc-runner"
git -C "${SEED}" tag temporary-1.0.0
git -C "${UPSTREAM}" fetch -q "${SEED}" 'refs/tags/*:refs/tags/*'
expect_block_success "tag present upstream is selectable" "${SRC_STALE_TAG}" "temporary-1.0.0"
git -C "${UPSTREAM}" tag -d temporary-1.0.0 >/dev/null
expect_block_failure "deleted upstream tag fails by name" "${SRC_STALE_TAG}" "temporary-1.0.0" \
    "requested ioc_runner_version not found: temporary-1.0.0"

# An unreadable HEAD must be reported as such, not as a pinned checkout.
declare -g SRC_BROKEN="${WORKSPACE}/broken/epics-ioc-runner"
expect_block_success "readable checkout is prepared" "${SRC_BROKEN}" ""
rm -f "${SRC_BROKEN}/.git/HEAD"
expect_block_failure "unreadable HEAD is reported distinctly" "${SRC_BROKEN}" "" \
    "cannot read HEAD"

print_summary
