# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
from typing import cast


def pages():
    page_buttons={}
    button_list=driver.find_element_by_class_name('pagination')
    buttons=button_list.find_elements_by_tag_name('a')
    for button in buttons:
        key=button.text
        page_buttons[key]= button
        
    return page_buttons

    
    
    
def car(strTitle,strPrice, strMileage, strColor, strId, strLink):
   return {'Title'  : strTitle,
           'Price'  : strPrice,
           'Mileage': strMileage,
           'Color'  : strColor,
           'Id'     : strId,
           'Link'   : strLink }

def parseCarTag(child):
        strTitle=child.h2.text
        strPrice=child.find(attrs={"data-qaid" : "cntnr-lstng-price-outer"}).text
        mileage=child.find(attrs={"data-qaid" : "mileage"}).text
        strMileage=mileage[0:(mileage.find('miles')-1)]
        strColor=child.find('div', class_='col-xs-7').strong.text
        match = re.search(r'listingId=(?P<id>\d+)',child.h2.a.get('href'))
        strId=match.group('id')
        strLink = 'http://www.autotrader.com//cars-for-sale/vehicledetails.xhtml?listingId=' + strId
        return {'Title'  : strTitle,
                'Price'  : strPrice,
                'Milage' : strMileage,
                'Color'  : strColor,
                'Id'     : strId,
                'Link'   : strLink }
                     
def processPage(soup,car_list):
    cars=soup.find('div', 'loading-indicator')
    for child in soup.children:
        car_list.append(parseCarTag(child))
    RecordsParsed=len(list(cars.children))
    return (RecordsParsed,car_list)
    
                
                
                
                
                
                
                
car_list=[]
cycles=0
driver=webdriver.PhantomJS()
url='http://www.autotrader.com/cars-for-sale/Sedan/Pewee+Valley+KY-40056?zip=40056&startYear=2013&maxMileage=75000&numRecords=100&mpgRanges=40-MPG%2C31-40MPG&sortBy=derivedpriceASC&maxPrice=10000&vehicleStyleCodes=SEDAN&firstRecord=0&endYear=2017&searchRadius=75'
driver.get(url=url)
soup=BeautifulSoup(driver.page_source,"lxml")
results=int(soup.find(attrs={"data-qaid": "cntnr-resultTotal"}).text)
if results>0:
    cars=soup.find('div', 'loading-indicator')
    recordsPerCycle=len(list(cars.children))
    cyclesRequired=int(results/recordsPerCycle+1)
    if cyclesRequired>1:
        page_buttons=pages()
    for child in cars.children:
        car_list.append(parseCarTag(child))
    results_left=results-len(car_list)
    cycles=+1
    
    if cyclesRequired>cycles:
        page_buttons.get(str(cycles+1)).click()
        
        
        

    
    cars_df= pd.DataFrame(car_list)


