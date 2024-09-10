import paramiko
import datetime
import os
import time

def create_backup_folder(save_path):
    folder_name = "router_backup"
    folder_path = os.path.join(save_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def backup_router_config(hostname, username, password, save_path):
    try:
        while True:
            # Connect to the router via SSH
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname, username=username, password=password)

            # Run command to export configuration
            stdin, stdout, stderr = ssh_client.exec_command("/export")

            # Save configuration to a file with timestamp
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"router_config_{hostname}_{now}.txt"
            backup_file_path = os.path.join(save_path, filename)
            with open(backup_file_path, "w") as f:
                f.write(stdout.read().decode())

            print(f"Configuration backup successful: {backup_file_path}")

            # Close SSH connection
            ssh_client.close()

            # Sleep for 10 seconds before the next backup
            time.sleep(10)

    except Exception as e:
        print(f"Error: {e}")

def main():
    # Router details
    hostname = 'ip'
    username = 'python'
    password = 'python@123'

    # Path to save backup files
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    backup_folder_path = create_backup_folder(desktop_path)

    # Call the backup function
    backup_router_config(hostname, username, password, backup_folder_path)

if __name__ == "__main__":
    main()