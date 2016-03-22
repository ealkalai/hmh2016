from flask import Flask, request, Response, render_template, redirect, url_for, send_file, json
from flask.ext.qrcode import QRcode
import json

import cStringIO, qrcode
import pprint

application = Flask(__name__)
QRcode(application)

#from app.models import User

# Website/Service Backend entry points
#======================================


@application.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@application.route("/qrcode", methods=['GET', 'POST'])
def thanks():
    response = ing_create_challenge()
    data = response.get_data()
    return render_template('data.html', d=data)

@application.route("/response", methods=['GET'])
def get_response():
    #verify device/pin
    #do callback
    return 200

@application.route("/callback", methods=['GET'])
def handle_callback():
    return Response(status=200)


# ING Backend entry points
#=========================

@application.route("/response", methods=['POST'])
def post_response():
    #verify device/pin
    data = request.get_json()
    pprint.pprint(data)
    handle_callback()
    return Response(json.dumps(data), status=200, mimetype='application/json')

def ing_create_challenge():
    data = {"url" : "http://google.com", "date" : 2016, "uuid" : 123}
    return Response(json.dumps(data), status=200, mimetype='application/json')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)