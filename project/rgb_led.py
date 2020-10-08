from machine import PWM, Pin
from math import sin, pi
from project.pins import *
from project.colors import *


class RGBLED:
	def __init__(self, r_pin, g_pin, b_pin):
		freq = 1000
		self.R = PWM(r_pin, freq = freq)
		self.G = PWM(g_pin, freq = freq)
		self.B = PWM(b_pin, freq = freq)

	def rgb_color(self, rgb):
		r, g, b = rgb
		self.R.duty(duty_val(r, 255))
		self.G.duty(duty_val(g, 255))
		self.B.duty(duty_val(b, 255))

	def pulse(self, t):
		for i in range(200):
			gain = sin(i / 100 * pi)
			[led.duty(int(led.duty() * gain)) for led in [self.R, self.G, self.B]]
			print('led duty: ', gain)


def duty_val(val, max_val = 100):
	return 1023 - int(val / max_val * 1023)

# led = RGBLED(Pin(D6), Pin(D7), Pin(D8))
# led.rgb_color(magenta)
