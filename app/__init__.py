from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.qrcode import QRcode

app = Flask(__name__)
QRcode(app)

# #Create an instance of SQLAclhemy
# db = SQLAlchemy(app)
#
# login_manager = LoginManager()
# login_manager.init_app(app)
#
# from app import models