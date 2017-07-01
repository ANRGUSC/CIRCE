"""
 ** Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 **     contributor: Quynh Nguyen, Bhaskar Krishnamachari
 **     Read license file in main directory for more details
"""

import random
import subprocess
import decimal
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import os
import csv
import paramiko
from scp import SCPClient
from pymongo import MongoClient
import datetime
import pandas as pd
import numpy as np
from pymongo import MongoClient
import time
import stat


class droplet_measurement():
    def __init__(self):
        self.file_size = [1,10,100,1000,10000]#K =1024
        self.dir_local = '../generated_test'
        self.dir_remote = 'online_profiler/received_test'
        self.my_host =  None
        self.my_region = None
        self.hosts = []
        self.usernames = []
        self.passwords = []
        self.regions = []
        self.client_mongo = None
        self.db = None
        self.scheduling_file = '../scheduling.txt'
        self.measurement_script = os.path.join(os.getcwd(),'droplet_scp_time_transfer')


    def do_add_host(self):
        """add_host
        Add the host to the host list"""
        if self.scheduling_file:
            with open(self.scheduling_file, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                header = next(reader, None)
                self.my_host = header[0].split('@')[1]
                self.my_region = header[1]
                for row in reader:
                    self.hosts.append(row[0].split('@')[1])
                    self.regions.append(row[1])
                    self.usernames.append(row[0].split('@')[0])
                    self.passwords.append(row[2])
        else:
            print("No detected droplets information... ")

    def do_log_measurement(self):
        self.client_mongo = MongoClient('mongodb://localhost:27017/')
        self.db = self.client_mongo.droplet_network_profiler

        for idx in range(0,len(self.hosts)):
            random_size = random.choice(self.file_size)
            local_path = '%s/%s_test_%dK'%(self.dir_local,self.my_host,random_size)
            remote_path = '%s'%(self.dir_remote)
            # print('---BASH---')
            # print(random_size)
            bash_script = self.measurement_script + " "+self.usernames[idx]+"@"+self.hosts[idx] + \
                          " " + self.passwords[idx] + " "+ str(random_size)
            proc = subprocess.Popen(bash_script,shell = True,stdout=subprocess.PIPE)
            tmp = proc.stdout.read().strip().decode("utf-8")
            results = tmp.split(" ")[1]
            # print(results)
            m = float(results.split("m")[0]) #minute
            s = float(results.split("m")[1][:-1]) #second
            elapsed=m*60+s
            # print(elapsed)
            cur_time = datetime.datetime.utcnow()
            logging = self.db[self.hosts[idx]]
            new_log = {"Source[IP]":self.my_host,"Source[Reg]":self.my_region,"Destination[IP]":self.hosts[idx],
                        "Destination[Reg]":self.regions[idx],'Time_Stamp[UTC]':cur_time,
                       'File_Size[KB]':random_size,'Transfer_Time[s]':elapsed}
            log_id = logging.insert_one(new_log).inserted_id
            # print(log_id)



class droplet_regression():
    def __init__(self):
        self.client_mongo = None
        self.db = None
        self.my_host =  None
        self.my_region = None
        self.hosts = []
        self.regions = []
        self.usernames = []
        self.passwords = []
        self.parameters_file = None
        self.scheduling_file = '../scheduling.txt'
        self.dir_remote = 'Network_Profiler/parameters'
        with open('../central.txt','r') as f:
            line = f.read().split(' ')
            self.central_IP= line[0]
            self.central_username = line[1]
            self.central_password = line[2]


    def do_add_host(self):
        """add_host
        Add the host to the host list"""

        if self.scheduling_file:
            with open(self.scheduling_file, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                header = next(reader, None)
                self.my_host = header[0].split('@')[1]
                self.my_region = header[1]
                self.parameters_file = '../parameters_%s.csv'%(self.my_host)
                for row in reader:
                    self.hosts.append(row[0].split('@')[1])
                    self.regions.append(row[1])
                    self.usernames.append(row[0].split('@')[0])
                    self.passwords.append(row[2])
            #print(self.hosts)
        else:
            print("No detected droplets information... ")


    def do_regression(self):
        self.client_mongo = MongoClient('mongodb://localhost:27017/')
        self.db = self.client_mongo.droplet_network_profiler
        regression = self.db[self.my_host]
        reg_cols = ['Source[IP]','Source[Reg]','Destination[IP]','Destination[Reg]','Time_Stamp[UTC]','Parameters']
        reg_data = []
        reg_data.append(reg_cols)

        for idx in range(0,len(self.hosts)):
            host = self.hosts[idx]
            logging = self.db[host]
            cursor = logging.find({})
            df =  pd.DataFrame(list(cursor))

            df['X'] = df['File_Size[KB]']* 8 #Kbits
            df['Y'] = df['Transfer_Time[s]']*1000 #ms

            # Quadratic prediction
            quadratic = np.polyfit(df['X'],df['Y'],2)
            parameters = " ".join(str(x) for x in quadratic)
            cur_time = datetime.datetime.utcnow()
            # print('==============')
            # print(parameters)

            new_reg = {"Source[IP]":self.my_host,"Source[Reg]":self.my_region,"Destination[IP]":self.hosts[idx],
                        "Destination[Reg]":self.regions[idx],'Time_Stamp[UTC]':cur_time,
                      'Parameters':parameters}
            reg_id = regression.insert_one(new_reg).inserted_id
            #print(reg_id)
            temp = [self.my_host,self.my_region,self.hosts[idx],self.regions[idx],str(cur_time),parameters]
            reg_data.append(temp)
        # Write parameters into text file
        with open(self.parameters_file, "w") as f:
            writer = csv.writer(f)
            writer.writerows(reg_data)

    def do_send_parameters(self):
        # Sending information to central node
        local_path = self.parameters_file
        remote_path = '%s'%(self.dir_remote)
        copy_script = os.path.join(os.getcwd(),"droplet_copy_central")
        bash_script = copy_script + " "+ local_path+ " "+ self.central_IP+" "+ remote_path+ " "+self.central_password
        st = os.stat(copy_script)
        os.chmod(copy_script, st.st_mode | stat.S_IEXEC)
        proc = subprocess.Popen(bash_script,shell = True,stdout=subprocess.PIPE)
        # client = paramiko.SSHClient()
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.connect(central_IP, username=self.username,password=self.password)
        # local_path = self.parameters_file
        # remote_path = '%s'%(self.dir_remote)
        # scp = SCPClient(client.get_transport())
        # scp.put(local_path, remote_path)
        # scp.close()


def prepare_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['droplet_network_profiler']
    with open('../scheduling.txt', 'r') as f:
        first_line = f.readline()
        account, region, password = first_line.split(',')
        ip = account.split('@')[1]
        db.create_collection(ip)
    with open('../scheduling.txt', 'r') as f:
        next(f)
        for line in f:
            account, region, password = line.split(',')
            ip = account.split('@')[1]
            db.create_collection(ip, capped=True, size=10000, max=10)

def regression_job():
    print('Log regression every 10 minute....')
    d = droplet_regression()
    d.do_add_host()
    d.do_regression()
    d.do_send_parameters()
def measurement_job():
    print('Log measurement every minute....')
    d = droplet_measurement()
    d.do_add_host()
    d.do_log_measurement()

if __name__ == '__main__':
    print('Step 1: generating files of random sizes')
    bash_script = os.path.join(os.getcwd(),'droplet_generate_random_files')
    proc = subprocess.Popen(bash_script,shell = True,stdout=subprocess.PIPE)

    print('Step 2: Prepare the database')
    prepare_database()

    sched = BackgroundScheduler()
    sched.start()
    print('Step 3: Scheduling measurement job')
    sched.add_job(measurement_job,'interval',id='measurement', minutes=1,replace_existing=True)

    print('Step 4: Scheduling regression job')
    sched.add_job(regression_job,'interval', id='regression', minutes=10, replace_existing=True)

    print('Step 5: Start the schedulers')

    while True:
        time.sleep(10)
    sched.shutdown()