from bs4 import BeautifulSoup
from selenium import webdriver
from functions import processPage,get_results_per_page, WriteDictToCSV
import os

car_list = []
cycles = 0
driver = webdriver.PhantomJS()
url='http://www.autotrader.com/cars-for-sale/cars+under+15000/Toyota/Corolla/?zip=40056&startYear=2012&maxMileage=75000&numRecords=100&endYear=2016&modelCodeList=COROL&makeCodeList=TOYOTA&mpgRanges=40-MPG%2C31-40MPG&sortBy=derivedpriceASC&maxPrice=13000&firstRecord=0&searchRadius=100'
driver.get(url=url)
soup = BeautifulSoup(driver.page_source, "lxml")
results = int(soup.find(attrs={"data-qaid": "cntnr-resultTotal"}).text)
results_per_page=get_results_per_page(soup)
cyclesRequired = int(results / results_per_page + 1)
if cyclesRequired>1:
    page_buttons = {}
    button_list = driver.find_element_by_class_name('pagination')
    buttons = button_list.find_elements_by_tag_name('a')
    for button in buttons:
        key = button.text
        page_buttons[key] = button
for index in range(1,cyclesRequired+1):
    processed_page = processPage(driver.page_source)
    car_list+=processed_page[1]
    if index<cyclesRequired:
        page_buttons.get(str(index+1)).click()
csv_colums = ['Title','Price','Milage','Color','ID','Link']
currentPath = os.getcwd()
csv_file = currentPath + "/test.csv"
WriteDictToCSV(csv_file,csv_colums,car_list)
