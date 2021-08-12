#!/usr/bin/env python
import getpass
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
from datetime import datetime

class Vcenter:
    def __init__(self,host,user,pwd,port=443,use_ssl=True):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.use_ssl = use_ssl
        self.si = self.connect()
       
    def connect():
        if self.use_ssl:
            raise Exception("SSL not yet implemented")
        
        try:
            self.si = SmartConnectNoSSL(host=self.host, user=self.user, pwd=self.pwd, port=self.port)
            return self.si
        except IOError as e:
            #print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return 0

    def get_vm_hosts(self):
        host_view = self.si.content.viewManager.CreateContainerView(self.si.content.rootFolder,
                                                            [vim.HostSystem],
                                                            True)
        hosts = list(host_view.view)
        host_view.Destroy()
        return hosts

    def get_host_cert_dates(self,esxi_hostnames):
        mob = vim.HostSystem
        content = self.si.content
        mob_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [mob],
                                                        True)
        for mob in mob_list.view:
            if mob.name == esxi_hostnames:
                cert_info = mob.configManager.certificateManager.certificateInfo
                return (f"Certificate for {esxi_hostnames} Valid from {str(cert_info.notBefore)} to  {str(cert_info.notAfter)}")
        mob_list.Destroy()

