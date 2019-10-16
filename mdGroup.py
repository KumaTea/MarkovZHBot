from botSession import bot
from mdGrpCmd import group_cmd
from markov import save_msg


class Group:

    def __init__(self, data):
        self.data = data
        bot_getter = bot.get(data)
        self.chat_id = bot_getter.chat('id')
        self.msg = bot_getter.message()
        self.msg_id = bot_getter.message('id')
        self.reply_to = bot_getter.reply('id')

    def text(self):
        if self.msg.startswith('/'):
            resp = group_cmd(self.chat_id, self.msg, self.msg_id)
        else:
            resp = save_msg(self.chat_id, self.msg)
        return resp
