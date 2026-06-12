from app import db
from flask_login import UserMixin

# User table
class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role     = db.Column(db.String(10), nullable=False)  # 'admin' or 'student'

# Question table
class Question(db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    text   = db.Column(db.String(500), nullable=False)
    opt_a  = db.Column(db.String(200), nullable=False)
    opt_b  = db.Column(db.String(200), nullable=False)
    opt_c  = db.Column(db.String(200), nullable=False)
    opt_d  = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(1),   nullable=False)  # 'a','b','c','d'

# Result table
class Result(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score   = db.Column(db.Integer, nullable=False)
    total   = db.Column(db.Integer, nullable=False)
    user    = db.relationship('User', backref='results')