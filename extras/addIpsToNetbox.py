import requests
from pynetbox import api
import pandas as pd

url = 'https://192.168.4.101'
token = '557a399a7d9b54276d49019d8b8ba433546239d8'
session = requests.Session()
session.verify = False
nb = api(url, token=token)
nb.http_session = session

p9_ips = ['192.168.4.25/32',
'192.168.4.47/32',
'192.168.4.49/32',
'192.168.4.52/32',
'192.168.4.53/32',
'192.168.4.54/32',
'192.168.4.55/32',
'192.168.4.56/32',
'192.168.4.59/32',
'192.168.4.60/32',
'192.168.4.63/32',
'192.168.4.64/32',
'192.168.4.90/32',
'192.168.4.91/32',
'192.168.4.92/32',
'192.168.4.94/32',
'192.168.4.96/32',
'192.168.4.97/32',
'192.168.4.98/32',
'192.168.4.103/32',
'192.168.4.198/32']


df = pd.read_excel('Book2.xlsx')
# print(df)
def adding_new_data_netbox():

    for i in range(len(df)):
        ip_address_data = {
            'address': df['IP'][i],
            'status': 'active',
            'description': df['Name of vm'][i],
        }

        ip_address = nb.ipam.ip_addresses.create(**ip_address_data)

    ips = nb.ipam.ip_addresses.filter(version=4)

    for ip in ips:
        ip.custom_fields = {'Environment': 'INT', 'Priority': 'Low', 'Resource_Types': 'VM'}
        ip.save()


def updating_fields_nextbox():

    ip_addresses = nb.ipam.ip_addresses.all()
    i = 0

    for ip_address in ip_addresses:
        ip_address.description = df['Name of vm'][i]
        ip_address.save()
        print(ip_address, i)
        i +=1


def update_custom_field_netbox():

    for ip in p9_ips:
        # Fetch the IP address object from NetBox
        ip_address_obj = nb.ipam.ip_addresses.get(address=ip)

        if ip_address_obj is None:
            print(f"IP address {ip} not found.")
            continue

        # Update the custom field
        ip_address_obj.custom_fields['Application'] = 'P9'
        ip_address_obj.save()
        print(f"Updated IP {ip} - Set Application to P9")

        # ip.custom_fields['Application'] = 'P9'
        # ip.save()

        # print(f"Updated IP {ip_address} - Set {custom_field_name} to {custom_field_value}")

# updating_fields_nextbox()

update_custom_field_netbox()