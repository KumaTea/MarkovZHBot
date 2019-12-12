import logging
from flask import Flask, request as flask_req
from botSession import markov, dp
from telegram import Update
from starting import starting
from register import register_handlers


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

register_handlers()
starting()


@app.route('/', methods=['POST'])
def main():
    update = Update.de_json(flask_req.json, markov)
    dp.process_update(update)
    return '', 200


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=10569, debug=False)
