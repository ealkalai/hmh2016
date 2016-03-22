from flask import Flask, request, render_template, redirect, url_for, send_file
from flask.ext.qrcode import QRcode
import json
import random

import cStringIO, qrcode
import json

application = Flask(__name__)
QRcode(application)

#from app.models import User

@application.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@application.route("/qrcode", methods=['GET', 'POST'])
def qr_page():
    data = ing_create_challenge()
    return render_template('data.html',d=data)

@application.route("/loggedin", methods=['GET', 'POST'])
def logged_in():
    return render_template('logged_in.html')

@application.route("/response", methods=['POST'])
def post_response():
    #verify device/pin
    #do callback
    return True

@application.route("/response", methods=['GET'])
def get_response():
    if random.randint(0,100) < 10:
        return '{"url": "http://google.com"}'

def ing_create_challenge():
    return '{url: "http://google.com", date: 2016, uuid: 123}'

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)