from botSession import dp
from mdFunctions import *
from telegram.ext import MessageHandler, CommandHandler, Filters


def register_handlers():
    dp.add_handler(CommandHandler(['say', 'speak', 'markov'], say, Filters.group))
    dp.add_handler(CommandHandler(['new', 'ano', 'change'], new, Filters.group))
    dp.add_handler(CommandHandler(['stat', 'total'], stat, Filters.group))

    dp.add_handler(MessageHandler(Filters.group & (~ Filters.command), record))

    dp.add_handler(MessageHandler(Filters.private, private))
    return True
