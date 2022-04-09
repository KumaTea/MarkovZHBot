import markovify


if __name__ == '__main__':
    new_text = []
    with open('history_cut.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    for i in text.splitlines():
        try:
            model = markovify.Text(i)
            new_text.append(i)
        except:
            continue
    with open('processed.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_text))

    with open('processed.txt', 'r', encoding='utf-8') as f:
        text = f.read()

        model = markovify.Text(
            '\n'.join(
                text.splitlines()[:int(input('How many lines? '))]
            )
        ).compile()
        for j in range(100):
            result = model.make_sentence()
            # result = model.make_short_sentence(20)
            if result and len(result) < 50:
                print(result.replace(' ', ''), '\n')
