import requests
from bs4 import BeautifulSoup
from lxml import html
import csv


class hatla2eeScraper:
    def __init__(self):
        self.url = 'https://eg.hatla2ee.com/en/car'
        self.optionsUrl = 'https://eg.hatla2ee.com/en/carSell/model?Brand='
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; "
            "x64; rv:66.0) "
            "Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8",
        }
        self.cars = []
        self.cars.append(['make', 'model', 'year'])

    def getMakes(self):
        try:
            request = requests.get(url=self.url, headers=self.headers)
            request.encoding = "utf-8"
            html = request.text
            carMainPage = BeautifulSoup(html, "lxml")
            makeSelect = carMainPage.find('select', id='make')
            self.makes = []
            skip = 1
            for option in makeSelect.find_all('option'):
                if skip == 1:
                    skip = 0
                    continue
                make = []
                make.append(option['value'])
                make.append(option.text)
                self.makes.append(make)
        except Exception as e:
            print(e)
            exit(1)

    def getModels(self, makeCode, makeName):
        try:
            url = self.optionsUrl + makeCode
            request = requests.get(url=url, headers=self.headers)
            request.encoding = "utf-8"
            html = request.text
            makeOptions = BeautifulSoup(html, "lxml")
            skip = 1
            for option in makeOptions.find_all('option'):
                if skip == 1:
                    skip = 0
                    continue
                for i in range(1991,2021):
                    car = []
                    car.append(makeName)
                    car.append(option.text)
                    car.append(i)
                    self.cars.append(car)
        except Exception as e:
            print(e)
            exit(1)

if __name__ == "__main__":
    scraper = hatla2eeScraper()
    scraper.getMakes()
    skip = 1
    for make in scraper.makes:
        #skip headers row
        if skip == 1:
            skip=0
            continue
        scraper.getModels(make[0],make[1])
    with open('cars.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(scraper.cars)
