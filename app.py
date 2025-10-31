from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create database if not exists
def init_db():
    conn = sqlite3.connect('billing.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS billing (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        utr TEXT,
                        amount REAL,
                        date_time TEXT
                    )''')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('billing.db')
    rows = conn.execute("SELECT * FROM billing ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    utr = request.form['utr']
    amount = request.form['amount']
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('billing.db')
    conn.execute("INSERT INTO billing (name, utr, amount, date_time) VALUES (?, ?, ?, ?)", 
                 (name, utr, amount, date_time))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    print("✅ Flask Billing App started — open http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=10000)

