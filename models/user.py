""" User model
"""

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from .base import db
from libs.tools import cheap_uuid


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=cheap_uuid)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(250))
    tokens = db.relationship("Token", cascade="all, delete, delete-orphan")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.filter_by(public_id=user_id).first()

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "name": self.name,
            "email": self.email,
            "id": self.public_id,
        }
