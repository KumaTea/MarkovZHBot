import logging
from queue import Queue
from telegram import Bot
from botInfo import self_id
from baseTools import query_token
from telegram.ext import Dispatcher
from apscheduler.schedulers.background import BackgroundScheduler


markov = Bot(query_token(self_id))
update_queue = Queue()
dp = Dispatcher(markov, update_queue, use_context=True)

scheduler = BackgroundScheduler(misfire_grace_time=60)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
