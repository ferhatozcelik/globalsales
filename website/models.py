from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Advert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    category = db.Column(db.String(200))
    description = db.Column(db.String(10000))
    add_user_id = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))
    first_name = db.Column(db.String(500))
    phone_number = db.Column(db.String(500))
    role = db.Column(db.String(500))