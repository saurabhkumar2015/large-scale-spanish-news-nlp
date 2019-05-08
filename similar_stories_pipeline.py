import nltk
import sys
import string
import re
from pyspark import SparkContext, SparkConf
from nltk.stem import PorterStemmer
import json
import pandas as pd
import datetime
import numpy as np

import es_core_news_sm
nlp = es_core_news_sm.load()


ps = PorterStemmer()
print('Punctuations to be removed:',string.punctuation)
exclude = set(string.punctuation)

#nem_score, es_score
def process(fileName, output):
    lines = open(file=fileName,mode="r").readlines()
    data_list = []
    for line in lines:
        if line is None or line.strip().__len__() ==0:
            continue
        for data in json.loads(line):
            title = data['title'].replace('None','')
            text = data['text'].replace('None','')
            tmp = ""
            if title is not None or title.strip() != "None":
                tmp = tmp + title.strip() +'.'
            if text is  None or text.strip() == "None":
                continue
            tmp = tmp + text.strip()
            tmp.replace("\\u00",'').replace("\n","")
            data_list.append(tmp)
            # print("$$$$$$$News is:",tmp)
    conf = SparkConf().setAppName("Train_News").setMaster("local[1]")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")
    dataRdd = sc.parallelize(data_list).distinct(numPartitions=1)
    tokenizedRdd = dataRdd.map(lambda x : [x,preprocess(x)])
    taggedRdd = tokenizedRdd.map(lambda x: [x[0],x[1], getNamedEntities(x[0]), extractSignature(x[0])])
    prepared_data = taggedRdd.collect()

    result = []
    i=0
    for data1 in prepared_data:
        print('Processed data:',i)
        i = i +1
        for data2 in prepared_data:
            if data1 == data2:
                continue
            nn_count = 0
            spot_count = 0
            nn_score = 0
            lav_d_count = 0
            lav_d_score = 0
            spot_score = 0

            if len(data1[2]) != 0:
                for nn in data1[2]:
                    n = len(nn)
                    if nn in data2[2]:
                        nn_count = nn_count+1
                    for tmp in data2[2]:
                        l = len(tmp)
                        if lav_distance(nn,tmp)/(n+l) < 0.25:
                            lav_d_count = lav_d_count +1
                nn_score = nn_count / len(data1[2])
                lav_d_score = lav_d_count / len(data1[2])
            if len(data1[3]) != 0:
                for nn in data1[3]:
                    if nn in data2[3]:
                        spot_count = spot_count+1
                spot_score = spot_count / len(data1[3])
            result.append([data1[0],data1[2],data1[3],data2[0],data2[2], data2[3], nn_count, nn_score, lav_d_count, lav_d_score, spot_count, spot_score])
    df = pd.DataFrame(data = result, columns=["News1","Names_Entities_1","Spot_words_1","News2","Names_Entities_2","Spot_words_2",
                                              "Named_Entity_match_count","Named_Entity_match_score","Laven_Named_Entity_match_score","Laven_Named_Entity_match_count","Spot_Words_Match_score","Spot_Words_Match_Score"])
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(" ","_").replace(":","_")
    df.query( 'Named_Entity_match_score > 0 or Spot_Words_Match_Score > 0.25').to_csv(output+time+".csv")
    print('Report File Saved')


def getNamedEntities(x):
    # data = ''.join(ch for ch in x if ch not in exclude)
    # print(data)
    # stem = ps.stem(data)
    doc = nlp(x)
    doc_set = set()
    for X in doc.ents:
        doc_set.add(X.text.replace('\n',''))
    return doc_set

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

#https://www.hindawi.com/journals/mpe/2016/3919043/
#get words around spots
def extractSignature(x):
    splits = re.split('[?.,]',x)
    spot_words = set()
    for token in splits:
        words = token.strip().split()
        l = len(words)
        if l > 0:
            spot_words.add(words[0])
            if l > 1:
                spot_words.add(words[l - 1].strip())
    return spot_words

def lav_distance(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Number of arguments is not correct. We have 2 arguments')
        exit()

    file_name = sys.argv[1]
    process(fileName=file_name, output=sys.argv[2])
