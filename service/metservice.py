#!/usr/bin/env python3
# coding=utf-8

import requests
import json
import dateutil.parser
from datetime import date

"""Service for fetching weather data from MET Weather API (https://api.met.no/doc/)."""


def get_cache_content():
	with open("./cache.json", "r") as cache_file:
		try:
			cache = cache_file.read()
			json_object = json.loads(cache)
		except ValueError:
			# if the cache is empty, return empty cache object
			emtpy_today = [{
				"timestamp": '',
				"weekday": 'TODAY',
				"temperature": '',
				"description": 'no_image'
			}] * 3
			return json.loads('{"today": ' + json.dumps(emtpy_today) + ', "last_modified": null}')

		return json_object


def save_to_cache(response):
	cache = get_cache_content()
	time_series = response.json()['properties']['timeseries']
	today = update_today_forecast(time_series, cache['today'])

	with open("./cache.json", "w") as cache_file:
		cache_dict = {
			"last_modified": response.headers['Last-Modified'],
			"content": response.json(),
			"today": today
		}
		cache_file.write(json.dumps(cache_dict))


def update_today_forecast(time_series, today):
	for i in range(len(time_series)):
		dt = dateutil.parser.isoparse(time_series[i]['time'])

		item = {
			"timestamp": time_series[i]['time'],
			"weekday": format_weekday(dt),
			"temperature": format_temp(time_series[i]['data']['instant']['details']['air_temperature']),
			"description": parse_description(time_series, i)
		}

		if dt.time().hour == 6:
			today[0] = item
		elif dt.time().hour == 12:
			today[1] = item
		elif dt.time().hour == 18:
			today[2] = item

		if dt.date() != date.today():
			break

	return today


def parse_description(time_series, i):
	next_6_hours = time_series[i]['data'].get('next_6_hours')
	if next_6_hours is not None:
		return next_6_hours['summary']['symbol_code']
	else:
		return "no description"


def format_temp(temperature):
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

			# if today's forecast doesn't contain earlier hours anymore, load them from cache
			if dt.date() == date.today():
				if len(data) == 0:
					data.append(cache['today'][0])
					continue
				if len(data) == 1:
					data.append(cache['today'][1])
					continue
				if len(data) == 2:
					data.append(cache['today'][2])
					continue
			else:
				# add forecast for each next day in selected hours - 6, 12 and 18
				if dt.time().hour == 6 or dt.time().hour == 12 or dt.time().hour == 18:
					data.append({
						"timestamp": time_series[i]['time'],
						"weekday": format_weekday(dt),
						"temperature": format_temp(time_series[i]['data']['instant']['details']['air_temperature']),
						"description": parse_description(time_series, i)
					})

			if len(data) == 12:
				break

		return data

