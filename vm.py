from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

host = 'vcsa.sonicad.org'
user = 'roapi@vsphere.local'
password = 'W7*Q%NK^!V!up5'
port = 443  # default port for vSphere client




to_check = ['192.168.4.15',
'192.168.4.20',
'192.168.4.35',
'192.168.4.45',
'192.168.4.48',
'192.168.4.66',
'192.168.4.93',
'192.168.4.107',
'192.168.4.153',
'192.168.4.159',
'192.168.4.160',
'192.168.4.211']

# Disable SSL warnings (not recommended for production)
context = ssl._create_unverified_context()

# Connect to vSphere client
si = SmartConnect(host=host, user=user, pwd=password, port=port, sslContext=context)

# Retrieve content from vCenter
content = si.RetrieveContent()

def get_all_vms(content):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    return container.view

# Get list of VMs
vms = get_all_vms(content)
# print(vms)

# Open a text file for writing
with open("vm_details.txt", "w") as file:
    # Define the column widths
    col_widths = [50, 15, 30, 20]

    # Write the header
    header = f"{'VM-Name':<{col_widths[0]}} {'IP Address':<{col_widths[1]}} {'OS':<{col_widths[2]}} {'Hostname':<{col_widths[3]}}"
    file.write(header + "\n")
    file.write("-" * sum(col_widths) + "\n")

    # Write details of each VM
    for vm in vms:
        guest = vm.guest
        print(vm.name)
        # break;
        if guest is not None:
            vm_name = vm.name
            ip_address = guest.ipAddress if guest.ipAddress else "N/A"
            os = guest.guestFullName if guest.guestFullName else "N/A"
            hostname = guest.hostName if guest.hostName else "N/A"

            # Format the line with fixed column widths
            line = f"{vm_name:<{col_widths[0]}} {ip_address:<{col_widths[1]}} {os:<{col_widths[2]}} {hostname:<{col_widths[3]}}"
            file.write(line + "\n")

# Disconnect from vCenter
Disconnect(si)
