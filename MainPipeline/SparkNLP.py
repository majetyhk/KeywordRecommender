from pyspark.sql import SparkSession
from pyspark import *
from random import random
#from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.ml.clustering import LDA as newLDA
from pyspark.mllib.linalg import Vectors
sparkSess = SparkSession.builder.appName("PythonPi").getOrCreate()
sc = sparkSess.sparkContext

#conf = SparkConf().setAppName("TopicModeling").setMaster('spark://152.7.99.47:7077').set("spark.executor.memory", "500M").set("spark.cores.max","1")

#sc = SparkContext(conf = conf)

#inpData = sc.textFile("sample_data.txt")
myInp = "Topics correspond to cluster centers, and documents correspond to examples rows in a dataset \nTopics and documents both exist in a feature space, where feature vectors are vectors of word counts bag of words \nRather than estimating a clustering using a traditional distance, LDA uses a function based on a statistical model of how text documents are generated"
inpData = sc.parallelize(myInp)
p2 = inpData.collect()
parsedData = inpData.map(lambda line: [x for x in line.strip().split(' ')])
# Index documents with unique IDs
p3 = parsedData.collect()
#print(p3)
corpus = parsedData.zipWithIndex().map(lambda x: [x[1], x[0]]).cache()
p4 = corpus.collect()
print(p4)
# Cluster the documents into three topics using LDA
ldaModel = LDA.train(corpus, k=3)

# Output topics. Each is a distribution over words (matching word count vectors)
print("Learned topics (as distributions over vocab of " + str(ldaModel.vocabSize())
      + " words):")
topics = ldaModel.topicsMatrix()
for topic in range(3):
    print("Topic " + str(topic) + ":")
    for word in range(0, ldaModel.vocabSize()):
        print(" " + str(topics[word][topic]))

# Save and load model
#ldaModel.save(sc, "target/PythonLatentDirichletAllocationExample/LDAModel")
#sameModel = LDAModel.load(sc, "target/PythonLatentDirichletAllocationExample/LDAModel")
# $example off$

sc.stop()

