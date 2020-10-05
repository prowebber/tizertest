import json


def get_config():
	"""
	Open the JSON config file and convert to a Python dict
	"""
	with open('/shoetizer_config.txt') as params:
		data = json.load(params)
	return data


def save_config(config_dict):
	"""
	Update the config file with new settings
	"""
	# Save the settings
	with open('/shoetizer_config.txt', 'w') as data_out:
		json.dump(config_dict, data_out)
