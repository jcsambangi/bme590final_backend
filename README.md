# bme590final_backend
[![Build Status](https://travis-ci.org/jcsambangi/bme590final_backend.svg?branch=master)](https://travis-ci.org/jcsambangi/bme590final_backend)
Back end functionality for the HIE sensor management tool. Front end can be found [here](https://github.com/jcsambangi/bme590final).
v1.0.0 released 12/14/18 by Teresa Mao, Claire Niederriter, and Jaydeep Sambangi
## Overview
This repository holds a Flask app that runs on `localhost:5000` which communicates with the React front end to service its RESTful API requests. It also communicated with a local MySQL database, configured as described below. This server supports the following routes:
* GET `/`
* GET `/api/dashr/find_pins`
* POST `/api/dashr/upload`
However, the server is built to communicate only with the front end, with user input being controlled such that back end validation is unnecessary. Therefore, these routes should only be accessed through the above specified React front end. Before the software can be used at all, the below two steps should be carried out.
### Setting up the Database
* Download [MySQL Community Edition](https://dev.mysql.com/downloads/windows/installer/8.0.html).
* [Here](https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial-creating-a-model.html) is a helpful guide to navigate setting up the database. Schema for the tables that should live inside the local database are included in the Schema folder inside this repository, should the user want to shortcut the next two bullet points.
* In your local MySQL database, create the following tables - feel free to use the guide above with the variable names below, or directly use the code below:
  * `CREATE TABLE dashr (pin INTEGER, data LONGTEXT, dashr_create_time DATETIME, session_time DATETIME, PRIMARY KEY(pin, dashr_create_time))`
  * `CREATE TABLE serial_pin (serial INTEGER PRIMARY KEY, pin INTEGER)`
* Seed the `serial_pin` table with the following two values, taken from the two DASHRs used for testing:
  * `INSERT INTO serial_pin VALUES (261122326, 435), (261791206, 9307)`
* Next, create a `config.py` file in this respository (locally - this is in the .gitignore and will not be added to git).
* In the file, add the following code (square brackets indicate portions that should be replaced with user-specific information):
  * `mysql = {'host': [db host], 'user': [user], 'password': [password], 'db': [name of db]}`
### Spinning Up the Server
The back end server can be spun up locally by calling `FLASK_APP=app.py flask run` while inside the root of the repository.

