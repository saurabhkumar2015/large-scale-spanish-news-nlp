from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import yaml
import connector
from ufal.udpipe import Model, Pipeline, ProcessingError
import json


model = Model.load('../spanish-ancora-ud-2.3-181115.udpipe')

with open('../data.json') as json_file:
    data = json.load(json_file, encoding="utf-8")


db = connector.intializeConnector()
tests = db.newsArticles

# To check if the mongo connection is made successfully
# serverStatusResult=db.command("serverStatus")
# print(serverStatusResult)


pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT,"conllu")
error = ProcessingError()

for i in range(0, len(data)):
    article = data[i]
    articleText = article['text']
    parsedArticle = pipeline.process(articleText, error)
    article['_id'] = article['Domain'] + ' : ' + article['title']
    article['parsed_tree'] = parsedArticle
    try:
        tests.insert_one(article)
        print('Inserted newsArticle ' + str(i))
    except:
        print('entry already exists')
        # Same Key already present. Update with the latest info
        IDquery = {'_id' : article['_id']}
        updatedArticle = {"$set": article}
        tests.update_one(IDquery, updatedArticle)
        print('Updated newsArticle ' + str(i))

