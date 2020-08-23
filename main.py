import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv


def compute_max_temp(df):
    # find the highest temperature in each day
    return list(df.groupby('date')['temp'].max())


class Weather:
    def __init__(self, id):
        ''' create an object with id being the specific day in yyyymmdd format'''
        self.id = id
        self.url = 'https://www.timeanddate.com/weather/australia/melbourne/historic?hd='\
            + str(self.id)
        self.date = str(self.id % 100)
        self.file = 'data/melbourne.18_08_2020.22_08_2020.csv'

    def getPage(self):
        ''' collect the page '''
        return requests.get(self.url)

    def parseText(self):
        ''' 
        extract data from html to CSV 
            date,time,temp,wind,humidity,barometer
            20,12:00 am,8,17,76,997
            20,12:30 am,9,24,71,997
        '''
        page = self.getPage()
        soup = BeautifulSoup(page.content, 'html.parser')
        # jump to the body of the table
        table = soup.find(id='wt-his').tbody
        with open(self.file, 'a') as f:
            for tr in table.findAll('tr'):
                # remove the span class for full day format
                tr.find('span').decompose()
                # get time
                time = tr.find_all('th')[0].text
                tds_list = tr.find_all('td')
                # get temp
                temp = tds_list[1].text.split()[0]
                # get wind
                wind = tds_list[3].text.split()[0]
                # get humidity
                humidity = tds_list[5].text.replace("%", "")
                # get barometer
                barometer = tds_list[6].text.split()[0]
                # write line to CSV file
                f.write(",". join((self.date, time, temp,
                                   wind, humidity, barometer))+"\n")


if __name__ == "__main__":

    # create header
    with open('data/melbourne.18_08_2020.22_08_2020.csv', 'a') as f:
        f.write('date,time,temp,wind,humidity,barometer\n')

    # create Weather objects according to given days
    weather_list = [Weather(i) for i in range(20200818, 20200823)]
    for weather in weather_list:
        # write to CSV
        weather.parseText()

    # load data frame from data/melbourne.18_08_2020.22_08_2020.csv
    df = pd.read_csv('data/melbourne.18_08_2020.22_08_2020.csv')
    
    # compute max temperature for each day
    list_max_temps = compute_max_temp(df)
    print('Max temp for each day: {}'.format(
        ','.join([str(t) for t in list_max_temps])))
