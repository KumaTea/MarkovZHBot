import os
import json
from datetime import datetime

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
    files = []
    for i in os.listdir('stat'):
        if os.path.isfile(i):
            files.append(i)
    for i in files:
        os.remove(i)
        print(f'Deleted \'{i}\'')


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

    stat_data['send']['count'] += 1
    if keyword:
        kw_count = stat_data['send']['keyword'].get(keyword, 0)
        stat_data['send']['keyword'][keyword] = kw_count + 1


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
        return None, None, None, None, None, None

    if stat_data['send']['keyword']:
        kw = stat_data['send']['keyword']
    else:
        kw = None
    re_c = stat_data['receive']['count']
    m_msg = most(stat_data['receive']['msg_by'])
    m_cmd = most(stat_data['receive']['cmd_by'])
    sd_c = stat_data['send']['count']
    date = stat_data['date']
    return re_c, m_msg, m_cmd, sd_c, kw, date
