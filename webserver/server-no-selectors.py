import socket
# import types


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
		# html_file = '/webserver/config.html'
		
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
	
	def start(self):
		print("Starting server...")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevent address already in use error
		
		s.bind((self.host, self.port))  # Associate the socket with port/host
		s.listen(self.max_fail_conn)  # Start listening; exit if max failed conn is reached
		print("listening on", (self.host, self.port))
		
		s.setblocking(False)  # Set socket to 'non-blocking' mode
		
		# Wait until client is connected
		connected = False
		while not connected:
			try:
				conn, addr = s.accept()
				connected = True
			except Exception as e:
				pass
		
		# When the client/browser is connected
		print("accepted connection from", addr)
		conn.setblocking(True)
		# data = ClientData(addr=addr, inb=b"", outb=b"")
		content = b""
		
		resp = conn.recv(1024)
		print("reading...")
		print(resp)
		
		content = build.pg_config()
		print("Done all data from browser")
		
		try:
			while True:
				# Write to the browser next
				if content:  # If there is data to be sent
					print('echoing', repr(content), 'to', addr)
					sent = conn.send(content)  # Send the data
					content = content[sent:]  # Update the total bytes remaining to be sent
				else:
					# s.close()  # Close the connection
					print("Closed connection")
					break
				
				
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
			
		print("Done")
	
	def _process_conn(self, sock, data, action):
		"""
		Handles the current connection
		"""
		if action == 'read':
			browser_data = sock.recv(1024)  # Read data from the browser
			
			if browser_data:
				data.outb = build.pg_config()
			else:  # If there is no data, the client has closed their connection
				print('closing connection to', data.addr)
				sock.close()
		if action == 'write':
			if data.outb:  # If there is data to be sent
				print('echoing', repr(data.outb), 'to', data.addr)
				sent = sock.send(data.outb)  # Send the data
				data.outb = data.outb[sent:]  # Update the total bytes remaining to be sent
			else:
				sock.close()  # Close the connection
			
	
if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	app = Server(host, port)
	app.start()

# time.sleep(5)  # Wait 5 seconds
#
# client = Client()
# client.start_client(host, port, 1)
