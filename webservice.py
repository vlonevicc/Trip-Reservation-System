import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '1234'


def get_db_connection():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(base_dir, "final_project_files", "reservations.db")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn



#cost matrix
def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]


#routes
@app.route('/')
def index():
    return redirect(url_for('home'))


#home menu
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        option = request.form.get('option')

        if option == "reserve":
            return redirect(url_for('reservations'))

        elif option == "admin":
            return redirect(url_for('admin'))

    return render_template('home.html')


#admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        admin = conn.execute(
            "SELECT * FROM admins WHERE username = ? AND password = ?", 
            (username, password)
        ).fetchone()
        conn.close()

        if admin:
            return "Admin login successful! (Dashboard goes here)"
        else:
            error = "Invalid username or password."

    return render_template('admin.html', error=error)


#make reservation
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    message = None

    if request.method == 'POST':
        first = request.form["first_name"]
        last = request.form["last_name"]
        row = int(request.form["seat_row"])
        col = int(request.form["seat_col"])

        full_name = f"{first} {last}"

        #generate a simple eTicket code
        e_ticket = f"{first[0]}{last[0]}TICKET{row}{col}"

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber) VALUES (?, ?, ?, ?)",
            (full_name, row, col, e_ticket)
        )
        conn.commit()
        conn.close()

        message = f"Reservation successful! Your ticket code is: {e_ticket}"

    return render_template('reservations.html', message=message)


app.run(port=5003)