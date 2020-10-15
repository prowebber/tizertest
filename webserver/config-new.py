import ujson
from time import sleep
from webserver.server import Server, OpenSockets, ClientClosedError


class UserInteraction(OpenSockets):
	def __init__(self):
		print("Called")
		pass

	def process(self):
		print("At process")
		try:
			# See if there's any data
			raw = self.read()
			if not raw:
				return

			msg = raw.decode("utf-8")
			data = ujson.loads(msg)
			print("Command: %s" % data['cmd'])
		except ClientClosedError:
			print('client closed err')
			self.close()

# Start the webserver
server = Server('0.0.0.0', 80)  # Start the server on localhost at this port
server.start()


# ui = UserInteraction()
# try:
# 	while True:
# 		ui.process()
# except KeyboardInterrupt:
# 	pass