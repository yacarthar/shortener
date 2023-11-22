""" app
"""

# import json
import logging
import os

from flask import Flask

from blueprints.dmz import dmz
from blueprints.user import user
from blueprints.shortener import shortener

from config import app_config
from models import db


def create_app(config="dev"):
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)
    app.config.from_object(app_config.get(config))

    with app.app_context():
        db.init_app(app)
        # db.drop_all()
        db.create_all()

    app.register_blueprint(dmz)
    app.register_blueprint(user)
    app.register_blueprint(shortener)
    return app


app = create_app(os.getenv("CONFIG_NAME"))


if __name__ == "__main__":
    app.run(port=5000)
