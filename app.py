from flask import Flask, render_template, request
import socket
import datetime
from collections import Counter
from flask import jsonify, request
app = Flask(__name__, static_folder='static', template_folder='templates')


def log_visit(endpoint):
    with open("access.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {request.remote_addr} - {endpoint}\n")

@app.route('/')
def index():
    log_visit("Homepage")
    return render_template('vito.html')
@app.route('/sluzby')
def sluzby():
    log_visit("Služby")
    return render_template('sluzby.html')

@app.route('/kontakt')
def kontakt():
    log_visit("Kontakt")
    return render_template('kontakt.html')


@app.route('/fotogalerie')
def fotogalerie():
    log_visit("Fotogalerie")
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

    # FullCalendar expects ISO 8601 (YYYY-MM-DD)
    events = [{"title": f"Návštěv: {count}", "start": str(date)} for date, count in date_counter.items()]
    return jsonify(events)

@app.route("/admin")
def admin_dashboard():
    key = request.args.get("key")
    if key != "VITO123":
        abort(403)
    return render_template("admin.html")

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n📱 Otevři na mobilu: http://{local_ip}:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
