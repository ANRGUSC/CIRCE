import pandas as pd
import os
from pymongo import MongoClient
import pandas as pd

# Input files

relation_info = 'central_input/nodes.txt'
pairs_info = 'central_input/link_list.txt'
df_rel = pd.read_csv(relation_info, header=0, delimiter=',',index_col=0)
dict_rel = df_rel.T.to_dict('list')
# Output files
scheduling_folder = 'scheduling'
if not os.path.exists(scheduling_folder):
    os.makedirs(scheduling_folder)
output_file = 'scheduling.txt'

df_links = pd.read_csv(pairs_info, header=0)


df_links.replace('(^\s+|\s+$)', '', regex=True, inplace=True)

for cur_node, row in df_rel.iterrows():
    cur_schedule = os.path.join(scheduling_folder,dict_rel.get(cur_node)[0])
    if not os.path.exists(cur_schedule):
        os.makedirs(cur_schedule)
    temp = df_links.loc[df_links['Source']==cur_node]
    temp = pd.merge(temp, df_rel, left_on = 'Destination', right_index = True, how = 'inner')
    temp_schedule = pd.DataFrame(columns=['Node','Region'])
    temp_schedule=temp_schedule.append({'Node':dict_rel.get(cur_node)[0],'Region':row['Region']},ignore_index=True)
    temp_schedule=temp_schedule.append(temp[['Node','Region']],ignore_index=False)
    temp_schedule.to_csv(os.path.join(cur_schedule,output_file),header=False,index=False)

print('Create the central database')
client = MongoClient('mongodb://localhost:27017/')
db = client['central_network_profiler']
buffer_size = len(df_links.index)*100
db.create_collection('quadratic_parameters', capped=True, size=10000, max=buffer_size)

