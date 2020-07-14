#!/usr/bin/env python3
# coding=utf-8

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.config import Config
from kivy.uix.label import Label


class CustomLayout(FloatLayout):
	pass


class MainApp(App):

	Config.set('graphics', 'width', '1920')
	Config.set('graphics', 'height', '1080')

	def build(self):
		custom = CustomLayout()
		custom.add_widget(
			AsyncImage(
				source="./wallpapers/01947_atouchofred_1920x1080.jpg",
				size_hint=(1, 1),
				pos_hint={'center_x': .5, 'center_y': .5}))

		custom.add_widget(
			Label(
				text="Temperature: 26°C",
				font_name='./fonts/Roboto-Regular.ttf',
				font_size=50,
				valign='top',
				halign='left'))

		return custom


if __name__ == '__main__':
	MainApp().run()
