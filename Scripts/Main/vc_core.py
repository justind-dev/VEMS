"""
Basic Python scripts for utlizing pyvmomi with the vsphere enviroment.

VMWare
Environment
Management
Scripts'

"""

from toolbelt import Vcenter

def main():
    connection = Vcenter(host="",user="",pwd="",use_ssl=False)
    
    connection.get_certificate_expirations()

    for host in connection.certificates_expiring_in_days(30):
        print(host)
    
    return 0

# Start program
if __name__ == "__main__":
    main()
