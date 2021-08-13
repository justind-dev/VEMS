"""
Customizable reports for vSphere enviornment

VMWare Environment Management Scripts"

You will need to store credentials for smtp and the vsphere connection 
using KEYRING module first. 

credential service name = vems_vsphere

"""
import ssl, keyring
from toolbelt import Vcenter


def main():
    #GET CREDENTIALS
    #modify this line to match your username stored in vems_vsphere credential object
    credential = keyring.get_credential("vems_vsphere","Administrator@vsphere.local")
    keyring_pass = credential.password
    keyring_username = credential.username

    #create service instance, edit IP / FQDN of vcenter into 'host' argument
    connection = Vcenter(host="vcenter_ip",user=keyring_username,pwd=keyring_pass,use_ssl=False)


    return 0






# Start program
if __name__ == "__main__":
    main()