import logging
from session import logger
from register import register_handlers


def initialize():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    register_handlers()
    return logger.info("Initialized.")
