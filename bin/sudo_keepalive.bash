#!/usr/bin/env bash
#
# Run a command with a live sudo credential for ansible-provision.
# Refreshes the sudo timestamp in the background so a long local-connection
# apply never triggers a mid-run sudo re-prompt. Password-required sudo is
# preserved; the operator authenticates once. This avoids the ansible-core
# local-connection become-prompt race recorded in docs/CLOSED_DOORS.md
# (2026-09-07): with the timestamp kept valid, sudo never prompts, so
# --ask-become-pass is unnecessary and the fragile prompt handshake is never
# entered.
#
# Usage: bin/sudo_keepalive.bash <command> [args...]
#   e.g. bin/sudo_keepalive.bash make iocserver.rocky8 RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
# Run in the SAME terminal as the command; the sudo timestamp is tty-scoped.

set -e

declare -g KEEPALIVE_PID

if [[ "$#" -eq 0 ]]; then
    printf "Usage: %s <command> [args...]\n" "$0"
    exit 2
fi

printf "%s\n" "------------------------------------------------------------"
printf "sudo keepalive: authenticating once, then refreshing every 60s\n"
printf "%s\n" "------------------------------------------------------------"

# Establish the tty sudo timestamp up front (the only password prompt).
sudo -v

# Refresh it in the background so it never ages out during the run.
( while true; do sudo -n -v 2>/dev/null || exit; sleep 60; done ) &
KEEPALIVE_PID=$!
trap 'kill "${KEEPALIVE_PID}" 2>/dev/null || true' EXIT

# Run the requested command under the live credential.
"$@"
