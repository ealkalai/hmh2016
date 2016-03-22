from app import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    extend_existing=True

    id_u            = db.Column(db.Integer, primary_key = True)
    name            = db.Column(db.String(200))
    email           = db.Column(db.String(200))
    background      = db.Column(db.String(200))
    expected_grad   = db.Column(db.String(200))
    comments        = db.Column(db.String(200))
    interest        = db.Column(db.String(500))


    def __init__(self, name, email, background, expected_grad, comments, interest):
        self.name           = name
        self.email          = email
        self.background     = background
        self.expected_grad  = expected_grad
        self.comments       = comments
        self.interest       = interest

    def __repr__(self):
        return "Username: %s" % self.name