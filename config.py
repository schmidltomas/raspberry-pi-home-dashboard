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
general = dict(
	screen_width='1920',
	screen_height='1080',
	# screen_width='840',
	# screen_height='400',
	fullscreen=0,
	borderless=0,
	show_cursor=0,
	# locale='en_GB.utf8',
	locale='cs_CZ.utf8',
	first_name='Tomáši'
)
texts = dict(
	en_GB=dict(
		today='TODAY',
		time_to_work='TIME TO WORK',
		morning='Good morning, ',
		afternoon='Good afternoon, ',
		evening='Good evening, ',
		night='Good night, ',
	),
	cs_CZ=dict(
		today='DNES',
		time_to_work='ČAS DO PRÁCE',
		morning='Dobré ráno, ',
		afternoon='Dobré odpoledne, ',
		evening='Dobrý večer, ',
		night='Dobrou noc, ',
	)
)
