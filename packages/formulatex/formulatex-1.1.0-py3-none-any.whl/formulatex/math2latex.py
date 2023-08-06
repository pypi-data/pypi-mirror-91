import pyperclip
from flask import Flask
from flask import request
from flask import render_template
from gevent import pywsgi
import socket
import requests
import json
import os, sys

APP_ID = APP_KEY = ''
ENABLE_HISTORY = True
TEMPLATE_FOLDER = os.path.join(sys.exec_prefix, "formulatex_src/templates")
STATIC_FOLDER = os.path.join(sys.exec_prefix, "formulatex_src/statics")
HISTORY_FILE = os.path.join(sys.exec_prefix, "formulatex_src/formulas.txt")
DATAFILE_FILE = os.path.join(sys.exec_prefix, "formulatex_src/data.json")

app = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER,
    static_url_path="/static"
)


def ipconfig():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def formulas():
    global ENABLE_HISTORY
    if not ENABLE_HISTORY or not os.path.exists(HISTORY_FILE):
        return ''
    with open(HISTORY_FILE, "r") as reader:
        _formulas = [line.strip().replace('\\', '\\\\').replace('\\n', '\n').split('\t') for line in reader.readlines()]
    return _formulas


@app.route('/copy', methods=["POST"])
def copy():
    pyperclip.copy(request.form.get("latex"))
    return "0"


@app.route('/', methods=['GET'])
def home():
    return render_template("hand_input.html", formulas=formulas())


@app.route('/submit', methods=['POST'])
def submit():
    global APP_ID, APP_KEY
    image_uri = request.form.get("image_uri")
    r = requests.post("https://api.mathpix.com/v3/text",
        data=json.dumps({'src': image_uri}),
        headers={
          "app_id": APP_ID,
          "app_key": APP_KEY,
          "Content-type": "application/json"
        })
    result = json.loads(r.text)
    pyperclip.copy(result['latex_styled'])
    log = "{}\t{}".format(result['confidence_rate'], result["latex_styled"].replace('\n', '\\n'))
    with open(HISTORY_FILE, "a") as writer:
        writer.write(log + "\n")
    app.logger.info(log)
    return r.text


@app.route('/paste', methods=['GET'])
def paste():
    return render_template("paste.html", formulas=formulas())


@app.route('/usage', methods=['POST'])
def usage():
    global APP_ID, APP_KEY
    url = "https://api.mathpix.com/api/ocr/user-data?perPage=2000&fromDate=2020-09-19&page=1"
    headers = {
        "authority": "api.mathpix.com",
        "authorization": "Bearer bbfMOyAzbW0AFR3skhi9G4G4isqO2h2hm5_fkDOU47PPfqyHkE5S8xqZetx-_NN8xvRCvvbGkEPaCfKRqh_ZdA",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    }
    data = {
        "app_key": APP_KEY,
    }
    res = requests.post(url, data=data, headers=headers)
    _usage = len(json.loads(res.text)['list'])
    return str(_usage)


def check_port(port, ip='127.0.0.1'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        print(port, 'NOT available')
    except:
        print(port, 'available')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='app_id')
    parser.add_argument('--key', help='app_key')
    parser.add_argument('--ip', help='ip address bind with server')
    parser.add_argument('--port', help='port bind with server', type=int, default=8000)
    parser.add_argument('--file', help='file storing id and key', default=DATAFILE_FILE)
    parser.add_argument('--store', help='store id and key in default file', action="store_true")
    parser.add_argument('--check-port', help='check whether a port is available', type=int)
    parser.add_argument('--check-ip', help='get ip address', action="store_true")
    parser.add_argument('--no-history', help='disable history loading', action="store_true")
    args = parser.parse_args().__dict__
    if args['check_port']:
        check_port(args['check_port'])
    elif args['check_ip']:
        print(ipconfig())
    elif args['store']:
        data = {"app_id": input("APP_ID: "), "app_key": input("APP_KEY: ")}
        with open(DATAFILE_FILE, "w") as writer:
            writer.write(json.dumps(data))
        print("Successfully stored data in", DATAFILE_FILE)
    else:
        global APP_ID, APP_KEY, ENABLE_HISTORY
        if not args['ip']:
            args['ip'] = ipconfig()
        if not APP_ID and args['id']:
            APP_ID = args['id']
        if not APP_KEY and args['key']:
            APP_KEY = args['key']
        if not APP_ID or not APP_KEY:
            if os.path.exists(DATAFILE_FILE):
                with open(args['file'], 'r') as reader:
                    data = json.loads(reader.read())
                    if not APP_ID:
                        APP_ID = data['app_id']
                    if not APP_KEY:
                        APP_KEY = data['app_key']
        assert APP_ID, 'app_id required'
        assert APP_KEY, 'app_key required'
        ENABLE_HISTORY = not args['no_history']
        server = pywsgi.WSGIServer((args['ip'], args['port']), app)
        print("FormuLaTeX serve at http://{}:{}/ (Press CTRL+C to quit)".format(args['ip'], args['port']))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('FormuLaTeX stop serving')


if __name__ == '__main__':
    main()
