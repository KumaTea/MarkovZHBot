import sys
import gzip
from pyrogram import Client

app = Client('me')
target = int(input('Chat ID: '))

history_file = 'history.gz'
end_text = input('End text: ')


if __name__ == '__main__':
    with app:
        history = []

        with gzip.open(history_file, 'rb') as f:
            old_history = f.read().decode('utf-8').split('\n')

        i = 0
        for message in app.iter_history(target):  # noqa
            if message.text:
                if message.text == end_text:
                    break
                history.append(message.text)
                i += 1
                sys.stdout.write('\rGetting: {}'.format(i))
        history.extend([j[:-1] for j in old_history])
        with gzip.open(history_file, 'wb') as f:
            f.write('\n'.join(history).encode('utf-8'))
