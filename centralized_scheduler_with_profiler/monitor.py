import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import datetime
taskmodule = __import__(sys.argv[len(sys.argv)-1])
import paramiko
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import platform
from os import path

filenames=[]
files_out=[]

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

            #Runtime profiler (finished_time)
            my_ip=ni.ifaddresses('eth0')[AF_INET][0]['addr']
            pathrun=os.path.join(path.dirname(path.dirname(path.abspath(__file__))),'runtime/')
            finished_time=datetime.datetime.utcnow()
            output_size= os.path.getsize(event.src_path)*8/1000 #in Kbits

            finishedtime_file=os.path.join(pathrun,'droplet_runtime_finished_%s'%(my_ip))
            task_name = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]

            new_file = os.path.split(event.src_path)[-1]


            temp = new_file.split('_')[0]
            extension = new_file.split('.')[-1]
            input_name = temp+'.'+extension
            with open(finishedtime_file, 'a') as f:
                line = 'finished_time,%s,%s,%s,%s,%f\n' %(my_ip,task_name,input_name,finished_time,output_size)
                f.write(line)


            global files_out
            new_file = os.path.split(event.src_path)[-1]

            #based on flag2 decide whether to send one output to all children or different outputs to different children in
            #order given in DAG
            flag2 = sys.argv[2]

            #case if you are sending back to scheduler; flag does not matter
            if sys.argv[3] == 'scheduler':
                IPadrr = sys.argv[4]
                user = sys.argv[5]
                password=sys.argv[6]
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                ssh.connect(IPadrr, username=user,password=password)
                sftp=ssh.open_sftp()
                sftp.put(event.src_path, os.path.join('apac_scheduler/centralized_scheduler_with_profiler/output', new_file))
                sftp.close()
                ssh.close()

            elif flag2 == 'true':
                for i in range(3, len(sys.argv)-1,4):
                    next_task_name=sys.argv[i]
                    IPaddr=sys.argv[i+1]
                    user=sys.argv[i+2]
                    password=sys.argv[i+3]

                    ssh=paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(IPaddr,username=user,password=password)
                    sftp=ssh.open_sftp()
                    sftp.put(event.src_path, os.path.join('centralized_scheduler', next_task_name, 'input', new_file))
                    sftp.close()
                    ssh.close()
            #flag2 == false
            else:
                num_child = (len(sys.argv) - 4) / 4
                files_out.append(new_file)

                if (len(files_out) == num_child):

                    for i in range(3, len(sys.argv)-1,4):
                        myfile = files_out.pop(0)
                        event_path = os.path.join(''.join(os.path.split(event.src_path)[:-1]), myfile)

                        next_task_name=sys.argv[i]
                        IPaddr=sys.argv[i+1]
                        user=sys.argv[i+2]
                        password=sys.argv[i+3]

                        ssh=paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(IPaddr,username=user,password=password)
                        sftp=ssh.open_sftp()
                        sftp.put(event_path, os.path.join('centralized_scheduler', next_task_name, 'input', myfile))
                        sftp.close()
                        ssh.close()

                    files_out=[]

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

            #Runtime profiler (created_time)
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
            taskname = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
            new_file = os.path.split(event.src_path)[-1]
            if '_' in new_file:
                temp = new_file.split('_')[0]
            else:
                temp = new_file.split('.')[0]
            extension = new_file.split('.')[-1]
            input_name = temp+'.'+extension
            with open(runtime_file, 'a') as f:
                line = 'created_input,%s,%s,%s,%s,%f\n' %(my_ip,taskname,input_name,created_time,0)
                f.write(line)

            q.put(new_file)
            filename = new_file

            #Runtime profiler (starting_time)
            my_ip=ni.ifaddresses('eth0')[AF_INET][0]['addr']

            input_path = os.path.split(event.src_path)[0]
            output_path = os.path.join(os.path.split(input_path)[0],'output')

            runtime_path = os.path.join(os.path.split(input_path)[0],'runtime')
            execution_time=datetime.datetime.utcnow()
            runtime_file=os.path.join(pathrun,'droplet_runtime_task_%s'%(my_ip))
            task_name = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
            if '_' in filename:
                temp = filename.split('_')[0]
            else:
                temp = filename.split('.')[0]
            extension = filename.split('.')[-1]
            input_name = temp+'.'+extension
            with open(runtime_file, 'a') as f:
                line = 'execution_time,%s,%s,%s,%s,%f\n' %(my_ip,task_name,input_name,execution_time,0)
                f.write(line)


            global filenames
            flag1 = sys.argv[1]

            if flag1 == "1":

                inputfile=q.get()
                input_path = os.path.split(event.src_path)[0]
                output_path = os.path.join(os.path.split(input_path)[0],'output')
                dag_task = multiprocessing.Process(target=taskmodule.task, args=(inputfile, input_path, output_path))
                dag_task.start()
                dag_task.join()

            else:

                filenames.append(q.get())
                if (len(filenames) == int(flag1)):

                    input_path = os.path.split(event.src_path)[0]
                    output_path = os.path.join(os.path.split(input_path)[0],'output')

                    dag_task = multiprocessing.Process(target=taskmodule.task, args=(filenames, input_path, output_path))
                    dag_task.start()
                    dag_task.join()
                    filenames = []


if __name__ == '__main__':

    q=multiprocessing.Queue()

    #monitor INPUT as another process
    w=Watcher()
    w.start()

    #monitor OUTPUT in this process
    w1=Watcher1()
    w1.run()
