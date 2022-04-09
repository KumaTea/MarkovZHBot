import logging
from tools import mkdir
from session import logger


def initialize():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    mkdir('data')

    return logger.info("Initialized.")
