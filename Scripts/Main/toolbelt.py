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
        self._views = [] 

    def connect(self):
        if self.use_ssl:
            raise Exception("SSL not yet implemented")
        
        try:
            self.si = SmartConnectNoSSL(host=self.host, user=self.user, pwd=self.pwd, port=self.port)
            return self.si
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return 0

    def get_obj(self,content, vimtype, name):
        """
        Get the vsphere managed object associated with a given text name
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        self._views.append(container)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj


    def get_obj_by_moId(self,content, vimtype, moid):
        """
        Get the vsphere managed object by moid value
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        self._views.append(container)
        for c in container.view:
            if c._GetMoId() == moid:
                obj = c
                break
        return obj

class Host:
    def __init__(self,moid):
        self.moid = self.moid
        self.name = self.moid.name
        self.connectionState = self.moid.runtime.connectionState
        self.powerState = self.moid.runtime.powerState
        self.certificateExpirationDate = self.moid.configManager.certificateManager.certificateInfo.notAfter
        self.certificateStatus = "Unknown"
        self.bootTime = self.moid.runtime.bootTime
        self.fullEsxiVersion = self.moid.ConfigInfo.product.fullName
        self.productUUID = self.moid.ConfigINfo.product.instanceUuid
    
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
