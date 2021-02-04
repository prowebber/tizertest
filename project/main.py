from core.config_man import get_config, save_config
from machine import Pin, Timer, PWM
from project.pins import *
from project.devices import LED, Button
from project.tones import Speaker
# from project.rest_api import Rest
from utime import ticks_ms, ticks_diff
from sys import exit
from time import time


def start(timeout = None):
	t0 = time()
	if c['enable_led']:
		led.on()
	# Play tritone on boot
	if not c['mute']:
		speaker.play_tones(['C5', 'E5', 'G5'])
	while True:
		if timeout:
			if time() - t0 > timeout:
				time_out()
				break


def time_out():
	if not c['mute']:
		speaker.play_tones(['G5', 'E5', 'C5'])


def run(_tmax = None):
	global running, t_max
	t_max = _tmax
	# Run once up to t_max ms if not running
	if not running:
		running = True
		if not c['mute']:  # Play note (if enabled)
			speaker.play_tones(['G5'])
		t_single(c['pump_delay'], pump_on)
		t_single(c['relay_delay'], relay_on)


def long_run():
	# timeout in 7sec
	run(7000)


def end_run():
	pump_off()
	relay_off()


def pump_on():
	pump.on()
	per = t_max if t_max else c['pump_ms']
	t_single(per, pump_off)


def pump_off():
	pump.off()


def relay_on():
	global t_max, t0_relay
	per = t_max if t_max else c['relay_ms']
	relay.on()
	t0_relay = ticks_ms()
	t_single(per, relay_off)


def relay_off():
	relay.off()
	global running, t_max, t0_relay
	if running:
		relay_duration = ticks_diff(ticks_ms(), t0_relay)
		c['unit_spray_ms'] += relay_duration
		c['bag_spray_ms'] += relay_duration
		save_config(c)
		running = False
		t_max = None


def t_single(per, f):
	# to shorten code
	Timer(-1).init(period = per, mode = Timer.ONE_SHOT, callback = lambda t: f())


global running, tmax, t0_relay
b_wifi = Button(5)
b_foot = Button(4)
speaker = Speaker(D5)
led = LED(D1)
pump = Pin(D6, Pin.OUT, value = 0)
# relay = Pin(D7, Pin.OUT, value = 0)
t0_relay = None
t_max = None
running = False
b_foot.on_hold(run, end_run, 300)
# b_foot.on_hold(long_run, end_run)
c = get_config()  # Get config info
# api = Rest()

# start(15)
