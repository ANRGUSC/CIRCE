# CIRCE - CentralIzed Runtime sChedulEr

# Introduction

CIRCE is a runtime scheduling software tool for dispersed computing, which can deploys pipelined  
computations described in the form a directed acyclic graph (DAG) on multiple geographically
dispersed computers (nodes or droplets).

The tool is run on a host node (also called scheduler node). The tool needs information about
which nodes are available for computation, the description of the DAG along with code for 
the corresponding tasks, and based on measurements of compute costs for each task on each 
node and the communication cost of transferring data from one node to another, first uses a 
DAG-based scheduling algorithm (at present, we include a modified version of an implementation [2] 
of the well-known HEFT algorithm [1] with the tool) to determine
at which node to place each task from the DAG. CIRCE then deploys the corresponding tasks to each 
node and executes each task, using input and output queues for each task for pipelined execution
and taking care of the data transfer between different nodes.

List of nodes (droplets) for the experiment, including the scheduler node, is
kept in file nodes.txt (the user needs to fill the file with the appropriate IP addresses,
usernames and passwords of their servers):

| scheduler | IP |username | pw |
| ------ |----|--|-- |
| node1 | IP| username |pw |
| node2 | IP| username| pw |
| node3  | IP |username |pw |

DAG description (as adjacency list) is kept in file dag.txt:

| task1 task2 task3 |
| ------ |
| task2 task4 |
| task3 task4 |
| task4 scheduler  |

The running example given above is a four task DAG:

| task1 -> task2, task3 |
| ------ |
| task2 -> task4 |
| task3 ->  task4 |
| task4 ->  scheduler  |

The last line tells that the ‘childless task’ (task4) should send its output to
the scheduler node. The other lines list the child tasks after the arrow.

# User Guide
The system consists of several tools and requires the following steps:
  
- PROFILING:
  - Execution profiler: produces profiler_nodeX.txt file for each node,
    which gives the execution time of each task on that node and the
    amount of data it passes to its child tasks. These results are required
    in the next step for HEFT algorithm.
    - INPUT: dag.txt, nodes.txt, DAG task files (task1.py, task2.py,. . . ), DAG input file (input.txt)
    - OUTPUT: profiler_nodeNUM.txt
    - USER GUIDE: There are two ways to run the execution profiler:
        1. copy the app/ folder to the each of the nodes using scp and
           inside app/ folder perform the following commands:
           ```sh
           $ docker build –t profilerimage .
           $ docker run –h hostname profilerimage
           ```
           where hostname is the name of the node (node1, node2, etc.,..).
        2. inside circe/docker_execution_profiler/ folder
           perform the following command:
           ```sh
           $ python3 scheduler.py
           ```
           In this case, the file scheduler.py will copy the app/ folder
           to each of the nodes and execute the docker commands.
           In both cases make sure that the command inside file app/start.sh
           gives the details (IP, username and password) of your scheduler machine.
  - Central network profiler: automatically scheduling and logs com-
    munication information of all links betweet nodes in the network,
    which gives the quaratic regression parameters of each link repre-
    senting the corresponding communication cost. These results are
    required in the next step for HEFT algorithm.
    - INPUT: central.txt stores credential information of the central node:
        IP username pw 
        nodes.txt stores credential information of the nodes information:
        
        | Tag,Node,Region |
        |--------|
        | node1,username1@IP1,region1 |
        | node2,username2@IP2,region2 |
        | node3,username3@IP3,region3 |
        
        link list.txt stores the the links between nodes required to log
        the communication.
        
        | Source,Destination |
        |------|
        | node1,node2 |
        | node1,node3 |
        | node2,node1 |
        | node2,node3 |
        | node3,node1 |
        | node3,node2 |
        
    - OUTPUT: all quadratic regression parameters are stored in the
        local MongoDB on the central node.
    - USER GUIDE AT CENTRAL NETWORK PROFILER:
            1. run the command ./central init to install required libraries
            2. inside the folder central input add information about the
            nodes and the links.
            3. python3 central scheduler.py to generate the schedul-
            ing files for each node, prepare the central database and col-
            lection, copy the scheduling information and network scripts
            for each node in the node list and schedule updating the
            central database every 10th minute.  
    - USER GUIDE AT OTHER DROPLETS:
        1. The central network profiler copied all required scheduling
            files and network scripts to the folder online profiler in each
            droplet.
        2. run the command ./droplet init to install required libraries
        3. run the command python3 automate droplet.py to gen-
           erate files with different sizes to prepare for the logging mea-
           surements, generate the droplet database, schedule logging
           measurement every minute and logging regression every 10th
           minute.
  - System resource profiler:This tool will get system utilization from
    node 1, node 2 and node 3. Then these information will be sent to
    scheduler node and stored into mongoDB.The information includes:
    IP address of each node, cpu utilization of each node, memory uti-
    lization of each node, and the latest update time.
    - USER GUIDE:
      For working nodes: copy the mongo script/ folder to each
      working node using scp. In each node, type:
      ```sh
      $ python2 mongo script/install package.py
      $ python2 mongo script/server.py
      ```
      For scheduler node: copy mongo control/ folder to scheduler node using scp under circe/central_network profiler if a node’s IP address changes, just update the mongo control/ip path file inside apac scheduler/central network profiler/mongo control/ folder, type: python2 install package.py
            python2 jobs.py (if you want to run in backend, type: python2 jobs.py and then close the                terminal)
            
- HEFT (adapted/modified from [2])
  - HEFT input file construction: HEFT implementation takes a file of .tgff format, which describes the DAG and its various costs, as input. The first step is to construct this file.
    - INPUT: dag.txt, profiler_nodeNUM.txt
    - OUTPUT: input.tgff
    - USER GUIDE: from circe/heft/ folder execute:
    ```sh
     $ python write_input_file.py
    ```
  - HEFT algorithm. This is the scheduling algorithm which decides
    where to run each task. It writes its output in a configuration file,
    needed in the next step by the run-time centralized scheduler.
    - INPUT: input.tgff
    - OUTPUT: configuration.txt
    - USER GUIDE: from circe/heft/ run:
    ```sh
    $ python main.py
    ```

- CENTRALIZED SCHEDULER WITH PROFILER
  - Centralized run-time scheduler. This is the run-time scheduler. It takes the
    configuration file, given by HEFT, and orchestrates the execution of
    tasks on given nodes.
    - INPUT: configuration.txt, nodes.txt
    - OUTPUT: DAG output files appear in circe/centralized_scheduler/output/ folder
    - USER GUIDE: inside circe/centralized_scheduler/ folder run:
    ```sh
    $ python3 scheduler.py
    ```
    wait several seconds and move input1.txt to apac scheduler/centralized_scheduler/input/
    folder (repeat the same for other input files).
  - Run-time task profiler
        
        
# Project Structure 

It is assumed that the folder circe/ is located on the users home path
(for example: /home/apac). The structure of the project within circe/
folder is the following:

- nodes.txt
- dag.txt
- configuration.txt (output of the HEFT algorithm)
- profiler node1.txt, profiler node2.txt,... (output of execution profiler)
- docker_execution_profiler/
    - scheduler.py
    - app/
        - dag.txt
        - requirements.txt
        - Dockerfile
        - DAG task files (task1.py, task2.py,...)
        - DAG input file (input1.txt)
        - start.sh
        - profiler.py
- centralized scheduler with profiler/
    - input/ (this folder should be created by user)
    - output/ (this folder should be created by user)
    - input1.txt
    - scheduler.py
    - monitor.py
    - DAG task files (task1.py, task2.py,...)
    - nodes.txt
    - read config.txt
- heft/
    - write_input_file.py
    - heft_dup.py
    - main.py
    - create_input.py
    - cpop.py
    - read config.py
    - input.tgff (output of write input file.py)
    - readme.md
- central network profiler/
    - folder central_input: link list.txt, nodes.txt, central.txt
    - central copy nodes
    - central init
    - central query statistics.py
    - central scheduler.py
    - folder network script: automate droplet.py, droplet generate random files, droplet init, droplet scp time transfer
    - folder mongo control
        - mongo scrip/
          - server.py
          - install package.py
        - mongo control/
          - insert to mongo.py
          - read info.py
          - read info.pyc
          - install package.py
          - jobs.py
          - ip path

Note that while we currently use an implementation of HEFT for use with CIRCE, other schedulers may be used as well. 

# References
[1] H. Topcuoglu, S. Hariri, M.Y. Wu, Performance-Effective and Low-Complexity Task
Scheduling for Heterogeneous Computing, IEEE Transactions on Parallel and
Distributed Systems, Vol. 13, No. 3, pp. 260 - 274, 2002.
[2] Ouyang Liduo, HEFT Implementation Original Source Code, https://github.com/oyld/heft  (we have modified this code in ours.)
            
