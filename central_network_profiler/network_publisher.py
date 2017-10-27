# On server: mosquitto_sub -h localhost -t topic/network -u 'apac' -P 'apac20!7' &
import paho.mqtt.client as mqtt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from os import path
import time
import pandas as pd
import json


client = mqtt.Client()
MQTT_Username = "apac"
MQTT_Password = "apac20!7"
client.username_pw_set(MQTT_Username, MQTT_Password)
client.connect("localhost",1883,60)
client.loop_start()

class Watcher():
    DIRECTORY_TO_WATCH = os.getcwd()+'/parameters2'

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

        elif event.event_type == 'created' or event.event_type == 'modified':
            print("Received file as output - %s." % event.src_path)
            parameter_file = event.src_path
            df = pd.read_csv(parameter_file,delimiter=',',header=0)
            data_json = df.to_json(orient='records')
            try:
                #client.publish("topic/network", parameter_file);
                client.publish("topic/network", data_json);
            except:
                print('Error publish')

if __name__ == '__main__':
    #monitor parameters folder
    w1=Watcher()
    w1.run()
    client.loop_stop()
    client.disconnect()
