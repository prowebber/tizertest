from machine import PWM, Pin
from math import sin, pi
from utime import sleep_ms, ticks_ms, ticks_diff


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

# led = RGBLED(Pin(D6), Pin(D7), Pin(D8))
# led.rgb_color(magenta)
