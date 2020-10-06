from assets.http_requests import HttpClient

def api_get():
	req = HttpClient()
	print("Sending GET request")
	response = req.get("https://2a0e4a14-bbcd-49c2-9679-41557c0e4eb6.mock.pstmn.io/user?id=1480977", dtype='json')
	print("Request sent")
	print(response)