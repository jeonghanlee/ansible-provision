# Ansible Command Reference

`inventory/lab.ini` contains group relationships only. Set
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
ansible all -i inventory/lab.ini -i "$RUNTIME_INVENTORY" -m raw -a "uptime"

# Verify connectivity to a single group
ansible rocky8 -i inventory/lab.ini -i "$RUNTIME_INVENTORY" -m raw -a "uptime"
```

---

## ansible-playbook

```bash
# Run a species assembly
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/species/bare.yml
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/species/iocrunner.yml

# Run one operator playbook
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/operators/common.yml
```

```bash
# Limit to a vacuum
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/species/iocrunner.yml --limit rocky8

# Limit to a single VM
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/species/iocrunner.yml --limit "$TARGET_HOST"

# Run a specific role via tag
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/species/iocrunner.yml --tags epics

# Dry run: validates inventory, reachability, and template rendering only.
# Raw tasks are skipped in check mode, so this is not a change preview.
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/species/iocrunner.yml -C

# Verbose output
ansible-playbook -i inventory/lab.ini -i "$RUNTIME_INVENTORY" playbooks/species/iocrunner.yml -v
```

---

## Ad-hoc Commands

```bash
# Run a command on all nodes without requiring managed-host Python
ansible all -i inventory/lab.ini -i "$RUNTIME_INVENTORY" -m raw -a "uptime"

# Check a service status
ansible rocky8 -i inventory/lab.ini -i "$RUNTIME_INVENTORY" -m raw -a "systemctl is-active chronyd"

# Check OS release data without gathering facts
ansible "$TARGET_HOST" -i inventory/lab.ini -i "$RUNTIME_INVENTORY" -m raw -a "cat /etc/os-release"

# Check a binary exists
ansible all -i inventory/lab.ini -i "$RUNTIME_INVENTORY" -m raw -a "command -v procServ"
```

---

## Inventory Inspection

```bash
# List all hosts in inventory
ansible-inventory -i inventory/lab.ini -i "$RUNTIME_INVENTORY" --list

# List hosts in a specific group
ansible-inventory -i inventory/lab.ini -i "$RUNTIME_INVENTORY" --graph

# Show variables for a host
ansible-inventory -i inventory/lab.ini -i "$RUNTIME_INVENTORY" --host "$TARGET_HOST"
```

---

## Makefile Wrappers

```bash
make ping RUNTIME_INVENTORY="$RUNTIME_INVENTORY"

make bare.rocky8 RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
make iocrunner.debian13 RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
make epics_dev.ubuntu24 RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_LIMIT="$TARGET_HOST"
make bare.rocky8.check RUNTIME_INVENTORY="$RUNTIME_INVENTORY"
make op.nfs_sim.rocky8 RUNTIME_INVENTORY="$RUNTIME_INVENTORY"

make vars                              # print active configuration
make PRINT.INVENTORY                   # print a specific variable
```

```bash
# Pass extra options via environment variables
make bare.rocky8 RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_OPTS=-v
make iocrunner RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_TAGS=con
make iocrunner.debian13 RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_LIMIT="$TARGET_HOST"
```

```bash
# Host without passwordless sudo: ansible.cfg keeps become_ask_pass off, so a
# cold sudo timestamp stalls the first become task on the local connection.
# Pass --ask-become-pass to prompt once for the sudo password at the start.
# Keep every option inside one ANSIBLE_OPTS value; a second assignment replaces it.
make iocserver.rocky8 RUNTIME_INVENTORY="$RUNTIME_INVENTORY" ANSIBLE_OPTS="--ask-become-pass"
```
