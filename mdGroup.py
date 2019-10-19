from botSession import bot
from mdGrpCmd import group_cmd
from markov import save_msg
from botInfo import self_id
from mdStat import stat_receive


class Group:

    def __init__(self, data):
        self.data = data
        bot_getter = bot.get(data)
        self.chat_id = bot_getter.chat('id')
        self.msg = bot_getter.message()
        self.msg_id = bot_getter.message('id')
        self.reply_to = bot_getter.reply('id')
        self.reply_to_user = bot_getter.reply('user')
        self.user_id = bot_getter.user('id')

    def text(self):
        if self.msg.startswith('/'):
            resp = group_cmd(self.chat_id, self.msg, self.msg_id, self.reply_to, user_id=self.user_id)
        else:
            resp = save_msg(self.chat_id, self.msg)
            stat_receive(self.chat_id, self.user_id, 'msg')
            if self.reply_to_user == self_id:
                group_cmd(self.chat_id, '/say', self.msg_id, self.msg_id, False, user_id=self.user_id)
        return resp
