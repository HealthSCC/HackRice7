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

        table, table_id = ('patient', 'pid') if request.form.get('check-doctor') is None else ('doctor', 'did')
        db = get_db()
        values = query_db(db, 'SELECT {} FROM {} ORDER BY {} DESC LIMIT 1'.format(table_id, table, table_id), one=True)
        current_id = 1
        if values is not None:
            print values
            current_id = values[0] + 1
        args = (current_id, user_email, password, first_name, last_name)
        crud_db(db, 'INSERT INTO {} VALUES (?,?,?,?,?)'.format(table), args)

        return redirect(url_for('home'))

    """GET Method"""
    if 'user' in session:
        print session['user']

    return render_template("signup.html", error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('useremail')
        password = request.form.get('password')

        if email is None or password is None:
            return render_template("error.html", info="Incomplete Input")
        table, email_name = ('patient', 'useremail') if request.form.get('check-doctor') is None else (
            'doctor', 'doctoremail')

        print email, password
        query_result = query_db(get_db(), 'SELECT * FROM {} WHERE {} = ? and password = ?'.format(table, email_name),
                                (email, password), one=True)
        print query_result
        if query_result is None:
            return render_template("error.html", info="Incorrect Username or PassWord")
        else:
            session['id'], session['useremail'] = int(query_result[0]), email
            session['firstname'], session['lastname'] = str(query_result[3]), str(query_result[4])
            session['type'] = table
            return redirect(url_for('calendar'))

    return render_template('login.html')


@app.route('/calendar')
def calendar():
    if 'type' in session:
        if session['type'] == 'patient':
            args = (session['id'],)
            values = query_db(get_db(),
                              'select advise from suggestion where pid = ? and julianday(worstdate)-julianday(\'now\') < 5 order by bestdate limit 3',
                              args)
            descriptions = ""
            for i in range(0, len(values)):
                descriptions += ("* " + (str(values[i][0])) + " ")
            print descriptions
            return render_template('calendar_user.html', firstname=session['firstname'], lastname=session['lastname'],
                                   descriptions=descriptions)
        else:
            values = query_db(get_db(),
                              'select * from event')
            number_of_patient = len(values)
            patients = []
            for value in values:
                each_dict = {
                    'pid': int(value[0]),
                    'startdate': str(value[1])[5:],
                    'enddate': str(value[2])[5:],
                    'category': str(value[3]),
                    'description': str(value[5])
                }
                print each_dict
                patients.append(each_dict)
            return render_template('calendar_doctor.html', firstname=session['firstname'], lastname=session['lastname'],
                                   number_of_patient=number_of_patient,
                                   patients=patients)
    else:
        return render_template('error.html', firstname=None, lastname=None)


@app.route('/_insert_event', methods=['POST'])
def insert_event():
    if request.method == 'POST':
        category_select = request.form.get('category_select')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        time = request.form.get('time')
        args = (session['id'], start_date, end_date, category_select, time, description)
        crud_db(get_db(), 'INSERT INTO event VALUES (?,?,?,?,?,?)', args)
        return redirect(url_for('calendar'))
    else:
        return render_template("error.html")


@app.route('/_insert_suggestion', methods=['POST'])
def insert_suggestion():
    if request.method == 'POST' and session['type'] == 'doctor':
        print "yes"
        advise = request.form.get('advise', None)
        best_date = request.form.get('best_date', None)
        worst_date = request.form.get('worst_date', None)
        pid = request.form.get('pid', None)
        args = (pid, session['id'], best_date, worst_date, advise)
        crud_db(get_db(), 'INSERT INTO suggestion VALUES (?,?,?,?,?)', args)
        return redirect(url_for('calendar'))

    return render_template("error.html")


@app.route('/_get_events')
def get_events():
    if 'type' in session:
        events_return = []
        if session['type'] == 'patient':
            args = (session['id'],)
            events_query = query_db(get_db(), 'SELECT * FROM event WHERE pid = ?', args, one=False)
            for event in events_query:
                sy, sm, sd = str(event[1]).split("-")
                ey, em, ed = str(event[2]).split("-")
                each_dict = {
                    'title': str(event[5]),
                    'starty': sy,
                    'startm': sm,
                    'startd': sd,
                    'endy': ey,
                    'endm': em,
                    'endd': ed,
                    'time': int(event[4]),
                    'url': str(event[3]),
                }
                events_return.append(each_dict)
    return jsonify(events_return)


if __name__ == '__main__':
    app.run()
