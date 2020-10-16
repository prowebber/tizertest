# WebSocket

### Requirements

**References**
- https://realpython.com/python-sockets/
- https://github.com/realpython/materials/tree/master/python-sockets-tutorial
- https://github.com/BetaRavener/upy-websocket-server




#### Install MicroPython Selectors
```python
import upip
upip.install("micropython-selectors")
```


```
TestServer
|-- WebSocketMultiServer.__init__()
|   |-- WebSocketServer.__init()

TestServer.start()
|-- WebSocketServer.start()
|   |-- self._setup_conn()

TestServer.process_all()
|-- WebSocketServer.process_all()
|   |-- WebSocketClient.process()
|   |   |-- 
```



### Init
```
TestServer
|-- WebSocketMultiServer.__init__()
|   |-- set index_page
|   |-- set max_connections
|   |-- WebSocketServer.__init__()
|   |   |-- set self._listen_s = None
|   |   |-- set self._clients = []
|   |   |-- set self._max_connections
|   |   |-- set self._page

```

### Start
```
TestServer.start()
|-- WebSocketServer.start()
|   |-- WebSocketServer._setup_conn()
|   |   |   |-- Pass WebSocketMultiServer._accept_conn()
|   |   |   |   |-- start listening for connection
|   |   |   |   |-- Receive data
|   |   |-- Create the socket
|   |   |-- bind the socket
|   |   |-- start listening
```