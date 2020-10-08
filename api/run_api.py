from core.http_requests import HttpClient
from machine import unique_id

def board_id():
	uid = unique_id()
	return '{:02x}{:02x}{:02x}{:02x}'.format(uid[0], uid[1], uid[2], uid[3])

def api_get():
	req = HttpClient()
	print("Sending GET request")
	response = req.get("https://2a0e4a14-bbcd-49c2-9679-41557c0e4eb6.mock.pstmn.io/user?id=1480977", dtype='json')
	print("Request sent")
	print(response)