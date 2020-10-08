from webserver.ws_connection import ClientClosedError
from webserver.ws_server import WebSocketClient
from webserver.ws_multiserver import WebSocketMultiServer
import ujson
from time import sleep


class TestClient(WebSocketClient):
	def __init__(self, conn):
		super().__init__(conn)
	
	def process(self):
		try:
			raw = self.connection.read()
			if not raw:
				return
			msg = raw.decode("utf-8")
			data = ujson.loads(msg)
			
			print("Command: %s" % data['cmd'])
			
			if 'cmd' in data:
				cmd = data['cmd']  # Get the command
				
				if cmd == 'save_settings':
					self.save_settings(data)
				elif cmd == 'load_params':
					self.load_params(data)
				elif cmd == 'reset_bag':
					self.reset_bag(data)
			else:
				print("No command")
			
			print(msg)
			
			# self.connection.write(msg)
		except ClientClosedError:
			print('client closed err')
			self.connection.close()
			
	def reset_bag(self, data):
		from core.config_man import get_config, save_config
		
		config = get_config()
		device_id = config['device_id']
		
		print("Resetting bag...")
		
	def load_params(self, data):
		print("Loading params")
		self.connection.write('steve')
			
	def save_settings(self, data):
		print("Save Settings")
		print(data)
		
		from core.config_man import get_config, save_config
		
		config = get_config()
		config['wifi_ssid'] = data['wifi_ssid']
		config['wifi_pass'] = data['wifi_pass']
		save_config(config)
		
		self.connection.write("Updated successfully!")
		


class TestServer(WebSocketMultiServer):
	def __init__(self):
		super().__init__("/webserver/config.html", 50)
	
	def _make_client(self, conn):
		return TestClient(conn)


server = TestServer()
server.start()
try:
	while True:
		server.process_all()
except KeyboardInterrupt:
	pass

server.stop()
