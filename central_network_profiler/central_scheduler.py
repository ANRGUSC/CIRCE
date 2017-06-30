"""
 ** Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 **     contributor: Quynh Nguyen, Bhaskar Krishnamachari
 **     Read license file in main directory for more details
"""
import os
from pymongo import MongoClient
import pandas as pd
import json
from apscheduler.schedulers.background import BackgroundScheduler
import time
import subprocess

def do_update_quadratic():
    client_mongo = MongoClient('mongodb://localhost:27017/')
    db = client_mongo.central_network_profiler
    parameters_folder='parameters'
    logging = db['quadratic_parameters']
    try:
        for subdir, dirs, files in os.walk(parameters_folder):
            for file in files:
                if file.startswith("."): continue
                measurement_file = os.path.join(subdir, file)
                df = pd.read_csv(measurement_file,delimiter=',',header=0)
                data_json = json.loads(df.to_json(orient='records'))
                logging.insert(data_json)
    except Exception as e:
        print(e)

print('Step 1: Preparing the scheduling text files')
relation_info = 'central_input/nodes.txt'
pairs_info = 'central_input/link_list.txt'
df_rel = pd.read_csv(relation_info, header=0, delimiter=',',index_col=0)
dict_rel = df_rel.T.to_dict('list')
# Output files
scheduling_folder = 'scheduling'
if not os.path.exists(scheduling_folder):
    os.makedirs(scheduling_folder)
output_file = 'scheduling.txt'

df_links = pd.read_csv(pairs_info, header=0)
df_links.replace('(^\s+|\s+$)', '', regex=True, inplace=True)

for cur_node, row in df_rel.iterrows():
    cur_schedule = os.path.join(scheduling_folder,dict_rel.get(cur_node)[0])
    if not os.path.exists(cur_schedule):
        os.makedirs(cur_schedule)
    temp = df_links.loc[df_links['Source']==cur_node]
    temp = pd.merge(temp, df_rel, left_on = 'Destination', right_index = True, how = 'inner')
    temp_schedule = pd.DataFrame(columns=['Node','Region'])
    temp_schedule=temp_schedule.append({'Node':dict_rel.get(cur_node)[0],'Region':row['Region']},ignore_index=True)
    temp_schedule=temp_schedule.append(temp[['Node','Region']],ignore_index=False)
    temp_schedule.to_csv(os.path.join(cur_schedule,output_file),header=False,index=False)

print('Step 2: Create the central database ')
client = MongoClient('mongodb://localhost:27017/')
db = client['central_network_profiler']
buffer_size = len(df_links.index)*100
db.create_collection('quadratic_parameters', capped=True, size=1000000, max=buffer_size)

print('Step 3: Copying files and network scripts to the droplets ')
bash_script = os.path.join(os.getcwd(),'central_copy_nodes')
proc = subprocess.Popen(bash_script,shell = True,stdout=subprocess.PIPE)

print('Step 4: Scheduling updating the central database')
parameters_folder = 'parameters'
if not os.path.exists(parameters_folder):
    os.makedirs(parameters_folder)

sched = BackgroundScheduler()
sched.add_job(do_update_quadratic,'interval', id='update',minutes=10,replace_existing=True)
sched.start()
while True:
    time.sleep(10)
#sched.shutdown()


