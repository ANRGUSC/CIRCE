import paramiko
import os

def connect(IPaddr, user, passwrd):


    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IPaddr, username=user, password=passwrd)
    ssh.exec_command("pkill -f centralized_scheduler")
    ssh.exec_command("rm out_info.txt")
    ssh.exec_command("rm -rf centralized_scheduler/")
    ssh.close()


IP=['162.243.19.184','107.170.77.194','165.227.141.81','104.131.133.156','128.199.253.181','139.59.58.153','178.62.94.150',
'37.139.9.234','165.227.15.16','178.62.214.132','139.59.24.161','46.101.29.130','95.85.44.221','138.68.43.235']
users = 'apac'
passwords='apac20!7'
for i in range(0, len(IP)):
        print(IP[i])
        connect(IP[i], users, passwords)

os.system('pkill -f scheduler')
