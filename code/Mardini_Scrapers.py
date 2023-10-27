# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 18:03:18 2022

@author: rania

"""
"""

#option 1 following guides online, note that you need to avoid detection to use this process
#so don't I won't use this until I've worked on avoiding bot detection
#references of what to keep in mind:
https://developers.google.com/search/docs/crawling-indexing/robots/intro
https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja

import csv
import requests

csvlink = 'https://perso.telecom-paristech.fr/eagan/class/igr204/data/cereal.csv'
results = []

with requests.get(csvlink, stream = True) as response:
    response.raise_for_status()
    
    
    lines = (line.decode('utf-8') for line in response.iter_lines())
    
    for row in csv.reader(lines):
        results.append(row)

#another option       
#using pandas again, from a different website; had issues with this but leaving it in
#because it's another easy way of getting content

import pandas as pd
import numpy as np
import matplotlib as plt

table = pd.read_html('https://www.kaggle.com/datasets/crawford/80-cereals')

df = table[0]

#this gave me an error, fun
"""

#using the usual parsers: requests and BeautifulSoup4; using a sandbox for the table

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.scrapethissite.com/pages/forms/'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

htmlcontent = soup.prettify()
print(htmlcontent)

#so now I have the html of the entire page
#what if I only want the table?
#inspecting the webpage, I can see what tables and tag classes to parse
#is this the best way to do this? probably not, but it's the easiest to organize

#table = soup.find('table', {'class' : 'lineItemsTable'})
#results = []

name = []
year = []
wins = []
losses = []
ot = []
pct = []
gf = []
ga = []
diff = []

for row in soup.findAll('tr', {'class': 'team'}):
    name.append((row.find('td', {'class', 'name'})).text)
    year.append((row.find('td', {'class', 'year'})).text)
    wins.append((row.find('td', {'class', 'wins'})).text)
    losses.append((row.find('td', {'class', 'losses'})).text)
    ot.append((row.find('td', {'class', 'ot-losses'})).text)
    pct.append((row.find('td', {'class', 'pct'})).text)
    gf.append((row.find('td', {'class', 'gf'})).text)
    ga.append((row.find('td', {'class', 'ga'})).text)
    diff.append((row.find('td', {'class', 'diff'})).text)
    
#now to put this all into a pandas df

df = pd.DataFrame(
    {'name': name,
     'year': year,
     'wins': wins,
     'losses': losses,
     'ot losses': ot,
     'win%': pct,
     'goals_for': gf,
     'goals_against': ga,
     'diff': diff})

#note that if you get a valueerror for requiring an array of equal size
#it's possible you need to delete one of the mismatched lists and run the loop again
#something may have gotten lost along the lines while toying with the program