from bs4 import BeautifulSoup
import re
import csv


def car(strTitle, strPrice, strMileage, strColor, strId, strLink):
    return  {'Title': strTitle,
            'Price': strPrice,
            'Mileage': strMileage,
            'Color': strColor,
            'Id': strId,
            'Link': strLink}


def parseCarTag(child):
    try:
        strTitle = child.h2.text
    except AttributeError:
        strTitle = ""
    try:
        strPrice = child.find(attrs={"data-qaid": "cntnr-lstng-price-outer"}).text
    except AttributeError:
        strPrice = ""
    try:
        mileage = child.find(attrs={"data-qaid": "mileage"}).text
        strMileage = mileage[0:(mileage.find('miles') - 1)]
    except AttributeError:
        strMileage = ""
    try:
        strColor = child.find('div', class_='col-xs-7').strong.text
    except AttributeError:
        strColor = ""
    try:
        match = re.search(r'listingId=(?P<id>\d+)', child.h2.a.get('href'))
        strId = match.group('id')
        strLink = 'http://www.autotrader.com//cars-for-sale/vehicledetails.xhtml?listingId=' + strId
    except AttributeError:
        strId = ""
        strLink = ""

    return {'Title': strTitle,
            'Price': strPrice,
            'Milage': strMileage,
            'Color': strColor,
            'Id': strId,
            'Link': strLink}


def processPage(source):
    records=[]
    soup = BeautifulSoup(source,"lxml")
    cars = soup.find('div', 'loading-indicator')
    for child in cars.children:
        records.append(parseCarTag(child))
    records_parsed = len(list(cars.children))
    return records_parsed, records


def get_results_per_page(soup):
    results = soup.find(id='numRecords')
    numResults = 0
    for child in results.children:
        if child.has_attr('selected'):
            numResults=int(child.text)
    return numResults

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return