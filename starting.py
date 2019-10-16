import os
import requests
from botSession import bot


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
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if folder:
        if type(folder) == list or type(folder) == tuple:
            for items in folder:
                if not os.path.exists(str(items)):
                    os.mkdir(str(items))
        else:
            if not os.path.exists(str(folder)):
                os.mkdir(str(folder))


def del_admin(filename='admin'):
    files = []
    for i in os.listdir():
        if os.path.isfile(i) and filename in i:
            files.append(i)
    for i in files:
        os.remove(i)
        print(f'Deleted \'{i}\'')


def starting():
    mkdir('data')
    del_admin()
    webhook_url = get_webhook(port=4041)
    set_proxy(port=10080)
    set_webhook(webhook_url)
    print('Starting fine.')
