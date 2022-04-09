from functions import *
from session import markov
from pyrogram import filters
from pyrogram.handlers import MessageHandler


def register_handlers():
    markov.add_handler(MessageHandler(private_reply, filters.private))
    return True
