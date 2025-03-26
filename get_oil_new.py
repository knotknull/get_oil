#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests 
import re 
from datetime import datetime


## target page
pdo = "https://patriotdiscountoil.com/"

## call get method to request target page
pdo_pg = requests.get(pdo)

## lets make soup !!
soup = BeautifulSoup(pdo_pg.content, "html.parser")

## set the search text
srch_text = "Today’s Oil Price"

## 
## THIS IS WHAT WE ARE SEARCHING FOR 
## 
##		<div class="elementor-widget-container">
##							Today’s Oil Price<br>3.32<sup>9</sup> /gal						</div>
##				</div>
## 
## search by text with the help of the lambda function (?)
## find all tags named div and return text inside
## works  
## findit = soup.find_all(lambda tag: tag.name == "div" and  srch_text in tag.text)
## works  
now=datetime.now()
for item in soup.find(lambda tag: tag.name == "div" and  srch_text in tag.text):
    if(srch_text in item.text ):    
        ## Found Today's Oil Price
        pdo_price=re.findall("[0-9.]+",item.text ) 
        ## Pull out the price
        the_price=pdo_price[0];
        print(f'Date: {now:%Y%m%d}, PDO Price: {the_price}')

