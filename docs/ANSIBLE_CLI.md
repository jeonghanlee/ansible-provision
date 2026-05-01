# Ansible Command Reference

## Connectivity

```bash
# Verify connectivity to all nodes (raw module, no Python dependency)
ansible all -i inventory/testbed.ini -m raw -a "uptime"

# Verify connectivity to a single group
ansible rocky8 -i inventory/testbed.ini -m raw -a "uptime"
```

---

## ansible-playbook

```bash
# Run full stack
ansible-playbook -i inventory/testbed.ini site.yml

# Run a specific playbook
ansible-playbook -i inventory/testbed.ini playbooks/01_base.yml
ansible-playbook -i inventory/testbed.ini playbooks/02_apps.yml
ansible-playbook -i inventory/testbed.ini playbooks/03_epics.yml
```

```bash
# Limit to an OS group
ansible-playbook -i inventory/testbed.ini site.yml --limit rocky8

# Limit to a single VM
ansible-playbook -i inventory/testbed.ini site.yml --limit testbed-rocky8-server

# Run a specific role via tag
ansible-playbook -i inventory/testbed.ini site.yml --tags epics

# Dry run (no changes applied)
ansible-playbook -i inventory/testbed.ini site.yml -C

# Verbose output
ansible-playbook -i inventory/testbed.ini site.yml -v
```

---

## Ad-hoc Commands

```bash
# Run a shell command on all nodes
ansible all -i inventory/testbed.ini -m shell -a "uptime"

# Check a service status
ansible rocky8 -i inventory/testbed.ini -m shell -a "systemctl is-active chronyd"

# Gather facts from a single node
ansible testbed-rocky8-server -i inventory/testbed.ini -m setup

# Check a binary exists
ansible all -i inventory/testbed.ini -m shell -a "which procServ"
```

---

## Inventory Inspection

```bash
# List all hosts in inventory
ansible-inventory -i inventory/testbed.ini --list

# List hosts in a specific group
ansible-inventory -i inventory/testbed.ini --graph

# Show variables for a host
ansible-inventory -i inventory/testbed.ini --host testbed-rocky8-server
```

---

## Makefile Wrappers

```bash
make ping                              # ansible all -m raw -a "uptime"
make all                               # site.yml on all nodes
make check                             # site.yml dry run

make 01_base                           # 01_base.yml on all nodes
make 01_base.rocky8                    # limit to rocky8 group
make 01_base.rocky8.server             # limit to single VM
make 01_base.rocky8.server.check       # dry run on single VM
make 04_nfs_sim                        # 04_nfs_sim.yml on nfs_sim_nodes (out-of-band)

make vars                              # print active configuration
make PRINT.INVENTORY                   # print a specific variable
```

```bash
# Pass extra options via environment variables
make 01_base ANSIBLE_OPTS=-v
make 02_apps ANSIBLE_TAGS=con
make 03_epics ANSIBLE_LIMIT=rocky8
```
