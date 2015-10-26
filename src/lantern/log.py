# coding: utf-8
import logging

from config import LOGGING_LEVEL, LOGGING_FILE

def create_logger(name, console=False):
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)

    if console:
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler(LOGGING_FILE)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
