# passenger_wsgi.py
#
# Enable the application contained within this directory for Passenger
# More info:
# http://kb.apisnetworks.com/cgi-passenger/passenger-application-layout/

import sqlite3
from flask import (Flask, Response, render_template, request, session, g, url_for, abort, redirect, flash)
from contextlib import closing

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
application = Flask(__name__)
application.config.from_pyfile('/home/danielsenhwong/project_secrets/danielsenhwong_dev_db.cnf', silent=True)

# Database-related functions
# Connect to the database
def connect_db():
    return sqlite3.connect(application.config['DATABASE'])

# Initialize the database
def init_db():
    with closing(connect_db()) as db:
        with application.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Connect to the database before a request is made
@application.before_request
def before_request():
    g.db = connect_db()

# Close database connection if an exception is raised
@application.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Application routes
@application.route("/")
#def hello():
#	return "Hello World!"

def index():
    cur = g.db.execute('select title, description from projects order by id desc')
    projects = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('index.html', projects=projects)

if __name__ == "__main__":
	application.run()
