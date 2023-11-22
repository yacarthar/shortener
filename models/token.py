""" Token model
"""

from .base import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(40), nullable=False, index=True)
    ttype = db.Column(db.String(10), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    token = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def find_by_jti(jti):
        return Token.query.filter_by(jti=jti).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def revoke(self):
        self.revoked = True
        self.save()
