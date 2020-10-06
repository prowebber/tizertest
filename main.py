from assets.config_man import get_config, save_config
import gc
import move_files

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
	is_update = oc.start()  # Check for new version
	
	if is_update:  # If there is a new version
		from assets.ota_download import OTADownload
		
		oi = OTADownload(github_url, tgt_dir=target_dir)  # Init
		oi.start()  # Download & install; reboot when done
		

def ota_check():
	"""
	Check for any new updates posted to GitHub
	"""
	from assets.ota_check import OTACheck
	
	github_url = config_data['ota_github_url']
	target_dir = config_data['ota_tgt_dir']
	
	o = OTACheck(github_url, tgt_dir=target_dir)
	o.start()  # Check for pending updates


def ota_install():
	"""
	Download an replace existing files with updated files
	"""
	from assets.ota_download import OTADownload
	
	github_url = config_data['ota_github_url']
	target_dir = config_data['ota_tgt_dir']
	
	o = OTADownload(github_url, tgt_dir=target_dir)  # Init OTA
	o.start()
	
def force_ota():
	import os
	if 'next' not in os.listdir():  # If next dir does not exist
		os.mkdir('next')
	os.rename('/project/.version', '/next/.version_on_reboot')
	
	ota()

def start(broadcast=0):
	wifi_status = _conn_wifi()  # Connect to WiFi
	if wifi_status == 1:  # If connected to WiFi
		ota()  # Check for OTA
		
	if broadcast == 1:
		from project.local_server import LocalServer
		
		app = LocalServer()
		app.start()
		
	from project.main import Main
	app = Main()
	app.start()


