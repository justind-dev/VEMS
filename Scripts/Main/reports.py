"""
Customizable reports for vSphere enviornment

VMWare
Environment
Management
Scripts'

You will need to store credentials for smtp and the vsphere connection 
using keyring module first. If you use active directory do so in this
format: domain\\samaccountname
credential service name = vems_vsphere
username = vsphere username
password = vsphere password
"""
import smtplib, ssl, keyring
from toolbelt import Vcenter

def main():
    connection = Vcenter(host="vcenter",user="example@vsphere.local",use_ssl=False)
    connection.get_hosts()
    connection.get_certificate_expirations()

    for host in connection.certificates_expiring_in_days(30):
        print(host)
    
    return 0

# Start program
if __name__ == "__main__":
    main()
