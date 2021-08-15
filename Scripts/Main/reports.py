#!/usr/bin/env python
from pyVmomi import vim, vmodl
import datetime, pytz

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
   

def get_host_certificate_expiration_by_name(self, content, name):
    """
    Get the exiration date of a certificate for a host
    """
    certificate = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True)
    self._views.append(container)
    for host in container.view:
        if host.name == name:
            certificate = host.configManager.certificateManager.certificateInfo.notAfter
            break
    return certificate


def get_certificates_expiring_in_days(service_manager, view_manager, number_of_days):
    expiration_dates = {}
    returned_expirations = []
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(days=number_of_days)
    container = service_manager.content.viewManager.CreateContainerView(
        service_manager.content.rootFolder, [vim.HostSystem], True)

    for host in container.view:
        try:
            expiration_dates[host.name] = host.configManager.certificateManager.certificateInfo.notAfter
        except:
            expiration_dates[host.name] = "Certificate could not be retrieved, check host."
            continue        

    for k, v in expiration_dates.items():
        if not type(v) == str:
            if v <= pytz.timezone('US/Eastern').localize(expiration_datetime):
                returned_expirations.append(k)
        else:
            continue
    return returned_expirations


def print_hosts_with_certificates_expiring_in_days(service_manager, view_manager, number_of_days):
    for host in get_certificates_expiring_in_days(service_manager,view_manager, number_of_days):
        print(f"{host} certificate expires in {number_of_days} days or less.")


