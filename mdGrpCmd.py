from botSession import bot
from markov import gen_msg
from botInfo import selfid
from tools import get_chat_admin
from threading import Timer


def group_cmd(chat_id, command, msg_id, reply_to=None):
    command = command[1:]
    is_admin = selfid in get_chat_admin(chat_id)

    if command.startswith(('speak', 'say', 'markov', '说')):
        msg = gen_msg(chat_id)
        if is_admin:
            bot.delete(chat_id, msg_id).message()
        if reply_to:
            result = bot.send(chat_id).message(msg, reply_to=reply_to)
        else:
            result = bot.send(chat_id).message(msg)

    elif command.startswith(('space', 'loud', '空格')):
        msg = gen_msg(chat_id, True)
        if is_admin:
            bot.delete(chat_id, msg_id).message()
        if reply_to:
            result = bot.send(chat_id).message(msg, reply_to=reply_to)
        else:
            result = bot.send(chat_id).message(msg)

    else:
        result = False

    if result:
        sent_meg = bot.get(result).message('id')
        del_sent = Timer(1800, bot.delete(chat_id).message, [sent_meg])
        del_sent.start()

    return result
