import socket


class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
	
	def start_conn(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	
if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	app = Server(host, port)
