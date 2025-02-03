import paramiko
from paramiko.ssh_exception import SSHException
import configparser
import os
import requests
from pynetbox import api

config = configparser.ConfigParser()
config.read('config.cnf')
directory = config.get('output_cfg_files', 'path').strip()
os.makedirs(directory, exist_ok=True)



def get_netbox_data():
    url = config.get('netbox', 'netboxUrl').strip()
    token = config.get('netbox', 'netboxApiToken').strip()
    session = requests.Session()
    session.verify = False
    nb = api(url, token=token)
    nb.http_session = session
    ip_addresses = nb.ipam.ip_addresses.all()
    hosts = []
    priority = []
    environment = []
    resource_type = []

    for ip_address in ip_addresses:
        custom_fields_priority = ip_address.custom_fields['Priority']
        custom_fields_environment = ip_address.custom_fields['Environment']
        custom_fields_resource_types = ip_address.custom_fields['Resource_Types']
        hosts.append(str(ip_address.address)[:-3])
        priority.append(custom_fields_priority)
        environment.append(custom_fields_environment)
        resource_type.append(custom_fields_resource_types)

    return hosts, priority, environment, resource_type

def check_ssh_access(ip):
    try:
        username = "root"
        password = config.get('root', 'ssh_password').strip()
        if ip in pass_exception:
            password = pass_exception[ip]
        else:
            password = config.get('root', 'ssh_password').strip()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, 'root', password ,timeout=3)
        ssh.close()
        return True
    except SSHException:
        return False


def create_hosts_file(output):
    with open('hosts_not_accessible.txt', 'w') as file:
        # file.write(headers)
        for i in output:
            file.write(i)
            file.write('\n')
        file.close()


inventory = {}
output=[]
hosts, priority, environment, resource_type = get_netbox_data()
pass_exception = {}
with open("../passwordException.txt", "r") as lines:
    next(lines)
    for line in lines:
        if not line or line.startswith('#'):
            continue
        key, value = line.strip().split()
        pass_exception[key] = value
print(pass_exception)
# print((hosts))
#
for ip in hosts:
    try:
        success = check_ssh_access(ip)
        inventory[ip] = 'yes' if success else 'no'
        # if success =='no':
        #     output.append(ip)
        #     print(ip)
    except:
        print(ip + " not accessible probably windows machine")

for ip, access in inventory.items():
    if access =='yes':
        continue

    print(f'IP: {ip}, SSH Access: {access}')
    output.append(ip)




create_hosts_file(output)
print(output)