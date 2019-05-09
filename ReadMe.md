## Large Scale Data Collection of Spanish News

## 1) Web crawler and metadata generator:
  Use files in crawler folder for scrapping URLs from different spanish website.
  test.py is sample crawler along with metadata generator.
  read.py is generic metadata generator for all the URLs stored in text file
  rest are different crawlers for different websites.

## 2) NLTK Downloads

import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

## 3) Use Json file to write to Kafka
push to kafka: python write_to_kafka.py <absolute path of json file> <topic name>
example python write_to_kafka.py C:\Users\Saurabh\Downloads\courses\bg\project\data.json guardian222
check via consumer: .\kafka-console-consumer.sh  --bootstrap-server localhost:9092 --topic guardian2

## 3) Pipline to generate match article pairs
python similar_stories_pipeline.py <data file> <result file>

python similar_stories_pipeline.py C:\Users\Saurabh\Downloads\courses\bg\project\data.json C:\Users\Saurabh\Downloads\courses\bg\project\result_

## References:
1. News-please https://github.com/fhamborg/news-please
2. Scrapy https://scrapy.org/
3. Apache Kafka https://kafka.apache.org/
4. SPEC paper https://ieeexplore.ieee.org/document/7474330
5. Universal Dependency https://universaldependencies.org/
6. ufal-udpipe python package.
7. Deduplication Papers/Resources
a. https://www.hindawi.com/journals/mpe/2016/3919043/
b. https://www.aclweb.org/anthology/P16-4019
c. Dissertation of Dr. Ahmad Mustafa,
https://search.proquest.com/pqdtlocal1006281/docview/2086379093/EDE7D1E6
ED9843E5PQ/1?accountid=7120
d. https://www.eventregistry.org/documentation?tab=semanticSimilarity
8. List of news sources
https://docs.google.com/spreadsheets/d/13DmJ140wW8pCp6nyRSAk911S7AoF-6zJOJF77qoMuM/
edit?usp=sharing

