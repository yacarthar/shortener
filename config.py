""" configs
"""

import os
from datetime import timedelta
from dotenv import load_dotenv
from constants import ENV_FILE

load_dotenv(ENV_FILE)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    CSRF_ENABLED = True

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP=False

    exp_secs = os.getenv("JWT_ACCESS_TOKEN_EXPIRES")
    if exp_secs and isinstance(exp_time, str):
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=exp_secs)
    else:
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


class DevelopmentConfig(Config):
    """Configurations for Development."""
    FLASK_ENV = os.getenv('FLASK_ENV')
    DEBUG = True
    CSRF_ENABLED = False


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI_TEST")
    DEBUG = True


class StagingConfig(DevelopmentConfig):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "stag": StagingConfig,
    "prod": ProductionConfig,
}