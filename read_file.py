import binascii
import base64
import time
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
    # read_file_data("..\..\..\Downloads\L0.BIN", 9307)
    read_numpy("..\..\..\Downloads\L0.BIN")


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
    ctr = 0
    with open(filepath, "rb") as f:
        # metadata = f.read(512)
        # b64data = binascii.b2a_base64(f.read())
        data_binary = f.read()
        # b64data = binascii.b2a_base64(data)
    # with open(filepath, "rb") as f:
    #     byte = f.read(1)
    #     while byte != "" and ctr < 100:
    #         # Do stuff with byte.
    #         byte = f.read(1)
    #         print(byte, end='', flush=True)
    #         ctr = ctr + 1

    b64data = base64.b64encode(data_binary)
    # print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", create_time))
    print("B64: ")
    print(b64data)
    decoded = base64.decodebytes(b64data)
    print(decoded)
    print(len(decoded))
    print("".join(["{:08b}".format(x) for x in decoded]))

    # TODO: save to db

    return create_time


def read_numpy(path):
    print(numpy.fromfile(path, dtype="uint8"))
    return ""


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


if __name__ == '__main__':
    main()
