""" configs
"""

import os

from dotenv import load_dotenv
from constants import ENV_FILE

load_dotenv(ENV_FILE)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP=False