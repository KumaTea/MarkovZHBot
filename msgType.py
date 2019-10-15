from botSession import bot
from mdGroup import Group


def msg_type(data):
    chat_id = bot.get(data).chat('id')
    message_type = bot.get(data).message('type')

    if chat_id < 0:
        if 'text' in message_type:
            resp = Group(data).text()
        else:
            resp = 'ignore'

    else:
        resp = 'ignore'

    return resp
