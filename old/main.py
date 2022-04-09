from telegram import Update
from starting import starting
from botSession import markov, dp
from diskIO import write_msg, write_stat
from flask import Flask, request as flask_req


app = Flask(__name__)

starting()


@app.route('/', methods=['POST'])
def main():
    update = Update.de_json(flask_req.json, markov)
    dp.process_update(update)
    return '', 200


@app.route('/', methods=['GET'])
def status():
    return '@MarkovZHBot is online.', 200


@app.route('/write', methods=['GET'])
def write():
    msg_status = write_msg()
    stat_status = write_stat()
    return f'Writing message: {msg_status}\nWriting stat: {stat_status}', 200


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=10569, debug=False)
