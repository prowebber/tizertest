import sys
import socket
import selectors
import traceback
from webserver.msg_client import Message


class MpClient:
	def __init__(self, host, port):
		self.sel = selectors.DefaultSelector()
		
		self.host = host
		self.port = port
		self.messages = [b'Message 1 from client', b'Message 2 from client']
	
	def start(self, action, value):
		request = self.create_request(action, value)
		self.start_connection(request)
		
		try:
			while True:
				events = self.sel.select(timeout=1)
				for key, mask in events:
					message = key.data
					try:
						message.process_events(mask)
					except Exception:
						print(
							"main: error: exception for",
							f"{message.addr}:\n{traceback.format_exc()}",
						)
						message.close()
				# Check for a socket being monitored to continue.
				if not self.sel.get_map():
					break
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
		finally:
			self.sel.close()
	
	def create_request(self, action, value):
		if action == "search":
			return dict(
				type="text/json",
				encoding="utf-8",
				content=dict(action=action, value=value),
			)
		
		else:
			return dict(
				type="binary/custom-client-binary-type",
				encoding="binary",
				content=bytes(action + value, encoding="utf-8"),
			)
	
	def start_connection(self, request):
		addr = (self.host, self.port)
		print("starting connection to", addr)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setblocking(False)
		sock.connect_ex(addr)
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		message = Message(self.sel, sock, addr, request)
		self.sel.register(sock, events, data=message)


if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	
	app = MpClient(host, port)
	app.start('search', 'morpheus')
