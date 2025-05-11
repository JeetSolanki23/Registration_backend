# ./config/development.py

from .default import Config
import os

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URL')
        