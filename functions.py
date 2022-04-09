from data import *
from record import *
from random import choice


async def private_reply(client, message):
    return await message.reply(choice(private_replies))


async def write_all_messages(client, message):
    if not message.chat.id == creator:
        return None
    force_write_all_messages()
    return await message.reply('Wrote all messages.')
