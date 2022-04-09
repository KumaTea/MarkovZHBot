import logging
from pyrogram import Client
from apscheduler.schedulers.background import BackgroundScheduler


markov = Client('markov')

scheduler = BackgroundScheduler(misfire_grace_time=60)

logger = logging.getLogger('markov')
# logger.setLevel(logging.INFO)
