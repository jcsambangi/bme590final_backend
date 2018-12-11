import pymysql
import os
import config as config
from datetime import datetime

connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


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
    for pin in chosen:
        log["logpins"] = log["logpins"].append(pin)
        ret = read_DASHR(pin, chosen.pin, now)
        count = 0
        currNotes = []
        for thing in ret:
            if thing == 1:
                count += 1
            elif type(thing) == str:
                currNotes.append(thing)
        logForThisPin["notes"] = log["notes"].append(currNotes)
        logForThisPin["numfiles"] = log["numfiles"].append(count)
    return log


def read_DASHR(pin, location, now):
    """Downloads data fom a single DASHR.

    :param pin: pin of chosen DASHR
    :param location: drive path of chosen DASHR
    :returns: array of timestamps of files read
    """
    ret = []
    for path, subdirs, files in os.walk(location):
        for name in files:
            if name[-3:] == ".BIN":
                filepath = pathlib.PurePath(path,name).as_posix()
                ret.append(read_file_data(filepath, pin, now))
    return stamps


def read_file(file, pin):
    """
    Takes file
    Reads timestamp from metadata and data within
    encodes data to base64
    stores data to DB
    returns timestamp
    :param: file from os
    :return: JSON object - dictionary of pins to {array of times, number of times}
    """
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
