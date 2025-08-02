from netmiko import ConnectHandler

USERNAME = "d4c"
PASSWORD = "d4c"
ENABLE_SECRET = "d4c"

S1_DEVICE = {
    'device_type': 'cisco_ios',
    'ip': '172.31.10.3',
    'username': USERNAME,
    'password': PASSWORD,
    'secret': ENABLE_SECRET,
    'config_commands': [
        'vlan 101',
        'name Control-Data-Plane'
    ]
}

R1_DEVICE = {
    'device_type': 'cisco_ios',
    'ip': '172.31.10.4',
    'username': USERNAME,
    'password': PASSWORD,
    'secret': ENABLE_SECRET,
    'config_commands': [
        'router ospf 1',
        'network 192.168.10.0 0.0.0.255 area 0',
        'network 1.1.1.1 0.0.0.0 area 0',
    ]
}

R2_DEVICE = {
    'device_type': 'cisco_ios',
    'ip': '172.31.10.5',
    'username': USERNAME,
    'password': PASSWORD,
    'secret': ENABLE_SECRET,
    'config_commands': [
        'interface GigabitEthernet0/1',
        'ip nat outside',
        'interface GigabitEthernet0/2',
        'ip nat inside',
        'access-list 1 permit any',
        'ip nat inside source list 1 interface GigabitEthernet0/1 overload',
        'exit',
        'router ospf 1',
        'network 192.168.20.0 0.0.0.255 area 0',
        'network 2.2.2.2 0.0.0.0 area 0',
        'default-information originate',
    ]
}

devices_to_configure = [S1_DEVICE, R1_DEVICE, R2_DEVICE]

for device in devices_to_configure:
    print("-" * 50)
    print(f"==> Configuring device: {device['ip']}")
    
    config_commands = device.get('config_commands', [])
    
    if not config_commands:
        print(f"\tINFO: No configuration commands for {device['ip']}. Skipping.")
        continue

    try:
        with ConnectHandler(**device) as net_connect:
            print(f"\tSUCCESS: Connected. Current prompt: {net_connect.find_prompt()}")

            print(f"\t-> Sending {len(config_commands)} configuration commands...")
            output = net_connect.send_config_set(config_commands)
            
            print("\n" + output + "\n")

            print("\t-> Saving configuration...")
            save_output = net_connect.save_config()
            print(f"\t{save_output}")

    except Exception as e:
        print(f"!!! ERROR: Failed to configure {device['ip']}. Reason: {e}")

print("-" * 50)
print("Script finished.")