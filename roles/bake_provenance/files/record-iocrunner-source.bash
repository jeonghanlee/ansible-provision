#!/bin/bash -p
#
# Records one application checkout in the active IOC runner bake manifest.

if [[ ! -o privileged ]]; then
    printf "%s\n" "error: execute this script directly or with /bin/bash -p" >&2
    exit 1
fi

set -euo pipefail

unset BASH_ENV ENV CDPATH
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY
unset GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_CONFIG_GLOBAL GIT_CONFIG_SYSTEM
unset GIT_CONFIG_COUNT GIT_CEILING_DIRECTORIES
unset TMPDIR TMP TEMP

readonly SAFE_PATH="/usr/sbin:/usr/bin:/sbin:/bin"
export PATH="${SAFE_PATH}"
export LC_ALL=C

readonly MANIFEST="/etc/iocrunner-bake.manifest"
readonly MANIFEST_HEADER="# iocrunner golden bake manifest"
readonly MANIFEST_SCHEMA="manifest_schema 1"

declare -g TEMP_FILE=""

function die {
    printf "error: %s\n" "$*" >&2
    exit 1
}

function cleanup {
    local rc=$?
    if [[ -n "${TEMP_FILE}" ]]; then
        /usr/bin/rm -f -- "${TEMP_FILE}"
    fi
    return "${rc}"
}

function require_command {
    local command_name="$1"
    local command_path

    command_path="$(command -v "${command_name}" 2>/dev/null || true)"
    [[ -n "${command_path}" && -x "${command_path}" ]] \
        || die "required command not found: ${command_name}"
}

function validate_record_value {
    local field_name="$1"
    local value="$2"

    [[ -n "${value}" ]] || die "${field_name} must not be empty"
    [[ "${value}" != *[[:space:]]* ]] \
        || die "${field_name} contains whitespace"
}

function validate_parent {
    local parent="$1"
    local owner mode

    [[ -d "${parent}" && ! -L "${parent}" ]] \
        || die "manifest parent is not a regular directory: ${parent}"

    read -r owner mode < <(/usr/bin/stat -Lc '%u %a' -- "${parent}")
    [[ "${owner}" == "0" ]] || die "manifest parent is not owned by root"
    (( (8#${mode} & 8#022) == 0 )) \
        || die "manifest parent is group- or world-writable"
}

function validate_manifest {
    local line
    local line_number=0
    local schema_count=0
    local key
    local tail_value
    local requested_value

    [[ ! -L "${MANIFEST}" ]] || die "manifest must not be a symbolic link"
    [[ -f "${MANIFEST}" ]] || die "manifest must be a regular file"
    [[ "$(/usr/bin/stat -Lc '%u' -- "${MANIFEST}")" == "0" ]] \
        || die "manifest is not owned by root"
    (( (8#$(/usr/bin/stat -Lc '%a' -- "${MANIFEST}") & 8#022) == 0 )) \
        || die "manifest is group- or world-writable"

    while IFS= read -r line || [[ -n "${line}" ]]; do
        line_number=$((line_number + 1))
        if [[ "${line_number}" == "1" ]]; then
            [[ "${line}" == "${MANIFEST_HEADER}" ]] \
                || die "manifest header is malformed"
            continue
        fi

        [[ -n "${line}" ]] || die "manifest contains an empty line"
        key="${line%% *}"
        case "${key}" in
            manifest_schema)
                [[ "${line}" == "${MANIFEST_SCHEMA}" ]] \
                    || die "manifest schema is malformed"
                schema_count=$((schema_count + 1))
                ;;
            bake_date|os_type|cloud-provision|ansible-provision|epics_env_version|epics_base_version)
                [[ "${line}" == "${key} "* && "${line#* }" != *[[:space:]]* ]] \
                    || die "manifest record is malformed at line ${line_number}"
                ;;
            base_image)
                [[ "${line}" == base_image\ schema=1\ name=*\ sha256=* ]] \
                    || die "base image record is malformed"
                ;;
            app_con|app_procserv|app_conserver|app_epics)
                [[ "${line}" == "${key} schema=1 repo="*" commit="*" state="*" tag="*" recorded_at="* ]] \
                    || die "application record is malformed at line ${line_number}"
                tail_value="${line#* recorded_at=}"
                [[ "${tail_value}" != *[[:space:]]* ]] \
                    || die "application record has extra fields at line ${line_number}"
                ;;
            app_ioc_runner)
                [[ "${line}" == "${key} schema=1 repo="*" commit="*" state="*" tag="*" recorded_at="* ]] \
                    || die "application record is malformed at line ${line_number}"
                tail_value="${line#* recorded_at=}"
                if [[ "${tail_value}" == *[[:space:]]* ]]; then
                    requested_value="${tail_value#* }"
                    [[ "${requested_value}" == requested=?* \
                        && "${requested_value}" != *[[:space:]]* ]] \
                        || die "application record has extra fields at line ${line_number}"
                fi
                ;;
            pip3)
                [[ "${line}" == "pip3 "* ]] \
                    || die "pip record is malformed at line ${line_number}"
                ;;
            *)
                die "unknown manifest record at line ${line_number}: ${key}"
                ;;
        esac
    done < "${MANIFEST}"

    [[ "${schema_count}" == "1" ]] \
        || die "manifest must contain exactly one schema record"
}

trap cleanup EXIT
trap 'exit 1' HUP INT TERM

[[ "${EUID}" == "0" ]] || die "root privileges are required"
[[ "$#" == "3" || "$#" == "4" ]] \
    || die "usage: record-iocrunner-source <app_name> <repo> <checkout> [requested_ref]"

readonly APP_NAME="$1"
readonly REPO_URL="$2"
readonly CHECKOUT="$3"
readonly REQUESTED_REF="${4:-}"

case "${APP_NAME}" in
    app_con|app_procserv|app_conserver|app_epics|app_ioc_runner) ;;
    *) die "unknown application name: ${APP_NAME}" ;;
esac

validate_record_value "repository URL" "${REPO_URL}"
validate_record_value "checkout path" "${CHECKOUT}"

# The requested ref records the caller's version selector beside the resolved
# commit; only the IOC runner carries one.
if [[ "$#" == "4" ]]; then
    [[ "${APP_NAME}" == "app_ioc_runner" ]] \
        || die "requested ref is only valid for app_ioc_runner: ${APP_NAME}"
    validate_record_value "requested ref" "${REQUESTED_REF}"
fi

for command_name in awk chown chmod date git mktemp mv rm sort stat; do
    require_command "${command_name}"
done

if [[ ! -e "${MANIFEST}" && ! -L "${MANIFEST}" ]]; then
    exit 0
fi

validate_parent "${MANIFEST%/*}"
validate_manifest

[[ -d "${CHECKOUT}/.git" ]] || die "checkout is not a Git repository: ${CHECKOUT}"

declare -g COMMIT
declare -g TAG="-"
declare -g STATE
declare -g RECORDED_AT
declare -g TARGET_MODE
declare -g DIRTY_OUTPUT

COMMIT="$(/usr/bin/git -C "${CHECKOUT}" rev-parse --verify HEAD)"
[[ "${COMMIT}" =~ ^[0-9a-f]{40}$ ]] || die "checkout HEAD is not a 40-hex commit"

DIRTY_OUTPUT="$(/usr/bin/git -C "${CHECKOUT}" status --porcelain=v1 --untracked-files=normal)"
if [[ -n "${DIRTY_OUTPUT}" ]]; then
    STATE="dirty"
else
    TAG="$(/usr/bin/git -C "${CHECKOUT}" tag --points-at HEAD | /usr/bin/sort | /usr/bin/awk 'NR == 1 {print; exit}')"
    if [[ -n "${TAG}" ]]; then
        STATE="clean-tagged"
    else
        TAG="-"
        STATE="clean-untagged"
    fi
fi

validate_record_value "tag" "${TAG}"
RECORDED_AT="$(/usr/bin/date -u +%FT%TZ)"
TARGET_MODE="$(/usr/bin/stat -Lc '%a' -- "${MANIFEST}")"
TEMP_FILE="$(/usr/bin/mktemp "${MANIFEST%/*}/.iocrunner-bake.manifest.tmp.XXXXXX")"

/usr/bin/awk -v app="${APP_NAME}" '$1 != app {print}' "${MANIFEST}" > "${TEMP_FILE}"
printf "%s schema=1 repo=%s commit=%s state=%s tag=%s recorded_at=%s" \
    "${APP_NAME}" "${REPO_URL}" "${COMMIT}" "${STATE}" "${TAG}" "${RECORDED_AT}" \
    >> "${TEMP_FILE}"
if [[ -n "${REQUESTED_REF}" ]]; then
    printf " requested=%s" "${REQUESTED_REF}" >> "${TEMP_FILE}"
fi
printf "\n" >> "${TEMP_FILE}"

/usr/bin/chown 0:0 "${TEMP_FILE}"
/usr/bin/chmod "${TARGET_MODE}" "${TEMP_FILE}"
/usr/bin/mv -f -- "${TEMP_FILE}" "${MANIFEST}"
TEMP_FILE=""

validate_manifest
