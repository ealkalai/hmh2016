from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

#Create an Instance of Flask
app = Flask(__name__)
#Include config from config.py
app.config.from_object('config')
app.secret_key = 'some_secret'



#Create an instance of SQLAclhemy
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app import models