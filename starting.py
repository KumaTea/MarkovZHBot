import os
import sys
import json
import requests
import markovify
from botSession import bot, scheduler
from mdStat import read_stat
from tools import reset_cache, reset_triggered_user, remove_inactive_chats
from diskIO import write_msg, write_stat
import botCache
from botInfo import chat_cool_threshold, bl_trig_rate, cache_size, large_size


def set_proxy(ip='127.0.0.1', port=1080, protocol='http'):
    proxy = f'{protocol}://{ip}:{port}'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy


def get_webhook(index=0, port=4040):
    return requests.get(f'http://127.0.0.1:{port}/api/tunnels').json()['tunnels'][index]['public_url']


def set_webhook(url):
    https_url = url.replace('http:', 'https:')
    result = bot.set().webhook(https_url)
    retry = 0
    while retry < 5:
        if result['ok']:
            return result['description']
        else:
            result = bot.set().webhook(url)
            retry += 1


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
    for i in os.listdir('data'):
        if os.path.isfile(f'data/{i}') and os.path.getsize(f'data/{i}') > size:
            files.append(f'data/{i}')
    for i in files:
        chat_id = int(os.path.splitext(i)[0].replace('data/', ''))
        print(f'[INFO] Generating cached Markov model for chat {chat_id}.')
        with open(i, 'r', encoding='UTF-8') as f:
            if os.path.getsize(i) > large:
                botCache.models[chat_id] = markovify.Text(f, retain_original=False)
            else:
                botCache.models[chat_id] = markovify.Text(f)
        print(f'[INFO] Generated.')


def pre_blacklist():
    chats = []
    for i in os.listdir('stat'):
        if os.path.isfile(f'stat/{i}') and not i.startswith('.'):
            chats.append(int(i.replace('.json', '')))
    for i in chats:
        with open(f'stat/{i}.json', 'r') as f:
            botCache.stat_db[i] = json.load(f)
    for i in botCache.stat_db:
        re_c, m_msg, m_cmd, sd_c, kw, date, size = read_stat(i)
        if sd_c and sd_c > chat_cool_threshold:
            botCache.black_chats[i] = bl_trig_rate
            print(f'[INFO] Chat {i} in blacklist today...')


def starting():
    mkdir(['data', 'stat'])
    if 'win32' in sys.platform:
        webhook_url = get_webhook()
        set_proxy()
        set_webhook(webhook_url)
    elif 'darwin' in sys.platform:
        webhook_url = get_webhook()
        set_proxy(port=1082)
        set_webhook(webhook_url)
    else:  # Linux
        webhook_url = get_webhook(port=4041)
        set_webhook(webhook_url)
    pre_model()
    pre_blacklist()

    scheduler.add_job(write_stat, 'cron', minute='*/30')
    scheduler.add_job(write_msg, 'cron', minute='*/15')
    scheduler.add_job(reset_cache, 'cron', hour=0, minute=2)
    scheduler.add_job(remove_inactive_chats, 'cron', hour=0, minute=3)
    scheduler.add_job(reset_triggered_user, 'cron', minute=1)
    scheduler.start()
    print('[INFO] Starting fine.')
