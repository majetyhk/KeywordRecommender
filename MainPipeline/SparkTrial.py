
from pyspark.sql import SparkSession
from random import random

if __name__=="__main__":
    #conf = SparkConf().setAppName("TopicModeling").setMaster('spark://152.7.99.47:7077').set("spark.executor.memory", "500M").set("spark.cores.max","1")

    #sc = SparkContext(conf = conf)
    sparkSess = SparkSession \
        .builder \
        .appName("PythonPi") \
        .getOrCreate()
    sc = sparkSess.sparkContext
    def inside(p):
        x, y = random(), random()
        return x*x + y*y < 1

    count = sc.parallelize(range(0, 40000)).filter(inside).count()
    print("Pi is roughly %f" % (4.0 * count /40000))
    sc.stop()



