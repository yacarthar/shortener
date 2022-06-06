""" app
"""

# import json
import logging

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from config import Config
from models import db, Url
from libs import cheap_hash


def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        # db.drop_all()
        db.create_all()

    return app

app = create_app()

@app.route('/')
def home():
    return jsonify({"data": "hello world."})

@app.route('/files', methods=["POST"])
def file_handler():
    file = request.files.get("file1")
    return jsonify({"input_data": file.filename})

@app.route('/shorten', methods=["POST"])
def shortener():
    url = request.json.get("url")
    new_url = Url(
        url=url,
        short_url=cheap_hash(url)
    )
    db.session.add(new_url)
    db.session.commit()

    return jsonify({"input_data": url})

@app.route('/u/<short_url>', methods=["GET"])
def get_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    return jsonify({"full_url": url.url})


if __name__ == "__main__":
    app.run(port=5000)