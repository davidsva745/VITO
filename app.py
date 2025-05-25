from flask import Flask, render_template, request
import socket
import datetime
app = Flask(__name__, static_folder='static', template_folder='templates')


def log_visit(endpoint):
    with open("access.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {request.remote_addr} - {endpoint}\n")

@app.route('/')
def index():
    log_visit("Homepage")
    return render_template('vito.html')  # hlavní stránka

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

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n📱 Otevři na mobilu: http://{local_ip}:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
