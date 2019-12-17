import os
import gzip
import json
import markovify
# from mdStat import read_stat
import brainCache
from brainSession import scheduler
from brainInfo import *
# from brainTools import remove_inactive_chats
from diskIO import write_msg  # , write_stat


def mkdir(folder=None):
    if folder:
        if type(folder) == list or type(folder) == tuple:
            for items in folder:
                if not os.path.exists(str(items)):
                    os.mkdir(str(items))
        else:
            if not os.path.exists(str(folder)):
                os.mkdir(str(folder))


def pre_model(size=cache_size, large=large_size):
    files = []
    for i in os.listdir('../data/text'):
        if os.path.isfile(f'../data/text/{i}') and os.path.getsize(f'../data/text/{i}') > size:
            files.append(f'../data/text/{i}')
    for i in files:
        chat_id = int(os.path.splitext(i)[0].replace('../data/text/', ''))
        print(f'[INFO] Generating cached Markov model for chat {chat_id}.')
        with gzip.open(i, 'rb') as f:
            if os.path.getsize(i) > large:
                brainCache.models[chat_id] = markovify.Text(f.read().decode('utf-8'), retain_original=False)
            else:
                brainCache.models[chat_id] = markovify.Text(f.read().decode('utf-8'))
        print(f'[INFO] Generated.')


def pre_blacklist():
    chats = []
    for i in os.listdir('../stat'):
        if os.path.isfile(f'../stat/{i}') and not i.startswith('.'):
            chats.append(int(i.replace('.json', '')))
    for i in chats:
        with open(f'../stat/{i}.json', 'r') as f:
            brainCache.stat_db[i] = json.load(f)
    for i in brainCache.stat_db:
        re_c, m_msg, m_cmd, sd_c, kw, date, size = read_stat(i)
        if sd_c and sd_c > chat_cool_threshold:
            brainCache.black_chats[i] = bl_trig_rate
            print(f'[INFO] Chat {i} in blacklist today...')


def starting():
    mkdir(['../data', '../stat', '../data/text'])
    pre_model()
    # pre_blacklist()

    # scheduler.add_job(write_stat, 'cron', minute='*/30')
    scheduler.add_job(write_msg, 'cron', minute='*/15')
    # scheduler.add_job(reset_cache, 'cron', hour=0, minute=2)
    # scheduler.add_job(remove_inactive_chats, 'cron', hour=0, minute=3)
    scheduler.start()
    print('[INFO] Starting fine.')
