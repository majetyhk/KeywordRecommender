import pyspark
from pyspark.sql.functions import *
from pyspark.sql import SQLContext, SparkSession, Row
from nltk.corpus import stopwords
import re as re
import os
from pyspark.ml.feature import CountVectorizer , IDF, Tokenizer, StopWordsRemover
from kafka import KafkaConsumer
from pyspark.mllib.linalg import Vector, Vectors
# from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.ml.clustering import LDA as newLDA

# data = sqlContext.read.format("csv").options(header='true', inferschema='true')\
#       .load(os.path.realpath("clothingReviews.csv"))
# reviews = data.filter("'Review Text' IS NOT NULL")['Review Text']
# reviewsRdd = reviews.rdd
#
# tokens = reviewsRdd                                                   \
#     .map( lambda document: document.strip().lower())               \
#     .map( lambda document: re.split(" ", document))          \
#     .map( lambda word: [x for x in word if x.isalpha()])           \
#     .map( lambda word: [x for x in word if len(x) > 3] )           \
#     .map( lambda word: [x for x in word if x not in StopWords])    \
# #     .zipWithIndex()

class SparkInstance:
    def __init__(self,AppName ="NLPApp"):
        self.sparkSess = SparkSession.builder.appName("NLPApp").getOrCreate()
        self.sc = self.sparkSess.sparkContext
        self.sqlContext = SQLContext(self.sc)

    def closeConnection(self):
        self.sc.stop()

class ConsumerInstance():
    def __init__(self, brokerList="localhost:9092", topicList="default-topic"):
        self.bootstrapServerList = brokerList
        self.topics = topicList
        self.Consumer = KafkaConsumer(bootstrap_servers=self.bootstrapServerList,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        self.Consumer.subscribe(self.topics)

    def close(self):
        self.Consumer.close()

    def getKafkaConsumer(self):
        return self.Consumer

def getTopics(sc,sqlContext,inpSubtitles):
    # myInp = "Topics correspond to cluster centers, and documents correspond to examples rows in a dataset \nTopics and documents both exist in a feature space, where feature vectors are vectors of word counts bag of words \nRather than estimating a clustering using a traditional distance, LDA uses a function based on a statistical model of how text documents are generated"
    myInp = inpSubtitles
    inpData = sc.parallelize(myInp.splitlines())
    # myInpSplittedList = inpData.map(lambda x: x.split('\n') )
    # res = myInpSplittedList.collect()
    row_rdd = inpData.map(lambda x: x.split(" ")).map(lambda x: Row(x))
    df = sqlContext.createDataFrame(row_rdd, ['allWords'])
    mainDf = df.withColumn("index", monotonically_increasing_id())

    remover = StopWordsRemover(inputCol="allWords", outputCol="words")
    res = remover.transform(mainDf)
    cv = CountVectorizer(inputCol="words", outputCol="features")
    model = cv.fit(res)  # even df works
    result = model.transform(res)
    result.show(truncate=False)

    idf = IDF(inputCol="features", outputCol="finalFeatures")
    idfModel = idf.fit(result)
    result_tfidf = idfModel.transform(result)
    num_topics = 5
    # lda_model = LDA.train(result_tfidf['index','finalFeatures'],k = num_topics, maxIterations= 100)
    lda_obj = newLDA(featuresCol="finalFeatures", k=3, maxIter=100)
    lda_model = lda_obj.fit(result_tfidf["index", "finalFeatures"])
    lda_model.describeTopics().show()
    topics = lda_model.describeTopics()
    topics_rdd = topics.rdd
    vocab = model.vocabulary
    topicsWordsRdd = topics_rdd.map(lambda x: x['termIndices']).map(lambda x: [vocab[idx] for idx in x])

    topics_words = topicsWordsRdd.collect()
    # for idx, topic in enumerate(topics_words):
    #     print("topic: ", idx)
    #
    #     for word in topic:
    #         print(word + ",", end=" ")
    #     print("----------")
    return topics_words

def getSubsFromMessage(message):
    pass

def main():
    kafkaBrokerList = ["152.46.17.189:9092", "152.46.17.100:9092", "152.46.16.167:9092"]
    topicNameList = ["VideoSubtitles"]
    DataReader = ConsumerInstance(kafkaBrokerList, topicNameList).getKafkaConsumer()
    print("Kafka Cluster Connected")
    sparkInst = SparkInstance()
    print("Spark Cluster Connected")

    try:
        count = 0
        for message in DataReader:
            print(message)
            # topicsWordArrayList = getTopics(sparkInst.sc, sparkInst.sqlContext, message)
            print("\n###################----------###################\n")
            #print(topicsWordArrayList)
    except Exception as e:
        print("Error Occurred: "+str(e))
    finally:
        sparkInst.closeConnection()
        DataReader.close()
        print("Spark and Kafka Connections closed!")

#sc.stop()
#print(res)
#data = []
if __name__ == "__main__":
    main()
