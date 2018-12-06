import pyspark

from pyspark.sql import SQLContext, SparkSession, Row
sparkSess = SparkSession.builder.appName("PythonPi").getOrCreate()
sc = sparkSess.sparkContext
sqlContext = SQLContext(sc)

from nltk.corpus import stopwords
import re as re
import os
from pyspark.ml.feature import CountVectorizer , IDF, Tokenizer

from pyspark.mllib.linalg import Vector, Vectors
#from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.ml.clustering import LDA as newLDA

data = sqlContext.read.format("csv").options(header='true', inferschema='true').load(os.path.realpath("clothingReviews.csv"))
reviews = data.filter("'Review Text' IS NOT NULL")['Review Text']
reviewsRdd = reviews.rdd

tokens = reviewsRdd                                                   \
    .map( lambda document: document.strip().lower())               \
    .map( lambda document: re.split(" ", document))          \
    .map( lambda word: [x for x in word if x.isalpha()])           \
    .map( lambda word: [x for x in word if len(x) > 3] )           \
    .map( lambda word: [x for x in word if x not in StopWords])    \
    .zipWithIndex()

myInp = "Topics correspond to cluster centers, and documents correspond to examples rows in a dataset \nTopics and documents both exist in a feature space, where feature vectors are vectors of word counts bag of words \nRather than estimating a clustering using a traditional distance, LDA uses a function based on a statistical model of how text documents are generated"

inpData = sc.parallelize(myInp.splitlines())
#myInpSplittedList = inpData.map(lambda x: x.split('\n') )
#res = myInpSplittedList.collect()
row_rdd = inpData.map(lambda x:x.split(" ")).map(lambda x: Row(x))
df=sqlContext.createDataFrame(row_rdd,['words'])
res = df.withColumn("index", monotonically_increasing_id())

cv = CountVectorizer(inputCol="words", outputCol="features")
model = cv.fit(res) # even df works
result = model.transform(res)
result.show(truncate=False)

idf = IDF(inputCol="features", outputCol="finalFeatures")
idfModel = idf.fit(result)
result_tfidf = idfModel.transform(result)
num_topics = 5
#lda_model = LDA.train(result_tfidf['index','finalFeatures'],k = num_topics, maxIterations= 100)
lda_obj = newLDA(featuresCol = "finalFeatures", k = 3, maxIter = 100)
lda_model = lda_obj.fit(result_tfidf["index","finalFeatures"])
lda_model.describeTopics().show()


#print(res)
#data = []

