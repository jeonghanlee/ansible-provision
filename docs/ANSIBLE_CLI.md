# Ansible Command Reference

`inventory/testbed.ini` contains group relationships only. Set
`RUNTIME_INVENTORY` to a host inventory produced by
`cloud-provision/bin/generate_ansible_inventory.bash`; set `TARGET_HOST` to
the generated VM name when selecting one host.

```bash
export RUNTIME_INVENTORY=/tmp/cloud-provision-host.ini
export TARGET_HOST=actual-vm-name
```

## Connectivity

```bash
# Verify connectivity to all nodes (raw module, no Python dependency)
ansible all -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" -m raw -a "uptime"

# Verify connectivity to a single group
ansible rocky8 -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" -m raw -a "uptime"
```

---

## ansible-playbook

```bash
# Run full stack
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" site.yml

# Run a specific playbook
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" playbooks/01_base.yml
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" playbooks/02_apps.yml
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" playbooks/03_epics.yml
```

```bash
# Limit to an OS group
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" site.yml --limit rocky8

# Limit to a single VM
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" site.yml --limit "$TARGET_HOST"

# Run a specific role via tag
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" site.yml --tags epics

# Dry run (no changes applied)
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" site.yml -C

# Verbose output
ansible-playbook -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" site.yml -v
```

---

## Ad-hoc Commands

```bash
# Run a command on all nodes without requiring managed-host Python
ansible all -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" -m raw -a "uptime"

# Check a service status
ansible rocky8 -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" -m raw -a "systemctl is-active chronyd"

# Check OS release data without gathering facts
ansible "$TARGET_HOST" -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" -m raw -a "cat /etc/os-release"

# Check a binary exists
ansible all -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" -m raw -a "command -v procServ"
```

---

## Inventory Inspection

```bash
# List all hosts in inventory
ansible-inventory -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" --list

# List hosts in a specific group
ansible-inventory -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" --graph

# Show variables for a host
ansible-inventory -i inventory/testbed.ini -i "$RUNTIME_INVENTORY" --host "$TARGET_HOST"
```

---

## Makefile Wrappers

```bash
make ping RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
make all RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
make check RUNTIME_INVENTORY="$RUNTIME_INVENTORY"

make 01_base RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
make 01_base.rocky8 RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
make 01_base.rocky8.server RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_LIMIT="$TARGET_HOST"
make 01_base.rocky8.server.check RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_LIMIT="$TARGET_HOST"
make 04_nfs_sim RUNTIME_INVENTORY="$RUNTIME_INVENTORY"

make vars                              # print active configuration
make PRINT.INVENTORY                   # print a specific variable
```

```bash
# Pass extra options via environment variables
make 01_base RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_OPTS=-v
make 02_apps RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_TAGS=con
make 03_epics RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_LIMIT=rocky8
```
