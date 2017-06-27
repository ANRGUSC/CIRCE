import platform
import datetime
import time
import os
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pymongo import MongoClient
import pandas as pd
import json

#Update scheduler output folder information in mongodb
class Watcher:
    DIRECTORY_TO_WATCH = os.getcwd()+'/output'

    def __init__(self):
        self.observer = Observer()


    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':

            print("Received file as output - %s." % event.src_path)
            new_file_name = os.path.split(event.src_path)[-1]

            if platform.system() == 'Windows':
                print(os.path.getctime(event.src_path))
            else:
                stat = os.stat(event.src_path)
                try:
                    print(stat.st_birthtime)
                except AttributeError:
                    print('Linux...')
                    # We're probably on Linux. No easy way to get creation dates here,
                    # so we'll settle for when its content was last modified.
                    created_time=datetime.datetime.fromtimestamp(stat.st_mtime)

                    record = {'File Name':event.src_path,'Created Time':created_time}
                    print(record)
                    client_mongo = MongoClient('mongodb://localhost:27017/')
                    db = client_mongo.central_task_runtime_profiler
                    logging = db['scheduler_output']
                    post_id = logging.insert_one(record).inserted_id
                    print(post_id)

if __name__ == '__main__':
    w = Watcher()
    w.run()
