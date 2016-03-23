from flask import Flask, request, Response, render_template, redirect, url_for, send_file, json
from flask.ext.qrcode import QRcode
import json
import random

import cStringIO, qrcode
import pprint
import uuid

application = Flask(__name__)
QRcode(application)

pending_stuff = dict()

#from app.models import User

# Website/Service Backend entry points
#======================================


@application.route("/", methods=['GET'])
def login():
    return render_template('login.html')

@application.route("/qrcode", methods=['GET'])
def qr_page():
    text = '{"text": "Login to Mijn ING","extra_parameters": {}}'
    data = ing_create_challenge(json.loads(text))
    d = data.get_data()
    return render_template('data.html',d=d)

@application.route("/loggedin", methods=['GET', 'POST'])
def logged_in():
    return render_template('logged_in.html')

@application.route("/response", methods=['GET'])
def get_response():
    if "123" in pending_stuff:
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

def ing_create_challenge():
    random_something = "123"
    #random_something = str(uuid.uuid4())
    data = {"url" : "http://google.com", "date" : 2016, "uuid" : random_something}
    return Response(json.dumps(data), status=200, mimetype='application/json')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)