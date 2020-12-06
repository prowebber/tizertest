from core.config_man import get_config, save_config
from machine import Pin, Timer, PWM
from project.pins import *
from project.devices import LED, Button
from project.tones import Speaker
from project.rest_api import Rest
from utime import ticks_ms, ticks_diff


class Main:
	def __init__(self):
		self.b_wifi = Button(D2)
		self.b_foot = Button(D4)
		self.speaker = Speaker(D5)
		self.led = LED(D8)
		self.pump = Pin(D6, Pin.OUT, value = 0)
		self.relay = Pin(D7, Pin.OUT, value = 0)
		self.t0_relay = None
		self.t_max = None
		self.running = False
		# Set hold time to 2sec on wifi button
		self.b_foot.on_click(self.run)
		self.b_foot.on_hold(self.long_run, self.end_run)
		self.c = get_config()  # Get config info
		self.api = Rest()

	def start(self):
		if self.c['enable_led']:
			self.led.on()
		# Play tritone on boot
		if not self.c['mute']:
			self.speaker.play_tones(['C5', 'E5', 'G5'])
		while True:
			pass

	def run(self, tmax = None):
		self.t_max = tmax
		# Run once up to t_max ms if not running
		if not self.running:
			self.running = True
			# disable switch while running
			self.sync_params()
			if not self.c['mute']:  # Play note (if enabled)
				self.speaker.play_tones(['G5'])
			t_single(self.c['pump_delay'], self.pump_on)
			t_single(self.c['relay_delay'], self.relay_on)

	def long_run(self):
		# timeout in 10sec
		self.run(10000)

	def end_run(self):
		self.pump_off()
		self.relay_off()

	def pump_on(self):
		self.pump.on()
		per = self.t_max if self.t_max else self.c['pump_ms']
		t_single(per, self.pump_off)

	def pump_off(self):
		self.pump.off()

	def relay_on(self):
		per = self.t_max if self.t_max else self.c['relay_ms']
		self.relay.on()
		self.t0_relay = ticks_ms()
		t_single(per, self.relay_off)

	def relay_off(self):
		self.relay.off()

		if self.running:
			relay_duration = ticks_diff(ticks_ms(), self.t0_relay)
			self.c['unit_spray_ms'] += relay_duration
			self.c['bag_spray_ms'] += relay_duration
			save_config(self.c)
			self.running = False
			self.t_max = None


def t_single(per, f):
	# to shorten code
	Timer(-1).init(period = per, mode = Timer.ONE_SHOT, callback = lambda t: f())
