import binascii
import base64
import time
import os
import pymysql
import config as config

connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


def read_file_data(filepath):
    """
    Takes file
    Reads timestamp from metadata and data within
    encodes data to base64
    stores data to DB
    returns timestamp
    :param: file from os
    :return: JSON object - dictionary of pins to {array of times, number of times}
    """
    create_time = time.gmtime(os.path.getmtime(filepath))
    with open(filepath, "r") as f:
        # metadata = f.read(512)
        # b64data = binascii.b2a_base64(f.read())
        data_binary = f.read()
        # b64data = binascii.b2a_base64(data)

    b64data = base64.b64encode(data_binary)
    print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", create_time))
    # print(data)
    print(b64data)
    print(b64data.decode('ascii'))

    # TODO: find pin

    # TODO: save to db

    return data_binary


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
