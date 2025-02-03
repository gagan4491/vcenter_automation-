import re

from modules.functions import get_all_vms
from modules.ssh_session import create_ssh_session, create_ssh_sessionqa
from modules.vcenter_connection import con_vcenter_qa

# from pyVmomi import vim

con = con_vcenter_qa()
content = con.RetrieveContent()
# print(content)
def is_ipv4(address):
    return re.match(r'^\d{1,3}(\.\d{1,3}){3}$', address) is not None

vms = get_all_vms(content)


command_hostname = "cat /etc/hostname"

with open("vm_details_QA.csv", "w") as file:
    # Write the header
    file.write(f"{'VM Name'},{'IP Address'},{'Hostname'},{'Vm_Tool_Version'},{'cat/etc/hostname'}\n")

    # Iterate over each VM and write details
    for vm in vms:
        hostname = vm.guest.hostName if vm.guest.hostName is not None else "N/A"
        toolversion = vm.guest.toolsVersion if vm.guest.toolsVersion is not None else "N/A"
        ip_written = False
        cat_hostname =""
        if vm.guest is not None and vm.guest.net:

            for nic in vm.guest.net:
                if nic.ipConfig is not None and nic.ipConfig.ipAddress:
                    # Find the first IPv4 address that does not start with 172
                    for ip in nic.ipConfig.ipAddress:
                        if is_ipv4(ip.ipAddress) and not ip.ipAddress.startswith('172'):
                            ip_info = f"{ip.ipAddress}/{ip.prefixLength}"
                            try:

                                print(ip.ipAddress)
                                ssh = create_ssh_sessionqa(hostname=ip.ipAddress)
                                # print(ssh)
                                ############
                                stdin, stdout, stderr = ssh.exec_command(command_hostname)
                                lines = stdout.readlines()
                                cat_hostname= (str(lines[0])).strip()
                                file.write(f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname}\n")




                            except:
                                print("dont have access to : ",ip.ipAddress)
                                cat_hostname = "dont have access "
                                file.write(f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname}\n")
                            ip_info = f"{ip.ipAddress}/{ip.prefixLength}"
                            # file.write(f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname}\n")
                            # print(f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname}")
                    # ssh.close()
                    # # print("ssh close")
                    # del ssh, stdin, stdout, stderr




        # if not ip_written:
        #     print(f"{vm.name},{'IP not available'},{hostname}")


