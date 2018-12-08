import binascii
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
    with open(filepath, "rb") as f:
        # metadata = f.read(512)
        b64data = binascii.b2a_base64(f.read())

    print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", create_time))
    print(b64data)
    return create_time, b64data


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
