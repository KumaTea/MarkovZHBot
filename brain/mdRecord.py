from markov import save_msg
try:
    from localDB import chat
except ImportError:
    from emptyLocalDB import chat
# from mdStat import stat_receive


def record(data):
    """
        data = {
        'chat_id': chat_id,
        'user_id': user_id,
        'text': text,
    }
    """
    chat_id = data['chat_id']
    if chat_id in chat and 'combine' in chat[chat_id]:
        chat_id = chat[chat_id]['combine']
    user_id = data['user_id']
    text = data['text']
    
    if chat_id in chat:
        if 'append' in chat[chat_id]:
            resp = save_msg(chat_id, text)
            save_msg(chat[chat_id]['append'], text)
            # stat_receive(chat_id, user_id, 'msg')
        elif 'combine' in chat[chat_id]:
            resp = save_msg(chat[chat_id]['combine'], text)
            # stat_receive(chat_id, user_id, 'msg')
        else:
            resp = save_msg(chat_id, text)
            # stat_receive(chat_id, user_id, 'msg')
    else:
        resp = save_msg(chat_id, text)
        # stat_receive(chat_id, user_id, 'msg')
    return resp
