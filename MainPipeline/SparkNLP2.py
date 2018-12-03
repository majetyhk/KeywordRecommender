from pyspark import *

from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.mllib.linalg import Vectors


if __name__ == "__main__":
    #sc = SparkContext(appName="LatentDirichletAllocationExample")  # SparkContext
    conf = SparkConf().setAppName("LDATrial").setMaster('spark://152.7.99.47:7077')
    sc = SparkContext(conf=conf)

    data = sc.textFile("..\\sample_lda_data.txt")

    # parsedData = data.map(lambda line: Vectors.dense([float(x) for x in line.strip().split(' ')]))
    # # Index documents with unique IDs
    # corpus = parsedData.zipWithIndex().map(lambda x: [x[1], x[0]]).cache()
    #
    # # Cluster the documents into three topics using LDA
    # ldaModel = LDA.train(corpus, k=3)
    #
    # # Output topics. Each is a distribution over words (matching word count vectors)
    # print("Learned topics (as distributions over vocab of " + str(ldaModel.vocabSize())
    #       + " words):")
    # topics = ldaModel.topicsMatrix()
    # for topic in range(3):
    #     print("Topic " + str(topic) + ":")
    #     for word in range(0, ldaModel.vocabSize()):
    #         print(" " + str(topics[word][topic]))
    #
    # # Save and load model
    # ldaModel.save(sc, "target/org/apache/spark/PythonLatentDirichletAllocationExample/LDAModel")
    # sameModel = LDAModel\
    #     .load(sc, "target/org/apache/spark/PythonLatentDirichletAllocationExample/LDAModel")
    # # $example off$

    sc.stop()