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
       
    def connect(self):
        if self.use_ssl:
            raise Exception("SSL not yet implemented")
        
        try:
            self.si = SmartConnectNoSSL(host=self.host, user=self.user, pwd=self.pwd, port=self.port)
            return self.si
        except IOError as e:
            #print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return 0

    def get_vm_hosts(self):
        hosts = []
        content_view = self.si.content.viewManager.CreateContainerView(self.si.content.rootFolder,
                                                            [vim.HostSystem],
                                                            True)
        host_view = content_view.view
        content_view.Destroy()
        for host in host_view:
            hosts.append(host.name)
        return hosts

    def get_host_cert_expiration_date(self,esxi_hostname):
        mob = vim.HostSystem
        content = self.si.content
        mob_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [mob],
                                                        True)
        for mob in mob_list.view:
            if mob.name == esxi_hostname:
                cert_info = mob.configManager.certificateManager.certificateInfo
                expiration_date = str(cert_info.notAfter)
        mob_list.Destroy()
        return expiration_date


