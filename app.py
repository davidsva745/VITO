from flask import Flask, render_template, request, jsonify, abort
import socket
import datetime
import time
from collections import Counter

app = Flask(__name__, static_folder='static', template_folder='templates')

last_visits = {}  # IP → timestamp

def log_visit():
    now = time.time()
    ip = request.remote_addr

    # Loguj pouze pokud uplynulo víc než 10 minut od poslední návštěvy z IP
    if ip not in last_visits or now - last_visits[ip] > 600:
        last_visits[ip] = now
        with open("access.log", "a") as f:
            f.write(f"{datetime.datetime.now()} - {ip}\n")

@app.route('/')
def index():
    log_visit()
    return render_template('vito.html')

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

    date_counter = Counter()
    with open("access.log") as f:
        for line in f:
            try:
                date_str = line.split(" - ")[0].split()[0]
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                date_counter[date_obj.date()] += 1
            except:
                continue

    events = [{"title": f"Návštěv: {count}", "start": str(date)} for date, count in date_counter.items()]
    return jsonify(events)

@app.route('/admin')
def admin_dashboard():
    if request.args.get("key") != "VITO123":
        abort(403)
    return render_template('admin.html')

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n📱 Otevři na mobilu: http://{local_ip}:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
