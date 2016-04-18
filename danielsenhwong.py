# danielsenhwong.py
#
# A Python app using the Flask framework to serve a simple database-driven bio page.

import os
import sqlite3
from flask import (Flask, Response, render_template, request, session, g, url_for, abort, redirect, flash)
from contextlib import closing

#####
# VARIABLES
#####
database_cnf_path = '/home/danielsenhwong/project_secrets/danielsenhwong_dev_db.cnf'

#####
# CONFIG
#####
# Set up the application
application = Flask(__name__)

# Database configuration in separate file
application.config.from_pyfile(database_cnf_path, silent=True)

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
# INTERNAL ROUTING - Modify internal URLs, e.g. url_for()
#####
# From https://gist.github.com/Ostrovski/f16779933ceee3a9d181
# Solve issue of static files not being refreshed
# Add a hash parameter to a URL for static content, e.g. CSS files
# Intercept url_for() calls and add the hash as 'h' parameter
@application.url_defaults
def hashed_url_for_static_file(endpoint, values):
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            if '.' in endpoint:  # has higher priority
                blueprint = endpoint.rsplit('.', 1)[0]
            else:
                blueprint = request.blueprint  # can be None too

            if blueprint:
                static_folder = application.blueprints[blueprint].static_folder
            else:
                static_folder = application.static_folder

            param_name = 'h'
            while param_name in values:
                param_name = '_' + param_name
            values[param_name] = static_file_hash(os.path.join(static_folder, filename))
            
def static_file_hash(filename):
  return int(os.stat(filename).st_mtime) # or app.config['last_build_timestamp'] or md5(filename) or etc...

#####
# ROUTING
#####
@application.route('/')
def index():
    data = g.db.execute('select title, description, url from projects order by id desc')
    projects = [dict(title=row[0], description=row[1], url=row[2]) for row in data.fetchall()]
    return render_template('index.html', projects=projects, page_title='Home')

@application.route('/projects')
def show_projects():
    data = g.db.execute('select title, description, url from projects order by id desc')
    projects = [dict(title=row[0], description=row[1], url=row[2]) for row in data.fetchall()]
    return render_template('show.html', projects=projects, page_title='Project List')

@application.route('/projects/add', methods=['POST'])
def add_project():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into projects (title, description, url) values (?, ?, ?)',
            [
                request.form['title'],
                request.form['description'],
                request.form['url']
            ])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_projects'))

@application.route('/login', methods=['GET', 'POST'])
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
    return render_template('login.html', error=error, page_title='Login')

@application.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('show_projects'))

#####
# RUN FLASK
#####
if __name__ == "__main__":
	application.run()
