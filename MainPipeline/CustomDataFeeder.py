import threading
import time
import os
import json
import re
import shutil
#reload(sys)
#sys.setdefaultencoding('utf-8')

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
#        temp = bmsg.decode('utf-8')
#        temp2 = json.loads(temp.replace("'",'"'))
#        print(temp2)
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
                print(abspath)
                with open(abspath, 'r', encoding="utf-8") as f:
                    parsed = f.read()       #json.load(f)
                
                with open(metapath+file.split('.txt')[0]+'.json', 'r') as f:
                    meta = json.load(f)

                loadObject['meta'] = meta
                loadObject['extract'] = re.sub("[^a-zA-Z\s\n]", "", parsed)	#regex to retain just a-zA-Z and spaces in parsed string, to remove ',"
                
                red = repr(loadObject)     # converts dictionary to string
                #now = json.loads(re)       $ viceversa string to dictionary
                print("sending data to kafka"+str(file))
                dataLoader.send(red)
                textdir = "rm -r "+home+"/text/"+file
                os.system(textdir)
        except Exception as e:
            print("No files found here!")
            raise e

    #textdir = "rm -R "+home+"/text/"     
    # s.system(textdir) #shutil.rmtree(home+"/text") 



if __name__ == "__main__":
    main()
