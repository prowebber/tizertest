import socket
import os
from time import sleep
import websocket_helper
from websocket import websocket
import ujson

class Build:
	def __init__(self):
		self.http_text = {
			200: "OK",
			404: "Not Found",
			500: "Internal Server Error",
			503: "Service Unavailable"
		}
		
		self.mime_types = {
			"jpg": "image/jpeg",
			"jpeg": "image/jpeg",
			"png": "image/png",
			"gif": "image/gif",
			"html": "text/html",
			"htm": "text/html",
			"css": "text/css",
			"js": "application/javascript"
		}
	
	def headers(self, http_code, filename=None, length=None):
		content_type = "text/html"
		
		# Get the file type
		if filename:
			file_type = filename.split('.')[1]
			if file_type in self.mime_types:
				content_type = self.mime_types[file_type]
		
		headers = "HTTP/1.1 {} {}\n" \
		          "Content-Type: {}\n" \
		          "Content-Length: {}\n" \
		          "Server: Shoetizer\n" \
		          "Connection: close\n\n".format(http_code, self.http_text[http_code], content_type, length)
		return str.encode(headers)
	
	def pg_404(self):
		content = self.headers(404)
		content += "<html><body><h1>" + "Test test" + "</h1></body></html>"
		
		return str.encode(content)
	
build = Build()

class Clients:
	"""
	Handle all client connections
	"""
	def __init__(self, conn, addr, s, on_close):
		self.conn = conn
		self.addr = addr
		self.s = s
		self.on_close = on_close
		
		self.s.setblocking(True)  # Set socket to 'non-blocking' mode
		
	def connect(self):
		"""
		Connect to the client
		"""
		# Wait until client is connected
		connected = False
		while not connected:
			try:
				conn, addr = self.s.accept()
				self.addr = addr
				self.conn = conn
				connected = True
			except Exception as e:
				pass
		print("New connection")


class ClientClosedError(Exception):
	pass

class OpenSockets:
	"""
	Handle WebSocket communications between Python and JS
	- Send all WebSocket responses to this class
	"""
	def __init__(self, conn, addr, s, on_close):
		print("Start of init")
		self.conn = conn
		self.addr = addr
		self.s = s
		self.on_close = on_close
		self.ws = websocket(s, True)
		self.process()
		self.client_close = False
		print("End of init")
		
	def process(self):
		pass
		
	def check_sigs(self):
		print("At process")
		try:
			# See if there's any data
			raw = self.read()
			if not raw:
				return
			
			print(raw)
			# msg = raw.decode("utf-8")
			# data = ujson.loads(msg)
			# print("Command: %s" % data['cmd'])
		except ClientClosedError:
			print('client closed err')
			self.close()
	
	def read(self):
		msg_bytes = None
		try:
			msg_bytes = self.ws.read()
		except OSError:
			return False
		
		if not msg_bytes and self.client_close:
			print("Throw client close err")
			raise ClientClosedError()
		
		return msg_bytes
	
	def close(self):
		"""
		Close the socket connection
		"""
		print("Closing socket connection")
		self.s.close()
		self.ws = None


class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.max_fail_conn = 4
		self.clients = []
		self.web_root_dir = '/webserver/'
		self.index_page = 'config.html'
		self.sys_path = ""  # Blank on ESP
		
	def start(self):
		# Start initial connection
		print("Starting server...")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevent address already in use error
		
		s.bind((self.host, self.port))  # Associate the socket with port/host
		s.listen(self.max_fail_conn)  # Start listening; exit if max failed conn is reached
		
		try:
			while True:
				try:
					conn, addr = s.accept()
					client = Clients(conn, addr, s, None)
					print("New connection!")
					self._process_conn(client)
				except Exception as e:
					pass
		except KeyboardInterrupt:
			s.close()
		
	def _process_conn(self, client):
		resp = client.conn.recv(64).decode()
		conn = client.conn
		
		conn.setblocking(True)
		
		# Process any websocket connections
		try:
			# If this is a websocket signal
			websocket_helper.server_handshake(conn)
			print("Websocket A")
			OpenSockets(conn, client.addr, client.s, None)  # Add this connect to the open sockets list
			print("Websocket B")
		except OSError:
			# If no websocket connection, run the page request
			# Get the requested page
			if resp:
				if "GET" == resp.split(" ")[0]:  # If this is a GET request
					get_file = resp.split(" ")[1].split("?")[0]
					print("Get file: %s" % get_file)
					self._serve_file(client, get_file)
				
	def _serve_file(self, client, file_uri):
		# check if file exists in web directory
		path = file_uri.split("/")
		filename = path[-1]
		subdir = "/" + "/".join(path[1:-1]) if len(path) > 2 else ""
		
		if filename == '':  # If this is the index page
			filename = self.web_root_dir + self.index_page
		else:
			subdir += "/"
			
		# Get the correct path
		file_path = self.sys_path + subdir + filename
		file_size = os.stat(file_path)[6]
		
		print("File Path: %s" % file_path)
		client.conn.sendall(build.headers(200, filename, file_size))  # Send the headers
	
		# Send file by chunks to prevent large memory consumption
		chunk_size = 1024
		with open(file_path, "rb") as f:
			while True:
				data = f.read(chunk_size)
				client.conn.sendall(data)
				if len(data) < chunk_size:
					break
					
		print("Served file")
		sleep(0.1)
	
if __name__ == "__main__":
	"""
	For testing on local machine
	"""
	host = '127.0.0.1'
	port = 65432
	app = Server(host, port)
	app.sys_path = "C:/WebPure Dropbox/Steven Holdaway/machine/desktop/python/tizertest"
	app.start()

# time.sleep(5)  # Wait 5 seconds
#
# client = Client()
# client.start_client(host, port, 1)
