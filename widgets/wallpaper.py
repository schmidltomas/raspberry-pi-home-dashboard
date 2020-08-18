#!/usr/bin/env python3
# coding=utf-8

from kivy.uix.image import AsyncImage

import glob
import random
import config
import logger


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
