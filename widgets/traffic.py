#!/usr/bin/env python3
# coding=utf-8

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.graphics.context_instructions import Color

import config
import locale
import logger

from service.gdmservice import GDMService


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