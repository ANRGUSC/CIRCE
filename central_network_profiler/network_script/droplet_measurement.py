import paramiko
import os
import csv
from scp import SCPClient
import random
from monotonic import monotonic
from timeit import default_timer as timer
import time
from pymongo import MongoClient
import datetime
import pandas as pd
import decimal
import subprocess

class droplet_measurement():
    def __init__(self):
        self.username = 'apac'
        self.password = 'apac20!7'
        self.file_size = [1,10,100,1000,10000]#K =1024
        self.dir_local = '../generated_test'
        self.dir_remote = 'online_profiler/received_test'
        self.my_host =  None
        self.my_region = None
        self.hosts = []
        self.regions = []
        self.client_mongo = None
        self.db = None
        self.scheduling_file = '../scheduling.txt'
        self.measurement_script = os.path.join(os.getcwd(),'droplet_scp_time_transfer')


    def do_add_host(self, file_hosts):
        """add_host
        Add the host to the host list"""
        if file_hosts:
            with open(file_hosts, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                header = next(reader, None)
                self.my_host = header[0].split('@')[1]
                self.my_region = header[1]
                for row in reader:
                    self.hosts.append(row[0].split('@')[1])
                    self.regions.append(row[1])
            print(self.hosts)
        else:
            print("No detected droplets information... ")

    def do_log_measurement(self):
        self.client_mongo = MongoClient('mongodb://localhost:27017/')
        self.db = self.client_mongo.droplet_network_profiler

        for idx in range(0,len(self.hosts)):
            random_size = random.choice(self.file_size)
            local_path = '%s/%s_test_%dK'%(self.dir_local,self.my_host,random_size)
            remote_path = '%s'%(self.dir_remote)
            print('---BASH---')
            print(random_size)
            bash_script = self.measurement_script + " "+self.username+"@"+self.hosts[idx] + " "+ str(random_size)
            proc = subprocess.Popen(bash_script,shell = True,stdout=subprocess.PIPE)
            tmp = proc.stdout.read().strip().decode("utf-8")
            results = tmp.split(" ")[1]
            print(results)
            m = float(results.split("m")[0]) #minute
            s = float(results.split("m")[1][:-1]) #second
            elapsed=m*60+s
            print(elapsed)
            cur_time = datetime.datetime.utcnow()
            logging = self.db[self.hosts[idx]]
            new_log = {"Source[IP]":self.my_host,"Source[Reg]":self.my_region,"Destination[IP]":self.hosts[idx],
                        "Destination[Reg]":self.regions[idx],'Time_Stamp[UTC]':cur_time,
                       'File_Size[KB]':random_size,'Transfer_Time[s]':elapsed}
            log_id = logging.insert_one(new_log).inserted_id
            print(log_id)

if __name__ == '__main__':
    d = droplet_measurement()
    d.do_add_host(d.scheduling_file)
    d.do_log_measurement()
