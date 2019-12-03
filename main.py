from flask import Flask, request as flask_req
from msgType import msg_type
from starting import starting
import logging
from diskIO import write_msg, write_stat


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

starting()


@app.route('/', methods=['POST'])
def main():
    data = flask_req.json
    # print(data)
    resp = msg_type(data)
    return '', 200


@app.route('/write', methods=['GET'])
def write():
    msg_status = write_msg()
    stat_status = write_stat()
    return f'Writing message: {msg_status}\nWriting stat: {stat_status}', 200


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=10569, debug=False)
