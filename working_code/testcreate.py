import ssl
import datetime
import argparse
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

def find_vm_by_ip(vms, target_ip):
    """Find a VM by its IP address."""
    for vm in vms:
        try:
            if vm.guest.ipAddress == target_ip:
                return vm
        except Exception:
            pass  # Ignore VMs without an IP set
    return None

def create_snapshot(vm, snapshot_name, snapshot_desc, memory_flag, quiesce_flag):
    """Create a snapshot for the given VM."""
    try:
        task = vm.CreateSnapshot_Task(
            name=snapshot_name, 
            description=snapshot_desc, 
            memory=memory_flag,  # Memory enabled by default
            quiesce=quiesce_flag
        )
        print(f"Creating snapshot '{snapshot_name}' for VM '{vm.name}' (IP: {vm.guest.ipAddress}) with Memory={memory_flag}...")
        return task
    except Exception as e:
        print(f" Failed to create snapshot: {str(e)}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Create a VM snapshot with memory enabled by default.")
parser.add_argument("--ip", required=True, help="IP address of the VM.")
parser.add_argument("--name", required=True, help="Name for the snapshot.")
parser.add_argument("--no-memory", action="store_true", help="Disable VM memory in the snapshot.")
parser.add_argument("--quiesce", action="store_true", help="Quiesce the file system before snapshot.")
args = parser.parse_args()

# Connection details
vcenter_ip = int_host
username = int_user
password = int_pass

# Connect to vCenter
service_instance = get_vcenter_connection(vcenter_ip, username, password)
content = service_instance.RetrieveContent()

# Get all VMs
vms = get_all_vms(content)

# Find VM by IP
vm = find_vm_by_ip(vms, args.ip)

if vm:
    print(f"Found VM: {vm.name} (IP: {args.ip})")

    # Generate snapshot name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_name = args.name

    # Append VM name and IP to description for tracking
    full_description = f"Snapshot_by_python_script--{timestamp}"

    # Memory is enabled by default unless the user passes --no-memory
    memory_flag = not args.no_memory

    # Create snapshot
    create_snapshot(vm, snapshot_name, full_description, memory_flag, args.quiesce)
    print(f"Snapshot '{snapshot_name}' created successfully for VM '{vm.name}' (IP: {args.ip}).")

else:
    print(f" No VM found with IP address: {args.ip}")
