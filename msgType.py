from botSession import bot
from mdGroup import Group


def msg_type(data):
    bot_getter = bot.get(data)
    chat_id = bot_getter.chat('id')
    message_type = bot_getter.message('type')

    if chat_id < 0:
        if 'text' in message_type:
            resp = Group(data).text()
        else:
            resp = 'ignore'

    else:
        resp = 'ignore'

    return resp
