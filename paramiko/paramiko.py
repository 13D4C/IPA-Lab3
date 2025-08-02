import paramiko
import time
import os
import re

DEVICES_IPS = ['172.31.10.1', '172.31.10.2', '172.31.10.3', '172.31.10.4', '172.31.10.5']
USERNAME = "d4c"
ENABLE_PASSWORD = "d4c" 

PRIVATE_KEY_FILE = os.path.join(os.path.expanduser('~'), '.ssh', 'id_rsa')

for ip in DEVICES_IPS:
    print("-" * 50)
    print(f"==> Connecting to device: {ip}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=ip,
            username=USERNAME,
            key_filename=PRIVATE_KEY_FILE,
            look_for_keys=False,
            timeout=10
        )
        print(f"SUCCESS: Connected to {ip} via SSH.")

        with client.invoke_shell() as ssh:
            time.sleep(1)
            ssh.recv(65535)

            ssh.send("terminal length 0\n")
            time.sleep(1)
            ssh.recv(65535)

            ssh.send("enable\n")
            time.sleep(1)
            ssh.recv(65535)
            ssh.send(f"{ENABLE_PASSWORD}\n")
            time.sleep(1)
            ssh.recv(65535)
            
            print(f"\t-> Fetching full configuration from {ip}...")
            ssh.send("show running-config\n")
            time.sleep(8) 

            # รับข้อมูลทั้งหมด
            full_config = ssh.recv(65535).decode("utf-8")

            hostname_match = re.search(r"hostname\s+(\S+)", full_config)
            
            if hostname_match:
                hostname = hostname_match.group(1)
                filename = f"{hostname}_running-config.txt"
            else:
                hostname = ip
                filename = f"{ip}_running-config.txt"
            
            with open(filename, "w") as file:
                file.write(full_config)
            
            print(f"\tSUCCESS: Configuration saved to '{filename}'")

    except Exception as e:
        print(f"!!! ERROR: An error occurred with device {ip}. Reason: {e}")

    finally:
        if client.get_transport() and client.get_transport().is_active():
            client.close()
            print(f"<== Connection to {ip} closed.")

print("-" * 50)
print("Script finished successfully.")