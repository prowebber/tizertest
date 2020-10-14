import socket
import selectors
import types

class MpServer:
	"""
	Custom WebServer
	@ref: https://realpython.com/python-sockets/
	"""
	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 65432
		self.max_unaccepted_conn = 4
		self.sel = selectors.DefaultSelector()
	
	def start(self):
		print("Starting server...")
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		soc.bind((self.host, self.port))  # Associate the socket with the specified host and port
		soc.listen(self.max_unaccepted_conn)  # Accept connections and convert to 'listening' socket
		print('listening on', (self.host, self.port))
		soc.setblocking(False)  # Set socket to 'non-blocking' mode
		
		# Register the socket to have READ events monitored with selector
		self.sel.register(soc, selectors.EVENT_READ, data=None)
		
		while True:
			events = self.sel.select(timeout=None)  # Blocking until sockets are ready for I/O
			for key, mask in events:  # Return a list for each socket
				if key.data is None:
					self.accept_wrapper(key.fileobj)
				else:
					self.service_connection(key, mask)
					
	def accept_wrapper(self, soc):
		conn, addr = soc.accept()
		print('accepted connection from', addr)
		
		conn.setblocking(False)
		data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.sel.register(conn, events, data=data)
		
	def service_connection(self, key, mask):
		sock = key.fileobj
		data = key.data
		
		if mask & selectors.EVENT_READ:
			recv_data = sock.recv(1024)
			
			if recv_data:
				data.outb += recv_data
			else:
				print('closing connection to', data.addr)
				self.sel.unregister(sock)
				sock.close()
		if mask & selectors.EVENT_WRITE:
			if data.outb:
				print('echoing', repr(data.outb), 'to', data.addr)
				sent = sock.send(data.outb)
				data.outb = data.outb[sent:]
	
	
	def start_prev(self):
		print("Starting server...")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((self.host, self.port))  # Associate the socket with the specified host and port
			s.listen(self.max_unaccepted_conn)  # Accept connections and convert to 'listening' socket
			conn, addr = s.accept()  # Block and wait for a connection, return values when client connects
			with conn:
				print('Connected by', addr)
				while True:  # Loop through all the blocking calls to conn.recv
					data = conn.recv(1024)
					if not data:
						break
					conn.sendall(data)
					

					
if __name__ == "__main__":
	app = MpServer()
	
	app.host = '127.0.0.1'
	app.port = 65432
	app.start()
