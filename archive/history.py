import sys
from pyrogram import Client

app = Client('me')
target = -0

history_file = 'history.txt'


if __name__ == '__main__':
    with app:
        history = []
        i = 0
        for message in app.iter_history(target):
            if message.text:
                history.append(message.text)
                i += 1
                sys.stdout.write('\rGetting: {}'.format(i))
        with open(history_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(history))
