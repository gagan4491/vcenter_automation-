import ssl
from pyvim import connect
from pyVmomi import vim
from modules.config_parser import int_host, int_user, int_pass

# Disable SSL verification for self-signed certificates
context = ssl._create_unverified_context()


def get_vcenter_connection(vcenter_ip, username, password):
    """Connect to vCenter and return the service instance."""
    si = connect.SmartConnect(host=vcenter_ip, user=username, pwd=password, sslContext=context)
    return si


def get_all_vms(content):
    """Retrieve all VMs from vCenter."""
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    return container.view


def get_vm_ip(vm):
    """Retrieve the IP address of the VM (if available)."""
    try:
        return vm.guest.ipAddress if vm.guest.ipAddress else None  # Return None if no IP
    except Exception:
        return None


def find_vm_by_ip(vms, target_ip):
    """Find a VM by its IP address."""
    for vm in vms:
        try:
            if vm.guest.ipAddress == target_ip:
                return vm
        except Exception:
            pass  # Ignore VMs that do not have an IP set
    return None


def find_snapshot_by_description(snapshot_tree, target_description):
    """Recursively searches for a snapshot with a specific description."""
    for snapshot in snapshot_tree:
        if snapshot.description.strip().lower() == target_description.strip().lower():
            return snapshot

        # Check child snapshots recursively
        found_snapshot = find_snapshot_by_description(snapshot.childSnapshotList, target_description)
        if found_snapshot:
            return found_snapshot
    return None


def delete_snapshot(vm, snapshot):
    """Deletes the specified snapshot from the VM."""
    try:
        task = snapshot.snapshot.RemoveSnapshot_Task(removeChildren=False)
        print(f"Deleting snapshot '{snapshot.name}' for VM '{vm.name}'...")
        return task
    except Exception as e:
        print(f" Failed to delete snapshot: {str(e)}")


# Connection details
vcenter_ip = int_host
username = int_user
password = int_pass

# Connect to vCenter
service_instance = get_vcenter_connection(vcenter_ip, username, password)
content = service_instance.RetrieveContent()

# Get all VMs
vms = get_all_vms(content)

# Prompt user for target VM IP and snapshot description
target_ip = input("Enter the VM's IP address: ").strip()
target_description = input("Enter the description of the snapshot to delete: ").strip()

# Find VM by IP
vm = find_vm_by_ip(vms, target_ip)

if vm:
    print(f" Found VM: {vm.name} (IP: {target_ip})")

    if vm.snapshot is not None:
        snapshot_to_delete = find_snapshot_by_description(vm.snapshot.rootSnapshotList, target_description)

        if snapshot_to_delete:
            delete_snapshot(vm, snapshot_to_delete)
            print(f" Snapshot '{snapshot_to_delete.name}' deleted successfully for VM '{vm.name}'.")
        else:
            print(f" No snapshot found with the description '{target_description}' for VM '{vm.name}'.")
    else:
        print(f" VM '{vm.name}' has no snapshots.")
else:
    print(f" No VM found with IP address: {target_ip}")
