import pandas as pd
import itertools

print('Preparing the link list text files')
relation_info = 'central_input/nodes.txt'
pairs_info = 'central_input/link_list.txt'
df_rel = pd.read_csv(relation_info, header=0, delimiter=',',index_col=0)
dict_rel = df_rel.T.to_dict('list')

with open(pairs_info, 'w') as f:
    f.write('Source,Destination\n')
    for pair in itertools.combinations(dict_rel.keys(),2):
        f.write(",".join(pair)+"\n")
        f.write(",".join(pair[::-1])+"\n")