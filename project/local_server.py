import usocket
import ure
from utime import sleep_ms
from assets.config_man import get_config, save_config

class LocalServer:
	def __init__(self):
		pass
	
	def start(self):
		broadcast_server()
		self.pg_config_show()
		
	def pg_config_html(self):
		config_data = get_config()  # Get the config params
		enable_led = config_data['enable_led']
		wifi_ssid = config_data['wifi_ssid']
		wifi_pass = config_data['wifi_pass']
		wifi_status = config_data['wifi_status']
		wifi_connect_on_boot = config_data['wifi_connect_on_boot']
		
		# Specify values
		led_option = """<select name="led"><option value="1">Keep On</option><option value="0" selected>Turn Off</option></select>"""
		if enable_led == "1":
			led_option = """<select name="led"><option value="1" selected>Keep On</option><option value="0">Turn Off</option></select>"""
		
		wifi_on_boot = """<select name="wifi_on_boot"><option value="1">Yes</option><option value="0" selected>No</option></select>"""
		if wifi_connect_on_boot == "1":
			wifi_on_boot = """<select name="wifi_on_boot"><option value="1" selected>Yes</option><option value="0">No</option></select>"""
		
		wifi_status = "Connected to: " + wifi_ssid if wifi_status == 1 else "Not connected"
		
		raw = """<!DOCTYPE html>
						<html>
						<head>
							<title>ShoeTizer Settings</title>
							<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
							  h1{color: #0F3376; padding: 2vh;}
							  p{font-size: 1.5rem;}
							  table tr td:first-child{
							    font-size:14px;
								text-align:right;
							  }
							  table tr td:last-child{
								text-align:left;
							  }
						    </style>
						</head>
						<body>
							<h1>ShoeTizer Settings</h1>
							<form>
							<table>
							<caption>Settings</caption>
							<tbody>
							<tr><td>WiFi Network Name: </td><td><input type="text" name="network_name" value="%s"></td></tr>
							<tr><td>WiFi Network Password: </td><td><input type="text" name="network_pass" value="%s"></td></tr>
							<tr><td>WiFi Connect on Startup: </td><td>%s</td></tr>
							<tr><td>Power Light: </td><td>%s</td></tr>
							</tbody>
							</table>
							  <input type="hidden" name="end_field" value="end">
							  <button>Submit</button>
						    </form>

						    <table>
							<caption>Information</caption>
							<tbody>
							<tr><td>WiFi Status: </td><td>%s</td></tr>
							<tr><td>Lifetime uses: </td><td></td></tr>
							<tr><td>Solution remaining: </td><td></td></tr>
							</tbody>
							</table>
						</body>
						</html>
						"""
		html = raw % (wifi_ssid, wifi_pass, wifi_on_boot, led_option, wifi_status)
		
		return html
		
	def pg_config_show(self):
		s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
		s.bind(('', 80))
		s.listen(1)
		
		response = self.pg_config_html()  # Get any response
		
		# Loop until page has been displayed
		while True:
			update_config()  # Update the config settings
			conn, addr = s.accept()  # Get connection details
			print('Got a connection from %s' % str(addr))
			request = conn.recv(1024)  # Save the request data
			
			# Check to see if the request contains submitted settings
			reg_match = ure.match("GET\s\/\?network_name=(.*?)&network_pass=(.*?)&wifi_on_boot=(\d)&led=(\d)&", request)
			
			if reg_match:
				wifi_ssid = reg_match.group(1)
				wifi_pass = reg_match.group(2)
				wifi_on_boot = reg_match.group(3)
				enable_led = reg_match.group(4)
				
				# Update the config settings
				config_data = get_config()
				config_data['enable_led'] = enable_led
				config_data['wifi_ssid'] = wifi_ssid
				config_data['wifi_pass'] = wifi_pass
				config_data['wifi_connect_on_boot'] = wifi_on_boot
				
				print('WiFi Name: %s' % wifi_ssid)
				print('WiFi Pass: %s' % wifi_pass)
				print('Enable LED: %s' % enable_led)
				print('WiFi Connect on Boot: %s' % wifi_on_boot)
		
				save_config(config_data)  # Save the config params
				
				response = """<!DOCTYPE html><html><head><title>Saved</title> </head><body><h1>Saved</h1></body></html>"""
			else:
				response = self.pg_config_html()
		
			conn.send('HTTP/1.0 200 OK\r\n')
			conn.send("Content-Type: text/html\r\n\r\n")
			conn.sendall(response)
			sleep_ms(200)  # Wait for the chip to load the page before closing the connection
			conn.close()
			
			

def update_config():
	config_data = get_config()
	print(config_data)


def broadcast_server():
	"""
	Start broadcasting WiFi
	"""
	print('broadcast server reached')
	from assets.wifi_conn import broadcast_wifi
	
	wifi_ssid = 'ShoeTizer' # @todo mac address based
	wifi_pass = '123456789'
	
	broadcast_wifi(wifi_ssid, wifi_pass)
	print("Broadcasting...")