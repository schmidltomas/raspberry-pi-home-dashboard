#!/usr/bin/env python3
# coding=utf-8

import requests
from datetime import date

"""Service for fetching weather data from openweathermap.org."""


def format_temperature(temperature):
	return str(str(temperature).split(".")[0]) + "°C"


def format_icon_url(icon_id):
	return OWMService.icon_url + str(icon_id) + '@2x.png'


def format_weekday(timestamp):
	weekday_date = date.fromtimestamp(int(timestamp))

	if weekday_date == date.today():
		return "TODAY"
	else:
		return weekday_date.strftime('%A').upper()


class OWMService:
	url = "http://api.openweathermap.org/data/2.5/onecall"
	icon_url = "http://openweathermap.org/img/wn/"
	lat = "49.1953"
	lon = "16.6086"
	units = "metric"
	exclude = "minutely,hourly"
	api_key = "API_KEY"

	def fetch_data(self):
		params = {'lat': self.lat, 'lon': self.lon, 'units': self.units, 'exclude': self.exclude, 'appid': self.api_key}
		response = requests.get(url=self.url, params=params)

		data = []
		for i in range(4):
			data.append({
				"temperature": format_temperature(response.json()['daily'][i]['temp']['day']),
				"description": response.json()['daily'][i]['weather'][0]['description'],
				"icon_url": format_icon_url(response.json()['daily'][i]['weather'][0]['icon']),
				"weekday": format_weekday(response.json()['daily'][i]['dt'])
			})

		return data

