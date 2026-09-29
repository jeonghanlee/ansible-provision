#!/bin/bash
# Load-test step 2: start the second load IOC, then register its PVs.
set -e
D=/usr/local/share/aasoak9
O=/var/tmp/aasoak9
B=/opt/epics/1.3.0/rocky-8.10/7.0.10/base/bin/linux-x86_64
date -u +%FT%TZ > "$O/step2-started.txt"
systemd-run --unit=aasoak9-load2 "$B/softIoc" -S -d "$D/load2.db"
sleep 20
/usr/bin/python3 "$D/register.py" "$D/pvs-load2.csv" "$O" registered-load2.csv
