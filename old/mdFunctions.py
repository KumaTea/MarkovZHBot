import botCache
from random import choice
from botSession import markov
from mdMarkov import gen_msg, save_msg
from botInfo import self_id, private_messages, send_records


def private(update, context):
    return update.message.reply_text(choice(private_messages), quote=False)


def can_delete(chat_id):
    if chat_id in botCache.delete_privilege:
        return botCache.delete_privilege[chat_id]
    else:
        delete_status = markov.get_chat_member(chat_id, self_id).can_delete_messages
        botCache.delete_privilege[chat_id] = delete_status
        return delete_status


def say(update, context):
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id
    reply_info = message.reply_to_message
    text = message.text
    command = False

    if text and text.startswith('/'):
        command = True
    if command and can_delete(chat_id):
        markov.delete_message(chat_id, message_id)

    cached_item = None
    if chat_id in botCache.sentences_db and botCache.sentences_db[chat_id]:
        cached_item = botCache.sentences_db[chat_id].pop()

    if cached_item:
        sentence = cached_item
    else:
        # markov.send_chat_action(chat_id, 'typing')
        sentence = gen_msg(chat_id)

    if reply_info:
        if reply_info.from_user.id == self_id and not command:
            return message.reply_text(sentence)
        else:
            # is command
            return markov.send_message(chat_id, sentence, reply_to_message_id=reply_info.message_id)
    else:
        return message.reply_text(sentence, quote=False)


def new(update, context):
    message = update.message
    reply_to_message = message.reply_to_message
    if reply_to_message.from_user.id != self_id:
        return False
    chat_id = message.chat_id
    message_id = message.message_id
    user_id = message.from_user.id
    command = True

    if command and can_delete(chat_id):
        markov.delete_message(chat_id, message_id)

    # if cached
    if chat_id in botCache.sentences_db and botCache.sentences_db[chat_id]:
        sentence = botCache.sentences_db[chat_id].pop()
        return markov.edit_message_text(sentence, chat_id, reply_to_message.message_id)
    else:
        # markov.send_chat_action(chat_id, 'typing')
        sentence = gen_msg(chat_id)
        return markov.edit_message_text(sentence, chat_id, reply_to_message.message_id)


def record(update, context):
    message = update.message
    chat_id = message.chat_id
    # user_id = message.from_user.id
    text = message.text
    if message.reply_to_message and message.reply_to_message.from_user.id == self_id:
        say(update, context)
    if text:
        return save_msg(chat_id, text)
