from pyspark.sql import SparkSession
from pyspark import *
from random import random
sparkSess = SparkSession \
        .builder \
        .appName("PythonPi") \
        .getOrCreate()
sc = sparkSess.sparkContext

#conf = SparkConf().setAppName("TopicModeling").setMaster('spark://152.7.99.47:7077').set("spark.executor.memory", "500M").set("spark.cores.max","1")

#sc = SparkContext(conf = conf)