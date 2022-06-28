from flask import Blueprint, jsonify, request

from libs.tools import cheap_hash
from models import db, Url

shortener = Blueprint('shorten', __name__)


@shortener.route('/shorten', methods=["POST"])
def encode():
    url = request.json.get("url")
    new_url = Url(
        url=url,
        short_url=cheap_hash(url)
    )
    db.session.add(new_url)
    db.session.commit()

    return jsonify(
        {
            "input_data": url,
            "shorten_url": new_url.short_url
        }
    )

@shortener.route('/s/<short_url>', methods=["GET"])
def decode(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    return jsonify({"full_url": url.url})
