#!/usr/bin/env python
# VEMS Core
# Copyright (c) 2021 Justin Dunn. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Basic Python functions for connecting to the VMWare enviroment.

VMWare
Environment
Management
Scripts
"""

import getpass
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
import atexit
from toolbelt import get_host_expiring_certs, get_vm_hosts, get_host_cert_dates
#place holder for vcenter connection
vc = ''

#function to connect to vcenter, it takes IP or host name, username, password, and the port.
def vems_connect(vc_ip,vc_un,vc_pw,vc_port):
    try:
        global vc 
        vc = SmartConnectNoSSL(host=vc_ip, user=vc_un, pwd=vc_pw, port=vc_port)
        print("Connected to vCenter Successfully")
        return 1
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        return 0

def get_vcinfo():
    aboutInfo = vc.content.about
    print ("Product Name:",aboutInfo.fullName)
    print("Product Build:",aboutInfo.build)
    print("Product Unique Id:",aboutInfo.instanceUuid)
    print("Product Version:",aboutInfo.version)
    print("Product Base OS:",aboutInfo.osType)
    print("Product vendor:",aboutInfo.vendor)
    return 0

def get_vclogin():
    vcenter_host = input("Enter your vCenter IP or Hostname: ")
    vcenter_port = 443
    vcenter_username = input("vCenter Username: ")
    vcenter_password = getpass.getpass(prompt="Password: ", stream=None)
    login_info = [vcenter_host,vcenter_username,vcenter_password,vcenter_port]
    return login_info

def main():
    #print("Hello world!")
    login_info = get_vclogin()
    if vems_connect(*login_info):
        get_vcinfo()
        #lets get all hosts and all of the expiring certificates
        try: 
            hosts = get_vm_hosts(vc)
            get_host_expiring_certs(vc)
        except:
            pass


        Disconnect(vc)
    return 0


# Start program
if __name__ == "__main__":
    main()