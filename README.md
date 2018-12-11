# bme590final_backend
Back end functionality for the HIE sensor management tool.
## Setting up the Database
* create a config.py file (this is in the gitignore and will not be added to git)
* in the file, add the following code:
  * mysql = {'host': [db host],
         'user': [user],
         'password': [password],
         'db': [name of db]}
* in your local mysql database (same one named above), create the following tables:
  * CREATE TABLE dashr (pin INTEGER, data LONGTEXT, dashr_create_time DATETIME, session_time DATETIME, PRIMARY KEY(pin, dashr_create_time))
  * CREATE TABLE serial_pin (serial INTEGER PRIMARY KEY, pin INTEGER)
* seed the serial_pin table with the following two values, taken from the two dashrs that we have
  * INSERT INTO serial_pin VALUES (261122326, 435), (261791206, 9307)

