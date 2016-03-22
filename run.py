from flask import Flask, request, render_template, redirect, url_for
from app import app, db

import string
import random

application = Flask(__name__)

from app.models import User


@application.route("/thanks2buyer")
def thanks1():
    print(rand(800))
    return render_template('thanks2buyer.html', name="Julian")

@application.route("/thanks", methods=['GET', 'POST'])
def thanks():
    name            = request.form['name']
    email           = request.form['email']
    background      = request.form['background']
    expected_grad   = request.form['grad_date']
    comment         = request.form['comment']
    interest        = request.form['interest']

    user=User(name,email,background,expected_grad,comment,interest)
    db.session.add(user)
    db.session.commit()

    return render_template('thanks.html', name=name)

@application.route("/", methods=['GET', 'POST'])
def login():
    print(rand(800))
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return render_template('login.html', username=request.form['username'], callback=request.args.get('callback'))
        else:
            error = 'Invalid username/password.'
    return render_template('login.html', error=error, callback=request.args.get('callback'))

def valid_login(username, password):
    user = User.query.filter_by(username=username).first()

    if user == None:
        return False

    if user.password == password:
        return True
    else:
        return False

@application.route("/add_contract", methods=['GET', 'POST'])
def add_contract():
    if request.method == 'POST':
        domain  = request.form['domain']
        name    = request.form['name']
        email   = request.form['email']

        contract = Contract(domain, name, email)
        db.session.add(contract)
        db.session.commit()

        return render_template('add_contract.html', domain=domain, name=name, email=email)
    else:
        return render_template('add_contract.html')

@application.route("/update_contract", methods=['GET', 'POST'])
def update_contract():
    if request.method == 'POST':
        domain = request.form['domain']
        name = request.form['name']
        email = request.form['email']
        price = request.form['price']

        contract = Contract.query.filter_by(domain = domain).first()

        contract.seller_name  = name
        contract.seller_email = email
        contract.price        = price

        db.session.commit()

        return render_template('update_contract.html', name=name, email=email, price=price)
    else:
        return render_template('update_contract.html')

@application.route("/registrar1")
def registrar1():
    print(rand(900))
    return render_template('registrar1.html')

@application.route("/listDomains")
def listDomains():
    print(rand(900))
    return render_template('listDomains.html', domains=["google.com", "ing.nl", "ing.com", "youtube.com"])

@application.route("/search", methods=['POST'])
def search():
    print(rand(1000))
    domains = ["google.com", "ing.nl", "ing.com", "youtube.com"]
    return render_template('listDomains.html', domain="ing.com")

@application.route("/commonapi/me")
def me():
    return "{id: 3, name: Julian}"

@application.route("/registrar1/token/<token>")
def setToken(token):
    print(rand(600))
    #should do a get to /commonapi/me
    return redirect(url_for('thanks1'))

@application.route("/expense_dashboard/")
def excess():
    return '''  <script type="text/javascript">
                    var token = window.location.href.split("access_token=")[1].split("&state=")[0]; 
                    window.location = "http://localhost:5000/registrar1/token/" + token;
                </script> '''

def rand(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)