#!/usr/bin/env python3
# coding=utf-8

import requests

"""Service for fetching weather data from openweathermap.org."""


class OWMService:
	url = "http://api.openweathermap.org/data/2.5/weather"
	icon_url = "http://openweathermap.org/img/wn/"
	city = "Brno"
	api_key = "<API_KEY>"

	def fetch_data(self):
		params = {'q': self.city, 'appid': self.api_key, 'units': 'metric'}
		response = requests.get(url=self.url, params=params)
		return response

	def get_icon_url(self, icon_id):
		return self.icon_url + str(icon_id) + '@2x.png'
