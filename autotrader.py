from bs4 import BeautifulSoup
from selenium import webdriver
import functions
import os
import csv
from collections import defaultdict

car_list = defaultdict(dict)
cycles = 0
driver = webdriver.PhantomJS()
url = 'http://www.autotrader.com/cars-for-sale/cars+under+15000/Toyota/Corolla/?zip=40056&startYear=2012&maxMileage' \
      '=75000&numRecords=100&endYear=2016&modelCodeList=COROL&makeCodeList=TOYOTA&mpgRanges=40-MPG%2C31-40MPG&sortBy' \
      '=derivedpriceASC&maxPrice=13000&firstRecord=0&searchRadius=100 '
driver.get(url=url)
soup = BeautifulSoup(driver.page_source, "lxml")
results = int(soup.find(attrs={"data-qaid": "cntnr-resultTotal"}).text)
results_per_page = functions.get_results_per_page(soup)
cyclesRequired = int(results / results_per_page + 1)
if cyclesRequired > 1:
    page_buttons = {}
    button_list = driver.find_element_by_class_name('pagination')
    buttons = button_list.find_elements_by_tag_name('a')
    for button in buttons:
        key = button.text
        page_buttons[key] = button
for index in range(1, cyclesRequired + 1):
    processed_page = functions.processPage(driver.page_source)
    car_list.update(processed_page[1])
    if index < cyclesRequired:
        page_buttons.get(str(index + 1)).click()
current_dir = os.getcwd()
csvfile = current_dir + "/test.csv"
with open(csvfile,'a+') as car_csv:
    fieldnames=['Title','Price','Mileage','Color','Link']
    writer = csv.DictWriter(car_csv,fieldnames=fieldnames)
    writer.writeheader()
    for k,v in car_list.items():
        writer.writerow(v)


print('The End')
