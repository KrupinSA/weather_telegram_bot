import requests
from bs4 import BeautifulSoup
import re

RAW_URL = "https://yandex.ru/pogoda/perm/month"
API_URL = ''

START_ROW = 1
END_ROW = 6

response = requests.get(RAW_URL, )

response.raise_for_status()
soup = BeautifulSoup(response.content, 'lxml')

raw_climate_calendar = soup.find_all('div', class_ = 'climate-calendar__row')

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
        pressure = other_data[0].find_all('td')[1].text
        humidity = other_data[1].find_all('td')[1].text
        climate_calendar[cur_data] = temp, rain, pressure, humidity