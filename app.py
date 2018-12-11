from flask import Flask, request, jsonify, abort
import pymysql
import config as config
from flask_cors import CORS
import json
import datetime
from python_http_client import exceptions
from DASHR import findSNs

app = Flask(__name__)
CORS(app)
connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    try:
        with connection.cursor() as cursor:
            print("connected to db")
    except Exception as e:
        return str(e)
    return 'Server is up'


@app.route('/api/dashr/find_pins', methods=['GET'])
def find_pins():
    dict = findSNs()
    arr = []
    for SN in dict:
        arr.append(SN)
    print({"pins": arr})
    return jsonify({"pins": arr})


@app.route('/api/dashr/upload', methods=['POST'])
def upload():
    DASHRlut = findSNs()
    checked = request.get_json()
    from read_file import read_selected, narrow
    chosen = narrow(checked, DASHRlut)
    log = read_selected(chosen)
    return jsonify(log)


# delete files from usb when done - do this last
@app.route('/api/dashr/delete_from_drive')
def delete():
    return "files deleted"


if __name__ == '__main__':
    app.run('localhost')

