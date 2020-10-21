from core.config_man import get_config, save_config
from machine import Pin, Timer, PWM
from project.pins import *
from project.colors import *
from project.devices import RGBLED, LED, Button
from project.tones import Speaker
from project.rest_api import Rest
from utime import sleep_ms, ticks_ms, ticks_diff
from main import setup


class Main:
	def __init__(self):
		self.b_wifi = Button(D1)
		self.b_foot = Button(D2)

		self.speaker = Speaker(D6)
		self.led = LED(D8)
		self.pump = Pin(D7, Pin.OUT, value = 0)  # green
		self.relay = Pin(D5, Pin.OUT, value = 0)  # green
		self.t0_relay = None
		self.t_max = None
		self.running = False
		# Set hold time to 2sec on wifi button
		self.b_wifi.on_hold(setup, 2000)
		self.b_foot.on_click(self.run)
		self.sync_params()
		print('config: ', self.c)
		self.api = Rest()
		# API params
		self.unit_id = None
		self.bag_id = None
		self.has_wifi = False

	def start(self):
		print('project main started')
		if self.enable_led:
			self.led.on()
		# Play tritone on boot
		if not self.mute:
			self.speaker.play_tones(['C5', 'E5', 'G5'])  # Play tritone
		while True:
			pass

	def run(self, tmax = None):
		self.t_max = tmax
		# Run once up to t_max ms if not running
		if not self.running:
			self.running = True
			# disable switch while running
			print('run...')
			self.sync_params()
			if not self.mute:  # Play note (if enabled)
				self.speaker.play_tones(['G5'])
			t_single(self.pump_delay, self.pump_on)
			t_single(self.relay_delay, self.relay_on)

	def long_run(self):
		# timeout in 10sec
		self.run(10000)

	def pump_on(self):
		print('pump_on')
		self.pump.on()
		per = self.t_max if self.t_max else self.pump_ms
		t_single(per, self.pump_off)

	def pump_off(self):
		print('pump_off')
		self.pump.off()

	def relay_on(self):
		print('relay_on')
		per = self.t_max if self.t_max else self.relay_ms
		self.relay.on()
		self.t0_relay = ticks_ms()
		t_single(per, self.relay_off)

	def relay_off(self):
		print('relay_off')
		self.relay.off()
		relay_duration = ticks_diff(ticks_ms(), self.t0_relay)
		self.unit_spray_ms += relay_duration
		self.bag_spray_ms += relay_duration
		self.c['unit_spray_ms'] = self.unit_spray_ms
		self.c['bag_spray_ms'] = self.bag_spray_ms
		save_config(self.c)

		if self.has_wifi == '1':
			response = self.api.post('/tizer/devices/' + self.unit_id + '/usage', {
				'bag_id': self.bag_id,
				'usage_type': 1,
				'duration': relay_duration
			})
			print("API Response:\n", response)
		self.running = False
		self.t_max = None

	def sync_params(self):
		# Stored Params
		self.c = get_config()  # Get config info
		self.unit_id = self.c['unit_id']
		self.bag_id = self.c['bag_id']
		self.enable_led = self.c['enable_led']
		self.mute = self.c['mute']
		self.pump_delay = self.c['pump_delay']
		self.pump_ms = self.c['pump_ms']
		self.relay_delay = self.c['relay_delay']
		self.relay_ms = self.c['relay_ms']
		self.unit_spray_ms = self.c['unit_spray_ms']
		self.bag_spray_ms = self.c['bag_spray_ms']
		self.has_wifi = self.c['has_wifi']


def t_single(per, f):
	# to shorten code
	Timer(-1).init(period = per, mode = Timer.ONE_SHOT, callback = lambda t: f())
