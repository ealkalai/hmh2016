from flask import Flask, request, Response, render_template, redirect, url_for, send_file, json
from flask.ext.qrcode import QRcode
import json
import random

import cStringIO, qrcode
import pprint
import uuid
from datetime import datetime

application = Flask(__name__)
QRcode(application)

pending_stuff = dict()

#from app.models import User

# Website/Service Backend entry points
#======================================


@application.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@application.route("/qrcode", methods=['GET', 'POST'])
def qr_page():
    text = '{"text": "Login to Mijn ING","extra_parameters": {}}'
    data = ing_create_challenge(json.loads(text))
    #data = ing_create_challenge({"text":"Sign in at website","extra_vars":{}})
    d = json.loads(data.get_data())
    pprint.pprint(d)
    return render_template('data.html',d=d,uuid=d['uuid'])

@application.route("/loggedin", methods=['GET', 'POST'])
def logged_in():
    return render_template('logged_in.html')

@application.route("/response", methods=['GET'])
def get_response():
    rv = request.args.get('uuid')
    pprint.pprint(rv)
    if rv in pending_stuff:
        return '{"url": "http://google.com"}'
    else:
        return 'not yet'

@application.route("/callback", methods=['GET'])
def handle_callback(data):
    pprint.pprint(pending_stuff)
    pending_stuff[data['uuid']] = data
    return Response(status=200)


# ING Backend entry points
#=========================

@application.route("/response", methods=['POST'])
def post_response():
    #verify device/pin
    data = request.get_json()
    pprint.pprint(data)
    handle_callback(data)
    return Response(json.dumps(data), status=200, mimetype='application/json')

def ing_create_challenge(data_in):
    pprint.pprint(data_in)
    #random_something = "123"
    #date = str(2016)
    date = str(datetime.now())
    #random_something = str(uuid.uuid4())
    random_something = str(random.randint(0,100))
    data_out = {"text" : data_in['text'], "date" : date, "uuid" : random_something, "extra_parameters" : data_in['extra_parameters']}
    pprint.pprint(data_out)
    return Response(json.dumps(data_out), status=200, mimetype='application/json')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)