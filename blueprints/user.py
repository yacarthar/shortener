""" user handlers
"""
from flask import Blueprint, request, make_response, jsonify

from libs.auth import (
    create_token,
    token_required,
    token_required_for_logout,
    token_required_for_refresh,
)
from models import User, Token

user = Blueprint("user", __name__)


@user.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if User.find_by_email(email=email):
        return make_response("User exists", 202)

    user = User(name, email, password)
    user.save()
    return make_response(jsonify(user.json()), 201)


@user.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return make_response("Invalid body", 401)

    user = User.find_by_email(email=data.get("email"))
    if not user:
        return make_response("Invalid User", 401)
    if not user.validate_password(data.get("password")):
        return make_response("Invalid Password", 403)

    access_token = create_token(user)
    refresh_token = create_token(user, ttype="refresh")

    return make_response(
        jsonify(
            access_token=access_token, refresh_token=refresh_token, user=user.json()
        ),
        201,
    )


@user.route("/user", methods=["GET"])
@token_required
def protected(current_user):
    return jsonify(user=current_user.json()), 200


@user.route("/logout", methods=["DELETE"])
@token_required_for_logout
def logout(token):
    token_db = Token.find_by_jti(token.get("jti"))
    token_db.revoke()
    return jsonify(message="token revoked")


@user.route("/auth/refresh", methods=["POST"])
@token_required_for_refresh
def refresh(token):
    user = User.find_by_id(user_id=token.get("sub"))
    access_token = create_token(user)
    refresh_token = create_token(user, ttype="refresh")
    return make_response(
        jsonify(
            access_token=access_token, refresh_token=refresh_token, user=user.json()
        ),
        201,
    )
