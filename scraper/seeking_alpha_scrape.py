# Seeking alpha

from bs4 import BeautifulSoup
import requests
import json
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
import json
import requests
import pandas as pd
import numpy as np
from arango import ArangoClient
import os

proxy = "10.3.100.207:8080"

client = ArangoClient(host="10.5.30.185", port=8529,
                      username='root', password='shubham')
db = client.db('Finance')
news = db.collection("news_articles")

def seekingalpha(stock, span):
    data_fin = []
    date_today = datetime.now().day
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    link = 'http://seekingalpha.com/symbol/' + stock + '/latest'
    response = requests.get(link, headers=headers)
    html = response.content
    source = BeautifulSoup(html, "lxml")
    division = source.find('ul', {'id': 'symbol-page-latest'})
    division = division.findAll('div', {'class': 'symbol_article'})
    print("seekingalpha", len(division))
    #data_fin.append(["content", "title", "date", "ticker", "source", "url"])
    for a in division:
        try:
            final_url = "http://seekingalpha.com" + a.a["href"]
            date_scraped = datetime.fromtimestamp(int(a["time"]))
            print("seekingalpha", date_scraped.day, date_today)
            if (not abs(date_scraped.day - date_today) in range(1, span+1)):
                continue
            if ("http://seekingalpha.com/article" in final_url):
                # data_fin.append([a['title_detail']['value'], a['link'], a['title'], a['published'], ""])
                print("seekingalpha", "scraping", final_url)
                response = requests.get(final_url, headers=headers)
                html = response.content
                source = BeautifulSoup(html, "lxml")
                div2 = source.find('div', {'class': 'sa-art article-width'})
                data_fin.append([div2.text, a.text, str(
                    date_scraped), stock, "seekingalpha", final_url])
            elif ("http://seekingalpha.com/news" in final_url):
                print("seekingalpha", "scraping", final_url)
                response = requests.get(final_url, headers=headers)
                html = response.content
                source = BeautifulSoup(html, "lxml")
                div2 = source.find('div', {'id': 'bullets_ul'})
                data_fin.append([div2.text, a.text, str(
                    date_scraped), stock, "seekingalpha", final_url])
            else:
                print(final_url)
            print("added")
        except Exception as e:
            print(a, final_url, e)
    content = []
    title = []
    date = []
    ticker = []
    source = []
    url = []
    for a in data_fin:
        content.append(a[0])
        title.append(a[1])
        date.append(a[2])
        ticker.append(a[3])
        source.append(a[4])
        url.append(a[5])
        data = {'content': a[0], 'title': a[1], 'date': a[2],
                           'ticker': a[3], 'source': a[4], 'url': a[5]}
        os.environ['http_proxy'] = ""
        os.environ['HTTP_PROXY'] = ""
        os.environ['https_proxy'] = ""
        os.environ['HTTPS_PROXY'] = ""
        if a[0] != "":
            print "Inserting to DB"
            news.insert(data)
            print "Inserted"
        os.environ['http_proxy'] = proxy
        os.environ['HTTP_PROXY'] = proxy
        os.environ['https_proxy'] = proxy
        os.environ['HTTPS_PROXY'] = proxy

print seekingalpha("AAPL", 1)
