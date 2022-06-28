""" auth tools
"""

from datetime import datetime
from uuid import uuid4
from functools import wraps

from flask import request, jsonify, current_app
import jwt

from models import User, Token

def create_token(user, ttype="access"):
    """ https://pyjwt.readthedocs.io/en/stable/usage.html
    """
    jti = str(uuid4())
    now = datetime.utcnow()
    payload = {
        "type": ttype,
        "iat": now,
        "nbf": now,
        "exp": now + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        "sub": user.public_id,
        "jti": jti,
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"])
    token_db = Token(
        jti=jti,
        ttype=ttype,
        token=token,
        user_id=user.id,
        created_at=now
    )
    token_db.save()
    return token

def get_jwt():
    token = request.headers.get("Authorization")
    if not token:
        return {}
    token = token.partition("Bearer ")[-1]
    return jwt.decode(
        token,
        current_app.config['SECRET_KEY'],
        algorithms=["HS256"]
    )

def get_jwt_user_id():
    token = get_jwt()
    return token.get("sub")

def token_required(f):
    @wraps(f)
    def _token_required(*args, **kwargs):
        user_id = get_jwt_user_id()
        if not user_id:
            current_user = None
        else:
            current_user = User.find_by_id(user_id)

        return  f(current_user, *args, **kwargs)
  
    return _token_required