import threading
import time
import os
import json
from os.path import expanduser

from kafka import KafkaProducer


class Producer:

    def __init__(self, brokerList, topic = "default-topic"):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.runLock = False
        self.bootstrapServerList = brokerList
        self.myTopic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrapServerList)

    def stop(self):
        self.stop_event.set()

    def releaseRunLock(self):
        self.runLock = 0

    def changeToTopic(self, newTopic):
        self.myTopic = newTopic

    def send(self, msg):
        bmsg = bytes(msg, 'utf-8')
        self.producer.send(self.myTopic, bmsg)
    


def main():
    kafkaBrokerList = ["152.46.17.189:9092","152.46.17.100:9092","152.46.16.167:9092"]
    topicName = "VideoSubtitles"
    dataLoader = Producer(kafkaBrokerList,topicName)

    home = expanduser("~") 
    print(home)   
    textpath = home+'/text/'
    metapath = home+'/videoJson/'

    for file in os.listdir(textpath):
        try:
            loadObject = {}
            if file.endswith(".txt"):
                abspath = textpath+file
                with open(abspath) as f:
                    parsed = f.read()       #json.load(f)
                
                with open(metapath+file.split('.txt')[0]+'.json', 'r') as f:
                    meta = json.load(f)

                loadObject['meta'] = meta
                loadObject['extract'] = parsed
                
                re = repr(loadObject)     # converts dictionary to string
                #now = json.loads(re)       $ viceversa string to dictionary
                print("sending data to kafka"+str(file))
                dataLoader.send(re)

        except Exception as e:
            print("No files found here!")
            raise e




if __name__ == "__main__":
    main()
