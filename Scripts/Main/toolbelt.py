#!/usr/bin/env python
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
import datetime
import pytz

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

    def certificate_expirations(self):
        expirations = {}
        for host in self.allhosts:
            try:
                expirations[host.name] = host.configManager.certificateManager.certificateInfo.notAfter
            except:
                datetime.datetime(1988, 12, 30)
                continue
        return expirations
    
    def certificates_expiring_in_days(self, number_of_days):
        expirations = []
        expiration_datetime = datetime.datetime.now() + datetime.timedelta(days=number_of_days)
        for k, v in self.certificate_expirations().items():
            if v <= pytz.timezone('US/Eastern').localize(expiration_datetime):
                expirations.append(k)
        return expirations
    