#!/usr/bin/env bash
#
# Host environment setup for ansible-provision.
# Verifies and installs ansible-core required to run the playbooks.

set -e

declare -g OS_ID

if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS_ID="${ID}"
fi

printf "%s\n" "------------------------------------------------------------"
printf "Host Environment Setup (%s)\n" "${OS_ID:-unknown}"
printf "%s\n" "------------------------------------------------------------"

if [[ "${OS_ID}" == "rocky" ]]; then
    PKG_CMD="dnf"
elif [[ "${OS_ID}" == "debian" ]]; then
    PKG_CMD="apt"
else
    printf "Error: Unsupported host OS: %s\n" "${OS_ID:-unknown}"
    exit 1
fi

if command -v ansible-playbook >/dev/null 2>&1; then
    printf "  ansible-playbook [OK]\n"
else
    printf "  ansible-playbook [MISSING]\n"
    printf "Installing ansible-core...\n"
    if [[ "${OS_ID}" == "debian" ]]; then
        sudo "${PKG_CMD}" update
    fi
    sudo "${PKG_CMD}" install -y ansible-core
fi

printf "%s\n" "------------------------------------------------------------"
printf "Host setup complete.\n"
printf "%s\n" "------------------------------------------------------------"
