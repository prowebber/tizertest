from machine import PWM, Pin
from math import sin, pi
from project.pins import *
from project.colors import *
from utime import sleep_ms, ticks_ms, ticks_diff


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

	def pulse(self, timeout_ms = 0):
		leds = [self.R, self.G, self.B]
		init_duties = [led.duty() for led in leds]
		t0 = ticks_ms()
		while ticks_diff(ticks_ms(), t0) < timeout_ms:
			for i in range(200):
				gain = sin(i / 100 * pi)
				print('gain: ', gain)
				[led.duty(int(duty * gain)) for led in leds for duty in init_duties]
				print('led duty: ', gain)
				sleep_ms(10)


def duty_val(val, max_val = 100):
	return 1023 - int(val / max_val * 1023)

# led = RGBLED(Pin(D6), Pin(D7), Pin(D8))
# led.rgb_color(magenta)
