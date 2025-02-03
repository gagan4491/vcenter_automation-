#!/usr/bin/python3
# pip3 install -r requirements.txt
# passing the host Ips in the given list

import configparser
import os
import paramiko
import requests
from pynetbox import api

###########################################################
config = configparser.ConfigParser()
config.read('config.cnf')
directory = config.get('output_cfg_files', 'path').strip()
os.makedirs(directory, exist_ok=True)


# ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

###########################################################
def pass_exepction():


    with open("../passwordException.txt", "r") as lines:
        next(lines)
        for line in lines:
            key, value = line.strip().split()
            pass_exception[key] = value
    print(pass_exception)
    return pass_exception


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
    description =[]

    for ip_address in ip_addresses:
        custom_fields_priority = ip_address.custom_fields['Priority']
        custom_fields_environment = ip_address.custom_fields['Environment']
        custom_fields_resource_types = ip_address.custom_fields['Resource_Types']
        hosts.append(str(ip_address.address)[:-3])
        priority.append(custom_fields_priority)
        environment.append(custom_fields_environment)
        resource_type.append(custom_fields_resource_types)
        description.append(str(ip_address.description))

    return hosts, priority, environment, resource_type,description


def get_inventory_info():
    command_cpu = "lscpu |grep 'CPU(s):' | head -1 |awk '{print $2}'"
    command_ram = "free -m | grep 'Mem:' | awk '{print $2}'"
    command_disks = "df -h | grep '^/dev/' | grep -v 'snap' | grep -v '/boot' | awk '{print $2, $6}'"
    uname = "lsb_release -d | sed -e 's/Description:[[:space:]]*//' -e 's/ ([^)]*)//; s/ GNU\/Linux//; s/ (.*$)//; s/ " "LTS//'"
    output = []
    port = 22
    username = "root"
    password = config.get('root', 'ssh_password').strip()

    for i in range(len(hosts)):
        if priority[i] == 'Ignore':
            continue
        if resource_type[i] != 'VM':
            continue

        if hosts[i] in pass_exception:
            password = pass_exception[hosts[i]]
        else:
            password = config.get('root', 'ssh_password').strip()


        temp_output = []
        print("running commands now for IP :" + hosts[i])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(password)
        ssh.connect(hosts[i], port, username, password)

        ############
        stdin, stdout, stderr = ssh.exec_command(uname)
        lines = stdout.readlines()
        # print(len(lines[0].replace(" ", "")))
        temp_output.append(lines[0].replace(" ", "").rstrip().ljust(14))
        #########

        temp_output.append(hosts[i])

        #########
        temp_output.append(description[i].rstrip().ljust(30))

        #########

        temp_output.append(priority[i].ljust(14))
        #########

        temp_output.append(environment[i].ljust(18))

        #########

        stdin, stdout, stderr = ssh.exec_command(command_cpu)
        lines = stdout.readlines()
        temp_output.append(lines[0].rstrip())
        #########
        stdin, stdout, stderr = ssh.exec_command(command_ram)
        lines = stdout.readlines()
        temp_output.append(lines[0].rstrip().ljust(6))
        #########

        stdin, stdout, stderr = ssh.exec_command(command_disks)

        lines = stdout.read()
        olines = lines.decode().split('\n')
        li = []

        for l in olines:
            # print(l)
            if l == '':
                continue
            li.append(l.rstrip().replace('G', ''))
        temp_output.append(li)
        #########
        output.append(temp_output)
        ssh.close()
        del ssh, stdin, stdout, stderr
    return output


def create_inventory_file(output):
    headers = "OS-Version\t\t\tIP's\t\t\t\tDescription\t\t\t\t\t\t\tPriorty\t\t\t\tEnvironment\t\t\t\tCPU's\tRAM(MB)\t\tDISKS(GB/TB)\n"
    print("writting output to the inventory.txt file ...")
    with open('inventory.txt', 'w') as file:
        file.write(headers)
        for output in output:
            print(output)
            for output in output:
                output = output.__str__().replace('[\'', '').replace('\']', '').replace("'", "") + '\t \t'
                file.write(output)
            file.write('\n')
        file.close()


def create_hosts_file(output):
    with open('../hosts.txt', 'w') as file:
        # file.write(headers)
        for i in range(len(hosts)):
            # print(priority[i])
            if priority[i] == 'Ignore':
                continue
            print(hosts[i])

            file.write(hosts[i])
            file.write('\n')
        file.close()


####################################################


if __name__ == '__main__':
    # print_hi('PyCharm')
    pass_exception = {}
    with open("../passwordException.txt", "r") as lines:
        next(lines)
        for line in lines:
            if not line or line.startswith('#'):
                continue
            key, value = line.strip().split()
            pass_exception[key] = value
    print(pass_exception)

    hosts, priority, environment, resource_type,description = get_netbox_data()
    output_from_inventory = get_inventory_info()
    create_inventory_file(output_from_inventory)
    create_hosts_file(output_from_inventory)
