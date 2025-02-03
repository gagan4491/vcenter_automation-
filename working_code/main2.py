#!/usr/bin/python3

import re
from modules.config_parser import ssh_keyfile_path, ssh_password, env_cfg, int_host, int_user, int_pass, qa_host, \
    qa_user, qa_pass, prod_host, prod_user, prod_pass
from modules.functions import get_all_vms, add_timestamp_to_filename
from modules.ssh_session import create_ssh_session
from modules.vcenter_connection import con_vcenter

keyfile_4k = ssh_keyfile_path
password = ssh_password
env = env_cfg
filename = ''
if env == 'INT':
    print("#########################################################")
    print("running inventory for INT")
    print("#########################################################")
    host = int_host
    user = int_user
    password = int_pass
    con = con_vcenter(host=int_host, user=int_user, password=password)
    filename = 'vm_details_Int.csv'

elif env == 'QA':
    print("#########################################################")
    print("running inventory for QA")
    print("#########################################################")
    host = qa_host
    user = qa_user
    password = qa_pass
    con = con_vcenter(host=qa_host, user=qa_user, password=password)
    filename = 'vm_details_QA.csv'

elif env == 'PROD':
    print("#########################################################")
    print("running inventory for PROD")
    print("#########################################################")
    host = prod_host
    user = prod_user
    password = prod_pass
    con = con_vcenter(host=prod_host, user=prod_user, password=password)
    filename = 'vm_details_Prod.csv'
else:
    print("check the environment field under conf.cnf thanks......")

final_filename = add_timestamp_to_filename(filename)
print(final_filename)
content = con.RetrieveContent()


def is_ipv4(address):
    return re.match(r'^\d{1,3}(\.\d{1,3}){3}$', address) is not None


def get_snapshots(vm):
    """Retrieve the names and count of snapshots for a given VM."""
    snapshot_names = []
    if vm.snapshot is not None:
        snapshot_names = get_snapshot_names(vm.snapshot.rootSnapshotList)
    snapshot_count = len(snapshot_names)
    return snapshot_count, snapshot_names


def get_snapshot_names(tree):
    """Helper function to recursively retrieve snapshot names from the tree."""
    names = []
    for snapshot in tree:
        names.append(snapshot.name)
        if snapshot.childSnapshotList:
            names.extend(get_snapshot_names(snapshot.childSnapshotList))
    return names


vms = get_all_vms(content)

command_hostname = "cat /etc/hostname"
command_check_ska = "cat /etc/ssh/sshd_config|grep 'keys-sync'"

with open(final_filename, "w") as file:
    file.write(
        f"{'VM Name'},{'IP Address'},{'Hostname'},{'Vm_Tool_Version'},{'cat/etc/hostname'},{'SKA'},{'Auth'},{'OS'},{'Snapshots Count'},{'Snapshot Names'}\n")

    for vm in vms:
        hostname = vm.guest.hostName if vm.guest.hostName is not None else "N/A"
        toolversion = vm.guest.toolsVersion if vm.guest.toolsVersion is not None else "N/A"
        ip_written = False
        cat_hostname = ""
        ska = ''
        snapshot_count, snapshot_names = get_snapshots(vm)  # Get the number and names of snapshots
        snapshot_names_str = ', '.join(snapshot_names) if snapshot_names else "None"

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
                                ssh, auth = create_ssh_session(hostname=ip.ipAddress, keyfile_4k=keyfile_4k,
                                                               password=password)
                                ############
                                if ssh:
                                    stdin, stdout, stderr = ssh.exec_command(command_hostname)
                                    lines = stdout.readlines()
                                    cat_hostname = (str(lines[0])).strip()
                                    stdin, stdout, stderr = ssh.exec_command(command_check_ska)
                                    ska_command_output = stdout.readlines()
                                    if ska_command_output:
                                        ska = 'Yes'
                                    else:
                                        ska = 'No'
                                    file.write(
                                        f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname},{ska},{auth},{os},{snapshot_count},{snapshot_names_str}\n")
                                    ssh.close()
                                    del ssh, stdin, stdout, stderr
                                else:
                                    print(f"Failed to connect to the {ip.ipAddress}")
                            except:
                                print("Don't have access to: ", ip.ipAddress)
                                cat_hostname = "unknown"
                                auth = "unknown"
                                ska = 'N/A'
                                file.write(
                                    f"{vm.name},{ip_info},{hostname},{toolversion},{cat_hostname},{ska},{auth},{os},{snapshot_count},{snapshot_names_str}\n")
                            ip_info = f"{ip.ipAddress}/{ip.prefixLength}"

print("You will find the output in the given: ", final_filename)
