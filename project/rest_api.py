from core.http_requests import HttpClient
import ujson

class Rest:
	"""
	Call the Rest API
	"""
	def __init__(self):
		self.req = HttpClient()
		self.api_root = 'http://datapeak.co/rest_api'
		self.api_ver = 'v1'
		
	def _req_url(self, endpoint):
		return self.api_root + '/' + self.api_ver.strip("/") + '/' + endpoint.lstrip("/")
		
	def get(self, endpoint):
		"""
		Perform a GET request
		"""
		return self.req.get(self._req_url(endpoint), dtype='json')
	
	def post(self, endpoint, payload=None):
		"""
		Performa a POST request
		:param payload: Dict of the body you're sending
		"""
		if payload:
			payload = ujson.dumps(payload)  # Convert dict to string
			return self.req.post(self._req_url(endpoint), data=payload, dtype='json')
		else:
			return self.req.post(self._req_url(endpoint), dtype='json')
