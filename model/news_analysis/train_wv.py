from gensim.models import Word2Vec
import sys
import itertools
reload(sys)
sys.setdefaultencoding('UTF-8')
import os


base_path = "/home/shubham/MTP/Stock_predictor/model/news_analysis/financial-news-dataset/"

for d in next(os.walk(base_path))[1]:
    for i in next(os.walk(base_path + d))[1]:
        print i


# stoplist = set('for a of the and to in'.split())
# texts = [[word for word in document] for document in documents]
#
# texts, dictionary = build_corpus(docs['content'])
# print(texts)
# model = Word2Vec(texts)
