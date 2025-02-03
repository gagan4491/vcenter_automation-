from pyvim import connect
from pyVmomi import vim
import ssl

from modules.config_parser import int_host, int_user, int_pass

# Disable SSL verification for self-signed certificates
context = ssl._create_unverified_context()


def get_vcenter_connection(vcenter_ip, username, password):
    # Connect to vCenter
    si = connect.SmartConnect(host=vcenter_ip, user=username, pwd=password, sslContext=context)
    return si


vcenter_ip = int_host
username = int_user
password = int_pass

# Connect to vCenter
conn = get_vcenter_connection(vcenter_ip, username, password)

content = conn.RetrieveContent()
# print(content)
root_folder = content.rootFolder

vm_view = content.viewManager.CreateContainerView(
    container=root_folder, type=[vim.VirtualMachine], recursive=True
)
vms = vm_view.view
for vm in vms:
    print(vm.name)


