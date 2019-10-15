import jieba
import markovify


def save_msg(chat_id, message):
    cut_message = (' '.join(jieba.cut(message)))
    with open(f'data/{chat_id}.txt', 'a', encoding='UTF-8') as f:
        f.write(f'\n{cut_message}')
    return True


def gen_msg(chat_id, space=False):
    error_msg = '目前发言过少，无法生成句子，请加大力度。'
    try:
        with open(f'data/{chat_id}.txt', 'r') as f:
            markov = markovify.Text(f)
            sentence = markov.make_sentence()
            if sentence:
                if space:
                    return sentence
                else:
                    return sentence.replace(' ', '')
            else:
                return error_msg
    except FileNotFoundError:
        return error_msg
