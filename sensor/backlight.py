#!/usr/bin/env python3
# coding=utf-8

import RPi.GPIO as GPIO
import time
from rpi_backlight import Backlight

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

backlight = Backlight()


def main():
	try:
		time.sleep(2)  # to stabilize sensor
		start_time = time.time()

		while True:
			elapsed_time = time.time() - start_time
			if elapsed_time > 600:
				backlight.power = False

			if GPIO.input(23) and not backlight.power:
				backlight.power = True
				start_time = time.time()
				time.sleep(5)  # to avoid multiple detection

			time.sleep(0.5)  # loop delay, should be less than detection delay

	except KeyboardInterrupt:
		GPIO.cleanup()
		backlight.power = True
		pass
	except:
		GPIO.cleanup()
		backlight.power = True


if __name__ == '__main__':
	main()
