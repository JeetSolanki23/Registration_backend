# ./app/api/errors/__init__.py
from flask import Blueprint


errors = Blueprint('errors', __name__)
from .routes import *
