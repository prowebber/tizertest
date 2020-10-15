import socket
import selectors
# import types


class ClientData:
	"""
	MicroPython version of types.SimpleNamespace
	"""
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)
	
	def __repr__(self):
		keys = sorted(self.__dict__)
		items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
		return "{}({})".format(type(self).__name__, ", ".join(items))
	
	def __eq__(self, other):
		return self.__dict__ == other.__dict__


class Build:
	
	def __init__(self):
		self.http_text = {
			200: "OK",
			404: "Not Found",
			500: "Internal Server Error",
			503: "Service Unavailable"
		}
	
	def headers(self, http_code):
		content_type = "text/html"
		length = None
		
		headers = "HTTP/1.1 {} {}\n" \
		          "Content-Type: {}\n" \
		          "Content-Length: {}\n" \
		          "Server: Shoetizer\n" \
		          "Connection: close\n\n".format(http_code, self.http_text[http_code], content_type, length)
		return headers
	
	def pg_404(self):
		content = self.headers(404)
		content += "<html><body><h1>" + "Test test" + "</h1></body></html>"
		
		return str.encode(content)
	
	def pg_config(self):
		html_file = 'C:/WebPure Dropbox/Steven Holdaway/machine/desktop/python/tizertest/webserver/config.html'
		
		# Read in the page
		content = self.headers(200)
		with open(html_file, "r") as f:
			content += f.read()
		
		return str.encode(content)


build = Build()


class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.max_fail_conn = 4
		self.sel = selectors.DefaultSelector()
		self.sel_b = None
	
	def start(self):
		print("Starting server...")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevent address already in use error
		
		s.bind((self.host, self.port))  # Associate the socket with port/host
		s.listen(self.max_fail_conn)  # Start listening; exit if max failed conn is reached
		print("listening on", (host, port))
		
		s.setblocking(False)  # Set socket to 'non-blocking' mode
		
		# Register the socket to have READ events monitored with selector
		self.sel.register(s, selectors.EVENT_READ, data=None)
		
		try:
			while True:
				events = self.sel.select(timeout=None)  # Block until sockets are ready for I/O
				for key, mask in events:  # Return a list for each socket
					if key.data is None:  # If there is no data, it is the listening socket and needs to be connected
						self._accept_conn(key.fileobj)  # Pass the socket object
					else:  # If there IS data, it is an existing connection and needs to be handled
						self._process_conn(key, mask)
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
		finally:
			self.sel.close()
	
	def _process_conn(self, key, mask):
		"""
		Handles the current connection
		"""
		sock = key.fileobj  # Socket Object
		data = key.data  # Data Object
		
		# If the socket is ready for reading
		if mask & selectors.EVENT_READ:
			browser_data = sock.recv(1024)  # Read data from the browser
			if browser_data:
				# data.outb += browser_data  # Record all data received
				
				# print(os.stat(html_file))
				
				# data.outb = build.pg_404()
				data.outb = build.pg_config()
			
			else:  # If there is no data, the client has closed their connection
				print('closing connection to', data.addr)
				self.sel.unregister(sock)  # Stop handling this socket
				sock.close()  # Close the connection
		
		# If the socket is ready for writing
		if mask & selectors.EVENT_WRITE:
			if data.outb:  # If there is data to be sent
				print('echoing', repr(data.outb), 'to', data.addr)
				sent = sock.send(data.outb)  # Send the data
				data.outb = data.outb[sent:]  # Update the total bytes remaining to be sent
			else:
				self.sel.unregister(sock)  # Stop handling this socket
				sock.close()  # Close the connection
	
	def _accept_conn(self, sock):
		"""
		- Accept the socket connection from the browser
		- Register the connection with the selector
		"""
		conn, addr = sock.accept()
		print("accepted connection from", addr)
		conn.setblocking(False)
		
		data = ClientData(addr=addr, inb=b"", outb=b"")
		# data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
		print(data)
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.sel.register(conn, events, data=data)  # Register the connection with the socket


if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	app = Server(host, port)
	app.start()

# time.sleep(5)  # Wait 5 seconds
#
# client = Client()
# client.start_client(host, port, 1)
