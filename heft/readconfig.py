import os

def read_config(path):

    dag_info=[]
    config_file = open(path,'r')
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
    return dag_info













