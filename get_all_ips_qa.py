import re

from modules.functions import get_all_vms
from modules.vcenter_connection import con_vcenter_qa
from pyVmomi import vim

con = con_vcenter_qa()
content = con.RetrieveContent()

def is_ipv4(address):
    return re.match(r'^\d{1,3}(\.\d{1,3}){3}$', address) is not None


vms = get_all_vms(content)

# print(vim.net.IpConfigInfo.IpAddress)
# for vm in vms:
#     if vm.guest is not None and vm.guest.net is not None:
#         for net in vm.guest.net:
#             if net.ipConfig is not None and net.ipConfig.ipAddress is not None:
#                 for ip in net.ipConfig.ipAddress:
#                     print(f"VM: {vm.name}, IP Address: {ip.ipAddress}")


# for vm in vms:
#     if vm.guest is not None and vm.guest.net:
#         print(f"VM: {vm.name}")
#         for nic in vm.guest.net:
#             print(f"  NIC Device: {nic.deviceConfigId}, MAC Address: {nic.macAddress}")
#             for ip in nic.ipConfig.ipAddress:
#                 if not ip :
#                     print("N/A")
#                 else:
#                     print(f"    IP Address: {ip.ipAddress}, Prefix Length: {ip.prefixLength}")


#
# with open("vm_details.csv", "w") as file:
#     # Write the header
#     file.write(f"{'VM Name':<30},{'IP Address':<20}\n")
#
#     # Iterate over each VM and write details
#     for vm in vms:
#         if vm.guest is not None and vm.guest.net:
#             for nic in vm.guest.net:
#                 if nic.ipConfig is not None and nic.ipConfig.ipAddress:
#                     ip_info = str(nic.ipConfig.ipAddress[0].ipAddress) + '/' + str(nic.ipConfig.ipAddress[0].prefixLength)
#                     file.write(f"{vm.name:<30},{ip_info:<20}\n")
#                 else:
#                     file.write(f"{vm.name:<30},{'IP not available':<20}\n")
# with open("vm_details.csv", "w") as file:
#     # Write the header
#     file.write(f"{'VM Name':<30},{'IP Address':<20}\n")
#
#     # Iterate over each VM and write details
#     for vm in vms:
#         if vm.guest is not None and vm.guest.net:
#             for nic in vm.guest.net:
#                 if nic.ipConfig is not None and nic.ipConfig.ipAddress:
#                     # Find the first IPv4 address
#                     ipv4_info = next(((ip.ipAddress, ip.prefixLength) for ip in nic.ipConfig.ipAddress if is_ipv4(ip.ipAddress)), ('IP not available', ''))
#                     ip_info = f"{ipv4_info[0]}/{ipv4_info[1]}" if ipv4_info[1] != '' else ipv4_info[0]
#                     file.write(f"{vm.name:<30},{ip_info:<20}\n")
#                 else:
#                     file.write(f"{vm.name:<30},{'IP not available':<20}\n")

# with open("vm_details.csv", "w") as file:
#     # Write the header
#     file.write(f"{'VM Name':<35},{'IP Address':<20}{'Hostname':<35}\n")
#
#     # Iterate over each VM and write details
#     for vm in vms:
#         if vm.guest is not None and vm.guest.net:
#             for nic in vm.guest.net:
#                 if nic.ipConfig is not None and nic.ipConfig.ipAddress:
#                     # Find the first IPv4 address that does not start with 172
#                     for ip in nic.ipConfig.ipAddress:
#                         if is_ipv4(ip.ipAddress) and not ip.ipAddress.startswith('172'):
#                             ip_info = f"{ip.ipAddress}/{ip.prefixLength}"
#                             file.write(f"{vm.name:<30},{ip_info:<20}\n,{vm.host}")
#                             break
#                     # else:
#                     #     file.write(f"{vm.name:<30},{'IP not available':<20}\n")
#                 else:
#                     file.write(f"{vm.name:<30},{'IP not available':<20}\n")


with open("vm_details_qa.csv", "w") as file:
    # Write the header
    file.write(f"{'VM Name'},{'IP Address'},{'Hostname'},{'Vm_Tool_Version'}\n")

    # Iterate over each VM and write details
    for vm in vms:
        hostname = vm.guest.hostName if vm.guest.hostName is not None else "N/A"
        toolversion = vm.guest.toolsVersion if vm.guest.toolsVersion is not None else "N/A"
        ip_written = False
        if vm.guest is not None and vm.guest.net:

            for nic in vm.guest.net:
                if nic.ipConfig is not None and nic.ipConfig.ipAddress:
                    # Find the first IPv4 address that does not start with 172
                    for ip in nic.ipConfig.ipAddress:
                        if is_ipv4(ip.ipAddress) and not ip.ipAddress.startswith('172'):
                            ip_info = f"{ip.ipAddress}/{ip.prefixLength}"
                            file.write(f"{vm.name},{ip_info},{hostname},{toolversion}\n")

                            ip_written = True
                            break
        if not ip_written:
            file.write(f"{vm.name},{'IP not available'},{hostname}\n")
            print(f"{vm.name},{'IP not available'},{hostname}\n")
