#!/usr/bin/env python3
# coding=utf-8

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import Line, RoundedRectangle
from kivy.graphics.context_instructions import Color

import config
import locale
import logger

from service.metservice import METService


class WeatherWidget(RelativeLayout):
	met_service = None

	def __init__(self, **kwargs):
		super(WeatherWidget, self).__init__(**kwargs)
		self.met_service = METService()
		logger.info("Initialized WeatherWidget")

		with self.canvas:
			Color(0.15, 0.15, 0.15, .4, mode='rgba')
			RoundedRectangle(pos=(-25, -25), size=(985, 240), radius=[(5, 5), (5, 5), (5, 5), (5, 5)])
			Color(1, 1, 1, .2, mode='rgba')
			Line(points=[220, 190, 220, 0])
			Line(points=[470, 190, 470, 0])
			Line(points=[720, 190, 720, 0])

	def on_kv_post(self, base_widget):
		logger.info("Initial WeatherWidget update")
		self.update()

		for i in range(0, 4):
			for j in range(0, 3):
				# TemperatureIcon
				self.children[i].children[j].children[0].children[0].update_icon()
				# Temperature
				self.children[i].children[j].children[1].children[0].update()
				self.children[i].children[j].children[1].children[1].update()
				if j == 0:
					self.children[i].children[j].children[2].children[0].update()
					self.children[i].children[j].children[2].children[1].update()

	def update(self, *args):
		data = self.met_service.fetch_data()

		data_index = 11
		for i in range(0, 4):
			for j in range(2, -1, -1):
				self.children[i].children[j].temperature = data[data_index]['temperature']
				self.children[i].children[j].description = data[data_index]['description']
				self.children[i].children[j].weekday = data[data_index]['weekday']
				data_index -= 1

		logger.info("Updated WeatherWidget data")


class WeatherDay(RelativeLayout):
	pass


class Weather(RelativeLayout):
	pass


class WeatherHeader(Label):
	def update(self, *args):
		if self.parent.parent.weekday == "TODAY":
			self.text = config.texts[locale.getlocale()[0]]['today']
		else:
			self.text = self.parent.parent.weekday


class WeatherHeaderLayout(RelativeLayout):
	pass


class TemperatureLabelLayout(RelativeLayout):
	pass


class Temperature(Label):
	def update(self, *args):
		self.text = self.parent.parent.temperature


class TemperatureIcon(AsyncImage):
	def update_icon(self, *args):
		self.source = './icons/' + self.parent.parent.description + '.png'
		self.reload()


class TemperatureIconLayout(RelativeLayout):
	pass
