# passenger_wsgi.py
#
# Enable the application contained within this directory for Passenger
# More info:
# http://kb.apisnetworks.com/cgi-passenger/passenger-application-layout/

import sqlite3
from flask import Flask, Response, render_template, request, session, g,
url_for, abort, redirect, flash
from danielsenhwong import *

# Tutorial/demo
#def application(environ, start_response):
#	start_response('200 OK', [('Content-Type', 'text/plain')])
#	v = sys.version_info
#	str = 'hello world from %d.%d.%d!\n' % (v.major, v.minor, v.micro)
#	return [bytes(str, 'UTF-8')]

# Configure database and connections
# Include the following in a separate file that will not be copied to github
#DATABASE = '/tmp/danielsenhwong.db'
#DEBUG = True
#SECRET_KEY =
#USERNAME = 
#PASSWORD = 

# Set up the application
dsw = Flask(__name__)
dsw.config.from_pyfile('/home/danielsenhwong/project_secrets/danielsenhwong_dev_db.cnf', silent=True)

# Connect to the database
def connect_db():
    return sqlite3.connect(dsw.config['DATABASE'])

# Application routes
@dsw.route("/")
#def hello():
#	return "Hello World!"

def index():
    return render_template('index.html')

if __name__ == "__main__":
	dsw.run()
