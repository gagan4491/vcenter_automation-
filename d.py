import re

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# vSphere connection details
# host = 'vcsa.sonicad.org'
# user = 'roapi@vsphere.local'
# password = 'W7*Q%NK^!V!up5'
# port = 443  # default port for vSphere client
#
# # Disable SSL warnings (not recommended for production)
# context = ssl._create_unverified_context()
#
# # Connect to vSphere client
# si = SmartConnect(host=host, user=user, pwd=password, port=port, sslContext=context)
#
# # Retrieve content from vCenter
# content = si.RetrieveContent()
from modules.functions import get_all_vms
from modules.vcenter_connection import con_vcenter_qa, con_vcenter_int
from pyVmomi import vim

con = con_vcenter_int()
content = con.RetrieveContent()

def get_all_vms(content):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    return container.view


def is_ipv4(address):
    return re.match(r'^\d{1,3}(\.\d{1,3}){3}$', address) is not None


# Get list of VMs
vms = get_all_vms(content)


# Open a text file for writing
with open("vm_details_qa.txt", "w") as file:
    # Define the column widths
    col_widths = [50, 15, 30, 20]

    # Write the header
    header = f"{'VM-Name':<{col_widths[0]}} {'IP Address':<{col_widths[1]}} {'OS':<{col_widths[2]}} {'Hostname':<{col_widths[3]}}"
    file.write(header + "\n")
    file.write("-" * sum(col_widths) + "\n")

    # Write details of each VM
    for vm in vms:
        guest = vm.guest
        print(guest)
        # break
        if guest is not None:
            vm_name = vm.name
            if not guest.ipAddress:
                continue
            ip_address = ''
            for nic in vm.guest.net:
                if nic.ipConfig is not None and nic.ipConfig.ipAddress:
                    # Find the first IPv4 address that does not start with 172
                    for ip in nic.ipConfig.ipAddress:
                        if is_ipv4(ip.ipAddress) and not ip.ipAddress.startswith('172'):
                            ip_address = f"{ip.ipAddress}/{ip.prefixLength}"

            os = guest.guestFullName
            hostname = guest.hostName

            # Format the line with fixed column widths
            line = f"{vm_name:<{col_widths[0]}} {ip_address:<{col_widths[1]}} {os:<{col_widths[2]}} {hostname:<{col_widths[3]}}"
            file.write(line + "\n")

# Disconnect from vCenter
# Disconnect(si)
