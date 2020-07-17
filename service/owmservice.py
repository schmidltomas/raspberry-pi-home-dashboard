#!/usr/bin/env python3
# coding=utf-8

import requests

"""Service for fetching weather data from openweathermap.org."""


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
		return requests.get(url=self.url, params=params)

	def get_icon_url(self, icon_id):
		return self.icon_url + str(icon_id) + '@2x.png'
