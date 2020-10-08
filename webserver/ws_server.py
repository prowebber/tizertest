import socket
import network

"""
WebSocket Server
"""


class WebSocketClient:
	def __init__(self, conn):
		self.connection = conn
	
	def process(self):
		pass


class WebSocketServer:
	def __init__(self, page, max_connections=1):
		self._listen_s = None
		self._clients = []
		self._max_connections = max_connections
		self._page = page
	
	def _setup_conn(self, port, accept_handler):
		self._listen_s = socket.socket()
		self._listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		ai = socket.getaddrinfo("0.0.0.0", port)
		addr = ai[0][4]
		
		self._listen_s.bind(addr)
		self._listen_s.listen(4)  # Stops the connection if this many items fail
		if accept_handler:
			self._listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
			
		# Only broadcast this (don't allow access over network IP)
		iface = network.WLAN(network.AP_IF)
		if iface.active():
			print("WebSocket started on ws://%s:%d" % (iface.ifconfig()[0], port))
			
	def _make_client(self, conn):
		return WebSocketClient(conn)
	
	def stop(self):
		if self._listen_s:
			self._listen_s.close()
		self._listen_s = None
		for client in self._clients:
			client.connection.close()
		print("Stopped WebSocket server.")
	
	def start(self, port=80):
		if self._listen_s:
			self.stop()
		self._setup_conn(port, self._accept_conn)
		print("Started WebSocket server...")
	
	def process_all(self):
		for client in self._clients:
			client.process()
	
	def remove_connection(self, conn):
		for client in self._clients:
			if client.connection is conn:
				self._clients.remove(client)
				return
