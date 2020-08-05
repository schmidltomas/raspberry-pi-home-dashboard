#!/usr/bin/env python3
# coding=utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import Line, RoundedRectangle
from kivy.graphics.context_instructions import Color
from kivy.config import Config
from kivy.clock import Clock

import time
import glob
import random

from service.metservice import METService
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


class WeatherWidget(RelativeLayout):
	met_service = None

	def __init__(self, **kwargs):
		super(WeatherWidget, self).__init__(**kwargs)
		self.met_service = METService()

		with self.canvas:
			Color(1, 1, 1, .1, mode='rgba')
			RoundedRectangle(pos=(-25, -25), size=(985, 240), radius=[(8, 8), (8, 8), (8, 8), (8, 8)])
			Color(1, 1, 1, .2, mode='rgba')
			Line(points=[220, 190, 220, 0])
			Line(points=[470, 190, 470, 0])
			Line(points=[720, 190, 720, 0])

	def update(self, *args):
		data = self.met_service.fetch_data()

		data_index = 11
		for i in range(0, 4):
			for j in range(2, -1, -1):
				self.children[i].children[j].temperature = data[data_index]['temperature']
				self.children[i].children[j].description = data[data_index]['description']
				self.children[i].children[j].weekday = data[data_index]['weekday']
				data_index -= 1


class WeatherDay(RelativeLayout):
	pass


class Weather(RelativeLayout):
	pass


class WeatherLabel(Label):
	def update(self, *args):
		self.text = self.parent.parent.weekday


class WeatherLabelLayout(RelativeLayout):
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


class NewsWidget(RelativeLayout):
	rss_service = None

	def __init__(self, **kwargs):
		super(NewsWidget, self).__init__(**kwargs)
		self.rss_service = RSSService()

		with self.canvas:
			Color(1, 1, 1, .1, mode='rgba')
			RoundedRectangle(pos=(0, -200), size=(760, 300), radius=[(8, 8), (8, 8), (8, 8), (8, 8)])
			Color(1, 1, 1, .2, mode='rgba')
			Line(points=[15, 0, 745, 0])
			Line(points=[15, -100, 745, -100])

	def update(self, *args):
		data = self.rss_service.fetch_data()

		data_index = 0
		for i in range(2, -1, -1):
			self.children[i].title = data[data_index]['title']
			self.children[i].image_url = data[data_index]['image_url']
			self.children[i].published = data[data_index]['published']
			data_index += 1


class NewsLine(RelativeLayout):
	pass


class NewsTitle(RelativeLayout):
	pass


class News(Label):
	def __init__(self, **kwargs):
		super(News, self).__init__(**kwargs)
		self.bind(size=self.concat_length)

	def update_text(self, *args):
		self.text = self.parent.parent.published + ' • ' + self.parent.parent.title

	def concat_length(self, *args):
		if self.size[1] <= 32:
			self.text = self.text + '\n '

		if self.size[1] > 89:
			self.text = self.text[0:89] + '...'


class NewsImage(AsyncImage):
	def update_image(self, *args):
		self.source = self.parent.image_url
		self.reload()


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

		# Wallpaper
		# Clock.schedule_once(layout.ids.wallpaper.random_image, 1)

		# Time widget
		Clock.schedule_interval(layout.ids.time.update, 1)
		Clock.schedule_interval(layout.ids.time_shadow.update, 1)
		Clock.schedule_interval(layout.ids.date.update, 1)
		Clock.schedule_interval(layout.ids.date_shadow.update, 1)

		# Weather widget
		Clock.schedule_once(layout.ids.weather_widget.update, 1)

		# Weather widget - today
		Clock.schedule_once(layout.ids.temperature_0_0.update, 1)
		Clock.schedule_once(layout.ids.temperature_0_0_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_0_0_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.temperature_0_1.update, 1)
		Clock.schedule_once(layout.ids.temperature_0_1_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_0_1_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.weather_0_2_label.update, 1)
		Clock.schedule_once(layout.ids.weather_0_2_label_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_0_2.update, 1)
		Clock.schedule_once(layout.ids.temperature_0_2_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_0_2_icon.update_icon, 1)

		# Weather widget - tomorrow
		Clock.schedule_once(layout.ids.temperature_1_0.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_0_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_0_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.temperature_1_1.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_1_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_1_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.weather_1_2_label.update, 1)
		Clock.schedule_once(layout.ids.weather_1_2_label_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_2.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_2_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_1_2_icon.update_icon, 1)

		# Weather widget - tomorrow + 1
		Clock.schedule_once(layout.ids.temperature_2_0.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_0_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_0_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.temperature_2_1.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_1_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_1_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.weather_2_2_label.update, 1)
		Clock.schedule_once(layout.ids.weather_2_2_label_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_2.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_2_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_2_2_icon.update_icon, 1)

		# Weather widget - tomorrow + 2
		Clock.schedule_once(layout.ids.temperature_3_0.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_0_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_0_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.temperature_3_1.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_1_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_1_icon.update_icon, 1)
		Clock.schedule_once(layout.ids.weather_3_2_label.update, 1)
		Clock.schedule_once(layout.ids.weather_3_2_label_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_2.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_2_shadow.update, 1)
		Clock.schedule_once(layout.ids.temperature_3_2_icon.update_icon, 1)

		# News widget
		Clock.schedule_once(layout.ids.news_widget.update, 1)

		Clock.schedule_once(layout.ids.news_1_image.update_image, 1)
		Clock.schedule_once(layout.ids.news_1.update_text, 1)
		Clock.schedule_once(layout.ids.news_1_shadow.update_text, 1)

		Clock.schedule_once(layout.ids.news_2_image.update_image, 1)
		Clock.schedule_once(layout.ids.news_2.update_text, 1)
		Clock.schedule_once(layout.ids.news_2_shadow.update_text, 1)

		Clock.schedule_once(layout.ids.news_3_image.update_image, 1)
		Clock.schedule_once(layout.ids.news_3.update_text, 1)
		Clock.schedule_once(layout.ids.news_3_shadow.update_text, 1)

		return layout


if __name__ == '__main__':
	MainApp().run()
