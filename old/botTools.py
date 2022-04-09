import os
import botCache
from time import time
from botSession import logger
from baseTools import del_files
from botInfo import chat_expire_time


def reset_cache():
    del_files('stat')
    botCache.black_chats = {}
    botCache.triggered_users = []
    botCache.names = {}
    botCache.stat_db = {}
    logger.info('[INFO] Cache reset.')


def reset_triggered_user():
    botCache.triggered_users = []


def remove_inactive_chats(path='data'):
    files = []
    current = time()
    for i in os.listdir(path):
        if os.path.isfile(f'{path}/{i}'):
            files.append(f'{path}/{i}')
    for i in files:
        if current - os.path.getmtime(i) > chat_expire_time:
            os.remove(i)
            logger.warning(f'[INFO] Deleted {i}')
