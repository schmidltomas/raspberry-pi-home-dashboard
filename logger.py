import logging
from datetime import datetime

''' Simple file logger class.'''

logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)
timestamp = str(datetime.timestamp(datetime.now())).split('.')[0]
file_handler = logging.FileHandler('app_' + timestamp + '.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def debug(msg):
	logger.debug(msg)


def info(msg):
	logger.info(msg)


def error(msg):
	logger.error(msg)
