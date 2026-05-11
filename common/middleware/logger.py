import logging
import sys

logger = logging.getLogger("ems_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s -  %(message)s")
 
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)