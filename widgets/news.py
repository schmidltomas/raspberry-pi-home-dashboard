#!/usr/bin/env python3
# coding=utf-8

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import Line, RoundedRectangle
from kivy.graphics.context_instructions import Color

import logger

from service.rssservice import RSSService


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
		if self.size[1] >= 84:
			self.text = self.text[0:92] + '…'


class NewsImage(AsyncImage):
	def update_image(self, *args):
		self.source = self.parent.image_url
		self.reload()
