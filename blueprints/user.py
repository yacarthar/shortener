""" user handlers
"""

from datetime import datetime, timedelta


from flask import Blueprint, request, make_response, jsonify, current_app

from libs.auth import create_token, token_required
from models import db, User

user = Blueprint('user', __name__)


@user.route('/signup', methods =['POST'])
def signup():
    form = request.form
    name = form.get('name')
    email = form.get('email')
    password = form.get('password')
  
    if User.find_by_email(email=email):
        return make_response('User exists', 202)

    user = User(name, email, password)
    user.save()
    return make_response(jsonify(user.json()), 201)


@user.route('/login', methods =['POST'])
def login():
    form = request.form
    if not form or not form.get('email') or not form.get('password'):
        return make_response("Invalid Form", 401)
  
    user = User.find_by_email(email=form.get('email'))  
    if not user:
        return make_response("Invalid User", 401)
    if not user.validate_password(form.get('password')):
        return make_response("Invalid Password", 403)

    access_token = create_token(user)
    refresh_token = create_token(user, ttype="refresh")

    return make_response(
        jsonify(access_token=access_token,
            refresh_token=refresh_token
        ),
        201
    )


@user.route('/user', methods =['GET'])
@token_required
def protected(current_user):
    if not current_user:
        return jsonify(message="Authenticate failed"), 401
    return jsonify(user=current_user.json()), 200