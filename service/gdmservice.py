#!/usr/bin/env python3
# coding=utf-8

import googlemaps
from datetime import datetime
import config
import logger
import json

"""Service for fetching traffic time data from Google Distance Matrix API."""


class GDMService:
	origin = config.gdm_service['origin']
	destination = config.gdm_service['destination']
	mode = config.gdm_service['mode']
	units = config.gdm_service['units']
	language = config.gdm_service['language']
	api_key = config.gdm_service['api_key']
	client = googlemaps.Client(key=api_key)

	def fetch_data(self):
		# 5 minutes from now
		departure_timestamp = datetime.timestamp(datetime.now()) + 300
		departure_time = datetime.fromtimestamp(departure_timestamp).strftime('%Y-%m-%d %H:%M:%S')
		logger.info("Fetching traffic time data for=" + departure_time)

		response = self.client.distance_matrix(
			origins=[self.origin], destinations=[self.destination], mode=self.mode,
			departure_time=departure_timestamp, units=self.units, language=self.language)

		data = {
			"distance": response['rows'][0]['elements'][0]['distance']['text'],
			"duration": response['rows'][0]['elements'][0]['duration']['text'],
			"duration_in_traffic": response['rows'][0]['elements'][0]['duration_in_traffic']['text']
		}

		logger.info("Fetched GDMService data=" + json.dumps(data, ensure_ascii=False))
		return data
