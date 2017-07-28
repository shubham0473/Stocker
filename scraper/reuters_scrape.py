from bs4 import BeautifulSoup
import lxml
import urllib2
import requests
from datetime import datetime, timedelta
from newspaper import Article
import lxml
import pandas as pd
import numpy as np
import time
from dateutil.parser import parse
from datetime import datetime, timedelta
import sys
from torrequest import TorRequest
sys.path.append('/home/shubham/MTP/Stock_predictor/db')

from connection import NewsColl

Newsdb = NewsColl()

class ReutersSpider(object):
    def __init__(self, start_page, end_page, req_port):
        self.start_page = start_page
        self.end_page = end_page
        self.

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def bloomberg(ticker, span):
    url = "https://www.reuters.com/news/archive/marketsNews?view=page&page={0}&pageSize=10"
    for i in range(1, 10):
        r = requests.get(url.format(i))
        data = r.text
        ts = []
        title = []
        urls = []
        cont = []
        soup = BeautifulSoup(data, "lxml")
        div = soup.find("section", {"class": "module-content"})
        # print div
        newsitems = div.findAll('div', {'class': 'story-content'})
        # print newsitems
        for news in newsitems:
            article_time = news.find(
                'time', {"class": "article-time"})
            timestamp = parse(article_time.find('span', {"class": "timestamp"}).string)
            today = datetime.now()
            print "News for :", timestamp
            title = news.find('h3', {"class": "story-title"}).text
            link = "https://www.reuters.com/" + str(news.find('a', href=True)['href'])
            content = news.find('p').text
            print title, content

            data = {'content': content, 'title': title, 'date': str(timestamp),
                            'source': "reuters", 'url': link}
            Newsdb.insert(data)

def main():
    bloomberg("AAPL", 100)

if __name__ == '__main__':
    main()
