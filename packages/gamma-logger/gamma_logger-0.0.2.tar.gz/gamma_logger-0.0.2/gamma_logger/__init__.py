import logging
import logging.config
import os

class logger():
	def __init__(self, name):
		this_dir, this_filename = os.path.split(__file__)
		CONF_PATH = os.path.join(this_dir, "logging.conf")
		logging.config.fileConfig(CONF_PATH)
		self.name = name
		self.logger = logging.getLogger(self.name)
        
	def write_to_log(self, error_msg, error_type='C'):
		if error_type == 'D':
			self.logger.debug(error_msg)
		elif error_type == 'I':
			self.logger.info(error_msg)
		elif error_type == 'W':
			self.logger.warning(error_msg)
		elif error_type == 'E':
			self.logger.error(error_msg)
		else:	
			self.logger.critical(error_msg)
