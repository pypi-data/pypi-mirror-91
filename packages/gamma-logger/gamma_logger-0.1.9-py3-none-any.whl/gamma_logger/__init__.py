from logging import getLogger
from logging import config
from os import path
from os import makedirs
from os import getcwd

class logger():
    
    def __init__(self, name):
        """Initialises the logger object"""
        if not path.exists(path.join(getcwd(), "logs")):
            makedirs(path.join(getcwd(), "logs"))
        this_dir, this_filename = path.split(__file__)
        CONF_PATH = path.join(this_dir, "logging.conf")
        config.fileConfig(CONF_PATH)
        self.name = name
        self.logger = getLogger(self.name)
        
    def write_to_log(self, error_msg, error_type='C'):
        """Writes the error message to log"""
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
