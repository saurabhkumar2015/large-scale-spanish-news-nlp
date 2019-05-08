# generic metadata generator for all urls stored in text file
# reading urls from text file and generating metadata to data.json file

from newsplease import NewsPlease
import json

data = []

f=open("y.txt", "r")

c = f.readlines()


for post in c:
	print(post)
	x = NewsPlease.from_url(post)
	data_json = {
	"URL": x.url,
	"Domain": x.source_domain,
	"title": x.title,
	"author": str(x.authors),
	"text": str(x.text),
	"date_published": str(x.date_publish)}
	data.append(data_json)

        
with open('data.json', 'w+') as outfile:
    json.dump(data, outfile)
    
