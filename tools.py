from botSession import bot


def get_chat_admin(chat_id):
    try:
        with open(f'admin{chat_id}.txt', 'r') as f:
            admin = list(map(int, f.readlines()))
    except FileNotFoundError:
        admin = bot.query(chat_id).group_admin()
        with open(f'admin{chat_id}.txt', 'w') as f:
            for i in admin:
                f.write(str(i) + '\n')
    return admin
