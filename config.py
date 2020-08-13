rss_service = dict(
	# note that not all RSS feeds have media_content
	url='https://www.theguardian.com/world/rss'
	# url='https://ct24.ceskatelevize.cz/rss/hlavni-zpravy'
)
met_service = dict(
	url='https://api.met.no/weatherapi/locationforecast/2.0/compact',
	user_agent='RaspberryPiHomeDashboard/0.1 https://github.com/schmidltomas',
	lat='<HOMETOWN_LATITUDE>',
	lon='<HOMETOWN_LONGITUDE>',
	altitude='<HOMETOWN_ALTITUDE>'
)
gdm_service = dict(
	origin='<HOME_ADDRESS>',
	destination='<WORK_ADDRESS>',
	mode='driving',
	units='metric',
	# language='cs',
	language='en',
	api_key='<GOOGLE_API_KEY>'
)
