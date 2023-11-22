""" auth tools
"""

from datetime import datetime, timedelta
from uuid import uuid4
from functools import wraps

from flask import request, jsonify, current_app
import jwt
from jwt.exceptions import DecodeError
from jwt import ExpiredSignatureError

from models import User, Token
from libs.custom_errors import *


def create_token(user, ttype="access"):
    """https://pyjwt.readthedocs.io/en/stable/usage.html"""
    jti = str(uuid4())
    now = datetime.utcnow()
    if ttype == "access":
        expire = now + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    else:
        expire = now + current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    payload = {
        "type": ttype,
        "iat": now,
        "nbf": now,
        "exp": expire,
        "sub": user.public_id,
        "jti": jti,
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"])
    token_db = Token(
        jti=jti,
        ttype=ttype,
        token=token.decode("utf-8"),
        user_id=user.id,
        created_at=now,
    )
    token_db.save()
    return token.decode("utf-8")


def get_jwt():
    token = request.headers.get("Authorization")
    if not token:
        raise TokenMissingError(token)
    token = token.partition("Bearer ")[-1]
    # tbd, try catch
    try:
        token_decode = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        return token_decode
    except ExpiredSignatureError:
        raise TokenExpiredError(token)
    except DecodeError:
        raise TokenDecodeError(token)


def validate_token(token, validate_type="access"):
    if token["type"] != validate_type:
        raise TokenTypeError(token, validate_type)

    token_db = Token.find_by_jti(token.get("jti"))
    if token_db.revoked:
        raise TokenRevokedError(token)


def token_required(f):
    @wraps(f)
    def _token_required(*args, **kwargs):
        try:
            token = get_jwt()
            validate_token(token)
        except Exception as e:
            return jsonify(message=e.message), 401
        user_id = token.get("sub")
        if not user_id:
            current_user = None
        else:
            current_user = User.find_by_id(user_id)

        return f(current_user, *args, **kwargs)

    return _token_required


def token_required_for_logout(f):
    @wraps(f)
    def _token_required_for_logout(*args, **kwargs):
        try:
            token = get_jwt()
            validate_token(token)
        except Exception as e:
            return jsonify(message=e.message)
        return f(token, *args, **kwargs)

    return _token_required_for_logout


def token_required_for_refresh(f):
    @wraps(f)
    def _token_required_for_refresh(*args, **kwargs):
        try:
            token = get_jwt()
            validate_token(token, validate_type="refresh")
        except Exception as e:
            return jsonify(message=e.message)
        return f(token, *args, **kwargs)

    return _token_required_for_refresh
