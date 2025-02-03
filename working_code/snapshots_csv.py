import datetime
import csv
from pyvim import connect
from pyVmomi import vim
import ssl
from modules.config_parser import int_host, int_user, int_pass

# Disable SSL verification for self-signed certificates
context = ssl._create_unverified_context()


def get_vcenter_connection(vcenter_ip, username, password):
    """Connect to vCenter and return the service instance."""
    si = connect.SmartConnect(host=vcenter_ip, user=username, pwd=password, sslContext=context)
    return si


# Connection details
vcenter_ip = int_host
username = int_user
password = int_pass

# Connect to vCenter
service_instance = get_vcenter_connection(vcenter_ip, username, password)
content = service_instance.RetrieveContent()


def get_all_vms(content):
    """Retrieve all VMs from vCenter."""
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    return container.view


def get_vm_ip(vm):
    """Retrieve the IP address of the VM (if available)."""
    try:
        ip_address = vm.guest.ipAddress
        return ip_address if ip_address else None  # Return None if no IP
    except Exception:
        return None


def extract_snapshot_info(snapshot_tree):
    """Recursively extracts snapshot details (name, description, createTime)."""
    snapshot_names = []
    snapshot_descriptions = []
    snapshot_dates = []

    for snapshot in snapshot_tree:
        snapshot_names.append(snapshot.name)
        snapshot_descriptions.append(snapshot.description if snapshot.description else "No description added")
        snapshot_dates.append(str(snapshot.createTime))  # Convert to string for CSV

        # Recursively process child snapshots if they exist
        if snapshot.childSnapshotList:
            child_names, child_descs, child_dates = extract_snapshot_info(snapshot.childSnapshotList)
            snapshot_names.extend(child_names)
            snapshot_descriptions.extend(child_descs)
            snapshot_dates.extend(child_dates)

    return snapshot_names, snapshot_descriptions, snapshot_dates


# Get VMs and process snapshots
vms = get_all_vms(content)
timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
csv_filename = f"vm_snapshots_{timestamp}.csv"

# Open CSV file and write the headers
with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
    csv_writer = csv.DictWriter(file,
                                fieldnames=["VM Name", "VM IP", "Number of Snapshots", "Snapshot Names", "Descriptions",
                                            "Created On"])
    csv_writer.writeheader()

    for vm in vms:
        vm_ip = get_vm_ip(vm)  # Get the IP address of the VM

        # Skip VMs with no IP (unknown)
        if vm_ip is None:
            continue

        if vm.snapshot is not None:
            # Extract all snapshots and group them
            snapshot_names, snapshot_descriptions, snapshot_dates = extract_snapshot_info(vm.snapshot.rootSnapshotList)

            # Count the number of snapshots
            num_snapshots = len(snapshot_names)

            # Use newline characters to separate multiple values for better readability in Excel
            csv_writer.writerow({
                "VM Name": vm.name,
                "VM IP": vm_ip,
                "Number of Snapshots": num_snapshots,
                "Snapshot Names": "\n".join(snapshot_names),
                "Descriptions": "\n".join(snapshot_descriptions),
                "Created On": "\n".join(snapshot_dates)
            })

print(f"Snapshot details saved to {csv_filename}")
