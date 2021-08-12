#!/usr/bin/env python
from pyVmomi import vim, vmodl
from datetime import datetime

def get_vm_hosts(si):
    host_view = si.content.viewManager.CreateContainerView(si.content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    hosts = list(host_view.view)
    host_view.Destroy()
    return hosts

def get_host_cert_dates(si,esxi_hostname):
    mob = vim.HostSystem
    content = si.content
    mob_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                       [mob],
                                                       True)
    for mob in mob_list.view:
        if mob.name == esxi_hostname:
            cert_info = mob.configManager.certificateManager.certificateInfo
            print(f'Certificate for {esxi_hostname} Valid from ' + str(cert_info.notBefore) + ' to ' + str(cert_info.notAfter))

def get_host_expiring_certs(si,hosts):
    mob = vim.HostSystem
    content = si.content
    mob_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                       [mob],
                                                       True)
    for host in hosts:
        for mob in mob_list.view:
            if mob.name == host:
                cert_info = mob.configManager.certificateManager.certificateInfo
                now = datetime.now()
                dt_string = now.strftime("%Y/%m%d")
                cert_exp = cert_info.notAfter
