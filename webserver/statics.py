def createParamsJs():
	from core.config_man import get_config
	
	config = get_config()  # Load the config
	ml_sprayed = getSprayVolumeBag(config)
	
	text = "var params={"
	text += "'ml_sprayed':'" + str(ml_sprayed) + "',"
	text += "'melody':'" + config['mute'] + "',"
	text += "'spray_time':'" + config['relay_open_time_ms'] + "',"
	text += "'ssid':'" + config['wifi_ssid'] + "',"
	text += "'pass':'" + config['wifi_pass'] + "',"
	text += "'has_wifi':'" + str(config['has_wifi'])
	text += "'};"
	
	f = open('/webserver/src/js/params.js', 'w')
	f.write(text)
	f.close()


def getSprayVolumeBag(config):
	ml_per_sec = 0.8
	bag_ml = 500
	ml_sprayed = 0
	
	bag_spray_ms = int(config['bag_spray_ms'])
	if bag_spray_ms:
		ml_sprayed = round((bag_spray_ms / 1000) * ml_per_sec)
	
	return ml_sprayed
