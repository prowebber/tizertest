from core.http_requests import HttpClient


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
