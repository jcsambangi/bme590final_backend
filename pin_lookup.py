import pymysql
import config as config

connection = pymysql.connect(host=config.mysql['host'],
                             user=config.mysql['user'],
                             password=config.mysql['password'],
                             db=config.mysql['db'],
                             cursorclass=pymysql.cursors.DictCursor)


def pin(serial_num):
    q = "SELECT pin FROM serial_pin WHERE serial = {}".format(serial_num)
    try:
        with connection.cursor() as cursor:
            cursor.execute(q)
            result = cursor.fetchall()
            return result
    except Exception as e:
        return str(e)
    return "ok"
