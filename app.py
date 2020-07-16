#!/usr/bin/env python3
# coding=utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.config import Config
from kivy.uix.label import Label
from kivy.clock import Clock

import time
import glob
import random

from service.owmservice import OWMService


class CustomLayout(FloatLayout):
	pass


class Wallpaper(AsyncImage):
	def random_image(self, *args):
		wallpapers = glob.glob("./wallpapers/*.jpg")
		self.source = wallpapers[random.randint(0, len(wallpapers) - 1)]
		self.reload()


class Time(Label):
	def update(self, *args):
		# self.text = time.strftime("%H:%M:%S")
		self.text = time.strftime("%H:%M")


class Date(Label):
	def update(self, *args):
		# self.text = time.strftime("%A %d %B %Y")
		self.text = time.strftime("%a %d %B")


class Temperature(Label):
	def update(self, *args):
		owm_service = OWMService()
		response = owm_service.fetch_data()
		temp = response.json()['main']['temp']
		self.text = str(str(temp).split(".")[0]) + "°C"


class TemperatureIcon(AsyncImage):
	def fetch_image(self, *args):
		weather = OWMService()
		response = weather.fetch_data()
		icon_url = weather.get_icon_url(response.json()['weather'][0]['icon'])
		self.source = icon_url
		self.reload()


class MainApp(App):

	# Config.set('graphics', 'fullscreen', 1)
	Config.set('graphics', 'width', '1920')
	Config.set('graphics', 'height', '1080')

	def build(self):
		layout = CustomLayout()
		Clock.schedule_once(layout.ids.wallpaper.random_image, 1)
		Clock.schedule_interval(layout.ids.time.update, 1 / 1.)
		Clock.schedule_interval(layout.ids.time_shadow.update, 1 / 1.)
		Clock.schedule_interval(layout.ids.date.update, 1 / 1.)
		Clock.schedule_interval(layout.ids.date_shadow.update, 1 / 1.)

		# TODO redundant API call
		Clock.schedule_once(layout.ids.temperature.update, 1)
		Clock.schedule_once(layout.ids.temperature_icon.fetch_image, 1)

		return layout


if __name__ == '__main__':
	MainApp().run()
