import csv

import requests
from pynetbox import api
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


netboxUrl = 'https://192.168.4.101'
netboxApiToken = '557a399a7d9b54276d49019d8b8ba433546239d8'

def netbox_connection():
    url = netboxUrl
    token = netboxApiToken
    session = requests.Session()
    session.verify = False
    nb = api(url, token=token)
    nb.http_session = session

    return nb
# nb = netbox_connection()

def get_netbox_data(nb):

    nb = netbox_connection()
    ip_addresses = nb.ipam.ip_addresses.all()

    for ip_address in ip_addresses:
        print(ip_address)


    return


def update_ip_prefix(nb):
    ip_addresses = nb.ipam.ip_addresses.filter(mask_length=32)

    for ip_address in ip_addresses:
        # Extract the IP part (without the prefix)
        ip_part = ip_address.address.split('/')[0]

        # Update the IP address with a new prefix
        new_address = f'{ip_part}/24'
        ip_address.update({'address': new_address})

        print(f'Updated IP: {ip_address.address}')

    return

# def update_hostname_custom_field(ip_address, new_hostname):
#     ip_record = nb.ipam.ip_addresses.get(address=ip_address)
#     if ip_record:
#         ip_record.custom_fields['Hostname'] = new_hostname
#         ip_record.save()
#         print(f"Updated Hostname for {ip_address} to {new_hostname}")
#     else:
#         print(f"IP address {ip_address} not found")


# Print the custom fields


# def update_hostname_in_netbox(device_name, new_hostname):
#     # Find the device in NetBox
#     device = nb.dcim.devices.get(name=device_name)
#     if device:
#         device.name = new_hostname
#         device.save()
#         print(f"Updated hostname for {device_name} to {new_hostname}")
#     else:
#         print(f"Device {device_name} not found")



# # get_netbox_data(nb)
#
# # update_ip_prefix(nb)
# # with open('../vm_details.csv', mode='r') as file:
# #     csv_reader = csv.DictReader(file)
# #     for row in csv_reader:
# #         ip = row['IP Address'].strip()
# #         hostname = row['Hostname'].strip()
# #
# #         print(ip,hostname)
# #
# custom_fields = nb.extras.custom_fields.all()
# for cf in custom_fields:
#     print(f"Name: {cf.name}, Label: {cf.label}, Type: {cf.type}")


def update_hostname_custom_field(ip_address, new_hostname):
    nb =netbox_connection()

    ip_record = nb.ipam.ip_addresses.get(address=ip_address)
    if ip_record:
        ip_record.custom_fields['Hostname'] = new_hostname
        ip_record.save()
        print(f"Updated Hostname for {ip_address} to {new_hostname}")
    else:
        print(f"IP address {ip_address} not found")


# nb = netbox_connection()



def add_ip_to_netbox(ip,hostname):
    nb = netbox_connection()
    print(ip,hostname)
    ip_address_data = {
        'address': ip,
        'status': 'active',
        'description': '',
        'custom_fields' : {'Environment': 'INT', 'Priority': 'Low', 'Resource_Types': 'VM', 'Hostname': str(hostname)}

    }

    ip_address = nb.ipam.ip_addresses.create(**ip_address_data)



# with open('../vm_details.csv', mode='r') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         ip_address = row['IP Address'].strip()
#         hostname = row['Hostname'].strip()
#         print(ip_address,hostname)
#         update_hostname_custom_field(ip_address, hostname)