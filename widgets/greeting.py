#!/usr/bin/env python3
# coding=utf-8

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label

import time
import config
import locale
import logger
import random


class GreetingWidget(RelativeLayout):
	first_name = None
	locale_short = None
	greeting_text = None

	def __init__(self, **kwargs):
		super(GreetingWidget, self).__init__(**kwargs)
		self.first_name = config.general['first_name']
		self.locale_short = locale.getlocale()[0]
		logger.info("Initialized GreetingWidget")

	def generate_greeting(self):
		hour = int(time.strftime("%H"))

		texts = config.texts[self.locale_short]
		if 5 <= hour < 12:
			adj_index = random.randint(0, len(texts['morning_afternoon_adjectives']) - 1)
			self.greeting_text = texts['morning_afternoon_adjectives'][adj_index] + texts['morning'] + self.first_name
		elif 12 <= hour < 18:
			adj_index = random.randint(0, len(texts['morning_afternoon_adjectives']) - 1)
			self.greeting_text = texts['morning_afternoon_adjectives'][adj_index] + texts['afternoon'] + self.first_name
		elif 18 <= hour < 21:
			adj_index = random.randint(0, len(texts['evening_adjectives']) - 1)
			self.greeting_text = texts['evening_adjectives'][adj_index] + texts['evening'] + self.first_name
		elif 21 <= hour < 5:
			adj_index = random.randint(0, len(texts['night_adjectives']) - 1)
			self.greeting_text = texts['night_adjectives'][adj_index] + texts['night'] + self.first_name

	def on_kv_post(self, base_widget):
		logger.info("Initial GreetingWidget update")
		self.generate_greeting()
		self.children[0].update()
		self.children[1].update()


class Greeting(Label):
	def update(self, *args):
		self.text = self.parent.greeting_text
		logger.info("Updated GreetingWidget text=" + self.text)
