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
import sys
from torrequest import TorRequest

sys.path.append('/home/shubham/MTP/Stock_predictor/db')

from connection import NewsColl

news = NewsColl()

proxy = "10.3.100.207:8080"

client = ArangoClient(host="10.5.30.185", port=8529,
                      username='root', password='shubham')
db = client.db('Finance')
news = db.collection("news_articles")

NASDAQ=['AAPL', 'CSCO', 'INTC', 'MSFT']
NYSE=['DIS', 'WMT', 'VZ', 'V', 'UTX', 'UNH', 'TRV', 'PG', 'PFE', 'NKE', 'MRK', 'MMM', 'MCD', 'JPM',
'JNJ', 'IBM', 'HD', 'GS', 'GE', 'XOM', 'DD', 'KO', 'CVX', 'CAT', 'BA', 'AXP']

def google_finance(company_ticker, span):
    today = datetime.now()
    startdate = today
    enddate = startdate - timedelta(days=span)
    startdt = datetime.strftime(startdate, "%Y-%m-%d")
    enddt = datetime.strftime(enddate, "%Y-%m-%d")
    if not company_ticker in NYSE:
        url = 'https://www.google.com/finance/company_news?q=NASDAQ%3A' + company_ticker + \
            '&ei=ixzVWIG4F5WqugTCt5zIDQ&startdate=' + startdt + '&enddate=' + \
        enddt + '&start=0&num=100000'
    else:
         url = 'https://www.google.com/finance/company_news?q=NYSE%3A' + company_ticker + \
            '&ei=ixzVWIG4F5WqugTCt5zIDQ&startdate=' + startdt + '&enddate=' + \
        enddt + '&start=0&num=100000'
    print url
    response = requests.get(url)
    html = response.content
    source = BeautifulSoup(html)
    articles = source.find_all('span', {'class': "name"})
    title = []
    date = []
    content = []
    news_source = []
    sources = []
    url = []
    dates = source.find_all('span', {'class': "date"})
    partial_sources = source.find_all('div', {'class': "byline"})
    for line in partial_sources:
        for row in line.find_all('span', {'class': "src"}):
            sources.append(row)

    today = datetime.now().day

    for i in range(len(articles)):
        if dates[i].text[-1] != 'o':  # checking the format of hours ago
            article_time = dates[i].text
            article_time = datetime.strptime(article_time, "%b %d, %Y")
            # considering time to be midday 12 when time not available
            article_time = article_time + timedelta(hours=12)
        else:
            temp = dates[i].text
            if temp[1] == ' ':  # checking single digit hours
                hours = temp[0]
            else:
                hours = temp[0:2]
            current_time = datetime.now()
            article_time = current_time - timedelta(hours=int(hours))

        print 'found'
        article_initial = articles[i]
        link = article_initial.find('a')['href']
        article = Article(link)
        article_time = datetime.strftime(article_time, "%Y-%m-%d %H:%M:%S")
        try:
            article.download()
            article.parse()
            data = {'content': article.text, 'title': article_initial.text, 'date': article_time,
                               'ticker': company_ticker, 'url': link}
            # os.environ['http_proxy'] = ""
            # os.environ['HTTP_PROXY'] = ""
            # os.environ['https_proxy'] = ""
            # os.environ['HTTPS_PROXY'] = ""
            if article.text != "":
                # print "Inserting to DB"
                news.insert(data)
                # print "Inserted"
            # os.environ['http_proxy'] = proxy
            # os.environ['HTTP_PROXY'] = proxy
            # os.environ['https_proxy'] = proxy
            # os.environ['HTTPS_PROXY'] = proxy
        except Exception as e:
            print e
            continue

def main():
    for ticker in NYSE + NASDAQ:
        print ticker
        google_finance(ticker, 3650)

if __name__ == '__main__':
    main()

# print google_finance("AAPL", 1)
