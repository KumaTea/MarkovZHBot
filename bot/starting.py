import requests
from botSession import markov


def get_webhook(index=0, port=4040):
    return requests.get(f'http://127.0.0.1:{port}/api/tunnels').json()['tunnels'][index]['public_url']


def set_webhook(url):
    webhook_url = url.replace('http:', 'https:')
    result = markov.set_webhook(webhook_url)


def starting():
    webhook_url = get_webhook(port=4041)
    set_webhook(webhook_url)
    print('[INFO] Starting fine.')
