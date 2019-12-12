from telegram import Bot
from telegram.ext import Dispatcher
from botInfo import self_id
from botTools import query_token
from queue import Queue


markov = Bot(query_token(self_id))
update_queue = Queue()
dp = Dispatcher(markov, update_queue, use_context=True)

brain_token = query_token('brain')
