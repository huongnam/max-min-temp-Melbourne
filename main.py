import os
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv


def compute_max_temp(df):
    # groups = df.groupby('date')
    # return groups.max()['temp'].values.tolist()
    return list(df.groupby('date')['temp'].max())


class Weather:
    def __init__(self, id, date=None, time=None, temp=None, wind=None,
                 humidity=None, barometer=None):
        self.id = id
        self.url = 'https://www.timeanddate.com/weather/australia/melbourne/historic?hd='\
            + str(self.id)
        self.date = date
        self.time = time
        self.temp = temp

    def getPage(self):
        return requests.get(self.url)

    def parseText(self):
        page = self.getPage()
        soup = BeautifulSoup(page.content, 'html.parser')
        date = str(self.id % 100)
        # table = soup.find(id='wt-his')
        table = soup.find(id='wt-his').tbody
        # print(table)
        with open('data/melbourne.18_08_2020.22_08_2020.csv', 'a') as f:
            # f.write('date,time,temp,wind,humidity,barometer\n')
            for tr in table.findAll('tr'):
                time = tr.find_all('th')[0].text
                # print(time)
                list_tds = tr.find_all('td')
                temp = list_tds[1].text.split()[0]
                wind = list_tds[3].text.split()[0]
                humidity = list_tds[5].text.replace("%", "")
                barometer = list_tds[6].text.split()[0]
                f.write(",". join((date, time, temp, wind, humidity, barometer))+"\n")



if __name__ == "__main__":
    # load your dataframe from data/melbourne.18_08_2020.22_08_2020.csv

    # compute max temperature for each day

    # print('Max temp for each day: {}'.format(','.join([str(t) for t in ])))
    # print("haha")
    with open('data/melbourne.18_08_2020.22_08_2020.csv', 'a') as f:
        f.write('date,time,temp,wind,humidity,barometer\n')
    weather_list = [Weather(i) for i in range(20200818, 20200823)]
    for weather in weather_list:
        # print(weather)
        weather.parseText()
    # print(w1.url)
    # w1.parseText()
    df = pd.read_csv('data/melbourne.18_08_2020.22_08_2020.csv')
    list_max_temps = compute_max_temp(df)
    # print(compute_max_temp(df))
    # print(df.head(5))
    
    # print(a)
    print('Max temp for each day: {}'.format(','.join([str(t) for t in list_max_temps])))