∗ USER GUIDE AT CENTRAL NETWORK PROFILER:
1. run the command ./central init to install required libraries
2. inside the folder central input add information about the
nodes and the links.
3. python3 central scheduler.py to generate the scheduling
files for each node, prepare the central database and collection,
copy the scheduling information and network scripts
for each node in the node list and schedule updating the
central database every 10th minute.

∗ USER GUIDE AT OTHER DROPLETS:
1. The central network profiler copied all required scheduling
files and network scripts to the folder online profiler in each
droplet.
2. run the command ./droplet init to install required libraries
3. run the command python3 automate droplet.py to generate
files with different sizes to prepare for the logging measurements,
generate the droplet database, schedule logging
measurement every minute and logging regression every 10th
minute