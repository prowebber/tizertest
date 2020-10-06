from assets.config_man import get_config, save_config
import gc

# Load config data
config_data = get_config()
gc.enable()  # Enable automatic garbage collection


def _conn_wifi():
	"""
	Connect to WiFi
	"""
	from assets.wifi_conn import connect_to_wifi
	wifi_ssid = config_data['wifi_ssid']
	wifi_pass = config_data['wifi_pass']
	
	is_connected = 0  # Set to not connected by default
	if wifi_ssid and wifi_pass:
		print("Connecting to WiFi")
		is_connected = connect_to_wifi(wifi_ssid, wifi_pass)
	
	config_data['wifi_status'] = is_connected
	save_config(config_data)  # Update the config
	
	return is_connected


def ota():
	"""
	OTA - All
	- Check if updates exist
	- Download, install, & reboot if updates exist
	:return:
	"""
	from assets.ota_check import OTACheck
	
	github_url = config_data['ota_github_url']
	target_dir = config_data['ota_tgt_dir']
	
	# Check if any new updates are posted to GitHub
	oc = OTACheck(github_url, tgt_dir=target_dir)
	if oc.start():  # If there is a new version
		from assets.ota_download import OTADownload
		
		oi = OTADownload(github_url, tgt_dir=target_dir)  # Init #@todo look at IIFE
		oi.start()  # Download & install; reboot when done


def force_ota_prev():
	import os
	if 'next' not in os.listdir():  # If next dir does not exist
		os.mkdir('next')
	try:
		f = open('/project/.version', "r")
		os.rename('/project/.version', '/next/.version_on_reboot')
	except OSError:  # open failed
		pass
	
	ota()

def force_ota(target_dir=None):
	"""
	Force update from Master branch
	"""
	github_url = config_data['ota_github_url']
	if not target_dir:
		target_dir = config_data['ota_tgt_dir']
	
	from assets.ota_download import OTADownload
	oi = OTADownload(github_url, tgt_dir=target_dir)  # Init #@todo look at IIFE
	oi.dev_download()


def del_proj():
	import os
	for f in os.listdir('project'):
		os.remove('project/' + f)

def start(broadcast=0):
	wifi_status = _conn_wifi()  # Connect to WiFi
	# if wifi_status:  # If connected to WiFi
		# ota()  # Check for OTA
	
	if broadcast == 1:
		from project.local_server import LocalServer
		
		app = LocalServer()
		app.start()
	
	from project.main import Main
	app = Main()
	app.start()
