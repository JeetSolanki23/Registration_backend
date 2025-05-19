# ./app/api/main/__init__.py
from flask import Blueprint

payment = Blueprint('payment', __name__)

from . import routes
