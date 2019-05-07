from ufal.udpipe import Model, Pipeline, ProcessingError
import json

model = Model.load('../spanish-ancora-ud-2.3-181115.udpipe')

with open('../data.json') as json_file:
    data = json.load(json_file, encoding="utf-8")

print(len(data))
print(data[0]['text'])

#
# pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT,"conllu")
#
# error = ProcessingError()
#
# for i in range(0, len(data)):
#     articleText = data[i]['text']
#     parsedArticle = pipeline.process(articleText, error)
#     print(parsedArticle)