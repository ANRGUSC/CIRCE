"""
 * Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Aleksandra Knezevic
 *      Bhaskar Krishnamachari
 *     Read license file in main directory for more details  
"""

import paramiko
import os

def connect(IPaddr, user, passwrd):


    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IPaddr, username=user, password=passwrd)
    ssh.exec_command("pkill -f centralized_scheduler")
    ssh.exec_command("rm out_info.txt")
    ssh.exec_command("rm -rf centralized_scheduler/")
    ssh.close()

#update list of IP addresses used, user name and password
IP=['IP','IP','IP']
users = 'user'
passwords='password'
for i in range(0, len(IP)):
        print(IP[i])
        connect(IP[i], users, passwords)

os.system('pkill -f scheduler')
