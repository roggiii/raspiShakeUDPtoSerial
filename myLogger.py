
import logging
from logging.handlers import RotatingFileHandler

import os.path

# when the script is executed automatically on boot, linux needs an absolute
# path to the log file
LOG_FILE_PATH = os.path.dirname(__file__)+'/debug_file.txt'

# logger configuration
# saves file "debug_log.txt" in the same folder as the script
# one handler is needed for printing to the terminal and the other for printing to the logfile
# this avoids the need to have print()-functions and logger()-functions simultaneously
# on linux all the output from the programm should be written to the log file, otherwise ssh-terminal will get clogged up when
# this script is running in the background all the time and using the terminal window will be impossible

# how to use logger in multiple files/instances:
# https://stackoverflow.com/questions/50391429/logging-in-classes-python

logger = logging.getLogger("Auswerteskript")
logger.setLevel(logging.DEBUG)

# Create a formatter to define the log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s    %(message)s')

# Create a file handler to write logs to a file
file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5*1024*1024, backupCount=0)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create a stream handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.CRITICAL)  # You can set the desired log level for console output
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)