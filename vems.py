#!/usr/bin/env python
"""
Customizable reports for vSphere environment

VMWare Environment Management Scripts"

You will need to store credentials for smtp and the vsphere connection 
using KEYRING module first. 

credential vsphere name = vems_vsphere

"""
import atexit
import keyring
import sys
from connection_manager import ServiceManager, ViewManager
from toolbelt import Report


def main():

    """
        CONNECT TO SERVICE MANAGER
        Modify this section to match your username stored in vems_vsphere credential object
        as created by keyring ahead of time.

        Modify vcenter_ip_or_fqdn to match your own vcenter ip address of fully qualified
        domain name.
    """

    credential = keyring.get_credential("vems_vsphere", "Administrator@vsphere.local")
    keyring_pass = credential.password
    keyring_username = credential.username

    service_manager = ServiceManager(server="vcenter_ip_or_fqdn",
                                     username=keyring_username,
                                     password=keyring_pass)
    try:
        service_manager.connect()
    except:
        print("Could not make connection, check connection, or credentials ")
        sys.exit()
    try:
        view_manager = ViewManager(service_manager)
    except:
        print("Could not create VAPI view manager")
        service_manager.disconnect()

    """
        REPORTS SECTION
        Here you call the reports you have defined in toolbelt.py
    """
    reports = Report(service_manager, view_manager)

    reports.create_report()

    # Clean up...
    service_manager.disconnect()
    atexit.register(view_manager.destroy_container_views)

    return 0


# Start program
if __name__ == "__main__":
    main()
