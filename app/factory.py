# ./app/factory.py
from flask import Flask
import os

from config import config
from .extensions import db, migrate, jwt, redis_client, cors, marshmallow
from .models import *
from .api import register_api
from .manage import register_commands

def initialize_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    redis_client.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": app.config['ALLOWED_ORIGINS'],
            "supports_credentials": True,
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    marshmallow.init_app(app)



def create_app(config_name=os.environ.get('FLASK_ENV','default')):
    app = Flask(__name__)
    
    if config_name not in config:
        raise ValueError(f"Invalid config name: '{config_name}'. Must be one of {list(config.keys())}")
    app.config.from_object(config[config_name])
    
    initialize_extensions(app)
    register_api(app)
    register_commands(app)
    
    
    return app