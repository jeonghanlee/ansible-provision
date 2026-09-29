#!/bin/bash
# Record the host journald facts once, at soak start and at soak end.
# Usage: journald_facts.sh <out_file>
out="$1"
{
  printf 'ts: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'systemd: %s\n' "$(systemctl --version | head -n 1)"
  if [ -d /var/log/journal ]; then
    printf 'persistent_dir: present\n'
  else
    printf 'persistent_dir: absent\n'
  fi
  printf 'disk_usage: %s\n' "$(journalctl --disk-usage 2>/dev/null)"
  printf -- '--- journald.conf with drop-ins ---\n'
  if systemd-analyze cat-config systemd/journald.conf >/dev/null 2>&1; then
    systemd-analyze cat-config systemd/journald.conf
  else
    cat /etc/systemd/journald.conf /etc/systemd/journald.conf.d/*.conf 2>/dev/null
  fi
  printf -- '--- keys set explicitly (unset keys take the systemd defaults) ---\n'
  grep -hE '^[[:space:]]*(Storage|SystemMaxUse|SystemKeepFree|SystemMaxFileSize|MaxRetentionSec|RateLimitIntervalSec|RateLimitInterval|RateLimitBurst)=' \
    /etc/systemd/journald.conf /etc/systemd/journald.conf.d/*.conf 2>/dev/null || printf 'none\n'
} > "${out}"
