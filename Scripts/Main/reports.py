"""
Customizable reports for vSphere enviornment

VMWare
Environment
Management
Scripts"

You will need to store credentials for smtp and the vsphere connection 
using KEYRING module first. 

credential service name = vems_vsphere

"""
import ssl, keyring
from toolbelt import Vcenter


def main():
    #modify this line to match your username stored in vems_vsphere credential object
    credential = keyring.get_credential("vems_vsphere","Administrator@vsphere.local")

    keyring_pass = credential.password
    keyring_username = credential.username

    connection = Vcenter(host="vcenter_ip",user=keyring_username,pwd=keyring_pass,use_ssl=False)

    connection.get_hosts()

    connection.get_certificate_expirations()

    for host in connection.certificates_expiring_in_days(30):
        print(host)
    
    return 0



# Start program
if __name__ == "__main__":
    main()