from assets.config_man import get_config, save_config

# Load config data
config_data = get_config()


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


def _ota_check():
	# @todo add this once ShoteTizer github is added
	pass


def start(broadcast=0):
	# 1) Connect to WiFi
	wifi_status = _conn_wifi()
	
	if wifi_status == 1:  # If connected to WiFi
		pass
	
	if broadcast == 1:
		from project.local_server import LocalServer
		
		app = LocalServer()
		app.start()


