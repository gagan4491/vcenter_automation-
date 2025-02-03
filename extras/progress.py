from tqdm import tqdm
import time

#!/usr/bin/python3
import paramiko
### passing the host Ips in the given list
# host = ['192.168.101.251','192.168.101.252','192.168.101.254','192.168.101.248']
# host = ['192.168.2.2']
host= []
port = 22
username = "root"
password = "1234"

with open("../hosts.txt", "r") as lines:
    for line in lines:
        if line.strip() == "":
            continue
        host.append(line.strip())
        # print("hello")

###  the commands  to run to get the inventory.
command_cpu = "lscpu |grep 'CPU(s):' | head -1 |awk '{print $2}'"
command_ram = "free -m | grep 'Mem:' | awk '{print $2}'"
command_disks = "df -h | grep '^/dev/' | grep -v 'snap' | awk '{print $2, $6}'"
output =[]

items = range(len(host))  # Example iterable


for item in tqdm(items, total=len(items)):

    for i in host:
        temp_output = []

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(i, port, username, password)

        temp_output.append(i)
        stdin, stdout, stderr = ssh.exec_command(command_cpu)
        lines = stdout.readlines()
        # print(lines[0])
        temp_output.append(lines[0].rstrip())
        stdin, stdout, stderr = ssh.exec_command(command_ram)
        lines = stdout.readlines()
        temp_output.append(lines[0].rstrip())

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

    # print(lines)
    # print(output)
    # print(type(lines))
    # print(lines[0])
    # for output in output:
    # print(output)

    headers = "IP's\t\t\t\tCPU's\tRAM(MB)\t\tDISKS(GB)\n"  # headers to add tot inventory file

    with open('inventory.txt', 'w') as file:
        file.write(headers)
        for output in output:
            # print(len(output))
            # file.write(output.__str__() + '\n')

            for output in output:
                file.write(output.__str__().replace('[\'', '').replace('\']', '').replace("'", "").replace('G',
                                                                                                           '') + '\t \t')  ## parsing the values to the inventory file .
            file.write('\n')

        # for line in lines:
        #     line = line.rstrip()
        #     columns = line.split()
        #     if len(columns) == 5:
        #



    time.sleep(1)  # Simulate some work





