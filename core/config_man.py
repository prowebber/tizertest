import json


def get_config():
	"""
	Open the JSON config file and convert to a Python dict
	"""
	with open('.sconfig') as params:
		data = json.load(params)
	return data


def save_config(config_dict):
	"""
	Update the config file with new settings
	"""
	# Save the settings
	with open('.sconfig', 'w') as data_out:
		json.dump(config_dict, data_out)

def board_id():
	from machine import unique_id
	uid = unique_id()
	return '{:02x}{:02x}{:02x}{:02x}'.format(uid[0], uid[1], uid[2], uid[3])