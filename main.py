"""
Script for crawling supplier information from Just Dial website
Author: murali6688
Date: 2019-06-08
"""

import requests
import re 
from lxml import html
from bs4 import BeautifulSoup
from argparse import ArgumentParser

def parse_keywords(tree):
    key_words = []
    for row in tree.xpath('//*[@id="alsol"]')[0].xpath('table')[0].xpath('tr'):
        for col in row.xpath('td'):
            values = col.xpath('a')
            for val in values:
                key_words.append(val.text)
    return key_words

def get_mobile(soup):
    cipherKey = str(soup.select('style[type="text/css"]')[1])
    keys = re.findall('-(\w+):before', cipherKey, flags=0)
    values = [int(item)-1 for item in re.findall('9d0(\d+)', cipherKey, flags=0)]
    cipherDict = dict(zip(keys,values))
    cipherDict[list(cipherDict.keys())[list(cipherDict.values()).index(10)]] = '+'
    decodeElements = [item['class'][1].replace('icon-','') for item in soup.select('.telCntct span[class*="icon"]')]

    telephoneNumber = ''.join([str(cipherDict.get(i)) for i in decodeElements])

    return telephoneNumber


def main(url):
    """
    Open justdial page and fetch the supplier info from the page including phone number
    Args
        url: Valid url of justdial
    """

    source_page = requests.get(url, headers  = {'User-Agent': 'Mozilla/5.0'})

    tree = html.fromstring(source_page.content)

    c_name = tree.xpath('//*[@id="setbackfix"]/div[1]/div/div[1]/div[2]/div/div/h1/span/span')[0].text.strip()

    c_addr = tree.xpath('//*[@id="fulladdress"]/span/span')[0].text.strip()

    key_words = parse_keywords(tree)

    soup = BeautifulSoup(source_page.content, 'lxml')

    c_phone = get_mobile(soup)

    return [url, c_name, c_addr, c_phone, key_words]


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--u', '-url', required=True, help='Pass the valid just dial url for fetching the data')
    args = parser.parse_args()

    records = main(args.u)

    print(records)

