import binascii
import base64
import time
from datetime import datetime
import os
import pymysql
import numpy
import config as config


connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


def main():
    # read_file_data("..\..\..\Downloads\L0.BIN", 9037)
    read_file_data("test.txt", 9307)
    # read_numpy("..\..\..\Downloads\L0.BIN")


def read_file_data(filepath, pin):
    """
    Takes file and pin
    Reads timestamp from metadata and data within
    encodes data to base64
    stores data to DB
    returns timestamp
    :param: file from os
    :return: timestamp of create_time
    """
    create_time = time.gmtime(os.path.getmtime(filepath))
    create_datetime = datetime.fromtimestamp(time.mktime(create_time))
    # Open file and read data
    with open(filepath, "rb") as f:
        data_raw = f.read()
    # Encode to base64
    b64data = base64.b64encode(data_raw)
    # Save to DB
    try:
        with connection.cursor() as cursor:
            print("CONNECTED TO DB")
            cursor.execute("SELECT MAX(timestamp) FROM dashr WHERE pin = {}"
                           .format(pin))
            max_time = cursor.fetchone()["MAX(timestamp)"]
            if max_time is None:
                max_time = datetime.min
    except Exception as e:
        return str(e)
    try:
        with connection.cursor() as cursor:
            if create_datetime > max_time:
                # ASSUMING clocks don't reset and/or go backwards
                print("time is greater - save data to db")
                cursor.execute("INSERT INTO dashr VALUES ({}, '{}', '{}')".
                               format(pin, b64data.decode("utf-8"),
                                      create_datetime))
            else:
                # data had previously been inserted into DB
                print("time is less - don't save: " + create_datetime)
                return ""
            # Commit changes (insert) to DB
            connection.commit()
            return time.strftime("%Y-%m-%d %H:%M:%S",
                                 create_time)
    except Exception as e:
        print(str(e))
        return str(e)


# def read_numpy(path):
#     data_arr = numpy.fromfile(path, dtype="uint8")
#     # print(data_arr[100])
#     for i in range(0, 700):
#         print(data_arr[i], end=" ")
#     print(len(data_arr))
#     return ""


    # q = "SELECT timestamp, data FROM dashr WHERE pin = {}".format(pin)
    # # print(request.args['start_date'])
    # if 'start_date' in request.args:
    #     q = q + " AND timestamp > {}".format(request.args['start_date'])
    # if 'end_date' in request.args:
    #     q = q + " AND timestamp < {}".format(request.args['end_date'])
    # print(q)
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute(q)
    #         result = cursor.fetchall()
    #         return jsonify(result)
    # except Exception as e:
    #     return str(e)

# DECODING:
    # decoded = base64.b64decode(b64data)
    # decoded = base64.decodebytes(decoded64)
    # print(decoded)
    # print(len(decoded))
    # print("".join(["{:08b}".format(x) for x in decoded]))

if __name__ == '__main__':
    main()
