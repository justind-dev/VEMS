#!/usr/bin/env python
import getpass
from http.client import parse_headers
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

    def certificate_expirations(self):
        expirations = {}
        for host in self.allhosts:
            expirations[host.name] = host.configManager.certificateManager.certificateInfo.notAfter
        return expirations            
    
    def get_certificate_expired(self,days):
        # today = str(datetime.now()).split()
        today = datetime.strptime(today[0],"%Y-%d-%m")
        for host in self.allhosts:
            try: 
                expires_date = str(host.configManager.certificateManager.certificateInfo.notAfter)
            except:
                print(f"Issue retrieving certificate details on {host.name}")
                continue
            expires_date = expires_date.split()
            expires_date = str(expires_date[0])
            try:               
                expires_date = datetime.strptime(expires_date,"%Y-%m-%d")
            except ValueError as e:
                print(f"Date conversion error: {e}")
                continue
            #print(f"Host: {host.name} certificate expires on {expires_date}")
            try: 
                if  (expires_date < today + timedelta(days)):
                    print(f"Host: {host.name} certificate expires in less than 30 days on {expires_date}")
                else:
                    print(f"Host: {host.name} certificate is OK")
            except:
                print(f"There was an error comparing dates...")
                continue
