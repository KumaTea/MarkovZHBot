import os
import json
import brainCache
import markovify
from brainInfo import large_size


def write_msg():
    for chat in brainCache.msg_db:
        with open(f'../data/{chat}.txt', 'a', encoding='UTF-8') as f:
            f.write(brainCache.msg_db[chat])
        print(f'[INFO] Wrote message of {chat}.')
    brainCache.msg_db = {}
    return True


def write_stat():
    for chat in brainCache.stat_db:
        with open(f'../stat/{chat}.json', 'w') as f:
            json.dump(brainCache.stat_db[chat], f)
        print(f'[INFO] Wrote stat of {chat}.')
    brainCache.stat_db = {}
    return True


def renew_model(chat_id):
    if os.path.getsize(f'../data/{chat_id}.txt') > large_size:
        with open(f'../data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
            markov = markovify.Text(f, retain_original=False)
    else:
        with open(f'../data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
            markov = markovify.Text(f)
    brainCache.models[chat_id] = markov
    print(f'[INFO] Generated new model for {chat_id}')
    return True
