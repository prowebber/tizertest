import socket
import selectors
import types

class MpClient:
	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 65432
		self.messages = [b'Message 1 from client', b'Message 2 from client']
		self.sel = selectors.DefaultSelector()
		
	def start_connections(self, host, port, num_conns):
		"""
		Initiate connections
		:param host:
		:param port:
		:param num_conns: Number of connections to create on the server
		:return:
		"""
		server_addr = (host, port)
		for i in range(0, num_conns):
			connid = i + 1
			print('starting connection', connid, 'to', server_addr)
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setblocking(False)
			sock.connect_ex(server_addr)
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
			data = types.SimpleNamespace(connid=connid,
			                             msg_total=sum(len(m) for m in self.messages),
			                             recv_total=0,
			                             messages=list(self.messages),
			                             outb=b'')
			self.sel.register(sock, events, data=data)
			
	def service_connection(self, key, mask):
		sock = key.fileobj
		data = key.data
		
		if mask & selectors.EVENT_READ:
			recv_data = sock.recv(1024)  # Should be ready to read
			if recv_data:
				print('received', repr(recv_data), 'from connection', data.connid)
				data.recv_total += len(recv_data)
			if not recv_data or data.recv_total == data.msg_total:
				print('closing connection', data.connid)
				self.sel.unregister(sock)
				sock.close()
		if mask & selectors.EVENT_WRITE:
			if not data.outb and data.messages:
				data.outb = data.messages.pop(0)
			if data.outb:
				print('sending', repr(data.outb), 'to connection', data.connid)
				sent = sock.send(data.outb)  # Should be ready to write
				data.outb = data.outb[sent:]
		
	def start_prev(self):
		print("Starting client...")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((self.host, self.port))
			s.sendall(b'Hello World!')
			data = s.recv(1024)
		print('Received', repr(data))
		
		
mp_client = MpClient()

if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	num_connections = 4
	mp_client.start_connections(host, port, num_connections)