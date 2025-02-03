#!/usr/bin/python3
# pip3 install -r requirements.txt
# passing the host Ips in the given list

import configparser
import os
import re

import paramiko
import requests
from pynetbox import api

###########################################################
config = configparser.ConfigParser()
config.read('../config.cnf')


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
    description = []

    for ip_address in ip_addresses:
        custom_fields_priority = ip_address.custom_fields['Priority']
        custom_fields_environment = ip_address.custom_fields['Environment']
        custom_fields_resource_types = ip_address.custom_fields['Resource_Types']
        hosts.append(str(ip_address.address)[:-3])
        priority.append(custom_fields_priority)
        environment.append(custom_fields_environment)
        resource_type.append(custom_fields_resource_types)
        description.append(str(ip_address.description))

    return hosts, priority, environment, resource_type, description


def get_inventory_info(pass_exception):
    # command_cpu = "lscpu |grep 'CPU(s):' | head -1 |awk '{print $2}'"
    # command_ram = "free -m | grep 'Mem:' | awk '{print $2}'"
    # command_disks = "df -h | grep '^/dev/' | grep -v 'snap' | grep -v '/boot' | awk '{print $2, $6}'"
    # uname = "lsb_release -d | sed -e 's/Description:[[:space:]]*//' -e 's/ ([^)]*)//; s/ GNU\/Linux//; s/ (.*$)//; s/ " "LTS//'"
    command_keys = "ls /root/.ssh/ | grep keys"
    output = []
    #port = 22
    username = "root"


    for i in range(len(hosts)):
        if priority[i] == 'Ignore':
            continue
        if resource_type[i] != 'VM':
            continue


        # if hosts[i] in pass_exception:
        #     password = pass_exception[hosts[i]]
        # else:
        #     password = config.get('root', 'ssh_password').strip()
        #
        # temp_output = []
        # print("running commands now for IP :" + hosts[i])
        # ssh = create_ssh_session(hostname=hosts[i],username=username,password=password,private_key=key)
        if hosts[i] in pass_exception:
            # print("yes")
            password = pass_exception[hosts[i]]['password']
            ssh_port = pass_exception[hosts[i]]['port']
            # print(password,port)
        else:
            password = config.get('root', 'ssh_password').strip()
            ssh_port = config.get('root', 'ssh_port').strip()
            # print(port,password)
        temp_output = []
    # password = config.get('root', 'ssh_password').strip()
# ######
#     for i in range(len(hosts)):
#         if priority[i] == 'Ignore':
#             continue
#         if resource_type[i] != 'VM':
#             continue
#
#         if hosts[i] in pass_exception:
#             password = pass_exception[hosts[i]]
#         else:
#             password = config.get('root', 'ssh_password').strip()
#
#         temp_output = []
# ######
        print("running commands now for IP :" + hosts[i])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(password)
        ssh.connect(hosts[i], ssh_port, username, password)
        temp_output.append(hosts[i])
        stdin, stdout, stderr = ssh.exec_command(command_keys)
        authorized_files = stdout.readlines()
        authorized_files = [file.strip() for file in authorized_files]
        temp_output.append(authorized_files)
        output.append(temp_output)
    print(output)

    return output


def customised_credentials_ssh():
    pass_exception = {}
    with open("../customCredentials/customized_credentials_ssh.txt", "r") as lines:
        next(lines)
        for line in lines:
            if not line or line.startswith('#'):
                continue
            items = line.strip().split()
            # print(len(items))
            if len(items) == 3:
                key, value, port = items
                pass_exception[key] = {'password': value, 'port': int(port)}

            else:
                key, value = items
                pass_exception[key] = {'password': value, 'port': 22}



    # print(pass_exception)
    return pass_exception

def ska_ips():
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ska_ips = []
    with open("../ska_ips.txt", "r") as lines:
        for line in lines:

            if not line or line.startswith('#') or not ip_pattern.match(line):
                continue
            # if not ip_pattern.match(line):
            #     print(f"Skipping non-IP value: {line}")
            #     continue

            ska_ips.append(line.strip())
    return ska_ips

def create_inventory_file(output):
    headers = "IP\t\t\t\t\t\t\t\tKey Files\n"
    print("writting output to the inventory.txt file ...")
    with open('keys_inventory.txt', 'w') as file:
        file.write(headers)
        for output in output:
            print(output)
            for output in output:
                output = output.__str__().replace('[\'', '').replace('\']', '').replace("'", "") + '\t \t'
                file.write(output)
            file.write('\n')
        file.close()


if __name__ == '__main__':
    password_exception = customised_credentials_ssh()
    ska_ip= ska_ips()

    hosts, priority, environment, resource_type, description = get_netbox_data()

    output_from_inventory = get_inventory_info(password_exception)
    create_inventory_file(output_from_inventory)
