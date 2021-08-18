#!/usr/bin/env python
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vmodl, vim


class ServiceManager(object):
    """
    Connects to services on a vCenter node.
    """

    def __init__(self, server, username, password):
        self.server_url = server
        self.username = username
        self.password = password
        self.vim_url = None
        self.session = None
        self.si = None
        self.content = None
        self.vim_uuid = None

    def connect(self):
        # Connect to VIM API Endpoint on vCenter Server system
        self.si = SmartConnectNoSSL(host=self.server_url,
                                    user=self.username,
                                    pwd=self.password
                                    )
        assert self.si is not None

        # Retrieve the service content
        self.content = self.si.RetrieveContent()
        assert self.content is not None
        self.vim_uuid = self.content.about.instanceUuid

    def disconnect(self):
        print('disconnecting the session')
        Disconnect(self.si)


class ViewManager(object):
    """
    Handles the views and tasks.
    """

    def __init__(self, service_manager):
        self._views = {}  # dictionary of container views
        self.content = service_manager.content

    def create_view(self, vimtype):
        if vimtype in self._views:
            container = self._views[vimtype]
            return container
        else:
            container = self.content.viewManager.CreateContainerView(
                self.content.rootFolder, [vimtype], True)
            self._views[vimtype] = container
            return container

    def get_obj(self, vimtype, name):
        """
         Get the vsphere managed object associated with a given text name
        """
        obj = None
        container = self.create_view(vimtype)
        for child_object in container.view:
            if child_object.name == name:
                obj = child_object
                break
        return obj

    def get_host_conn_state(self, name):
        host = self.get_obj(vim.HostSystem, name)
        if not host is None:
            conn_state = host.runtime.connectionState
            return conn_state
        else:
            return f"Error getting connection state for {name}"

    def destroy_container_views(self):
        if len(self._views) > 0:
            for k, v in self._views.items():
                try:
                    v.view.Destroy()
                except vmodl.fault.ManagedObjectNotFound:
                    # silently bypass the exception if the objects are already deleted/not found on the server
                    continue
        else:
            print("No views to destroy")
            exit()
