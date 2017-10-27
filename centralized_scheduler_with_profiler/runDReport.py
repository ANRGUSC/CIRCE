
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
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time

def report_job():
    with open('centralized_scheduler/nodes.txt', 'r') as f:
        scheduler_info = f.readline().split()

    scheduler_IP = scheduler_info[1]
    username = scheduler_info[2]
    password = scheduler_info[3]
    print(scheduler_info)
    dir_remote = 'apac_scheduler/centralized_scheduler_with_profiler/runtime'

    my_ip=ni.ifaddresses('eth0')[AF_INET][0]['addr']
    local_input_path = 'centralized_scheduler/runtime/droplet_runtime_input_%s'%(my_ip)
    local_task_path = 'centralized_scheduler/runtime/droplet_runtime_task_%s'%(my_ip)
    local_finished_path = 'centralized_scheduler/runtime/droplet_runtime_finished_%s'%(my_ip)
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
        client.close()
        os.remove(local_input_path)
        os.remove(local_task_path)
        os.remove(local_finished_path)
    else:
        print('No files exist...')

if __name__ == '__main__':
    sched = BackgroundScheduler()
    sched.start()
    print('Scheduling task-runtime report job')
    sched.add_job(report_job,'interval',id='report', minutes=10,replace_existing=True)

    print('Start the schedulers')

    while True:
        time.sleep(10)
    #sched.shutdown()




