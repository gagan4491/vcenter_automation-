from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def con_vcenter_int():

    host = 'vcsa.sonicad.org'
    user = 'roapi@vsphere.local'
    password = 'W7*Q%NK^!V!up5'
    port = 443  # default port for vSphere client

    # Disable SSL warnings (not recommended for production)
    context = ssl._create_unverified_context()

    # Connect to vSphere client
    si = SmartConnect(host=host, user=user, pwd=password, port=port, sslContext=context)

    return si



def con_vcenter_qa():

    host = 'lon-vcenter.alertdriving.local'
    user = 'roapi@vsphere.local'
    password = '3&@9ctJKuWXmxm'
    port = 443  # default port for vSphere client

    # Disable SSL warnings (not recommended for production)
    context = ssl._create_unverified_context()

    # Connect to vSphere client
    si = SmartConnect(host=host, user=user, pwd=password, port=port, sslContext=context)

    return si