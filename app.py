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


@app.route('/api/dashr/find_pins')
def find_pins():
    dict = findSNs()
    arr = []
    for SN in dict:
        arr.append(SN)
    print({"pins": arr})
    return jsonify({"pins": arr})


@app.route('/api/dashr/upload', methods=['POST'])
def upload():
    print("UPLOADING")
    req = request.get_json()
    print(req)
    return "log"


# delete files from usb when done - do this last
@app.route('/api/dashr/delete_from_drive')
def delete():
    return "files deleted"


# @app.route('/api/dashr', methods=['POST'])
def post_dashr_data():
    """
    data in json form:
    [
    "PIN1": [
        {timestamp, encoded data}, {timestamp, encoded data}, ...
    ],
    "PIN2": [ {}, {}, ...],
    "PIN3": [], ...
    ]
    :return:
    """
    print("POSTING")
    data = request.json
    print(data)
    # data_dict = all_data.json
    # print(data_dict)
    q = "INSERT INTO dashr VALUES"
    for pin in data:
        print(pin)
        for file in data[pin]:
            print(file)
            val = "({},'{}','{}'),".format(pin, file['data'], file['timestamp'])
            q = q + val
    q = q[:-1]
    print(q)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(q)
        connection.commit()
        return "posted"
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run('localhost')

