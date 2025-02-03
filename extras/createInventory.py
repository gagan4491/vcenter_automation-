#!/usr/bin/python3
# pip3 install -r requirements.txt
# passing the host Ips in the given list
import os

import paramiko
# import os
import configparser
import re

config = configparser.ConfigParser()
config.read('config.cnf')

password = config.get('root', 'ssh_password')

directory =config.get('output_cfg_files', 'path')
# os.mkdir(directory)
os.makedirs(directory,exist_ok='True')
#
# files = os.listdir(directory)
# for file in files:
#     file_path = os.path.join(directory, file)
#     if os.path.isfile(file_path):
#         os.remove(file_path)

ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
# passing the host Ips in the given list
# host = ['192.168.101.251','192.168.101.252','192.168.101.254','192.168.101.248']
# host_home = ['192.168.2.64']
host = []
priority =[]
port = 22
username = "root"
# password = "1234"

with open("../hosts.txt", "r") as lines:
    for line in lines:

        if not line or line.startswith('#') or not ip_pattern.match(line):
            continue
        # if not ip_pattern.match(line):
        #     print(f"Skipping non-IP value: {line}")
        #     continue

        host.append(line.strip())
        # print("hello")

#  the commands  to run to get the inventory.
command_cpu = "lscpu |grep 'CPU(s):' | head -1 |awk '{print $2}'"
command_ram = "free -m | grep 'Mem:' | awk '{print $2}'"
command_disks = "df -h | grep '^/dev/' | grep -v 'snap' | grep -v '/boot' | awk '{print $2, $6}'"
uname = "lsb_release -d | sed -e 's/Description:[[:space:]]*//' -e 's/ ([^)]*)//; s/ GNU\/Linux//; s/ (.*$)//; s/ LTS//'"
priority = 'Medium'

output = []
for i in host:
    temp_output = []
    print("running commands now for IP :" + i)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(i, port, username, password)

    ############
    stdin, stdout, stderr = ssh.exec_command(uname)
    lines = stdout.readlines()
    # print(len(lines[0].replace(" ", "")))
    temp_output.append(lines[0].replace(" ", "").rstrip().ljust(14))


    temp_output.append(i)

    #########

    temp_output.append(priority.ljust(14))

    #########

    stdin, stdout, stderr = ssh.exec_command(command_cpu)
    lines = stdout.readlines()
    # print(lines[0])
    temp_output.append(lines[0].rstrip())

    stdin, stdout, stderr = ssh.exec_command(command_ram)
    lines = stdout.readlines()
    temp_output.append(lines[0].rstrip().ljust(6))

    # print(lines[0])
    stdin, stdout, stderr = ssh.exec_command(command_disks)

    lines = stdout.read()
    olines = lines.decode().split('\n')
    li = []

    for l in olines:
        # print(l)
        if l == '':
            continue
        li.append(l.rstrip())
    temp_output.append(li)
    # print(temp_output)
    output.append(temp_output)
    ssh.close()
    del ssh, stdin, stdout, stderr

############
# stdin, stdout, stderr = ssh.exec_command(uname)
# lines = stdout.readlines()
# print(lines[0])
# # temp_output.append(lines[0].rstrip())

#########


# print(lines)
# print(output)
# print(type(lines))
# print(lines[0])
# for output in output:
# print(output)

headers = "OS-Version\t\t\tIP's\t\t\t\tPriorty\t\t\t\tCPU's\tRAM(MB)\t\tDISKS(GB/TB)\n"  # headers to add tot inventory file

print("writting output to the inventory.txt file ...")
with open('inventory.txt', 'w') as file:
    file.write(headers)
    for output in output:
        print(output)
        # file.write(output.__str__() + '\n')

        for output in output:
            output = output.__str__().replace('[\'', '').replace('\']', '').replace("'", "").replace('G', '') + '\t \t'
            file.write(output)  ## parsing the values to the inventory file .
        file.write('\n')
    file.close()

    # for line in lines:
    #     line = line.rstrip()
    #     columns = line.split()
    #     if len(columns) == 5:
