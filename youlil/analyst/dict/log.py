import os
import logging
#from config import config


#LOG_FILENAME = os.path.expanduser(config.get('default', 'log'))

LOG_FORMAT = '%(asctime)s.%(msecs)03d [%(process)d] %(levelname)-4s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename="./dict.log", level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOG_DATEFMT)

log = logging.getLogger()

if __name__ == "__main__":
    log.debug("This is a test")