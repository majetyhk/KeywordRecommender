import threading
import time

from kafka import KafkaProducer


class Producer(threading.Thread):

    def __init__(self, brokerList, topic = "default-topic"):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.runLock = False
        self.bootstrapServerList = brokerList
        self.myTopic = topic

    def stop(self):
        self.stop_event.set()

    def releaseRunLock(self):
        self.runLock = 0

    def changeToTopic(self, newTopic):
        self.myTopic = newTopic

    def run(self):
        producer = KafkaProducer(bootstrap_servers=self.bootstrapServerList)
        while not self.stop_event.is_set() and self.runLock<5:
            producer.send(self.myTopic, b"test")
            producer.send(self.myTopic, b"\xc2Hola, mundo!")
            self.runLock += 1
            time.sleep(1)

        producer.close()


def main():
    kafkaBrokerList = ["152.46.17.189:9092","152.46.17.100:9092","152.46.16.167:9092"]
    topicName = "SampleTestTopic"
    dataLoader = Producer(kafkaBrokerList,topicName)
    repeat = True
    try:
        inp = input("Enter any key to Produce messages(Type 'end' to quit): ")
        if inp == 'end':
            repeat = False
        else:
            dataLoader.start()
    except:
        print("Invalid Input/Error Occurred\nExiting...!")

    while repeat:
        try:
            inp = input("Enter 'm' key to Produce more messages(Type 'c' to change topic and 'end' to quit): ")
            if inp == 'end':
                repeat = False
                dataLoader.stop()
                dataLoader.join()
            elif inp == 'c':
                newTopic = input("Enter new topic name")
                dataLoader.changeToTopic(newTopic)
            elif inp == 'm':
                dataLoader.releaseRunLock()
        except KeyboardInterrupt:
            repeat = False
            dataLoader.stop()
            dataLoader.join()
        except:
            print("Invalid Input/Error Occurred\nExiting...!")
            repeat = False
            dataLoader.stop()
            dataLoader.join()
    # time.sleep(10)



if __name__ == "__main__":
    main()
