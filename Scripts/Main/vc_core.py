#!/usr/bin/env python
# VEMS Core
# Copyright (c) 2021 Justin Dunn. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Basic Python functions for connecting to the VMWare enviroment.

VMWare
Environment
Management
Scripts
"""

from Scripts.Main.toolbelt import Vcenter
import getpass
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl
import atexit
import toolbelt

def main():
    connection = Vcenter(host="",user="",pwd="")


    return 0


# Start program
if __name__ == "__main__":
    main()