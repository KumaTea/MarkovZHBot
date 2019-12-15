import json
import logging
from starting import starting
from flask import Flask, request as flask_req
from brainTools import post_legality
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


@app.route('/generate', methods=['POST'])
def process_generate():
    description, code = post_legality(flask_req, 'generate')
    if code > 299:
        return description, code
    else:
        return generate(json.loads(flask_req.form.get('data'))), 200


@app.route('/record', methods=['POST'])
def process_record():
    description, code = post_legality(flask_req, 'record')
    if code > 299:
        return description, code
    else:
        return record(json.loads(flask_req.form.get('data'))), 200


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=10569, debug=False)
