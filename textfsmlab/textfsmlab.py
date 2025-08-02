from netmiko import ConnectHandler

USERNAME = "d4c"
PASSWORD = "d4c"
ENABLE_SECRET = "d4c"

R1_DEVICE = {
    'device_type': 'cisco_ios',
    'ip': '172.31.10.4',
    'username': USERNAME,
    'password': PASSWORD,
    'secret': ENABLE_SECRET,
}

R2_DEVICE = {
    'device_type': 'cisco_ios',
    'ip': '172.31.10.5',
    'username': USERNAME,
    'password': PASSWORD,
    'secret': ENABLE_SECRET,
}

devices_to_update = [R1_DEVICE, R2_DEVICE]

for device in devices_to_update:
    print("-" * 50)
    print(f"==> Auto-configuring descriptions for: {device['ip']}")

    try:
        with ConnectHandler(**device) as net_connect:
            print(f"\t-> Connected to {device['ip']}.")

            print("\t-> Fetching CDP neighbor information...")
            cdp_neighbors = net_connect.send_command('show cdp neighbors', use_textfsm=True)
            print(f"\t-> Found {len(cdp_neighbors)} neighbors.")

            config_commands = []
            if cdp_neighbors:
                for neighbor in cdp_neighbors:
                    local_int = neighbor['local_interface']
                    remote_host = neighbor['neighbor'].split('.')[0]
                    remote_int = neighbor['neighbor_interface']
                    
                    description = f"Connect to {remote_int} of {remote_host}"
                    
                    config_commands.append(f"interface {local_int}")
                    config_commands.append(f"description {description}")

            if config_commands:
                print("\t-> Deploying generated interface descriptions...")
                output = net_connect.send_config_set(config_commands)
                print("\n--- Deployment Output ---")
                print(output)
                print("-------------------------\n")

                save_output = net_connect.save_config()
                print(f"\t-> {save_output}")
            else:
                print("\t-> No neighbors found or no configs to deploy.")

    except Exception as e:
        print(f"!!! ERROR: Failed on {device['ip']}. Reason: {e}")

print("-" * 50)
print("Script finished.")