from core.config_man import get_config, save_config
from machine import Pin, Timer, PWM
from project.pins import *
from project.colors import *
from project.devices import RGBLED, LED, Button
from project.tones import Speaker
from project.rest_api import Rest
from utime import sleep_ms, ticks_ms, ticks_diff


class Main:
	def __init__(self):
		self.switch_wifi = Button(D1)
		self.switch_foot = Button(D2)
		self.speaker = Speaker(D6)
		self.led = LED(D8)
		self.pump = Pin(D7, Pin.OUT, value = 0)  # green
		self.relay = Pin(D5, Pin.OUT, value = 0)  # green

		# # Timers
		self.pump_timer = Timer(1)
		self.relay_timer = Timer(4)
		self.relay_on_time = None
		# Set hold time to 2sec on wifi button
		self.switch_wifi.hold_ms = 2000

		self.update_params()
		self.api = Rest()

		# API params
		self.device_id = None
		self.doypack_id = None
		self.wifi_status = False

	def start(self):
		print('project main started')

		# Play tritone on boot
		if not self.mute:
			self.speaker.play_tones(['C5', 'E5', 'G5'])  # Play tritone
		while True:
			if self.switch_wifi.held:
				print('wifi broadcast')
				self.switch_wifi.reset()
			if self.switch_foot.released:
				self.run_device()
			elif self.switch_foot.held:
				self.run_device(timeout = 10000)

	def run_device(self, timeout = None):
		"""
		Run the Shoetizer one time, up to timeout ms
		"""
		print('run device')
		self.update_params()
		if not self.mute:  # Play note (if enabled)
			self.speaker.play_tones(['G5'])
		self.pump_timer.init(period = self.pump_delay_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.pump_on())
		self.relay_timer.init(period = self.relay_delay_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.relay_on(timeout))

		save_config(self.config)

	def pump_on(self):
		"""
		Run the pump
		"""
		print('pump_on')
		self.pump.on()

		self.pump_timer.init(period = self.pump_run_time_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.pump_off())

	def pump_off(self):
		"""
		Turn off the pump
		"""
		print('pump_off')
		self.pump.off()

	def relay_on(self, timeout):
		print('relay_on')
		per = timeout if timeout else self.relay_open_time_ms
		self.relay.on()
		self.relay_on_time = ticks_ms()
		self.relay_timer.init(period = per, mode = Timer.ONE_SHOT, callback = lambda t: self.relay_off())

	def relay_off(self):
		print('relay_off')
		self.relay.off()
		relay_duration = ticks_diff(ticks_ms(), self.relay_on_time)
		self.config['total_unit_spray_time'] += relay_duration
		self.config['total_doypack_spray_time'] += relay_duration

		if self.wifi_status == '1':
			response = self.api.post('/tizer/devices/' + self.device_id + '/usage', {
				'doypack_id': self.doypack_id,
				'usage_type': 1,
				'duration': relay_duration
			})
			print("API Response:\n", response)

	def update_params(self):
		# Stored Params
		self.config = get_config()  # Get config info
		self.device_id = self.config['device_id']
		self.doypack_id = self.config['doypack_id']
		self.wifi_status = self.config['wifi_status']
		self.burst_count = int(self.config['spray_burst_count'])
		self.mute = int(self.config['mute'])
		self.pump_delay_ms = int(self.config['pump_delay_ms'])
		self.pump_run_time_ms = int(self.config['pump_run_time_ms'])
		self.relay_delay_ms = int(self.config['relay_delay_ms'])
		self.relay_open_time_ms = int(self.config['relay_open_time_ms'])
		self.total_unit_spray_time = int(self.config['total_unit_spray_time'])
		self.total_doypack_spray_time = int(self.config['total_doypack_spray_time'])
