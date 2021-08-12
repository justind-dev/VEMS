"""
Basic Python scripts for utlizing pyvmomi with the vsphere enviroment.

VMWare
Environment
Management
Scripts
"""
import getpass
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
import atexit
from toolbelt import Vcenter

def main():
    connection = Vcenter(host="",user="",pwd="",use_ssl=False)

    hosts = connection.get_vm_hosts()

    print(hosts)
    for host in hosts:
        print(connection.get_host_cert_expiration_date(host))
    return 0


# Start program
if __name__ == "__main__":
    main()