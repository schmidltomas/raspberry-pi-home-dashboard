#!/usr/bin/env python3
# coding=utf-8

import requests
import json
import os
import dateutil.parser
from datetime import date

"""Service for fetching weather data from MET Weather API (https://api.met.no/doc/)."""


def get_cache_content():
	cache_file = open("./cache.json", "r")
	cache = cache_file.read()
	return json.loads(cache)


def save_to_cache(response):
	os.remove('./cache.json')
	cache_file = open("./cache.json", "w")
	cache_dict = {
		"last_modified": response.headers['Last-Modified'],
		"content": response.json()
	}
	cache_file.write(json.dumps(cache_dict))


def parse_description(time_series, i):
	next_6_hours = time_series[i]['data'].get('next_6_hours')
	if next_6_hours is not None:
		return next_6_hours['summary']['symbol_code']
	else:
		return "no description"


def format_temperature(temperature):
	return str(str(temperature).split(".")[0]) + "°C"


def format_weekday(dt):
	if dt.date() == date.today():
		return "TODAY"
	else:
		return dt.strftime('%A').upper()


class METService:
	url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
	user_agent = "RaspberryPiHomeDashboard/0.1 https://github.com/schmidltomas"
	lat = "49.195"
	lon = "16.608"
	altitude = "220"

	def fetch_data(self):
		cache = get_cache_content()

		params = {'lat': self.lat, 'lon': self.lon, 'altitude': self.altitude}
		headers = {'User-Agent': self.user_agent, 'If-Modified-Since': cache['last_modified']}
		response = requests.get(url=self.url, params=params, headers=headers)

		if response.status_code == 304:
			print(str(response.status_code) + " - Loading from cache...")
			time_series = cache['content']['properties']['timeseries']
		else:
			print(str(response.status_code) + " - Fetching new request...")
			save_to_cache(response)
			time_series = response.json()['properties']['timeseries']

		data = []
		for i in range(len(time_series)):
			dt = dateutil.parser.isoparse(time_series[i]['time'])

			# if dt.time().hour == 6 or dt.time().hour == 12 or dt.time().hour == 18:
			if dt.time().hour == 12:
				data.append({
					"timestamp": time_series[i]['time'],
					"weekday": format_weekday(dt),
					"temperature": format_temperature(time_series[i]['data']['instant']['details']['air_temperature']),
					"description": parse_description(time_series, i)
				})

		return data

