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
import config
import constants
import locale

from service.metservice import METService
from service.rssservice import RSSService
from service.gdmservice import GDMService
import logger


class CustomLayout(FloatLayout):
	pass


class Wallpaper(AsyncImage):
	resolution = None

	def __init__(self, **kwargs):
		super(Wallpaper, self).__init__(**kwargs)
		self.resolution = config.general['screen_width'] + 'x' + config.general['screen_height']

		# hack for official Raspberry Pi display
		if self.resolution == "840x400":
			self.resolution = "1800x1080"

	def random_image(self, *args):
		wallpapers = glob.glob("./wallpapers/" + self.resolution + "/*.jpg")
		self.source = wallpapers[random.randint(0, len(wallpapers) - 1)]
		self.reload()
		logger.info("Set random wallpaper=" + self.source)


class TimeWidget(RelativeLayout):
	pass


class Time(Label):
	def update(self, *args):
		self.text = time.strftime("%H:%M")


class Date(Label):
	def update(self, *args):
		if locale.getlocale()[0] == "cs_CZ":
			self.text = time.strftime("%a %d. %B")
		else:
			self.text = time.strftime("%a %d %B")


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


class NewsWidget(RelativeLayout):
	rss_service = None

	def __init__(self, **kwargs):
		super(NewsWidget, self).__init__(**kwargs)
		self.rss_service = RSSService()
		logger.info("Initialized NewsWidget")

		with self.canvas:
			Color(0.15, 0.15, 0.15, .4, mode='rgba')
			RoundedRectangle(pos=(0, -200), size=(760, 300), radius=[(5, 5), (5, 5), (5, 5), (5, 5)])
			Color(1, 1, 1, .2, mode='rgba')
			Line(points=[15, 0, 745, 0])
			Line(points=[15, -100, 745, -100])

	def on_kv_post(self, base_widget):
		logger.info("Initial NewsWidget update")
		self.update()

		for i in range(0, 3):
			# News
			self.children[i].children[0].children[0].update_text()
			self.children[i].children[0].children[1].update_text()
			# NewsImage
			self.children[i].children[1].update_image()

	def update(self, *args):
		data = self.rss_service.fetch_data()

		data_index = 0
		for i in range(2, -1, -1):
			self.children[i].title = data[data_index]['title']
			self.children[i].image_url = data[data_index]['image_url']
			self.children[i].published = data[data_index]['published']
			data_index += 1

		logger.info("Updated NewsWidget data")


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


class GreetingWidget(RelativeLayout):
	pass


class Greeting(Label):
	first_name = None
	locale_short = None

	def __init__(self, **kwargs):
		super(Greeting, self).__init__(**kwargs)
		self.first_name = config.general['first_name']
		self.locale_short = locale.getlocale()[0]
		logger.info("Initialized GreetingWidget")

	def on_kv_post(self, base_widget):
		logger.info("Initial Greeting update")
		self.update()

	def update(self, *args):
		hour = int(time.strftime("%H"))

		if 6 < hour < 12:
			self.text = config.texts[self.locale_short]['morning'] + self.first_name
		elif 12 <= hour < 18:
			self.text = config.texts[self.locale_short]['afternoon'] + self.first_name
		elif 18 <= hour < 21:
			self.text = config.texts[self.locale_short]['evening'] + self.first_name
		elif 21 <= hour < 6:
			self.text = config.texts[self.locale_short]['night'] + self.first_name

		logger.info("Updated GreetingWidget text=" + self.text)


class TrafficWidget(RelativeLayout):
	gdm_service = None
	data = None

	def __init__(self, **kwargs):
		super(TrafficWidget, self).__init__(**kwargs)
		self.gdm_service = GDMService()
		logger.info("Initialized TrafficWidget")

		with self.canvas:
			Color(0.15, 0.15, 0.15, .4, mode='rgba')
			RoundedRectangle(pos=(-25, -25), size=(270, 140), radius=[(5, 5), (5, 5), (5, 5), (5, 5)])

	def on_kv_post(self, base_widget):
		logger.info("Initial TrafficWidget update")
		self.update()
		self.children[1].children[0].update()
		self.children[1].children[1].update()
		self.children[2].update()

	def update(self, *args):
		self.data = self.gdm_service.fetch_data()
		logger.info("Updated TrafficWidget data")


class TrafficTitleLayout(RelativeLayout):
	pass


class Traffic(Label):
	def update(self, *args):
		self.text = self.parent.parent.data['duration_in_traffic']


class TrafficIcon(AsyncImage):
	def update(self, *args):
		self.source = './icons/car.png'
		self.reload()


class TrafficHeaderLayout(RelativeLayout):
	pass


class TrafficHeader(Label):
	def __init__(self, **kwargs):
		super(TrafficHeader, self).__init__(**kwargs)
		self.text = config.texts[locale.getlocale()[0]]['time_to_work']


class MainApp(App):
	logger.info("Started MainApp")
	Config.set('graphics', 'fullscreen', config.general['fullscreen'])
	Config.set('graphics', 'borderless', config.general['borderless'])
	Config.set('graphics', 'width', config.general['screen_width'])
	Config.set('graphics', 'height', config.general['screen_height'])
	Config.set("graphics", "show_cursor", config.general['show_cursor'])
	locale.setlocale(locale.LC_ALL, config.general['locale'])

	def build(self):
		layout = CustomLayout()

		# Wallpaper
		Clock.schedule_interval(layout.ids.wallpaper.random_image, constants.daily)

		# Time widget
		Clock.schedule_interval(layout.ids.time.update, constants.every_second)
		Clock.schedule_interval(layout.ids.time_shadow.update, constants.every_second)
		Clock.schedule_interval(layout.ids.date.update, constants.every_second)
		Clock.schedule_interval(layout.ids.date_shadow.update, constants.every_second)

		# Weather widget
		Clock.schedule_interval(layout.ids.weather_widget.update, constants.every_15_min)

		# Weather widget - today
		Clock.schedule_interval(layout.ids.temperature_0_0.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_0_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_0_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_1.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_1_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_1_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_0_2_label.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_0_2_label_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_2.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_2_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_0_2_icon.update_icon, constants.every_15_min)

		# Weather widget - tomorrow
		Clock.schedule_interval(layout.ids.temperature_1_0.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_0_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_0_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_1.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_1_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_1_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_1_2_label.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_1_2_label_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_2.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_2_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_1_2_icon.update_icon, constants.every_15_min)

		# Weather widget - tomorrow + 1
		Clock.schedule_interval(layout.ids.temperature_2_0.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_0_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_0_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_1.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_1_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_1_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_2_2_label.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_2_2_label_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_2.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_2_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_2_2_icon.update_icon, constants.every_15_min)

		# Weather widget - tomorrow + 2
		Clock.schedule_interval(layout.ids.temperature_3_0.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_0_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_0_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_1.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_1_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_1_icon.update_icon, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_3_2_label.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.weather_3_2_label_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_2.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_2_shadow.update, constants.every_15_min)
		Clock.schedule_interval(layout.ids.temperature_3_2_icon.update_icon, constants.every_15_min)

		# Greeting widget
		Clock.schedule_interval(layout.ids.greeting.update, constants.hourly)
		Clock.schedule_interval(layout.ids.greeting_shadow.update, constants.hourly)

		# News widget
		Clock.schedule_once(layout.ids.news_widget.update)

		Clock.schedule_interval(layout.ids.news_1_image.update_image, constants.every_30_min)
		Clock.schedule_interval(layout.ids.news_1.update_text, constants.every_30_min)
		Clock.schedule_interval(layout.ids.news_1_shadow.update_text, constants.every_30_min)

		Clock.schedule_interval(layout.ids.news_2_image.update_image, constants.every_30_min)
		Clock.schedule_interval(layout.ids.news_2.update_text, constants.every_30_min)
		Clock.schedule_interval(layout.ids.news_2_shadow.update_text, constants.every_30_min)

		Clock.schedule_interval(layout.ids.news_3_image.update_image, constants.every_30_min)
		Clock.schedule_interval(layout.ids.news_3.update_text, constants.every_30_min)
		Clock.schedule_interval(layout.ids.news_3_shadow.update_text, constants.every_30_min)

		# Traffic widget
		Clock.schedule_interval(layout.ids.traffic_widget.update, constants.hourly)
		Clock.schedule_interval(layout.ids.traffic.update, constants.hourly)
		Clock.schedule_interval(layout.ids.traffic_shadow.update, constants.hourly)
		Clock.schedule_interval(layout.ids.traffic_icon.update, constants.hourly)

		logger.info("MainApp built")
		return layout


if __name__ == '__main__':
	MainApp().run()
