from machine import PWM, Pin, Timer
from math import sin, pi
from utime import sleep_ms, ticks_ms, ticks_diff
from project.pins import *


class Button:
	def __init__(self, pin):
		self.button = Pin(pin, Pin.OUT, value = 0)
		self.hold_ms = 500
		self.pressed_time = None
		self.enabled = True
		# start recursive state check
		self.check(self.button.value())
		self.pressed = False
		self.released = False
		self.held = False

	def check(self, val_1):
		if self.enabled:
			Timer(-1).init(period = 100, mode = Timer.ONE_SHOT, callback = lambda t: self.check(self.button.value()))
			val_2 = not self.button.value()

			self.pressed = val_2 and not val_1
			if self.pressed:
				self.pressed_time = ticks_ms()

			self.released = val_1 and not val_2
			if self.released:
				print('button released')

			self.held = val_1 and val_2 and ticks_diff(ticks_ms(), self.pressed_time) >= self.hold_ms
			if self.held:
				print('button held')

	def deinit(self):
		self.enabled = False


#
# def pressed(self):
# 	print('button pressed')
#
# def released(self):
# 	print('button released')
#
# def held(self):
# 	print('button held')


class LED:
	def __init__(self, pin):
		self.led = Pin(pin, Pin.OUT, value = 0)
		self.led_timer = Timer(-1)
		self.blink_timer = Timer(-1)
		self.TIMEOUT = False
		self.blinking = False

	def blink(self, freq = 1, timeout_ms = -1):
		Timer(-1).init(period = timeout_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.blink_off(sleep = int(1000 / freq)))
		self.led_timer.init(period = int(1000 / freq), mode = Timer.PERIODIC, callback = lambda t: self.toggle())

	def blink_multi(self, n = 2, freq = 1, timeout_ms = -1):
		Timer(-1).init(period = timeout_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.timeout())
		on_time = int(1000 / freq)
		blink_hz = int(freq * (n + 1))
		self.TIMEOUT = False
		self.blinking = False
		self.blink_timer.init(period = on_time, mode = Timer.PERIODIC, callback = lambda t: self.toggle_blink(n = n, on_time = on_time, blink_hz = blink_hz))

	def blink_off(self, sleep = 0):
		self.led_timer.deinit()
		self.off()

	def timeout(self):
		self.TIMEOUT = True
		self.blink_off()
		self.blink_timer.deinit()

	def toggle(self):
		self.led.value(not self.led.value())

	def toggle_blink(self, n, on_time, blink_hz):
		if self.blinking:
			self.blink_off()
		elif not self.TIMEOUT:
			self.blink(freq = blink_hz, timeout_ms = 2 * n * int(on_time / (n + 1)))
		self.blinking = not self.blinking

	def on(self):
		self.led.on()

	def off(self):
		self.led.off()


class RGBLED:
	def __init__(self, power_pin, r_pin, g_pin, b_pin):
		freq = 1000
		self.power = power_pin
		self.R = PWM(r_pin, freq = freq)
		self.G = PWM(g_pin, freq = freq)
		self.B = PWM(b_pin, freq = freq)

	def pulse(self, freq = 1, timeout_ms = -1):
		self.on()
		leds = [self.R, self.G, self.B]
		init_duties = [duty_val(led.duty(), 1023) for led in leds]
		t0 = ticks_ms()
		timeout = False
		while not timeout:
			for i in range(100):
				if ticks_diff(ticks_ms(), t0) >= timeout_ms:
					timeout = True
					break
				# oscillate from 0 to 1
				gain = sin(i / 50 * pi) * 0.25 + 0.25
				# multiply each channel's init_duty by gain to fade without changing ratios
				[led.duty(duty_val(int(duty * gain), 1023)) for led in leds for duty in init_duties]
				sleep_ms(int(freq * 10))
		self.off()

	def off(self):
		self.power.value(0)
		[led.duty(0) for led in [self.R, self.G, self.B]]

	def on(self):
		self.power.value(1)

	def rgb_color(self, rgb):
		r, g, b = rgb
		self.R.duty(duty_val(r, 255))
		self.G.duty(duty_val(g, 255))
		self.B.duty(duty_val(b, 255))


def duty_val(val, max_val = 100):
	return 1023 - int(val / max_val * 1023)


def test_led():
	led = LED(SD3)
	led.blink_multi(3, 1, 12000)
	switch = Button(D2)
