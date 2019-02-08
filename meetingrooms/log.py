import logging
import logging.handlers

logger = logging.getLogger('meetingrooms')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')

fileHandler = logging.handlers.RotatingFileHandler('meetingrooms.log', maxBytes=1048576, backupCount=5)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

# StreamHandler defaults to stderr
consoleHandler = logging.StreamHandler()
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
 
