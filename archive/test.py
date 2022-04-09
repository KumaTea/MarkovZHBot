import markovify
from tqdm import tqdm, trange


if __name__ == '__main__':
    test_result = []

    with open('history_cut.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    new_text = []
    failed = 0
    for i in tqdm(text.split('\n')):
        try:
            model = markovify.Text(i)
            new_text.append(i)
        except:
            failed += 1
            continue
    print('Failed:', failed)

    loop = trange(int(len(new_text) / 100) + 1)
    for i in loop:
        model = markovify.Text(
            '\n'.join(
                new_text[:(i+1)*100]
            )
        ).compile()
        success_times = 0
        for j in range(100):
            result = model.make_sentence()
            if result:
                success_times += 1
        loop.set_description('{}:{}'.format(i+1, success_times))
        test_result.append('{}:{}'.format(i+1, success_times))

    with open('test_result.txt', 'w') as f:
        f.write('\n'.join(test_result))
