from data import *
from random import choice


async def private_reply(client, message):
    return await message.reply(choice(private_replies))
