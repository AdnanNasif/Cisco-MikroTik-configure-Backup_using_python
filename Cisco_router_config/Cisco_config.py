import paramiko
import os
from datetime import datetime

def backup_router_config(hostname, username, password):
    # SSH Connection Parameters
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Cisco router
        ssh_client.connect(hostname, port=22, username=username, password=password, timeout=5)

        # Send command to get configuration
        stdin, stdout, stderr = ssh_client.exec_command('show running-config')

        # Get configuration output
        config_output = stdout.read().decode()

        # Create backup folder if it doesn't exist
        backup_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'backup')
        os.makedirs(backup_folder, exist_ok=True)

        # Generate file name based on date and time
        now = datetime.now()
        file_name = f'{hostname}_config_backup_{now.strftime("%Y-%m-%d_%H-%M-%S")}.txt'

        # Write configuration to file
        with open(os.path.join(backup_folder, file_name), 'w') as f:
            f.write(config_output)

        print(f"Configuration backup successful. Saved as: {file_name}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close SSH connection
        ssh_client.close()

# Provide router details
router_hostname = 'your_router_ip'
router_username = 'your_username'
router_password = 'your_password'

# Call the function to backup router configuration
backup_router_config(router_hostname, router_username, router_password)