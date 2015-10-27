# coding: utf-8
import logging

from config import LOGGING


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING['level'])
    logger.propagate = 0

    if LOGGING['handler'] == 'StreamHandler':
        handler = logging.StreamHandler()
    elif LOGGING['handler'] == 'FileHandler':
        handler = logging.FileHandler(LOGGING['filepath'])
    else:
        raise ValueError('please use FileHandler or StreamHandler for logging')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
