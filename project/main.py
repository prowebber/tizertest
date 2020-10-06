from assets.config_man import get_config, save_config
from machine import Pin, Timer, PWM
from project.pins import *
from utime import sleep_ms


class Main:
	def __init__(self):
		self.relay = Pin(D8, Pin.OUT, value=0)  # green
		self.pump = Pin(D7, Pin.OUT, value=0)  # green
		self.switch_foot = Pin(D2, Pin.IN, Pin.PULL_UP)
		
		# Timers
		self.pump_timer = Timer(1)
		self.relay_timer = Timer(4)
		
		# Stored Params
		self.config = get_config()  # Get config info
		
	def start(self):
		print("got to start...")
		print("testing....bbbbtest4")
		# Play melody on boot
		if self.config['melody_on_boot']:
			print("playing melody")
			play_melody(['C5', 'E5', 'G5'])  # Play tritone
		
		while True:
			if self.is_switch_pressed():  # If the foot bttn is pressed
				self.run_device()
	
	def is_switch_pressed(self):
		"""
		Determine if the foot button has been pressed
		:return: bool - True if pressed, False if not
		"""
		first = not self.switch_foot.value()
		sleep_ms(100)
		second = not self.switch_foot.value()
		
		return first and not second
	
	def run_device(self):
		"""
		Run the Shoetizer for 1 iteration
		"""
		self.config = get_config()  # Get config info (since it has been updated)
		
		burst_count = int(self.config['spray_burst_count'])
		melody_on_spray = int(self.config['melody_on_spray'])
		pump_delay_ms = int(self.config['pump_delay_ms'])
		relay_delay_ms = int(self.config['relay_delay_ms'])
		relay_open_time_ms = int(self.config['relay_open_time_ms'])
		total_unit_spray_time = int(self.config['total_unit_spray_time'])
		total_doypack_spray_time = int(self.config['total_doypack_spray_time'])
		
		for i in range(burst_count):  # Repeat for each burst
			
			if melody_on_spray == 1:  # Play note (if enabled)
				play_melody(['G5'])
			
			self.pump_timer.init(period=pump_delay_ms, mode=Timer.ONE_SHOT, callback=lambda t: self.pump_on())
			self.relay_timer.init(period=relay_delay_ms, mode=Timer.ONE_SHOT, callback=lambda t: self.relay_on())
			
			# Track how long the unit and doypack have sprayed solution
			self.config['total_unit_spray_time'] = total_unit_spray_time + relay_open_time_ms
			self.config['total_doypack_spray_time'] = total_doypack_spray_time + relay_open_time_ms
			
		save_config(self.config)
		
	def pump_on(self):
		"""
		Run the pump
		"""
		per = self.config['pump_run_time_ms']
		self.pump.on()
		self.pump_timer.init(period=per, mode=Timer.ONE_SHOT, callback=lambda t: self.pump_off())
		
	def pump_off(self):
		"""
		Turn off the pump
		"""
		self.pump.off()
	
	def relay_on(self):
		per = self.config['relay_open_time_ms']
		self.relay.on()
		self.relay_timer.init(period=per, mode=Timer.ONE_SHOT, callback=lambda t: self.relay_off())
	
	def relay_off(self):
		self.relay.off()


def play_melody(notes_list, volume=10):
	from project.tones import play_tones
	
	play_tones(notes_list, volume=volume)