import os
import gzip
import botCache
import markovify
from baseTools import mkdir
from register import cron
from botSession import markov, scheduler, logger
from botInfo import *
from botTools import reset_cache, reset_triggered_user, remove_inactive_chats


def pre_model():
    for i in os.listdir('data/text'):
        file_path = os.path.join('data/text', i)
        chat_id = int(os.path.splitext(i)[0].replace('data/text/', ''))
        logger.info(f'Generating cached Markov model for chat {chat_id}.')
        with gzip.open(file_path, 'rb') as f:
            if len(f.read().splitlines()) > min_message_count:
                botCache.models[chat_id] = markovify.Text(f.read().decode('utf-8')).compile()
    return logger.info(f'Generating Done.')


def starting():
    mkdir(['data'])
    pre_model()
    cron(scheduler)
    scheduler.start()
    return logger.info('[INFO] Starting fine.')
