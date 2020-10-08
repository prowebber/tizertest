def connect_to_wifi(wifi_ssid, wifi_pass):
	"""
	Connect to a WiFi network
	:param wifi_ssid: Name of the WiFi network
	:param wifi_pass: Password to WiFi network
	"""
	import network

	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():  # If the device is NOT connected to WiFi
		print("Connecting to: %s" % wifi_ssid)
		sta_if.active(True)  # Make sure the station mode is active
		sta_if.connect(wifi_ssid, wifi_pass)  # Connect

		while not sta_if.isconnected():
			pass

	if sta_if.isconnected():
		print('network config:', sta_if.ifconfig())
		import ntptime
		from machine import RTC
		ntptime.settime()  # set the rtc datetime from the remote server
		print('clock synced to UTC')
		return 1  # Specify it is connected
	return 0  # Otherwise say it is NOT connected


def broadcast_wifi(wifi_ssid, wifi_pass):
	"""
	Broadcast a WiFi network for devices to connect to
	"""
	import network

	# Setup the access point
	ap = network.WLAN(network.AP_IF)
	ap.active(True)
	ap.config(essid = wifi_ssid, password = wifi_pass)

	while ap.active() == False:
		pass
