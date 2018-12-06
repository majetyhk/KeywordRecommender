from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
Topics correspond to cluster centers, and documents correspond to examples rows in a dataset
Topics and documents both exist in a feature space, where feature vectors are vectors of word counts bag of words
Rather than estimating a clustering using a traditional distance, LDA uses a function based on a statistical model of how text documents are generated

import pyspark
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
# stuff we'll need for text processing
from nltk.corpus import stopwords
import re as re
from pyspark.ml.feature import CountVectorizer , IDF
# stuff we'll need for building the model

from pyspark.mllib.linalg import Vector, Vectors
from pyspark.mllib.clustering import LDA, LDAModel
# reading the data
data = sqlContext.read.format("csv") \
   .options(header='true', inferschema='true') \
   .load(os.path.realpath("Womens Clothing E-Commerce Reviews.csv"))

reviews = data.map(lambda x : x['Review Text']).filter(lambda x: x is not None)

tokens = reviews                                                   \
    .map( lambda document: document.strip().lower())               \
    .map( lambda document: re.split(" ", document))          \
    .map( lambda word: [x for x in word if x.isalpha()])           \
    .map( lambda word: [x for x in word if len(x) > 3] )           \
    .map( lambda word: [x for x in word if x not in StopWords])    \
    .zipWithIndex()



row_rdd = rdd1.map(lambda x: Row(x))
df=sqlContext.createDataFrame(row_rdd,['numbers']).show()
cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=3, minDF=2.0)
model = cv.fit(df)
result = model.transform(df)
result.show(truncate=False)
from pyspark.sql.functions import monotonicallyIncreasingId
res = df.withColumn("id", monotonicallyIncreasingId())
df_txts = sqlContext.createDataFrame(row_rdd, ["list_of_words",'index'])

idf = IDF(inputCol="raw_features", outputCol="features")
idfModel = idf.fit(result_cv)
result_tfidf = idfModel.transform(result_cv) 



