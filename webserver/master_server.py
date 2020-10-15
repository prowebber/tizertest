import socket
import network
from websocket import websocket
import websocket_helper
from time import sleep
import os

class ClientClosedError(Exception):
	pass




class SocketConnection:
	def __init__(self, addr, s, close_callback):
		self.client_close = False
		self._need_check = False
		
		self.address = addr
		self.socket = s
		self.ws = websocket(s, True)
		self.close_callback = close_callback
		
		s.setblocking(False)
		s.setsockopt(socket.SOL_SOCKET, 20, self.notify)
	
	def notify(self, s):
		self._need_check = True
	
	def read(self):
		if self._need_check:
			self._check_socket_state()
		
		msg_bytes = None
		try:
			msg_bytes = self.ws.read()
		except OSError:
			return False
		# self.client_close = True
		
		if not msg_bytes:  # Keep the connection open for multiple cmds
			return
		
		if not msg_bytes and self.client_close:
			print("Got to this client close")
			raise ClientClosedError()
		
		return msg_bytes
	
	def write(self, msg):
		try:
			self.ws.write(msg)
		except OSError:
			self.client_close = True
	
	def _check_socket_state(self):
		self._need_check = False
		sock_str = str(self.socket)
		state_str = sock_str.split(" ")[1]
		state = int(state_str.split("=")[1])
		
		if state == 3:
			self.client_close = True
	
	def is_closed(self):
		return self.socket is None
	
	def close(self):
		print("Closing connection.")
		self.socket.setsockopt(socket.SOL_SOCKET, 20, None)
		self.socket.close()
		self.socket = None
		self.ws = None
		if self.close_callback:
			self.close_callback(self)


class SocketClient:
	def __init__(self, conn):
		self.connection = conn
	
	def process(self):
		pass

class SocketServer:
	def __init__(self, page):
		self._listen_s = None
		self._clients = []
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
		
		for i in (network.AP_IF, network.STA_IF):
			iface = network.WLAN(i)
			if iface.active():
				print("WebSocket started on ws://%s:%d" % (iface.ifconfig()[0], port))
	
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


class SocketMultiServer(SocketServer):
	def __init__(self, index_page, max_conn=10):
		super().__init__(index_page)
		dir_idx = index_page.rfind("/webserver/")
		self.max_conn = max_conn
		self._web_dir = index_page[0:dir_idx] if dir_idx > 0 else "/"
		
	def create_socket(self, conn):
		pass
	
	def _accept_conn(self, list):
		cl, addr = self._listen_s.accept()
		
		if len(self._clients) >= self.max_conn:
			cl.setblocking(True)
			create_static_page(cl, 503, "503 Too Many Connections")
			return
		
		requested_file = None
		data = cl.recv(64).decode()  # Get first 64 chars of browser response
		
		if data and "Upgrade: websocket" not in data.split("\r\n") and "GET" == data.split(" ")[0]:
			requested_file = data.split(" ")[1].split("?")[0]
			requested_file = self._page if requested_file in [None, "/"] else requested_file
		
		try:
			websocket_helper.server_handshake(cl)
			self._clients.append(self.create_socket(SocketConnection(addr, cl, self.remove_connection)))
		except OSError:
			if requested_file:
				self._serve_file(requested_file, cl)
			else:
				create_static_page(cl, 500, "500 Internal Server Error [2]")
	
	def _serve_file(self, requested_file, c_socket):
		print("### Serving file: {}".format(requested_file))
		try:
			# check if file exists in web directory
			path = requested_file.split("/")
			filename = path[-1]
			subdir = "/" + "/".join(path[1:-1]) if len(path) > 2 else ""
			
			if filename not in os.listdir(self._web_dir + subdir):
				create_static_page(c_socket, 404, "404 Not Found")
				return
			
			# Create path based on web root directory
			file_path = self._web_dir + requested_file
			length = os.stat(file_path)[6]
			c_socket.sendall(build_headers(200, file_path, length))
			# Send file by chunks to prevent large memory consumption
			chunk_size = 1024
			with open(file_path, "rb") as f:
				while True:
					data = f.read(chunk_size)
					c_socket.sendall(data)
					if len(data) < chunk_size:
						break
			sleep(0.1)  # Wait before ending the session
			c_socket.close()
		except OSError:
			create_static_page(c_socket, 500, "500 Internal Server Error [2]")


http_codes = {
	200: "OK",
	404: "Not Found",
	500: "Internal Server Error",
	503: "Service Unavailable"
}

mime_types = {
	"jpg": "image/jpeg",
	"jpeg": "image/jpeg",
	"png": "image/png",
	"gif": "image/gif",
	"html": "text/html",
	"htm": "text/html",
	"css": "text/css",
	"js": "application/javascript"
}


def build_headers(code, filename=None, length=None):
	content_type = "text/html"
	
	if filename:
		ext = filename.split(".")[1]
		if ext in mime_types:
			content_type = mime_types[ext]
	
	return "HTTP/1.1 {} {}\n" \
	       "Content-Type: {}\n" \
	       "Content-Length: {}\n" \
	       "Server: Shoetizer\n" \
	       "Connection: close\n\n".format(
		code, http_codes[code], content_type, length)


def create_static_page(sock, code, msg):
	sock.sendall(build_headers(code))
	sock.sendall("<html><body><h1>" + msg + "</h1></body></html>")
	sleep(0.1)
	sock.close()
