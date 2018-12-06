import time
import multiprocessing

from kafka import KafkaConsumer


class Consumer(multiprocessing.Process):
    def __init__(self, brokerList = ["localhost:9092"], topicList = ["default-topic"]):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.bootstrapServerList = brokerList
        self.topics = topicList

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=self.bootstrapServerList,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe(self.topics)

        while not self.stop_event.is_set():
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break
            print("Press Ctrl+c to stop")

        consumer.close()

def main():
    kafkaBrokerList = ["152.46.17.189:9092", "152.46.17.100:9092", "152.46.16.167:9092"]
    topicNameList = ["VideoSubtitles"]
    DataReader = Consumer(kafkaBrokerList,topicNameList)

    try:
        DataReader.start()
    except KeyboardInterrupt:
        DataReader.stop()
        DataReader.join()

if __name__ == "__main__":
    main()
