import jieba
import markovify


punctuation = ['，', '。', '？', '?']
ignore = ['http', '【']


def msg_format(message):
    for item in punctuation:
        message = message.replace(f'{item} {item} {item}', f'{item}{item}{item}')
    return message


def save_msg(chat_id, message):
    save = True
    for item in ignore:
        if item in message:
            save = False
    if save:
        cut_message = (' '.join(jieba.cut(message)))
        format_message = msg_format(cut_message)
        with open(f'data/{chat_id}.txt', 'a', encoding='UTF-8') as f:
            f.write(f'\n{format_message}')
    return True


def gen_msg(chat_id, space=False):
    error_msg = '生成句子失败了，请重试。'
    try:
        with open(f'data/{chat_id}.txt', 'r', encoding='UTF-8') as f:
            markov = markovify.Text(f)
            sentence = markov.make_sentence()
            retry = 0
            while not sentence:
                sentence = markov.make_sentence()
                retry += 1
                if retry > 10:
                    return error_msg
            if space:
                return sentence
            else:
                return sentence.replace(' ', '')

    except FileNotFoundError:
        return error_msg
