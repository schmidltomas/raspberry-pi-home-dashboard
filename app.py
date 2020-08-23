#!/usr/bin/env python3
# coding=utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.clock import Clock

import config
import constants
import locale
import logger

from widgets.greeting import Greeting
from widgets.news import NewsWidget, NewsImage, News
from widgets.time_and_date import Time, Date
from widgets.traffic import TrafficWidget, TrafficHeader, TrafficIcon, Traffic
from widgets.wallpaper import Wallpaper
from widgets.weather import WeatherWidget, Weather, Temperature, TemperatureIcon


class CustomLayout(FloatLayout):
	pass


class MainApp(App):
	logger.info("Started MainApp")
	Config.set('graphics', 'fullscreen', config.general['fullscreen'])
	Config.set('graphics', 'borderless', config.general['borderless'])
	Config.set('graphics', 'width', config.general['screen_width'])
	Config.set('graphics', 'height', config.general['screen_height'])
	Config.set('graphics', 'show_cursor', config.general['show_cursor'])
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
		Clock.schedule_interval(layout.ids.weather_widget.update, constants.every_30_min)

		# Weather widget - today
		Clock.schedule_interval(layout.ids.temperature_0_0.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_0_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_0_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_1.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_1_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_1_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_0_2_label.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_0_2_label_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_2.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_2_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_0_2_icon.update_icon, constants.every_30_min)

		# Weather widget - tomorrow
		Clock.schedule_interval(layout.ids.temperature_1_0.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_0_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_0_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_1.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_1_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_1_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_1_2_label.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_1_2_label_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_2.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_2_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_1_2_icon.update_icon, constants.every_30_min)

		# Weather widget - tomorrow + 1
		Clock.schedule_interval(layout.ids.temperature_2_0.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_0_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_0_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_1.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_1_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_1_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_2_2_label.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_2_2_label_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_2.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_2_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_2_2_icon.update_icon, constants.every_30_min)

		# Weather widget - tomorrow + 2
		Clock.schedule_interval(layout.ids.temperature_3_0.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_0_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_0_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_1.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_1_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_1_icon.update_icon, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_3_2_label.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.weather_3_2_label_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_2.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_2_shadow.update, constants.every_30_min)
		Clock.schedule_interval(layout.ids.temperature_3_2_icon.update_icon, constants.every_30_min)

		# Greeting widget
		Clock.schedule_interval(layout.ids.greeting_widget.generate_greeting, constants.hourly)
		Clock.schedule_interval(layout.ids.greeting.update, constants.hourly)
		Clock.schedule_interval(layout.ids.greeting_shadow.update, constants.hourly)

		# News widget
		Clock.schedule_interval(layout.ids.news_widget.update, constants.every_30_min)

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
