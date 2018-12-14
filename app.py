from flask import Flask, request, jsonify, abort
import pymysql
import config as config
from flask_cors import CORS
import json
import datetime
from python_http_client import exceptions
from DASHR import findSNs, compCrawl

app = Flask(__name__)
CORS(app)
connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    """Test route to indicate whether server is up.

    :returns: "Server is up" if up
    """
    try:
        with connection.cursor() as cursor:
            print("connected to db")
    except Exception as e:
        return str(e), 400
    return 'Server is up', 200


@app.route('/api/dashr/find_pins', methods=['GET'])
def find_pins():
    """GET route through which front end can learn of connected DASHRs

    :returns: JSON dictionary with array of pins
    """
    dict = findSNs(compCrawl())
    arr = []
    for SN in dict:
        arr.append(SN)
    print({"pins": arr})
    return jsonify({"pins": arr}), 200


@app.route('/api/dashr/upload', methods=['POST'])
def upload():
    """POST route through which downloading sequence is triggered

    :param checked: which pins were selected by user
    :returns: log of arrays with pins, files downloaded counts, and notes
    """
    DASHRlut = findSNs(compCrawl())
    checked = request.get_json()
    from read_file import read_selected, narrow
    chosen = narrow(checked, DASHRlut)
    log = read_selected(chosen)
    return jsonify(log), 200


# delete files from usb when done - hypothetical route for future
@app.route('/api/dashr/delete_from_drive')
def delete():
    return "files deleted"


if __name__ == '__main__':
    app.run('localhost')
