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