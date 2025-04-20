# Ansible Wrapper for System Metrics Collection and PostgreSQL Installation

This program is designed to collect merics from specified hosts, score them, install PostgreSQL on less-loaded host, and configure it to allow external connections.


## Overview

The playbook performs the following steps:

1. **Collect System Metrics**: Gathers metrics such as I/O wait, disk usage, CPU LA, RAM usage from each host.
2. **Evaluate Scores**: Calculates a final score for each host based on the collected metrics and identifies the host with the lowest score (lower is less loaded).
3. **Install PostgreSQL**: Installs PostgreSQL on the host with the lowest score, using tasks for Debian and RedHat based systems.
4. **Configure PostgreSQL**: Configures PostgreSQL to listen on all IP addresses and allows external connections from all IP, with exception for `student` user, which can be accessible only from other host.

## Requirements

- Python and [Ansible installed](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pipx-install) on the control machine.  
- To use the wrapper, `ansible-runner` package should be installed. 
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To run wrapper, you have to use Python3:
```bash
python3 main.py <hosts>
```

To run the playbook directly, use the following command:
```bash
ansible-playbook -i inventory.example.ini playbook/main.yml
```

Ensure that the inventory file is correctly configured with the target hosts. [Example: inventory.example.ini](inventory.example.ini).

## Roles

The playbook uses the following roles:

- **metrics_collection**: Collects system metrics and calculates a final score for each host.
- **score_evaluation**: Aggregates scores, identifies the host with the lowest score, and sets up a dynamic group for it.
- **postgresql_install**: Installs PostgreSQL on the selected host, with OS-specific tasks (Debian and RedHat supported).
- **postgresql_configure**: Configures PostgreSQL to allow external connections.

## Variables

The playbook uses customizable variables:

- **postgresql_version**: PostgreSQL version to install. Defined in [`playbook/group_vars/all.yml`](playbook/group_vars/all.yml).
- **score_weights**: Weights for the metrics in the score calculation, defined in [`playbook/roles/metrics_collection/defaults/main.yml`](playbook/roles/metrics_collection/defaults/main.yml). Sample metrics are weighted based on their impact on database performance, with higher weights indicating greater importance:
    1. IO wait (weight: 6, because disk I/O is crucial for PostgreSQL performance)
    2. Free disk space with threshold (weight: 3, as sufficient disk space is essential)
    3. Load average (weight: 1, since CPU load is less critical for the database)
    4. RAM (weight: 1, as free memory is less significant for the database)

- **disk_threshold_gb**: The disk space threshold in GB for score calculation (to ensure that free space is not the primary metric for evaluation when 500 GB are available). Defined in [`playbook/roles/metrics_collection/defaults/main.yml`](playbook/roles/metrics_collection/defaults/main.yml).

## Output

The playbook provides the following output:

- System metrics for each host, including average wait avergae, load average, free disk space, used RAM, and total score.
- Installation result of PostgreSQL and a inventory name of installation host.

## Notes

- The playbook is designed for Debian (tested on Ubuntu Oracular) and RedHat (tested on CentOS 9 and AlmaLinux 9) based systems. 
- The playbook is tested to work with two hosts but should also be functional with any number of hosts.