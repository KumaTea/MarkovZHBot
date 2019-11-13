from botSession import bot
from markov import gen_msg
from tools import get_chat_admin
from threading import Timer
from modelCache import name
from mdStat import stat_receive, stat_send, read_stat
import time
import random
from modelCache import blacklist
from botInfo import self_id, cool_threshold, trig_rate
try:
    import localDB
except ImportError:
    import emptyLocalDB as localDB


def group_cmd(chat_id, command, msg_id, reply_to=None, del_cmd=True, del_msg=True, user_id=None, reply_to_user=None):
    """
    chat_id, command, msg_id, reply_to=None, del_cmd=True, del_msg=True, user_id=None, reply_to_user=None
    """
    command = command[1:]
    is_admin = self_id in get_chat_admin(chat_id)
    sd_c = None

    if command.startswith(('speak', 'say', 'markov', '说')):
        msg = gen_msg(chat_id)
        stat_receive(chat_id, user_id, 'cmd')
        if is_admin and del_cmd:
            bot.delete(chat_id, msg_id).message()
        if reply_to:
            result = bot.send(chat_id).message(msg, reply_to=reply_to)
        else:
            result = bot.send(chat_id).message(msg)

    elif command.startswith(('space', 'loud', '空格')):
        msg = gen_msg(chat_id, True)
        stat_receive(chat_id, user_id, 'cmd')
        if is_admin and del_cmd:
            bot.delete(chat_id, msg_id).message()
        if reply_to:
            result = bot.send(chat_id).message(msg, reply_to=reply_to)
        else:
            result = bot.send(chat_id).message(msg)

    elif command.startswith('stat'):
        start_time = int(time.time() * 1000)
        msg = None
        stat_receive(chat_id, user_id, 'cmd')
        re_c, m_msg, m_cmd, sd_c, kw, date, size = read_stat(chat_id)
        try:
            if date:
                start_msg = '查询统计数据中，请稍后。。。'
                sent_start = bot.send(chat_id).message(start_msg)
                sent_start_id = bot.get(sent_start).message('id')
                if m_msg in name:
                    mm_f, mm_l = name[m_msg]
                else:
                    m_msg_u = bot.query(chat_id).chat_member(m_msg)
                    mm_f, mm_l = m_msg_u['first_name'], m_msg_u.get('last_name', '')
                    name[m_msg] = mm_f, mm_l
                if m_cmd in name:
                    mc_f, mc_l = name[m_cmd]
                else:
                    m_cmd_u = bot.query(chat_id).chat_member(m_cmd)
                    mc_f, mc_l = m_cmd_u['first_name'], m_cmd_u.get('last_name', '')
                    name[m_cmd] = mc_f, mc_l

                stat_msg = f'今天是{date}，以下是数据报告：\n' \
                           f'我共学习{re_c}次，说话{sd_c}次。kw' \
                           f'今天发言最多的是{mm_f}{mm_l}，让我说话最多的是{mc_f}{mc_l}。\n' \
                           f'本群目前的数据量为{size}。' \
                           f'本次查询花费了delayed_time_length秒。'
                if kw:
                    kw_k, kw_v = '', ''
                    for i in kw:
                        kw_k, kw_v = i, kw[i]
                    to_send = stat_msg.replace('。kw', f'，其中{kw_k}了{kw_v}次。')
                else:
                    to_send = stat_msg.replace('kw', '')
                if (mm_f, mm_l) == (mc_f, mc_l):
                    to_send = to_send.replace('让我说话最多的是', '让我说话最多的也是')
                if chat_id in localDB.chat:
                    if 'replace' in localDB.chat[chat_id]:
                        if localDB.chat[chat_id]['replace']:
                            for i in localDB.chat[chat_id]['replace']:
                                to_send = to_send.replace(i, localDB.chat[chat_id]['replace'][i])
                end_time = int(time.time() * 1000)
                to_send = to_send.replace('delayed_time_length', str((end_time - start_time) / 1000))
                result = bot.edit(chat_id, sent_start_id).message(to_send)
            else:
                print('[INFO] Stat: No date')
                result = False
        except KeyError:
            print('[ERROR] Stat: KeyError')
            result = False

    elif command.startswith(('re', 'new', 'ano', 'change')):
        if reply_to and reply_to_user == self_id:
            msg = gen_msg(chat_id)
            stat_receive(chat_id, user_id, 'cmd')
            if is_admin and del_cmd:
                bot.delete(chat_id, msg_id).message()
            result = bot.edit(chat_id, reply_to).message(msg)
        else:
            msg = None
            result = False

    else:
        msg = None
        result = False

    if result:
        if chat_id in localDB.chat:
            kw = localDB.chat[chat_id].get('keyword', False)
            if kw and msg and kw in msg:
                stat_send(chat_id, kw)
            else:
                stat_send(chat_id)
        else:
            stat_send(chat_id)
        if del_msg:
            try:
                sent_meg = bot.get(result).message('id')
                del_sent = Timer(21600, bot.delete(chat_id).message, [sent_meg])
                del_sent.start()
            except KeyError:
                print('[ERROR] KeyError, ignoring...')
        else:
            print(f'[INFO] Not delete message for chat {chat_id}')
        if sd_c:
            if sd_c > cool_threshold and chat_id not in blacklist:
                blacklist[chat_id] = trig_rate
                bot.send(chat_id).message(f'由于本群今日触发量超过{cool_threshold}，本群已于今日进入冷却名单。')
                print(f'[INFO] Adding {chat_id} into blacklist...')
        else:
            if random.random() > 0.9:
                re_c, m_msg, m_cmd, sd_c, kw, date, size = read_stat(chat_id)
                if sd_c:
                    if sd_c > cool_threshold and chat_id not in blacklist:
                        blacklist[chat_id] = trig_rate
                        print(f'[INFO] Adding {chat_id} into blacklist...')
                        bot.send(chat_id).message(f'由于本群今日触发量超过{cool_threshold}，本群已于今日进入冷却名单。')

    return result
