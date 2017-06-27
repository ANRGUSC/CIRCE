import os
import csv
import paramiko
from scp import SCPClient
from pymongo import MongoClient
import datetime
import pandas as pd
import numpy as np

class droplet_regression():
    def __init__(self):
        self.client_mongo = None
        self.db = None
        self.my_host =  None
        self.my_region = None
        self.hosts = []
        self.regions = []
        self.parameters_file = None
        self.dir_remote = 'central_network_profiler/parameters'
        with open('../central.txt','r') as f:
            line = f.read().split(' ')
            self.central_IP= line[0]
            self.username = line[1]
            self.password = line[2]


    def do_add_host(self, file_hosts):
        """add_host
        Add the host to the host list"""
        if file_hosts:
            with open(file_hosts, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                header = next(reader, None)
                self.my_host = header[0].split('@')[1]
                self.my_region = header[1]
                self.parameters_file = '../parameters_%s.csv'%(self.my_host)
                for row in reader:
                    self.hosts.append(row[0].split('@')[1])
                    self.regions.append(row[1])
            print(self.hosts)
        else:
            print("No detected droplets information... ")

    # def send_regression(self):


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
            print(parameters)

            new_reg = {"Source[IP]":self.my_host,"Source[Reg]":self.my_region,"Destination[IP]":self.hosts[idx],
                        "Destination[Reg]":self.regions[idx],'Time_Stamp[UTC]':cur_time,
                      'Parameters':parameters}
            reg_id = regression.insert_one(new_reg).inserted_id
            temp = [self.my_host,self.my_region,self.hosts[idx],self.regions[idx],str(cur_time),parameters]
            reg_data.append(temp)
        # Write parameters into text file
        with open(self.parameters_file, "w") as f:
            writer = csv.writer(f)
            writer.writerows(reg_data)

    def do_send_parameters(self,central_IP):
        # Sending information to central node
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(central_IP, username=self.username,password=self.password)
        local_path = self.parameters_file
        remote_path = '%s'%(self.dir_remote)
        scp = SCPClient(client.get_transport())
        scp.put(local_path, remote_path)
        scp.close()

if __name__ == '__main__':
    d = droplet_regression()
    scheduling_file = '../scheduling.txt'
    d.do_add_host(scheduling_file)
    d.do_regression()
    d.do_send_parameters(d.central_IP)