import re
import gzip
import jieba
import lzma as xz
from tqdm import tqdm


url_regex = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9]+\.[^\s]{2,}'

max_message_count = 10000


def skip_message(text):
    # commands
    if text.startswith('/'):
        return True

    # contains url
    if re.search(url_regex, text):
        return True

    if len(text) < 5 or len(text) > 20:
        return True

    return False


if __name__ == '__main__':
    history = []

    with gzip.open('history.gz', 'rb') as f:
        old_history = f.read().decode('utf-8').split()

    for message in tqdm(old_history):
        if skip_message(message):
            continue
        history.append(' '.join(jieba.lcut(message)))

    history = history[:max_message_count]
    with xz.open('history_cut.xz', 'wb') as f:
        f.write('\n'.join(history).encode('utf-8'))
    with open('history_cut.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(history))
