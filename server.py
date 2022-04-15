#!/usr/bin/env python3
import os
from datetime import date, datetime
from flask import Flask, request
from script import Script


app = Flask(__name__)

SERVER_CONFIG = {'debug': True, 'host': '0.0.0.0', 'port': 9999}
DATA_DIR = './data'

    
@app.route('/<uid>/<name>', methods=['POST'])
def main(uid, name):
    service = Service(uid)
    data = request.get_data()
    response = service.get_data(data, name)
    return response


class Service:
    def __init__(self, uid):
        self._make_dir(uid)
        self.uid = uid

        
    def script_(self, file):
        project = Script(file, 'akes-project-4037cc052234.json', '1TkBDXHKLVHVmuilU2Iuak34kmjuQPKX40LhbReXc4DE', 1968705244)
        project.main___()

        
    def get_data(self, request_body, name):
        timestamp = date.today()
        with open(f'{DATA_DIR}/{self.uid}/{timestamp}_{name}', 'wb') as fd:
            fd.write(request_body)
            self.script_(fd)
        return {'success': True, 'status': 'body saved'}

    def _make_dir(self, uid):
        if not os.path.exists(f'{DATA_DIR}/{uid}'):
            os.mkdir(f'{DATA_DIR}/{uid}')


if __name__ == '__main__':
    app.run(**SERVER_CONFIG)
