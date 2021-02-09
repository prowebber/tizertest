from machine import PWM, Pin, Timer
from utime import sleep_ms, ticks_ms, ticks_diff

class Button:
	def __init__(self, pin):
		self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
		self.hold_ms = 500
		self.pressed_time = None
		self.enabled = True
		self.f_press = None
		self.f_click = None
		self.f_hold = None
		self.f_end_hold = None
		self.held = False
		self.set_irq()

	def on_change(self, val):
		# @todo allow args/kwargs in event callbacks
		if self.enabled:
			if val:
				self.click()
			else:
				self.press()
		elif self.held and val and self.f_end_hold:
			self.f_end_hold()
			self._reset()

	def on_press(self, callback):
		self.f_press = callback

	def on_click(self, callback):
		self.f_click = callback

	def on_hold(self, callback, end_hold = None, hold_ms = 500):
		self.f_hold = callback
		self.hold_ms = hold_ms
		self.f_end_hold = end_hold

	def press(self):
		self.pressed_time = ticks_ms()
		if self.f_press:
			self.f_press()
		# check in hold_ms for hold
		t_single(self.hold_ms, self._check_hold)

	def click(self):
		self.enabled = False
		self._reset()
		if self.f_click:
			self.f_click()
		self.enabled = True

	def set_irq(self):
		self.button.irq(lambda p: self.on_change(p.value()))

	def _check_hold(self):
		# @todo set to allow click to stop (for spraying)
		if self.pressed_time and self.f_hold:
			self.held = True
			self.enabled = False
			print('button held')
			self.f_hold()

	def _reset(self):
		self.pressed_time = None
		self.held = False
		self.enabled = True


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
		t_single(timeout_ms, self.timeout)
		# Timer(-1).init(period = timeout_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.timeout())
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


def duty_val(val, max_val = 100):
	return 1023 - int(val / max_val * 1023)



def t_single(per, f):
	# to shorten code @todo add args/kwargs to f
	Timer(-1).init(period = per, mode = Timer.ONE_SHOT, callback = lambda t: f())
