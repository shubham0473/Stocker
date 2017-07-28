import pandas
import nltk
# import keras
import StanfordDependencies
from arango import ArangoClient
import os
import pandas as pd
import spacy
import sys
sys.path.append('/home/shubham/MTP/Stock_predictor/db')

from SOV_extract import findSVAOs

from connection import NewsColl

NewsDB = NewsColl()
nlp = spacy.load('en')

# client = ArangoClient(host="10.5.30.185", port=8529,
#                       username='root', password='shubham')
# db = client.db("Finance")
#
# news = db.collection("news_articles")
#
# os.environ['http_proxy'] = ""
# os.environ['HTTP_PROXY'] = ""
# os.environ['https_proxy'] = ""
# os.environ['HTTPS_PROXY'] = ""
# print news.indexes()

# for n in NewsDB.retrieve():
#     print n

# doc = nlp(u'I like green eggs and ham.')
# for np in doc.noun_chunks:
#     print(np.text, np.root.text, np.root.dep_, np.root.head.text)



from spacy.en import English
parser = English()

articles = NewsDB.retrieve()

for article in articles.iterrows():
    # print article[1]
    headline = parser(article[1]['title'])
    content = parser(article[1]['content'])
    print(findSVAOs(headline), findSVAOs(content))
