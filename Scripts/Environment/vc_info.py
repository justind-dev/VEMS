#This Script Pulls ESXi Host Version information from your vcenter server.
import requests

from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl

vcenter_host = "[VCENTER IP]"
vcenter_port = 443
vcenter_username = "user@VSPHERE.local"
vcenter_password = "password"
 
# Connecting to vCenter
try:
    vc = SmartConnectNoSSL(host=vcenter_host, user=vcenter_username, pwd=vcenter_password, port=vcenter_port)
    #Debug print("We have successfully connected to the VCenter server!")
    aboutInfo = vc.content.about
    print ("Product Name:",aboutInfo.fullName)
    print("Product Build:",aboutInfo.build)
    print("Product Unique Id:",aboutInfo.instanceUuid)
    print("Product Version:",aboutInfo.version)
    print("Product Base OS:",aboutInfo.osType)
    print("Product vendor:",aboutInfo.vendor)
    Disconnect(vc)
except IOError as e:
    print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    #Debug print ("We Could NOT Connect")
 
