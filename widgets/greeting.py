#!/usr/bin/env python3
# coding=utf-8

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label

import time
import config
import locale
import logger


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

		if 5 <= hour < 12:
			self.text = config.texts[self.locale_short]['morning'] + self.first_name
		elif 12 <= hour < 18:
			self.text = config.texts[self.locale_short]['afternoon'] + self.first_name
		elif 18 <= hour < 21:
			self.text = config.texts[self.locale_short]['evening'] + self.first_name
		elif 21 <= hour < 5:
			self.text = config.texts[self.locale_short]['night'] + self.first_name

		logger.info("Updated GreetingWidget text=" + self.text)