import gc
import json

gc.enable()  # Enable automatic garbage collection


def move_files():
	from utils import move_files
	move_files()

def get_config():
	"""
	Open the JSON config file and convert to a Python dict
	"""
	with open('/.sconfig') as params:
		data = json.load(params)
	return data


def save_config(config_dict):
	"""
	Update the config file with new settings
	"""
	# Save the settings
	with open('.sconfig', 'w') as data_out:
		json.dump(config_dict, data_out)

# Load config data
config_data = get_config()


# Verify the board ID is recorded
if not config_data['device_id']:
	from core.config_man import board_id

	config_data['device_id'] = board_id()


def _conn_wifi(broadcast=False):
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

	config_data['wifi_status'] = is_connected
	save_config(config_data)  # Update the config

	# Broadcast the WiFi
	if broadcast:
		broadcast_wifi('ShoeTizer-' + config_data['device_id'], '123456789')
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


def force_ota(target_dir = None):
	"""
	Force update from Master branch
	"""
	github_url = config_data['ota_github_url']
	if not target_dir:
		target_dir = config_data['ota_tgt_dir']
		
	print("OTA Target dir: " + target_dir)

	from core.ota_download import OTADownload
	if _conn_wifi():  # Connect to WiFi
		oi = OTADownload(github_url, tgt_dir = target_dir)  # Init #@todo look at IIFE
		oi.dev_download()


def setup():
	wifi_status = _conn_wifi(True)  # Connect to WiFi
	if wifi_status:  # If connected to WiFi
		from webserver.statics import createParamsJs
		createParamsJs()  # Create JS params file
		import webserver.config
		# from webserver.server import Server
		# app = Server('0.0.0.0', 80)
		# app.start()


def rest():
	from project.rest_api import Rest
	
	api = Rest()

	# Get time
	# resp = api.get('/tizer')

	# Post doypack
	payload = {
		'device_id': 'stevtest',
		'volume_ml': '500'
	}
	resp = api.post('/tizer/doypacks', payload)
	print(resp)


def start():
	# if _conn_wifi():  # If connected to WiFi
	# 	ota()  # Check for OTA

	from project.main import Main
	app = Main()
	app.start()
