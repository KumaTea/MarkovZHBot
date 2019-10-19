from botSession import bot
from markov import gen_msg
from botInfo import self_id
from tools import get_chat_admin
from threading import Timer
from mdStat import stat_receive, stat_send, read_stat
import localDB


def group_cmd(chat_id, command, msg_id, reply_to=None, del_cmd=True, del_msg=True, user_id=None):
    command = command[1:]
    is_admin = self_id in get_chat_admin(chat_id)

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
        msg = None
        re_c, m_msg, m_cmd, sd_c, kw, date = read_stat(chat_id)
        try:
            if date:
                m_msg_u = bot.query(chat_id).chat_member(m_msg)
                mm_f, mm_l = m_msg_u['first_name'], m_msg_u.get('last_name', '')
                m_cmd_u = bot.query(chat_id).chat_member(m_cmd)
                mc_f, mc_l = m_cmd_u['first_name'], m_cmd_u.get('last_name', '')
                stat_msg = f'今天是{date}，以下是数据报告：\n' \
                           f'我共学习{re_c}次，说话{sd_c}次。kw\n' \
                           f'今天发言最多的是{mm_f}{mm_l}，指使我说话最多的则是{mc_f}{mc_l}。'
                if kw:
                    kw_k, kw_v = '', ''
                    for i in kw:
                        kw_k, kw_v = i, kw[i]
                    to_send = stat_msg.replace('。kw', f'，其中{kw_k}了{kw_v}次。')
                else:
                    to_send = stat_msg.replace('kw', '')
                if chat_id in localDB.chat:
                    if localDB.chat[chat_id]['replace']:
                        for i in localDB.chat[chat_id]['replace']:
                            to_send = to_send.replace(i, localDB.chat[chat_id]['replace'][i])
                result = bot.send(chat_id).message(to_send)
            else:
                result = False
        except KeyError:
            result = False

    else:
        msg = None
        result = False

    if result:
        if chat_id in localDB.chat:
            kw = localDB.chat[chat_id]['keyword']
            if msg and kw in msg:
                stat_send(chat_id, kw)
            else:
                stat_send(chat_id)
        else:
            stat_send(chat_id)
        if del_msg:
            sent_meg = bot.get(result).message('id')
            del_sent = Timer(1800, bot.delete(chat_id).message, [sent_meg])
            del_sent.start()

    return result
