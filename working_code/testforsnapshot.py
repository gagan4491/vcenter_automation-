from pyvim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vms_from_folder(folder):
    """Recursively retrieve VMs from folders."""
    vms = []
    for entity in folder.childEntity:
        print(f"Checking entity: {entity.name} (Type: {type(entity)}) in folder: {folder.name}")
        if isinstance(entity, vim.VirtualMachine):
            vms.append(entity)
        elif isinstance(entity, vim.Folder):
            print(f"Traversing folder: {entity.name}")
            vms.extend(get_vms_from_folder(entity))
    return vms

def main():
    from modules.config_parser import int_host, int_user, int_pass

    vcenter_host = int_host
    vcenter_user = int_user
    vcenter_password = int_pass

    # Ignore SSL warnings (only for testing, not recommended for production)
    context = ssl._create_unverified_context()

    # Connect to vCenter
    print("Connecting to vCenter...")
    si = SmartConnect(host=vcenter_host, user=vcenter_user, pwd=vcenter_password, sslContext=context)

    if si:
        print("Connected successfully to vCenter!")
    else:
        print("Failed to connect to vCenter.")
        return

    content = si.RetrieveContent()

    # Retrieve VMs
    for datacenter in content.rootFolder.childEntity:
        print(f"Datacenter: {datacenter.name}")
        if isinstance(datacenter, vim.Datacenter):
            vm_folder = datacenter.vmFolder
            print(f"VM Folder: {vm_folder.name}")
            for entity in vm_folder.childEntity:
                print(f"Entity in VM Folder: {entity.name} (Type: {type(entity)})")
            vms = get_vms_from_folder(vm_folder)
            for vm in vms:
                print(f"Found VM: {vm.name}")

    # Disconnect from vCenter
    Disconnect(si)

if __name__ == "__main__":
    main()
