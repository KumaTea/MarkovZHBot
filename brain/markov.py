import jieba
import markovify
import random
import brainCache
from brainInfo import renew_rate
from diskIO import renew_model
try:
    from localDB import chat
except ImportError:
    from emptyLocalDB import chat


punctuation_zh = ['，', '。', '？', '！']
punctuation_en = [',', '?', '!']
no_space = ['_', '.']
switch_space = ['@', '/']
ignore = ['http', '【', 'likenum', '#']
ignore_starting = ['@']
error_msg = '生成句子失败了，请重试。'


def format_in(message):
    for item in punctuation_zh:
        message = message.replace(f'{item} {item} {item}', f'{item}{item}{item}')
    return message


def format_out(sentence):
    words = sentence.split(' ')
    new_sen = ''
    for item in words:
        if item.encode('UTF-8').isalpha():
            new_sen += f' {item} '
        else:
            new_sen += item
    for item in punctuation_en:
        new_sen = new_sen.replace(f' {item} ', f'{item} ')
    for item in no_space:
        new_sen = new_sen.replace(f'{item} ', f'{item}').replace(f' {item}', f'{item}')
    for item in switch_space:
        new_sen = new_sen.replace(f'{item} ', f' {item}')
    new_sen = new_sen.replace('  ', ' ')
    return new_sen


def save_msg(chat_id, message):
    save = True
    for item in ignore:
        if item in message:
            save = False
    for item in ignore_starting:
        if message.startswith(item):
            save = False
    if save:
        cut_message = (' '.join(jieba.cut(message)))
        format_message = format_in(cut_message)
        if chat_id in brainCache.msg_db:
            brainCache.msg_db[chat_id] += f'{format_message}\n'
        else:
            brainCache.msg_db[chat_id] = f'{format_message}\n'
    return True


def gen_sentence(model, space='English', retry_times=10):
    sentence = model.make_sentence()
    retry = 0
    while not sentence:
        sentence = model.make_sentence()
        retry += 1
        if retry > retry_times:
            return False
    if space == 'English':
        # English determination
        return format_out(sentence)
    elif space:
        return sentence
    else:
        return sentence.replace(' ', '')


def gen_msg(chat_id, space='English', cache=False, retry_times=10):
    if chat_id in chat and 'combine' in chat[chat_id]:
        chat_id = chat[chat_id]['combine']
    if cache or chat_id in brainCache.models:
        if random.random() < renew_rate:
            renew_model(chat_id)
        sentence = gen_sentence(brainCache.models[chat_id], space, 3)
        return sentence
    else:
        try:
            with open(f'../data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
                markov = markovify.Text(f)
                sentence = gen_sentence(markov, space, retry_times)
            return sentence

        except FileNotFoundError:
            return error_msg
