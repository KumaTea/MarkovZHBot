from botSession import bot
from markov import gen_msg


def group_cmd(chat_id, command):

    if command.startswith(('speak', 'say', 'markov', '说')):
        msg = gen_msg(chat_id)
        result = bot.send(chat_id).message(msg)
        return result

    elif command.startswith(('space', 'loud', '空格')):
        msg = gen_msg(chat_id, True)
        result = bot.send(chat_id).message(msg)
        return result

    else:
        return 'Pass in group'
