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
        self.host_view = self.si.content.viewManager.CreateContainerView(self.si.content.rootFolder,
                                                            [vim.HostSystem],
                                                            True).view

    def connect(self):
        if self.use_ssl:
            raise Exception("SSL not yet implemented")
        
        try:
            self.si = SmartConnectNoSSL(host=self.host, user=self.user, pwd=self.pwd, port=self.port)
            return self.si
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return 0

class Host:
    def __init__(self,mobid):
        self.mobid = self.mobid
        self.name = self.mobid.name
        self.connectionState = self.mobid.runtime.connectionState
        self.powerState = self.mobid.runtime.powerState
        self.certificateExpirationDate = self.mobid.configManager.certificateManager.certificateInfo.notAfter
        self.certificateStatus = "Unknown"
        self.bootTime = self.mobid.runtime.bootTime
        self.fullEsxiVersion = self.mobid.ConfigInfo.product.fullName
        self.productUUID = self.mobid.ConfigINfo.product.instanceUuid
    
    def print_host_info(self):
        print(f"HOST INFORMATION\n",
                f"Name: {self.name}\n",
                f"Connection State: {self.connectionState}\n",
                f"Power State: {self.powerState}\n",
                f"Certificate Expiration Date: {self.certificateExpirationDate}\n",
                f"Last boot time: {self.bootTime}\n",
                f"Full Product Information: {self.fullEsxiVersion}\n",
                f"Product UUID: {self.productUUID}\n"         
            )

    def check_certificate_expiration(self, number_of_days):
        expiration_datetime = datetime.datetime.now() + datetime.timedelta(days=number_of_days)
        expiration_datetime = pytz.timezone("UTC").localize(expiration_datetime)
        if not self.connectionState == "Connected":
            if self.certificateExpirationDate <= expiration_datetime:
                self.certificateStatus = "Certificate Expiring Soon"
            else:
                self.certificateStatus = "Certificate OK"
        else:
            self.certificateStatus = "Unable to querey, check host connection"


# now, instead of generating storing host information in tuples or lists or dicts 
# we can store all information related to a host in a class
