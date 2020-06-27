import wikipedia
from bs4 import BeautifulSoup
import requests
import re
import json


def wikipd(search_term):
    sumr = wikipedia.summary(search_term)[0:300]
    return sumr


def get_data(q):
    url = '{0}{1}'.format('https://en.wikipedia.org/wiki/', q)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    infobox = soup.select('.infobox')
    img = infobox[0]
    img_404 = '//upload.wikimedia.org/wikipedia/en/thumb/0/06/Wiktionary-logo-v2.svg/30px-Wiktionary-logo-v2.svg.png'
    if img.findChild("img")['src'] == img_404:
      return 0
    else:
      url = img.findChild("img")['src'].replace('//', '')
      return url
