# passenger_wsgi.py
#
# Enable the application contained within this directory for Passenger
# More info:
# http://kb.apisnetworks.com/cgi-passenger/passenger-application-layout/

import sqlite3
from flask import (Flask, Response, render_template, request, session, g, url_for, abort, redirect, flash)
from contextlib import closing
from danielsenhwong import *

#####
# CONFIG
#####
# Set up the application
application = Flask(__name__)

# Database configuration in separate file
application.config.from_pyfile('/home/danielsenhwong/project_secrets/danielsenhwong_dev_db.cnf', silent=True)

#####
# DATABASE
#####
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

#####
# ROUTING
#####
# Application routes
@application.route('/')
def index():
    cur = g.db.execute('select title, description from projects order by id desc')
    projects = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('index.html', projects=projects)

def show_projects():
    cur = g.db.execute('select title, description from projects order by id desc')
    projects = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('index.html', projects=projects)

@application.route('/add_project', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != application.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != application.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_projects'))
    return render_template('login.html', error=error)

@application.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('show_projects'))
if __name__ == "__main__":
	application.run()
