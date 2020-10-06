from webserver.ws_connection import ClientClosedError
from webserver.ws_server import WebSocketClient
from webserver.ws_multiserver import WebSocketMultiServer
import ujson

class TestClient(WebSocketClient):
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            json_msg = ujson.loads(msg)
            print("message follows...")
            print(msg)
            print("SSID: %s" % json_msg['wifi_ssid'])

            self.connection.write(msg)
            # items = msg.split(" ")
            # cmd = items[0]
            # if cmd == "Hello":
            #     self.connection.write(cmd + " World")
            #     print("Hello World")
        except ClientClosedError:
            self.connection.close()


class TestServer(WebSocketMultiServer):
    def __init__(self):
        super().__init__("/webserver/config.html", 10)

    def _make_client(self, conn):
        return TestClient(conn)


server = TestServer()
server.start()
try:
    while True:
        server.process_all()
except KeyboardInterrupt:
    pass
server.stop()