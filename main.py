import gc
from json import load, dump
from utils import *
from machine import Timer
from time import time

t0 = time()
gc.enable()  # Enable automatic garbage collection


def move_files():
	from utils import move_files
	move_files()


def get_config():
	"""
	Open the JSON config file and convert to a Python dict
	"""
	with open('.sconfig') as params:
		data = load(params)
	return data


def save_config(config_dict):
	"""
	Update the config file with new settings
	"""
	# Save the settings
	with open('.sconfig', 'w') as data_out:
		dump(config_dict, data_out)


async def _conn_wifi(broadcast = False):
	"""
	Connect to WiFi
	"""
	from core.wifi_conn import connect_to_wifi, broadcast_wifi
	wifi_ssid = config_data['wifi_ssid']
	wifi_pass = config_data['wifi_pass']

	is_connected = 0  # Set to not connected by default
	if wifi_ssid and wifi_pass:
		print("Connecting to WiFi")
		is_connected = connect_to_wifi(wifi_ssid, wifi_pass)

	config_data['has_wifi'] = is_connected
	save_config(config_data)  # Update the config

	# Broadcast the WiFi
	if broadcast:
		broadcast_wifi('ShoeTizer-' + config_data['unit_id'], '123456789')
		print("Broadcasting WiFi...")

	return is_connected


def ota():
	"""
	OTA - All
	- Check if updates exist
	- Download, install, & reboot if updates exist
	:return:
	"""
	from core.ota_check import OTACheck

	github_url = config_data['ota_github_url']
	target_dir = config_data['ota_tgt_dir']

	# Check if any new updates are posted to GitHub
	oc = OTACheck(github_url, tgt_dir = target_dir)
	if oc.start():  # If there is a new version
		from core.ota_download import OTADownload

		oi = OTADownload(github_url, tgt_dir = target_dir)  # Init #@todo look at IIFE
		oi.start()  # Download & install; reboot when done


def force_ota(target_dir = 'project'):
	"""
	Force update from Master branch
	"""
	github_url = config_data['ota_github_url']

	print("OTA Target dir: " + target_dir)

	from core.ota_download import OTADownload
	if _conn_wifi():  # Connect to WiFi
		oi = OTADownload(github_url, tgt_dir = target_dir)  # Init #@todo look at IIFE
		oi.dev_download()


def setup():
	has_wifi = _conn_wifi(True)  # Connect to WiFi
	if has_wifi:  # If connected to WiFi
		from webserver.statics import createParamsJs
		createParamsJs()  # Create JS params file

		from webserver.config import InitServer

		index_pg = "/webserver/config.html"
		max_conn = 50
		server = InitServer(index_pg, max_conn)
		server.start()

		try:
			while True:
				server.process_all()
		except KeyboardInterrupt:
			pass

		server.stop()


def rest():
	from project.rest_api import Rest

	api = Rest()

	# Get time
	# resp = api.get('/tizer')

	# Post doypack
	payload = {
		'unit_id': 'stevtest',
		'volume_ml': '500'
	}
	resp = api.post('/tizer/doypacks', payload)
	print(resp)


def start():
	global t1
	print(f"start reached: {round(time() - t1, 3)} s")
	t1 = time()

	Timer(-1).init(period = 0, mode = Timer.ONE_SHOT, callback = lambda t: _conn_wifi())
	# 	ota()  # Check for OTA
	from project.main import start as main_start
	print(f"project main imported: {round(time() - t1, 3)} s")
	t1 = time()

	main_start()


global t1
t1 = time()
print(f"load config reached: {round(time() - t0, 3)} s")
# Load config data
config_data = get_config()
# Verify the board ID is recorded
if not config_data['unit_id']:
	from core.config_man import board_id

	config_data['unit_id'] = board_id()

print(f"config loaded: {round(time() - t1, 3)} s")
t1 = time()
start()
