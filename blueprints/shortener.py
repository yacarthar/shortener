from flask import Blueprint, jsonify, request, redirect, make_response

from libs.tools import cheap_hash
from libs.auth import token_required
from models import db, Url

shortener = Blueprint("shorten", __name__)


@shortener.route("/shorten", methods=["POST"])
@token_required
def encode(current_user):
    print(type(current_user))
    url = request.json.get("url")
    new_url = Url(url=url, short_url=cheap_hash(url), user_id=current_user.id)
    new_url.save()
    return jsonify({"full_url": url, "short_url": new_url.short_url})


@shortener.route("/s/<short_url>", methods=["GET"])
def get_full_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first()

    # log & monitor click
    url.click += 1
    url.save()

    return redirect(url.url)


@shortener.route("/s/<short_url>/info", methods=["GET"])
@token_required
def get_url_info(current_user, short_url):
    url = Url.query.filter_by(short_url=short_url, user_id=current_user.id).first()
    if not url:
        return make_response(jsonify(message="forbidden url"), 403)
    return jsonify(url.json())
