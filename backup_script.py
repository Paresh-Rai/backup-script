Pythmport csv
import os
from netmiko import ConnectHandler

csv_file = "/home/jonsnow/devices.csv"
backup_folder = "/home/jonsnow/backups"

os.makedirs(backup_folder, exist_ok=True)

username = os.getenv("SSH_USER")

with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        device_name = row["name"]
        device_ip = row["ip"]

        device = {
            "device_type": "cisco_ios",
            "host": device_ip,
            "username": username,
            "use_keys": True,
            "key_file": "/home/jonsnow/.ssh/id_rsa",
            "passphrase": None,
            "disabled_algorithms": {
                "pubkeys": ["rsa-sha2-512", "rsa-sha2-256"]
            }
        }

        print(f"Connecting to {device_name} ({device_ip})...")

        net_connect = ConnectHandler(**device)
        output = net_connect.send_command("show running-config")

        filename = os.path.join(backup_folder, f"{device_name}_backup.txt")
        with open(filename, "w") as backup_file:
            backup_file.write(output)

        print(f"Backup saved to {filename}")
        net_connect.disconnect()
