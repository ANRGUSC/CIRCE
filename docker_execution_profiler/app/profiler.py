import timeit
import os
import sys
import paramiko

nodename = sys.argv[1]

def convert_bytes(num):
    """ Convert bytes to Kbit as required by HEFT"""

    # for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
    #     if num < 1024.0:
    #         return "%3.1f %s" % (num, x)
    #     num /= 1024.0
    return num*0.008

def file_size(file_path):
    """ Return the file size in bytes """

    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


#create the task list in the order of execution
task_order = []
tasks_info = open(os.path.join(os.path.dirname(__file__), 'dag.txt'), "r")


#create DAG dictionary
tasks = {}
for line in tasks_info:
    data = line.strip().split(" ")
    tasks.setdefault(data[0], [])
    if data[0] not in task_order:
        task_order.append(data[0])
    for i in range(1, len(data)):
        if (data[i] != 'scheduler'):
            tasks[data[0]].append(data[i])
print("tasks: ", tasks)

#import task modules, put then in a list and create task-module dictinary
task_module = {}
modules=[]
for task in tasks.keys():
    print(task)
    taskmodule  = __import__(task)
    modules.append(taskmodule)
    task_module[task]=(taskmodule)


#write results in a text file
myfile = open(os.path.join(os.path.dirname(__file__), 'profiler_'+nodename+'.txt'), "w")
myfile.write('{0:<5s} {1:<15s} {2:<5s} \n'.format('task', 'time (sec)', 'output_data (Kbit)'))

inputfile = 'input.txt'
pathin = os.path.abspath(os.path.dirname(__file__))
pathout = os.path.abspath(os.path.dirname(__file__))

#execute each task and get the timing and data size
for task in task_order:
    module = task_module.get(task)

    k = timeit.Timer("module.task(inputfile, pathin, pathout)", globals = globals())
    mytime = min(k.repeat(3,1000))/1000
    output_data = file_size(module.task(inputfile, pathin, pathout))
    myfile.write('{0:<5s} {1:<15.10f} {2:s} \n'.format(task, mytime, str(output_data)))

myfile.close()

#send output file back to the scheduler machine
IP = sys.argv[2]
user = sys.argv[3]
pw = sys.argv[4]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(IP, username=user, password=pw)
sftp=ssh.open_sftp()
sftp.put('profiler_'+nodename+'.txt', 'profiler_'+nodename+'.txt')

sftp.close()
ssh.close()








