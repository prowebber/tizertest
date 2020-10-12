from core.config_man import get_config, save_config
from machine import Pin, Timer, PWM
from project.pins import *
from project.colors import *
from project.devices import RGBLED, LED
from project.tones import Speaker
from project.rest_api import Rest
from utime import sleep_ms, ticks_ms, ticks_diff


class Main:
	def __init__(self):

		self.switch_wifi = Pin(D1, Pin.IN, Pin.PULL_UP)
		self.switch_foot = Pin(D2, Pin.IN, Pin.PULL_UP)
		self.rgbled = RGBLED(Pin(SD2, Pin.OUT), Pin(D3), Pin(D4), Pin(D5))
		self.led = LED(Pin(SD3))
		self.speaker = Speaker(Pin(D6))
		self.pump = Pin(D7, Pin.OUT, value = 0)  # green
		self.relay = Pin(D8, Pin.OUT, value = 0)  # green

		# Timers
		self.pump_timer = Timer(1)
		self.relay_timer = Timer(4)

		self.pressed_time = None
		self.update_params()
		self.api = Rest()
		
		# API params
		self.device_id = None
		self.doypack_id = None
		self.wifi_status = False

	def start(self):
		print('project main started')
		self.led.blink(timeout_ms = 6000)

		self.rgbled.rgb_color(blue)
		sleep_ms(1000)

		#
		# self.rgbled.pulse(timeout_ms = 5500)
		# # Play melody on boot
		# if not self.mute:
		# 	self.speaker.play_tones(['C5', 'E5', 'G5'])  # Play tritone
		# while True:
		# 	switch_wifi_status = self.check_switch(self.switch_wifi, 2000)
		# 	if switch_wifi_status == 'held':
		# 		from main import setup
		# 		setup()
		# 		continue
		# 	elif switch_wifi_status == 'pressed':
		# 		continue
		# 	switch_foot_status = self.check_switch(self.switch_foot)
		# 	if switch_foot_status == 'released':
		# 		self.run_device()

	def check_switch(self, switch, hold_ms = 500):
		first = not switch.value()
		sleep_ms(100)
		second = not switch.value()
		status = None
		if first and not second:
			# return 'released'
			status = 'released'
		elif second and not first:
			status = 'pressed'
		# 	# return None
		elif first and second and ticks_diff(ticks_ms(), self.pressed_time) >= hold_ms:
			status = 'held'
		return status

	def switch_held(self):
		self.pressed_time = None

	def run_device(self):
		"""
		Run the Shoetizer for 1 iteration
		"""
		print('run device')
		self.update_params()

		for i in range(self.burst_count):  # Repeat for each burst
			if not self.mute:  # Play note (if enabled)
				self.speaker.play_tones(['G5'])
			#
			self.pump_timer.init(period = self.pump_delay_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.pump_on())
			self.relay_timer.init(period = self.relay_delay_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.relay_on())

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

	def relay_on(self):
		print('relay_on')
		self.relay.on()
		self.relay_timer.init(period = self.relay_open_time_ms, mode = Timer.ONE_SHOT, callback = lambda t: self.relay_off())

	def relay_off(self):
		print('relay_off')
		self.relay.off()
		self.config['total_unit_spray_time'] += self.relay_open_time_ms
		self.config['total_doypack_spray_time'] += self.relay_open_time_ms
		
		if self.wifi_status == '1':
			response = self.api.post('/tizer/devices/' + self.device_id + '/usage', {
				'doypack_id': self.doypack_id,
				'usage_type': 1,
				'duration': self.relay_open_time_ms
			})
			print("API Response:")
			print(response)
		

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


def play_melody(notes_list, volume = 10):
	from project.tones import play_tones

	play_tones(notes_list, volume = volume)
