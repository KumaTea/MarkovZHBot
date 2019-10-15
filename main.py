from flask import Flask, request as flaskreq
from msgType import msg_type
from starting import starting


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = flaskreq.json
    # print(data)
    resp = msg_type(data)
    return '', 200


# If run on local machine:
starting()
if __name__ == '__main__':
    app.run(host='localhost', port=10569, debug=False)
