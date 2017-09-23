import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
    render_template, flash

app = Flask(__name__)  # create the application instance :)
app.secret_key = os.urandom(24)


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/login')
def login():
    return render_template("login.html");


if __name__ == '__main__':
    app.run()
