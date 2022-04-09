from functions import *
from session import markov
from pyrogram import filters
from pyrogram.handlers import MessageHandler


def register_handlers():
    markov.add_handler(MessageHandler(write_all_messages, filters.command(['write', 'save'])))
    markov.add_handler(MessageHandler(private_reply, filters.private & ~filters.edited))

    markov.add_handler(MessageHandler(record_message, filters.group & ~filters.edited))
    return True
