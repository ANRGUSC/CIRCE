"""
 ** Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 **     contributor: Quynh Nguyen, Bhaskar Krishnamachari
 **     Read license file in main directory for more details
"""

from pymongo import MongoClient
import sys
import read_info

def insert_data(res):

    Client = MongoClient()

    db = Client["droplets_info"]

    coll = db["resource"]

    for i in res:
        info = eval(i)
        j={info.keys()[0]:info.values()[0]}
        coll.update(j,info,upsert=True)   # if not exist then insert, if exsit then update
    print 'insert successfully'


if __name__ == '__main__':
    if  len(sys.argv)!=2:
        print 'Usage:python insert_to_mongo.py ip_path'
        sys.exit(2)
    ip_path = sys.argv[1]
    res=read_info.open_file()
    insert_data(res)
