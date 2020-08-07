#!/usr/bin/env python3
# coding=utf-8

import googlemaps
from datetime import datetime

"""Service for fetching traffic time data from Google Distance Matrix API."""


class GDMService:
	origin = "<HOME_ADDRESS>"
	destination = "<WORK_ADDRESS>"
	mode = "driving"
	units = "metric"
	language = "en"
	api_key = "<GOOGLE_API_KEY>"
	client = googlemaps.Client(key=api_key)

	def fetch_data(self):
		# 5 minutes from now
		departure_time = datetime.timestamp(datetime.now()) + 300

		response = self.client.distance_matrix(
			origins=[self.origin], destinations=[self.destination], mode=self.mode,
			departure_time=departure_time, units=self.units, language=self.language)

		return {
			"distance": response['rows'][0]['elements'][0]['distance']['text'],
			"duration": response['rows'][0]['elements'][0]['duration']['text'],
			"duration_in_traffic": response['rows'][0]['elements'][0]['duration_in_traffic']['text']
		}
