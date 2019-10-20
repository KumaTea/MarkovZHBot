from botSession import bot
from mdGrpCmd import group_cmd
from markov import save_msg
from botInfo import self_id
from mdStat import stat_receive
import localDB
import time
from threading import Thread
from modelCache import cool_status


chat_id = 0


def cooler(chat):
    def executor(func):
        if chat in cool_status:
            if cool_status[chat]:
                t = Thread(target=do_colling, args=[chat])
                t.start()
                return func
            else:
                print('Cooling...')
        else:
            t = Thread(target=do_colling, args=[chat])
            t.start()
            return func
    return executor


def do_colling(chat, cool_time=2):
    cool_status[chat] = False
    time.sleep(cool_time)
    cool_status[chat] = True


class Group:

    def __init__(self, data):
        self.data = data
        bot_getter = bot.get(data)
        self.chat_id = bot_getter.chat('id')
        global chat_id
        chat_id = self.chat_id
        self.msg = bot_getter.message()
        self.msg_id = bot_getter.message('id')
        self.reply_to = bot_getter.reply('id')
        self.reply_to_user = bot_getter.reply('user')
        self.user_id = bot_getter.user('id')
        self.delete = (localDB.chat[self.chat_id]['delete'] if 'delete' in localDB.chat[self.chat_id] else True) \
            if self.chat_id in localDB.chat else True

    @cooler(chat_id)
    def text(self):
        if self.msg.startswith('/'):
            resp = group_cmd(
                self.chat_id, self.msg, self.msg_id, self.reply_to, del_msg=self.delete, user_id=self.user_id)
        else:
            if self.chat_id in localDB.chat:
                if 'append' in localDB.chat[self.chat_id]:
                    resp = save_msg(self.chat_id, self.msg)
                    save_msg(localDB.chat[self.chat_id]['append'], self.msg)
                    stat_receive(self.chat_id, self.user_id, 'msg')
                else:
                    resp = save_msg(self.chat_id, self.msg)
                    stat_receive(self.chat_id, self.user_id, 'msg')
            else:
                resp = save_msg(self.chat_id, self.msg)
                stat_receive(self.chat_id, self.user_id, 'msg')
            if self.reply_to_user == self_id:
                group_cmd(self.chat_id, '/say', self.msg_id, self.msg_id, False, user_id=self.user_id)
        return resp
