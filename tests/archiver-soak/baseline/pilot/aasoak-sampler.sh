#!/bin/bash
# Periodic soak metrics for the archiver endurance run. One CSV row per interval.
CSV=/var/tmp/aasoak-metrics.csv
INTERVAL=900
M=http://localhost:17665/mgmt/bpl
PVS="AASOAK:PLAIN AASOAK:ONE_UNDER AASOAK:TWO_UNDER_SCORE AASOAK:DASH-NAME AASOAK:TRAIL9 AASOAK:NUM_12_34 AASOAK:A_VERY_LONG_NAME_WITH_MANY_UNDERSCORES_HERE AASOAK:MIX_1-2 AASOAK:UPPER_lower AASOAK:SUB:NESTED AASOAK:PFX_A:PFX_B:LEAF"

if [ ! -f "$CSV" ]; then
  echo "iso_utc,epoch,sts_bytes,mts_bytes,lts_bytes,sts_files,mts_files,lts_files,pvs_with_mts,pvs_with_lts,instances,unit,mgmt_code,mgmt_seconds,java_rss_mb,journal_bytes,kernel_oom,load1" > "$CSV"
fi

while true; do
  now_i=$(date -u +%Y-%m-%dT%H:%M:%SZ); now_e=$(date +%s)
  stsb=$(du -sb /arch/sts 2>/dev/null | cut -f1); mtsb=$(du -sb /arch/mts 2>/dev/null | cut -f1); ltsb=$(du -sb /arch/lts 2>/dev/null | cut -f1)
  stsf=$(find /arch/sts -type f -name "*.pb" 2>/dev/null | wc -l)
  mtsf=$(find /arch/mts -type f -name "*.pb" 2>/dev/null | wc -l)
  ltsf=$(find /arch/lts -type f -name "*.pb" 2>/dev/null | wc -l)
  pm=0; pl=0
  for p in $PVS; do
    d=$(printf %s "$p" | tr ":_-" "/")
    [ -n "$(find /arch/mts -path "*${d}*" -name "*.pb" 2>/dev/null | head -1)" ] && pm=$((pm+1))
    [ -n "$(find /arch/lts -path "*${d}*" -name "*.pb" 2>/dev/null | head -1)" ] && pl=$((pl+1))
  done
  inst=$(ps -o args= -C java | grep -c catalina.base)
  unit=$(systemctl is-active epicsarchiverap-maven.service)
  mc=$(curl -s -o /dev/null -w "%{http_code}" --noproxy "*" --max-time 10 "$M/getApplianceInfo")
  ms=$(curl -s -o /dev/null -w "%{time_total}" --noproxy "*" --max-time 10 "$M/getApplianceInfo")
  rss=$(ps -o rss= -C java | awk "{s+=\$1} END {print int(s/1024)}")
  jb=$(journalctl --disk-usage 2>/dev/null | grep -oE "[0-9.]+[KMG]" | head -1)
  oom=$(journalctl -k --no-pager 2>/dev/null | grep -ci "Out of memory: Killed")
  l1=$(cut -d" " -f1 /proc/loadavg)
  echo "$now_i,$now_e,$stsb,$mtsb,$ltsb,$stsf,$mtsf,$ltsf,$pm,$pl,$inst,$unit,$mc,$ms,$rss,$jb,$oom,$l1" >> "$CSV"
  sleep "$INTERVAL"
done
