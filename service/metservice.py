#!/usr/bin/env python3
# coding=utf-8

import requests
import json
import dateutil.parser
from datetime import date
import datetime
import config
import logger

"""Service for fetching weather data from MET Weather API (https://api.met.no/doc/)."""


def get_cache_content():
	try:
		with open("./cache.json", "r") as cache_file:
			cache = cache_file.read()
			return json.loads(cache)
	except ValueError and FileNotFoundError:
		# if the cache is empty, return empty cache object
		emtpy_today = [{
			"timestamp": '',
			"weekday": 'TODAY',
			"temperature": '',
			"description": 'no_image'
		}] * 3
		return json.loads('{"today": ' + json.dumps(emtpy_today) + ', "last_modified": null}')


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
	tomorrow = datetime.date.today() + datetime.timedelta(days=1)

	if dt.date() == date.today():
		return "TODAY"
	elif dt.date() == tomorrow:
		return "TOMORROW"
	else:
		return dt.strftime('%A').upper()


def empty_data():
	data = []
	
	for i in range(12):
		data.append({
			"timestamp": "",
			"weekday": "NO DATA",
			"temperature": "N/A",
			"description": "no_image"
		})
	
	return data
	
	
def get_response(url, params, headers):
	try:
		return requests.get(url=url, params=params, headers=headers)
	except ConnectionError:
		return None


class METService:
	url = config.met_service['url']
	user_agent = config.met_service['user_agent']
	lat = config.met_service['lat']
	lon = config.met_service['lon']
	altitude = config.met_service['altitude']

	def fetch_data(self):
		logger.info("Fetching weather data from=" + self.url)
		cache = get_cache_content()

		params = {'lat': self.lat, 'lon': self.lon, 'altitude': self.altitude}
		headers = {'User-Agent': self.user_agent, 'If-Modified-Since': cache['last_modified']}
		response = get_response(self.url, params, headers)

		if response is None:
			logger.info("Connection error when getting response, returning empty data")
			return empty_data()
		if response.status_code == 304:
			logger.info("Received response=" + str(response.status_code) + ", loading from cache")
			time_series = cache['content']['properties']['timeseries']
		else:
			logger.info("Received response=" + str(response.status_code) + ", fetching new request")
			save_to_cache(response)
			time_series = response.json()['properties']['timeseries']

		data = []
		for i in range(len(time_series)):
			dt = dateutil.parser.isoparse(time_series[i]['time'])

			# if today's forecast doesn't contain earlier hours anymore, load them from cache
			if dt.date() == date.today():
				if len(data) == 0:
					logger.info("Loading 6AM data from cache=" + json.dumps(cache['today'][0], ensure_ascii=False))
					data.append(cache['today'][0])
					continue
				if len(data) == 1:
					logger.info("Loading 12PM data from cache=" + json.dumps(cache['today'][1], ensure_ascii=False))
					data.append(cache['today'][1])
					continue
				if len(data) == 2:
					logger.info("Loading 18PM data from cache=" + json.dumps(cache['today'][2], ensure_ascii=False))
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

		logger.info("Fetched METService data=" + json.dumps(data, ensure_ascii=False))
		return data

