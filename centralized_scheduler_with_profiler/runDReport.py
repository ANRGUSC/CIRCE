"""
 ** Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 **     contributor: Quynh Nguyen, Bhaskar Krishnamachari
 **     Read license file in main directory for more details
"""

import paramiko
from scp import SCPClient
from netifaces import AF_INET, AF_INET6, AF_LINK
import netifaces as ni
import os
import sys
from os import path

with open('nodes.txt', 'r') as f:
    scheduler_info = f.readline().split()

scheduler_IP = scheduler_info[1]
username = scheduler_info[2]
password = scheduler_info[3]
print(scheduler_info)
dir_remote = 'centralized_scheduler/runtime'

my_ip=ni.ifaddresses('eth0')[AF_INET][0]['addr']
local_input_path = 'runtime/droplet_runtime_input_%s'%(my_ip)
local_task_path = 'runtime/droplet_runtime_task_%s'%(my_ip)
local_finished_path = 'runtime/droplet_runtime_finished_%s'%(my_ip)
if path.isfile(local_input_path) and path.isfile(local_task_path) and path.isfile(local_finished_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(scheduler_IP, username=username,password=password)
    remote_path = '%s'%(dir_remote)
    scp = SCPClient(client.get_transport())
    scp.put(local_input_path, remote_path)
    scp.put(local_task_path, remote_path)
    scp.put(local_finished_path, remote_path)
    scp.close()
    os.remove(local_input_path)
    os.remove(local_task_path)
    os.remove(local_finished_path)
else:
    print('No files exist...')




