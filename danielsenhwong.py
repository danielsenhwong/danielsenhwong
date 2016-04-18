# danielsenhwong.py
#
# Flask-driven Python application to serve a personal bio page

#####
# IMPORTS
#####
import sqlite3
from flask import (Flask, Response, render_template, request, session, g,       url_for, abort, redirect, flash)
from contextlib import closing

#####
# VARIABLES
#####
project_secret_path = '/home/danielsenhwong/project_secrets/danielsenhwong_secret.txt'
database_cnf_path = '/home/danielsenhwong/project_secrets/danielsenhwong_dev_db.cnf'

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

