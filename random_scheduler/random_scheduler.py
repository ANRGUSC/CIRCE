import random

tasks=[]
node_num=14

with open("../dag_security.txt", "r") as input_file:
    num = input_file.readline().strip()
    for line in input_file:
        tasks.append(line.strip().split(" ")[0])



random.seed()
with open("../configuration_random.txt", 'a') as output: 
    for i in range(0, len(tasks)):
        node = random.randint(1, node_num)
        output.write(tasks[i]+" "+"node"+str(node)+"\n")

