from flask import Flask, request, jsonify, abort
import pymysql
import config as config
import json
import datetime
from python_http_client import exceptions

app = Flask(__name__)
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


# @app.route('/test')
# def add_data():
#     try:
#         # with connection.cursor() as cursor:
#         #     print("connecting")
#         #     # Create a new record
#         #     sql = "INSERT INTO dashr VALUES (9037, 'ASDLJGWGAD', '2018-12-02 15:23:19')"
#         #     cursor.execute(sql)
#         #
#         # # connection is not autocommit by default. So you must commit to save
#         # # your changes.
#         # connection.commit()
#
#         with connection.cursor() as cursor:
#             print("fetching data")
#             # Read a single record
#             sql = "SELECT * FROM dashr"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             print(result)
#             return "good?"
#     except Exception as e:
#         return str(e)


@app.route('/api/dashr/<pin>', methods=['GET'])
def get_dasher_data(pin):
    """
    pin: pin number to get data for
    OPTIONAL PARAMETERS:
    start_date: earliest day of range, inclusive
    end_date: most recent day of range, inclusive
    :return:
    """
    q = "SELECT timestamp, data FROM dashr WHERE pin = {}".format(pin)
    # print(request.args['start_date'])
    if 'start_date' in request.args:
        q = q + " AND timestamp > {}".format(request.args['start_date'])
    if 'end_date' in request.args:
        q = q + " AND timestamp < {}".format(request.args['end_date'])
    print(q)
    try:
        with connection.cursor() as cursor:
            cursor.execute(q)
            result = cursor.fetchall()
            return jsonify(result)
    except Exception as e:
        return str(e)


@app.route('/api/dashr', methods=['POST'])
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
    all_data = request.get_json()
    data_dict = json.load(all_data)
    print(data_dict)
    q = "INSERT INTO dashr VALUES"
    for pin in data_dict:
        for file in data_dict[pin]:
            val = "({},{},{}),".format(data_dict[pin], file['data'], file['timestamp'])
            q = q + val
    q = q[:-1]
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(q)
        connection.commit()
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()

