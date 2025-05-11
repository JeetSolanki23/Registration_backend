# ./config/production.py

from .default import Config
import os

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')