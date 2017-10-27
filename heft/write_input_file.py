import os
import readconfig
import pymongo
from pymongo import MongoClient
import pandas as pd
import json
import glob

from create_input import init


configuration_path='../dag_security.txt'
dag_info = readconfig.read_config(configuration_path)

tgff_file='input_0.tgff'
target = open(tgff_file, 'w')
target.write('@TASK_GRAPH 0 {')
target.write("\n")
target.write('\tAPERIODIC')
target.write("\n\n")


task_list = dag_info[1].keys()
print(task_list)


task_map = ['t0_%d'%(i) for i in range(0,len(task_list))]
task_dict = dict(zip(task_list, task_map))

num_nodes = len(os.listdir('/home/apac/apac_scheduler/profiler_files'))

computation_matrix =[]
for i in range(0, len(task_list)):
    task_times = []
    computation_matrix.append(task_times)

task_size = {}
for j in range(1, num_nodes):
    file_name = '../profiler_files/profiler_node'+str(j)+'.txt'
    with open(file_name) as inf:
        first_line = inf.readline()
        i=0
        for line in inf:
            parts = line.split()
            #get computation cost from comp time in sec
            computation_matrix[i].append(int(float(parts[1])*10)) #100000
            task_size[parts[0]]=parts[2]
            i=i+1
print(task_size)
for i in range(0,len(task_list)):
    #line = "\tTASK %s\tTYPE %d" %(task_dict.get(task_list[i]),i)
    line = "\tTASK %s\tTYPE %d" %(task_list[i], i)
    target.write(line)
    target.write("\n")
target.write("\n")
dag_key = [k for k in dag_info[1] if dag_info[1][k][0]!='scheduler']


dag = [(k,dag_info[1].get(k)) for k in dag_key]
for i in range(0,len(dag_key)):
    for j in range(0, len(dag_info[1].get(dag_key[i]))):
        #key = "task"+str(i+1)
        key = task_list[i]
        print("Problem: ", task_size.get(key))
        #file size in Kbit is communication const
        comm_cost = int(float(task_size.get(key)))

        line = "\tARC a0_%d \tFROM %s TO %s \tTYPE %d" %(i,task_dict.get(dag_key[i]),task_dict.get(dag_info[1].get(dag_key[i])[j]),comm_cost)
        target.write(line)
        target.write("\n")
target.write("\n")
target.write('}')

node_file = '../nodes_security.txt'
num_processor = 0;
processor_list = []
with open(node_file) as f:
    next(f)
    for line in f:
        #print(line)
        node_info = line.strip().split(" ")
        num_processor = num_processor +1
        processor_list.append(node_info[0])

target.write('\n@computation_cost 0 {\n')
line = '# type version %s\n' %(' '.join(processor_list))
target.write(line)

for i in range(0,len(task_list)):
    line='  %s    0\t%s\n'%(task_dict.get(task_list[i]),' '.join(str(x) for x in computation_matrix[i]))
    target.write(line)
target.write('}')
target.write('\n\n\n\n')


num_quadratic = num_processor*(num_processor-1)
print('=====================')
#print(num_quadratic)
target.write('\n@quadratic 0 {\n')
target.write('# Source Destination a b c\n')
client_mongo = MongoClient('mongodb://localhost:27017/')
db = client_mongo.central_network_profiler
logging = db['quadratic_parameters'].find().sort([("Time_Stamp[UTC]",pymongo.ASCENDING)]).limit(num_quadratic)

for record in logging:
    #print(record)
    info_to_csv=[record['Source[Tag]'],record['Destination[Tag]'],str(record['Parameters'])]
    line = '  %s\t%s\t%s\n'%(info_to_csv[0],info_to_csv[1],info_to_csv[2])
    target.write(line)

target.write('}')
target.close()


#test
num_task, task_names, num_processor, comp_cost, rate, data, quaratic_profile = init('input_0.tgff')
print(num_task)
print(num_processor)
print(comp_cost)
print(rate)
print(data)
#print(quaratic_profile)
