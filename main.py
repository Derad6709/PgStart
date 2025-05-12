import argparse
import ansible_runner
import os


def create_inventory(host_list):
    """Create inventory dictionary for Ansible."""
    inventory = {
        'all': {
            'children': {
                'myhosts': {
                    'hosts': {host: {'ansible_connection': 'ssh'} for host in host_list}
                }
            }
        }
    }
    return inventory


def run_playbook(inventory):
    """Run the Ansible playbook using ansible-runner."""
    runner = ansible_runner.run(
        playbook=f'{os.getcwd()}/playbook/main.yml',
        inventory=inventory,
        quiet=False
    )

    if runner.status == 'successful':
        print("Playbook executed successfully.")
    else:
        print(f"Playbook execution failed with status: {runner.status}")
        print(f"Events: {runner.events}")
        raise RuntimeError("Playbook execution failed.")


def main():
    """Main function to parse arguments and run the playbook."""
    parser = argparse.ArgumentParser(
        description='Run Ansible playbook with provided IPs or domain names using ansible-runner.')
    parser.add_argument(
        'hosts', help='Comma-separated list of IP addresses or domain names')
    args = parser.parse_args()

    try:
        host_list = args.hosts.split(',')
        inventory = create_inventory(host_list)
        run_playbook(inventory)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
