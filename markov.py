import os
import jieba
import markovify
import random
from modelCache import models
from botInfo import large_size
from localDB import chat


punctuation = ['，', '。', '？', '?']
punctuation_en = [',', '.', '?', '!', '_']
ignore = ['http', '【', 'likenum', '#']
ignore_starting = ['@']
error_msg = '生成句子失败了，请重试。'


def format_in(message):
    for item in punctuation:
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
    return new_sen.replace('  ', ' ').replace('@ ', ' @')


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
        with open(f'data/{chat_id}.txt', 'a', encoding='UTF-8') as f:
            f.write(f'\n{format_message}')
    return True


def gen_sentence(model, space='English', retry_times=10):
    sentence = model.make_sentence()
    retry = 0
    while not sentence:
        sentence = model.make_sentence()
        retry += 1
        if retry > retry_times:
            return error_msg
    if space == 'English':
        # English determination
        return format_out(sentence)
    elif space:
        return sentence
    else:
        return sentence.replace(' ', '')


def gen_msg(chat_id, space='English', cache=False, retry_times=10):
    if chat_id in chat:
        if 'combine' in chat[chat_id]:
            chat_id = chat[chat_id]['combine']
    if cache or chat_id in models:
        if random.random() > 0.1:
            sentence = gen_sentence(models[chat_id], space, 3)
        else:
            if os.path.getsize(f'data/{chat_id}.txt') > large_size:
                with open(f'data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
                    markov = markovify.Text(f, retain_original=False)
            else:
                with open(f'data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
                    markov = markovify.Text(f)
            sentence = gen_sentence(markov, space, 3)
            models[chat_id] = markov
            print(f'[INFO] Generated new model for {chat_id}')
        return sentence
    else:
        try:
            with open(f'data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
                markov = markovify.Text(f)
                sentence = gen_sentence(markov, space, retry_times)
            return sentence

        except FileNotFoundError:
            return error_msg
