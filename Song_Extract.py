# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 18:40:30 2020

@author: Zubin
"""

from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as BSoup
import re


## Extract half of list from Fantano Top 200 list linked website ##



html = urlopen('https://www.theneedledrop.com/101-200')
bs = BSoup(html.read(), 'html.parser')

for e in bs.p.find_all('br'):
    
    e.extract()
    
myList = []
shortened = []

for item in bs.p:
    
    myList.append(item)
    shortened.append(item[5:])




## Extract other half of list from Fantano Top 200 Youtube url ##


req = Request('https://www.youtube.com/watch?v=EyMX4lcKNPg', headers = {'User-Agent' : 'Mozilla/5.0'})    
html2 = urlopen(req).read()
bs2 = BSoup(html2, 'html.parser')
data2 = bs2.find_all("script" )[18]

s = data2.string
shortened.extend(s.string[s.string.find("A Tribe"):s.string.find("Still Brazy") + len("Still Brazy")].split('\\n'))

TOP200 = shortened.copy()



## Generalized function to extract lists from Fantano "Top List" Videos ##


def YTdescExtract(url):
    
    myList = []
    
    req = Request(url, headers = {'User-Agent' : 'Mozilla/5.0'})
    
    html = urlopen(req).read()
    
    bs = BSoup(html, 'html.parser')
    
    data = bs.find_all("p", {'id' : 'eow-description'})[0]
    
    for e in data.find_all(['br', 'a']):
        e.extract()
        
    for item in data:
        
#        if len(item) > 140 : 
            
#            continue
        
        if " - " in item :
            
            if re.findall('[0-9]+\.', item):
                
                if re.search('[a-zA-Z]', item) == None :
                    
                    continue
                
                else: 
                    
                    first = re.search('[a-zA-Z]', item)
                
                    myList.append(item[first.start():])
                    
                    
            else:
                
                myList.append(item)
                
    return myList
                
    
    
    
    
    

   


    