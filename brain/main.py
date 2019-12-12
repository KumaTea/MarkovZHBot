import logging
from starting import starting
from flask import Flask, request as flask_req
from brainSession import brain_token
from mdGenerate import generate
from mdRecord import record
from diskIO import write_msg

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
starting()


@app.route('/', methods=['GET'])
def main():
    return 'Brain of @MarkovZHBot', 200


@app.route('/write', methods=['GET'])
def write():
    msg_status = write_msg()
    # stat_status = write_stat()
    return f'Writing message: {msg_status}', 200


@app.route('/generate', methods=['GET', 'POST'])
def process_generate():
    received_token = flask_req.args.get('token', None) or flask_req.form.get('token', None)
    if received_token == brain_token:
        command = flask_req.args.get('command', None) or flask_req.form.get('command', None)
        if command == 'generate':
            data = flask_req.args.get('data', None) or flask_req.form.get('data', None)
            if data:
                resp = generate(data)
                return resp, 200
            else:
                return 'No data', 404
        else:
            return 'Wrong entry point', 404
    else:
        return 'Invalid token', 403


@app.route('/record', methods=['GET', 'POST'])
def process_record():
    received_token = flask_req.args.get('token', None) or flask_req.form.get('token', None)
    if received_token == brain_token:
        command = flask_req.args.get('command', None) or flask_req.form.get('command', None)
        if command == 'record':
            data = flask_req.args.get('data', None) or flask_req.form.get('data', None)
            if data:
                resp = record(data)
                return resp, 200
            else:
                return 'No data', 404
        else:
            return 'Wrong entry point', 404
    else:
        return 'Invalid token', 403


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=10569, debug=False)
