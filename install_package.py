"""
 ** Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 **     contributor: Quynh Nguyen, Bhaskar Krishnamachari
 **     Read license file in main directory for more details
"""

import os
import site


try:
    import requests
except ImportError:
    print "no lib requests"
    import pip
    cmd = "sudo pip2 install requests"
    print "Requests package is missing\nPlease enter root password to install required package"
    os.system(cmd)
    reload(site)
