import paramiko
import time, os

node1="104.131.111.58"
node2="139.59.58.153"
node3="207.154.243.148"

def control_node104():

    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(node1 , username="apac", password="apac20!7")
    print "node1 connect successfully!"
    ssh1.exec_command('python2 mongo_script/server.py')
    print "node1 listen at port 5000\n"

def control_node139():

    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect(node2 , username="apac", password="apac20!7")
    print "node2 connect successfully!"
    ssh2.exec_command('python2 mongo_script/server.py') 
    print "node2 listen at port 5000\n"

def control_node207():

    ssh3 = paramiko.SSHClient()
    ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh3.connect(node3 , username="apac", password="apac20!7")
    print "node3 connect successfully!"
    ssh3.exec_command('python2 mongo_script/server.py')
    print "node3 listen at port 5000\n"

def re_exe(cmd, inc = 60):
    while True:
        os.system(cmd)
        time.sleep(inc)


if __name__=="__main__":
    control_node104()
    control_node139()
    control_node207()
    re_exe("python2 insert_to_mongo.py ip_path", 60)
