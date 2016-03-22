from flask import Flask, request, render_template, redirect, url_for, send_file
from flask.ext.qrcode import QRcode

import cStringIO, qrcode

application = Flask(__name__)
QRcode(application)

#from app.models import User

@application.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@application.route("/qrcode", methods=['GET', 'POST'])
def thanks():
    img = "http://www.ing.com"
    return render_template('data.html',img=img)

@application.route("/response", methods=['POST'])
def post_response():
    #verify device/pin
    #do callback
    return 200

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)