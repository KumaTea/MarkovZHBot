import os
from datetime import datetime
import botCache
from localDB import chat


def empty_stat_data():
    return {'receive': {'count': 0, 'msg_by': [], 'cmd_by': []}, 'send': {'count': 0, 'keyword': {}}}


def stat_receive(chat_id, user_id, msg_type):
    if chat_id in botCache.stat_db:
        stat_data = botCache.stat_db[chat_id]
    else:
        stat_data = empty_stat_data()
        stat_data['chat_id'] = chat_id
        stat_data['date'] = datetime.now().strftime('%Y-%m-%d')

    stat_data['receive']['count'] += 1
    if 'message' in msg_type or 'msg' in msg_type:
        stat_data['receive']['msg_by'].append(user_id)
    else:
        botCache.triggered_users.append(user_id)
        stat_data['receive']['cmd_by'].append(user_id)

    botCache.stat_db[chat_id] = stat_data


def stat_send(chat_id, keyword=False):
    if chat_id in botCache.stat_db:
        stat_data = botCache.stat_db[chat_id]
    else:
        stat_data = empty_stat_data()
        stat_data['chat_id'] = chat_id
        stat_data['date'] = datetime.now().strftime('%Y-%m-%d')

    stat_data['send']['count'] += 1
    if keyword:
        kw_count = stat_data['send']['keyword'].get(keyword, 0)
        stat_data['send']['keyword'][keyword] = kw_count + 1

    botCache.stat_db[chat_id] = stat_data


def most(from_list):
    if from_list:
        count = 0
        num = from_list[0]
        for i in from_list:
            curr_freq = from_list.count(i)
            if curr_freq > count:
                count = curr_freq
                num = i
        return num
    else:
        return None


def read_stat(chat_id):
    if chat_id in botCache.stat_db:
        stat_data = botCache.stat_db[chat_id]
    else:
        return None, None, None, None, None, None, None

    if stat_data['send']['keyword']:
        kw = stat_data['send']['keyword']
    else:
        kw = None
    re_c = stat_data['receive']['count']
    m_msg = most(stat_data['receive']['msg_by'])
    m_cmd = most(stat_data['receive']['cmd_by'])
    sd_c = stat_data['send']['count']
    date = stat_data['date']
    if chat_id in chat:
        if 'combine' in chat[chat_id]:
            comb_chat = chat[chat_id]['combine']
            size = os.path.getsize(f'data/{comb_chat}.txt')
        else:
            size = os.path.getsize(f'data/{chat_id}.txt')
    else:
        size = os.path.getsize(f'data/{chat_id}.txt')
    if size > 1048576:
        f_size = f'{round(size/1048576, 2)}MB'
    elif size > 1024:
        f_size = f'{round(size / 1024, 2)}KB'
    else:
        f_size = f'{size}Bytes'
    return re_c, m_msg, m_cmd, sd_c, kw, date, f_size
