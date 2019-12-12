from markov import gen_msg
from brainInfo import sentences_per_request, keyword_retry
try:
    from localDB import chat
except ImportError:
    from emptyLocalDB import chat


def generate(data):
    """
    data = {
        'chat_id': chat_id,
        'user_id': user_id,
        'keyword': keyword,
    }
    """
    # DO STAT BEFORE CHAT_ID CHANGED
    chat_id = data['chat_id']
    if chat_id in chat and 'combine' in chat[chat_id]:
        chat_id = chat[chat_id]['combine']
    user_id = data['user_id']
    keyword = data['keyword']
    generate_list = data['generate_list']

    sentences_list = []

    if keyword:
        for i in range(keyword_retry):
            sentence = gen_msg(chat_id)
            if sentence:
                if keyword in sentence:
                    break
                else:
                    sentences_list.append(sentence)
        sentence = '指定关键词生成失败。'
    else:
        sentence = gen_msg(chat_id)
        if generate_list:
            for i in range(sentences_per_request):
                list_sentence = gen_msg(chat_id)
                if list_sentence:
                    sentences_list.append(list_sentence)

    response = {
        'response': True,
        'chat_id': data['chat_id'],
        'user_id': data['user_id'],
        'keyword': data['keyword'],
        'sentence': sentence,
        'sentences_list': sentences_list
    }

    return response
