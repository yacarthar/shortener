""" Url model
"""

from datetime import datetime
from .base import db


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    short_url = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    click = db.Column(db.Integer, default=0)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "full_url": self.url,
            "short_url": self.short_url,
            "click": self.click,
        }
