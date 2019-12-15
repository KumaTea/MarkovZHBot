from botSession import markov
from botInfo import bot_url


def set_frp(url, path=None):
    return markov.set_webhook(url, path)


def starting():
    set_frp(bot_url)
    print('[INFO] Starting fine.')
