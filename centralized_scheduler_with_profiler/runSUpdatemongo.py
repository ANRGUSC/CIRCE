
import os
import csv
from pymongo import MongoClient
import pandas as pd
import json
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time
import glob


def update_job():
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
                print(runtime_file)
                df = pd.read_csv(runtime_file,delimiter=',',header=None,names = ["Type", "Node IP","Task Name","File Name", "Time","File Size"])
                data_json = json.loads(df.to_json(orient='records'))
                logging.insert(data_json)
        for subdir, dirs, files in os.walk(runtime_folder):
            for file in files:
                runtime_file = os.path.join(subdir, file)
                os.remove(runtime_file)
    except Exception as e:
        print('MongoDB error')
        print(e)

    logging = db['scheduler_runtime']
    runtime_folder = "runtime_total"
    try:
        for subdir, dirs, files in os.walk(runtime_folder):
            for file in files:
                if file.startswith('.'): continue
                runtime_file = os.path.join(subdir, file)
                print(runtime_file)
                df = pd.read_csv(runtime_file,delimiter=',',header=None,names = ["Type","File Name", "Time"])
                data_json = json.loads(df.to_json(orient='records'))
                logging.insert(data_json)
        for subdir, dirs, files in os.walk(runtime_folder):
            for file in files:
                runtime_file = os.path.join(subdir, file)
                os.remove(runtime_file)

    except Exception as e:
        print('MongoDB error')
        print(e)

if __name__ == '__main__':
    sched = BackgroundScheduler()
    print('Scheduling updating mongo droplet at the central scheduler')
    sched.add_job(update_job,'interval',id='update', minutes=10,replace_existing=True)
    sched.start()



    while True:
        time.sleep(10)

