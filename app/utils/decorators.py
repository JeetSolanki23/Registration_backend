from functools import wraps
from flask import request, jsonify
from jsonschema import validate, ValidationError
from .errors import APIError
from .validators import validate_email, validate_phone, validate_dob
import logging

logger = logging.getLogger(__name__)

def validate_json(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                raise APIError('Request must be JSON', 400)

            data = request.get_json()

            try:
                validate(instance=data, schema=schema)
            except ValidationError as e:
                logger.warning(f"Validation error: {str(e)}")
                raise APIError(f"Invalid request: {e.message}", 400)

            return f(*args, **kwargs)
        return wrapper
    return decorator
