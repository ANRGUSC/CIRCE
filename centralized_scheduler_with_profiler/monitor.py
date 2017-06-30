"""
 * Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Aleksandra Knezevic, June 2017
 *      Bhaskar Krishnamachari, June 2017
 *     Read license file in main directory for more details  
"""

import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
taskmodule = __import__(sys.argv[len(sys.argv)-1])
import paramiko
import datetime
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import platform
from os import path


#for OUTPUT folder 
class Watcher1():
    
    DIRECTORY_TO_WATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'output/')

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.observer = Observer()

    def run(self):
        event_handler = Handler1()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler1(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
             
            print("Received file as output - %s." % event.src_path)

            new_file = os.path.split(event.src_path)[-1]
            #case if you are sending back to scheduler
            if nexttasks[0] == 'scheduler':
                sftp[0].put(event.src_path, os.path.join('circe/centralized_scheduler_with_profiler/output', new_file))
            else:
                i=0
                for sftp_output in sftp:
                    sftp_output.put(event.src_path, os.path.join('centralized_scheduler', nexttasks[i], 'input', new_file))
                    i=i+1


#for INPUT folder 
class Watcher(multiprocessing.Process):

    DIRECTORY_TO_WATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'input/')
    
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':

            print("Received file as input - %s." % event.src_path)
            new_file = os.path.split(event.src_path)[-1]


            if platform.system() == 'Windows':
                print(os.path.getctime(event.src_path))
            else:
                print(event.src_path)
                stat = os.stat(event.src_path)
                try:
                    print(stat.st_birthtime)
                except AttributeError:
                    created_time=datetime.datetime.fromtimestamp(stat.st_mtime)
                    print(created_time)

            my_ip=ni.ifaddresses('eth0')[AF_INET][0]['addr']
            pathrun=os.path.join(path.dirname(path.dirname(path.abspath(__file__))),'runtime/')
            runtime_file=os.path.join(pathrun,'droplet_runtime_input_%s'%(my_ip))
            new_file = os.path.split(event.src_path)[-1]
            taskname = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
            if '_' in new_file:
                temp_name = new_file.split('_')[0]
            else:
                temp_name = new_file.split('.')[0]

            with open(runtime_file, 'a') as f:
                line = 'created_input,%s,%s,%s,%s\n' %(my_ip,taskname,temp_name,created_time)
                f.write(line)


            q.put(new_file)

if __name__ == '__main__':

    nexttasks = [] 
    ssh = []
    sftp = []

    for i in range(1, len(sys.argv) - 1,4):

        task_name = sys.argv[i]
        IP = sys.argv[i+1]
        user = sys.argv[i+2]
        password = sys.argv[i+3]
        nexttasks.append(task_name)

        ssh_output = paramiko.SSHClient()
        ssh_output.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_output.connect(IP, username=user, password=password)
        ssh.append(ssh_output)
        sftp_output = ssh_output.open_sftp()
        sftp.append(sftp_output)


	#start the task as another process
    q=multiprocessing.Queue()
    dag_task = multiprocessing.Process(target=taskmodule.task, args=(q,))
    dag_task.start()

    #monitor INPUT as another process
    w=Watcher()
    w.start()

    #monitor OUTPUT in this process
    w1=Watcher1()
    w1.run()

    dag_task.join()





  



