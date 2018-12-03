from flask import Flask, request, jsonify, abort
import pymysql
import databaseconfig as dbconfig
import datetime
from python_http_client import exceptions

app = Flask(__name__)
connection = pymysql.connect(host=dbconfig.mysql['host'],
                             user=dbconfig.mysql['user'],
                             password=dbconfig.mysql['password'],
                             db=dbconfig.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)
print(dbconfig.mysql['host'])
@app.route('/')
def index():
    try:
        with connection.cursor() as cursor:
            print("connected to db")
    except Exception as e:
        return str(e)
    return 'Testing'


@app.route('/test')
def add_data():
    try:
        # with connection.cursor() as cursor:
        #     print("connecting")
        #     # Create a new record
        #     sql = "INSERT INTO dashr VALUES (9037, 'ASDLJGWGAD', '2018-12-02 15:23:19')"
        #     cursor.execute(sql)
        #
        # # connection is not autocommit by default. So you must commit to save
        # # your changes.
        # connection.commit()

        with connection.cursor() as cursor:
            print("fetching data")
            # Read a single record
            sql = "SELECT * FROM dashr"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return "good?"
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()

