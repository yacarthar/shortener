""" Token model
"""

from .base import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(40), nullable=False, index=True)
    ttype = db.Column(db.String(10), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    token = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, ttype, token, user_id, created_at):
        self.jti = jti
        self.ttype = ttype
        self.token = token
        self.user_id = user_id
        self.created_at = created_at


    @staticmethod
    def find_by_jti(jti):
        return Token.query.filter_by(jti=jti).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    # def json(self):
    #     return {
    #         "name": self.name,
    #         "email": self.email,
    #         "id": self.public_id,
    #     }