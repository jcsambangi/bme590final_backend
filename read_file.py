import binascii
import base64
import time
from datetime import datetime
import os
import pymysql
import os
import numpy
import pathlib
import config as config
from datetime import datetime


connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


def main():
    # read_file_data("..\..\..\Downloads\L0.BIN", 9037)
    read_file_data("test.txt", 9307, datetime.now())
    # read_numpy("..\..\..\Downloads\L0.BIN")
    

def narrow(checked, DASHRlut):
    """Returns dictionary mapping selected DASHRs to local drives.

    :param checked: array of integer pins
    :param DASHRlut: dictionary mapping of all locally detected DASHRs
    :returns: dictionary mapping only user-selected DASHRs
    """
    forHarvest = {}
    for pin in checked:
        if pin in DASHRlut:
            forHarvest[pin] = DASHRlut[pin]
    return forHarvest


def read_selected(chosen):
    """Downloads data from all selected DASHRs.

    :param chosen: dictionary mapping selected DASHRs to local drives
    :returns: log as dictionary
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    log = {}
    log["logpins"] = []
    log["numfiles"] = []
    log["notes"] = []
    print(chosen)
    for pin in chosen:
        print(pin)
        print(chosen[pin])
        curr_logpins = log["logpins"]
        curr_logpins.append(pin)
        log["logpins"] = curr_logpins
        ret = read_DASHR(pin, chosen[pin], now)
        count = 0
        currNotes = []
        print("________________________")
        for thing in ret:
            print(thing)
            if thing == 1:
                count += 1
            elif type(thing) == str:
                currNotes.append(thing)
            print(count)
        curr_lognotes = log["notes"]
        curr_lognotes.append(currNotes)
        log["notes"] = curr_lognotes
        curr_numFiles = log["numfiles"]
        curr_numFiles.append(count)
        log["numfiles"] = curr_numFiles
    print(log)
    return log


def read_DASHR(pin, location, now):
    """Downloads data fom a single DASHR.

    :param pin: pin of chosen DASHR
    :param location: drive path of chosen DASHR
    :returns: array of timestamps of files read
    """
    ret = []
    print("IN READ_DASHR")
    for path, subdirs, files in os.walk(location):
        print(path)
        for name in files:
            print(name)
            print(name[-3:])
            if name[-3:] == "BIN":
                print("3")
                filepath = pathlib.PurePath(path, name).as_posix()
                print(filepath)
                ret.append(read_file_data(filepath, pin, now))
    print(ret)
    return ret


def read_file_data(filepath, pin, time_session):
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
            cursor.execute("SELECT MAX(dashr_create_time) FROM dashr WHERE pin = {}"
                           .format(pin))
            max_time = cursor.fetchone()["MAX(dashr_create_time)"]
            print(max_time)
            if max_time is None:
                max_time = datetime.min
            print(max_time)
    except Exception as e:
        return str(e)
    try:
        with connection.cursor() as cursor:
            if create_datetime > max_time:
                # ASSUMING clocks don't reset and/or go backwards
                print("time is greater - save data to db")
                cursor.execute("INSERT INTO dashr VALUES ({}, '{}', '{}', '{}')".
                               format(pin, b64data.decode("utf-8"),
                                      create_datetime, time_session))
            else:
                # data had previously been inserted into DB
                print("time is less - don't save: " + datetime.strftime(
                    create_datetime, "%Y-%m-%d %H:%M:%S"))
                return 0
            # Commit changes (insert) to DB
            connection.commit()
            return 1
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
