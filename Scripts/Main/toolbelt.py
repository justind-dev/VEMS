#!/usr/bin/env python
import keyring
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
import datetime
import pytz

class Vcenter:
    def __init__(self,host,user,port=443,use_ssl=True):
        self.host = host
        self.user = user
        self.pwd = keyring.get_password("vems_vsphere",self.user)
        self.port = port
        self.use_ssl = use_ssl
        self.si = self.connect()
        self.content = ''
        self.allhosts = {}
        self.certficate_expirations = {}

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
        self.allhosts =  self.si.content.viewManager.CreateContainerView(self.si.content.rootFolder,
                                                            [vim.HostSystem],
                                                            True).view
    def print_hostnames(self):
        for host in self.allhosts:
            print(host.name)

    def get_certificate_expirations(self):
        for host in self.allhosts:
            try:
                self.certficate_expirations[host.name] = host.configManager.certificateManager.certificateInfo.notAfter
            except:
                self.certficate_expirations[host.name] = "Could not retrieve"
                continue
        
    
    def certificates_expiring_in_days(self, number_of_days):
        expirations = []
        expiration_datetime = datetime.datetime.now() + datetime.timedelta(days=number_of_days)
        for k, v in self.certficate_expirations.items():
            if not k == "Could not retrieve":
                if v <= pytz.timezone('US/Eastern').localize(expiration_datetime):
                    expirations.append(k)
        return expirations
    