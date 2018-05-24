# Scrape Data for Shares Outstanding

from urllib.request import urlopen
from bs4 import BeautifulSoup
from os import listdir
import json

url_begin = "https://www.nasdaq.com/symbol/"
url_end = "/stock-report"

stockInfoDir = 'StockInfo/'
fileNames = listdir('StockInfo/')
tickers = []
outstandingShares = {}
noOutstandingShares = []

def setup():
    for fileName in fileNames:
        ticker = fileName.split('_')[1].split('.')[0]
        outstanding = getSharesOutstanding(ticker)
        if(outstanding == 0):
            noOutstandingShares.append(ticker)
        outstandingShares[ticker] = outstanding
        print(str(ticker) + "\t" + str(outstanding))

    print(noOutstandingShares)

    f = open('outstandingShares.txt', 'w+')
    f.write(json.dumps(outstandingShares))

def getSharesOutstanding(ticker):
    page = urlopen(url_begin + ticker + url_end)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', attrs={'class': 'marginB5px'})
    rows = []

    if(table is None):
        return 0

    for row in table.findAll("tr"):
        cells = row.findAll("td")
        rows.append(cells)

    commaShares = str(rows[3][1]).split('>')[1].split('<')[0]
    outstanding = commaShares.replace(",","")
    return int(outstanding)

setup()
