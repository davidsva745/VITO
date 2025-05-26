from flask import Flask, render_template, request, jsonify, abort
import socket
import datetime
import time
import sqlite3
from collections import Counter
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
DB_PATH = "data.db"

# Inicializace databáze
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()

# Logování návštěvy
def log_visit():
    now = time.time()
    ip = request.remote_addr
    cutoff = datetime.datetime.now() - datetime.timedelta(minutes=10)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp FROM visits WHERE ip = ? ORDER BY timestamp DESC LIMIT 1", (ip,))
        row = c.fetchone()

        if not row or datetime.datetime.fromisoformat(row[0]) < cutoff:
            c.execute("INSERT INTO visits (ip, timestamp) VALUES (?, ?)", (ip, datetime.datetime.now().isoformat()))
            conn.commit()

@app.route('/')
def index():
    log_visit()
    return render_template('index.html')

@app.route('/sluzby')
def sluzby():
    log_visit()
    return render_template('sluzby.html')

@app.route('/kontakt')
def kontakt():
    log_visit()
    return render_template('kontakt.html')

@app.route('/fotogalerie')
def fotogalerie():
    log_visit()
    return render_template('fotogalerie.html')

@app.route('/admin/stats-daily.json')
def stats_daily():
    if request.args.get("key") != "VITO123":
        return jsonify({"error": "unauthorized"}), 403

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT DATE(timestamp) FROM visits")
        dates = c.fetchall()

    counter = Counter(date[0] for date in dates)
    events = [{"title": f"Návštěv: {count}", "start": date} for date, count in counter.items()]
    return jsonify(events)

@app.route('/admin')
def admin_dashboard():
    if request.args.get("key") != "VITO123":
        abort(403)
    return render_template('admin.html')

if __name__ == '__main__':
    init_db()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n📱 Otevři na mobilu: http://{local_ip}:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
