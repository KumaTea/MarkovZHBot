import os
import memory
import lzma as xz
from data import *
from session import logger


def write_messages(chat_id):
    if chat_id not in memory.messages:
        return None
    if not memory.messages[chat_id]:
        return None

    history = memory.messages[chat_id].copy()
    try:
        with xz.open(os.path.join('data', f'{chat_id}.xz'), 'rb') as f:
            old_history = f.read().decode('utf-8').split('\n')
    except FileNotFoundError:
        old_history = []

    history.extend(old_history)
    history = history[:max_message_count]  # reverse order

    with xz.open(os.path.join('data', f'{chat_id}.xz'), 'wb') as f:
        f.write('\n'.join(history).encode('utf-8'))

    del memory.messages[chat_id]
    return logger.info(f'{chat_id} messages saved.')


def force_write_all_messages():
    for chat_id in memory.messages.copy():
        write_messages(chat_id)
    return True


async def record_message(client, message):
    text = message.text
    if text is None:
        return None

    chat_id = message.chat.id
    if chat_id not in memory.messages:
        memory.messages[chat_id] = []
    memory.messages[chat_id].insert(0, text)

    if len(memory.messages[chat_id]) > max_message_cache_size:
        write_messages(chat_id)
    return True
