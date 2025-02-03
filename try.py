import csv
import pynetbox

from modules.netbox import netbox_connection, add_ip_to_netbox

# Connect to NetBox
nb = netbox_connection()

# Function to get all IP addresses from NetBox
def get_all_netbox_ips():
    netbox_ips = set()
    ip_records = nb.ipam.ip_addresses.all()
    for ip_record in ip_records:
        # Assuming you're interested in the main IP address, not the CIDR
        netbox_ips.add(ip_record.address)
    return netbox_ips

# Read IP addresses from the CSV file
csv_ip_hostnames = {}  # Dictionary to map IP addresses to hostnames

with open('vm_details.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        ip_address = row['IP Address']
        hostname = row['Hostname'].strip() if 'Hostname' in row else 'N/A'

        if ip_address != 'IP not available':
            csv_ip_hostnames[ip_address] = hostname

# Get all IP addresses from NetBox
netbox_ips = get_all_netbox_ips()

# Find IP addresses that are in the CSV but not in NetBox, and get their hostnames
missing_ips = set(csv_ip_hostnames.keys()).difference(netbox_ips)

# Print the missing IP addresses and their hostnames
for ip in missing_ips:
    print(f"Missing IP: {ip}, Hostname: {csv_ip_hostnames[ip]}")
    ip = str(ip)
    hostname = str(csv_ip_hostnames[ip])

    # add_ip_to_netbox(ip,hostname)


#
#
#
# custom_fields = nb.extras.custom_fields.all()
# for cf in custom_fields:
#     print(f"Name: {cf.name}, Label: {cf.label}, Type: {cf.type}")
#
#
