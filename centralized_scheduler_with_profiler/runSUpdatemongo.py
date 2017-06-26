# run cron jobs every kth minute
import os
import csv
from pymongo import MongoClient
import pandas as pd
import json



#Update scheduler runtime folder information in mongodb


client_mongo = MongoClient('mongodb://localhost:27017/')
db = client_mongo.central_task_runtime_profiler
logging = db['droplet_runtime']
runtime_folder = "runtime"
try:
    for subdir, dirs, files in os.walk(runtime_folder):
        for file in files:
            if file.startswith('.'): continue
            runtime_file = os.path.join(subdir, file)
            df = pd.read_csv(runtime_file,delimiter=',',header=None,names = ["Type", "Node IP","Task Name","File Name", "Time","File Size"])
            data_json = json.loads(df.to_json(orient='records'))
            logging.insert(data_json)
except Exception as e:
    print('MongoDB error')
    print(e)

