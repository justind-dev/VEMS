#!/usr/bin/env python
"""
Customizable reports for vSphere enviornment

VMWare Environment Management Scripts"

You will need to store credentials for smtp and the vsphere connection 
using KEYRING module first. 

credential vsphere name = vems_vsphere

"""
import ssl, keyring, atexit,sys
from pyVmomi import vim, vmodl
from connection_manager import ServiceManager, ViewManager
import reports


def main():
    #GET CREDENTIALS
    #modify this line to match your username stored in vems_vsphere credential object
    credential = keyring.get_credential("vems_vsphere","Administrator@vsphere.local")
    keyring_pass = credential.password
    keyring_username = credential.username

    service_manager = ServiceManager(server="vcenter_ip_or_fqdn",
                                     username=keyring_username,
                                     password=keyring_pass)
    print("Connecting to VAPI...")
    try: 
        service_manager.connect()
    except:
        print("Could not make connection, check connection, or credentials ")
        sys.exit()

    print("Creating VAPI view manager...")
    try:
        view_manager = ViewManager()
    except:
        print("Could not create VAPI view manager")
        service_manager.disconnect()

    # Let's run some reports...
    print("HOSTS WITH CERTIFICATES EXPIRING SOON")
    reports.print_hosts_with_certificates_expiring_in_days(service_manager, 30)

    #Clean up...
    service_manager.disconnect()
    atexit.register(view_manager.destroy_container_views)
    
    return 0

# Start program
if __name__ == "__main__":
    main()

