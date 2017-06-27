import pymongo
import os
from pymongo import MongoClient

def prepare_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['droplet_network_profiler']
    with open('../scheduling.txt', 'r') as f:
        first_line = f.readline()
        ip, region = first_line.split(',')
        db.create_collection(ip)
    with open('../scheduling.txt', 'r') as f:
        next(f)
        for line in f:
            ip, region = line.split(',')
            db.create_collection(ip, capped=True, size=10000, max=10)

prepare_database()
