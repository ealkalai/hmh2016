from flask import Flask, request, Response, render_template, redirect, url_for, send_file, json
from flask.ext.qrcode import QRcode
import json
import random

import pprint
import uuid
from datetime import datetime

application = Flask(__name__)
QRcode(application)

pending_stuff = dict()

# Website/Service Backend entry points
#======================================


@application.route("/", methods=['GET'])
def login():
    return render_template('login.html')

@application.route("/qrcode", methods=['GET', 'POST'])
def qr_page():
    text = '{"text": "Login to Mijn ING", "something_generic" : ""}'
    data = ing_create_challenge(json.loads(text), "web")
    d = data.get_data()
    temp = json.loads(data.get_data())
    return render_template('data.html',d=d,uuid=temp['uuid'])\

@application.route("/atm", methods=['GET', 'POST'])
def atm_page():
    textTwenty = '{"text": "ING ATM", "something_generic" : "20"}'
    textFifty = '{"text": "ING ATM", "something_generic" : "50"}'
    dataTwenty = ing_create_challenge(json.loads(textTwenty), "atm")
    dataFifty = ing_create_challenge(json.loads(textFifty), "atm")
    tempTwenty = json.loads(dataTwenty.get_data())
    tempFifty = json.loads(dataFifty.get_data())
    dTwenty = dataTwenty.get_data()
    dFifty = dataFifty.get_data()
    return render_template('atm.html',dTwenty=dTwenty,dFifty=dFifty,uuidTwenty=tempTwenty['uuid'],uuidFifty=tempFifty['uuid'])

@application.route("/loggedin", methods=['GET', 'POST'])
def logged_in():
    rv = request.args.get('uuid')
    name = pending_stuff[rv]['user']
    device = pending_stuff[rv]['device']
    return render_template('logged_in.html',name=name, device=device)

@application.route("/moneywithdrawn", methods=['GET', 'POST'])
def money_withdrawn():
    rv = request.args.get('uuid')
    name = pending_stuff[rv]['user']
    amount = pending_stuff[rv]['something_generic']
    return render_template('moneywithdrawn.html',name=name, amount=amount)

@application.route("/response", methods=['GET'])
def get_response():
    rv = request.args.get('uuid')
    if rv in pending_stuff:
        return '{"url": "http://google.com"}'
    else:
        return 'not yet'

@application.route("/callback", methods=['GET'])
def handle_callback(data):
    pending_stuff[data['uuid']] = data
    return Response(status=200)


# ING Backend entry points
#=========================

@application.route("/response", methods=['POST'])
def post_response():
    #verify device/pin
    data = request.get_json()
    handle_callback(data)
    return Response(json.dumps(data), status=200, mimetype='application/json')

def ing_create_challenge(data_in, service):
    date = str(datetime.now())
    random_something = str(uuid.uuid4())
    data_out = {"text" : data_in['text'], "date" : date, "uuid" : random_something, "service_id": service, "something_generic" : data_in['something_generic']}
    return Response(json.dumps(data_out), status=200, mimetype='application/json')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)