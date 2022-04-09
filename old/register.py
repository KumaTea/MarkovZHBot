from botSession import dp
from mdFunctions import *
from botSession import logger
from diskIO import write_msg
from telegram.ext import MessageHandler, CommandHandler, Filters
from botTools import reset_cache, reset_triggered_user, remove_inactive_chats


def register_handlers():
    dp.add_handler(CommandHandler(['say', 'speak', 'markov'], say, Filters.group))
    dp.add_handler(CommandHandler(['new', 'ano', 'change'], new, Filters.group))

    dp.add_handler(MessageHandler(Filters.chat_type.group & (~ Filters.command), record))
    dp.add_handler(MessageHandler(Filters.chat_type.private, private))
    return True


def cron(scheduler):
    # scheduler.add_job(write_stat, 'cron', minute='*/30')
    scheduler.add_job(write_msg, 'cron', hour='*')
    scheduler.add_job(reset_cache, 'cron', hour=0, minute=2)
    scheduler.add_job(remove_inactive_chats, 'cron', hour=0, minute=3)
    # scheduler.add_job(reset_triggered_user, 'cron', minute=1)
    return logger.info('Cron jobs added')
