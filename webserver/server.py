import socket
import selectors


class Message:
	def __init__(self, selector, sock, addr, req):
		self.selector = selector
		self.sock = sock
		self.addr = addr
		self.req = req
		
	def client_process_events(self, mask):
		if mask & selectors.EVENT_READ
			self.client_read()
			
	def client_read(self):

class Client:
	def __init__(self):
		self.sel = selectors.DefaultSelector()
	
	def start_client(self, host, port, action, value):
		req = self._create_request(action, value)  # Create the request
		self._start_conn(host, port, req)  # Start the connection
		
		# Wait for messages/data
		try:
			while True:
				events = self.sel.select(timeout=1)
				for key, mask in events:
					msg = key.data
					try:
					
				pass
		except KeyboardInterrupt:
			print("Keyboard interrupt...exiting")
		finally:
			self.sel.close()
	
	def _create_request(self, action, value):
		pass
	
	def _start_conn(self, host, port, req):
		addr = (host, port)
		print("starting connection to", addr)
		# Start the client socket
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.setblocking(False)
		cs.connect_ex(addr)
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		msg = Message(self.sel, cs, addr, req)
		self.sel.register(cs, events, data=msg)

class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.max_fail_conn = 4
		
		self.sel = selectors.DefaultSelector()
	
	def start_conn(self):
		# Start a socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# Associate the socket with port/host
		s.bind((self.host, self.port))
		s.listen(self.max_fail_conn)  # Start listening; exit if max failed conn is reached
		print("listening on", (host, port))
		s.setblocking(False)  # Set socket to 'non-blocking' mode
		
		# Register the socket to have READ events monitored with selector
		self.sel.register(s, selectors.EVENT_READ, data=None)
		
		try:
			while True:
				events = self.sel.select(timeout=None)  # Blocking until sockets are ready for I/O
				print("Starting events....")
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
		finally:
			self.sel.close()
	
	
if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	app = Server(host, port)
