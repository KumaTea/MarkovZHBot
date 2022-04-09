from session import markov
from init import initialize
from register import register_handlers


initialize()

register_handlers()


if __name__ == '__main__':
    markov.run()  # app.run(main())
