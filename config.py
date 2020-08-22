rss_service = dict(
	# note that not all RSS feeds have media_content
	url='http://rss.cnn.com/rss/edition_world.rss'
	# url='https://www.theguardian.com/world/rss'
	# url='http://www.independent.co.uk/news/world/rss'
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
	locale='en_GB.utf8',
	# locale='cs_CZ.utf8',
	first_name='Tom'
)
texts = dict(
	en_GB=dict(
		today='TODAY',
		tomorrow='TOMORROW',
		time_to_work='TIME TO WORK',
		morning=' morning, ',
		afternoon=' afternoon, ',
		morning_afternoon_adjectives=['Good', 'Great', 'Beautiful'],
		evening=' evening, ',
		evening_adjectives=['Good', 'Great', 'Beautiful'],
		night=' night, ',
		night_adjectives=['Good', 'Great', 'Beautiful'],
	),
	cs_CZ=dict(
		today='DNES',
		tomorrow='ZÍTRA',
		time_to_work='ČAS DO PRÁCE',
		morning=' ráno, ',
		afternoon=' odpoledne, ',
		morning_afternoon_adjectives=['Dobré', 'Krásné', 'Hezké'],
		evening=' večer, ',
		evening_adjectives=['Dobrý', 'Krásný', 'Hezký'],
		night=' noc, ',
		night_adjectives=['Dobrou', 'Krásnou', 'Hezkou']
	)
)
