import os
import json
from datetime import datetime
import modelCache
from tools import del_files
from localDB import chat

empty_stat_data = {
    'date': '',
    'receive': {
        'count': 0,
        'msg_by': [],
        'cmd_by': [],
    },
    'send': {
        'count': 0,
        'keyword': {},
    },
}


def reset_stat():
    del_files('stat')
    modelCache.blacklist = {}
    print('[INFO] Stat reset.')


def new_stat(chat_id):
    stat_data = empty_stat_data
    stat_data['date'] = datetime.now().strftime('%Y-%m-%d')
    with open(f'stat/{chat_id}.json', 'w') as file:
        json.dump(stat_data, file)


def stat_receive(chat_id, user_id, msg_type):
    try:
        with open(f'stat/{chat_id}.json', 'r') as f:
            stat_data = json.load(f)
    except FileNotFoundError:
        stat_data = empty_stat_data
        stat_data['date'] = datetime.now().strftime('%Y-%m-%d')
    except json.decoder.JSONDecodeError:
        stat_data = empty_stat_data
        stat_data['date'] = datetime.now().strftime('%Y-%m-%d')

    stat_data['receive']['count'] += 1
    if 'message' in msg_type or 'msg' in msg_type:
        stat_data['receive']['msg_by'].append(user_id)
    else:
        stat_data['receive']['cmd_by'].append(user_id)

    with open(f'stat/{chat_id}.json', 'w') as f:
        json.dump(stat_data, f)


def stat_send(chat_id, keyword=False):
    try:
        with open(f'stat/{chat_id}.json', 'r') as f:
            stat_data = json.load(f)
    except FileNotFoundError:
        stat_data = empty_stat_data
        stat_data['date'] = datetime.now().strftime('%Y-%m-%d')
    except json.decoder.JSONDecodeError:
        stat_data = empty_stat_data
        stat_data['date'] = datetime.now().strftime('%Y-%m-%d')

    stat_data['send']['count'] += 1
    if keyword:
        kw_count = stat_data['send']['keyword'].get(keyword, 0)
        stat_data['send']['keyword'][keyword] = kw_count + 1

    with open(f'stat/{chat_id}.json', 'w') as f:
        json.dump(stat_data, f)


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
    try:
        with open(f'stat/{chat_id}.json', 'r') as f:
            stat_data = json.load(f)
    except FileNotFoundError:
        return None, None, None, None, None, None, None
    except json.decoder.JSONDecodeError:
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
