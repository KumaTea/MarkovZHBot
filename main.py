from flask import Flask, request as flaskreq
from msgType import msg_type
from starting import starting
import logging


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/', methods=['POST'])
def main():
    data = flaskreq.json
    # print(data)
    resp = msg_type(data)
    return '', 200


starting()

# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=10569, debug=False)
