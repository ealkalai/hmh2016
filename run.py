from flask import Flask, request, render_template, redirect, url_for

#import qrcode

application = Flask(__name__)

#from app.models import User

@application.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@application.route("/challenge", methods=['GET', 'POST'])
def thanks():
    url = "http://www.google.com"
    return render_template('data.html', url=url)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)