import re
import jieba
from data import *


punctuation_en = [',', '?', '!']
no_space = ['_', '.']
switch_space = ['@', '/']
ignore = ['http', '【', 'likenum', '#']
ignore_starting = ['@']
error_msg = '生成句子失败了，请重试。'

url_regex = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9]+\.[^\s]{2,}'


def skip_message(text):
    # commands
    if text.startswith('/'):
        return True

    # contains url
    if re.search(url_regex, text):
        return True

    return False


def process_message(text):
    return text
