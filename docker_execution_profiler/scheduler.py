
"""
 * Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Aleksandra Knezevic
 *      Bhaskar Krishnamachari
 *     Read license file in main directory for more details  
"""

import paramiko
import os
from multiprocessing import Process
import time

def connect(host):

    os.system("sshpass -p 'apac20!7' scp -r -o StrictHostKeyChecking=no app/ "+host[2]+'@'+host[1]+':~/')

    #host is a list [nodename, IP, username, password]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host[1], username=host[2], password=host[3])

    print("Starting connection with ", host[1])

    chan = ssh.get_transport().open_session()

    chan.exec_command("cd app/; docker build -t profilerimage .")
    chan.recv_exit_status()
    chan1 = ssh.get_transport().open_session()
    chan1.exec_command("cd app/; docker run -h "+host[0]+" profilerimage")
    chan1.recv_exit_status()

    print("Closing connection with ", host[1])

    ssh.close()

nodes = []
nodepath = os.path.join(os.path.abspath(__file__+"/../.."), "nodes_security.txt")

with open(nodepath, 'r') as nodefile:
    next(nodefile)
    for line in nodefile:
        data = line.strip().split(" ")
        nodes.append(data)
print(nodes)

jobs = []
for node in nodes:
    task = Process(target = connect, args=(node,))
    jobs.append(task)
    task.start()

for job in jobs:
    job.join()

