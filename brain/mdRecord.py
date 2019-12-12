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
        'text_list': text_list,
    }
    """
    chat_id = data['chat_id']
    if chat_id in chat and 'combine' in chat[chat_id]:
        chat_id = chat[chat_id]['combine']
    user_id = data['user_id']
    text_list = data['text_list']
    
    if chat_id in chat:
        if 'append' in chat[chat_id]:
            for item in text_list:
                save_msg(chat_id, item)
                save_msg(chat[chat_id]['append'], item)
                # stat_receive(chat_id, user_id, 'msg')
        elif 'combine' in chat[chat_id]:
            for item in text_list:
                save_msg(chat[chat_id]['combine'], item)
                # stat_receive(chat_id, user_id, 'msg')
        else:
            for item in text_list:
                save_msg(chat_id, item)
                # stat_receive(chat_id, user_id, 'msg')
    else:
        for item in text_list:
            save_msg(chat_id, item)
        # stat_receive(chat_id, user_id, 'msg')
    return True
