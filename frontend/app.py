# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import os
import json
from db_helper import *
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, Blueprint, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app, jsonify

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database/hackrice.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


#####################

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


        #####################

        # Session
        # user -> user_email


#####################
@app.route("/home", methods=["GET"])
def home():
    return render_template("homepage.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    error = None
    """POST Method"""
    if request.method == 'POST':
        user_email = request.form.get('useremail', None)
        password = request.form.get('password', None)
        re_password = request.form.get('re_password', None)
        first_name = request.form.get('firstname', None)
        last_name = request.form.get('lastname', None)

        if user_email is None or password is None or re_password is None or first_name is None or last_name is None:
            return render_template("error.html", info='Incomplete Information')
        if password != re_password:
            return render_template("error.html", info='Password Not Match')

        db = get_db()
        current_id = query_db(db, 'SELECT id FROM patient ORDER BY id DESC LIMIT 1', one=True)[0]
        args = (current_id + 1, user_email, password, first_name, last_name)
        crud_db(db, 'INSERT INTO patient VALUES (?,?,?,?,?)', args)
        return redirect(url_for('signup'))

    """GET Method"""
    if 'user' in session:
        print session['user']

    return render_template("signup.html", error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        user_email = request.form.get('useremail')
        password = request.form.get('password')

        if user_email is None or password is None:
            return render_template("error.html", info="Incomplete Input")
        query_result = query_db(get_db(), 'SELECT * FROM patient WHERE useremail = ? and password = ?',
                                (user_email, password), one=True)
        if query_result is None:
            return render_template("error.html", info="Incorrect Username or PassWord")
        else:
            session['user'] = user_email
            return redirect(url_for('calendar'))

    return render_template('login.html')


@app.route('/calendar')
def calendar():
    events = {'title': 'Click for Google',
              'start': 'new Date(y, m, 28)',
              'end': 'new Date(y, m, 29)',
              'url': 'http://google.com/'
              }

    return render_template('calendar.html', events=events)


@app.route('/_get_events')
def get_events():
    events = [{'title': 'Click for Google',
               'url': 'http://google.com/'
               },
              {'title': 'Click for Facebook',
               'url': 'http://facebook.com/'
               }]
    return jsonify(events)


if __name__ == '__main__':
    app.run()
