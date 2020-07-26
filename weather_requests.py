import requests
from bs4 import BeautifulSoup
import re

RAW_URL = "https://yandex.ru/pogoda/yaroslavl/month"
API_URL = ''

START_ROW = 1
END_ROW = 6

def get_raw_climate():
    response = requests.get(RAW_URL, )

    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')

    return soup.find_all('div', class_ = 'climate-calendar__row')

def get_weathers():
    raw_climate_calendar = get_raw_climate()
    climate_calendar = {}
    for cur_row in range(START_ROW, END_ROW):
        week = raw_climate_calendar[cur_row].find_all('div', class_ = 'climate-calendar__cell')
        for cur_day in week:
            cur_day = cur_day.find('div', class_ = 'climate-calendar-day__detailed-container')
            cur_data = cur_day.find('h6').text.split(',')[0] # Берем число, месяц.
            rain = cur_day.find('img').attrs['src']
            rain = re.search(r'/[a-z\.\-_]+$', rain).group(0)[1:] # что-то типа ovc_ra.svg
            if re.search(r'ra', rain):
                rain = "Возможны осадки"
            else:
                rain = "Без осадков"
            temp = cur_day.find('span', class_ = 'temp__value').text
            other_data = cur_day.find_all('tr', class_ = 'climate-calendar-day__detailed-data-table-row')
            pressure = other_data[0].find_all('td')[1].text #давление
            humidity = other_data[0].find_all('td')[3].text #Влажность
            climate_calendar[cur_data] = temp, rain, pressure, humidity
    return climate_calendar

