"""
 * Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Aleksandra Knezevic
 *      Bhaskar Krishnamachari
 *     Read license file in main directory for more details  
"""

import os

def read_config(path1,path2):

    nodes = {}
    node_file = open(path2, "r")
    for line in node_file:
        node_line = line.strip().split(" ")
        nodes.setdefault(node_line[0], [])
        for i in range(1, len(node_line)):
            nodes[node_line[0]].append(node_line[i])
    #print(nodes)

    dag_info=[]
    config_file = open(path1,'r')
    dag_size = int(config_file.readline())

    dag={}
    for i, line in enumerate(config_file, 1):
        dag_line = line.strip().split(" ")
        if i == 1:
            dag_info.append(dag_line[0])
        dag.setdefault(dag_line[0], [])
        for j in range(1,len(dag_line)):
            dag[dag_line[0]].append(dag_line[j])
        if i==dag_size:
            break

    dag_info.append(dag)

    hosts={}
    for line in config_file:
        #get task, node IP, username and password
        myline = line.strip().split(" ")
        hosts.setdefault(myline[0],[])
        for j in range(0,2):
            if j==0:
                hosts[myline[0]].append(myline[j])
            if j==1:
                hosts[myline[0]].append(nodes.get(myline[1])[0])
                hosts[myline[0]].append(nodes.get(myline[1])[1])
                hosts[myline[0]].append(nodes.get(myline[1])[2])

    hosts.setdefault('scheduler',[])
    hosts['scheduler'].append('scheduler')
    hosts['scheduler'].append(nodes.get('scheduler')[0])
    hosts['scheduler'].append(nodes.get('scheduler')[1])
    hosts['scheduler'].append(nodes.get('scheduler')[2])

    dag_info.append(hosts)
    return dag_info














