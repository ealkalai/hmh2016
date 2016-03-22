from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)

# #Create an instance of SQLAclhemy
# db = SQLAlchemy(app)
#
# login_manager = LoginManager()
# login_manager.init_app(app)
#
# from app import models