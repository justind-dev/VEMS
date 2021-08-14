#!/usr/bin/env python
"""
Customizable reports for vSphere enviornment

VMWare Environment Management Scripts"

You will need to store credentials for smtp and the vsphere connection 
using KEYRING module first. 

credential service name = vems_vsphere

"""
import ssl, keyring, atexit
from pyVmomi import vim, vmodl
from connection_manager import ServiceManager, ViewManager
import reports


def main():
    #GET CREDENTIALS
    #modify this line to match your username stored in vems_vsphere credential object
    credential = keyring.get_credential("vems_vsphere","Administrator@vsphere.local")
    keyring_pass = credential.password
    keyring_username = credential.username

    #create service instance, edit IP / FQDN of vcenter into 'host' argument
    # the view_manager handles our views and objects and tasks
    service_manager = ServiceManager(server="vcenter_ip_or_fqdn",
                                     username=keyring_username,
                                     password=keyring_pass)
    service_manager.connect()
    view_manager = ViewManager()

    #Here we can define our reports
    reports.print_host_names(service_manager,view_manager)


    #Clean Up
    service_manager.disconnect()
    atexit.register(view_manager.destroy_container_views)
    
    return 0

# Start program
if __name__ == "__main__":
    main()

