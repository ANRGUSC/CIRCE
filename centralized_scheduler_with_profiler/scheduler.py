import paramiko
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from multiprocessing import Process
from readconfig import read_config


class Watcher:
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

            #copy the file to the first task node input folder
            sftp.put(event.src_path, os.path.join('centralized_scheduler', first_task, 'input', new_file_name))


def connect(host,nexthosts):

	#if flag=true monitor.py should sent the output file to the homemachine/output folder
	#instead of nextmachine/input folder
 
    #nexthosts could be a list of hosts or a single host
    hosts_num = len(nexthosts)

    arg_string=""
    scripts=[]
    print("host: ", str(host[0]), " nexttask: ", str(nexthosts))
    for i in range(len(nexthosts)):
        arg_string = arg_string+nexthosts[i][0]+" "+nexthosts[i][1]+" "+nexthosts[i][2]+" "+nexthosts[i][3]+" "
        
    taskscript = host[0]+".py"

	#host is a task-node list [task script, IP, username, password]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host[1], username=host[2], password=host[3])

    input_folder = os.path.join('centralized_scheduler', host[0],'input')
    output_folder = os.path.join('centralized_scheduler', host[0],'output')
    runtime_folder = os.path.join('centralized_scheduler','runtime')

    ssh.exec_command("mkdir -p "+input_folder)
    ssh.exec_command("mkdir -p "+output_folder)
    ssh.exec_command("mkdir -p "+runtime_folder)

    sftp=ssh.open_sftp()

    copy_monitor = os.path.join('centralized_scheduler', host[0],'monitor.py')
    copy_task_script = os.path.join('centralized_scheduler', host[0], taskscript)
    copy_runtime_script = os.path.join('centralized_scheduler','runDReport.py')
    copy_nodes_script = os.path.join('centralized_scheduler','nodes.txt')


    sftp.put('monitor.py', copy_monitor)
    sftp.put(taskscript, copy_task_script)
    sftp.put('runDReport.py', copy_runtime_script)
    sftp.put('nodes.txt', copy_nodes_script)

    stdin, stdout, stderr = ssh.exec_command("python3 "+copy_monitor+" "+arg_string+host[0])
    print("python3 "+copy_monitor+" "+arg_string+host[0])

    sftp.close()
    ssh.close()


if __name__ == '__main__':

    path1 = os.path.join(os.path.abspath(__file__+"/../.."), "configuration.txt")
    path2 = "nodes.txt"
    dag_info = read_config(path1,path2)
   
    #get DAG and home machine info
    first_task = dag_info[0]
    dag = dag_info[1]
    hosts=dag_info[2]
    print(len(dag_info))
    print(dag_info[0])
    print(dag_info[1])
    print(dag_info[2])

    jobs=[]
    for key, value in dag.items():
        task = key
        host = hosts.get(task)
        nexthosts=[]
        for i in range(len(value)):
            nexthosts.append(hosts.get(value[i]))
        dag_task=Process(target=connect, args=(host, nexthosts,))
        jobs.append(dag_task)
        dag_task.start()

    #connect to the first host
    first_task_host = hosts.get(first_task)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(first_task_host[1], username=first_task_host[2], password=first_task_host[3])
    sftp=ssh.open_sftp()


    #monitor intput folder for the incoming files
    w = Watcher()
    w.run()

    for job in jobs:
        job.join()








