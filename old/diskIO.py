import os
import json
import gzip
import botCache
import markovify
from botInfo import large_size


def write_msg():
    for chat in botCache.msg_db:
        with gzip.open(f'data/text/{chat}.gz', 'rb') as f:
            text = f.read()
        with gzip.open(f'data/text/{chat}.gz', 'wb') as f:
            f.write(text + botCache.msg_db[chat].encode('utf-8'))
        print(f'[INFO] Wrote message of {chat}.')
    botCache.msg_db = {}
    return True


# def write_stat():
#     for chat in botCache.stat_db:
#         with open(f'stat/{chat}.json', 'w') as f:
#             json.dump(botCache.stat_db[chat], f)
#         print(f'[INFO] Wrote stat of {chat}.')
#     botCache.stat_db = {}
#     return True


def renew_model(chat_id):
    if os.path.getsize(f'data/text/{chat_id}.gz') > large_size:
        with gzip.open(f'data/text/{chat_id}.gz', 'rb') as f:
            markov = markovify.Text(f.read().decode('utf-8'), retain_original=False)
    else:
        with gzip.open(f'data/text/{chat_id}.gz', 'rb') as f:
            markov = markovify.Text(f.read().decode('utf-8'))
    botCache.models[chat_id] = markov
    print(f'[INFO] Generated new model for {chat_id}')
    return True
