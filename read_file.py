import binascii
import base64
import time
from datetime import datetime
import os
import pymysql
import os
import numpy
import pathlib
try:
    import config as config
except:
    import fakeConfig as config


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
    for_harvest = {}
    for pin in checked:
        if pin in DASHRlut:
            for_harvest[pin] = DASHRlut[pin]
    return for_harvest


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
        curr_logpins = log["logpins"]
        curr_logpins.append(pin)
        log["logpins"] = curr_logpins
        ret = read_DASHR(pin, chosen[pin], now)
        count = 0
        currNotes = []
        for thing in ret:
            if thing == 1:
                count += 1
            elif type(thing) == str:
                currNotes.append(thing)
        curr_lognotes = log["notes"]
        curr_lognotes.append(currNotes)
        log["notes"] = curr_lognotes
        curr_num_files = log["numfiles"]
        curr_num_files.append(count)
        log["numfiles"] = curr_num_files
    return log


def read_DASHR(pin, location, now):
    """Downloads data fom a single DASHR.

    :param pin: pin of chosen DASHR
    :param location: drive path of chosen DASHR
    :returns: array of binaries describing whether each file was read
    """
    ret = []
    for path, subdirs, files in os.walk(location):
        for name in files:
            if name[-3:] == "BIN":
                filepath = pathlib.PurePath(path, name).as_posix()
                ret.append(read_file_data(filepath, pin, now))
    return ret


def read_file_data(filepath, pin, time_session):
    """Reads file and stores data in database based on creation date.
    Encodes data to base64 before storing. Returns 0, 1, or a note.
    
    :param filepath: path on local machine where file can be found
    :param pin: DASHR from which data is being read
    :param time_session: datetime of the session - ie when files are harvested
    :return: 1 if saved, 0 if not, str(error) if error
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
            cursor.execute("SELECT MAX(dashr_create_time) FROM "
                           "dashr WHERE pin = {}"
                           .format(pin))
            max_time = cursor.fetchone()["MAX(dashr_create_time)"]
            if max_time is None:
                max_time = datetime.min
    except Exception as e:
        print(str(e))
        return str(e)
    try:
        with connection.cursor() as cursor:
            if create_datetime > max_time:
                # Assuming DASHR RTCs don't reset and/or go backwards
                print("time is greater - save data to db")
                cursor.execute("INSERT INTO dashr VALUES ({},'{}','{}','{}')".
                               format(pin, b64data.decode("utf-8"),
                                      create_datetime, time_session))
            else:
                # if data past this time has previously been inserted into DB
                print("don't save")
                print("create time: " + datetime.strftime(create_datetime,
                      "%Y-%m-%d %H:%M:%S"))
                print("max time: " + datetime.strftime(max_time,
                      "%Y-%m-%d %H:%M:%S"))
                return 0
            # Commit changes (insert) to DB
            connection.commit()
            return 1
    except Exception as e:
        print(str(e))
        return str(e)


# Possible future features:
# DECODING:
    # decoded = base64.b64decode(b64data)
    # decoded = base64.decodebytes(decoded64)
    # print(decoded)
    # print(len(decoded))
    # print("".join(["{:08b}".format(x) for x in decoded]))

if __name__ == '__main__':
    main()
