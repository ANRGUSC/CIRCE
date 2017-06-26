import os
import csv
from pymongo import MongoClient
import pandas as pd
import json


class central_update_mongo():
    def __init__(self):
        self.client_mongo = None
        self.db = None
        self.parameters_folder='parameters'
    def do_update_quadratic(self):
        self.client_mongo = MongoClient('mongodb://localhost:27017/')
        self.db = self.client_mongo.central_network_profiler
        logging = self.db['quadratic_parameters']
        try:
            for subdir, dirs, files in os.walk(self.parameters_folder):
                for file in files:
                    if file.startswith("."): continue
                    measurement_file = os.path.join(subdir, file)
                    df = pd.read_csv(measurement_file,delimiter=',',header=0)
                    print('--------')
                    print(df)
                    data_json = json.loads(df.to_json(orient='records'))
                    logging.insert(data_json)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    d = central_update_mongo()
    d.do_update_quadratic() #SCP to all the hosts