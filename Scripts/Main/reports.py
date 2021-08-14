#!/usr/bin/env python
from pyVmomi import vim, vmodl

def get_host_names(service_manager, view_manager):
    all_hosts = view_manager.get_all_objects(service_manager.content, 
                                             vim.HostSystem)
    host_names = []
    for host in all_hosts:
        host_name = view_manager.get_obj(service_manager.content,
                                         vim.HostSystem,host).name
        host_names.append(host_name)
    return host_names


def print_host_names(service_manager, view_manager):
    all_hosts = view_manager.get_all_objects(service_manager.content, 
                                             vim.HostSystem)
    for host in all_hosts:
        host_name = view_manager.get_obj(service_manager.content,
                                         vim.HostSystem,host).name
        print(host_name)
   


