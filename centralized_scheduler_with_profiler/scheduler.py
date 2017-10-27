import multiprocessing
import paramiko
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from readconfig import read_config
import datetime
import netifaces as ni
import platform
from os import path



class Watcher():
    DIRECTORY_TO_WATCH = os.getcwd()+'/input'

    def __init__(self):
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
            new_file_name = os.path.split(event.src_path)[-1]

            #Runtime profiler (INPUT FILE on SCHEDULER)
            pathrun=os.path.join(path.dirname(path.abspath(__file__)),'runtime_total/')
            created_time=datetime.datetime.utcnow()
            runtime_file=os.path.join(pathrun,'scheduler_runtime_input')
            with open(runtime_file, 'a+') as f:
                line = 'created_input,%s,%s\n' %(new_file_name,created_time)
                f.write(line)

            #first task info
            first_task='local_pro'
            IPaddr ='162.243.19.184'
            user= 'apac'
            password='apac20!7'

            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPaddr, username=user , password=password )
            sftp=ssh.open_sftp()
            sftp.put(event.src_path, os.path.join('centralized_scheduler', first_task, 'input', new_file_name))
            ssh.close()
            sftp.close()

class Watcher1(multiprocessing.Process):
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
            new_file_name = os.path.split(event.src_path)[-1]

            #Runtime profiler (OUT FILE on SCHEDULER)
            pathrun=os.path.join(path.dirname(path.abspath(__file__)),'runtime_total/')
            finished_time=datetime.datetime.utcnow()
            finished_file=os.path.join(pathrun,'scheduler_runtime_finished')
            with open(finished_file, 'a+') as f:
                line = 'finished_time,%s,%s\n' %(new_file_name,finished_time)
                f.write(line)


def connect(host,nexthosts,flags):

    #flags[0] tells how many inputs tasks needs to wait for
    #flags[1] tells whether task sends different output to different children(FALSE) or one output to all children(TRUE)
    flag_string = flags[0] + " " +flags[1]+" "

    #nexthosts could be a list of hosts or a single host
    hosts_num = len(nexthosts)

    arg_string=""

    for i in range(len(nexthosts)):
        arg_string = arg_string+nexthosts[i][0]+" "+nexthosts[i][1]+" "+nexthosts[i][2]+" "+nexthosts[i][3]+" "

    taskscript = os.path.join('securityapp', host[0]+".py")

    #host is a task-node list [task script, IP, username, password]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host[1], username=host[2], password=host[3])

    print('=======================================')
    print('Initializing ', host[0], ' on ', host[1])

    input_folder = os.path.join('centralized_scheduler', host[0],'input')
    output_folder = os.path.join('centralized_scheduler', host[0],'output')
    runtime_folder = os.path.join('centralized_scheduler','runtime')

    ssh.exec_command("mkdir -p "+input_folder)
    ssh.exec_command("mkdir -p "+output_folder)
    ssh.exec_command("mkdir -p "+runtime_folder)

    sftp=ssh.open_sftp()

    copy_monitor = os.path.join('centralized_scheduler', host[0],'monitor.py')
    copy_task_script = os.path.join('centralized_scheduler', host[0], host[0]+".py")
    copy_runtime_script = os.path.join('centralized_scheduler','runDReport.py')

    sftp.put('monitor.py', copy_monitor)
    sftp.put(taskscript, copy_task_script)
    sftp.put('runDReport.py', copy_runtime_script)

    stdin, stdout, stderr = ssh.exec_command("python3 "+copy_monitor+" "+ flag_string+arg_string+host[0]+" &> out_info.txt")

    #start run-time profilers on nodes
    stdin, stdout, stderr = ssh.exec_command("python3 "+copy_runtime_script)

    sftp.close()
    ssh.close()


if __name__ == '__main__':

    path1 = os.path.join(os.path.abspath(__file__+"/../.."), "config_security.txt")
    path2 = os.path.join(os.path.abspath(__file__+"/../.."), "nodes_security.txt")
    dag_info = read_config(path1,path2)

    #get DAG and home machine info
    first_task = dag_info[0]
    dag = dag_info[1]
    hosts=dag_info[2]


    jobs=[]
    for key, value in dag.items():
        task = key
        host = hosts.get(task)
        nexthosts=[]
        flags=[]
        for i in range(2,len(value)):
            nexthosts.append(hosts.get(value[i]))
        flags.append(value[0])
        flags.append(value[1])
        dag_task=multiprocessing.Process(target=connect, args=(host, nexthosts,flags,))
        jobs.append(dag_task)
        dag_task.start()

    #monitor output folder for the incoming files
    w1=Watcher1()
    w1.start()

    #monitor input folder for the incoming files
    w = Watcher()
    w.run()

    for job in jobs:
        job.join()
