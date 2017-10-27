"""
 ** Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 **     contributor: Quynh Nguyen, Bhaskar Krishnamachari
 **     Read license file in main directory for more details
"""


import paramiko
import time, os

node1="IP"
node2="IP"
node3="IP"

def control_node104():

    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(node1 , username="user", password="password")
    print "node1 connect successfully!"
    ssh1.exec_command('python2 mongo_script/install_package.py')
    print "dependency install successfully!"
    ssh1.exec_command('python2 mongo_script/server.py')
    print "node1 listen at port 5000\n"

def control_node139():

    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect(node2 , username="user", password="password")
    print "node2 connect successfully!"
    ssh2.exec_command('python2 mongo_script/install_package.py')
    print "dependency install successfully!"
    ssh2.exec_command('python2 mongo_script/server.py') 
    print "node2 listen at port 5000\n"

def control_node207():

    ssh3 = paramiko.SSHClient()
    ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh3.connect(node2 , username="user", password="password")
    print "node3 connect successfully!\n"
    ssh3.exec_command('python2 mongo_script/install_package.py')
    print "dependency install successfully!"
    ssh3.exec_command('python2 mongo_script/server.py')
    print "node3 listen at port 5000\n"

def re_exe(cmd, inc = 60):
    while True:
        os.system(cmd)
        time.sleep(inc)


if __name__=="__main__":
    control_node104()
    control_node139()
    control_node207()
    re_exe("python2 insert_to_mongo.py ip_path", 60)
