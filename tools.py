import os
from botSession import bot


def get_chat_admin(chat_id):
    try:
        with open(f'admin/{chat_id}.txt', 'r') as f:
            admin = list(map(int, f.readlines()))
    except FileNotFoundError:
        admin = bot.query(chat_id).group_admin()
        with open(f'admin/{chat_id}.txt', 'w') as f:
            for i in admin:
                f.write(str(i) + '\n')
    return admin


def del_files(path):
    files = []
    for i in os.listdir(path):
        if os.path.isfile(f'{path}/{i}'):
            files.append(f'{path}/{i}')
    if files:
        for i in files:
            os.remove(i)
            print(f'[INFO] Deleted {i}')
