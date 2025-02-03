#!/usr/bin/python3

import re

from modules.functions import get_all_vms, add_timestamp_to_filename
from modules.ssh_session import create_ssh_session
from modules.vcenter_connection import con_vcenter_int, con_vcenter_qa



# from pyVmomi import vim
keyfile_2k = '/Users/gsingh/.ssh/id_rsa'
keyfile_4k = None
password = 'sonic_root'
env = 'INT'
filename ='vm_details_QA.csv'
if env == 'INT':
    con = con_vcenter_int()
    filename= 'vm_details_Int.csv'
    

else:
    con = con_vcenter_qa()
    filename='vm_details_QA.csv'


final_filename = add_timestamp_to_filename(filename)
print(final_filename)
content = con.RetrieveContent()
# print(content)
def is_ipv4(address):
    return re.match(r'^\d{1,3}(\.\d{1,3}){3}$', address) is not None

vms = get_all_vms(content)


command_hostname = "cat /etc/hostname"
command_check_ska = "cat /etc/ssh/sshd_config|grep 'keys-sync'"

with open(final_filename, "w") as file:
    # Write the header
    file.write(f"{'VM Name'},{'IP Address'},{'Hostname'},{'Vm_Tool_Version'},{'cat/etc/hostname'},{'SKA'},{'Auth'},{'OS'}\n")

    # Iterate over each VM and write details
    for vm in vms:
        hostname = vm.guest.hostName if vm.guest.hostName is not None else "N/A"
        toolversion = vm.guest.toolsVersion if vm.guest.toolsVersion is not None else "N/A"
        ip_written = False
        cat_hostname = ""
        ska = ''

        if vm.guest is not None and vm.guest.net:
            os = vm.guest.guestFullName if vm.guest.guestFullName else "N/A"

            for nic in vm.guest.net:
                if nic.ipConfig is not None and nic.ipConfig.ipAddress:
                    # Find the first IPv4 address that does not start with 172
                    for ip in nic.ipConfig.ipAddress:
                        if is_ipv4(ip.ipAddress) and not ip.ipAddress.startswith('172'):
                            ip_info = f"{ip.ipAddress}/{ip.prefixLength}"
                            try:

                                print(ip.ipAddress)
                                ssh,auth = create_ssh_session(hostname=ip.ipAddress,keyfile_2k=keyfile_2k,keyfile_4k=keyfile_4k,password=password)
                                # print(auth)
                                ############
                                if ssh:
                                    stdin, stdout, stderr = ssh.exec_command(command_hostname)
                                    lines = stdout.readlines()
                                    cat_hostname= (str(lines[0])).strip()
                                    stdin, stdout, stderr = ssh.exec_command(command_check_ska)
                                    ska_command_output = stdout.readlines()
                                    if ska_command_output:
                                        ska= 'Yes'
                                    else:
                                        ska = 'No'
                                    file.write(f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname},{ska},{auth},{os}\n")
                                    ssh.close()
                                    del ssh, stdin, stdout, stderr
                                else:
                                    print(f"Failed to connect to the {ip.ipAddress}")
                            except:
                                print("dont have access to : ",ip.ipAddress)
                                cat_hostname = "unknown"
                                auth = "unknown"
                                ska = 'N/A'
                                file.write(f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname},{ska},{auth},{os}\n")
                            ip_info = f"{ip.ipAddress}/{ip.prefixLength}"

print("you will find the output in the given : ",final_filename)
