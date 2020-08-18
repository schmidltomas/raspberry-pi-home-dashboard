#!/usr/bin/env python3
# coding=utf-8

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label

import time
import locale


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
