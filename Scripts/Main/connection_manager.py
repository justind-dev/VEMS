#!/usr/bin/env python
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vmodl


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

    def __init__(self):
        self._views = []  # list of container views

    def get_obj(self, content, vimtype, name):
        """
        Get the vsphere managed object associated with a given text name
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vimtype], True)
        self._views.append(container)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj

    def get_obj_by_moid(self, content, vimtype, moid):
        """
        Get the vsphere managed object by moid value
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vimtype], True)
        self._views.append(container)
        for c in container.view:
            if c._GetMoId() == moid:
                obj = c
                break
        return obj

    def get_all_objects(self, content, vimtype):
        """
        Get all managed objects of a certain type
        """
        objects = {}
        container = content.viewManager.CreateContainerView(content.rootFolder,
                                                            [vimtype], True)
        self._views.append(container)
        for c in container.view:
            objects[c.name] = c
        return objects

    def destroy_container_views(self):
        for view in self._views:
            try:
                view.Destroy()
            except vmodl.fault.ManagedObjectNotFound:
                pass  # silently bypass the exception if the objects are already deleted/not found on the server
