import requests
import sqlite3
from flask import Flask, render_template, url_for, redirect, request, abort

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '1234'


def get_db_connection():
    conn = sqlite3.connect('reservations.db')

    conn.row_factory = sqlite3.Row

    return conn

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    # add code here
    return render_template('home.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # add code here
    return render_template('admin.html')

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    # add code here
    return render_template('reservations.html')



app.run(port=5003)