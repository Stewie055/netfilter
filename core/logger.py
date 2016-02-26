import logging
import sys


class logger:

    log_level = 0
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def setup_logger(self, name, formatter, logfile='./logs/mitm.log'):
        fileHandler = logging.FileHandler(logfile)
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.propagate = False
        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)
        logger.setLevel(self.log_level)

        return logger
