import socket
import selectors
import types
import time

messages = [b"Message 1 from client.", b"Message 2 from client."]

class Client:
	def __init__(self):
		self.sel = selectors.DefaultSelector()
	
	def start_client(self, host, port, num_conn):
		self._start_conn(host, port, num_conn)  # Start the connection
		
		# Wait for messages/data
		try:
			while True:
				events = self.sel.select(timeout=1)
				if events:
					for key, mask in events:
						self._service(key, mask)
				if not self.sel.get_map():
					break
		except KeyboardInterrupt:
			print("Keyboard interrupt...exiting")
		finally:
			self.sel.close()
			
	def _start_conn(self, host, port, num_conns):
		server_addr = (host, port)
		
		for i in range(0, num_conns):
			connid = i + 1
			print("starting connection", connid, "to", server_addr)
			
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setblocking(False)
			sock.connect_ex(server_addr)
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
			data = types.SimpleNamespace(
				connid=connid,
				msg_total=sum(len(m) for m in messages),
				recv_total=0,
				messages=list(messages),
				outb=b"",
			)
			self.sel.register(sock, events, data=data)
	
	def _service(self, key, mask):
		sock = key.fileobj
		data = key.data
		
		if mask & selectors.EVENT_READ:
			recv_data = sock.recv(1024)  # Should be ready to read
			
			if recv_data:
				print("received", repr(recv_data), "from connection", data.connid)
				data.recv_total += len(recv_data)
			if not recv_data or data.recv_total == data.msg_total:
				print("closing connection", data.connid)
				self.sel.unregister(sock)
				sock.close()
		if mask & selectors.EVENT_WRITE:
			if not data.outb and data.messages:
				data.outb = data.messages.pop(0)
			if data.outb:
				print("sending", repr(data.outb), "to connection", data.connid)
				sent = sock.send(data.outb)  # Should be ready to write
				data.outb = data.outb[sent:]

class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.max_fail_conn = 4
		
		self.sel = selectors.DefaultSelector()
	
	# noinspection DuplicatedCode
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
		print("Step a")
		
		try:
			while True:
				events = self.sel.select(timeout=None)  # Blocking until sockets are ready for I/O
				for key, mask in events:  # Return a list for each socket
					if key.data is None:
						self._accept_conn(key.fileobj)
					else:
						self._service(key, mask)
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
		finally:
			self.sel.close()
					
						
	def _accept_conn(self, sock):
		conn, addr = sock.accept()
		print("accepted connection from", addr)
		conn.setblocking(False)
		
		data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.sel.register(conn, events, data=data)
		
	def _web_content(self, code):
		code = 404
		http_code = "Not Found"
		content_type = "text/html"
		length = None
		
		headers = "HTTP/1.1 {} {}\n" \
		       "Content-Type: {}\n" \
		       "Content-Length: {}\n" \
		       "Server: Shoetizer\n" \
		       "Connection: close\n\n".format(code, http_code, content_type, length)
		return headers
		
	def _service(self, key, mask):
		sock = key.fileobj
		data = key.data
		
		if mask & selectors.EVENT_READ:
			recv_data = sock.recv(1024)  # Should be ready to read
			if recv_data:
				data.outb += recv_data
			else:
				print("closing connection to", data.addr)
				self.sel.unregister(sock)
				sock.close()
		if mask & selectors.EVENT_WRITE:
			if data.outb:
				print("echoing", repr(data.outb), "to", data.addr)
				# sent = sock.send(data.outb)  # Should be ready to write
				# print('send')
				# print(data.outb[sent:])
				content = str.encode(self._web_content(404))
				
				
				# sock.sendall(content)
				# sock.sendall(b"<html><body><h1>" + b"Test test" + b"</h1></body></html>")
				# time.sleep(0.1)
				# sock.close()
				# data.outb = content
				# data.outb = data.outb[sent:]
	
	
if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	app = Server(host, port)
	app.start()
	
	# time.sleep(5)  # Wait 5 seconds
	#
	# client = Client()
	# client.start_client(host, port, 1)
