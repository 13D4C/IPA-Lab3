from netmiko import ConnectHandler
import re

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

routers_to_check = [R1_DEVICE, R2_DEVICE]

INTERFACE_PATTERN = re.compile(
    r'^(?P<interface>\S+)\s+.*\s+'
    r'(?P<status>up|down|administratively down)\s+'
    r'(?P<protocol>up|down)$'
)

for device in routers_to_check:
    print("-" * 50)
    print(f"==> Checking active interfaces on: {device['ip']}")
    
    try:
        with ConnectHandler(**device) as net_connect:
            print(f"\t-> Connected to {device['ip']}.")
            
            output = net_connect.send_command('show ip interface brief')
            
            print(f"\t-> Found active interfaces:")
            
            found_active_interface = False
            for line in output.splitlines():
                match = INTERFACE_PATTERN.search(line.strip())
                
                if match:
                    interface_name = match.group('interface')
                    status = match.group('status')
                    protocol = match.group('protocol')
                    
                    if status == 'up' and protocol == 'up':
                        print(f"\t  - Interface: {interface_name:<25} | Status: {status}, Protocol: {protocol}")
                        found_active_interface = True

            if not found_active_interface:
                print("\t  - No active interfaces found.")

    except Exception as e:
        print(f"!!! ERROR: Failed on {device['ip']}. Reason: {e}")

print("-" * 50)
print("Script finished.")