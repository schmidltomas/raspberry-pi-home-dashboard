#!/usr/bin/env python3
# coding=utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.config import Config
from kivy.uix.label import Label
from kivy.clock import Clock

import time


class Time(Label):
	def update(self, *args):
		self.text = time.asctime()


class Temperature(Label):
	pass


class Wallpaper(AsyncImage):
	pass


class MainApp(App):

	Config.set('graphics', 'width', '1920')
	Config.set('graphics', 'height', '1080')

	def build(self):
		layout = FloatLayout()
		Clock.schedule_interval(layout.ids.time.update, 1 / 1.)
		return layout


if __name__ == '__main__':
	MainApp().run()
