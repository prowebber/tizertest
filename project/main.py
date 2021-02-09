from core.config_man import get_config, save_config
from machine import Pin, Timer, RTC, deepsleep, DEEPSLEEP, DEEPSLEEP_RESET, reset_cause
from project.pins import *
from project.devices import LED, Button
from project.tones import Speaker
# from project.rest_api import Rest
from utime import ticks_ms, ticks_diff
from sys import exit
from time import time


def start():
	t0 = time()
	if c['enable_led']:
		led.on()
	# Play tritone on boot
	if not c['mute']:
		speaker.play_tones(['C5', 'E5', 'G5'])
	deep_sleep()
	while True:
		pass


def run(_tmax = None):
	global running, t_max
	t_max = _tmax
	# Run once up to t_max ms if not running
	if not running:
		running = True
		if not c['mute']:  # Play note (if enabled)
			speaker.play_tones(['G5'])
		pump_on()


def long_run():
	# timeout in 7sec
	run(7000)


def end_run():
	pump_off()


def pump_on():
	global t0_pump
	pump.on()
	print('pump on')
	t0_pump = ticks_ms()
	per = t_max if t_max else c['pump_ms']
	t_single(per, pump_off)


def pump_off():
	global running, t_max, t0_pump
	pump.off()
	print('pump off')
	if running:
		spray_duration = ticks_diff(ticks_ms(), t0_pump)
		c['unit_spray_ms'] += spray_duration
		c['bag_spray_ms'] += spray_duration
		save_config(c)
		running = False
		t_max = None


def _conn_wifi(broadcast = False):
	"""
	Connect to WiFi
	"""
	from core.wifi_conn import connect_to_wifi, broadcast_wifi
	wifi_ssid = c['wifi_ssid']
	wifi_pass = c['wifi_pass']

	is_connected = 0  # Set to not connected by default
	if wifi_ssid and wifi_pass:
		print("Connecting to WiFi")
		is_connected = connect_to_wifi(wifi_ssid, wifi_pass)

	c['has_wifi'] = is_connected
	save_config(c)  # Update the config

	# Broadcast the WiFi
	if broadcast:
		broadcast_wifi('ShoeTizer-' + c['unit_id'], '123456789')
		print("Broadcasting WiFi...")

	return is_connected


def broadcast():
	led.blink(4)
	print('broadcasting from project main')
	_conn_wifi(True)


def end_broadcast():
	pass


def deep_sleep():
	# configure RTC.ALARM0 to be able to wake the device
	rtc = RTC()
	rtc.irq(trigger = rtc.ALARM0, wake = DEEPSLEEP)

	# check if the device woke from a deep sleep
	if reset_cause() == DEEPSLEEP_RESET:
		print('woke from a deep sleep')

	# set RTC.ALARM0 to fire after 10 seconds (waking the device)
	rtc.alarm(rtc.ALARM0, 10000)

	# put the device to sleep
	deepsleep()


def t_single(per, f):
	# to shorten code
	Timer(-1).init(period = per, mode = Timer.ONE_SHOT, callback = lambda t: f())


global running, tmax
b_foot = Button(5)
b_wifi = Button(4)
speaker = Speaker(14)
led = LED(13)
pump = Pin(D6, Pin.OUT, value = 0)
t_max = None
running = False
b_foot.on_hold(run, end_run, 300)
b_wifi.on_hold(broadcast, end_broadcast, 1000)
c = get_config()  # Get config info
# api = Rest()
