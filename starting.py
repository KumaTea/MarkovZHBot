import os
import requests
import markovify
from botSession import bot
from tools import del_files
from mdStat import reset_stat, read_stat
from modelCache import models, blacklist
from scheduler import scheduler
from botInfo import cool_threshold, trig_rate, cache_size, large_size


def getadminid():
    adminex = os.path.isfile('adminid.txt')
    if adminex:
        with open('adminid.txt', 'r') as admid:
            adminid = list(map(int, admid.readlines()))
    else:
        adminid = [0]  # not set!
    return adminid


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
                models[chat_id] = markovify.Text(f, retain_original=False)
            else:
                models[chat_id] = markovify.Text(f)
        print(f'[INFO] Generated.')


def pre_blacklist():
    chats = []
    for i in os.listdir('data'):
        if os.path.isfile(f'data/{i}'):
            chats.append(int(i.replace('.txt', '')))
    for i in chats:
        re_c, m_msg, m_cmd, sd_c, kw, date, size = read_stat(i)
        if sd_c:
            if sd_c > cool_threshold:
                blacklist[i] = trig_rate
                print(f'[INFO] Chat {i} in blacklist today...')


def starting():
    mkdir(['data', 'stat', 'admin'])
    del_files('admin')
    del_files('stat')
    if 'nt' in os.name:
        webhook_url = get_webhook(port=4041)
        set_proxy()
        set_webhook(webhook_url)
    else:
        webhook_url = get_webhook()
        set_webhook(webhook_url)
    pre_model()
    scheduler.add_job(reset_stat, 'cron', hour=0, minute=0)
    scheduler.start()
    print('[INFO] Starting fine.')
