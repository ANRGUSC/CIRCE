
* Input:
- central.txt: central_IP central_user central_pwd
- link_list.txt :
    Source Destination
    node1,node2
    node1,node3
    node2,node1
    ...

* Output: folder scheduling

1. central_schduler.py: scheduling file for each node in scheduling folder according to the following format:
- Row 0: Its own account, its region
- Row 1-end: Other accounts, corresponding regions

2. central_copy_nodes: scp to each node: OK!
- droplet_init: install required libraries & generate necessary folders
- scheduling.txt, central.txt,iperf.txt for each node
- generate_random_file script
- node/index.js : generate mongoDB database and collections
- measurement script
- regression script


# At each node
1. droplet_init: nstall required libraries & generate necessary folders

2. measurement
    - droplet_measurement.py (monotonic)
    - set up MongoDB, install pymongo : node.js
    - log transfer time to Mongodb
    - each node: MongoDB - DB "droplet_network_profiler" - each link is a capped_collection (Source IP, Destination IP, time_stamp UTC, file_size KB, time transfer seconds )
    - MongoDB & preparation: npm install mongodb, node index.js : generate new collections for each of the neighboring nodes: index.js (run everytime having a new scheduling file)

3. regression:
    - droplet_regression.py OK
    - each node: MongoDB - Collection "its_IP" for regression, parameters (Source IP, Destination IP, time_stamp UTC, file_size KB, Parameters)

4. crontab file : droplet_crontab
    + measurement every minute
    + regression every kth minute

5. Central processing
    - write parameters as text files, scp the file to the central node
    - update local mongodb server at central node (quadratic_parameters of DB central_network_profiler) every k minutes: central_update_mongo.py
    - update iperf information manually from text file (iperf of DB central_network_profiler) OK
    - central_query_statistics.py: query script the local database server, and return the expected latency for a given pair of droplets and file size
      Ex:   python central_query_statistics.py node1 node2 10

USER GUIDE (CENTRAL)

1. ./central_init : create folders & install required libraries
2. Modify central_input files (droplets and link information) => python central_scheduler.py: run scheduling code
3. ./central_copy_nodes: copy scripts and scheduling text files to droplets
4. crontab file to run central_update_mongo.py every kth minute: update new parameters into mongodb central database
5. python central_query_statistics.py SOURCE DESTINATION FILE_SIZE: return expected latency for a given pair of droplets and file size



USER GUIDE (DROPLETS)

1. ./droplet_init : create folders & install required librarie
2. ./droplet_generate_random_files : generate random files
3. python droplet_database.py: prepare MongoDB database
3. crontab file to run droplet_measurement.py every minute: time the transfer file procedure (scp)
4. crontab file to run droplet_regression.py every kth minute: calculate parameters for k measurement information using quaratic regression









