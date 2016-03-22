from flask import render_template, jsonify, request, flash, redirect, url_for, abort, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from sqlalchemy.orm.exc import NoResultFound
from app import app, db

from app.models import User
from datetime import timedelta

app.permanent_session_lifetime = timedelta(seconds=30*60)

class AuthUser(UserMixin):
    username = ""
    name = ""

    def __init__(self, username, password):
        self.id = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


    @classmethod
    def get(cls,id):
        username = ""
        if (isinstance(id, str) or isinstance(id, unicode)):
            username = id
        else:
            username = id()

        user = None
        if (id == "admin"):
            user = AuthUser(id,"xxxx")
            user.username = id
            user.name = "Administrator"


        else:
            try:
                object= db.session.query(User).filter_by(username=id).one()
                user = AuthUser(object.username,object.password)
                user.username = id

            except NoResultFound, e:
                print 'NoResultFound - reason "%s"' % str(e)
                return None

            return user





@app.errorhandler(401)
def page_not_found(e):
    return render_template('/errors/401.html'), 404


@login_manager.user_loader
def load_user(userid):
    return AuthUser.get(userid)

def load_user_from_request(request):
    try:
        username = "UnKnown"
        if (request is str):
            username = request
        else:
            username = request.form['username']
            password = request.form['password']
        print "load_user_from_request [" + username + "]"

        user_entry = AuthUser.get(username)


        if (user_entry is not None):
            if password == user_entry.password:
                print "User password OK..."
                return user_entry
            else:
                print "User password wrong"
    except Exception, e:
        print e
    return None


@login_manager.unauthorized_handler
def unauthorized():
    # print "unauthorized"
    return render_template('login.html')




@app.context_processor
def add_session_config():
    """Add current_app.permanent_session_lifetime converted to milliseconds
    to context. The config variable PERMANENT_SESSION_LIFETIME is not
    used because it could be either a timedelta object or an integer
    representing seconds.
    """
    return {
        'PERMANENT_SESSION_LIFETIME_MS': (
            app.permanent_session_lifetime.seconds * 1000),
    }