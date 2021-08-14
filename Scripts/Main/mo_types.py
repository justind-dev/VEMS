#!/usr/bin/env python

"""
    I do not know yet if we will be using this or not. 
    It's possible that it would be good if you are doing a very
    detailed report of the environment or cluster etc.

    We shall see, leaving for now.

"""
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
import datetime
import pytz


class Host:
    def __init__(self,view,moid):
        self.view = view
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

