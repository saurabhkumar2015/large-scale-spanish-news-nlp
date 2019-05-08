from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import yaml
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession, Row
import connector
from ufal.udpipe import Model, Pipeline, ProcessingError
import json
from pyspark.sql.functions import udf, round

from pyspark.sql.types import *
#
# model = Model.load('../spanish-ancora-ud-2.3-181115.udpipe')
# pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT,"conllu")
# error = ProcessingError()

# conf = SparkConf().setAppName('myApp').set('spark.executor.memory', '8g').set('spark.driver.memory', '4g').setMaster('local[8]')
#
#
# sparkContext = SparkContext(conf=SparkConf())


spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", "mongodb+srv://admin:admin@demo-dhnar.mongodb.net/myDB.spark?retryWrites=true") \
    .config("spark.mongodb.output.uri", "mongodb+srv://admin:admin@demo-dhnar.mongodb.net/myDB.spark?retryWrites=true") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.1')\
    .getOrCreate()

# model = Model.load('../spanish-ancora-ud-2.3-181115.udpipe')
data = spark.read.option("charset", "UTF-8").json('../d.json')
# dataRDD = data.rdd
# data.show()

class udPipe(object):

    def get(modelAdd, text):

        from ufal.udpipe import Model, Pipeline, ProcessingError

        error = ProcessingError()
        model = Model.load(modelAdd)
        pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
        parsedArticle = pipeline.process(text, error)

        return parsedArticle

def createParseTree(text):
    print("------------------------")
    # parsedArticle = pipeline.process(text, error)
    parsedArticle = udPipe.get('../spanish-ancora-ud-2.3-181115.udpipe', text)
    # print(parsedArticle)
    return str(parsedArticle)


#
article = data.rdd.map(lambda x: Row(_id = x[0]+' : ' +x[5], Domain = x[0], URL = x[1], author = x[2], date_published = x[3], text =x[4], title = x[5]))
# data.withColumn('_id', article("Domain"))
# article.foreach(print)
articleDF = article.toDF()
articleDF.show()

# NOTE: it seems that calls to udf() must be after SparkContext() is called
# udfParse = udf(createParseTree, StringType())
# articleDF = articleDF.withColumn("parse_tree", udfParse(col("URL")))
# articleDF.show()


opr = udf(lambda  z: createParseTree(z), StringType())

articleDF = articleDF.select('Domain', 'URL', '_id', 'author', 'date_published', 'text', 'title', opr('text').alias('parse_tree'))

# data.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
articleDF.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()

# with open('../data.json') as json_file:
#     data = json.load(json_file, encoding="utf-8")
#
#
# db = connector.intializeConnector()
# tests = db.newsArticles
#
# # To check if the mongo connection is made successfully
# # serverStatusResult=db.command("serverStatus")
# # print(serverStatusResult)
#
#
# pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT,"conllu")
# error = ProcessingError()
#
# for i in range(0, len(data)):
#     article = data[i]
#     articleText = article['text']
#     parsedArticle = pipeline.process(articleText, error)
#     article['_id'] = article['Domain'] + ' : ' + article['title']
#     article['parsed_tree'] = parsedArticle
#     try:
#         tests.insert_one(article)
#         print('Inserted newsArticle ' + str(i))
#     except:
#         print('entry already exists')
#         # Same Key already present. Update with the latest info
#         IDquery = {'_id' : article['_id']}
#         updatedArticle = {"$set": article}
#         tests.update_one(IDquery, updatedArticle)
#         print('Updated newsArticle ' + str(i))
#
