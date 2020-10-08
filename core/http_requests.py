import usocket
import gc

"""
Modified version of urequests
"""

class Response:
	def __init__(self, f):
		self.raw = f
		self.encoding = 'utf-8'
		self._cached = None
	
	def close(self):
		if self.raw:
			self.raw.close()
			self.raw = None
		self._cached = None
	
	@property
	def content(self):
		if self._cached is None:
			try:
				self._cached = self.raw.read()
			finally:
				self.raw.close()
				self.raw = None
		return self._cached
	
	@property
	def text(self):
		return str(self.content, self.encoding)
	
	def json(self):
		import ujson
		return ujson.loads(self.content)


class HttpClient:
	
	def request(self, method, url, data=None, json=None, headers={}, stream=None, dtype=None):
		"""
		:param dtype: string - type of data returned ('json', 'text')
		"""
		try:
			proto, dummy, host, path = url.split('/', 3)
		except ValueError:
			proto, dummy, host = url.split('/', 2)
			path = ''
		if proto == 'http:':
			port = 80
		elif proto == 'https:':
			import ussl
			port = 443
		else:
			raise ValueError('Unsupported protocol: ' + proto)
		
		if ':' in host:
			host, port = host.split(':', 1)
			port = int(port)
		
		# Get a tuple of address info
		ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
		ai = ai[0]
		
		s = usocket.socket(ai[0], ai[1], ai[2])
		try:
			s.connect(ai[-1])
			if proto == 'https:':
				s = ussl.wrap_socket(s, server_hostname=host)
			s.write(b'%s /%s HTTP/1.0\r\n' % (method, path))
			if not 'Host' in headers:
				s.write(b'Host: %s\r\n' % host)
			
			# Iterate over keys to avoid tuple alloc
			for k in headers:
				s.write(k)
				s.write(b': ')
				s.write(headers[k])
				s.write(b'\r\n')
				
			# add user agent
			s.write('User-Agent')
			s.write(b': ')
			s.write('MicroPython OTAUpdater')
			s.write(b'\r\n')
			
			if json is not None:
				assert data is None
				import ujson
				data = ujson.dumps(json)
				s.write(b'Content-Type: application/json\r\n')
			if data:
				s.write(b'Content-Length: %d\r\n' % len(data))
			s.write(b'\r\n')
			if data:
				s.write(data)
			
			l = s.readline()
			l = l.split(None, 2)
			status = int(l[1])
			reason = ''
			if len(l) > 2:
				reason = l[2].rstrip()
			while True:
				l = s.readline()
				if not l or l == b'\r\n':
					break
				if l.startswith(b'Transfer-Encoding:'):
					if b'chunked' in l:
						raise ValueError('Unsupported ' + l)
				elif l.startswith(b'Location:') and not 200 <= status <= 299:
					raise NotImplementedError('Redirects not yet supported')
		except OSError:
			s.close()
			raise
		
		resp = Response(s)
		resp.status_code = status
		resp.reason = reason
		
		if dtype == 'json':
			data = resp.json()
			resp.close()
			gc.collect()
			return data
		elif dtype == 'text':
			data = resp.text
			resp.close()
			gc.collect()
			return data
		else:
			return resp
	
	def head(self, url, **kw):
		return self.request('HEAD', url, **kw)
	
	def get(self, url, **kw):
		return self.request('GET', url, **kw)
	
	def post(self, url, **kw):
		return self.request('POST', url, **kw)
	
	def put(self, url, **kw):
		return self.request('PUT', url, **kw)
	
	def patch(self, url, **kw):
		return self.request('PATCH', url, **kw)
	
	def delete(self, url, **kw):
		return self.request('DELETE', url, **kw)
