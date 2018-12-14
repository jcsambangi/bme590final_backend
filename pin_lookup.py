import pymysql
try:
    import config as config
except:
    import fakeConfig as config

connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


def pin(serial_num):
    """Returns pin associated with input serial number in database

    :param serial_num: int serial number
    :returns: pin if available, FileNotFoundError otherwise
    """
    q = "SELECT pin FROM serial_pin WHERE serial = {}".format(serial_num)
    try:
        with connection.cursor() as cursor:
            cursor.execute(q)
            result = cursor.fetchone()
            return result["pin"]
    except Exception as e:
        raise FileNotFoundError
