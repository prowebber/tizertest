def createParamsJs():
	from assets.config_man import get_config
	
	config = get_config()  # Load the config
	
	text = "var params={" \
	       "'ssid':'" + config['wifi_ssid'] + "'," \
	       "'pass':'" + config['wifi_pass'] + "'," \
	       "'wifi_status':'" + str(config['wifi_status']) + "" \
	       "'};"
	
	f = open('/webserver/params.js', 'w')
	f.write(text)
	f.close()
