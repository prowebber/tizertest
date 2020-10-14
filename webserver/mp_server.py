import socket
import selectors
import types
import traceback

from webserver.msg_server import Message
from webserver.mp_client import MpClient

class MpServer:
	"""
	Custom WebServer
	@ref: https://realpython.com/python-sockets/
	"""
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.max_unaccepted_conn = 4
		self.sel = selectors.DefaultSelector()
		
	def start(self):
		lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Avoid bind() exception: OSError: [Errno 48] Address already in use
		lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		lsock.bind((self.host, self.port))  # Associate the socket with the specified host and port
		lsock.listen(self.max_unaccepted_conn)  # Accept connections and convert to 'listening' socket
		print("listening on", (host, port))
		lsock.setblocking(False)  # Set socket to 'non-blocking' mode
		
		# Register the socket to have READ events monitored with selector
		self.sel.register(lsock, selectors.EVENT_READ, data=None)
		
		try:
			while True:
				events = self.sel.select(timeout=None)  # Blocking until sockets are ready for I/O
				print("Starting events....")
				for key, mask in events:  # Return a list for each socket
					print(f"Key: {key}")
					if key.data is None:
						self.accept_wrapper(key.fileobj)
					else:
						message = key.data
						try:
							message.process_events(mask)
						except Exception:
							print(
								"main: error: exception for",
								f"{message.addr}:\n{traceback.format_exc()}",
							)
							message.close()
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
		finally:
			self.sel.close()


	def accept_wrapper(self, sock):
			conn, addr = sock.accept()
			print("accepted connection from", addr)
			
			# client = MpClient(self.host, self.port)
			# client.start('search', 'morpheus')
			
			conn.setblocking(False)
			msg = Message(self.sel, conn, addr)
			self.sel.register(conn, selectors.EVENT_READ, data=msg)
					
	
					

					
if __name__ == "__main__":
	host = '127.0.0.1'
	port = 65432
	
	# Init the MicroPython Server
	app = MpServer(host, port)
	app.start()
