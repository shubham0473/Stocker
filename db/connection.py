from arango import ArangoClient
import os
import pandas as pd

proxy = "10.3.100.207:8080"
client = ArangoClient(host="10.5.30.185", port=8529,
                      username='root', password='shubham')
db = client.db("Finance")

def set_proxy():
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

def unset_proxy():
    os.environ['http_proxy'] = ""
    os.environ['HTTP_PROXY'] = ""
    os.environ['https_proxy'] = ""
    os.environ['HTTPS_PROXY'] = ""

class NewsColl(object):

    def __init__(self):

        self.db = client.db('Finance')
        self.collection = db.collection("news_articles")
        print "connection up"

    def insert(self, data):
        # print "Inserting to DB"
        unset_proxy()
        self.collection.insert(data)
        set_proxy()
        # print "Inserted"


    def retrieve(self):
        unset_proxy()
        result = []
        for news in self.collection:
            print news
            result.append(news)
        set_proxy()
        return pd.DataFrame(result)

def main():
    n = NewsColl()
    print n.retrieve().iterrows()

if __name__ == '__main__':
    main()
