from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL

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
        context = None
        self.si = SmartConnectNoSSL(host=self.server_url,
                               user=self.username,
                               pwd=self.password,
                               sslContext=context)
        assert self.si is not None

        # Retrieve the service content
        self.content = self.si.RetrieveContent()
        assert self.content is not None
        self.vim_uuid = self.content.about.instanceUuid

    def disconnect(self):
        print('disconnecting the session')
        Disconnect(self.si)