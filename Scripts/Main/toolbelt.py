#!/usr/bin/env python
import getpass
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
from datetime import datetime, timedelta


class Vcenter:
    def __init__(self,host,user,pwd,port=443,use_ssl=True):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.use_ssl = use_ssl
        self.si = self.connect()
        self.content = ''
        self.allhosts = self.get_hosts()
       
    def connect(self):
        if self.use_ssl:
            raise Exception("SSL not yet implemented")
        
        try:
            self.si = SmartConnectNoSSL(host=self.host, user=self.user, pwd=self.pwd, port=self.port)
            return self.si
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return 0

    def get_hosts(self):
        return self.si.content.viewManager.CreateContainerView(self.si.content.rootFolder,
                                                            [vim.HostSystem],
                                                            True).view
    def print_hostnames(self):
        for host in self.allhosts:
            print(host.name)

    def get_certificate_expired(self,days):
        for host in self.allhosts:
            expires_string = str(host.configManager.certificateManager.certificateInfo.notAfter).split()
            expires_string = expires_string[0]
            expires_date = datetime.strptime(expires_string,"%Y-%d-%m")
            print(expires_date)
            if  (expires_date < datetime.now() + timedelta(days)):
                print(f"Host: {host.name} certificate expires in less than 30 days on {expires_date}")


    







