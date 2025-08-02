from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

USERNAME = "d4c"
PASSWORD = "d4c"
ENABLE_SECRET = "d4c"

R1_DATA = {
    'connection': {
        'device_type': 'cisco_ios',
        'ip': '172.31.10.4',
        'username': USERNAME,
        'password': PASSWORD,
        'secret': ENABLE_SECRET,
    },
    'device_name': 'R1',
    'ospf': {
        'router_id': '1.1.1.1',
        'area': 0,
        'networks': [
            {'ip': '192.168.10.0', 'wildcard': '0.0.0.255'},
            {'ip': '1.1.1.1', 'wildcard': '0.0.0.0'},
        ],
        'is_default_originate': False
    }
}

R2_DATA = {
    'connection': {
        'device_type': 'cisco_ios',
        'ip': '172.31.10.5',
        'username': USERNAME,
        'password': PASSWORD,
        'secret': ENABLE_SECRET,
    },
    'device_name': 'R2',
    'ospf': {
        'router_id': '2.2.2.2',
        'area': 0,
        'networks': [
            {'ip': '192.168.20.0', 'wildcard': '0.0.0.255'},
            {'ip': '2.2.2.2', 'wildcard': '0.0.0.0'},
        ],
        'is_default_originate': True
    }
}

routers_to_configure = [R1_DATA, R2_DATA]

env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('ospf_config.j2')

for router_data in routers_to_configure:
    print("-" * 50)
    print(f"==> Generating and deploying config for: {router_data['device_name']}")

    try:
        config_to_deploy = template.render(router_data)
        
        print("\n--- Generated Configuration ---")
        print(config_to_deploy)
        print("-----------------------------\n")
        
        with ConnectHandler(**router_data['connection']) as net_connect:
            print(f"\t-> Connected to {router_data['connection']['ip']}")
            
            config_lines = config_to_deploy.splitlines()
            output = net_connect.send_config_set(config_lines)

            print("\n--- Deployment Output ---")
            print(output)
            print("-------------------------\n")
            
            save_output = net_connect.save_config()
            print(f"\t-> {save_output}")

    except Exception as e:
        print(f"!!! ERROR: Failed on {router_data['device_name']}. Reason: {e}")

print("-" * 50)
print("Script finished.")