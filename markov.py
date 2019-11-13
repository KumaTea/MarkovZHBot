import os
import jieba
import markovify
import random
from modelCache import models
from botInfo import large_size


punctuation = ['，', '。', '？', '?']
ignore = ['http', '【', 'likenum', '#']
ignore_starting = ['@']
error_msg = '生成句子失败了，请重试。'


def msg_format(message):
    for item in punctuation:
        message = message.replace(f'{item} {item} {item}', f'{item}{item}{item}')
    return message


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
        format_message = msg_format(cut_message)
        with open(f'data/{chat_id}.txt', 'a', encoding='UTF-8') as f:
            f.write(f'\n{format_message}')
    return True


def gen_sentence(model, space, retry_times=10):
    sentence = model.make_sentence()
    retry = 0
    while not sentence:
        sentence = model.make_sentence()
        retry += 1
        if retry > retry_times:
            return error_msg
    if space:
        return sentence
    else:
        return sentence.replace(' ', '')


def gen_msg(chat_id, space=False, cache=False, retry_times=10):
    if cache or chat_id in models:
        if random.random() > 0.1:
            sentence = gen_sentence(models[chat_id], space, 3)
        else:
            with open(f'data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
                if os.path.getsize('') > large_size:
                    markov = markovify.Text(f, retain_original=False)
                else:
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
