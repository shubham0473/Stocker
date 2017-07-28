from bs4 import BeautifulSoup
import lxml
import urllib2
import requests
from datetime import datetime, timedelta
from newspaper import Article
import lxml
import pandas as pd
import numpy as np
from arango import ArangoClient
import os
proxy = "10.3.100.207:8080"

client = ArangoClient(host="10.5.30.185", port=8529,
                      username='root', password='shubham')
db = client.db('Finance')
news = db.collection("news_articles")


def bloomberg(ticker, span):
    import requests
    url = "https://www.bloomberg.com/quote/" + ticker + ":US"
    r = requests.get(url)
    data = r.text
    ts = []
    title = []
    urls = []
    cont = []
    soup = BeautifulSoup(data)
    div = soup.find("div", {"class": "news__state active"})
    newsitems = div.findAll('article', {'class': 'news-story'})
    for n in newsitems:
        try:
            tst = n.find(
                'time', {"class": "news-story__published-at"})["datetime"]
            day_n = int(tst[8:tst.find("T")])
            today = datetime.now().day
            if(abs(day_n - today) in range(1, span+1)):
                print "News for :", day_n
                tit = n.find('a', {"class": "news-story__url"}).text
                u = n.find('a', {"class": "news-story__url"})['href']
                try:
                    article = Article(u)
                    article.download()
                    article.parse()
                    #data2 = r2.tex
                    # soup2 = BeautifulSoup(data2)
                    # div2= soup2.find("div", { "class" : "body-copy" })
                    # cont.append(div2.text)
                    if article.text != "":
                        dt_tmp = tst.replace('T', " ")
                        dt = dt_tmp[:dt_tmp.find(".")]
                        src = url.split(".")[1]
                        data = {'content': article.text, 'title': tit, 'date': dt,
                                        'ticker': ticker, 'source': src, 'url': url}
                        print "Inserting to DB"
                        os.environ['http_proxy'] = ""
                        os.environ['HTTP_PROXY'] = ""
                        os.environ['https_proxy'] = ""
                        os.environ['HTTPS_PROXY'] = ""
                        news.insert(data)
                        print "Inserted"
                        os.environ['http_proxy'] = proxy
                        os.environ['HTTP_PROXY'] = proxy
                        os.environ['https_proxy'] = proxy
                        os.environ['HTTPS_PROXY'] = proxy
                except Exception as e:
                    print e
                    continue
        except Exception as e:
            print e
            continue
    # arrticker = [ticker] * len(cont)
    # print(len(cont))
    # src = [s.split(".")[1] for s in urls]
    # df = pd.DataFrame({'content': cont, 'title': title, 'date': ts,
    #                    'ticker': arrticker, 'source': src, 'url': urls})
    # df['content'].replace('', np.nan, inplace=True)
    # df.dropna(subset=['content'], inplace=True)
    # return df

def main():
    print bloomberg("AAPL", 100)

if __name__ == '__main__':
    main()
