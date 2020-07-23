#!/usr/bin/env python3
# coding=utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import Line
from kivy.config import Config
from kivy.clock import Clock

import time
import glob
import random

from service.owmservice import OWMService
from service.rssservice import RSSService


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
	temp = None

	def update(self, *args):
		self.text = str(str(self.temp).split(".")[0]) + "°C"


class TemperatureIcon(AsyncImage):
	icon = None

	def update_icon(self, *args):
		owm_service = OWMService()
		self.source = owm_service.get_icon_url(self.icon)
		self.reload()


class News(Label):
	def __init__(self, **kwargs):
		super(News, self).__init__(**kwargs)

		# with self.canvas:
		# 	Line(points=[20, 150, 500, 150])
		# 	Line(points=[20, 50, 500, 50])

	def update(self, *args):
		rssservice = RSSService()
		data = rssservice.fetch_data()
		self.text = data


class Greeting(Label):
	def __init__(self, **kwargs):
		super(Greeting, self).__init__(**kwargs)
		hour = int(time.strftime("%H"))
		name = "Tomáš"

		if 6 < hour < 11:
			self.text = "Good morning, " + name
		elif 12 < hour < 17:
			self.text = "Good afternoon, " + name
		elif 18 < hour < 21:
			self.text = "Good evening, " + name
		elif 22 < hour < 5:
			self.text = "Good night, " + name


class MainApp(App):
	# Config.set('graphics', 'fullscreen', 1)
	Config.set('graphics', 'width', '1920')
	Config.set('graphics', 'height', '1080')
	# Config.set('graphics', 'width', '840')
	# Config.set('graphics', 'height', '400')

	def build(self):
		layout = CustomLayout()
		# Clock.schedule_once(layout.ids.wallpaper.random_image, 1)

		Clock.schedule_interval(layout.ids.time.update, 1)
		Clock.schedule_interval(layout.ids.time_shadow.update, 1)
		Clock.schedule_interval(layout.ids.date.update, 1)
		Clock.schedule_interval(layout.ids.date_shadow.update, 1)

		owm_service = OWMService()
		response = owm_service.fetch_data()
		layout.ids.temperature.temp = response.json()['current']['temp']
		layout.ids.temperature_shadow.temp = response.json()['current']['temp']
		layout.ids.temperature_icon.icon = response.json()['current']['weather'][0]['icon']

		layout.ids.temperature_1.temp = response.json()['daily'][1]['temp']['day']
		layout.ids.temperature_1_shadow.temp = response.json()['daily'][1]['temp']['day']
		layout.ids.temperature_1_icon.icon = response.json()['daily'][1]['weather'][0]['icon']

		layout.ids.temperature_2.temp = response.json()['daily'][2]['temp']['day']
		layout.ids.temperature_2_shadow.temp = response.json()['daily'][2]['temp']['day']
		layout.ids.temperature_2_icon.icon = response.json()['daily'][2]['weather'][0]['icon']

		layout.ids.temperature_3.temp = response.json()['daily'][3]['temp']['day']
		layout.ids.temperature_3_shadow.temp = response.json()['daily'][3]['temp']['day']
		layout.ids.temperature_3_icon.icon = response.json()['daily'][3]['weather'][0]['icon']

		Clock.schedule_once(layout.ids.temperature.update, 1)
		Clock.schedule_once(layout.ids.temperature_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_icon.update_icon, 1)

		Clock.schedule_once(layout.ids.temperature_1.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_icon.update_icon, 1)

		Clock.schedule_once(layout.ids.temperature_2.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_icon.update_icon, 1)

		Clock.schedule_once(layout.ids.temperature_3.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_icon.update_icon, 1)

		Clock.schedule_once(layout.ids.news_1.update, 1)
		Clock.schedule_once(layout.ids.news_1_shadow.update, 1)

		return layout


if __name__ == '__main__':
	MainApp().run()
