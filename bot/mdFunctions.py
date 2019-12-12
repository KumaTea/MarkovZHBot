from botInfo import self_id, private_message, brain_url, send_records
from botSession import markov, brain_token
import botCache
import requests


def private(update, context):
    return update.message.reply_text(private_message, quote=False)


def can_delete(chat_id):
    if chat_id in botCache.delete_privilege:
        return botCache.delete_privilege[chat_id]
    else:
        delete_status = markov.get_chat_member(chat_id, self_id).can_delete_messages
        botCache.delete_privilege[chat_id] = delete_status
        return delete_status


def contact_brain(command, data=None, method='GET'):
    content = {
        'token': brain_token,
        'command': command,
        'data': data,
    }
    if method == 'GET':
        response = requests.get(f'{brain_url}/{command}', params=content).json()
    else:
        response = requests.post(f'{brain_url}/{command}', data=content).json()
    return response


def say(update, context):
    message = update.message

    chat_id = message.chat_id
    message_id = message.message_id
    user_id = message.from_user.id

    text = message.text
    command = False
    keyword = None

    if text.startswith('/'):
        command = True
        index = text.find('')
        if index != -1:
            keyword = text[index]

    if command and can_delete(chat_id):
        markov.delete_message(chat_id, message_id)

    if botCache.sentences_db[chat_id]:
        sentence = botCache.sentences_db[chat_id].pop()
        return message.reply_text(sentence, quote=False)
    else:
        markov.send_chat_action(chat_id, 'typing')

        result = generate(chat_id, user_id, keyword)
        if result['response']:
            sentence = result['sentence']
            if result['sentences_list']:
                if chat_id in botCache.sentences_db:
                    botCache.sentences_db[chat_id].extend(result['sentences_list'])
                else:
                    botCache.sentences_db[chat_id] = result['sentences_list']
            return message.reply_text(sentence, quote=False)
        else:
            return False


def new(update, context):
    message = update.message

    reply_to_message = message.reply_to_message
    if reply_to_message.from_user.id != self_id:
        return False
    chat_id = message.chat_id
    message_id = message.message_id
    user_id = message.from_user.id

    command = True
    keyword = None

    if command and can_delete(chat_id):
        markov.delete_message(chat_id, message_id)

    if botCache.sentences_db[chat_id]:
        sentence = botCache.sentences_db[chat_id].pop()
        return markov.edit_message_text(sentence, chat_id, reply_to_message.message_id)
    else:
        markov.send_chat_action(chat_id, 'typing')

        result = generate(chat_id, user_id, keyword)
        if result['response']:
            sentence = result['sentence']
            if result['sentences_list']:
                if chat_id in botCache.sentences_db:
                    botCache.sentences_db[chat_id].extend(result['sentences_list'])
                else:
                    botCache.sentences_db[chat_id] = result['sentences_list']
            return markov.edit_message_text(sentence, chat_id, reply_to_message.message_id)
        else:
            return False


def generate(chat_id, user_id, keyword=None):
    data = {
        'chat_id': chat_id,
        'user_id': user_id,
        'keyword': keyword,
        'generate_list': True
    }
    result = contact_brain('generate', data)
    return result


def record(update, context):
    message = update.message

    chat_id = message.chat_id
    user_id = message.from_user.id
    text = message.text
    if message.reply_to_message and message.reply_to_message.from_user.id == self_id:
        say(update, context)

    send = False
    if chat_id in botCache.recorded_db:
        botCache.recorded_db[chat_id].append(text)
        if len(botCache.recorded_db[chat_id]) > send_records:
            send = True
    else:
        botCache.recorded_db[chat_id] = [text]

    if send:
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'text_list': botCache.recorded_db[chat_id],
        }
        response = contact_brain('record', data)
        botCache.recorded_db[chat_id] = []
        return response
    else:
        return True


def stat(update, context):
    return update.message.reply_text('数据统计功能正在开发中。', quote=False)
